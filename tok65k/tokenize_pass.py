"""Tokenize the training sources, including ClimbMix after a fast junk filter.

Writes s3://nemotron-training-data-us-east-1/tokenized/tok65k/.
ClimbMix documents that fail the web-junk checks are encoded so their
tokens can be counted, then left out of the bins. translation-staging,
Latin-script Sangraha, English Sangraha, and languages outside the seven
are not listed.
"""

from __future__ import annotations

import argparse
import array
import gzip
import hashlib
import json
import os
import re
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Process, Queue

import boto3
import pyarrow.fs as pafs
import pyarrow.parquet as pq
from botocore.exceptions import ClientError
from tokenizers import Tokenizer

BUCKET = "nemotron-training-data-us-east-1"
REGION = "us-east-1"
OUT_PREFIX = "tokenized/tok65k"
MAX_TOKENS = 1_000_000_000
MAX_DOCS = 100_000
BATCH = 256

LANG_CODES = {
    "hin": "hin",
    "hin_Deva": "hin",
    "hi": "hin",
    "ben": "ben",
    "ben_Beng": "ben",
    "bn": "ben",
    "tam": "tam",
    "tam_Taml": "tam",
    "ta": "tam",
    "tel": "tel",
    "tel_Telu": "tel",
    "te": "tel",
    "kan": "kan",
    "kan_Knda": "kan",
    "kn": "kan",
    "mar": "mar",
    "mar_Deva": "mar",
    "mr": "mar",
    "guj": "guj",
    "guj_Gujr": "guj",
    "gu": "guj",
}
ID_COLS = (
    "doc_id",
    "document_id",
    "uuid",
    "id",
    "blob_id",
    "nemotron_pretraining_id",
)

V5 = "translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v5-20260906/"
V4 = "translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v4-20260905/"
HQIN = "translations/Cosmopedia-v2/Krutrim/krutrim-nemotron-cc-v21-hq-synth-v1-20260906/"
FSIN = (
    "translations/Nemotron-Pretraining-Specialized-v1.2/Fact-Seeking/"
    "indictrans2-en-indic-dist-200M-beam1-20260902/"
    "fact-seeking-70shard-10lang-r16-20260903/"
)
SEVEN_FOLDERS = (
    "hin/",
    "ben/",
    "tam/",
    "tel/",
    "kan/",
    "mar/",
    "guj/",
)
SEVEN_DEVA = (
    "hin_Deva/",
    "ben_Beng/",
    "tam_Taml/",
    "tel_Telu/",
    "kan_Knda/",
    "mar_Deva/",
    "guj_Gujr/",
)
BHASHA_FOLDERS = (
    "hin_Deva/",
    "ben_Beng/",
    "tam_Taml/",
    "kan_Knda/",
    "guj_Gujr/",
)
V5_LANGS = ("kan_Knda/", "mar_Deva/")
V4_LANGS = ("hin_Deva/", "ben_Beng/", "tam_Taml/", "tel_Telu/", "guj_Gujr/")
HQ_LANGS = ("hin_Deva/", "ben_Beng/", "tam_Taml/", "tel_Telu/", "mar_Deva/", "guj_Gujr/")


