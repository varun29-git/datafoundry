---
cursor:
  subagentId: "bc-d02834db-edd0-51e5-a6de-0e350f2d3f3b"
---

# Run the 65,536 tokenizer on the English and Indic sheets

Tokenize the sheets below with the frozen tokenizer. This job writes token ids and a census. It does not train the model, and it does not retrain the tokenizer.

The sheet numbers are billions of tokens. They were not counted with this tokenizer. The census replaces them where the files exist. A short file stays short. Nothing is repeated to manufacture the printed billion.

Combined sheet: **717B English + 247.98B Indic = 964.98B**. At `uint16`, the budgeted tokens are **1.76 TiB** of ids. Stored text is larger than several of the slice rows, so the bins can land above that if every in-scope document is kept.

## The tokenizer

File: [tokenizer-65k.json](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/tokenizer-65k.json).

sha256 `c53e0e95cd19e2954a8c7114c0a580eeb16698b153fdf84c5d80a7187d778d29`. That matches [the freeze note](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/tokenizer-65k-freeze.md). A later status line recorded `1bd42dcd…`. The bytes on disk are the `c53e0e95…` file. The fleet refuses any other hash.

65,536 pieces, ids 0–65535. That fits in `uint16` with nothing left over. `K = 40059` frozen Indic pieces, `U = 435`, English tail `25189`. `indic_model` is BPE. The space mark is Ġ (U+0120). `tokenizer_spec` is inside the file. The loader refuses to start if that block disagrees with the encoder.

Reference encoder: `Encoder.encode` in [build-65k.py](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/internal/build-65k.py). It does not open `tokenizer.model`. Normal text does not emit ids 0–31 (`<unk>` through the reserved specials). `<eod>` is id 4. The encoder does not insert it. The packer does, later, once per document.

Two paths, chosen by the router:

- Indic span. NFC, a leading Ġ, each ordinary space becomes Ġ, then BPE by `indic_scores` (higher score first, leftmost pair on a tie). A character with no piece becomes `<0xHH>` bytes. This is the Sarvam cut, with our ids.
- English span. The scissors regex, then the 25,189 English merges. Newline-plus-indent stays one chunk. A LaTeX command can be one chunk. Digits stay single. A contraction stays one chunk. A token does not cross a protected whitespace run.

Protected whitespace is a tab, a newline, a carriage return, or two or more spaces. Those runs take the English path and split the line. One ordinary space between two Indic words stays inside the Indic span (`जा रहा` is one span). `main जा रहा hoon` is English, space, Indic, space, English. A mixed word splits on the script change, and digits and punctuation stick to the run on their left.

Held-out fertility already measured with this file: English 1.4254 tokens per word, code 2.0299, math 1.8574. Round-trip mismatches on the gate files were 0. `<unk>` was 0.

The Python encoder is the correctness oracle. It is not the fleet encoder. Indic BPE builds a Python heap over every character. English BPE scans every pair on every merge, so a long chunk is quadratic. RQA rows are 11k–40k characters. Running that loop across this sheet is a multi-week job on one 32-core box.

The fleet encoder has to emit the same ids:

1. Load the json once, then fork. Workers inherit the tables. Do not parse the json inside every worker.
2. Keep the Python router. It is one pass over the characters.
3. Indic spans go through SentencePiece `EncodeAsPieces` on the Sarvam `tokenizer.model` (sha256 `4cd33409a577e8b416247587b0f5bd7a3eec245a1f18d4ec7793ff299ad3fbe2`), then a dict from piece string to our id. Gate 1 already says those piece strings match on the seven languages. A span whose pieces are not all in our table falls back to `IndicBPE` for that span only.
4. English spans go through a Rust BPE (Hugging Face `tokenizers`) loaded with `english_scissors` and `english_merges`, plus the forced LaTeX seeds. Same ids as `Encoder.bpe`.

