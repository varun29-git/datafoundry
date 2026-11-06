# High-Quality-DQA token counts

Full sum of `tokens` from every stats record under `s3://nemotron-training-data-us-east-1/ops/indic-cc-dqa-tokenize-20261101/stats/`. Each record is one restored parquet of `nvidia/Nemotron-CC-v2.1` / `High-Quality-DQA` / `cc_v21_hq_dqa`. The ids are the sibling `<basename>.tokens.uint16` beside that parquet, with `<basename>.tokens.index.jsonl`. No `<eod>` is added.

Counted at 2026-11-01 16:19:56 UTC. Stats records: 1,904 of 1,904. Failed files: 0. On every file the uint16 object is exactly two bytes per `tokens`. Document counts match the restore census on every language.

Grand total: **25,546,894,943** tokens across **17,425,910** documents.

## Tokens per language

Language is the config folder under `datasets/nemotron-indic-cc-v1/`.

| Language | Objects | Documents | Tokens |
|---|---:|---:|---:|
| `hi-Deva-IN` | 226 | 2,576,297 | 3,710,883,135 |
| `bn-Beng-IN` | 316 | 2,467,621 | 3,561,623,454 |
| `ta-Taml-IN` | 414 | 2,427,516 | 3,558,005,192 |
| `te-Telu-IN` | 243 | 2,535,023 | 3,826,993,087 |
| `kn-Knda-IN` | 256 | 2,326,859 | 3,557,937,368 |
| `mr-Deva-IN` | 219 | 2,571,682 | 3,629,897,801 |
| `gu-Gujr-IN` | 230 | 2,520,912 | 3,701,554,906 |
| **All seven** | **1,904** | **17,425,910** | **25,546,894,943** |
