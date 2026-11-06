# Indic specialized token counts

Full sum of `token_count` from every `.tokens.index.jsonl` under `s3://nemotron-training-data-us-east-1/datasets/nemotron-indic-specialized-v1/`.

Counted at 2026-10-31 23:01:28 UTC+05:30 (Asia/Calcutta). Each index line is one source document. The total for a file is the sum of its `token_count` fields. These are the stored token ids. No `<eod>` is added.

Index files summed: 8,768 of 8,768. Failed files: 0. On every file the first `token_start` is 0 and the last `token_start` + `token_count` equals the sum of `token_count`.

Grand total: **142,351,065,175** tokens across 88,275,650 documents.

## Tokens per language

Language is the config folder. Native-script folders are listed first, then Latin.

| Language | Index files | Documents | Tokens |
|---|---:|---:|---:|
| `hi-Deva-IN` | 844 | 12,041,387 | 19,176,844,381 |
| `bn-Beng-IN` | 1,542 | 11,685,514 | 18,279,140,222 |
| `ta-Taml-IN` | 2,003 | 11,735,355 | 18,702,134,908 |
| `te-Telu-IN` | 926 | 11,969,113 | 19,504,597,269 |
| `kn-Knda-IN` | 986 | 11,056,436 | 17,386,456,751 |
| `mr-Deva-IN` | 868 | 11,778,571 | 17,787,143,990 |
| `gu-Gujr-IN` | 904 | 11,738,710 | 18,735,991,918 |
| **Seven native** | 8,073 | 82,005,086 | **129,572,309,439** |
| `hi-Latn-IN` | 35 | 861,415 | 2,090,559,781 |
| `bn-Latn-IN` | 47 | 1,053,422 | 1,784,202,292 |
| `ta-Latn-IN` | 183 | 835,159 | 1,896,268,350 |
| `te-Latn-IN` | 178 | 882,427 | 1,835,346,515 |
| `kn-Latn-IN` | 174 | 787,511 | 1,856,520,337 |
| `mr-Latn-IN` | 39 | 859,485 | 1,624,977,918 |
| `gu-Latn-IN` | 39 | 991,145 | 1,690,880,543 |
| **Seven Latin** | 695 | 6,270,564 | **12,778,755,736** |
| **All fourteen** | 8,768 | 88,275,650 | **142,351,065,175** |
