# Indic specialized segment layout

Each language folder under `s3://<research-data-bucket>/datasets/nemotron-indic-specialized-v1/` now has one subfolder per `_source_config`. A parquet file that contained more than one `_source_config` was rewritten into one file per config. A file that already held a single config was copied to that config's subfolder. The original object was deleted only after the new objects existed and their parquet row counts summed to the original. `datasets/nemotron-indic-cc-v1/` was not changed.

Originals removed: 5,572. Left in place because verification failed: 0.

## Objects per language and subfolder

| Language | Subfolder (`_source_config`) | Objects | Bytes |
|---|---|---:|---:|
| `bn-Beng-IN` | `Nemotron-Pretraining-Code-Concepts` | 412 | 22,239,621,784 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Economics` | 24 | 125,006,858 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Formal-Logic` | 36 | 127,825,881 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Math-Textbooks` | 318 | 25,716,762,218 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Multiple-Choice` | 154 | 3,152,253,888 |
| `bn-Beng-IN` | `Nemotron-Pretraining-RQA` | 83 | 1,962,240,978 |
| `bn-Beng-IN` | `Nemotron-Pretraining-STEM-SFT` | 211 | 19,268,330,142 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 16 | 144,120,181 |
| `bn-Beng-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 288 | 10,117,304,759 |
| `bn-Latn-IN` | `Nemotron-Pretraining-Code-Concepts` | 16 | 3,001,362,243 |
| `bn-Latn-IN` | `Nemotron-Pretraining-Economics` | 1 | 23,951,550 |
| `bn-Latn-IN` | `Nemotron-Pretraining-Formal-Logic` | 2 | 23,197,596 |
| `bn-Latn-IN` | `Nemotron-Pretraining-Math-Textbooks` | 6 | 1,266,530,633 |
| `bn-Latn-IN` | `Nemotron-Pretraining-Multiple-Choice` | 4 | 495,464,944 |
| `bn-Latn-IN` | `Nemotron-Pretraining-RQA` | 2 | 759,295,644 |
| `bn-Latn-IN` | `Nemotron-Pretraining-STEM-SFT` | 5 | 2,248,836,293 |
| `bn-Latn-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 11 | 1,098,452,738 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Code-Concepts` | 274 | 22,146,203,795 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Economics` | 16 | 128,306,145 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Formal-Logic` | 20 | 130,172,441 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Math-Textbooks` | 194 | 25,737,471,449 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Multiple-Choice` | 80 | 3,180,213,148 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-RQA` | 18 | 1,829,278,577 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-STEM-SFT` | 118 | 18,015,832,589 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 8 | 220,730,023 |
| `gu-Gujr-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 176 | 10,033,721,752 |
| `gu-Latn-IN` | `Nemotron-Pretraining-Code-Concepts` | 14 | 2,714,517,068 |
| `gu-Latn-IN` | `Nemotron-Pretraining-Economics` | 1 | 39,566,348 |
| `gu-Latn-IN` | `Nemotron-Pretraining-Formal-Logic` | 1 | 6,872,353 |
| `gu-Latn-IN` | `Nemotron-Pretraining-Math-Textbooks` | 5 | 1,734,990,427 |
| `gu-Latn-IN` | `Nemotron-Pretraining-Multiple-Choice` | 4 | 524,015,423 |
| `gu-Latn-IN` | `Nemotron-Pretraining-RQA` | 2 | 739,684,384 |
| `gu-Latn-IN` | `Nemotron-Pretraining-STEM-SFT` | 4 | 1,935,723,124 |
| `gu-Latn-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 1 | 69,993,040 |
| `gu-Latn-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 7 | 957,477,179 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Code-Concepts` | 250 | 22,429,463,279 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Economics` | 14 | 127,040,321 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Formal-Logic` | 20 | 129,302,828 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Math-Textbooks` | 183 | 26,787,197,139 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Multiple-Choice` | 75 | 3,183,183,654 |
| `hi-Deva-IN` | `Nemotron-Pretraining-RQA` | 22 | 2,450,881,114 |
| `hi-Deva-IN` | `Nemotron-Pretraining-STEM-SFT` | 111 | 19,514,439,936 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 9 | 223,878,811 |
| `hi-Deva-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 160 | 10,116,779,875 |
| `hi-Latn-IN` | `Nemotron-Pretraining-Code-Concepts` | 9 | 1,446,337,521 |
| `hi-Latn-IN` | `Nemotron-Pretraining-Formal-Logic` | 1 | 19,035,479 |
| `hi-Latn-IN` | `Nemotron-Pretraining-Math-Textbooks` | 7 | 2,666,228,044 |
| `hi-Latn-IN` | `Nemotron-Pretraining-Multiple-Choice` | 3 | 361,334,587 |
| `hi-Latn-IN` | `Nemotron-Pretraining-RQA` | 2 | 787,503,551 |
| `hi-Latn-IN` | `Nemotron-Pretraining-STEM-SFT` | 6 | 2,472,088,817 |
| `hi-Latn-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 7 | 1,063,293,118 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Code-Concepts` | 287 | 22,051,420,406 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Economics` | 15 | 128,209,959 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Formal-Logic` | 20 | 132,995,619 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Math-Textbooks` | 228 | 24,944,198,782 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Multiple-Choice` | 84 | 3,156,827,413 |
| `kn-Knda-IN` | `Nemotron-Pretraining-RQA` | 19 | 1,706,542,180 |
| `kn-Knda-IN` | `Nemotron-Pretraining-STEM-SFT` | 119 | 16,643,084,772 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 10 | 226,935,553 |
| `kn-Knda-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 204 | 9,304,577,788 |
| `kn-Latn-IN` | `Nemotron-Pretraining-Code-Concepts` | 54 | 1,353,680,046 |
| `kn-Latn-IN` | `Nemotron-Pretraining-Economics` | 2 | 2,593,364 |
| `kn-Latn-IN` | `Nemotron-Pretraining-Formal-Logic` | 4 | 623,775 |
| `kn-Latn-IN` | `Nemotron-Pretraining-Math-Textbooks` | 36 | 2,808,513,092 |
| `kn-Latn-IN` | `Nemotron-Pretraining-Multiple-Choice` | 14 | 291,484,249 |
| `kn-Latn-IN` | `Nemotron-Pretraining-RQA` | 5 | 270,222,860 |
| `kn-Latn-IN` | `Nemotron-Pretraining-STEM-SFT` | 18 | 1,843,705,834 |
| `kn-Latn-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 2 | 2,714,954 |
| `kn-Latn-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 39 | 1,308,744,843 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Code-Concepts` | 264 | 22,555,919,677 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Economics` | 15 | 132,038,831 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Formal-Logic` | 18 | 132,680,963 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Math-Textbooks` | 185 | 26,207,490,052 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Multiple-Choice` | 75 | 3,279,623,108 |
| `mr-Deva-IN` | `Nemotron-Pretraining-RQA` | 18 | 1,963,057,014 |
| `mr-Deva-IN` | `Nemotron-Pretraining-STEM-SFT` | 109 | 18,514,846,724 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 12 | 225,988,249 |
| `mr-Deva-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 172 | 10,414,246,821 |
| `mr-Latn-IN` | `Nemotron-Pretraining-Code-Concepts` | 12 | 2,290,477,042 |
| `mr-Latn-IN` | `Nemotron-Pretraining-Economics` | 1 | 46,180,490 |
| `mr-Latn-IN` | `Nemotron-Pretraining-Formal-Logic` | 1 | 9,707,303 |
| `mr-Latn-IN` | `Nemotron-Pretraining-Math-Textbooks` | 9 | 2,377,527,452 |
| `mr-Latn-IN` | `Nemotron-Pretraining-Multiple-Choice` | 1 | 127,273,445 |
| `mr-Latn-IN` | `Nemotron-Pretraining-RQA` | 1 | 388,776,951 |
| `mr-Latn-IN` | `Nemotron-Pretraining-STEM-SFT` | 5 | 1,693,100,324 |
| `mr-Latn-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 9 | 912,173,283 |
| `ta-Latn-IN` | `Nemotron-Pretraining-Code-Concepts` | 60 | 2,001,436,770 |
| `ta-Latn-IN` | `Nemotron-Pretraining-Economics` | 3 | 9,308,981 |
| `ta-Latn-IN` | `Nemotron-Pretraining-Formal-Logic` | 3 | 1,932,892 |
| `ta-Latn-IN` | `Nemotron-Pretraining-Math-Textbooks` | 38 | 2,975,534,016 |
| `ta-Latn-IN` | `Nemotron-Pretraining-Multiple-Choice` | 18 | 344,413,086 |
| `ta-Latn-IN` | `Nemotron-Pretraining-RQA` | 6 | 261,752,036 |
| `ta-Latn-IN` | `Nemotron-Pretraining-STEM-SFT` | 15 | 1,293,549,093 |
| `ta-Latn-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 2 | 15,965,838 |
| `ta-Latn-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 38 | 1,239,304,681 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Code-Concepts` | 519 | 23,063,475,408 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Economics` | 30 | 139,874,049 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Formal-Logic` | 44 | 141,321,866 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Math-Textbooks` | 411 | 28,941,627,900 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Multiple-Choice` | 205 | 3,431,711,806 |
| `ta-Taml-IN` | `Nemotron-Pretraining-RQA` | 102 | 1,912,744,015 |
| `ta-Taml-IN` | `Nemotron-Pretraining-STEM-SFT` | 285 | 21,365,329,668 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 16 | 237,611,212 |
| `ta-Taml-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 391 | 10,037,285,091 |
| `te-Latn-IN` | `Nemotron-Pretraining-Code-Concepts` | 54 | 2,112,791,278 |
| `te-Latn-IN` | `Nemotron-Pretraining-Economics` | 3 | 10,143,781 |
| `te-Latn-IN` | `Nemotron-Pretraining-Formal-Logic` | 4 | 65,203,307 |
| `te-Latn-IN` | `Nemotron-Pretraining-Math-Textbooks` | 35 | 2,072,897,557 |
| `te-Latn-IN` | `Nemotron-Pretraining-Multiple-Choice` | 18 | 364,825,119 |
| `te-Latn-IN` | `Nemotron-Pretraining-RQA` | 8 | 1,265,983,820 |
| `te-Latn-IN` | `Nemotron-Pretraining-STEM-SFT` | 20 | 1,690,274,211 |
| `te-Latn-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 2 | 2,331,048 |
| `te-Latn-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 34 | 1,205,237,714 |
| `te-Telu-IN` | `Nemotron-Pretraining-Code-Concepts` | 267 | 22,615,069,699 |
| `te-Telu-IN` | `Nemotron-Pretraining-Economics` | 14 | 133,952,558 |
| `te-Telu-IN` | `Nemotron-Pretraining-Formal-Logic` | 18 | 135,766,690 |
| `te-Telu-IN` | `Nemotron-Pretraining-Math-Textbooks` | 221 | 27,902,542,394 |
| `te-Telu-IN` | `Nemotron-Pretraining-Multiple-Choice` | 76 | 3,274,000,672 |
| `te-Telu-IN` | `Nemotron-Pretraining-RQA` | 18 | 2,008,488,590 |
| `te-Telu-IN` | `Nemotron-Pretraining-STEM-SFT` | 126 | 20,089,809,162 |
| `te-Telu-IN` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 12 | 228,341,075 |
| `te-Telu-IN` | `Nemotron-Pretraining-Wiki-Rewrite` | 174 | 10,129,816,449 |