Before any VM reads the corpus, 1,000 documents per path (English web, code, math, and one file per Indic language) must match `Encoder.encode` byte for byte on the id list. One mismatch stops the fleet.

Planning rates, until that probe replaces them: the Python encoder at about 0.05–0.3 MB/s of text per core; the Rust-plus-SentencePiece path at about 5–20 MB/s per core. The probe is 100 MB of ClimbMix and 100 MB of Hindi Sangraha, both encoders, on the first instance. Fleet size comes from the measured rate, not from these ranges.

## What the sheets are

English is the 717B sheet. Indic is the seven-language sheet. Billions are the draw, not a second copy of a bigger public release.

| English | Billions | Role |
| --- | ---: | --- |
| ClimbMix | 400 | web, one pass |
| Nemotron Math 4+ | 52 | scored math web |
| Nemotron MIND | 35 | dialogue on those pages |
| RQA | 10 | long reasoning |
| Fact-Seeking | 5 | short quiz items |
| Specialized v1.1 | 9 | mostly Code-Concepts, annealing only |
| CodeAlchemy | 40 | synthetic code |
| Nemotron Code v2 | 45 | code |
| Nemotron-CC v2.1 HQ Synth | 50 | rephrased web |
| Genesis III | 52 | option-level STEM only |
| InfiniByte Reasoning | 19 | cross-domain problems |
| **Sum** | **717** | |

| Indic, billions | Hindi | Bengali | Tamil | Telugu | Kannada | Marathi | Gujarati | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Sangraha | 34.50 | 30.00 | 17.00 | 16.00 | 14.00 | 14.00 | 17.00 | 142.50 |
| FineWeb 2 | 4.82 | 2.65 | 1.84 | 1.47 | 0.68 | 1.12 | 0.74 | 13.32 |
| IndicCorp v2 | 8.00 | 1.60 | 1.20 | 1.00 | 0.55 | 0.85 | 0.60 | 13.80 |
| BhashaWiki | 3.30 | 2.60 | 2.45 | — | 2.40 | — | 2.86 | 13.61 |
| **Native** | **50.62** | **36.85** | **22.49** | **18.47** | **17.63** | **15.97** | **21.20** | **183.23** |
| Cosmopedia | 5.53 | 5.20 | 5.62 | 5.53 | 3.15 | 3.05 | 5.41 | 33.49 |
| Nemotron HQ-Synthetic | 2.07 | 1.58 | 2.17 | 2.50 | — | 0.02 | 2.49 | 10.83 |
| Fact-Seeking | 2.85 | 2.78 | 3.13 | 2.95 | 3.01 | 2.84 | 2.85 | 20.41 |
| **Translation** | **10.46** | **9.56** | **10.93** | **10.98** | **6.16** | **5.90** | **10.76** | **64.75** |
| **All** | **61.08** | **46.41** | **33.42** | **29.45** | **23.79** | **21.87** | **31.96** | **247.98** |

A dash is zero. Telugu and Marathi do not take BhashaWiki. Kannada does not take HQ-synthetic. Marathi HQ-synthetic is 0.02B, which is a stub, not a missing cell to fill by translating.

Languages outside these seven are not in this job. That drops Sangraha and FineWeb 2 splits for Nepali, Urdu, Malayalam, Sanskrit, Punjabi, Odia, Sindhi, Assamese, and the smaller Sangraha splits. It drops Latin-script Sangraha (`*_Latn`). It drops `sangraha/verified/eng`.

## Where the bytes are

Account `023894314260`. Region `us-east-1`. Buckets `nemotron-training-data-us-east-1` and `quark-research-repository-storage`. Sizes are the 27 September inventory and the 1 October prefix walk. “Missing” means neither bucket had that prefix.

