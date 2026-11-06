---
cursor:
  subagentId: "bc-786628f3-9c64-5c8e-bf36-95fa1100e011"
---

# Packing the 1T run

Decided 2026-11-01, revised 2026-11-02. This is how the 1.2B from-scratch run is sharded and batched. English is the locked 500B in [english-500b-mix.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/english-500b-mix.md), with Specialized v1.1 and CodeAlchemy split into their real subsegments. Indic is the locked 500B in [indic-500b-curriculum.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-500b-curriculum.md). The two halves are drawn 1:1 on the same steps. A piece is a string, not a language: [tokenizer plan](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/tokenizer-plan.md), plain version [tokenizer explained](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/tokenizer-explained.md).

The token budgets stay as written. One sequence is one language and one source. A source is a subsegment, not the parent dataset. A sum line is not a bucket.

## What a phase is

A phase is a contiguous run of optimizer steps that reads one sealed set of shards and one fixed vector of sampling weights. Warmup is the steps that consume the first 50,000,000,000 real tokens, 25,000,000,000 English and 25,000,000,000 Indic. Stable is the next 850,000,000,000 real tokens, 425,000,000,000 from each half. Decay is the last 100,000,000,000 real tokens, 50,000,000,000 from each half. A step belongs to one phase. A batch never contains tokens from two phases. The learning-rate segment changes on those same boundaries; this note does not choose the peak rate or the shape of the decay. Inside a phase the weights stay put, and every step draws English and all seven Indic languages. Each document is assigned to one phase before step 0 and is read only there.

| Phase | English | Indic | Combined real tokens | Share of the 1T |
| --- | ---: | ---: | ---: | ---: |
| Warmup | 25,000,000,000 | 25,000,000,000 | 50,000,000,000 | 5% |
| Stable | 425,000,000,000 | 425,000,000,000 | 850,000,000,000 | 85% |
| Decay | 50,000,000,000 | 50,000,000,000 | 100,000,000,000 | 10% |
| **Sum** | **500,000,000,000** | **500,000,000,000** | **1,000,000,000,000** | **100%** |

The reference batch is 1,000,000 real tokens, so the boundaries fall on batch edges: 50,000 warmup steps, 850,000 stable steps, 100,000 decay steps. Any other real-token batch size has to divide 50,000,000,000. The last batch of a phase is the one that finishes that phase’s shards. It is not padded with the next phase.

## What one batch contains

Every batch, in every phase: **500,000 English real tokens and 500,000 Indic real tokens.** That is the whole 1:1 rule. The batch is then split by the cumulative quotient below, so the phase sums land on the budgets exactly. A source with a zero budget contributes nothing in that phase. Pad tokens are not part of the 1,000,000.

### Indic languages

The weights are these phase totals. Hindi is the largest share in every phase. Bengali is second in warmup and decay, and last in stable.

| Language | Warmup | Stable | Decay |
| --- | ---: | ---: | ---: |
| Hindi | 5,417,103,550 | 85,215,326,818 | 9,367,569,632 |
| Bengali | 3,845,443,527 | 54,785,541,902 | 8,035,681,237 |
| Tamil | 3,320,046,617 | 56,515,958,641 | 6,830,661,409 |
| Telugu | 3,121,956,205 | 56,826,775,808 | 6,717,934,654 |
| Kannada | 3,013,603,895 | 57,787,672,538 | 5,865,390,234 |
| Marathi | 3,161,007,033 | 57,262,370,910 | 6,243,288,724 |
| Gujarati | 3,120,839,173 | 56,606,353,383 | 6,939,474,110 |
| **Indic half** | **25,000,000,000** | **425,000,000,000** | **50,000,000,000** |

Rate per 500,000 Indic tokens, which is Hindi’s warmup as an example: 5,417,103,550 / 25,000,000,000 × 500,000 = 108342.071. The first warmup batch, after the cumulative rule, is Hindi 108,342, Bengali 76,909, Tamil 66,401, Telugu 62,439, Kannada 60,272, Marathi 63,220, Gujarati 62,417. Later batches move by a token or two. The phase sum is the table.

### English sources

