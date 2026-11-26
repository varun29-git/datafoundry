# Indic CC native segment counts

Document rows already stored under `s3://<research-data-bucket>/datasets/nemotron-indic-cc-v1/` for the seven native configs. Latin configs were not scanned.

Counted at 2026-10-31 16:43:09 UTC+05:30 (Asia/Calcutta) by projecting `_source_repo`, `_source_config`, and `_subset_key` from each parquet file. The text column was not read. Nothing was tokenized. No token count is given.

Language is the config folder. Segment is `_source_repo`. Subsegment is `_source_config`. One document is one parquet row.

Files scanned: 28,030 of 28,030. Failed files: 0.

## Documents by language, segment, and subsegment

| Language | Segment | Subsegment | `_subset_key` | Documents |
|---|---|---|---|---:|
| `hi-Deva-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | `finepdfs_edu_eng_latn` | 2,133,856 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | `cc_v2_diverse_qa` | 34,550,914 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | `cc_v2_english_cc` | 54,167,556 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | `cc_v2_medium_high_quality` | 22,347,938 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | `cc_v21_hq_organic` | 5,755,969 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | `cc_v21_hq_dqa` | 2,576,297 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | `cc_v21_hq_synthetic` | 8,020,039 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | `cc_v21_medium_high_quality` | 1,420,033 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | `cc_v21_medium_high_quality_synthetic` | 5,576,781 |
| `bn-Beng-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | `finepdfs_edu_eng_latn` | 2,083,701 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | `cc_v2_diverse_qa` | 32,618,682 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | `cc_v2_english_cc` | 52,680,871 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | `cc_v2_medium_high_quality` | 22,146,323 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | `cc_v21_hq_organic` | 5,592,744 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | `cc_v21_hq_dqa` | 2,467,621 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | `cc_v21_hq_synthetic` | 7,798,514 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | `cc_v21_medium_high_quality` | 1,410,246 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | `cc_v21_medium_high_quality_synthetic` | 5,520,371 |
| `ta-Taml-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | `finepdfs_edu_eng_latn` | 2,392,466 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | `cc_v2_diverse_qa` | 32,772,840 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | `cc_v2_english_cc` | 51,001,321 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | `cc_v2_medium_high_quality` | 20,921,868 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | `cc_v21_hq_organic` | 5,463,617 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | `cc_v21_hq_dqa` | 2,427,516 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | `cc_v21_hq_synthetic` | 7,594,735 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | `cc_v21_medium_high_quality` | 1,217,942 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | `cc_v21_medium_high_quality_synthetic` | 4,520,882 |
| `te-Telu-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | `finepdfs_edu_eng_latn` | 2,563,395 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | `cc_v2_diverse_qa` | 33,735,595 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | `cc_v2_english_cc` | 51,844,882 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | `cc_v2_medium_high_quality` | 21,800,442 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | `cc_v21_hq_organic` | 5,642,841 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | `cc_v21_hq_dqa` | 2,535,023 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | `cc_v21_hq_synthetic` | 7,875,780 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | `cc_v21_medium_high_quality` | 1,390,373 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | `cc_v21_medium_high_quality_synthetic` | 5,386,316 |
| `kn-Knda-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | `finepdfs_edu_eng_latn` | 1,452,572 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | `cc_v2_diverse_qa` | 31,742,869 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | `cc_v2_english_cc` | 49,537,093 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | `cc_v2_medium_high_quality` | 20,231,602 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | `cc_v21_hq_organic` | 5,310,335 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | `cc_v21_hq_dqa` | 2,326,859 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | `cc_v21_hq_synthetic` | 7,360,113 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | `cc_v21_medium_high_quality` | 1,290,010 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | `cc_v21_medium_high_quality_synthetic` | 4,983,728 |
| `mr-Deva-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | `finepdfs_edu_eng_latn` | 826,925 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | `cc_v2_diverse_qa` | 33,968,944 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | `cc_v2_english_cc` | 53,958,551 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | `cc_v2_medium_high_quality` | 22,226,393 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | `cc_v21_hq_organic` | 5,711,919 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | `cc_v21_hq_dqa` | 2,571,682 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | `cc_v21_hq_synthetic` | 8,021,672 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | `cc_v21_medium_high_quality` | 1,417,478 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | `cc_v21_medium_high_quality_synthetic` | 5,531,761 |
| `gu-Gujr-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | `finepdfs_edu_eng_latn` | 2,031,099 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | `cc_v2_diverse_qa` | 34,033,849 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | `cc_v2_english_cc` | 53,492,720 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | `cc_v2_medium_high_quality` | 22,008,322 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | `cc_v21_hq_organic` | 5,629,553 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | `cc_v21_hq_dqa` | 2,520,912 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | `cc_v21_hq_synthetic` | 7,940,029 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | `cc_v21_medium_high_quality` | 1,400,858 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | `cc_v21_medium_high_quality_synthetic` | 5,486,539 |

## Totals per language

| Language | Files | Documents |
|---|---:|---:|
| `hi-Deva-IN` | 4,806 | 136,549,383 |
| `bn-Beng-IN` | 777 | 132,319,073 |
| `ta-Taml-IN` | 779 | 128,313,187 |
| `te-Telu-IN` | 5,311 | 132,774,647 |
| `kn-Knda-IN` | 6,263 | 124,235,181 |
| `mr-Deva-IN` | 4,888 | 134,235,325 |
| `gu-Gujr-IN` | 5,206 | 134,543,881 |
| **All seven** | **28,030** | **922,970,677** |

## Segments present

A segment is a distinct `_source_repo` value.

- `HuggingFaceFW/finepdfs-edu`
- `nvidia/Nemotron-CC-v2`
- `nvidia/Nemotron-CC-v2.1`

No language is missing a segment. Every native folder contains the same set of `_source_repo` values.

No language is missing a subsegment. Every native folder contains the same set of `_source_config` values.

## `_subset_key`

- `Diverse-QA` maps to 1 `_subset_key` value(s): `cc_v2_diverse_qa`.
- `High-Quality` maps to 2 `_subset_key` value(s): `cc_v21_hq_organic`, `cc_v2_english_cc`.
- `High-Quality-DQA` maps to 1 `_subset_key` value(s): `cc_v21_hq_dqa`.
- `High-Quality-Synthetic` maps to 1 `_subset_key` value(s): `cc_v21_hq_synthetic`.
- `Medium-High-Quality` maps to 2 `_subset_key` value(s): `cc_v21_medium_high_quality`, `cc_v2_medium_high_quality`.
- `Medium-High-Quality-Synthetic` maps to 1 `_subset_key` value(s): `cc_v21_medium_high_quality_synthetic`.
- `eng_Latn` maps to 1 `_subset_key` value(s): `finepdfs_edu_eng_latn`.
