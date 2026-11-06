# Indic CC token projection

Projected token counts for the seven native configs in `s3://nemotron-training-data-us-east-1/datasets/nemotron-indic-cc-v1/`. Latin configs were not read. `datasets/nemotron-indic-specialized-v1/` was not read.

Sampled at 2026-10-31 18:29:16 UTC+05:30 (Asia/Calcutta). Each cell is one language, one `_source_repo`, and one `_source_config`, the same cells as `docs/indic-cc-segment-counts.md`. At least 200 documents were encoded per cell. This sample did not wait for the folder move. It read objects that were already under that prefix, using the flat key when the original was still there and the moved key when the arrange writer had already copied that file.

Files are spread across each cell. Five files are used when the cell has that many, otherwise every file that contains the cell. A pure file contributes a prefix of its documents and reading stops at that file's share of the 200. A mixed file contributes a prefix of one row group, chosen from the middle of the row groups whose footer statistics are that segment and subsegment. Other row groups are not decoded. The text column was encoded with the stock tokenizer at `docs/hf-tokenizer` (`tokenizer.json`, vocab 65,536). That file has no post-processor, and `tokenizer_config.json` sets `add_bos_token` and `add_eos_token` to false, so these counts do not add `<s>` or `</s>`. Token id 4 (`<eod>`) is added once after each encoded document, and nowhere else. Null text is skipped and is not counted as a document.

Every token figure below is a projection from that sample, not a full token census. Projected tokens = (sample token sum / sample documents) × the document count from `docs/indic-cc-segment-counts.md`. No token count was filled in without a sample.

Cells: 63. Sample documents: 12,600. Files read: 315. Null text rows skipped: 0.

## Projected tokens: `nvidia/Nemotron-CC-v2`

Each value is the sample average multiplied by the census document count, rounded to the nearest token. The row total is the sum of the unrounded cell projections, then rounded.

| Language | `Diverse-QA` | `High-Quality` | `Medium-High-Quality` | Total |
|---|---:|---:|---:|---:|
| `hi-Deva-IN` | 24,843,489,203 | 41,382,116,920 | 19,695,796,458 | 85,921,402,580 |
| `bn-Beng-IN` | 22,543,097,317 | 41,666,617,896 | 23,444,983,381 | 87,654,698,593 |
| `ta-Taml-IN` | 27,454,299,661 | 39,086,392,388 | 15,393,787,428 | 81,934,479,476 |
| `te-Telu-IN` | 28,040,689,208 | 35,674,981,753 | 16,857,845,790 | 80,573,516,751 |
| `kn-Knda-IN` | 26,990,802,796 | 34,231,865,061 | 13,395,849,474 | 74,618,517,332 |
| `mr-Deva-IN` | 23,771,467,011 | 40,325,923,090 | 17,985,597,216 | 82,082,987,317 |
| `gu-Gujr-IN` | 27,443,534,480 | 42,761,277,977 | 17,265,748,692 | 87,470,561,149 |
| **All seven** | 181,087,379,675 | 275,129,175,085 | 124,039,608,438 | **580,256,163,198** |

### Sample size

Documents encoded. This is the sample size, not the census document count.

| Language | `Diverse-QA` | `High-Quality` | `Medium-High-Quality` | Total |
|---|---:|---:|---:|---:|
| `hi-Deva-IN` | 200 | 200 | 200 | 600 |
| `bn-Beng-IN` | 200 | 200 | 200 | 600 |
| `ta-Taml-IN` | 200 | 200 | 200 | 600 |
| `te-Telu-IN` | 200 | 200 | 200 | 600 |
| `kn-Knda-IN` | 200 | 200 | 200 | 600 |
| `mr-Deva-IN` | 200 | 200 | 200 | 600 |
| `gu-Gujr-IN` | 200 | 200 | 200 | 600 |
| **All seven** | 1,400 | 1,400 | 1,400 | **4,200** |

### Average tokens per document

Sample mean tokens per document, including the one `<eod>` at the end of each document.

| Language | `Diverse-QA` | `High-Quality` | `Medium-High-Quality` |
|---|---:|---:|---:|
| `hi-Deva-IN` | 719.04 | 763.97 | 881.33 |
| `bn-Beng-IN` | 691.11 | 790.92 | 1058.64 |
| `ta-Taml-IN` | 837.72 | 766.38 | 735.77 |
| `te-Telu-IN` | 831.19 | 688.11 | 773.28 |
| `kn-Knda-IN` | 850.29 | 691.03 | 662.12 |
| `mr-Deva-IN` | 699.80 | 747.35 | 809.20 |
| `gu-Gujr-IN` | 806.36 | 799.38 | 784.51 |