Decay is the published last 50B, disjoint documents, reserved first. Warmup and stable share one mixture: the other 450B. The sheet is in tenths of a billion, and 25/450 is not an integer token count per source. Warmup’s 25,000,000,000 English tokens are the largest-remainder cut of those residuals (`residual × 25,000,000,000 // 450,000,000,000`, then one extra token to each of the five largest fractional parts). Those five tokens go to InfiniByte, ClimbMix, Specialized v1.1, RQA, and Math 4+. Stable is the residual minus that warmup cut. The 500B and the decay 50B do not move. Specialized v1.1 and CodeAlchemy are then split into the subsegments below. Each of those subsegments keeps a share of the parent’s warmup, stable, and decay, so each is in every phase the parent was in. Code v2 is five source rows in the same table. Their integers are not assigned.

| Source | Warmup | Stable | Decay |
| --- | ---: | ---: | ---: |
| ClimbMix | 14,266,666,667 | 234,554,018,890 | 20,000,000,000 |
| Math 4+ | 2,855,555,556 | 49,544,444,444 | 9,000,000,000 |
| Nemotron Code v2, sum of five sources, not a bucket | 2,622,222,222 | 46,557,092,221 | 6,000,000,000 |
| Nemotron Code v2 `Synthetic-Question-Answering` | 1,360,120,802 | 24,148,704,513 | 3,112,140,818 |
| Nemotron Code v2 `Synthetic-Student-Teacher` | 139,340,722 | 2,473,969,899 | 318,830,466 |
| Nemotron Code v2 `Synthetic-Code-Review` | 465,172,917 | 8,259,062,946 | 1,064,378,708 |
| Nemotron Code v2 `Synthetic-Rewriting` | 465,716,114 | 8,268,707,312 | 1,065,621,617 |
| Nemotron Code v2 `Synthetic-Transpilation` | 191,871,667 | 3,406,647,551 | 439,028,391 |
| Specialized v1.1 `Code-Concepts` | 465,079,951 | 7,906,359,152 | 1,839,876,726 |
| Specialized v1.1 `Multiple-Choice` | 35,488,490 | 603,304,325 | 140,394,025 |
| Specialized v1.1 `Unconditional-Algorithmic` | 3,019,470 | 51,330,999 | 11,945,158 |
| Specialized v1.1 `Formal-Logic` | 1,059,047 | 18,003,792 | 4,189,635 |
| Specialized v1.1 `Economics` | 908,598 | 15,446,176 | 3,594,456 |
| Nemotron-CC-Code-v1 | 1,555,555,555 | 27,444,444,445 | 3,000,000,000 |
| InfiniByte | 1,027,777,778 | 18,472,222,222 | 3,000,000,000 |
| Genesis III, option-level | 555,555,555 | 10,944,444,445 | 3,500,000,000 |
| RQA | 605,555,556 | 11,294,444,444 | 2,500,000,000 |
| CodeAlchemy `code-dev` | 396,825,396 | 6,746,031,747 | 0 |
| CodeAlchemy `code-enhance` | 158,730,159 | 2,698,412,698 | 0 |
| Fact-Seeking | 450,000,000 | 8,150,000,000 | 1,000,000,000 |
| **English half** | **25,000,000,000** | **425,000,000,000** | **50,000,000,000** |

Specialized v1.1 bytes, which are the weights: Code-Concepts 32,090,527,236, Multiple-Choice 2,448,706,604, Unconditional-Algorithmic 208,343,534, Formal-Logic 73,074,239, Economics 62,693,323. The split is largest remainder of the locked 11.1B, of warmup 505,555,556, and of decay 2,000,000,000. Stable is the remainder of each row. This is not an index census. Each of the five is its own source and is in all three phases.

CodeAlchemy is two sources. Stored shards are code-dev 10 and code-enhance 4. The locked 10B and warmup 555,555,555 are split 10:4. Decay is 0. `code-dialogue` and `code-qa` are not sources.

Nemotron Code v2 is the five source rows above. The 2026-11-04 census sums the stored bins by source-file hash: 55,179,314,443 tokens in 30 files; the locked cap was 55,200,000,000, and ClimbMix funds the 20,685,557 difference. Synthetic-Question-Answering is 51.9% of the row. The five rows sum to 2,622,222,222 / 46,557,092,221 / 6,000,000,000. The sum line is not a source.

