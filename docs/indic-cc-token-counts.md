# Indic CC token counts

Full sum of `token_count` from every `.tokens.index.jsonl` under the included slices of `s3://nemotron-training-data-us-east-1/datasets/nemotron-indic-cc-v1/`.

Counted from `ops/indic-cc-tokenize-20261101/stats/` when that prefix held 46,141 objects, one per source parquet. These are stored token ids. No `<eod>` is in the bins.

Excluded and not read: `HuggingFaceFW/finepdfs-edu`, and `nvidia/Nemotron-CC-v2.1` `High-Quality-DQA`.

Files: 46,141. Documents: 892,060,753. Tokens: **750,022,728,096**.

## Instances

Spot `indic-cc-tokenize` boxes that ran the encode. The fleet was still up when this file was written.

- `i-0f6db2dea3370286d`
- `i-0fd5f45852f48ac71`
- `i-0c964d40d233016ad`
- `i-0c8b01a21db6c2e76`
- `i-0af4077080c4138e3`

`i-00674deee0b991001`, `i-01de091f1d0e45ce0`, `i-090328b39f051b8f6`, `i-0396c0276be20db6b`, and `i-0a2d3ef87e207ff2d` also took claims and were spot-interrupted. Their finished bins were kept.

## Tokens per language and slice

### `nvidia/Nemotron-CC-v2`

| Language | `Diverse-QA` | `High-Quality` | `Medium-High-Quality` | Total |
|---|---:|---:|---:|---:|
| Hindi | 27,087,081,346 | 44,289,055,503 | 19,788,788,045 | 91,164,924,894 |
| Bengali | 25,370,103,948 | 42,574,423,411 | 19,511,177,905 | 87,455,705,264 |
| Tamil | 26,216,081,689 | 41,514,236,696 | 18,535,632,927 | 86,265,951,312 |
| Telugu | 27,166,264,153 | 43,169,556,882 | 19,808,637,971 | 90,144,459,006 |
| Kannada | 25,408,333,380 | 39,072,152,508 | 17,353,434,516 | 81,833,920,404 |
| Marathi | 25,338,419,551 | 41,788,894,051 | 18,670,221,343 | 85,797,534,945 |
| Gujarati | 27,273,129,994 | 45,475,422,223 | 20,392,617,417 | 93,141,169,634 |
| **All seven** | 183,859,414,061 | 297,883,741,274 | 134,060,510,124 | **615,803,665,459** |

### `nvidia/Nemotron-CC-v2.1`

| Language | `High-Quality` | `High-Quality-Synthetic` | `Medium-High-Quality` | `Medium-High-Quality-Synthetic` | Total |
|---|---:|---:|---:|---:|---:|
| Hindi | 5,792,591,565 | 7,675,739,136 | 1,377,209,705 | 4,866,564,461 | 19,712,104,867 |
| Bengali | 5,599,141,473 | 7,471,969,117 | 1,367,759,745 | 4,828,587,341 | 19,267,457,676 |
| Tamil | 5,485,027,435 | 7,447,320,161 | 1,177,615,988 | 4,057,628,795 | 18,167,592,379 |
| Telugu | 5,864,830,338 | 7,881,917,403 | 1,404,699,601 | 4,881,604,766 | 20,033,052,108 |
| Kannada | 5,317,795,029 | 7,226,500,017 | 1,228,439,994 | 4,382,748,015 | 18,155,483,055 |
| Marathi | 5,459,456,470 | 7,327,267,962 | 1,303,170,432 | 4,612,124,258 | 18,702,019,122 |
| Gujarati | 5,839,612,582 | 7,856,962,961 | 1,420,381,177 | 5,064,396,710 | 20,181,353,430 |
| **All seven** | 39,358,454,892 | 52,887,676,757 | 9,279,276,642 | 32,693,654,346 | **134,219,062,637** |

## Documents per language and slice

### `nvidia/Nemotron-CC-v2`

