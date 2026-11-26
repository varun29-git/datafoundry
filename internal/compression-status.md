# Compression-ratio status

Checked 2026-10-04. Existing scores were not recomputed. Per-document score files are in the training bucket. This Mac has the scorer source only, not the score parquets.

## Definition on the finished sets

The finished scores are zstd, not the gzip bands in `docs/sota-curriculum.md`.

Source script, stored next to the scores and matching `scripts/score_compression_zstd3.py` on this Mac:

- Codec: zstd level 3. No dictionary.
- Field: UTF-8 bytes of the `text` column only.
- Ratio: `utf8_bytes / zstd_bytes` (original divided by compressed). Stored values are above 1. A FineWeb 2 Gujarati score file has ratio min 1.40 and max 5.73. A ClimbMix score file has ratio min 1.02 and max 16.84, and `utf8_bytes` min 200.
- Documents under 200 UTF-8 bytes are skipped, not banded.
- Columns: `dataset`, `lang`, `family`, `source_key`, `doc_index`, `utf8_bytes`, `zstd_bytes`, `ratio`.

There is no easy/mid/hard column on these files. The sheet’s gzip cuts (compressed/original, easy under 35%, mid 35% through 65% including both ends, hard over 65%, documents under 512 bytes forced to mid) are a different rule. A zstd ratio cannot be dropped into those cuts.

Prefix:

`s3://<research-data-bucket>/translation-staging/Cosmopedia-v2/Krutrim-decoupled/compression-zstd3/20261002/`

`inputs/` under that prefix is a staged copy of source parquet (824 objects, 633,719,368,369 bytes), not a second score.

## Curriculum datasets that already have scores

Object counts match the 2026-10-02 launch manifest. These are complete.

| Dataset | Score objects | Source files in the manifest | Score prefix |
| --- | ---: | ---: | --- |
| ClimbMix | 6,543 | 6,543 | `dataset=climbmix/` |
| Nemotron Math 4+ | 46 | 46 | `dataset=nemotron-math-4plus/` |
| Nemotron MIND | 90 | 90 | `dataset=nemotron-mind/` |
| Nemotron RQA | 175 | 175 | `dataset=rqa/` |
| Nemotron Fact-Seeking | 72 | 72 | `dataset=fact-seeking/` |
| Nemotron Specialized v1.1 | 68 | 68 | `dataset=specialized-v1.1/` |
| Sangraha verified Hindi | 100 | 100 | `dataset=sangraha-hin/` |
| Sangraha verified Bengali | 77 | 77 | `dataset=sangraha-ben/` |
| Sangraha verified Tamil | 53 | 53 | `dataset=sangraha-tam/` |
| Sangraha verified Telugu | 41 | 41 | `dataset=sangraha-tel/` |
| Sangraha verified Kannada | 21 | 21 | `dataset=sangraha-kan/` |
| Sangraha verified Marathi | 34 | 34 | `dataset=sangraha-mar/` |
| Sangraha verified Gujarati | 27 | 27 | `dataset=sangraha-guj/` |
| FineWeb 2 Hindi | 8 | 8 | `dataset=fineweb2-hin/` |
| FineWeb 2 Bengali | 5 | 5 | `dataset=fineweb2-ben/` |
| FineWeb 2 Tamil | 2 | 2 | `dataset=fineweb2-tam/` |
| FineWeb 2 Telugu | 1 | 1 | `dataset=fineweb2-tel/` |
| FineWeb 2 Kannada | 1 | 1 | `dataset=fineweb2-kan/` |
| FineWeb 2 Marathi | 2 | 2 | `dataset=fineweb2-mar/` |
| FineWeb 2 Gujarati | 1 | 1 | `dataset=fineweb2-guj/` |

ClimbMix is done. The Nemotron sets that were in that run are done: Math 4+, MIND, RQA, Fact-Seeking, and Specialized v1.1.

## Curriculum datasets with no compression-ratio output

| Dataset | What is missing |
| --- | --- |
| Nemotron InfiniByte | 30 parquet files are in the bucket. They were not in the score manifest. |
| Nemotron Code v2 | Not in the zstd run. Gzip scores for the new slice cover the whole prefix. |
| Nemotron-CC v2.1 HQ synthetic text | No text prefix. The TinyLlama pack was not in this score run. |
| CodeAlchemy | Not in the zstd run. Gzip scores for the new slice cover the whole prefix. |
| Genesis III | Not in the zstd run. Gzip scores for the new slice cover the whole prefix. |
| IndicCorp v2 | Not in the zstd run. Gzip scores for the new slice cover the whole prefix. |
| BhashaWiki | Not in the zstd run. Gzip scores for the new slice cover the whole prefix. |
| Sangraha synthetic and unverified | Not in the score manifest. Verified seven languages are scored. |
| Cosmopedia translations | Not in this score prefix. |
| Indic HQ-synthetic translations | Not in this score prefix. |
| Indic Fact-Seeking translations | Not in this score prefix. |