Decay divides the 500,000 English tokens by the source table. ClimbMix 200,000, Math 4+ 90,000, Code v2 `Synthetic-Question-Answering` 31,121, `Synthetic-Rewriting` 10,656, `Synthetic-Code-Review` 10,644, `Synthetic-Transpilation` 4,390, `Synthetic-Student-Teacher` 3,188, CC-Code-v1 30,000, InfiniByte 30,000, Genesis III 35,000, RQA 25,000, Specialized v1.1 Code-Concepts 18,399, Multiple-Choice 1,404, Unconditional-Algorithmic 119, Formal-Logic 42, Economics 36, Fact-Seeking 10,000, CodeAlchemy 0. Those v1.1 integers are the first decay batch under the cumulative rule on the decay column, and they sum to 20,000. Warmup and stable sit on the residual rates (ClimbMix about 275,945.90 of every 500,000). The cumulative rule turns that repeating fraction into integers.

Personas-India has no cursor until its token count exists. It stays on the English side. When the count exists, some other English row is cut by that count, as that sheet already says. The packer does not invent which row, and it does not add an eleventh stream on top of the 500,000.

### Indic sources inside a language

Split the language first, then the sources inside that language’s tokens. The pooled source mix is the sum of these cells. Sampling the pool first would smear the Gujarati move across the other six languages.

This Latin add is FineWeb-2 Latin. The count is the census in [indic-fineweb2-latin-token-counts.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-fineweb2-latin-token-counts.md), 311,404,717 tokens, taken in full. Specialized Latin was already in the specialized subsegment rows, 12,778,755,736, and is not repeated. Total Indic Latin is 13,090,160,453. Nemotron-CC was not cut. The unmeasured Latin budget is deleted. Each language’s Latin count is funded by reducing that language’s FineWeb-2 native by the same count. IndicCorp is the full pool. The reduction does not reach Sangraha or Code-Concepts.

For each language and each counted source, warmup / stable / decay = `n × percent // 100`, remainder in stable. Percents: Specialized subsegments 3/82/15, FineWeb-2 Latin 10/80/10, FineWeb-2 native 10/80/10, Sangraha 10/70/20, CC-v2 High-Quality 5/93/2, CC-v2.1 High-Quality 8/80/12, CC-v2.1 High-Quality-DQA 0/70/30, IndicCorp v2 0/100/0, CC-v2 Diverse-QA 0/70/30. One correction after that arithmetic: Gujarati CC-v2 High-Quality moves 49,629,202 from stable into warmup and 640,478,753 from stable into decay. The cells below are after that move. They sum to the language table and to the curriculum’s segment table. CC-v2 Diverse-QA is zero in every cell. A zero cell is not a bucket. The Specialized sum column is a check, not a source.

Warmup. IndicCorp and both diverse-QA rows are absent. Every specialized subsegment is present at 3% of its own tokens, including Code-Concepts.

| Language | Specialized sum | FineWeb-2 Latin | FineWeb-2 native | IndicCorp v2 | Sangraha | CC-v2 HQ | CC-v2.1 HQ | CC-v2.1 DQA | CC-v2 DQA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| hi | 638,022,124 | 21,399,711 | 1,445,040,411 | 0 | 1,101,843,355 | 1,747,390,624 | 463,407,325 | 0 | 0 |
| bn | 601,900,275 | 3,230,448 | 1,082,151,676 | 0 | 947,701,125 | 762,528,686 | 447,931,317 | 0 | 0 |
| ta | 617,952,097 | 1,456,777 | 395,824,156 | 0 | 544,756,613 | 1,321,254,780 | 438,802,194 | 0 | 0 |
| te | 640,198,313 | 4,376,900 | 176,121,614 | 0 | 469,836,141 | 1,362,236,810 | 469,186,427 | 0 | 0 |
| kn | 577,289,312 | 223,869 | 157,142,924 | 0 | 234,156,619 | 1,619,367,569 | 425,423,602 | 0 | 0 |
| mr | 582,363,657 | 306,927 | 259,243,422 | 0 | 359,300,856 | 1,523,035,654 | 436,756,517 | 0 | 0 |
| gu | 612,806,173 | 145,835 | 159,909,278 | 0 | 332,010,952 | 1,548,797,929 | 467,169,006 | 0 | 0 |
| **Sum** | **4,270,531,951** | **31,140,467** | **3,675,433,481** | **0** | **3,989,605,661** | **9,884,612,052** | **3,148,676,388** | **0** | **0** |

