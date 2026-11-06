# Indic specialized token projection

Projected token counts for the seven native configs already in `s3://nemotron-training-data-us-east-1/datasets/nemotron-indic-specialized-v1/`. Latin configs were not read.

Sampled at 2026-10-31 11:41:04 UTC+05:30 (Asia/Calcutta). Each cell is one language folder and one `_source_config`. At least 200 documents were encoded per cell. Many parquet files contain more than one `_source_config`, so each sampled row was kept only when its `_source_config` matched the cell. Files are spread across the cell, and rows are spread through the matching documents in each file. The text column was encoded with the stock tokenizer at `docs/hf-tokenizer` (`tokenizer.json`, vocab 65,536). That file has no post-processor, and `tokenizer_config.json` sets `add_bos_token` and `add_eos_token` to false, so these counts do not add `<s>` or `</s>`.

Every token figure below is a projection from that sample, not a full token census. Projected tokens = (sample token sum / sample documents) × the document count from `docs/indic-specialized-segment-counts.md`. The document counts themselves are the earlier full row census. No EC2 instance was launched.

Cells: 63. Sample documents: 12,678. Files read: 582. Failed files: 0.

## Projected tokens by language and segment

Segment here is `_source_config`. Each value is the sample average multiplied by the census document count, rounded to the nearest token. It is a projection, not a census.

| Language | Math-Textbooks | RQA | STEM-SFT | Wiki-Rewrite | Code-Concepts | Economics | Formal-Logic | Multiple-Choice | Unconditional-Algorithmic | Projected total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `hi-Deva-IN` | 7,942,536,820 | 626,716,069 | 4,729,817,065 | 2,398,833,351 | 2,517,784,740 | 36,842,983 | 47,576,439 | 577,289,202 | 85,136,002 | 18,962,532,670 |
| `bn-Beng-IN` | 7,406,732,421 | 531,005,841 | 4,709,973,772 | 2,898,063,347 | 2,534,392,888 | 22,787,900 | 40,676,167 | 562,483,493 | 51,806,630 | 18,757,922,459 |
| `ta-Taml-IN` | 7,741,857,112 | 477,658,377 | 4,577,760,125 | 2,362,015,932 | 2,517,559,162 | 23,217,145 | 37,063,077 | 573,456,948 | 83,048,359 | 18,393,636,238 |
| `te-Telu-IN` | 7,904,281,502 | 539,213,783 | 5,085,750,202 | 2,606,187,098 | 2,566,682,824 | 34,062,569 | 49,546,459 | 601,958,163 | 84,220,677 | 19,471,903,276 |
| `kn-Knda-IN` | 7,381,754,801 | 456,739,176 | 4,398,320,313 | 2,508,346,145 | 2,458,671,282 | 44,923,654 | 59,802,261 | 579,286,057 | 85,318,008 | 17,973,161,697 |
| `mr-Deva-IN` | 7,090,157,376 | 490,032,860 | 4,472,103,093 | 2,613,854,576 | 2,487,453,287 | 33,034,795 | 51,322,632 | 582,999,626 | 77,859,652 | 17,898,817,896 |
| `gu-Gujr-IN` | 7,554,407,379 | 478,217,289 | 4,926,488,235 | 2,890,219,938 | 2,413,674,075 | 31,396,861 | 41,821,265 | 613,849,718 | 76,796,658 | 19,026,871,418 |
| **All seven** | 53,021,727,411 | 3,599,583,394 | 32,900,212,806 | 18,277,520,386 | 17,496,218,257 | 226,265,906 | 327,808,300 | 4,091,323,207 | 544,185,986 | **130,484,845,654** |

The language total and the all-seven total are the sum of the cell projections, then rounded. They are still projections from the sample.

## Sample size per cell

Documents encoded. This is the sample size, not the census document count.