| Sheet row | Prefix | On disk | Against the sheet |
| --- | --- | --- | --- |
| ClimbMix 400 | `datasets/nemotron-climbmix/karpathy-400b-shuffle/` | 558.57 GiB, 6,543 parquet | The name is the 400B shuffle. One pass. If the census is under 400B, stop. |
| Math 4+ 52 | `datasets/nemotron-cc-math-v1/4plus/` | 57.92 GiB, 46 parquet | Published 52.32B. One pass of this prefix. |
| MIND 35 | `datasets/nemotron-cc-math-v1/4plus_MIND/` | 84.13 GiB, 90 parquet | Public regeneration is about 73B, so 35B is a slice. Tokenize the prefix. The sampler stops at 35B. |
| RQA 10 | `datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-RQA/` | 171.88 GiB, 175 parquet | Public size 134.6B. Tokenize the prefix. Draw 10B. |
| Fact-Seeking 5 | `datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/` | 42.51 GiB, 72 parquet | Published about 35B. Rows are ~100–500 characters. Draw 5B. |
| Specialized v1.1 9 | `datasets/Nemotron-Pretraining-Specialized-v1.1/` | 32.49 GiB, 68 parquet | Release about 9.30B. One pass. Draw subsets by stored bytes: Code-Concepts 8.28, Multiple-Choice 0.63, Unconditional-Algorithmic 0.05, Formal-Logic 0.02, Economics 0.02. |
| InfiniByte 19 | `datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-InfiniByte-Reasoning/` | 26.40 GiB, 30 parquet | Card says 19.4B. 26 GiB of parquet may census under 19B. One epoch of what is stored. Leave the extra 0.4B out by document-id hash if the census clears 19B. |
| CodeAlchemy 40 | none | Missing | Public release is on the order of 977B tokens. Download a slice, then tokenize. |
| Nemotron Code v2 45 | none | Missing, HF gated | Do not substitute Code-Concepts or Diverse-QA. |
| HQ Synth 50 | no English text tree | The other bucket has a TinyLlama `uint16` pack of **15,000,000,001** train tokens, Nemotron-CC-v2 High-Quality-Synthetic, not v2.1 text | See the HQ section. |
| Genesis III 52 | none | Missing | Public option-level is the row. Failure analysis is not. |
| Sangraha 142.50 | `datasets/sangraha/verified/`, `synthetic/`, `unverified/` | Verified seven languages **131.4 GB**. Whole Sangraha tree is 202.91 + 380.12 + 73.18 GiB, most of it other languages or Latin twins | Verified alone cannot be 142.5B. Synthetic native-script and unverified are in the row. The census decides the epoch. |
| FineWeb 2 13.32 | `datasets/fineweb2-indic/{hin_Deva,ben_Beng,tam_Taml,tel_Telu,kan_Knda,mar_Deva,guj_Gujr}/` | **84.7 GB** across those seven | This sheet includes FineWeb 2. Tokenize these seven prefixes only. |
| IndicCorp v2 13.80 | none | Missing | Not FineWeb 2. Download, then tokenize. |
| BhashaWiki 13.61 | none | Missing | Download. Telugu and Marathi stay absent. |
| Cosmopedia 33.49 | `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v5-20260906/` and the v4 rule | v5 **51.43 GiB**, 588 parquet. v4 **132.07 GiB**. Salvage 5.27 GiB. Checkpoints 2.37 GiB | 33.49B is a lot for v5 alone. Dedup first, then census. |
| HQ-Synthetic Indic 10.83 | `translations/Cosmopedia-v2/Krutrim/krutrim-nemotron-cc-v21-hq-synth-v1-20260906/` | **49.18 GiB**, 771 parquet | Kannada cell is zero. Confirm the census shows Kannada absent. Marathi at 0.02B should match a tiny split, not a full language prefix. |
| Fact-Seeking Indic 20.41 | `translations/.../fact-seeking-70shard-10lang-r16-20260903/` | **170.63 GiB**, 3,655 parquet | The name says 10 languages. Tokenize the seven. Leave the other three out of the bins. Smoke and pilot prefixes stay out. |

