# Mass tokenization, then the curriculum

Tokenize the training text once. The curriculum is a sampler over those tokens. It is not a second tokenization. The token files and the index are immutable. Do not write warmup, stable, or annealing token files. A phase weight is a sampler input. Changing it does not retokenize.

The English budgets and phases are the [English curriculum](sota-curriculum.md): 717B, warmup 36B, stable 537B, annealing 144B. Indic is the seven-language sheet in the [tokenize run plan](tokenize-run-plan.md), 247.98B on that sheet. The census replaces both numbers. A short file stays short.

Global MinHash is not part of this run. The English note still describes it. The later decision is to skip it: these sources are separate products, and leftover copies of high-quality text stay. Benchmark scans are not part of this run either. These are published datasets, used as released. Do not search them for GSM8K, MATH, MMLU, MMLU-Pro, HumanEval, MBPP, or DS-1000.

## Tokenizer

Load [hf-tokenizer](hf-tokenizer) with the stock fast tokenizer. That is the file vLLM reads. Indic is Sarvam score BPE. Characters are the atoms. There is no grapheme lock. `हिन्दी` is `Ġह` | `िन्` | `दी`.

Content files are `uint16`. Every content id satisfies 0 ≤ id ≤ 65535, and ids 0–31 occur zero times. The encoder fails on the first id outside 0–65535 or in 0–31. It does not cast that id and continue. Do not discover this after terabytes.

Content files do not contain `<eod>`. Checked the stock files. `tokenizer.json` gives `<eod>` id 4, as an added token and in the vocab. It is 4. `tokenizer_config.json` and `special_tokens_map.json` do not name `<eod>`. They name `<unk>`, `<s>`, `</s>`, and `<pad>`. The packer appends id 4 after each document later.

Three fixtures still differ between this file and the Python encoder: `C++में`, `\frac{1}{2}`, and a newline plus four spaces before `return`. The fleet uses the stock file, so those cuts are the training cuts. Do not mix the two encoders in one bin.

## What is tokenized

English, one pass of the stored text, then the sampler draws the budget:

| Row | Billions on the sheet | Prefix |
| --- | ---: | --- |
| ClimbMix | 400 | `datasets/nemotron-climbmix/karpathy-400b-shuffle/` |
| Math 4+ | 52 | `datasets/nemotron-cc-math-v1/4plus/` |
| MIND | 35 | `datasets/nemotron-cc-math-v1/4plus_MIND/` |
| RQA | 10 | `datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-RQA/` |
| Fact-Seeking | 5 | `datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/` |
| Specialized v1.1 | 9 | `datasets/Nemotron-Pretraining-Specialized-v1.1/` |
| CodeAlchemy | 40 | `datasets/codealchemy/` |
| Nemotron Code v2 | 45 | `datasets/nemotron-code-v2/` |
| HQ synth | 50, or two epochs of 15B | one branch: real v2.1 HQ text, or the TinyLlama 15B pack if that text is absent |
| Genesis III | 52 | `datasets/genesis-iii/`, option-level rows only |
| InfiniByte | 19 | `datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-InfiniByte-Reasoning/` |

Indic, seven languages only (Hindi, Bengali, Tamil, Telugu, Kannada, Marathi, Gujarati):

| Row | Billions on the sheet |
| --- | ---: |
| Sangraha | 142.50 |
| FineWeb 2 | 13.32 |
| IndicCorp v2 | 13.80 |
| BhashaWiki | 13.61 |
| Cosmopedia | 33.49 |
| Indic HQ-synthetic | 10.83 |
| Indic Fact-Seeking | 20.41 |

Sangraha drops `*_Latn`, `verified/eng`, and every language outside the seven. BhashaWiki has no Telugu and no Marathi. Kannada has no Indic HQ-synthetic. Cosmopedia keeps v5, and keeps a v4 row only when v5 does not already have that source id. `translation-staging/` stays out.

## One pass

Each worker reads one parquet, or one IndicCorp text file. For every document:

1. Drop it before encode when the row is empty, listed in that chunk’s quarantine file, outside the seven Indic languages, or a Genesis row that is not option-level. A Genesis file that does not name its pipeline is dropped. Failure analysis is not tokenized. There is no benchmark scan.
2. Encode with the stock tokenizer. The encoder fails on the first illegal id, as above. Record gzip level 6 on the UTF-8 text, `mtime=0`, ratio = compressed / original. Under 512 bytes is mid. Easy is under 35%. Mid is 35% through 65%, including both ends. Hard is over 65%. That label is a compression band. A compression band is a curriculum heuristic from the gzip level-6 ratio. It is not a measure of semantic difficulty. ClimbMix, Math 4+, MIND, RQA, Fact-Seeking, and Specialized already have zstd scores. Those are a different scale. This pass writes gzip, which is what the curriculum compression bands use. The five new slices already have gzip scores. Copy those ratios onto the index line instead of recomputing them.
3. Carve the holdout with a hash of the document id, so the val set is fixed before any shuffle. ClimbMix bucket 0 modulus 8000. Math 4+ modulus 10000. The first code source to finish: 5M tokens. RQA, Fact-Seeking, Specialized, InfiniByte, and each Indic language: 2,000 documents when the language has at least 10,000, otherwise 5%. Code and Genesis: 5M tokens once their prefixes exist. HQ keeps the existing 50,000,001 val tokens and does not put those documents in the train bin. The 0.4B InfiniByte remainder above 19B is holdout, not train.