| Language | Math-Textbooks | RQA | STEM-SFT | Wiki-Rewrite | Code-Concepts | Economics | Formal-Logic | Multiple-Choice | Unconditional-Algorithmic | Sample total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `hi-Deva-IN` | 200 | 214 | 200 | 200 | 200 | 200 | 200 | 200 | 207 | 1,821 |
| `bn-Beng-IN` | 200 | 200 | 200 | 200 | 200 | 214 | 200 | 200 | 216 | 1,830 |
| `ta-Taml-IN` | 200 | 201 | 214 | 200 | 200 | 200 | 200 | 200 | 200 | 1,815 |
| `te-Telu-IN` | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 1,800 |
| `kn-Knda-IN` | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 1,800 |
| `mr-Deva-IN` | 200 | 202 | 200 | 200 | 200 | 200 | 200 | 200 | 210 | 1,812 |
| `gu-Gujr-IN` | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 1,800 |

## Average tokens per document

Sample mean tokens per document. Each average is a projection from the sample, not a census.

| Language | Math-Textbooks | RQA | STEM-SFT | Wiki-Rewrite | Code-Concepts | Economics | Formal-Logic | Multiple-Choice | Unconditional-Algorithmic |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `hi-Deva-IN` | 2,836.68 | 5,036.09 | 3,058.93 | 1,036.76 | 622.06 | 402.12 | 364.50 | 614.75 | 1,764.11 |
| `bn-Beng-IN` | 2,748.24 | 5,377.71 | 3,112.53 | 1,287.75 | 639.23 | 253.96 | 317.79 | 613.82 | 1,781.64 |
| `ta-Taml-IN` | 2,818.80 | 5,184.22 | 3,014.86 | 1,085.88 | 625.06 | 257.81 | 293.79 | 629.36 | 1,730.71 |
| `te-Telu-IN` | 2,790.64 | 5,437.98 | 3,311.46 | 1,149.70 | 634.71 | 373.94 | 388.14 | 651.30 | 1,753.10 |
| `kn-Knda-IN` | 2,945.69 | 5,429.55 | 3,476.04 | 1,178.45 | 627.01 | 514.73 | 473.50 | 650.65 | 1,799.92 |
| `mr-Deva-IN` | 2,640.74 | 4,896.46 | 3,108.89 | 1,136.76 | 614.25 | 360.96 | 394.06 | 622.78 | 1,613.64 |
| `gu-Gujr-IN` | 2,778.79 | 5,119.94 | 3,418.26 | 1,266.42 | 602.86 | 344.43 | 321.92 | 659.21 | 1,624.02 |

## Cell detail