## Projected tokens: `nvidia/Nemotron-CC-v2.1`

Each value is the sample average multiplied by the census document count, rounded to the nearest token. The row total is the sum of the unrounded cell projections, then rounded.

| Language | `High-Quality` | `High-Quality-DQA` | `High-Quality-Synthetic` | `Medium-High-Quality` | `Medium-High-Quality-Synthetic` | Total |
|---|---:|---:|---:|---:|---:|---:|
| `hi-Deva-IN` | 5,011,491,970 | 3,667,139,794 | 9,091,035,008 | 1,255,813,284 | 5,367,344,990 | 24,392,825,045 |
| `bn-Beng-IN` | 5,115,682,937 | 3,686,662,788 | 7,200,601,932 | 1,415,181,861 | 4,799,106,927 | 22,217,236,445 |
| `ta-Taml-IN` | 4,861,225,908 | 3,557,209,121 | 7,014,914,956 | 1,067,617,509 | 3,845,281,394 | 20,346,248,888 |
| `te-Telu-IN` | 5,221,066,849 | 3,973,280,974 | 6,215,526,197 | 1,409,796,511 | 4,653,965,545 | 21,473,636,077 |
| `kn-Knda-IN` | 4,433,811,105 | 3,573,962,350 | 5,579,039,255 | 1,078,241,958 | 3,628,502,845 | 18,293,557,513 |
| `mr-Deva-IN` | 5,540,561,430 | 3,811,039,848 | 9,871,750,322 | 1,322,336,877 | 4,457,244,085 | 25,002,932,561 |
| `gu-Gujr-IN` | 4,630,616,968 | 3,713,076,494 | 7,464,262,462 | 1,304,822,180 | 5,440,918,428 | 22,553,696,532 |
| **All seven** | 34,814,457,166 | 25,982,371,369 | 52,437,130,132 | 8,853,810,179 | 32,192,364,213 | **154,280,133,060** |

### Sample size

Documents encoded. This is the sample size, not the census document count.

| Language | `High-Quality` | `High-Quality-DQA` | `High-Quality-Synthetic` | `Medium-High-Quality` | `Medium-High-Quality-Synthetic` | Total |
|---|---:|---:|---:|---:|---:|---:|
| `hi-Deva-IN` | 200 | 200 | 200 | 200 | 200 | 1,000 |
| `bn-Beng-IN` | 200 | 200 | 200 | 200 | 200 | 1,000 |
| `ta-Taml-IN` | 200 | 200 | 200 | 200 | 200 | 1,000 |
| `te-Telu-IN` | 200 | 200 | 200 | 200 | 200 | 1,000 |
| `kn-Knda-IN` | 200 | 200 | 200 | 200 | 200 | 1,000 |
| `mr-Deva-IN` | 200 | 200 | 200 | 200 | 200 | 1,000 |
| `gu-Gujr-IN` | 200 | 200 | 200 | 200 | 200 | 1,000 |
| **All seven** | 1,400 | 1,400 | 1,400 | 1,400 | 1,400 | **7,000** |

### Average tokens per document

Sample mean tokens per document, including the one `<eod>` at the end of each document.

| Language | `High-Quality` | `High-Quality-DQA` | `High-Quality-Synthetic` | `Medium-High-Quality` | `Medium-High-Quality-Synthetic` |
|---|---:|---:|---:|---:|---:|
| `hi-Deva-IN` | 870.66 | 1423.41 | 1133.54 | 884.36 | 962.45 |
| `bn-Beng-IN` | 914.70 | 1494.02 | 923.33 | 1003.50 | 869.35 |
| `ta-Taml-IN` | 889.75 | 1465.37 | 923.65 | 876.58 | 850.56 |
| `te-Telu-IN` | 925.25 | 1567.36 | 789.20 | 1013.97 | 864.03 |
| `kn-Knda-IN` | 834.94 | 1535.96 | 758.01 | 835.84 | 728.07 |
| `mr-Deva-IN` | 970.00 | 1481.92 | 1230.63 | 932.88 | 805.75 |
| `gu-Gujr-IN` | 822.55 | 1472.91 | 940.08 | 931.45 | 991.68 |

## Projected tokens: `HuggingFaceFW/finepdfs-edu`

Each value is the sample average multiplied by the census document count, rounded to the nearest token. The row total is the sum of the unrounded cell projections, then rounded.

