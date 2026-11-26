# FineWeb-2 Latin token counts

Full sum of `token_count` from every `.tokens.index.jsonl` under the seven Latin prefixes of `s3://<research-data-bucket>/datasets/fineweb2-indic/`.

Each prefix has one parquet, `train/000_00000.parquet`. The ids are the sibling `000_00000.tokens.uint16`, with `000_00000.tokens.index.jsonl`. An index line is `uuid` (the parquet `id`), `token_start`, and `token_count`. No `<eod>` was added.

Counted from those index files at 2026-11-02 12:53:56 UTC+05:30 (Asia/Calcutta). Stats records: 7 of 7, under `ops/indic-fineweb2-latin-tokenize-20261102/stats/`. Failed files: 0. On every file the first `token_start` is 0, `token_start` is contiguous, the last `token_start` + `token_count` equals the sum of `token_count`, and the uint16 object is exactly two bytes per token.

Grand total: **311,404,717** tokens across **139,953** documents. Files: **7**.

The curriculum figure 37,221,244,264 is an unmeasured budget. It is not this sum.

## Tokens per language

| Language | Folder | Files | Documents | Tokens |
|---|---|---:|---:|---:|
| Hindi | `hin_Latn` | 1 | 97,024 | 213,997,119 |
| Bengali | `ben_Latn` | 1 | 10,458 | 32,304,488 |
| Tamil | `tam_Latn` | 1 | 4,828 | 14,567,775 |
| Telugu | `tel_Latn` | 1 | 24,103 | 43,769,009 |
| Kannada | `kan_Latn` | 1 | 1,070 | 2,238,695 |
| Marathi | `mar_Latn` | 1 | 1,757 | 3,069,278 |
| Gujarati | `guj_Latn` | 1 | 713 | 1,458,353 |
| **Seven Latin** |  | **7** | **139,953** | **311,404,717** |

## Encode

Python NFC and the same Indic normalizer regexes as the Indic CC worker, then `encode_batch` with `normalizer=None` on `docs/hf-tokenizer`. Ids were checked against `Tokenizer.encode(..., add_special_tokens=False)` before each file was uploaded: 26 documents, 0 mismatches. The only rejected id is one above 65535. None appeared. Content ids are little-endian `uint16`.

No EC2 instance was started. The ten already-stopped instances were left stopped. No spot request was opened.
