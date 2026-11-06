import hashlib
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import urllib.request
from multiprocessing import Process, Queue

import boto3
from botocore.exceptions import ClientError

BUCKET = "nemotron-training-data-us-east-1"
OPS = "ops/english-tokenize-20261102/"
OUT = "tokenized/tok65k-english-v1"
REGION = "us-east-1"
CLAIM_SECS = 30 * 60
HEARTBEAT_SECS = 60
MAX_LOCAL_DL = 5

s3 = boto3.client("s3", region_name=REGION)
sm = boto3.client("secretsmanager", region_name=REGION)
dl_sem = threading.Semaphore(MAX_LOCAL_DL)

PROSE_FIELDS = [
    "persona", "professional_persona", "linguistic_persona", "sports_persona",
    "arts_persona", "travel_persona", "culinary_persona", "cultural_background",
    "linguistic_background", "skills_and_expertise", "hobbies_and_interests",
    "career_goals_and_ambitions",
]


def iid():
    req = urllib.request.Request(
        "http://169.254.169.254/latest/api/token", method="PUT",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "60"})
    tok = urllib.request.urlopen(req, timeout=5).read().decode()
    req = urllib.request.Request(
        "http://169.254.169.254/latest/meta-data/instance-id",
        headers={"X-aws-ec2-metadata-token": tok})
    return urllib.request.urlopen(req, timeout=5).read().decode()


def kh(s):
    return hashlib.sha256(s.encode()).hexdigest()


def task_uid(task):
    u = task["path"]
    if task.get("row_start") or task.get("row_end") is not None:
        u += f":{task.get('row_start', 0)}-{task.get('row_end')}"
    return u


def done_key(task):
    return f"{OUT}/_done/{task['source']}/{kh(task_uid(task))}"


def claim_key(task):
    return OPS + f"claims/{kh(task_uid(task))}"


def exists(key):
    try:
        s3.head_object(Bucket=BUCKET, Key=key)
        return True
    except ClientError:
        return False


def claim(task):
    try:
        s3.put_object(Bucket=BUCKET, Key=claim_key(task), Body=json.dumps(
            {"t": time.time(), "instance": INSTANCE}).encode())
        return True
    except ClientError:
        return False


def heartbeat(state):
    while True:
        try:
            s3.put_object(Bucket=BUCKET, Key=OPS + f"heartbeat/{INSTANCE}.json",
                          Body=json.dumps({**state, "instance": INSTANCE, "t": time.time()}).encode())
        except Exception:
            pass
        time.sleep(HEARTBEAT_SECS)


def get_hf_token():
    return sm.get_secret_value(SecretId="ci1/indic-cc-latin/hf-token")["SecretString"]


CHUNK_THRESHOLD = 2048


def encode_docs(tok, texts):
    """Encode each document whole. Newline splits are not identical to one BPE pass."""
    norm = ["" if t is None else t for t in texts]
    encs = [None] * len(norm)
    short_idx = [i for i, t in enumerate(norm) if len(t) <= CHUNK_THRESHOLD]
    if short_idx:
        encoded = tok.encode_batch([norm[i] for i in short_idx], add_special_tokens=False)
        for i, enc in zip(short_idx, encoded):
            encs[i] = enc.ids
    for i, text in enumerate(norm):
        if encs[i] is None:
            encs[i] = tok.encode(text, add_special_tokens=False).ids
    return encs


def keep_document(ids):
    """Empty rows have no tokens. A leading special id is still a real token."""
    return bool(ids)


def shard_object_keys(out_prefix, work_out, bin_path, index_path):
    """uint16 and the index must be different objects. The index must not replace the bin."""
    bin_key = f"{out_prefix}/{os.path.relpath(bin_path, work_out)}"
    index_key = f"{out_prefix}/{os.path.relpath(index_path, work_out)}"
    if bin_key == index_key:
        raise RuntimeError(f"token bin and index share one key: {bin_key}")
    return bin_key, index_key


def doc_iter(task, rows, cols):
    if task["source"] == "personas-india":
        for r in rows:
            yield "\n\n".join(str(r[f]) for f in PROSE_FIELDS if r[f])
    else:
        col = task["text_col"]
        for r in rows:
            yield r[col]