## Totals per language

| Language | Subfolders | Objects | Bytes |
|---|---:|---:|---:|
| `bn-Beng-IN` | 9 | 1,542 | 82,853,466,689 |
| `bn-Latn-IN` | 8 | 47 | 8,917,091,641 |
| `gu-Gujr-IN` | 9 | 904 | 81,421,929,919 |
| `gu-Latn-IN` | 9 | 39 | 8,722,839,346 |
| `hi-Deva-IN` | 9 | 844 | 84,962,166,957 |
| `hi-Latn-IN` | 7 | 35 | 8,815,821,117 |
| `kn-Knda-IN` | 9 | 986 | 78,294,792,472 |
| `kn-Latn-IN` | 9 | 174 | 7,882,283,017 |
| `mr-Deva-IN` | 9 | 868 | 83,425,891,439 |
| `mr-Latn-IN` | 8 | 39 | 7,845,216,290 |
| `ta-Latn-IN` | 9 | 183 | 8,143,197,393 |
| `ta-Taml-IN` | 9 | 2,003 | 89,270,981,015 |
| `te-Latn-IN` | 9 | 178 | 8,789,687,835 |
| `te-Telu-IN` | 9 | 926 | 86,517,787,289 |
| **All** |  | **8,768** | **645,863,152,419** |