Sangraha verified, seven languages, measured bytes:

| Split | Bytes |
| --- | ---: |
| `hin` | 37,340,748,989 |
| `ben` | 29,900,341,277 |
| `tam` | 18,707,825,069 |
| `tel` | 15,104,046,970 |
| `mar` | 12,781,930,636 |
| `guj` | 9,931,759,912 |
| `kan` | 7,649,517,444 |

FineWeb 2, seven prefixes, measured bytes: Hindi 34,272,968,716; Bengali 23,894,953,700; Tamil 9,438,382,231; Marathi 6,278,522,796; Telugu 3,950,350,913; Kannada 3,526,351,166; Gujarati 3,338,859,951.

Text column is `text` on these parquet files. Translations also carry a quarantine file per chunk. Sangraha rows use `doc_id`. Specialized rows use `uuid` or the parquet row id. The index stores whichever id the file has, and a stable key `{parquet key}:{row}` when it has none.

## What gets dropped before encode

Same pass as the read. A dropped row is a counter, not a token.

- Quarantine. For every translation chunk, drop ids listed in that chunk’s `quarantine_manifest.jsonl`. Read `translated_documents.parquet` only.
- Cosmopedia overlap. Keep v5. From v4, salvage, and the checkpoint run, keep a source id only when v5 does not have it. `translation-staging/` stays out. The 976 GB staging tree is not input.
- Sangraha `*_Latn`, `verified/eng`, and every language outside the seven.
- Genesis rows whose `pipeline` is not option-level, and any Genesis file that does not say which pipeline it is. If nothing is option-level, Genesis is zero and the English sheet is 665B. Do not train a mixed file to reach 52B.
- Documents with empty `text`.

Do these in the tokenize pass, because they are per-row. Do not wait on them.

Global near-duplicate removal is a second job, and it does not block the bins. MinHash on 5-grams, Jaccard 0.8, across ClimbMix, Math 4+, MIND, and HQ synth. On a hit, Math 4+ beats ClimbMix, Math 4+ beats a near-copy HQ page, ClimbMix beats a near-copy HQ page, and a MIND row at 0.8 or above against its Math 4+ page drops. Code rows, once the files exist, use Jaccard 0.7 inside and across the pair. The second job writes a drop-list of document ids. The sampler skips them. Token shards stay. Dropped tokens are not refilled.

There is no benchmark scan. The tokenize pass does not load GSM8K, MATH, MMLU, MMLU-Pro, HumanEval, MBPP, or DS-1000.

While each document is in memory, store gzip level 6 ratio (`mtime=0`, text bytes only) on the index line. Documents under 512 bytes are recorded as mid regardless of ratio. Band cuts stay the English sheet’s: under 35% easy, 35–65% mid, over 65% hard. The sampler uses the ratio. This pass does not sort the bins.

## Output

Bucket `s3://nemotron-training-data-us-east-1/tokenized/tok65k/`. Nothing else is written. No overwrite of `datasets/` or `translations/`.

```
tokenized/tok65k/
  manifest.json
  drop-list/            # second job, document ids
  {source}/{lang}/part-00000.uint16
  {source}/{lang}/part-00000.index.jsonl
  {source}/{lang}/part-00000.val.uint16
  {source}/{lang}/part-00000.val.index.jsonl
  _done/{source}/{parquet-key-hash}
```

`lang` is `en` or `hin`, `ben`, `tam`, `tel`, `kan`, `mar`, `guj`.

One part holds about 1B content tokens (2 GiB of `uint16`) or the rest of a small source. Tokens are concatenated in index order. The index line is one JSON object: `doc_id`, `row_key`, `token_start`, `n_tokens`, `n_bytes`, `gzip_ratio`, `parquet_key`. `token_start` is `uint64`.