Stable.

| Language | Specialized sum | FineWeb-2 Latin | FineWeb-2 native | IndicCorp v2 | Sangraha | CC-v2 HQ | CC-v2.1 HQ | CC-v2.1 DQA | CC-v2 DQA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| hi | 17,439,271,414 | 171,197,697 | 11,560,323,297 | 8,598,473,855 | 7,712,903,489 | 32,501,465,618 | 4,634,073,253 | 2,597,618,195 | 0 |
| bn | 16,451,940,862 | 25,843,592 | 8,657,213,411 | 1,861,152,984 | 6,633,907,878 | 14,183,033,577 | 4,479,313,180 | 2,493,136,418 | 0 |
| ta | 16,890,690,673 | 11,654,221 | 3,166,593,252 | 1,179,759,699 | 3,813,296,297 | 24,575,338,915 | 4,388,021,949 | 2,490,603,635 | 0 |
| te | 17,498,753,904 | 35,015,209 | 1,408,972,914 | 1,886,816,677 | 3,288,852,991 | 25,337,604,681 | 4,691,864,271 | 2,678,895,161 | 0 |
| kn | 15,779,241,213 | 1,790,957 | 1,257,143,396 | 2,245,371,670 | 1,639,096,336 | 30,120,236,784 | 4,254,236,024 | 2,490,556,158 | 0 |
| mr | 15,917,939,965 | 2,455,424 | 2,073,947,379 | 1,515,965,336 | 2,515,105,994 | 28,328,463,174 | 4,367,565,177 | 2,540,928,461 | 0 |
| gu | 16,750,035,419 | 1,166,683 | 1,279,274,231 | 1,794,591,509 | 2,324,076,670 | 27,194,430,369 | 4,671,690,067 | 2,591,088,435 | 0 |
| **Sum** | **116,727,873,450** | **249,123,783** | **29,403,467,880** | **19,082,131,730** | **27,927,239,655** | **182,240,573,118** | **31,486,763,921** | **17,882,826,463** | **0** |

Decay.

| Language | Specialized sum | FineWeb-2 Latin | FineWeb-2 native | IndicCorp v2 | Sangraha | CC-v2 HQ | CC-v2.1 HQ | CC-v2.1 DQA | CC-v2 DQA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| hi | 3,190,110,624 | 21,399,711 | 1,445,040,411 | 0 | 2,203,686,710 | 698,956,249 | 695,110,987 | 1,113,264,940 | 0 |
| bn | 3,009,501,377 | 3,230,448 | 1,082,151,676 | 0 | 1,895,402,250 | 305,011,474 | 671,896,976 | 1,068,487,036 | 0 |
| ta | 3,089,760,488 | 1,456,777 | 395,824,156 | 0 | 1,089,513,227 | 528,501,912 | 658,203,292 | 1,067,401,557 | 0 |
| te | 3,200,991,567 | 4,376,900 | 176,121,614 | 0 | 939,672,283 | 544,894,724 | 703,779,640 | 1,148,097,926 | 0 |
| kn | 2,886,446,563 | 223,869 | 157,142,924 | 0 | 468,313,238 | 647,747,027 | 638,135,403 | 1,067,381,210 | 0 |
| mr | 2,911,818,286 | 306,927 | 259,243,422 | 0 | 718,601,712 | 609,214,261 | 655,134,776 | 1,088,969,340 | 0 |
| gu | 3,064,030,869 | 145,835 | 159,909,278 | 0 | 664,021,905 | 1,240,146,243 | 700,753,509 | 1,110,466,471 | 0 |
| **Sum** | **21,352,659,774** | **31,140,467** | **3,675,433,481** | **0** | **7,979,211,325** | **4,574,471,890** | **4,723,014,583** | **7,664,068,480** | **0** |