def process_task(task, workdir):
    import array
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download
    from tokenizers import Tokenizer

    tok = Tokenizer.from_file(os.environ["TOK_PATH"])
    if task["kind"] == "hf":
        with dl_sem:
            token = os.environ.get("HF_TOKEN") or get_hf_token()
            local = hf_hub_download(task["repo"], task["path"], repo_type="dataset",
                                    token=token)
    else:
        local = os.path.join(workdir, "src.parquet")
        s3.download_file(BUCKET, task["key"], local)
    lang = task.get("lang", "en")
    base = os.path.basename(task["path"]).replace(".parquet", "")
    if task.get("row_start") or task.get("row_end") is not None:
        base += f"-r{task.get('row_start', 0)}-{task.get('row_end')}"
    outdir = os.path.join(workdir, "out", task["source"], lang)
    os.makedirs(outdir, exist_ok=True)
    train_ids, val_ids = array.array("H"), array.array("H")
    index, val_index = [], []
    total = docs = dropped = 0
    pf = pq.ParquetFile(local)
    cols = pf.schema_arrow.names
    text_col = task.get("text_col") or ("text" if "text" in cols else "content")
    task["text_col"] = text_col
    id_col = "uuid" if "uuid" in cols else None
    read_cols = sorted(set([text_col] + ([id_col] if id_col else []) + PROSE_FIELDS) & set(cols))
    row_lo = task.get("row_start", 0)
    row_hi = task.get("row_end")
    seen = 0
    for batch in pf.iter_batches(batch_size=20000, columns=read_cols):
        n0 = batch.num_rows
        b_lo = seen
        b_hi = seen + n0
        if b_hi <= row_lo:
            seen = b_hi
            continue
        if row_hi is not None and b_lo >= row_hi:
            break
        lo = max(0, row_lo - b_lo)
        hi = n0 if row_hi is None else min(n0, row_hi - b_lo)
        if lo > 0 or hi < n0:
            batch = batch.slice(lo, hi - lo)
        seen = b_hi
        n = batch.num_rows
        if task["source"] == "personas-india":
            coldata = {}
            for c in PROSE_FIELDS:
                if c in cols:
                    coldata[c] = batch.column(c).to_pylist()
            texts = []
            for i in range(n):
                texts.append("\n\n".join(str(coldata[c][i]) for c in PROSE_FIELDS if c in coldata and coldata[c][i]))
        else:
            texts = batch.column(text_col).to_pylist()
        uids = batch.column(id_col).to_pylist() if id_col else None
        for i, ids in enumerate(encode_docs(tok, texts)):
            if not keep_document(ids):
                dropped += 1
                continue
            uid = uids[i] if uids else f"{task['path']}:{task.get('row_start', 0) + docs + i}"
            rec = {"doc_id": uid, "n_tokens": len(ids), "token_start": total}
            h = hashlib.blake2b(str(uid).encode(), digest_size=8).digest()
            if int.from_bytes(h, "little") % 1000 == 0:
                val_index.append(rec)
                val_ids.extend(ids)
            else:
                index.append(rec)
                train_ids.extend(ids)
            total += len(ids)
        docs += n
    paths = {}
    for suffix, arr, idx in (("", train_ids, index), (".val", val_ids, val_index)):
        p = os.path.join(outdir, base + f".tokens{suffix}.uint16")
        with open(p, "wb") as f:
            arr.tofile(f)
        pi = os.path.join(outdir, base + f".tokens{suffix}.index.jsonl")
        with open(pi, "w") as f:
            for rec in idx:
                f.write(json.dumps(rec) + "\n")
        paths[suffix] = (p, pi)
    work_out = os.path.join(workdir, "out")
    for p, pi in paths.values():
        bin_key, index_key = shard_object_keys(OUT, work_out, p, pi)
        s3.upload_file(p, BUCKET, bin_key)
        s3.upload_file(pi, BUCKET, index_key)
    return {"path": task["path"], "source": task["source"], "lang": lang,
            "docs": docs, "dropped": dropped, "tokens": total,
            "seconds": None, "instance": INSTANCE}


def worker_loop(q, workdir):
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["RAYON_NUM_THREADS"] = "1"
    while True:
        task = q.get()
        if task is None:
            return
        t0 = time.time()
        try:
            stat = process_task(task, workdir)
            stat["seconds"] = round(time.time() - t0, 1)
            s3.put_object(Bucket=BUCKET, Key=done_key(task), Body=json.dumps(stat).encode())
            print(f"DONE {task['source']} {os.path.basename(task['path'])} {stat['tokens']:,} tok {stat['seconds']}s", flush=True)
        except Exception as e:
            print(f"FAIL {task['path']}: {e}", flush=True)
            traceback.print_exc()
        finally:
            try:
                s3.delete_object(Bucket=BUCKET, Key=claim_key(task))
            except ClientError:
                pass
            if task["kind"] == "hf" and "local" in dir():
                pass


def main():
    global INSTANCE
    INSTANCE = iid()
    workdir = sys.argv[1] if len(sys.argv) > 1 else "/work/fleet"
    os.makedirs(workdir, exist_ok=True)
    n_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    state = {"ok": 0, "fail": 0, "phase": "run"}
    threading.Thread(target=heartbeat, args=(state,), daemon=True).start()
    tasks = []
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=OPS + "manifest-v2/"):
        for obj in page.get("Contents", []):
            for line in s3.get_object(Bucket=BUCKET, Key=obj["Key"])["Body"].read().decode().splitlines():
                if line.strip():
                    tasks.append(json.loads(line))
    print(f"manifest: {len(tasks)} tasks", flush=True)
    q = Queue(maxsize=2 * n_workers)
    procs = [Process(target=worker_loop, args=(q, os.path.join(workdir, f"w{i}"))) for i in range(n_workers)]
    for p in procs:
        p.start()
    fed = skipped = 0
    for task in tasks:
        if exists(done_key(task)):
            skipped += 1
            continue
        if exists(claim_key(task)):
            continue
        if not claim(task):
            continue
        q.put(task)
        fed += 1
    for _ in procs:
        q.put(None)
    for p in procs:
        p.join()
    state["phase"] = "done"
    print(f"fleet box done: fed {fed}, skipped {skipped}", flush=True)


if __name__ == "__main__":
    main()
