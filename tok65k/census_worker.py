import json
import os
import sys
import time
import urllib.request
from multiprocessing import Process, Queue

import boto3

BUCKET = "nemotron-training-data-us-east-1"
OPS = "ops/english-tokenize-20261102/census/"
s3 = boto3.client("s3", region_name="us-east-1")

# (source_name, index prefix, is_val_aware)  — every tokenized dataset we have
PREFIXES = [
    ("climbmix", "tokenized/tok65k-climbmix-v4-prefilter/climbmix/"),
    ("math", "tokenized/tok65k-other-dual-v1-shard0/math/"),
    ("math", "tokenized/tok65k-other-dual-v1-shard1/math/"),
    ("code-v2", "tokenized/tok65k-other-dual-v1-shard0/code-v2/"),
    ("code-v2", "tokenized/tok65k-other-dual-v1-shard1/code-v2/"),
    ("codealchemy", "tokenized/tok65k-other-dual-v1-shard0/codealchemy/"),
    ("codealchemy", "tokenized/tok65k-other-dual-v1-shard1/codealchemy/"),
    ("genesis", "tokenized/tok65k-other-dual-v1-shard0/genesis/"),
    ("genesis", "tokenized/tok65k-other-dual-v1-shard1/genesis/"),
    ("rqa", "tokenized/tok65k-other-dual-v1-shard0/rqa/"),
    ("rqa", "tokenized/tok65k-other-dual-v1-shard1/rqa/"),
    ("specialized-v11", "tokenized/tok65k-other-dual-v1-shard0/specialized/"),
    ("specialized-v11", "tokenized/tok65k-other-dual-v1-shard1/specialized/"),
    ("fact-seeking", "tokenized/tok65k-other-dual-v1-shard0/fact-seeking/"),
    ("fact-seeking", "tokenized/tok65k-other-dual-v1-shard1/fact-seeking/"),
    ("infinibyte", "tokenized/tok65k-other-dual-v1-shard0/infinibyte/"),
    ("infinibyte", "tokenized/tok65k-other-dual-v1-shard1/infinibyte/"),
    ("mind", "tokenized/tok65k-other-dual-v1-shard0/mind/"),
    ("mind", "tokenized/tok65k-other-dual-v1-shard1/mind/"),
    ("hq-synth", "tokenized/tok65k-other-dual-v1-shard0/hq-synth/"),
    ("hq-synth", "tokenized/tok65k-other-dual-v1-shard1/hq-synth/"),
    ("fineweb2", "tokenized/tok65k-other-dual-v1-shard0/fineweb2/"),
    ("fineweb2", "tokenized/tok65k-other-dual-v1-shard1/fineweb2/"),
    ("indiccorp-v2", "tokenized/tok65k-other-dual-v1-shard0/indiccorp-v2/"),
    ("indiccorp-v2", "tokenized/tok65k-other-dual-v1-shard1/indiccorp-v2/"),
    ("sangraha-verified", "tokenized/tok65k-other-dual-v1-shard0/sangraha-verified/"),
    ("sangraha-verified", "tokenized/tok65k-other-dual-v1-shard1/sangraha-verified/"),
    ("bhashawiki", "tokenized/tok65k-other-dual-v1-shard0/bhashawiki/"),
    ("bhashawiki", "tokenized/tok65k-other-dual-v1-shard1/bhashawiki/"),
    ("sangraha-synthetic", "tokenized/tok65k-other-dual-v1-shard0/sangraha-synthetic/"),
    ("sangraha-synthetic", "tokenized/tok65k-other-dual-v1-shard1/sangraha-synthetic/"),
    ("sangraha-unverified", "tokenized/tok65k-other-dual-v1-shard0/sangraha-unverified/"),
    ("sangraha-unverified", "tokenized/tok65k-other-dual-v1-shard1/sangraha-unverified/"),
    ("cosmopedia", "tokenized/tok65k-other-dual-v1-shard0/cosmopedia/"),
    ("cosmopedia", "tokenized/tok65k-other-dual-v1-shard1/cosmopedia/"),
    ("fact-seeking-indic", "tokenized/tok65k-other-dual-v1-shard0/fact-seeking-indic/"),
    ("fact-seeking-indic", "tokenized/tok65k-other-dual-v1-shard1/fact-seeking-indic/"),
    ("hq-indic", "tokenized/tok65k-other-dual-v1-shard0/hq-indic/"),
    ("hq-indic", "tokenized/tok65k-other-dual-v1-shard1/hq-indic/"),
    ("ultradata-l3", "tokenized/tok65k-english-v1/ultradata-l3/"),
    ("code-v2-rewriting", "tokenized/tok65k-english-v1/code-v2-rewriting/"),
    ("personas-india", "tokenized/tok65k-english-v1/personas-india/"),
    ("indic-cc", "datasets/nemotron-indic-cc-v1/"),
    ("indic-specialized", "datasets/nemotron-indic-specialized-v1/"),
    ("fineweb2-latn", "datasets/fineweb2-indic/"),
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


def list_index_keys(prefix):
    token = None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": prefix, "MaxKeys": 1000}
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        for o in r.get("Contents", []):
            k = o["Key"]
            # dual-v1 and climbmix indexes are part-*.index.jsonl, not *.tokens.index.jsonl.
            # *.val.index.jsonl also ends with .index.jsonl.
            if k.endswith(".index.jsonl"):
                yield k
        token = r.get("NextContinuationToken")
        if not token:
            return


PAT = None


def count_file(key):
    global PAT
    import re
    if PAT is None:
        PAT = re.compile(rb'"n_tokens":\s*(\d+)|"token_count":\s*(\d+)')
    docs = [0, 0]  # [lt4k, ge4k]
    toks = [0, 0]
    body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    for m in PAT.finditer(body):
        n = int(m.group(1) or m.group(2))
        if n <= 0:
            continue
        b = 0 if n < 4096 else 1
        docs[b] += 1
        toks[b] += n
    return docs, toks


def worker(q, out_q):
    while True:
        item = q.get()
        if item is None:
            return
        src, key = item
        try:
            docs, toks = count_file(key)
            out_q.put((src, key, docs, toks, ".val." in key or ".tokens.val." in key))
        except Exception as e:
            out_q.put((src, key, "ERR", str(e)[:200], False))


def main():
    instance = iid()
    # build the task list: all index keys under all prefixes, skipping ones with a done part
    done = set()
    for obj in s3.list_objects_v2(Bucket=BUCKET, Prefix=OPS + "parts/").get("Contents", []):
        done.add(obj["Key"].rsplit("/", 1)[-1])
    import hashlib
    N_SHARDS = int(os.environ.get("N_SHARDS", "1"))
    my_shard = int(instance[-1], 16) % N_SHARDS
    tasks = []
    for src, prefix in PREFIXES:
        n0 = len(tasks)
        for key in list_index_keys(prefix):
            h = hashlib.sha256(key.encode()).hexdigest()
            if h in done:
                continue
            if int(h[0], 16) % N_SHARDS != my_shard:
                continue
            tasks.append((src, key))
        print(f"{src}: +{len(tasks) - n0} index files", flush=True)
    print(f"shard {my_shard}/{N_SHARDS}", flush=True)
    print(f"total tasks: {len(tasks)}", flush=True)
    q = Queue(maxsize=256)
    out_q = Queue()
    procs = [Process(target=worker, args=(q, out_q)) for _ in range(40)]
    for p in procs:
        p.start()
    for t in tasks:
        q.put(t)
    for _ in procs:
        q.put(None)
    import hashlib
    agg = {}
    errs = 0
    done_n = 0
    while done_n < len(tasks):
        src, key, docs, toks, is_val = out_q.get()
        done_n += 1
        if docs == "ERR":
            errs += 1
            continue
        a = agg.setdefault(src, [[0, 0], [0, 0]])
        a[0][0] += docs[0]
        a[0][1] += docs[1]
        a[1][0] += toks[0]
        a[1][1] += toks[1]
        s3.put_object(Bucket=BUCKET,
                      Key=OPS + f"parts/{hashlib.sha256(key.encode()).hexdigest()}",
                      Body=b"1")
        if done_n % 2000 == 0:
            print(f"{done_n}/{len(tasks)} files, {errs} errors, instance {instance}", flush=True)
    for p in procs:
        p.join()
    s3.put_object(Bucket=BUCKET, Key=OPS + f"by-worker/{instance}.json",
                  Body=json.dumps({"agg": agg, "files": len(tasks), "errors": errs}).encode())
    print(f"DONE {instance}: {errs} errors", flush=True)


if __name__ == "__main__":
    main()