| Language | `eng_Latn` | Total |
|---|---:|---:|
| `hi-Deva-IN` | 3,412,910,625 | 3,412,910,625 |
| `bn-Beng-IN` | 3,389,410,558 | 3,389,410,558 |
| `ta-Taml-IN` | 3,258,036,274 | 3,258,036,274 |
| `te-Telu-IN` | 4,431,892,066 | 4,431,892,066 |
| `kn-Knda-IN` | 2,203,159,530 | 2,203,159,530 |
| `mr-Deva-IN` | 1,402,158,838 | 1,402,158,838 |
| `gu-Gujr-IN` | 3,622,515,844 | 3,622,515,844 |
| **All seven** | 21,720,083,734 | **21,720,083,734** |

### Sample size

Documents encoded. This is the sample size, not the census document count.

| Language | `eng_Latn` | Total |
|---|---:|---:|
| `hi-Deva-IN` | 200 | 200 |
| `bn-Beng-IN` | 200 | 200 |
| `ta-Taml-IN` | 200 | 200 |
| `te-Telu-IN` | 200 | 200 |
| `kn-Knda-IN` | 200 | 200 |
| `mr-Deva-IN` | 200 | 200 |
| `gu-Gujr-IN` | 200 | 200 |
| **All seven** | 1,400 | **1,400** |

### Average tokens per document

Sample mean tokens per document, including the one `<eod>` at the end of each document.

| Language | `eng_Latn` |
|---|---:|
| `hi-Deva-IN` | 1599.41 |
| `bn-Beng-IN` | 1626.63 |
| `ta-Taml-IN` | 1361.79 |
| `te-Telu-IN` | 1728.91 |
| `kn-Knda-IN` | 1516.73 |
| `mr-Deva-IN` | 1695.63 |
| `gu-Gujr-IN` | 1783.53 |

## Cell detail

