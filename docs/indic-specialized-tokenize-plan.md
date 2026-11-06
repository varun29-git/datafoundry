# Fast tokenization of specialized

Tokenize every document under `s3://nemotron-training-data-us-east-1/datasets/nemotron-indic-specialized-v1/` with `docs/hf-tokenizer` (vocab 65,536). Store token ids in the same folders: `<lang>/<source_config>/`. Do not delete the text parquet. Do not touch the CC prefix.

This replaces a single-machine Python loop. The inner loop is the Rust tokenizer, `encode_batch`, one load per process.

## Output

- Beside each text file, same basename, suffix `.tokens.uint16`.
- Raw little-endian `uint16`. One id per token. No `<s>`, no `</s>`, no `<eod>`. The packer adds id 4 once per document later, the same rule as the English bins.
- A `.tokens.index.jsonl` line per document: row index, token start, token count.
- A file is final only when the index row count equals the source parquet row count. Until then the objects are temporary names. A dead worker’s partial file is deleted, not kept.

## Fleet

Same region as the bucket, `us-east-1`. Spot only. Compute boxes, not the network boxes used for the Hugging Face copy: `c7i.12xlarge` (48 vCPU). Five fit in the 256 vCPU Spot quota. On-demand is not the fallback.

One process per machine loads the tokenizer once and forks one worker per core. Each worker claims one parquet key. Keys are disjoint. A claim with no finished marker after 30 minutes is free again. That only releases the claim. It does not make a partial file final.

ClimbMix-style sharding: the large segment folders (Math-Textbooks, STEM-SFT, Code-Concepts, Wiki-Rewrite) start on separate machines. A 16-file folder is not spread across the fleet.

## Read and encode

- PyArrow reads the `text` column only, one row group at a time. The object is not downloaded whole.
- `encode_batch` on the batch. Not one Python `encode` per document.
- Null text is an empty document, zero tokens, still one index row, so the row count still matches.
- Ids must be in 0–65535. Ids 0–31 are a hard failure. The worker stops on the first one.

## Probe before the fleet

One Spot box, 100 MB of text from Math-Textbooks and 100 MB from STEM-SFT. Record MB/s per core. The fleet size comes from that number.

Planning rate if the probe is not back: 10 MB/s per core. Five `c7i.12xlarge` boxes are 240 cores, about 2.4 GB/s. The specialized prefix is 644 GB of parquet. At that rate the encode is on the order of 10–20 minutes once the boxes are up, plus S3 write. If the probe is near 1 MB/s per core, the plan is wrong and the encoder is still in Python. Do not add boxes to hide that.

## Not in this pass

Compression bands, phase files, a second copy of the text, and CC. CC is the same pipeline after specialized is done. It is 4.51 TB, so it gets the probe rate first, not a guess.