No MinHash. No drop list of near-duplicates. A MIND page and its Math 4+ page can both be tokenized. The sampler, not this pass, keeps the hard compression band of Math 4+ and the hard compression band of MIND out of the same phase.

## What is written

Bucket `s3://<research-data-bucket>/tokenized/tok65k/`. Nothing under `datasets/` or `translations/` is overwritten.

```
tokenized/tok65k/
  manifest.json
  {source}/{lang}/part-00000.uint16
  {source}/{lang}/part-00000.index.jsonl
  {source}/{lang}/part-00000.val.uint16
  {source}/{lang}/part-00000.val.index.jsonl
  _done/{source}/{parquet-key-hash}
```

`lang` is `en`, `hin`, `ben`, `tam`, `tel`, `kan`, `mar`, or `guj`. One part is about 1B content tokens (2 GiB of `uint16`) or the rest of a small source. The index line is `doc_id`, `row_key`, `token_start`, `n_tokens`, `n_bytes`, `gzip_ratio`, `compression_band`, `parquet_key`. `token_start` is `uint64`. `compression_band` is easy, mid, or hard.

`manifest.json` records, per source and language: bytes read, documents kept, documents dropped by reason, content tokens, val tokens, sha256 of each part, and the tokenizer file hash. The sheet billions are copied in as `sheet_billions`. The sampler uses the census, `content_tokens / 1e9`, not `sheet_billions`.

After drops, the same record is machine-checkable per source and per language. `total_source_tokens = train_available_tokens + validation_tokens`. `curriculum_draw <= available_train_tokens × allowed_epochs`. If the census is short of the sheet, the sampler uses the census. It does not invent tokens up to the sheet. ClimbMix on the sheet is 400B. A census of 327.4B stays 327.4B.

HQ synth takes one of two branches. Do not mix them.

- Real Nemotron-CC v2.1 HQ text exists: tokenize that text. Do not decode the TinyLlama pack. If unique content tokens are at least 50B, the sampler uses the 50B branch. If they are under 50B, the sampler uses those unique tokens. It does not invent tokens up to 50B. It does not switch to the 15B pack schedule.
- Real v2.1 HQ text does not exist: decode the TinyLlama HQ pack with TinyLlama, then encode the decoded text with this tokenizer. The manifest says `retokenized_from_tinyllama`. Cap that branch at two epochs, 30B. The English curriculum’s 15B branch is then the schedule. Do not also read a v2.1 prefix.

## Speed

The half-day budget is the slow planning rate, 5 MB/s per core. The fleet is built to run at the Rust tokenizer’s rate, and the probe replaces the guess before the four machines are launched. That run is the same 1,000-document check in Machines. A fast tokenizer that misses a saved row does not launch the fleet.

The inner loop is not Python. One process loads [hf-tokenizer](hf-tokenizer) once and calls `encode_batch`. The stock tokenizer is the Rust library. A per-document Python call would throw away the cores. The router is already inside that file, so the fleet does not reimplement it.

Parquet is read with column projection. Only `text`, the id column, and the pipeline flag for Genesis are pulled. Row groups stream. The object is not staged as a full extra copy if the reader can pull byte ranges. Same-region S3 is the path. ClimbMix’s 6,543 shards are about 90 MB each, so a Spot stop loses seconds of work, not an hour.

Gzip level 6 uses zlib-ng or libdeflate, not the Python gzip module. Documents under 512 bytes skip the compress call and are recorded as mid. The five slices that already have gzip level-6 scores copy the stored ratio. They are not compressed again.

Writes are a buffered `uint16` part and a buffered index. One parquet key maps to exactly one `_done` marker. `_done` exists means never process that key again. `_done` absent means any output for that key is temporary. Write the part and the index to temporary names, fsync and close, then rename both to the final names only after that success, then write `_done`. A dead worker’s partial output is not final and is not a second part. Claim expiry is not this safety model. The 1-in-10,000 decode check runs after the part is durable, not in front of the next file.

ClimbMix is about half the bytes, so it starts on two of the four machines immediately. The smaller sources share the other two. A source with 30 files is not spread so thin that startup costs more than the encode.