| Language | Segment (`_source_config`) | Parent repo | Census documents | Files sampled | Sample documents | Average tokens | Projected tokens |
|---|---|---|---:|---:|---:|---:|---:|
| `hi-Deva-IN` | `Nemotron-Pretraining-Math-Textbooks` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,799,946 | 10 | 200 | 2,836.68 | 7,942,536,819.6 |
| `hi-Deva-IN` | `Nemotron-Pretraining-RQA` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 124,445 | 13 | 214 | 5,036.09 | 626,716,068.9 |
| `hi-Deva-IN` | `Nemotron-Pretraining-STEM-SFT` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 1,546,230 | 10 | 200 | 3,058.93 | 4,729,817,065.1 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,313,790 | 10 | 200 | 1,036.76 | 2,398,833,351.5 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Code-Concepts` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 4,047,495 | 10 | 200 | 622.06 | 2,517,784,739.7 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Economics` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 91,623 | 10 | 200 | 402.12 | 36,842,982.6 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Formal-Logic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 130,527 | 10 | 200 | 364.50 | 47,576,438.9 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Multiple-Choice` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 939,071 | 10 | 200 | 614.75 | 577,289,201.9 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 48,260 | 9 | 207 | 1,764.11 | 85,136,002.2 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Math-Textbooks` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,695,087 | 10 | 200 | 2,748.24 | 7,406,732,421.4 |
| `bn-Beng-IN` | `Nemotron-Pretraining-RQA` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 98,742 | 10 | 200 | 5,377.71 | 531,005,840.8 |
| `bn-Beng-IN` | `Nemotron-Pretraining-STEM-SFT` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 1,513,230 | 10 | 200 | 3,112.53 | 4,709,973,771.9 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,250,486 | 10 | 200 | 1,287.75 | 2,898,063,346.5 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Code-Concepts` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 3,964,790 | 10 | 200 | 639.23 | 2,534,392,887.8 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Economics` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 89,731 | 11 | 214 | 253.96 | 22,787,900.3 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Formal-Logic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 127,997 | 10 | 200 | 317.79 | 40,676,166.6 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Multiple-Choice` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 916,373 | 10 | 200 | 613.82 | 562,483,493.0 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 29,078 | 11 | 216 | 1,781.64 | 51,806,630.2 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Math-Textbooks` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,746,513 | 10 | 200 | 2,818.80 | 7,741,857,111.8 |
| `ta-Taml-IN` | `Nemotron-Pretraining-RQA` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 92,137 | 11 | 201 | 5,184.22 | 477,658,377.3 |
| `ta-Taml-IN` | `Nemotron-Pretraining-STEM-SFT` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 1,518,399 | 11 | 214 | 3,014.86 | 4,577,760,125.3 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,175,219 | 10 | 200 | 1,085.88 | 2,362,015,931.6 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Code-Concepts` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 4,027,708 | 10 | 200 | 625.06 | 2,517,559,162.5 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Economics` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 90,057 | 10 | 200 | 257.81 | 23,217,144.9 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Formal-Logic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 126,155 | 10 | 200 | 293.79 | 37,063,077.5 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Multiple-Choice` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 911,182 | 10 | 200 | 629.36 | 573,456,947.6 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 47,985 | 10 | 200 | 1,730.71 | 83,048,359.3 |
| `te-Telu-IN` | `Nemotron-Pretraining-Math-Textbooks` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,832,421 | 10 | 200 | 2,790.64 | 7,904,281,501.5 |
| `te-Telu-IN` | `Nemotron-Pretraining-RQA` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 99,157 | 10 | 200 | 5,437.98 | 539,213,782.9 |
| `te-Telu-IN` | `Nemotron-Pretraining-STEM-SFT` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 1,535,803 | 10 | 200 | 3,311.46 | 5,085,750,202.4 |
| `te-Telu-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,266,841 | 10 | 200 | 1,149.70 | 2,606,187,097.7 |
| `te-Telu-IN` | `Nemotron-Pretraining-Code-Concepts` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 4,043,867 | 10 | 200 | 634.71 | 2,566,682,823.6 |
| `te-Telu-IN` | `Nemotron-Pretraining-Economics` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 91,091 | 10 | 200 | 373.94 | 34,062,568.5 |
| `te-Telu-IN` | `Nemotron-Pretraining-Formal-Logic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 127,651 | 10 | 200 | 388.14 | 49,546,459.1 |
| `te-Telu-IN` | `Nemotron-Pretraining-Multiple-Choice` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 924,241 | 10 | 200 | 651.30 | 601,958,163.3 |
| `te-Telu-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 48,041 | 10 | 200 | 1,753.10 | 84,220,677.1 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Math-Textbooks` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,505,951 | 10 | 200 | 2,945.69 | 7,381,754,801.2 |
| `kn-Knda-IN` | `Nemotron-Pretraining-RQA` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 84,121 | 10 | 200 | 5,429.55 | 456,739,175.6 |
| `kn-Knda-IN` | `Nemotron-Pretraining-STEM-SFT` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 1,265,325 | 10 | 200 | 3,476.04 | 4,398,320,313.0 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,128,513 | 10 | 200 | 1,178.45 | 2,508,346,144.8 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Code-Concepts` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 3,921,232 | 10 | 200 | 627.01 | 2,458,671,282.5 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Economics` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 87,277 | 10 | 200 | 514.73 | 44,923,653.8 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Formal-Logic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 126,297 | 10 | 200 | 473.50 | 59,802,261.0 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Multiple-Choice` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 890,319 | 10 | 200 | 650.65 | 579,286,057.4 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 47,401 | 10 | 200 | 1,799.92 | 85,318,007.9 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Math-Textbooks` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,684,908 | 10 | 200 | 2,640.74 | 7,090,157,376.5 |
| `mr-Deva-IN` | `Nemotron-Pretraining-RQA` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 100,079 | 11 | 202 | 4,896.46 | 490,032,860.0 |
| `mr-Deva-IN` | `Nemotron-Pretraining-STEM-SFT` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 1,438,491 | 10 | 200 | 3,108.89 | 4,472,103,092.5 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,299,390 | 10 | 200 | 1,136.76 | 2,613,854,576.4 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Code-Concepts` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 4,049,578 | 10 | 200 | 614.25 | 2,487,453,286.5 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Economics` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 91,518 | 10 | 200 | 360.96 | 33,034,794.9 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Formal-Logic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 130,239 | 10 | 200 | 394.06 | 51,322,631.5 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Multiple-Choice` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 936,117 | 10 | 200 | 622.78 | 582,999,625.8 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 48,251 | 11 | 210 | 1,613.64 | 77,859,651.7 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Math-Textbooks` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,718,596 | 10 | 200 | 2,778.79 | 7,554,407,378.8 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-RQA` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 93,403 | 10 | 200 | 5,119.94 | 478,217,288.8 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-STEM-SFT` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 1,441,229 | 10 | 200 | 3,418.26 | 4,926,488,235.4 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | `nvidia/Nemotron-Pretraining-Specialized-v1` | 2,282,188 | 10 | 200 | 1,266.42 | 2,890,219,937.9 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Code-Concepts` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 4,003,739 | 10 | 200 | 602.86 | 2,413,674,074.8 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Economics` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 91,156 | 10 | 200 | 344.43 | 31,396,861.1 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Formal-Logic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 129,914 | 10 | 200 | 321.92 | 41,821,265.3 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Multiple-Choice` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 931,197 | 10 | 200 | 659.21 | 613,849,718.4 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | 47,288 | 8 | 200 | 1,624.02 | 76,796,657.8 |