Specialized is not one column on disk. The eighteen sources are `math-textbooks-native`, `math-textbooks-latn`, `code-concepts-native`, `code-concepts-latn`, `wiki-rewrite-native`, `wiki-rewrite-latn`, `stem-sft-native`, `stem-sft-latn`, `multiple-choice-native`, `multiple-choice-latn`, `formal-logic-native`, `formal-logic-latn`, `rqa-native`, `rqa-latn`, `economics-native`, `economics-latn`, `unconditional-algorithmic-native`, and `unconditional-algorithmic-latn`. A missing folder is not a bucket (`hi` Latin has no Economics and no Unconditional-Algorithmic; `bn` Latin and `mr` Latin have no Unconditional-Algorithmic). Each existing source uses 3/82/15 of its own index sum. Code-Concepts native and Code-Concepts Latin are each in warmup, stable, and decay. The packer must not write one Code-Concepts shard stream and then the other subsegments. The index sum per subsegment is not in the store, so the integer cells for those eighteen sources are not in this note. The Specialized sum column is the language-level 3/82/15 and is only a check until those index sums are filled in. The sample projection is not a substitute.

FineWeb-2 Latin is the source `fineweb2-latn`, one row per language, 311,404,717 tokens across the seven, the census, taken in full. It is not a second copy of Specialized Latin.

### The cumulative split

Let `P` be the phase budget of a group (the Indic half, one language, or the English half) and `T_b` the budget of bucket `b`, with the `T_b` summing to `P`. After `s` tokens of that group have been scheduled (`s` = 500,000, 1,000,000, …), bucket `b` is owed

`floor(T_b × s / P) − (tokens of b already placed)`.

On these budgets that difference stays non-negative. The differences sum to `N − k` with `k` smaller than the number of buckets. Give those `k` tokens to the buckets with the largest `(T_b × s) mod P`. At `s = P` every bucket has received exactly `T_b`.

Do this for the seven languages against the 500,000 Indic tokens, then again inside each language against that language’s source cells, then again for the English sources against the 500,000 English tokens. A zero cell is not a bucket. A sum line is not a bucket, including the Specialized sum column and the Nemotron Code v2 cap. Inside specialized, the buckets are the eighteen subsegment names, once their token sums exist. Inside Code v2, the buckets are the five synthetic sources, once their token sums exist.

Sequences are the second remainder. Context length `L` is the model’s context. This note does not choose it. Each bucket keeps a carry, starting at 0. Add this batch’s token assignment to the carry. While the carry is at least `L` and the bucket still has a full sequence, emit one sequence and subtract `L`. A source whose assignment is under `L` simply waits in the carry until a later batch pays for a sequence. Gujarati FineWeb-2 Latin in warmup is the small open cell: about 2.92 tokens of a 500,000 Indic half, so at `L = 4096` it appears on some steps and not others. The phase still receives all 145,835 tokens.

## What one sequence contains

One sequence is one language and one source. English is the eighth language for this rule. Hindi and Marathi never share a sequence. Code-Concepts and Wiki-Rewrite never share a sequence. Native script and Latin script never share a sequence. Code and web never share a sequence. Two documents in one sequence are joined by a single `<eod>`, id 4, after each finished document. The packer adds it. The content bins do not already contain it. Do not also insert `<s>` or `</s>`.

A document longer than `L` is cut into consecutive sequences of the same bucket. The continuation is the next tokens of that document, in the same shard, before any other document. IndicCorp v2 is about 80.4 tokens a document on the full corpus, so a sequence holds many of them, each closed by `<eod>`. That packing is required. One short document alone in a 2048-wide row would be almost entirely pad, and pad is not a language.

Attention does not cross a document boundary. Inside one sequence, self-attention is block-diagonal by document: a token attends only to the tokens of its own document, and position ids reset at each `<eod>`. The `<eod>` belongs to the block of the document it closes. This is intra-document masking, the Zhao et al. (ACL 2024) result that Llama 3 and SmolLM3 train with; it is required, not optional. The packer records the per-document spans that make the mask buildable, and the trainer must implement it: block-diagonal attention and position reset at every `<eod>`. A training run that attends across documents inside a sequence is a different run than this note describes. Pad is outside every block.

The tail of a bucket may be shorter than `L`. Fill the rest with `<pad>`, id 3, and mask the pad in the loss. Pad is not charged to any budget and is not used to make two languages look equal. The loss is on real tokens and on `<eod>`.