| Language | Segment (`_source_repo`) | Subsegment (`_source_config`) | Census documents | Files sampled | Sample documents | Average tokens | Projected tokens |
|---|---|---|---:|---:|---:|---:|---:|
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | 34,550,914 | 5 | 200 | 719.04 | 24843489202.6 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | 54,167,556 | 5 | 200 | 763.97 | 41382116919.5 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | 22,347,938 | 5 | 200 | 881.33 | 19695796457.9 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | 5,755,969 | 5 | 200 | 870.66 | 5011491969.5 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | 2,576,297 | 5 | 200 | 1423.41 | 3667139794.3 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | 8,020,039 | 5 | 200 | 1133.54 | 9091035008.1 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | 1,420,033 | 5 | 200 | 884.36 | 1255813283.7 |
| `hi-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | 5,576,781 | 5 | 200 | 962.45 | 5367344989.5 |
| `hi-Deva-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | 2,133,856 | 5 | 200 | 1599.41 | 3412910625.0 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | 32,618,682 | 5 | 200 | 691.11 | 22543097317.0 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | 52,680,871 | 5 | 200 | 790.92 | 41666617895.7 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | 22,146,323 | 5 | 200 | 1058.64 | 23444983380.7 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | 5,592,744 | 5 | 200 | 914.70 | 5115682936.8 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | 2,467,621 | 5 | 200 | 1494.02 | 3686662788.3 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | 7,798,514 | 5 | 200 | 923.33 | 7200601931.6 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | 1,410,246 | 5 | 200 | 1003.50 | 1415181861.0 |
| `bn-Beng-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | 5,520,371 | 5 | 200 | 869.35 | 4799106927.0 |
| `bn-Beng-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | 2,083,701 | 5 | 200 | 1626.63 | 3389410557.6 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | 32,772,840 | 5 | 200 | 837.72 | 27454299660.6 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | 51,001,321 | 5 | 200 | 766.38 | 39086392388.0 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | 20,921,868 | 5 | 200 | 735.77 | 15393787427.7 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | 5,463,617 | 5 | 200 | 889.75 | 4861225907.7 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | 2,427,516 | 5 | 200 | 1465.37 | 3557209120.9 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | 7,594,735 | 5 | 200 | 923.65 | 7014914956.4 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | 1,217,942 | 5 | 200 | 876.58 | 1067617508.7 |
| `ta-Taml-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | 4,520,882 | 5 | 200 | 850.56 | 3845281393.9 |
| `ta-Taml-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | 2,392,466 | 5 | 200 | 1361.79 | 3258036274.1 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | 33,735,595 | 5 | 200 | 831.19 | 28040689208.1 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | 51,844,882 | 5 | 200 | 688.11 | 35674981753.0 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | 21,800,442 | 5 | 200 | 773.28 | 16857845789.8 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | 5,642,841 | 5 | 200 | 925.25 | 5221066849.5 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | 2,535,023 | 5 | 200 | 1567.36 | 3973280974.2 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | 7,875,780 | 5 | 200 | 789.20 | 6215526197.1 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | 1,390,373 | 5 | 200 | 1013.97 | 1409796510.8 |
| `te-Telu-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | 5,386,316 | 5 | 200 | 864.03 | 4653965545.1 |
| `te-Telu-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | 2,563,395 | 5 | 200 | 1728.91 | 4431892066.4 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | 31,742,869 | 5 | 200 | 850.29 | 26990802796.4 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | 49,537,093 | 5 | 200 | 691.03 | 34231865061.3 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | 20,231,602 | 5 | 200 | 662.12 | 13395849474.2 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | 5,310,335 | 5 | 200 | 834.94 | 4433811104.9 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | 2,326,859 | 5 | 200 | 1535.96 | 3573962349.6 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | 7,360,113 | 5 | 200 | 758.01 | 5579039255.1 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | 1,290,010 | 5 | 200 | 835.84 | 1078241958.4 |
| `kn-Knda-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | 4,983,728 | 5 | 200 | 728.07 | 3628502845.0 |
| `kn-Knda-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | 1,452,572 | 5 | 200 | 1516.73 | 2203159529.6 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | 33,968,944 | 5 | 200 | 699.80 | 23771467011.2 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | 53,958,551 | 5 | 200 | 747.35 | 40325923089.8 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | 22,226,393 | 5 | 200 | 809.20 | 17985597215.6 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | 5,711,919 | 5 | 200 | 970.00 | 5540561430.0 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | 2,571,682 | 5 | 200 | 1481.92 | 3811039847.8 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | 8,021,672 | 5 | 200 | 1230.63 | 9871750321.7 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | 1,417,478 | 5 | 200 | 932.88 | 1322336876.6 |
| `mr-Deva-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | 5,531,761 | 5 | 200 | 805.75 | 4457244084.6 |
| `mr-Deva-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | 826,925 | 5 | 200 | 1695.63 | 1402158837.8 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2` | `Diverse-QA` | 34,033,849 | 5 | 200 | 806.36 | 27443534479.6 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2` | `High-Quality` | 53,492,720 | 5 | 200 | 799.38 | 42761277977.2 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2` | `Medium-High-Quality` | 22,008,322 | 5 | 200 | 784.51 | 17265748692.2 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality` | 5,629,553 | 5 | 200 | 822.55 | 4630616967.9 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-DQA` | 2,520,912 | 5 | 200 | 1472.91 | 3713076493.9 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2.1` | `High-Quality-Synthetic` | 7,940,029 | 5 | 200 | 940.08 | 7464262462.3 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality` | 1,400,858 | 5 | 200 | 931.45 | 1304822179.8 |
| `gu-Gujr-IN` | `nvidia/Nemotron-CC-v2.1` | `Medium-High-Quality-Synthetic` | 5,486,539 | 5 | 200 | 991.68 | 5440918428.2 |
| `gu-Gujr-IN` | `HuggingFaceFW/finepdfs-edu` | `eng_Latn` | 2,031,099 | 5 | 200 | 1783.53 | 3622515844.0 |

Projected tokens in the cell table are unrounded. The matrices round each cell to the nearest token.

## Projected tokens by segment

Sum of the unrounded subsegment projections, then rounded to the nearest token.

| Language | `nvidia/Nemotron-CC-v2` | `nvidia/Nemotron-CC-v2.1` | `HuggingFaceFW/finepdfs-edu` | Projected total |
|---|---:|---:|---:|---:|
| `hi-Deva-IN` | 85,921,402,580 | 24,392,825,045 | 3,412,910,625 | 113,727,138,250 |
| `bn-Beng-IN` | 87,654,698,593 | 22,217,236,445 | 3,389,410,558 | 113,261,345,596 |
| `ta-Taml-IN` | 81,934,479,476 | 20,346,248,888 | 3,258,036,274 | 105,538,764,638 |
| `te-Telu-IN` | 80,573,516,751 | 21,473,636,077 | 4,431,892,066 | 106,479,044,894 |
| `kn-Knda-IN` | 74,618,517,332 | 18,293,557,513 | 2,203,159,530 | 95,115,234,374 |
| `mr-Deva-IN` | 82,082,987,317 | 25,002,932,561 | 1,402,158,838 | 108,488,078,715 |
| `gu-Gujr-IN` | 87,470,561,149 | 22,553,696,532 | 3,622,515,844 | 113,646,773,525 |
| **All seven** | 580,256,163,198 | 154,280,133,060 | 21,720,083,734 | **756,256,379,992** |

All-seven projected tokens, summed unrounded and then rounded: **756,256,379,992**.