Other Nemotron prefixes in the bucket were also outside that run: `datasets/nemotron-cc-v2/Diverse-QA/`, `datasets/nemotron-cc-hq/`, `datasets/nemotron-cc-math-v1/3/`, and the Specialized v1 subsets Math Textbooks, Wiki-Rewrite, Scientific-Coding, and STEM-SFT.

## Gzip scores for the five slices

These use the sheet rule, not the zstd scores above. gzip level 6, `mtime=0`, ratio = compressed/original, easy under 35%, mid 35% through 65% including both ends, hard over 65%. Documents under 512 UTF-8 bytes are mid. Empty text is skipped. Per-document ratios sit beside each prefix under `gzip6/`.

Scoring of the two unfinished prefixes finished at 2026-10-04T06:09:31Z. Files that already had a ratio parquet were not scored again. Counts below match `gzip6/band-summary.json` in the bucket.

| Dataset | Prefix | State |
| --- | --- | --- |
| CodeAlchemy | `datasets/codealchemy/` | scored, whole prefix (34/34) |
| Nemotron Code v2 | `datasets/nemotron-code-v2/` | scored, whole prefix (30/30) |
| Genesis III | `datasets/genesis-iii/` | scored, whole prefix (89/89) |
| IndicCorp v2 | `datasets/indiccorp-v2/` | scored, whole prefix (9/9) |
| BhashaWiki | `datasets/bhashawiki/` | scored, whole prefix (55/55) |

### CodeAlchemy

`datasets/codealchemy/gzip6/`. 34 of 34 files. `text` where that column exists, otherwise `text_with_placeholders` (code-dialogue). Documents under 512 bytes are mid. Ratio is gzip level 6 compressed/original.

| Band | Documents | UTF-8 bytes |
| --- | ---: | ---: |
| easy | 3,995,798 | 127,654,171,446 |
| mid | 1,160,709 | 11,670,193,986 |
| hard | 207 | 126,079 |
| total | 5,156,714 | 139,324,491,511 |

### Nemotron Code v2

`datasets/nemotron-code-v2/gzip6/`. 30 of 30 files. Column `content`. Documents under 512 bytes are mid. Ratio is gzip level 6 compressed/original.

| Band | Documents | UTF-8 bytes |
| --- | ---: | ---: |
| easy | 11,082,536 | 51,531,116,287 |
| mid | 49,004,639 | 124,219,419,919 |
| hard | 12,114 | 7,999,313 |
| total | 60,099,289 | 175,758,535,519 |

### Genesis III

`datasets/genesis-iii/gzip6/`. 89 of 89 files. Column `text`. Train shards mix option-level and failure-analysis rows, and both were scored. Documents under 512 bytes are mid. Ratio is gzip level 6 compressed/original.

| Band | Documents | UTF-8 bytes |
| --- | ---: | ---: |
| easy | 629,473 | 5,400,845,106 |
| mid | 37,968,808 | 188,857,566,889 |
| hard | 2,202 | 1,339,908 |
| total | 38,600,483 | 194,259,751,903 |

### IndicCorp v2

`datasets/indiccorp-v2/gzip6/`. 9 of 9 files. Each non-empty line is a document. Documents under 512 bytes are mid. Ratio is gzip level 6 compressed/original.

| Band | Documents | UTF-8 bytes |
| --- | ---: | ---: |
| easy | 26,819,121 | 66,367,292,123 |
| mid | 210,604,662 | 104,951,539,820 |
| hard | 177 | 98,088 |
| total | 237,423,960 | 171,318,930,031 |

### BhashaWiki

`datasets/bhashawiki/gzip6/`. 55 of 55 files. Column `text`. Documents under 512 bytes are mid. Ratio is gzip level 6 compressed/original.

| Band | Documents | UTF-8 bytes |
| --- | ---: | ---: |
| easy | 793,099 | 9,082,265,046 |
| mid | 211,001 | 165,896,366 |
| hard | 0 | 0 |
| total | 1,004,100 | 9,248,161,412 |