Indic validation tokens that remain inside a drawn row stay inside the budgets and are masked. The census holdout is FineWeb-2 10,300,598, IndicCorp v2 1,155,338, Sangraha 9,701,494. Every language draws FineWeb-2 native, IndicCorp, and Sangraha, so those val documents stay. The FineWeb-2 Latin count is not taken out of the val carve. Pack held-out documents as their own sequences in the same language and source, loss fully masked, so a training document does not attend into a held-out document. Do not drop them and do not refill them. English rows that were carved out into `.val` parts stay out of the train shards.

## Hindi, Marathi, and the shared script

Devanagari entries are shared because the string is the same. The embedding row for a shared piece receives gradient from every sequence that contains it. In this packing that gradient is two monolingual losses in the same step: a Hindi sequence and a Marathi sequence, weighted by how often the piece appears in each language’s tokens that step.

Under these budgets the Hindi:Marathi token ratio in the batch is the phase table, not 1:1 inside the phase. Warmup is 5,417,103,550 : 3,161,007,033 (1.714). Stable is 85,215,326,818 : 57,262,370,910 (1.488). Decay is 9,367,569,632 : 6,243,288,724 (1.500). The run-length ratio is 100,000,000,000 : 66,666,666,667 (1.500). Warmup is the Hindi-heavy phase. Stable is the lightest of the three, still above 1. That is the data, delivered every step. It is not a defect to fix by repeating Marathi.

The 100B and 66.67B totals are a data budget. They are not a pad, and they are not a script quota. The packer does not add pad, repeated Marathi, transliterated Marathi, or Hindi-script copies of Marathi to pull the ratio toward 1. Identical strings are already stored once in the vocabulary. There is no second copy of a piece to hand to Marathi.

## Shards on disk

The immutable bins stay where tokenization put them. A phase weight is not a reason to retokenize, and the bins are not rewritten into phase files. FineWeb-2 Latin is the seven index files in the census. That count is not a second epoch of Specialized Latin, and it is not a reason to invent tokens.

The training layout is a derived tree the packer can delete and rebuild:

```
packed/{phase}/{lang}/{source}/shard-00000.uint16
packed/{phase}/{lang}/{source}/shard-00000.seq.jsonl
packed/manifest.json
```

`phase` is `warmup`, `stable`, or `decay`. `lang` is `en`, `hi`, `bn`, `ta`, `te`, `kn`, `mr`, or `gu`. `source` is one subsegment, not the parent dataset. Indic specialized sources are the eighteen names above. FineWeb-2 Latin is `fineweb2-latn`. FineWeb-2 native-script is `fineweb2`. English Specialized v1.1 sources are `v11-code-concepts`, `v11-multiple-choice`, `v11-unconditional-algorithmic`, `v11-formal-logic`, and `v11-economics`. CodeAlchemy sources are `code-dev` and `code-enhance`. Nemotron Code v2 sources are `code-v2-question-answering`, `code-v2-student-teacher`, `code-v2-code-review`, `code-v2-rewriting`, and `code-v2-transpilation`. A shard holds about 1,000,000,000 real tokens, or the rest of a small bucket. `uint16` is little-endian and includes `<eod>` and, on a tail, `<pad>`. The jsonl records, per sequence, the real length, the pad length, the document ids with their token spans, and the validation mask. Those spans are the block boundaries for intra-document attention masking and position reset; the trainer builds the block-diagonal mask from them, and a shard whose jsonl lacks the spans is incomplete.

Build it in two streaming passes. Neither pass loads a trillion tokens.

1. Walk each source’s index, not its token bytes. Order documents by blake2b-64 of the document id, the same family as the validation carve, so the cut does not follow file order. Fill the phase quotas with the cumulative rule above. Decay documents are chosen in that hash order up to the decay budget and then sealed. English warmup is the first 25B of the remaining residual in that order; stable is the rest. Indic quotas are the cells above. Specialized quotas are 3/82/15 inside each subsegment, not one specialized bucket.
2. Read each content part sequentially once. Write each document into the shuffle buffer of its assigned bucket. The buffer is 65,536 documents, one seed recorded in the manifest. Pack the buffer’s output into sequences and append them to the current shard. The loader later permutes shard names with a second recorded seed.