Val is carved here so a later shuffle cannot leak it. Hash the document id with blake2b-64. ClimbMix bucket 0 modulus 8000 (about 50M tokens if the shuffle is 400B). Math 4+ modulus 10000 (about 5M). RQA, Fact-Seeking, Specialized, InfiniByte, and each Indic language: 2,000 documents when the language has at least 10,000, otherwise 5% of its documents. Code and Genesis use 5M tokens, same hash, once their prefixes exist. HQ synth keeps the existing rule: bucket 0 modulus 500, 50,000,001 tokens, and those documents are not retokenized into the train bin.

Content ids only. No `<eod>` in these files. The training packer appends id 4 after each document and then packs sequences. Putting `<eod>` in both places would train a double boundary.

`manifest.json` has, per source and language: parquet bytes read, documents kept, documents dropped by reason, content tokens, val tokens, sha256 of each part, and the tokenizer sha256. The English and Indic tables in this note are copied in as `sheet_billions`. The manifest’s `content_tokens / 1e9` is the number the sampler is allowed to believe.

## HQ synth, the row that is not text

The 50B English cell needs Nemotron-CC v2.1 high-quality synthetic text. That tree is not in the bucket.

What is stored is `s3://quark-research-repository-storage/data/nemotron_cc_v2_hqsynth_tinyllama_15b_parallel_20260730T185305Z/`: 15,000,000,001 train tokens and 50,000,001 val tokens, TinyLlama, `uint16`, sequence length 2048. It is v2, not v2.1. Decoding those ids with TinyLlama and encoding with this tokenizer is valid, and the manifest must say `retokenized_from_tinyllama`. The count will not be 15B and it will not be 50B. Two epochs of that retokenized text is the cap. The other 20B of the 50B cell is not created by a third epoch.

If a real v2.1 text prefix shows up and this tokenizer counts at least 50B unique tokens, use that prefix and ignore the TinyLlama pack. Until then the English sheet’s HQ cell is “two epochs of the 15B pack, retokenized,” and the phase tables in the English curriculum that assume 50B unique tokens do not apply.

The unfinished prefix `data/nemotron_cc_v2_hqsynth_tinyllama_15b_20260730T1840Z/` has no token bin. Leave it.

Indic HQ-synthetic is a different source (the 49.18 GiB translation). It does not fill the English cell.

## Missing prefixes, before their VMs start

Download into `datasets/` under names that match the sheet, parquet, `text` column, same region. Record bytes and object counts in the manifest. Do not point the tokenizer at a Hugging Face cache on a laptop.

| Row | Get | Then |
| --- | --- | --- |
| CodeAlchemy 40B | A 40B-token slice of `open-alchemy/code-alchemy`, not the whole ~977B | One pass of the slice. |
| Nemotron Code v2 45B | Gated `nvidia/Nemotron-Pretraining-Code-v2`. The token lives in Secrets Manager, not in the script. | Cap 2 epochs only if the unique count is under 45B. |
| Genesis III 52B | `qvac/GenesisIII`, `pipeline == option_level` only | Half of option-level is the idea of the 52B. If the option-level census is under 52B, the run shrinks. Annealing Genesis is cut first. |
| IndicCorp v2 13.80B | AI4Bharat IndicCorp v2, seven languages | One epoch if it is tens of GiB or more. |
| BhashaWiki 13.61B | The wiki-derived set, five languages (no Telugu, no Marathi) | One epoch. A missing language stays a dash. |
| English HQ text | Only if v2.1 text is actually published into the bucket | Otherwise the TinyLlama retokenize path above. |

These five downloads are on the order of a few hundred GiB for the slices, and more if someone pulls full CodeAlchemy or full Genesis. Cap each download at the slice. A full CodeAlchemy pull is about a terabyte of parquet and is not this job.

## Machines

Same region as the bucket. S3 same-region traffic is the path. Use an S3 gateway endpoint if the instances sit in a private subnet, so the reads do not go through NAT.

