# FineWeb-2 Indic, IndicCorp v2, and Sangraha verified token counts

Token totals for the seven native languages already stored as uint16 bins from the frozen 65,536 BPE tokenizer. No text was re-tokenized.

The raw prefixes have no `.tokens.uint16` or `.tokens.index.jsonl` beside the source files:

- `s3://nemotron-training-data-us-east-1/datasets/fineweb2-indic/`
- `s3://nemotron-training-data-us-east-1/datasets/indiccorp-v2/`
- `s3://nemotron-training-data-us-east-1/datasets/sangraha/verified/`

The bins that do exist are under `s3://nemotron-training-data-us-east-1/tokenized/tok65k-other-dual-v1/`, assembled from `tokenized/tok65k-other-dual-v1-shard0/` and `tokenized/tok65k-other-dual-v1-shard1/`. Each part is `part-*.uint16` plus `part-*.index.jsonl` (and a small `.val` pair). An index line has `n_tokens` and `token_start`, not the field name `token_count`.

Counted from `tokenized/tok65k-other-dual-v1/manifest.json` (`updated_unix` 1791522452, 2026-10-09 05:07:32 UTC). For each language, tokens are `train_tokens + val_tokens` and documents are `documents_kept`. The same 21 rows in the two shard manifests add up to the combined manifest on both documents and tokens. One FineWeb Hindi train part was checked directly: the sum of `n_tokens` is 65,435,402, `token_start` is contiguous from 0, and the paired `.uint16` is 130,870,804 bytes (exactly two bytes per token). The matching val part also matches.

`manifest.json` records `tokenizer_sha256` `bd790ad3d95b3a02abe6ddc0ca6546e062412fd2a2a46e639540f6b55746c6b7`, which is the frozen `tokenizer-65k.json` (65,536-piece BPE). `sampling_fraction` is 1.0 on these rows. `tokens_removed` is 0. The selection-policy targets do not include these three sources.

Grand total: **96.0B** (**96,043,927,930** tokens) across **347,925,875** kept documents.

| Dataset | Tokens | Billions | Documents |
|---|---:|---:|---:|
| FineWeb-2 Indic | 37,065,739,559 | 37.1 | 53,205,754 |
| IndicCorp v2 | 19,082,131,730 | 19.1 | 237,423,958 |
| Sangraha verified | 39,896,056,641 | 39.9 | 57,296,163 |
| **All three** | **96,043,927,930** | **96.0** | **347,925,875** |

Val holdout is inside those totals: FineWeb-2 10,300,598 tokens, IndicCorp v2 1,155,338, Sangraha verified 9,701,494.

## FineWeb-2 Indic

Source folders read into `fineweb2/{hin,ben,tam,tel,kan,mar,guj}`: `datasets/fineweb2-indic/{hin_Deva,ben_Beng,tam_Taml,tel_Telu,kan_Knda,mar_Deva,guj_Gujr}/`. `documents_dropped` is empty. No documents were skipped by sampling.

| Language | Folder | Files | Documents | Tokens | Billions |
|---|---|---:|---:|---:|---:|
| Hindi | `hin_Deva` | 8 | 22,095,985 | 14,664,401,238 | 14.7 |
| Bengali | `ben_Beng` | 5 | 15,185,742 | 10,853,821,251 | 10.9 |
| Tamil | `tam_Taml` | 2 | 5,528,854 | 3,972,809,339 | 4.0 |
| Telugu | `tel_Telu` | 1 | 1,964,395 | 1,804,985,151 | 1.8 |
| Kannada | `kan_Knda` | 1 | 2,390,982 | 1,573,667,939 | 1.6 |
| Marathi | `mar_Deva` | 2 | 3,912,702 | 2,595,503,501 | 2.6 |
| Gujarati | `guj_Gujr` | 1 | 2,127,094 | 1,600,551,140 | 1.6 |
| **Seven native** |  | 20 | 53,205,754 | **37,065,739,559** | **37.1** |

Latin-script text exists and was not tokenized. These prefixes have parquet and no bins: `hin_Latn`, `ben_Latn`, `tam_Latn`, `tel_Latn`, `kan_Latn`, `mar_Latn`, `guj_Latn`. Their token count is missing, not zero.

## IndicCorp v2

Source folders read into `indiccorp-v2/{hin,ben,tam,tel,kan,mar,guj}`: `datasets/indiccorp-v2/{hin_Deva,ben_Beng,tam_Taml,tel_Telu,kan_Knda,mar_Deva,guj_Gujr}/`. There is no Latin-script folder under this prefix.

| Language | Folder | Files | Documents | Tokens | Billions |
|---|---|---:|---:|---:|---:|
| Hindi | `hin_Deva` | 3 | 106,391,910 | 8,598,473,855 | 8.6 |
| Bengali | `ben_Beng` | 1 | 20,502,396 | 1,861,152,984 | 1.9 |
| Tamil | `tam_Taml` | 1 | 14,369,238 | 1,179,759,699 | 1.2 |
| Telugu | `tel_Telu` | 1 | 21,458,261 | 1,886,816,677 | 1.9 |
| Kannada | `kan_Knda` | 1 | 33,632,540 | 2,245,371,670 | 2.2 |
| Marathi | `mar_Deva` | 1 | 19,271,293 | 1,515,965,336 | 1.5 |
| Gujarati | `guj_Gujr` | 1 | 21,798,320 | 1,794,591,509 | 1.8 |
| **Seven native** |  | 9 | 237,423,958 | **19,082,131,730** | **19.1** |

On every IndicCorp language, `documents_dropped.empty` equals `documents_kept` (237,423,958 in total). That field is not an extra pile of dropped documents. It was not added to or subtracted from the totals above.

## Sangraha verified

Source folders read into `sangraha-verified/{hin,ben,tam,tel,kan,mar,guj}`: `datasets/sangraha/verified/{hin,ben,tam,tel,kan,mar,guj}/`. Verified has no Latin-script split. Other Sangraha trees (`synthetic/`, `unverified/`, and verified languages outside these seven, including `eng`) are not in this total.

| Language | Folder | Files | Documents | Tokens | Billions |
|---|---|---:|---:|---:|---:|
| Hindi | `hin` | 100 | 17,420,923 | 11,018,433,554 | 11.0 |
| Bengali | `ben` | 77 | 11,497,008 | 9,477,011,253 | 9.5 |
| Tamil | `tam` | 53 | 7,828,454 | 5,447,566,137 | 5.4 |
| Telugu | `tel` | 41 | 7,081,734 | 4,698,361,415 | 4.7 |
| Kannada | `kan` | 21 | 3,632,341 | 2,341,566,193 | 2.3 |
| Marathi | `mar` | 34 | 5,865,617 | 3,593,008,562 | 3.6 |
| Gujarati | `guj` | 27 | 3,970,086 | 3,320,109,527 | 3.3 |
| **Seven native** |  | 353 | 57,296,163 | **39,896,056,641** | **39.9** |

`documents_dropped.empty` is 95 documents (Hindi 9, Bengali 13, Tamil 58, Kannada 4, Gujarati 11). Telugu and Marathi record none. Those 95 are not in `documents_kept`.