That is the whole shuffle: hash order for assignment, a buffer inside the bucket, a permutation of shards. The loader’s job at step time is to advance one cursor per live bucket and take the sequences the cumulative rule asked for. Cursors are sequential reads. Data-parallel ranks can each own a stripe of each shard by sequence index. They do not need a shared shuffle of the token payload.

Before step 0 the manifest’s real-token sum per bucket has to match the budget. A short bucket stays short. The loader does not borrow from another language, another source, another phase, or a second pass. If one half of the 1:1 is short, training stops when the short half is exhausted. A specialized subsegment whose index sum is still unknown is not filled from another subsegment.

## Hindi at 100B

The language weights above are the curriculum. Hindi is 100,000,000,000. The other six share 400,000,000,000. Six times 66,666,666,666 is 399,999,999,996, so the remainder is 4 tokens. Tamil, Telugu, Kannada, and Marathi take one each and are 66,666,666,667. Bengali and Gujarati stay at 66,666,666,666. Those seven integers sum to 500,000,000,000. The packer does not invent the 4 tokens by padding, and it does not move a token from one language onto another.

Phase cells use the same percents and the same remainder-in-stable rule. Gujarati CC-v2 High-Quality then moves 49,629,202 from stable into warmup and 640,478,753 from stable into decay. The batch rule is untouched: 500,000 English and 500,000 Indic, cumulative split, one language and one source per sequence, every language in every step.

Hindi’s share of the Indic half is 21.67% of warmup, 20.05% of stable, and 18.74% of decay. The run-length share is 100/500 = 20%. A flat 20% in every phase is the wrong shortcut, because it would throw away the source percents. Shared Devanagari then sees the phase ratios above, 1.714 in warmup, 1.488 in stable, and 1.500 in decay, still inside every batch, still in separate sequences. The packer does not pull that ratio back toward 1.

A 120B Hindi budget is not this schedule. Six times 63,330,000,000 would have left the Indic half 20,000,000 short of 500B, and the packer still does not close a gap like that by padding.

## What not to do

- **Language blocks.** No English block, no Hindi block, no “finish Devanagari, then start Marathi,” no phase that is one language. Forgetting is what a one-language stretch trains.
- **Subsegment blocks.** No “finish Code-Concepts, then start the rest of Specialized.” No parent-dataset cursor that walks one config to exhaustion. Each subsegment has its own phase weights and its own cursor.
- **Marathi written into Hindi’s script.** No transliteration, no Marathi translated into Hindi to balance the script, no extra copies of shared pieces, no repeated Marathi documents, no pad whose purpose is to make the two languages equal. The language budgets are not a pad, and this packer will not add one.
- **A second epoch.** A short cell stays short. Unique high web is still unused. Synthetic rephrases of pages already in the mix stay out, as do medium-quality slices and FinePDFs. Specialized Latin is not repeated to fill FineWeb-2 Latin.
- **Two languages in one sequence,** including Hindi then Marathi across an `<eod>`. The separator is not the thing that keeps the languages apart. The sequence is.
- **Attention across a document boundary.** Intra-document masking is required: block-diagonal attention and position reset at every `<eod>`, built from the spans in the sequence jsonl. A trainer that lets one document attend into another inside a sequence is not running this spec.
- **A second temperature.** α was how mT5 and XLM-R chose a budget from raw corpus sizes. The budget is already chosen. Another α would undo it.
- **A global shuffle of the token files,** or a rewrite of the immutable bins into phase copies that then have to be retokenized when a weight changes.

## Why this won