Average tokens and projected tokens are sample projections. Projected tokens in this table are unrounded: sample token sum / sample documents × census documents. The matrix above rounds each cell to the nearest token.

## Projected tokens by parent repo

Sum of the unrounded `_source_config` projections, then rounded to the nearest token. Still a projection from the sample.

| Language | `Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Specialized-v1.1` | Projected total |
|---|---:|---:|---:|
| `hi-Deva-IN` | 15,697,903,305 | 3,264,629,365 | 18,962,532,670 |
| `bn-Beng-IN` | 15,545,775,381 | 3,212,147,078 | 18,757,922,459 |
| `ta-Taml-IN` | 15,159,291,546 | 3,234,344,692 | 18,393,636,238 |
| `te-Telu-IN` | 16,135,432,584 | 3,336,470,692 | 19,471,903,276 |
| `kn-Knda-IN` | 14,745,160,435 | 3,228,001,263 | 17,973,161,697 |
| `mr-Deva-IN` | 14,666,147,905 | 3,232,669,990 | 17,898,817,896 |
| `gu-Gujr-IN` | 15,849,332,841 | 3,177,538,577 | 19,026,871,418 |
| **All seven** | 107,799,043,997 | 22,685,801,657 | **130,484,845,654** |

## Segment names

- Math-Textbooks: `Nemotron-Pretraining-Math-Textbooks`
- RQA: `Nemotron-Pretraining-RQA`
- STEM-SFT: `Nemotron-Pretraining-STEM-SFT`
- Wiki-Rewrite: `Nemotron-Pretraining-Wiki-Rewrite`
- Code-Concepts: `Nemotron-Pretraining-Code-Concepts`
- Economics: `Nemotron-Pretraining-Economics`
- Formal-Logic: `Nemotron-Pretraining-Formal-Logic`
- Multiple-Choice: `Nemotron-Pretraining-Multiple-Choice`
- Unconditional-Algorithmic: `Nemotron-Pretraining-Unconditional-Algorithmic`