Instance role, and only this role: `s3:GetObject` and `s3:ListBucket` on both buckets, `s3:PutObject` on `tokenized/tok65k/*`. The Bedrock IAM user that listed the bucket from a laptop does not go on the fleet.

Stopped instances already in the account, from the tokenizer build: `i-0676987ec61af5f49` (`m7i.8xlarge`, name `tokenizer-65k`) and `i-0c6550d199294585f` (`m7i.4xlarge`). Leave the 4xlarge stopped. The 8xlarge is the probe and the golden-test box. It is not the corpus fleet. Stop it again when the golden test passes.

Fleet, after the golden test:

- Type `c7i.12xlarge` (48 vCPU, 96 GiB). Compute-heavy, and 96 GiB is enough to fork workers after one load of SentencePiece plus the json. List price used for the estimate: about **$2.14/hour** on-demand in `us-east-1`, from $0.714 per `c7i.4xlarge`-hour. Confirm with the pricing API the morning the fleet starts. The recorded `m7i.4xlarge` price is $0.8064/hour; an `m7i.8xlarge` is $1.6128/hour if the probe box is billed on-demand.
- Four instances. Spot, capacity-optimized, interruption-safe because a finished parquet key has a `_done` marker. On-demand only for a Spot drought.
- 200 GiB gp3 on each box. Scratch for one parquet download, the part file, and the upload. Delete the parquet after the part is on S3.
- Workers: one process loads, forks one worker per vCPU. Each worker pulls a parquet key by a conditional put on `_claim/{hash}`. A claim older than 30 minutes with no `_done` is free again.
- One parquet file is the unit. ClimbMix’s 6,543 shards and the Fact-Seeking translation’s 3,655 chunks are the long lists. Small sources (InfiniByte’s 30 files, Specialized’s 68) finish inside an hour and should not be spread so thin that startup dominates.

Work left after the golden test, using the planning rate of 5 MB/s per core on the fast path:

About 2 TB of in-scope parquet (English prefixes that exist, Sangraha for seven languages, FineWeb 2 for seven, the translation runs). Uncompressed text is on the order of 4–6 TB. At 5 MB/s and 192 cores (4 × 48), 5 TB is about **1.5–2 hours of encode**, plus S3 read time. A `c7i.12xlarge` is not line-rate bound on a few hundred mebibytes per second per box. Budget **half a day** of wall clock for the resident data, including starts, stalls, and the val split.

At the low end of the fast path (5 MB/s is already the low planning number), four boxes are enough. If the probe lands at 1 MB/s per core, use eight boxes and budget a day. If the probe lands at the Python rate, stop and fix the encoder. Do not scale the Python loop out. Sixteen boxes of Python Indic BPE is still the wrong plan.

Spot estimate: 4 × $2.14 × 0.4 spot discount × 8 hours ≈ **$30** of instance time for the resident corpus, if the fast path holds. On-demand for that same window is about $70. The probe box for a day is another $40 on-demand. The open bill is the missing downloads, which can dwarf this if a full release is pulled, and the stored bins.

Storage: 2 TB of `uint16` at S3 standard is about **$0.023/GB-month ≈ $47/month**. PUT of ~2,000 parts is noise. Do not use Glacier. The trainer will read these bins once per epoch.

## Order

1. Pin the json hash. Run the 1,000-document golden test on the 8xlarge. Record both throughput numbers in `manifest.json` under `probe`.
2. Download only the missing slices that are actually approved to fetch. IndicCorp, BhashaWiki, CodeAlchemy, Code v2, and Genesis are independent and can land in parallel. A row with no prefix does not get a bin of zeros. It is absent from the manifest until the prefix exists.
3. No global dedup and no benchmark scan. Gzip ratio is recorded while the document is in memory, so the band exists on the index line.