The Spot request names `c7i.12xlarge`, `c7i.8xlarge`, and `c7i.16xlarge`, capacity-optimized, so the machines can land in more than one zone. On-demand is not the fallback. That quota is 64 vCPU and cannot hold this fleet.

If the probe is well above 5 MB/s per core, wall clock falls toward the S3 read. A few terabytes at the network of these boxes is inside an hour. If the probe is near 1 MB/s per core, add boxes up to the 256 vCPU Spot quota instead of accepting a slow inner loop.

## Machines

Same region as the bucket. Leave the smaller tokenizer instance stopped. The larger tokenizer instance is the probe: 1,000 documents per path, before the fleet starts. Matching token ids is not enough. For each document, compare the whole preprocessing function: `document_id` (the index `doc_id`), the raw UTF-8 bytes and their hash, the token ids, `n_tokens`, the gzip ratio, the compression band, and the holdout or train assignment. One mismatch stops the fleet. The probe proves the preprocessing function is deterministic, not only that the tokenizer runs.

Fleet after the probe: four `c7i.12xlarge` (48 vCPU, 96 GiB), spot, 200 GiB gp3 each. One process loads the tokenizer and forks one worker per core. A worker claims a parquet key. A claim older than 30 minutes with no `_done` is free again. That expiry only releases the claim. It does not make a partial file final. Spot interruption loses the open temporary file only.

About 2 TB of parquet is already in scope, plus about 690 GB of text in the five new slices. Uncompressed text is on the order of 5–8 TB. At the fast-path planning rate, 5 MB/s per core on 192 cores, that is about half a day of wall clock. Spot for that window is about $30. On-demand is about $70. If the probe is near 1 MB/s per core, use eight boxes and budget a day.

Stop every instance when `manifest.json` is on S3.

## After the bins exist

The sampler reads the index. It does not encode again. The token files and the index stay immutable. Changing a phase weight does not retokenize.

1. Read the census from the manifest. Where the census is under the sheet, the sampler uses the census. It does not invent tokens up to the sheet. ClimbMix at 327.4B against a 400B sheet stays 327.4B. ClimbMix does not grow to fill a hole. Hindi does not absorb a short Indic language. HQ stays on the one branch chosen above. Real v2.1 text under 50B unique tokens is drawn at that count. It is not the 15B pack schedule.
2. The compression band is already on the index line. A short compression band moves its billions to mid for that dataset and that phase. It is not filled from Genesis, RQA, Fact-Seeking, or Specialized multiple choice.
3. Hash the document id into warmup, stable, or annealing in the proportions in Table 2 and Table 3 of the English curriculum. A document is in one phase. Indic uses the epoch caps in the tokenize run plan: verified Sangraha up to 3, the other native web rows 1 if the language prefix is tens of GiB, otherwise 3, each translation source up to 3 after the source-id overlap check.
4. Apply the format cap while assigning, not by deleting tokens after the fact. Genesis, RQA, Fact-Seeking, and Specialized multiple choice together stay at or under 10% of each phase on the main schedule. Only the TinyLlama HQ branch may put stable over that ceiling, because that branch lands the leftover 20B on RQA. A short real v2.1 census does not. Annealing stays under the ceiling.
5. Keep hard Math 4+ in annealing only, and hard MIND in stable only. Hard here is the compression band over 65%. When a WARC id matches, the page stays in hard Math 4+ and the dialogue moves to mid MIND of its phase.
6. Shuffle inside the phase. Do not sort a phase from the easy compression band to the hard compression band.
7. The training packer appends `<eod>` and packs sequences. That is not part of this tokenization.

The learning rate is not chosen here. Data warmup is the first 36B English tokens. The learning-rate warmup is the first 4B of those, then the peak holds through stable and decays linearly to zero across the 144B annealing tokens.

## Checks

- `_done` matches the parquet keys for each source. One key, one marker. A key with no `_done` has no final part.
- The sum of `n_tokens` equals the `uint16` file length divided by 2.
- Every content id satisfies 0 ≤ id ≤ 65535, and ids 0–31 occur zero times. The encoder already failed on the first violation.
- Per source and per language, after drops: `total_source_tokens = train_available_tokens + validation_tokens`, and `curriculum_draw <= available_train_tokens × allowed_epochs`.
- A census under the sheet is the draw. The sampler does not invent tokens up to `sheet_billions`.
- Decode 1 in 10,000 documents with the same stock tokenizer and compare to `text`.
- Every part’s sha256 is in the manifest before the instance that wrote it is stopped.
- The manifest’s phase draws, summed from the index, match Table 2 within the documents that were actually dropped.

## Not in this job

MinHash. Benchmark scans for GSM8K, MATH, MMLU, MMLU-Pro, HumanEval, MBPP, or DS-1000. A second copy of a dataset to fill a short compression band. Warmup, stable, and annealing as separate token files. Retokenizing because a phase weight changed. Sequence packing. The training run.