def sources():
    """Training sources. ClimbMix is first so workers start on it immediately."""
    rows = [
        ("climbmix", ["datasets/nemotron-climbmix/karpathy-400b-shuffle/"], "parquet", "en", False, "mod", 8000, 400),
        ("math", ["datasets/nemotron-cc-math-v1/4plus/"], "parquet", "en", False, "mod", 10000, 52),
        ("mind", ["datasets/nemotron-cc-math-v1/4plus_MIND/"], "parquet", "en", False, "docs", None, 35),
        ("rqa", ["datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-RQA/"], "parquet", "en", False, "docs", None, 10),
        ("fact-seeking", ["datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/"], "parquet", "en", False, "docs", None, 5),
        ("specialized", ["datasets/Nemotron-Pretraining-Specialized-v1.1/"], "parquet", "en", False, "docs", None, 9),
        ("codealchemy", ["datasets/codealchemy/"], "parquet", "en", True, "mod", 8000, 40),
        ("code-v2", ["datasets/nemotron-code-v2/"], "parquet", "en", True, "mod", 9000, 45),
        ("hq-synth", ["translations/Cosmopedia-v2/Krutrim/source-snapshots/Nemotron-CC-v2.1/High-Quality-Synthetic/"], "parquet", "en", False, "mod", 500, 50),
        ("genesis", ["datasets/genesis-iii/"], "parquet", "en", True, "mod", 10400, 52),
        ("infinibyte", ["datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-InfiniByte-Reasoning/"], "parquet", "en", False, "docs", None, 19),
        ("sangraha-verified", [f"datasets/sangraha/verified/{name}" for name in SEVEN_FOLDERS], "parquet", "path", False, "docs", None, None),
        ("sangraha-synthetic", [f"datasets/sangraha/synthetic/{name}" for name in SEVEN_DEVA], "parquet", "path", False, "docs", None, None),
        ("sangraha-unverified", [f"datasets/sangraha/unverified/{name}" for name in SEVEN_FOLDERS], "parquet", "path", False, "docs", None, None),
        ("fineweb2", [f"datasets/fineweb2-indic/{name}" for name in SEVEN_DEVA], "parquet", "path", False, "docs", None, 13.32),
        ("indiccorp-v2", [f"datasets/indiccorp-v2/{name}" for name in SEVEN_DEVA], "text", "path", True, "docs", None, 13.80),
        ("bhashawiki", [f"datasets/bhashawiki/{name}" for name in BHASHA_FOLDERS], "parquet", "path", True, "docs", None, 13.61),
        ("cosmopedia", [V5 + "language=" + name for name in V5_LANGS] + [V4 + "language=" + name for name in V4_LANGS], "translation", "path", False, "docs", None, 33.49),
        ("hq-indic", [HQIN + "language=" + name for name in HQ_LANGS], "translation", "path", False, "docs", None, 10.83),
        ("fact-seeking-indic", [FSIN + "language=" + name for name in SEVEN_DEVA], "translation", "path", False, "docs", None, 20.41),
    ]
    out = []
    for name, prefixes, kind, lang, gzip_copy, val_mode, modulus, sheet in rows:
        out.append(
            {
                "name": name,
                "prefixes": prefixes,
                "kind": kind,
                "lang": lang,
                "gzip_copy": gzip_copy,
                "val_mode": val_mode,
                "modulus": modulus,
                "sheet": sheet,
                "web_filter": name == "climbmix",
            }
        )
    return out


def s3_client():
    return boto3.client("s3", region_name=REGION)


def list_keys(s3, prefix):
    token = None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": prefix, "MaxKeys": 1000}
        if token:
            kw["ContinuationToken"] = token
        resp = s3.list_objects_v2(**kw)
        for obj in resp.get("Contents") or []:
            yield obj["Key"], int(obj["Size"])
        if not resp.get("IsTruncated"):
            return
        token = resp["NextContinuationToken"]


def is_data(key, kind):
    if "gzip6/" in key or "translation-staging/" in key or "/_parts/" in key:
        return False
    if "_Latn/" in key or key.startswith("datasets/sangraha/verified/eng/"):
        return False
    base = key.rsplit("/", 1)[-1]
    if kind == "translation":
        return base == "translated_documents.parquet"
    if kind == "text":
        return base.endswith(".txt")
    return base.endswith(".parquet") and not base.endswith(".ratios.parquet")


def lang_from_key(key):
    for part in key.split("/"):
        part = part.removeprefix("language=")
        if part in LANG_CODES:
            return LANG_CODES[part]
    return None