| Language | `Diverse-QA` | `High-Quality` | `Medium-High-Quality` | Total |
|---|---:|---:|---:|---:|
| Hindi | 34,550,914 | 54,167,556 | 22,347,938 | 111,066,408 |
| Bengali | 32,618,682 | 52,680,871 | 22,146,323 | 107,445,876 |
| Tamil | 32,772,840 | 51,001,321 | 20,921,868 | 104,696,029 |
| Telugu | 33,735,595 | 51,844,882 | 21,800,442 | 107,380,919 |
| Kannada | 31,742,869 | 49,537,093 | 20,231,602 | 101,511,564 |
| Marathi | 33,968,944 | 53,958,551 | 22,226,393 | 110,153,888 |
| Gujarati | 34,033,849 | 53,492,720 | 22,008,322 | 109,534,891 |
| **All seven** | 233,423,693 | 366,682,994 | 151,682,888 | **751,789,575** |

### `nvidia/Nemotron-CC-v2.1`

| Language | `High-Quality` | `High-Quality-Synthetic` | `Medium-High-Quality` | `Medium-High-Quality-Synthetic` | Total |
|---|---:|---:|---:|---:|---:|
| Hindi | 5,755,969 | 8,020,039 | 1,420,033 | 5,576,781 | 20,772,822 |
| Bengali | 5,592,744 | 7,798,514 | 1,410,246 | 5,520,371 | 20,321,875 |
| Tamil | 5,463,617 | 7,594,735 | 1,217,942 | 4,520,882 | 18,797,176 |
| Telugu | 5,642,841 | 7,875,780 | 1,390,373 | 5,386,316 | 20,295,310 |
| Kannada | 5,310,335 | 7,360,113 | 1,290,010 | 4,983,728 | 18,944,186 |
| Marathi | 5,711,919 | 8,021,672 | 1,417,478 | 5,531,761 | 20,682,830 |
| Gujarati | 5,629,553 | 7,940,029 | 1,400,858 | 5,486,539 | 20,456,979 |
| **All seven** | 39,106,978 | 54,610,882 | 9,546,940 | 37,006,378 | **140,271,178** |

## Files per language

| Language | Files | Documents | Tokens |
|---|---:|---:|---:|
| Hindi | 6,392 | 131,839,230 | 110,877,029,761 |
| Bengali | 3,584 | 127,767,751 | 106,723,162,940 |
| Tamil | 4,006 | 123,493,205 | 104,433,543,691 |
| Telugu | 8,131 | 127,676,229 | 110,177,511,114 |
| Kannada | 9,545 | 120,455,750 | 99,989,403,459 |
| Marathi | 6,885 | 130,836,718 | 104,499,554,067 |
| Gujarati | 7,598 | 129,991,870 | 113,322,523,064 |
| **All seven** | 46,141 | 892,060,753 | **750,022,728,096** |

## Spot-check against `Tokenizer.encode`

Stock `Tokenizer.encode(..., add_special_tokens=False)` on the tokenizer at `docs/hf-tokenizer`. The bins were written with that model and an equivalent normalizer (`normalizer=None` after the same NFC and Indic rewrites). Compared ids:

- `kn-Knda-IN` `Medium-High-Quality-Synthetic` `train-05898-of-07065.parquet`: 5 documents, 0 mismatches.
- `te-Telu-IN` `Medium-High-Quality-Synthetic` `train-05633-of-06169.parquet`: 3 documents, 0 mismatches.
- `gu-Gujr-IN` `Diverse-QA` `train-05110-of-06052.parquet`: 3 documents, 0 mismatches.
- `ta-Taml-IN` `High-Quality-Synthetic` `train-00333-of-00779.parquet`: 3 documents, 0 mismatches.

Mismatches: 0. A few documents encode to a stock special id below 32 (id 1, `<s>`). Those ids are in the bins because they are what `Tokenizer.encode` returns. No `<eod>` was added.

