---
cursor:
  subagentId: "bc-c3501724-2fcf-5456-8549-668a4adbdd33"
---

# Dataset fetch

Cloud-to-cloud copy onto `s3://nemotron-training-data-us-east-1/` from `i-0676987ec61af5f49` (`tokenizer-65k`, m7i.8xlarge, us-east-1). `i-0c6550d199294585f` stayed stopped. Nothing was written under `tokenized/` or under a `datasets/` prefix that already existed.

Counts below are data objects only. `gzip6/` score objects are separate and are recorded in `internal/compression-status.md`.

## Landed

| Prefix | Objects | Bytes | What was copied |
| --- | ---: | ---: | --- |
| `datasets/codealchemy/` | 34 | 36,538,476,879 | 40B-token slice of `open-alchemy/code-alchemy` (976.6B). Evenly spaced shards: code-dev 10, code-dialogue 19, code-enhance 4, code-qa 1. Code-trace was left out: its smallest file is about 1.06 GB, several times that subset’s 0.26B share of the slice. |
| `datasets/bhashawiki/` | 55 | 3,363,358,082 | All of `soketlabs/bhasha-wiki-indic` for Hindi, Bengali, Tamil, Kannada, and Gujarati. English and Urdu were not copied. Telugu and Marathi are not in that dataset. The five-language source is under the 13.61B sheet cell, so the whole source was taken. |
| `datasets/nemotron-code-v2/` | 30 | 83,081,560,228 | Gated `nvidia/Nemotron-Pretraining-Code-v2`, synthetic splits only. A 200-row sample put the five splits near 473B tokens. Six evenly spaced files per split. GitHub metadata was not copied. |
| `datasets/genesis-iii/` | 89 | 58,450,933,823 | `qvac/GenesisIII`. Train shards mix `option_level` and `failure_analysis` in the same file, so whole files were stored. About 52/191.43 of the train bytes, spread across domains. Preview files were not copied. |
| `datasets/indiccorp-v2/` | 9 | 171,793,777,944 | Seven languages of `ai4bharat/IndicCorpV2`: Hindi (`hi-1.txt`, `hi-2.txt`, `hi-3.txt`), Bengali, Tamil, Telugu, Kannada, Marathi, Gujarati. Other languages were not copied. Each language is one file, or three equal Hindi files, so the files were stored whole. |

Copies were not repeated. The halted scorer was resumed only for objects that had no gzip6 ratio parquet. It finished at 2026-10-04T06:09:31Z. Every data object under the five prefixes now has a ratio parquet and a meta file. `i-0676987ec61af5f49` is stopped, not terminated. `i-0c6550d199294585f` stayed stopped. Band counts are in `internal/compression-status.md`.