def blake64(text):
    digest = hashlib.blake2b(text.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big")


_LOREM = re.compile(r"lorem ipsum", re.I)
_ECOM = re.compile(
    r"customers who bought|customers also bought|people also viewed|"
    r"add to cart|frequently bought together|our editors recommend",
    re.I,
)
_BOILER = re.compile(
    r"privacy policy|terms of use|terms and conditions|cookie policy|"
    r"all rights reserved|skip to content|back to top|follow us",
    re.I,
)
_TRUNC = re.compile(r"\bread more\b|\bcontinue reading\b|\bclick here\b", re.I)
_CODE = re.compile(
    r"(?m)^[ \t]*(?:def |class |import |from |function |#include |public |private |"
    r"const |let |var |return |package |fn |func )"
)
_MATH = re.compile(r"\\frac\{|\\sum_|\\int_|\\begin\{equation\}|\\\[")
_CAMEL = re.compile(r"\b[a-z]{2,}[A-Z][a-zA-Z]{2,}\b")
_BULLET = re.compile(r"^\s*(?:[-*•]|\d{1,3}[.)])\s+\S")
_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_STOPWORDS = frozenset(
    """
    the a an and or of to in for on with at by from as is was are were be been being
    it this that these those i you he she we they not but if so than then into over
    after before about between out up down off too very can will just do does did
    has have had its their his her our your my me them which who what when where
    why how there here all any some no nor
    """.split()
)


def climbmix_reason(text):
    """High-precision web-junk label, or None when the document stays.

    The keep path only splits words and scans a short sample. Heavier
    checks run after a cheap hint, so ordinary pages stay cheap.
    Code-like and math-like documents skip the prose rules.
    """
    n_chars = len(text)
    if n_chars > 500_000:
        return "too_long"
    probe = text if n_chars <= 4000 else text[:2500] + "\n" + text[-1500:]
    low = probe.lower()
    if "lorem ipsum" in low:
        return "lorem_ipsum"
    if any(ch < " " and ch not in "\n\r\t" for ch in probe):
        bad = sum(ch < " " and ch not in "\n\r\t" for ch in probe)
        if bad * 100 > len(probe):
            return "control_chars"

    words = text.split()
    n_words = len(words)
    if n_words > 100_000:
        return "too_long"
    head = text[:2500]
    codeish = (
        "\\frac{" in head
        or "\\sum_" in head
        or "\\int_" in head
        or head.lstrip().startswith(
            ("def ", "class ", "import ", "from ", "#include", "function ", "fn ", "func ", "public ", "const ")
        )
        or "\ndef " in head
        or "\nclass " in head
        or "\nimport " in head
        or "\nfunction " in head
    )
    if codeish:
        if n_words < 15 and n_chars < 80:
            return "too_short"
    elif n_words < 50:
        return "too_short"

    if any(
        hint in low
        for hint in (
            "bought",
            "add to cart",
            "privacy",
            "terms of",
            "cookie",
            "click here",
            "read more",
            "continue reading",
            "rights reserved",
            "skip to content",
            "back to top",
            "follow us",
        )
    ):
        if _ECOM.search(low) and (len(_ECOM.findall(low)) >= 2 or n_words < 800):
            return "ecommerce"
        boiler = _BOILER.findall(low)
        if len(boiler) >= 4 or (len(boiler) >= 2 and n_words < 350):
            return "boilerplate"
        trunc = _TRUNC.findall(low)
        if len(trunc) >= 3 or (len(trunc) >= 2 and n_words < 250):
            return "truncation"

    if text.count("\n") >= 8:
        lines = text.splitlines()
        nonempty = [line for line in lines if line.strip()]
        n_non = len(nonempty)
        if n_non:
            ellipsis = short = terminal = bullets = dup = 0
            seen = set()
            for line in nonempty:
                stripped = line.strip()
                if len(stripped) < 30:
                    short += 1
                if stripped.endswith(("...", "…")):
                    ellipsis += 1
                elif stripped.endswith((".", "?", "!")):
                    terminal += 1
                if _BULLET.match(line) or (" " not in stripped and len(stripped) < 20):
                    bullets += 1
                if stripped in seen:
                    dup += 1
                else:
                    seen.add(stripped)
            if ellipsis >= 4 and ellipsis / n_non > 0.15:
                return "truncation"
            if n_non >= 12 and dup / n_non > 0.55:
                return "repeated_lines"
            if not codeish and n_non >= 8:
                short_frac = short / n_non
                if short_frac > 0.75:
                    return "short_lines"
                if terminal / n_non < 0.08 and short_frac > 0.50:
                    return "low_terminal"
                total_lines = len(lines)
                blanks = total_lines - n_non
                if total_lines >= 10 and blanks / total_lines > 0.55:
                    return "blank_lines"
                if bullets / n_non > 0.70:
                    return "list_junk"
    if codeish:
        return None

    if n_words >= 20:
        take = words if n_words <= 300 else words[:300]
        avg = sum(len(word) for word in take) / len(take)
        if avg < 2.5 or avg > 18:
            return "word_length"
        if n_chars >= 200:
            sample = text if n_chars <= 1500 else text[:1500]
            letters = sum(ch.isalpha() for ch in sample)
            if letters / len(sample) < 0.40:
                return "non_alpha"
            symbols = sum(ch in "#*_=~`|<>[]{}\\" for ch in sample)
            if symbols / len(sample) > 0.18:
                return "symbol_ratio"

    if n_words >= 80:
        take = words if n_words <= 1500 else words[:1500]
        counts = {}
        top = 0
        for word in take:
            count = counts.get(word, 0) + 1
            counts[word] = count
            if count > top:
                top = count
        if top >= 25 and top / len(take) > 0.08:
            gcounts = {}
            gtop = 0
            last = min(len(take) - 7, 600)
            for i in range(0, last, 2):
                gram = (take[i], take[i + 3], take[i + 7])
                count = gcounts.get(gram, 0) + 1
                gcounts[gram] = count
                if count > gtop:
                    gtop = count
            if gtop >= 6:
                return "ngram_repetition"

    if n_words >= 40:
        upper = letters = ascii_letters = stops = bare = checked = 0
        for word in words[:120]:
            checked += 1
            core = word.strip(".,;:!?\"'()[]{}")
            if not core or not any(ch.isalpha() for ch in core):
                bare += 1
                continue
            if core.lower() in _STOPWORDS:
                stops += 1
            for ch in core:
                if not ch.isalpha():
                    continue
                letters += 1
                if ch.isupper():
                    upper += 1
                if ch.isascii():
                    ascii_letters += 1
        if checked and bare / checked > 0.45:
            return "symbol_tokens"
        if letters > 40 and upper / letters > 0.65:
            return "all_caps"
        if letters and ascii_letters > 0.85 * letters and stops < 4:
            return "low_stopwords"
        if _CAMEL.search(head) and len(_CAMEL.findall(head)) >= 8:
            return "camel_case"
    return None



def gzip_ratio(data):
    if len(data) < 512:
        return None, "mid"
    ratio = len(gzip.compress(data, compresslevel=6, mtime=0)) / len(data)
    if ratio < 0.35:
        return ratio, "easy"
    if ratio <= 0.65:
        return ratio, "mid"
    return ratio, "hard"


def ratios_key(source_key):
    parts = source_key.split("/")
    root = "/".join(parts[:2])
    rest = "/".join(parts[2:])
    return f"{root}/gzip6/{rest}.ratios.parquet"


def key_hash(key):
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def done_set(s3):
    found = set()
    for key, _size in list_keys(s3, OUT_PREFIX + "/_done/"):
        found.add(key.rsplit("/", 1)[-1])
    return found


def parquet_rows(key):
    s3fs = pafs.S3FileSystem(region=REGION)
    pf = pq.ParquetFile(s3fs.open_input_file(f"{BUCKET}/{key}"))
    rows = pf.metadata.num_rows
    pf.close() if hasattr(pf, "close") else None
    return rows


def text_docs(s3, key):
    meta_key = ratios_key(key) + ".meta.json"
    try:
        body = s3.get_object(Bucket=BUCKET, Key=meta_key)["Body"].read()
    except ClientError:
        return 100_000
    return int(json.loads(body).get("docs") or 100_000)


def make_task(source, lang, key, size, modulus):
    return {
        "source": source["name"],
        "kind": source["kind"],
        "gzip_copy": source["gzip_copy"],
        "web_filter": source["web_filter"],
        "lang": lang,
        "modulus": modulus,
        "sheet": source["sheet"],
        "key": key,
        "size": size,
    }


def list_source(s3, source):
    listed = []
    for prefix in source["prefixes"]:
        for key, size in list_keys(s3, prefix):
            if not is_data(key, source["kind"]):
                continue
            lang = source["lang"] if source["lang"] != "path" else lang_from_key(key)
            if lang is None:
                continue
            listed.append((lang, key, size))
    return listed


def count_rows(source, lang, key):
    if source["kind"] == "text":
        return source["name"], lang, text_docs(s3_client(), key)
    try:
        return source["name"], lang, parquet_rows(key)
    except Exception as exc:
        print(f"count failed {key}: {exc}", flush=True)
        return source["name"], lang, 0


def feed_tasks(s3, source_rows, done, max_files, queue, counts):
    """Queue fixed-modulus sources first, then sources that need a row count."""
    queued = 0

    def emit(task):
        nonlocal queued
        if max_files and queued >= max_files:
            return False
        if key_hash(task["key"]) in done:
            return True
        queue.put(task)
        queued += 1
        return True

    doc_rows = []
    for source in source_rows:
        listed = list_source(s3, source)
        print(f"listed {source['name']} files={len(listed)}", flush=True)
        if source["val_mode"] == "mod":
            for lang, key, size in listed:
                if not emit(make_task(source, lang, key, size, source["modulus"])):
                    print(f"queued {queued}", flush=True)
                    return
            continue
        doc_rows.append((source, listed))

    pending = []
    for source, listed in doc_rows:
        for lang, key, size in listed:
            if key_hash(key) in done:
                continue
            pending.append((source, lang, key, size))
    if pending:
        with ThreadPoolExecutor(max_workers=32) as pool:
            futures = [pool.submit(count_rows, source, lang, key) for source, lang, key, _size in pending]
            for fut in as_completed(futures):
                name, lang, n = fut.result()
                counts[(name, lang)] = counts.get((name, lang), 0) + n
    for source, listed in doc_rows:
        by_lang = {}
        for lang, _key, _size in listed:
            by_lang.setdefault(lang, counts.get((source["name"], lang), 0))
        for lang, total in by_lang.items():
            if total >= 10_000:
                modulus = max(total // 2000, 1)
            elif total > 0:
                modulus = 20
            else:
                modulus = 20
                print(f"count missing for {source['name']} {lang}; using 5% val", flush=True)
            for item_lang, key, size in listed:
                if item_lang != lang:
                    continue
                if not emit(make_task(source, item_lang, key, size, modulus)):
                    print(f"queued {queued}", flush=True)
                    return
    print(f"queued {queued}", flush=True)


def choose_text(names, source_name):
    if source_name == "code-v2":
        if "content" not in names:
            raise RuntimeError("code-v2 file has no content column")
        return "content"
    if source_name in ("cosmopedia", "hq-indic", "fact-seeking-indic"):
        if "translation" not in names:
            raise RuntimeError("translation file has no translation column")
        return "translation"
    if source_name == "codealchemy":
        if "text" in names:
            return "text"
        if "text_with_placeholders" in names:
            return "text_with_placeholders"
        raise RuntimeError("codealchemy file has no text column")
    if "text" not in names:
        raise RuntimeError("file has no text column")
    return "text"


def as_str(value):
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if isinstance(value, str):
        return value
    return str(value)


def load_quarantine(s3, parquet_key):
    qkey = parquet_key.rsplit("/", 1)[0] + "/quarantine_manifest.jsonl"
    try:
        body = s3.get_object(Bucket=BUCKET, Key=qkey)["Body"].read()
    except ClientError as exc:
        code = exc.response["Error"].get("Code", "")
        if code in ("NoSuchKey", "404", "NotFound"):
            return set()
        raise
    found = set()
    for line in body.splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if "document_id" in rec and rec["document_id"] is not None:
            found.add(str(rec["document_id"]))
    return found


def load_ratios(source_key):
    rkey = ratios_key(source_key)
    s3fs = pafs.S3FileSystem(region=REGION)
    try:
        pf = pq.ParquetFile(s3fs.open_input_file(f"{BUCKET}/{rkey}"))
        table = pf.read(columns=["doc_index", "utf8_bytes", "ratio", "band"])
    except Exception:
        return None
    by_index = {}
    doc_index = table.column("doc_index").to_pylist()
    utf8_bytes = table.column("utf8_bytes").to_pylist()
    ratio = table.column("ratio").to_pylist()
    band = table.column("band").to_pylist()
    for i in range(table.num_rows):
        if doc_index[i] is None or utf8_bytes[i] is None or ratio[i] is None or band[i] is None:
            continue
        by_index[int(doc_index[i])] = {
            "utf8_bytes": int(utf8_bytes[i]),
            "ratio": float(ratio[i]),
            "band": str(band[i]),
        }
    return by_index


class PartWriter:
    def __init__(self, s3, source, lang, khash, split, tmpdir):
        self.s3 = s3
        self.source = source
        self.lang = lang
        self.khash = khash
        self.split = split
        self.tmpdir = tmpdir
        self.part_i = 0
        self.tokens = 0
        self.docs = 0
        self.buf = bytearray()
        self.lines = []
        self.uploaded = []

    def add(self, ids, record):
        n = len(ids)
        if self.docs and (self.tokens + n > MAX_TOKENS or self.docs >= MAX_DOCS):
            self.flush()
        record["token_start"] = self.tokens
        record["n_tokens"] = n
        self.buf += array.array("H", ids).tobytes()
        self.tokens += n
        self.docs += 1
        self.lines.append(record)

    def flush(self):
        if self.docs == 0:
            return
        suffix = ".val" if self.split == "val" else ""
        base = f"{OUT_PREFIX}/{self.source}/{self.lang}/part-{self.khash}-{self.part_i:02d}{suffix}"
        raw = bytes(self.buf)
        digest = hashlib.sha256(raw).hexdigest()
        index = "".join(json.dumps(rec, ensure_ascii=False) + "\n" for rec in self.lines).encode("utf-8")
        bin_path = os.path.join(self.tmpdir, f"{self.part_i}{suffix}.uint16")
        idx_path = bin_path + ".index.jsonl"
        for path, payload in ((bin_path, raw), (idx_path, index)):
            with open(path, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
        self.s3.upload_file(bin_path, BUCKET, base + ".uint16")
        self.s3.upload_file(idx_path, BUCKET, base + ".index.jsonl")
        os.remove(bin_path)
        os.remove(idx_path)
        self.uploaded.append(
            {
                "uint16": base + ".uint16",
                "index": base + ".index.jsonl",
                "sha256": digest,
                "n_tokens": self.tokens,
                "n_docs": self.docs,
                "split": self.split,
            }
        )
        self.part_i += 1
        self.tokens = 0
        self.docs = 0
        self.buf = bytearray()
        self.lines = []


def illegal_ids(ids):
    return bool(ids) and (min(ids) < 32 or max(ids) > 65535)


def iter_parquet_rows(key, columns):
    s3fs = pafs.S3FileSystem(region=REGION)
    pf = pq.ParquetFile(s3fs.open_input_file(f"{BUCKET}/{key}"))
    names = list(pf.schema_arrow.names)
    row = 0
    for batch in pf.iter_batches(batch_size=BATCH, columns=columns):
        cols = {name: batch.column(name).to_pylist() for name in columns}
        n = batch.num_rows
        for i in range(n):
            yield row, {name: cols[name][i] for name in columns}
            row += 1
    return names


def parquet_names(key):
    s3fs = pafs.S3FileSystem(region=REGION)
    pf = pq.ParquetFile(s3fs.open_input_file(f"{BUCKET}/{key}"))
    return list(pf.schema_arrow.names)


def iter_lines(s3, key):
    body = s3.get_object(Bucket=BUCKET, Key=key)["Body"]
    buf = b""
    first = True
    line_no = 0
    for chunk in body.iter_chunks(chunk_size=8 * 1024 * 1024):
        if first:
            first = False
            if chunk.startswith(b"\xef\xbb\xbf"):
                chunk = chunk[3:]
        buf += chunk
        while True:
            cut = buf.find(b"\n")
            if cut < 0:
                break
            raw = buf[:cut]
            buf = buf[cut + 1 :]
            if raw.endswith(b"\r"):
                raw = raw[:-1]
            line_no += 1
            yield line_no, raw.decode("utf-8")
    if buf:
        line_no += 1
        yield line_no, buf.decode("utf-8")


def process_task(task, tok, s3, tmpdir, stop_path):
    if os.path.exists(stop_path):
        raise SystemExit("stop file present")
    key = task["key"]
    khash = key_hash(key)
    source = task["source"]
    lang = task["lang"]
    dropped = {}
    kept = 0
    train_tokens = 0
    val_tokens = 0
    kept_bytes = 0
    removed_tokens = {}
    logged_illegal = False
    t0 = time.time()

    def drop(reason):
        dropped[reason] = dropped.get(reason, 0) + 1

    train = PartWriter(s3, source, lang, khash, "train", tmpdir)
    val = PartWriter(s3, source, lang, khash, "val", tmpdir)
    pending_text = []
    pending_meta = []
    pending_drop_text = []
    pending_drop_reason = []

    def flush_drops():
        if not pending_drop_text:
            return
        encoded = tok.encode_batch(pending_drop_text, add_special_tokens=False)
        for enc, reason in zip(encoded, pending_drop_reason):
            ids = list(enc.ids)
            removed_tokens[reason] = removed_tokens.get(reason, 0) + len(ids)
            drop(reason)
        pending_drop_text.clear()
        pending_drop_reason.clear()

    def flush_encode():
        nonlocal kept, train_tokens, val_tokens, kept_bytes, logged_illegal
        if not pending_text:
            return
        encoded = tok.encode_batch(pending_text, add_special_tokens=False)
        for enc, meta in zip(encoded, pending_meta):
            ids = list(enc.ids)
            if illegal_ids(ids):
                removed_tokens["illegal_id"] = removed_tokens.get("illegal_id", 0) + len(ids)
                drop("illegal_id")
                if not logged_illegal:
                    logged_illegal = True
                    print(
                        f"drop illegal_id {key} doc {meta['doc_id']} n_tokens={len(ids)}",
                        flush=True,
                    )
                continue
            record = {
                "doc_id": meta["doc_id"],
                "row_key": meta["row_key"],
                "n_bytes": meta["n_bytes"],
                "gzip_ratio": meta["gzip_ratio"],
                "compression_band": meta["compression_band"],
                "parquet_key": key,
            }
            writer = val if meta["is_val"] else train
            writer.add(ids, record)
            if meta["is_val"]:
                val_tokens += len(ids)
            else:
                train_tokens += len(ids)
            kept += 1
            kept_bytes += meta["n_bytes"]
        pending_text.clear()
        pending_meta.clear()

    ratios = load_ratios(key) if task["gzip_copy"] else None
    nonempty_i = 0

    def consider(row_id, text, doc_raw):
        nonlocal nonempty_i
        if text is None or text.strip() == "":
            drop("empty")
            return
        doc_id = as_str(doc_raw) if doc_raw is not None else f"{key}:{row_id}"
        if task.get("web_filter"):
            reason = climbmix_reason(text)
            if reason:
                pending_drop_text.append(text)
                pending_drop_reason.append(reason)
                if len(pending_drop_text) >= BATCH:
                    flush_drops()
                return
        raw = text.encode("utf-8")
        n_bytes = len(raw)
        nonempty_i += 1
        ratio = None
        band = None
        if ratios is not None:
            rec = ratios.get(row_id)
            if rec is None or rec["utf8_bytes"] != n_bytes:
                rec = ratios.get(nonempty_i - 1)
                if rec is not None and rec["utf8_bytes"] != n_bytes:
                    rec = None
            if rec is not None and rec["band"] in ("easy", "mid", "hard"):
                ratio = rec["ratio"]
                band = rec["band"]
                if n_bytes < 512:
                    band = "mid"
        if band is None:
            ratio, band = gzip_ratio(raw)
        is_val = blake64(doc_id) % task["modulus"] == 0
        pending_text.append(text)
        pending_meta.append(
            {
                "doc_id": doc_id,
                "row_key": f"{key}:{row_id}",
                "n_bytes": n_bytes,
                "gzip_ratio": ratio,
                "compression_band": band,
                "is_val": is_val,
            }
        )
        if len(pending_text) >= BATCH:
            flush_encode()

    if task["kind"] == "text":
        for line_no, text in iter_lines(s3, key):
            consider(line_no, text, None)
    else:
        names = parquet_names(key)
        if source == "genesis" and "pipeline" not in names:
            rows = parquet_rows(key)
            dropped["no_pipeline"] = rows
        else:
            text_col = choose_text(names, source)
            columns = [text_col]
            id_col = next((col for col in ID_COLS if col in names), None)
            if id_col:
                columns.append(id_col)
            if source == "genesis":
                columns.append("pipeline")
            quarantine = load_quarantine(s3, key) if task["kind"] == "translation" else set()
            for row, values in iter_parquet_rows(key, columns):
                if source == "genesis" and as_str(values.get("pipeline")) != "option_level":
                    drop("pipeline")
                    continue
                doc_raw = values.get(id_col) if id_col else None
                if quarantine and doc_raw is not None and str(as_str(doc_raw)) in quarantine:
                    drop("quarantine")
                    continue
                consider(row, as_str(values.get(text_col)), doc_raw)
    flush_drops()
    flush_encode()
    train.flush()
    val.flush()
    parts = train.uploaded + val.uploaded
    body = {
        "key": key,
        "source": source,
        "lang": lang,
        "object_bytes": task["size"],
        "kept_bytes": kept_bytes,
        "documents_kept": kept,
        "documents_dropped": dropped,
        "tokens_removed": sum(removed_tokens.values()),
        "tokens_removed_by_reason": removed_tokens,
        "train_tokens": train_tokens,
        "val_tokens": val_tokens,
        "parts": parts,
        "modulus": task["modulus"],
        "sheet_billions": task["sheet"],
        "seconds": round(time.time() - t0, 3),
    }
    s3.put_object(
        Bucket=BUCKET,
        Key=f"{OUT_PREFIX}/_done/{source}/{khash}",
        Body=json.dumps(body).encode("utf-8"),
    )
    print(
        f"done {source}/{lang} kept={kept} train_tokens={train_tokens} "
        f"val_tokens={val_tokens} tokens_removed={sum(removed_tokens.values())} "
        f"removed_by_reason={removed_tokens} dropped={dropped} {key}",
        flush=True,
    )
    return body


def append_line(path, obj):
    import fcntl

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.write(json.dumps(obj) + "\n")
        handle.flush()
        fcntl.flock(handle, fcntl.LOCK_UN)


def worker(queue, tok_path, tmp_root, stop_path, progress_path):
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["RAYON_NUM_THREADS"] = "1"
    tok = Tokenizer.from_file(tok_path)
    tok.no_truncation()
    probe = tok.encode("hello", add_special_tokens=False).ids
    if not probe or min(probe) < 32 or max(probe) > 65535:
        raise SystemExit(f"tokenizer self-check failed: {probe[:8]}")
    s3 = s3_client()
    os.makedirs(tmp_root, exist_ok=True)
    fail_path = os.path.join(os.path.dirname(progress_path), "fails.jsonl")
    while True:
        task = queue.get()
        if task is None:
            return
        if os.path.exists(stop_path):
            return
        tmpdir = os.path.join(tmp_root, key_hash(task["key"])[:12])
        os.makedirs(tmpdir, exist_ok=True)
        body = None
        try:
            last_error = None
            for attempt in range(3):
                try:
                    body = process_task(task, tok, s3, tmpdir, stop_path)
                    last_error = None
                    break
                except SystemExit:
                    raise
                except Exception as exc:
                    last_error = exc
                    traceback.print_exc()
                    print(f"retry {attempt + 1} {task['key']}: {exc}", flush=True)
                    time.sleep(2 ** attempt)
            if last_error is not None:
                append_line(fail_path, {"key": task["key"], "error": str(last_error)})
                print(f"FAIL {task['key']}", flush=True)
                continue
        except SystemExit as exc:
            with open(stop_path, "w", encoding="utf-8") as handle:
                handle.write(str(exc))
            print(f"STOP {exc}", flush=True)
            raise
        finally:
            if os.path.isdir(tmpdir):
                for name in os.listdir(tmpdir):
                    try:
                        os.remove(os.path.join(tmpdir, name))
                    except OSError:
                        pass
        append_line(progress_path, body)


def chunked(items, n):
    buckets = [[] for _ in range(n)]
    for i, item in enumerate(items):
        buckets[i % n].append(item)
    return [bucket for bucket in buckets if bucket]


def publish_manifest(s3, progress_path, tok_sha, counts):
    grouped = {}
    parts = []
    if os.path.exists(progress_path):
        with open(progress_path, encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                slot = grouped.setdefault(
                    (rec["source"], rec["lang"]),
                    {
                        "object_bytes": 0,
                        "kept_bytes": 0,
                        "documents_kept": 0,
                        "documents_dropped": {},
                        "tokens_removed": 0,
                        "tokens_removed_by_reason": {},
                        "train_tokens": 0,
                        "val_tokens": 0,
                        "files": 0,
                        "sheet_billions": rec.get("sheet_billions"),
                    },
                )
                slot["object_bytes"] += rec["object_bytes"]
                slot["kept_bytes"] += rec["kept_bytes"]
                slot["documents_kept"] += rec["documents_kept"]
                slot["train_tokens"] += rec["train_tokens"]
                slot["val_tokens"] += rec["val_tokens"]
                slot["tokens_removed"] += rec.get("tokens_removed") or 0
                slot["files"] += 1
                for reason, n in rec["documents_dropped"].items():
                    slot["documents_dropped"][reason] = slot["documents_dropped"].get(reason, 0) + n
                for reason, n in (rec.get("tokens_removed_by_reason") or {}).items():
                    bucket = slot["tokens_removed_by_reason"]
                    bucket[reason] = bucket.get(reason, 0) + n
                parts.extend(rec["parts"])
    removed = {}
    removed_total = 0
    for slot in grouped.values():
        removed_total += slot["tokens_removed"]
        for reason, n in slot["tokens_removed_by_reason"].items():
            removed[reason] = removed.get(reason, 0) + n
    manifest = {
        "tokenizer_sha256": tok_sha,
        "web_filter": ["climbmix"],
        "tokens_removed": removed_total,
        "tokens_removed_by_reason": removed,
        "row_counts": {f"{name}/{lang}": n for (name, lang), n in counts.items()},
        "sources": {
            f"{name}/{lang}": slot for (name, lang), slot in sorted(grouped.items())
        },
        "parts": parts,
        "updated_unix": time.time(),
    }
    s3.put_object(
        Bucket=BUCKET,
        Key=f"{OUT_PREFIX}/manifest.json",
        Body=json.dumps(manifest).encode("utf-8"),
    )


def main():
    if sys.byteorder != "little":
        raise SystemExit("uint16 parts are little-endian")
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["RAYON_NUM_THREADS"] = "1"
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--sources", default="")
    parser.add_argument("--tokenizer", required=True)
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    os.makedirs(args.workdir, exist_ok=True)
    os.makedirs(os.path.join(args.workdir, "tmp"), exist_ok=True)
    tok_sha = hashlib.sha256(open(args.tokenizer, "rb").read()).hexdigest()
    wanted = {name for name in args.sources.split(",") if name}
    rows = [row for row in sources() if not wanted or row["name"] in wanted]
    s3 = s3_client()
    done = done_set(s3)
    print(f"done markers {len(done)}", flush=True)
    progress = os.path.join(args.workdir, "progress.jsonl")
    stop = os.path.join(args.workdir, "STOP")
    if os.path.exists(stop):
        os.remove(stop)
    counts = {}
    queue = Queue(maxsize=128)
    n_workers = max(1, args.workers)
    procs = []
    for i in range(n_workers):
        proc = Process(
            target=worker,
            args=(queue, args.tokenizer, os.path.join(args.workdir, "tmp", str(i)), stop, progress),
        )
        proc.start()
        procs.append(proc)

    def feed():
        try:
            feed_tasks(s3, rows, done, args.max_files, queue, counts)
        except Exception:
            traceback.print_exc()
            print("FEED FAIL", flush=True)
        finally:
            for _ in procs:
                queue.put(None)

    feeder = threading.Thread(target=feed, daemon=True)
    feeder.start()
    failed = False
    try:
        while feeder.is_alive() or any(proc.is_alive() for proc in procs):
            time.sleep(60)
            try:
                publish_manifest(s3, progress, tok_sha, counts)
            except Exception as exc:
                print(f"manifest refresh failed: {exc}", flush=True)
            if os.path.exists(stop):
                failed = True
                for proc in procs:
                    proc.terminate()
                break
        for proc in procs:
            proc.join()
            if proc.exitcode not in (0, None):
                failed = True
    finally:
        publish_manifest(s3, progress, tok_sha, counts)
    fail_path = os.path.join(args.workdir, "fails.jsonl")
    if failed or os.path.exists(stop) or os.path.exists(fail_path):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