The batch is proportional to the phase budgets, and the budgets are already the multilingual decision. [mT5](https://arxiv.org/abs/2010.11934) and [XLM-R](https://arxiv.org/abs/1911.02116) sample a language with probability proportional to (corpus size)^α and both settled on α = 0.3, because α = 1 starves the tail and a very small α starves the head. [XLM-R](https://arxiv.org/html/1911.02116) samples batches from languages and trains on monolingual streams. [mT5](https://arxiv.org/pdf/2010.11934) tried one language at a time and rejected it: the model forgets the languages it is not seeing. BLOOM’s released blend is the crawl-shaped end of that knob, English 30.3%, Hindi 0.7%, Marathi 0.05%, Indic together about 2% ([training configuration](https://github.com/bigscience-workshop/bigscience/blob/master/train/tr11-176B-ml/README.md)). Megatron packed each dataset into 2048-token samples and then blended the datasets ([BLOOM’s data loader](https://huggingface.co/blog/bloom-megatron-deepspeed)). Samples stay one dataset; the blend is the batch. That is the geometry used here, with our budgets instead of BLOOM’s, and with a subsegment where Megatron used a dataset.

Gemma 1 and Gemma 2 do not publish a language temperature. Gemma 1 stages the mixture so high-quality data weighs more at the end ([Gemma](https://arxiv.org/html/2403.08295)). Gemma 3, which does discuss language balance, points at UniMax rather than at a temperature ([Gemma 3](https://arxiv.org/html/2503.19786), [Chung et al.](https://arxiv.org/abs/2304.09151)). UniMax’s complaint about temperature sampling is that the tail gets repeated past the point of use. This run is one pass. [PaLM](https://arxiv.org/html/2204.02311v5) made the same one-epoch choice: mixing proportions picked so no subcomponent is repeated, about 22% of tokens non-English, one shuffle. Our 1:1 is a larger Indic share than PaLM’s, and it is already locked. Packing’s job is to hit it every step, not to reopen it.

Phases are source mix, not language order. [MiniCPM](https://arxiv.org/abs/2404.06395) splits training into warmup, stable, and decay. Once warmup is long enough it stops mattering, a decay of about 10% of tokens matched a full cosine, and 2.5% fell short. Their decay mixes high-quality data into the pretraining data. [OLMo 2](https://arxiv.org/abs/2501.00656) spends the mid-training anneal, 5–10% of training, on a mix that is still about half filtered web: 47.2% DCLM in the 50B anneal ([Dolmino mix](https://huggingface.co/datasets/allenai/dolmino-mix-1124)). [Qwen2.5](https://arxiv.org/html/2412.15115v2) stages pretraining so the mixture can change, and keeps math and code inside pretraining. [Nemotron-CC](https://arxiv.org/html/2412.02595v1) finds the 1.1T high-quality subset, real high pages plus diverse QA, wins a 1T horizon, and finds that swapping repeated high pages for synthetic text beats the repeats. [FineWeb](https://arxiv.org/html/2406.17557) got its gain from per-snapshot curation and an educational filter, and a single global dedup across every snapshot did not beat that. So the decay shards are a different source mix, web stays in them, nothing is repeated to fill them, and the shuffle is inside a bucket. Code stays inside pretraining by giving Code-Concepts its own weight in every phase, rather than a block at one end.

Shared Devanagari is the same lever XLM-R names for capacity: training rate times a shared vocabulary. The vocabulary is frozen. The rate is the phase table, present on every step, in separate sequences. A pad, a repeat, or a second script for Marathi would be a different rate.

## Sources

- [Hu et al., MiniCPM](https://arxiv.org/abs/2404.06395) (2024)
- [OLMo et al., OLMo 2](https://arxiv.org/abs/2501.00656) (2025)
- [Gemma Team, Gemma](https://arxiv.org/html/2403.08295) (2024)
- [Gemma Team, Gemma 3](https://arxiv.org/html/2503.19786) (2025)
- [Qwen Team, Qwen2.5](https://arxiv.org/html/2412.15115v2) (2025)
- [Su et al., Nemotron-CC](https://arxiv.org/html/2412.02595v1) (2024)
- [Zhao et al., intra-document masking and packing](https://arxiv.org/abs/2402.13991) (ACL 2024)
- [Penedo et al., FineWeb](https://arxiv.org/html/2406.17557) (2024)
- [Xue et al., mT5](https://arxiv.org/abs/2010.11934) (2021)
- [Conneau et al., XLM-R](https://arxiv.org/abs/1911.02116) (2020)
- [BigScience Workshop, BLOOM](https://arxiv.org/abs/2211.05100) (2022)
- [BLOOM 176B training configuration](https://github.com/bigscience-workshop/bigscience/blob/master/train/tr11-176B-ml/README.md)
- [The technology behind BLOOM training](https://huggingface.co/blog/bloom-megatron-deepspeed)
- [Chowdhery et al., PaLM](https://arxiv.org/abs/2204.02311) (2022)
- [Chung et al., UniMax](https://arxiv.org/abs/2304.09151) (2023)
