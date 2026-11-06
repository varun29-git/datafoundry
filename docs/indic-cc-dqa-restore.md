# High-Quality-DQA restore

`nvidia/Nemotron-CC-v2.1` / `High-Quality-DQA` / `cc_v21_hq_dqa` is restored under `s3://nemotron-training-data-us-east-1/datasets/nemotron-indic-cc-v1/<lang>/nvidia/Nemotron-CC-v2.1/High-Quality-DQA/<original shard filename>`.

Instance `i-0c59043472bed30b0` was an on-demand `c7i.24xlarge` in `us-east-1a` with a 1 TB gp3 volume (16,000 IOPS, 1,000 MB/s). It shut itself down after the seven languages summed to 17,425,910 rows. AWS recorded that stop as an instance-initiated shutdown, and the instance is terminated. The eight running `indic-cc-tokenize` instances were not stopped or resized.

Kannada was the first language to match the census: 2,326,859 rows, 256 objects, 13,984,118,083 bytes.

## Census

Every restored parquet was read back. Each file contains only `_source_repo=nvidia/Nemotron-CC-v2.1`, `_source_config=High-Quality-DQA`, and `_subset_key=cc_v21_hq_dqa`. Files that failed that check: 0.

| Language | Objects | Bytes | Rows | Census | Difference |
|---|---:|---:|---:|---:|---:|
| `hi-Deva-IN` | 226 | 14,983,481,314 | 2,576,297 | 2,576,297 | 0 |
| `bn-Beng-IN` | 316 | 14,403,829,093 | 2,467,621 | 2,467,621 | 0 |
| `ta-Taml-IN` | 414 | 15,115,511,117 | 2,427,516 | 2,427,516 | 0 |
| `te-Telu-IN` | 243 | 15,114,887,601 | 2,535,023 | 2,535,023 | 0 |
| `kn-Knda-IN` | 256 | 13,984,118,083 | 2,326,859 | 2,326,859 | 0 |
| `mr-Deva-IN` | 219 | 15,218,529,851 | 2,571,682 | 2,571,682 | 0 |
| `gu-Gujr-IN` | 230 | 14,605,187,013 | 2,520,912 | 2,520,912 | 0 |
| **Total** | **1,904** | **103,425,544,072** | **17,425,910** | **17,425,910** | **0** |

Census matched: yes.