ClimbMix and the Nemotron sets that already have compression-ratio scores are not scored again. CodeAlchemy, Nemotron Code v2, Genesis III, IndicCorp v2, and BhashaWiki are scored as soon as that dataset’s prefix in the bucket is non-empty. Scoring does not wait for the other four to finish copying. The rule is gzip level 6, compressed size over original size, on the UTF-8 text. Easy is under 35%. Mid is 35% through 65%, including both ends. Hard is over 65%. A document under 512 bytes is mid. Band counts land before that dataset is tokenized.
4. Tokenize survivors only. Suggested order, so a useful census exists early: Specialized, InfiniByte, Fact-Seeking, Math 4+, MIND, FineWeb 2, Sangraha verified, translations, RQA, ClimbMix. ClimbMix is half the bytes. Start it in parallel rather than last, on two of the four boxes, with the smaller sources on the other two.
5. Retokenize the 15B HQ pack only if v2.1 text is still missing at that point. Dedup that pack on the decoded text first, then encode the survivors with this tokenizer.
6. Write `manifest.json`. Diff `content_tokens` against the sheet. Publish the shortfalls. Do not top up.
7. Stop every instance. The bins, the drop list, and the manifest are the handoff.

## Epoch caps once the census exists

These fire in the sampler, not by encoding the file twice.

| Source | Cap | If the census is short |
| --- | --- | --- |
| ClimbMix | 1 | Train one pass. Do not grow past the census. |
| Math 4+, MIND, RQA, Fact-Seeking, Genesis, CodeAlchemy | 1 of the draw, and at most 2 of the stored unique tokens | The draw shrinks. |
| Specialized v1.1 subsets under 1 GiB | 4 | Formal logic, economics, unconditional algorithmic. |
| Specialized Code-Concepts and Multiple-Choice | 2 | Only if the census is under the 8.28B and 0.63B cells. |
| InfiniByte | 1 | Train what is stored, up to 19B. |
| English HQ, TinyLlama path | 2 | Of the retokenized count. |
| Sangraha verified, per language | 3 | Web repeats are capped. Unused tokens do not move to Hindi. |
| Sangraha synthetic native, unverified | 1 | |
| FineWeb 2, IndicCorp v2, BhashaWiki | 1 if the language prefix is tens of GiB, else 3 | |
| Each translation source, per language, after dedup | 3 | |

Sangraha’s 142.50B is the cell most likely to miss on one epoch of the seven-language files. Verified for those languages is 131 GB of parquet. Even with synthetic and unverified, a single pass can land well under 142.5B, because the old inventory weight for all of Sangraha-as-used was tens of billions, not 142. The manifest’s number wins. Repeating verified to 3 epochs is allowed by the cap and still may not reach 142.5B. Past the cap, the Indic total shrinks. Hindi does not absorb the gap. Hindi is also capped at 25% of Indic tokens in a phase when a later mix is built. This tokenize job does not apply that cap. It only records per-language totals so the sampler can.

Cosmopedia’s 33.49B can miss if v5-plus-v4-only is closer to 15–25B. Same rule. Do not add staging to close it.

## Checks on the running job

- `_done` count versus parquet keys, per source. A source is finished when those sets match.
- Sum of `n_tokens` in the index equals the `uint16` file length divided by 2.
- Decode 1 in 10,000 documents and compare to `text`. A mismatch fails the part and deletes its `_done` marker.
- Ids 0–31 appear zero times.
- Every part’s sha256 is in the manifest before the instance that wrote it is terminated.
- Spot interruption loses the open parquet only. The claim expires. Another worker retries.

## What this job does not do

It does not assign warmup, stable, and annealing. Those ratios live in the English curriculum and are a hash over document ids after the drop-list exists. It does not build 2048-length training sequences. It does not start the 1.2B or 1.5B run. It does not retokenize OpenHermes. It does not touch `test16/`, the domain-classifier parquet, or `nemotron-cc-hq/` (that crawl is not ClimbMix). It does not train an 81,920 tokenizer.
