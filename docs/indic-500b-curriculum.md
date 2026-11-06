---
cursor:
  subagentId: "bc-8933ff20-4f5f-5085-ba48-7ebfdd02ad11"
---

# Indic half, 500B

Decided 2026-11-01. Language totals were reset 2026-11-02: Hindi is 100,000,000,000 and the other six languages share 400,000,000,000. Revised the same day so every specialized subsegment is its own row. FineWeb-2 Latin is the census of that day, taken in full, and the unmeasured Latin budget is deleted. This is the Indic half of the 1T run. English stays the locked 500B in [english-500b-mix.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/english-500b-mix.md). Personas-India stays on that English side. The two streams are drawn 1:1, so the last 50B of this schedule is the Indic side of the same decay window as the English last 50B.

Three phases. The tokens are the authority. A percent is that column divided by the row.

| Phase | Tokens | Share of the 500B |
| --- | ---: | ---: |
| Warmup | 25,000,000,000 | 5% |
| Stable | 425,000,000,000 | 85% |
| Decay | 50,000,000,000 | 10% |
| **Sum** | **500,000,000,000** | **100%** |

One pass. A short row is not refilled from another row, and it is not padded. Medium-quality slices, FinePDFs, and v2.1 High-Quality-Synthetic are out. Inside a phase, shuffle. A parent dataset with real subsegments is not one source.

## The 500B

This Latin add is FineWeb-2 Latin (`hin_Latn`, `ben_Latn`, `tam_Latn`, `tel_Latn`, `kan_Latn`, `mar_Latn`, `guj_Latn`). The count is the census in [indic-fineweb2-latin-token-counts.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-fineweb2-latin-token-counts.md), 2026-11-02 12:53:56 IST: Hindi 213,997,119, Bengali 32,304,488, Tamil 14,567,775, Telugu 43,769,009, Kannada 2,238,695, Marathi 3,069,278, Gujarati 1,458,353. That is 311,404,717 tokens, 139,953 documents, 7 files. Each language takes its own count in full. Specialized Latin stays 12,778,755,736 inside the specialized rows and is not repeated. Total Indic Latin is 13,090,160,453. Nemotron-CC was not cut.

Specialized is eighteen rows: nine `_source_config` values, each native and each Latin. The schedule takes every token in those rows, and the fourteen language totals sum to 142,351,065,175. The index sum is per language only ([indic-specialized-token-counts.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-specialized-token-counts.md)). Per-subsegment `token_count` was not readable from this machine. `s3://nemotron-training-data-us-east-1/datasets/nemotron-indic-specialized-v1/` returned 403. No credentials were available, and no instance was launched. The sample projection in [indic-specialized-token-projection.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-specialized-token-projection.md) is not the budget and is not copied into the cells below.

v2.1 `High-Quality` and v2.1 `High-Quality-DQA` are exact census sums, and this schedule uses all of those. v2 `High-Quality` is an exact draw against the census, stopped at each language's target, and that draw was not reduced to fund Latin. v2 `Diverse-QA` is in that census and this schedule uses none of it. Nemotron-CC v2 and v2.1, including High-Quality and High-Quality-DQA, are English Common Crawl translated into the seven languages. They are not native pages.

| Segment | Tokens in the 500B | Pool | Kind |
| --- | ---: | ---: | --- |
| Specialized, 18 subsegment rows, sum not a source | 142,351,065,175 | 142,351,065,175 exact by language, not by subsegment | exact language sums; subsegment tokens not counted |
| Nemotron-CC-v2 `High-Quality` | 196,699,657,060 | 297,883,741,274 exact | exact draw, not cut |
| Sangraha verified, seven native | 39,896,056,641 | 39,896,056,641 exact | exact, all of it |
| FineWeb-2 Latin, seven prefixes | 311,404,717 | 311,404,717 exact, 139,953 documents | exact, all of it |
| IndicCorp v2, seven native | 19,082,131,730 | 19,082,131,730 exact | exact, all of it |
| Nemotron-CC-v2.1 `High-Quality` | 39,358,454,892 | 39,358,454,892 exact | exact, all of it |
| Nemotron-CC-v2.1 `High-Quality-DQA` | 25,546,894,943 | 25,546,894,943 exact | exact, all of it |
| FineWeb-2 native-script | 36,754,334,842 | 37,065,739,559 exact | draw, pool minus FineWeb-2 Latin |
| Nemotron-CC-v2 `Diverse-QA` | 0 | 183,859,414,061 exact | exact, none of it |
| **Sum** | **500,000,000,000** |  |  |

Specialized exact source: [indic-specialized-token-counts.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-specialized-token-counts.md), language totals only. FineWeb-2, IndicCorp v2, and Sangraha exact source: [indic-other-token-counts.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-other-token-counts.md). v2 `High-Quality`, v2 `Diverse-QA`, and v2.1 `High-Quality` exact source: [indic-cc-token-counts.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-cc-token-counts.md). v2.1 `High-Quality-DQA` exact source: [indic-cc-dqa-token-counts.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-cc-dqa-token-counts.md). Byte and document layout of the eighteen specialized rows: [indic-specialized-segment-layout.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-specialized-segment-layout.md) and [indic-specialized-segment-counts.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-specialized-segment-counts.md).

Arithmetic. Specialized plus the native-script draws plus FineWeb-2 Latin is 142,351,065,175 + 95,732,523,213 + 311,404,717 = 238,394,993,105. The Common Crawl room under a 500B cap is 500,000,000,000 − 238,394,993,105 = 261,605,006,895. v2.1 `High-Quality` 39,358,454,892 plus `High-Quality-DQA` 25,546,894,943 plus the v2 `High-Quality` draw 196,699,657,060 is that room. v2 `Diverse-QA` contributes 0. Nemotron-CC was not cut.

v2.1 `High-Quality` 39,358,454,892 is the sum of the seven language cells in the census, and it matches the published all-seven total. `High-Quality-DQA` 25,546,894,943 is the sum of its seven language cells. There is no rounding token.

The unmeasured Latin budget is deleted. FineWeb-2 native and IndicCorp v2 are the pools in [indic-other-token-counts.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-other-token-counts.md), restored in full, minus only that language’s FineWeb-2 Latin. The Latin count is smaller than FineWeb-2 native in every language, so the reduction stays on FineWeb-2 native. IndicCorp v2 is the full pool. Sangraha is full. v2 `High-Quality` stays 196,699,657,060, because every language still meets its cap. Code-Concepts is not cut. No language borrows from another.

## Where each segment sits

Nominal rule, applied per language with integer division (`n * percent // 100`, remainder in stable). Specialized uses 3/82/15 on every subsegment. The language-level specialized cells are that same rule on the language total, and they are a check sum: adding the subsegment floors can differ by fewer than 20 tokens per language per edge. FineWeb-2 Latin and FineWeb-2 native use 10/80/10. Sangraha uses 10/70/20. IndicCorp uses 0/100/0. CC-v2 High-Quality uses 5/93/2. CC-v2.1 High-Quality uses 8/80/12. CC-v2.1 High-Quality-DQA uses 0/70/30. Those nominal sums are warmup 24,950,370,798, stable 425,690,107,955, and decay 49,359,521,247. Gujarati v2 `High-Quality` then moves 49,629,202 tokens from stable into warmup and 640,478,753 tokens from stable into decay, so the phase totals are exactly 25B, 425B, and 50B. Every other cell keeps the nominal rule. The tokens below are after that move.

| Segment | Warmup | Stable | Decay | Nominal rule |
| --- | ---: | ---: | ---: | --- |
| Specialized, sum of 18 rows, not a source | 4,270,531,951 | 116,727,873,450 | 21,352,659,774 | 3% / 82% / 15% on every subsegment |
| CC-v2 `High-Quality` | 9,884,612,052 | 182,240,573,118 | 4,574,471,890 | 5% / 93% / 2%, then the Gujarati move |
| Sangraha verified | 3,989,605,661 | 27,927,239,655 | 7,979,211,325 | 10% / 70% / 20% |
| FineWeb-2 Latin | 31,140,467 | 249,123,783 | 31,140,467 | 10% / 80% / 10%, census |
| IndicCorp v2 | 0 | 19,082,131,730 | 0 | 0% / 100% / 0% |
| CC-v2.1 `High-Quality` | 3,148,676,388 | 31,486,763,921 | 4,723,014,583 | 8% / 80% / 12% |
| CC-v2.1 `High-Quality-DQA` | 0 | 17,882,826,463 | 7,664,068,480 | 0% / 70% / 30% |
| FineWeb-2 native-script | 3,675,433,481 | 29,403,467,880 | 3,675,433,481 | 10% / 80% / 10% |
| CC-v2 `Diverse-QA` | 0 | 0 | 0 | 0% / 70% / 30%, none drawn |
| **Phase total** | **25,000,000,000** | **425,000,000,000** | **50,000,000,000** |  |

Decay composition of the 50,000,000,000. The tokens sum to the phase. The shares are rounded and add to 99.999%.

| Piece | Tokens | Share of decay |
| --- | ---: | ---: |
| Specialized, all 18 rows | 21,352,659,774 | 42.705% |
| CC-v2.1 `High-Quality-DQA` | 7,664,068,480 | 15.328% |
| Sangraha verified | 7,979,211,325 | 15.958% |
| FineWeb-2 Latin | 31,140,467 | 0.062% |
| FineWeb-2 native-script | 3,675,433,481 | 7.351% |
| Translated v2 and v2.1 `High-Quality` | 9,297,486,473 | 18.595% |
| **Decay** | **50,000,000,000** | **100%** |

FineWeb-2 Latin, FineWeb-2 native-script, and translated High-Quality in decay are 13,004,060,421, which is 26.008% of the phase. Sangraha adds another 7,979,211,325 of verified native prose. Prose together is 20,983,271,746, 41.967% of decay. Translated High-Quality is lighter than specialized and heavier than Sangraha. FineWeb-2 Latin is 0.062% of decay.

Warmup composition of the 25,000,000,000: CC-v2 `High-Quality` 9,884,612,052, Specialized 4,270,531,951, Sangraha 3,989,605,661, FineWeb-2 native-script 3,675,433,481, CC-v2.1 `High-Quality` 3,148,676,388, FineWeb-2 Latin 31,140,467. IndicCorp and both diverse-QA rows are absent from warmup. Code-Concepts is not absent from warmup.

## Why these phases

The learning-rate shape is warmup, then a constant peak, then decay. MiniCPM calls that warmup-stable-decay. On their small-model sweeps, a decay of about 10% of tokens matched a full cosine, and a decay of 2.5% fell short. Their decay is a mixture of the pretraining data and high-quality ability data, and the loss drop in that window is the reason they put the ability data there ([Hu et al., 2024](https://arxiv.org/abs/2404.06395)). This run uses that 10% window. It is also the English half's last 50B, so a 1:1 draw puts both decays on the same steps. The peak learning rate is not chosen here.

Gemma stages the mixture so relevant, high-quality data weighs more toward the end of training ([Gemma Team, 2024](https://arxiv.org/html/2403.08295v2)). Qwen2.5 stages pretraining so the mixture can change, keeps math and code inside pretraining, and upsamples science and academic text after a quality filter ([Qwen Team, 2025](https://arxiv.org/html/2412.15115v2)). OLMo 2 spends the mid-training anneal, 5–10% of training, on a mix that is still about half filtered web and half curated math, instruction, wiki, and papers ([OLMo et al., 2025](https://arxiv.org/abs/2501.00656)). The Indic decay does the same kind of raise inside the high band we already kept: Specialized moves from 28.470% of the run to 42.705% of decay, Sangraha from 7.979% of the run to 15.958% of decay, and v2.1 `High-Quality-DQA` from 5.109% of the run to 15.328% of decay. FineWeb-2 native, FineWeb-2 Latin, and translated High-Quality together stay in the phase, at 26.008%, in the same neighborhood as the 12B of ClimbMix inside the English last 50B. FineWeb-2 Latin is the small part of that 26.008%.

Warmup is 5%. MiniCPM finds the warmup length stops mattering once it is long enough, and their stable stage is the broad pretraining mix. Warmup here includes every specialized subsegment at 3% of that subsegment, not only Wiki-Rewrite and Math-Textbooks.

Chinchilla's Table 3 puts a 1B model at 20.2B compute-optimal tokens, and the paper's own caveat is that scaling tokens helps when the data is high quality ([Hoffmann et al., 2022](https://arxiv.org/pdf/2203.15556.pdf)). MiniCPM's warmup-stable-decay fits land at a higher token-per-parameter ratio than Chinchilla. Gemma 2 trains a 2B model on 2T tokens ([Gemma Team, 2024](https://arxiv.org/html/2408.00118)). This 1T run sits in that overtrained small-model region, so the cut is which high tokens to keep.

## Why this cut of the pool

The exact native-script draw is 95,732,523,213 tokens. The exact specialized text is 142,351,065,175. Both are one pass. Repeating them to use less Common Crawl would spend a second epoch while unique high web is still sitting unused. Up to about four epochs, repetition is close to unique data on the loss Muennighoff et al. measured, and past that the extra compute fades ([Muennighoff et al., 2023](https://arxiv.org/abs/2305.16264)). Unique still wins. This schedule stays at one epoch. Specialized Latin is already inside the specialized rows. It is not trained again as FineWeb-2 Latin.

Nemotron-CC's short-horizon winner, the 1.1T high-quality subset, is the highest-scoring real documents plus diverse question-answer pairs. The other synthetic rephrases exist to manufacture fresh tokens once high-quality pages would otherwise be repeated. Their long 15T run drops medium and medium-high in the second phase and keeps high real and high synthetic ([Su et al., 2024](https://arxiv.org/html/2412.02595v2)). This run is the short-horizon case: v2 `High-Quality` is counted at 297,883,741,274, and the schedule uses 196,699,657,060 of it. The unused 101,184,084,214 is why v2.1 `High-Quality-Synthetic` (counted 52,887,676,757) is out. It is a rephrase of high pages already in the mix. That unused high web was not spent on FineWeb-2 Latin. v2.1 `High-Quality-DQA` stays, all 25,546,894,943 counted tokens, because that is the diverse-QA half of the subset Nemotron-CC actually won with.

FineWeb's educational filter beat unfiltered web at a matched token budget ([Penedo et al., 2024](https://arxiv.org/html/2406.17557)), and FineWeb2's per-language filters are the multilingual version of that pipeline ([Penedo et al., 2025](https://arxiv.org/abs/2506.20920)). FineWeb-2 Latin and FineWeb-2 native-script are each in every phase at 10% / 80% / 10%, for all seven languages. The native draw is the pool minus that language’s Latin count. Sangraha verified is human-checked web, PDF, and transcripts ([Khan et al., 2024](https://aclanthology.org/2024.acl-long.843.pdf)). It is the native set that gets a real decay upweight, 20% of its tokens, and it was not cut. IndicCorp v2 is the news crawl with human-checked source sites ([Doddapaneni et al., 2023](https://aclanthology.org/2023.acl-long.693.pdf)). On our tokenizer the corpus is 19,082,131,730 tokens over 237,423,958 documents, 80.4 tokens per document. The draw is that full corpus, and it stays in stable. FineWeb-2 and Sangraha are both about 696 tokens per document on the full corpora.

No language needs v2 `Diverse-QA`. After specialized, FineWeb-2 Latin, FineWeb-2 native, IndicCorp v2, Sangraha, v2.1 `High-Quality`, and real `High-Quality-DQA`, every target closes inside that language's own v2 `High-Quality`. Kannada is the tightest: the draw is 32,387,351,380 of a pool of 39,072,152,508, leaving 6,684,801,128. Hindi leaves 9,341,243,012 of 44,289,055,503. The counted v2 `Diverse-QA` pool, 183,859,414,061, stays out.

## Languages

Hindi is 100,000,000,000. The other six languages share the remaining 400,000,000,000. Integer division gives 66,666,666,666 with a remainder of 4 tokens. Those 4 tokens go one each to the last four language codes among the six, `kn`, `mr`, `ta`, and `te`, so Tamil, Telugu, Kannada, and Marathi are 66,666,666,667. Bengali and Gujarati stay at 66,666,666,666. The seven totals sum to 500,000,000,000. That remainder is a real token inside each of those four languages' own pools. It is not pad, and it is not taken from another language.

The specialized total, including that language's Latin configs, is exact and is taken in full. FineWeb-2 Latin is the census, taken in full. FineWeb-2 native is that language's pool minus its Latin count. IndicCorp and Sangraha are taken in full. Then each language takes all of its v2.1 `High-Quality` and all of its real `High-Quality-DQA`. v2 `High-Quality` fills the rest of that language's target and is not cut. v2 `Diverse-QA` is not used.

| Language | Specialized | FineWeb-2 Latin | FineWeb-2 native | IndicCorp v2 | Sangraha | Native subtotal | v2 High-Quality | v2.1 High-Quality | v2.1 DQA | v2 Diverse-QA | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hindi `hi` | 21,267,404,162 | 213,997,119 | 14,450,404,119 | 8,598,473,855 | 11,018,433,554 | 34,067,311,528 | 34,947,812,491 | 5,792,591,565 | 3,710,883,135 | 0 | 100,000,000,000 |
| Bengali `bn` | 20,063,342,514 | 32,304,488 | 10,821,516,763 | 1,861,152,984 | 9,477,011,253 | 22,159,681,000 | 15,250,573,737 | 5,599,141,473 | 3,561,623,454 | 0 | 66,666,666,666 |
| Tamil `ta` | 20,598,403,258 | 14,567,775 | 3,958,241,564 | 1,179,759,699 | 5,447,566,137 | 10,585,567,400 | 26,425,095,607 | 5,485,027,435 | 3,558,005,192 | 0 | 66,666,666,667 |
| Telugu `te` | 21,339,943,784 | 43,769,009 | 1,761,216,142 | 1,886,816,677 | 4,698,361,415 | 8,346,394,234 | 27,244,736,215 | 5,864,830,338 | 3,826,993,087 | 0 | 66,666,666,667 |
| Kannada `kn` | 19,242,977,088 | 2,238,695 | 1,571,429,244 | 2,245,371,670 | 2,341,566,193 | 6,158,367,107 | 32,387,351,380 | 5,317,795,029 | 3,557,937,368 | 0 | 66,666,666,667 |
| Marathi `mr` | 19,412,121,908 | 3,069,278 | 2,592,434,223 | 1,515,965,336 | 3,593,008,562 | 7,701,408,121 | 30,460,713,089 | 5,459,456,470 | 3,629,897,801 | 0 | 66,666,666,667 |
| Gujarati `gu` | 20,426,872,461 | 1,458,353 | 1,599,092,787 | 1,794,591,509 | 3,320,109,527 | 6,713,793,823 | 29,983,374,541 | 5,839,612,582 | 3,701,554,906 | 0 | 66,666,666,666 |
| **Sum** | **142,351,065,175** | **311,404,717** | **36,754,334,842** | **19,082,131,730** | **39,896,056,641** | **95,732,523,213** | **196,699,657,060** | **39,358,454,892** | **25,546,894,943** | **0** | **500,000,000,000** |

Native-script text is 95,732,523,213 of the 500B, 19.15%: the FineWeb-2 native draw, the full IndicCorp v2, and Sangraha verified. Hindi's own row is 34.1% native-script. Kannada's is 9.2%. FineWeb-2 Latin is not in that native-script share. The Nemotron-CC rows that fill the rest, v2 `High-Quality`, v2.1 `High-Quality`, and v2.1 `High-Quality-DQA`, are English Common Crawl translated into that language. They are not native pages. Hindi's extra tokens, relative to the other six, are still translated Hindi v2 `High-Quality`. Specialized in the table includes the Latin config for that language (12,778,755,736 tokens across the seven).

Every language fits in its own high pool: all specialized subsegments, the FineWeb-2 Latin census, FineWeb-2 native after its Latin count is removed, all of IndicCorp v2, all Sangraha, all of that language's v2.1 `High-Quality`, all of its real `High-Quality-DQA`, then v2 `High-Quality`, then v2 `Diverse-QA` only if still short. None is short, and none reaches `Diverse-QA`. The smallest margin inside v2 `High-Quality` is Kannada's 6,684,801,128. Counting `Diverse-QA` as well, Kannada's high pool is 98,759,801,175 against a target of 66,666,666,667.

Phase totals by language, after the same per-language percents and the Gujarati move:

| Language | Warmup | Stable | Decay | Total |
| --- | ---: | ---: | ---: | ---: |
| Hindi | 5,417,103,550 | 85,215,326,818 | 9,367,569,632 | 100,000,000,000 |
| Bengali | 3,845,443,527 | 54,785,541,902 | 8,035,681,237 | 66,666,666,666 |
| Tamil | 3,320,046,617 | 56,515,958,641 | 6,830,661,409 | 66,666,666,667 |
| Telugu | 3,121,956,205 | 56,826,775,808 | 6,717,934,654 | 66,666,666,667 |
| Kannada | 3,013,603,895 | 57,787,672,538 | 5,865,390,234 | 66,666,666,667 |
| Marathi | 3,161,007,033 | 57,262,370,910 | 6,243,288,724 | 66,666,666,667 |
| Gujarati | 3,120,839,173 | 56,606,353,383 | 6,939,474,110 | 66,666,666,666 |
| **Sum** | **25,000,000,000** | **425,000,000,000** | **50,000,000,000** | **500,000,000,000** |

Hindi:Marathi is 5,417,103,550 : 3,161,007,033 in warmup (1.714), 85,215,326,818 : 57,262,370,910 in stable (1.488), and 9,367,569,632 : 6,243,288,724 in decay (1.500). Across the run it is 100,000,000,000 : 66,666,666,667 (1.500).

Hindi is the largest row in every phase because its budget is 100B. Bengali is second in warmup and in decay because it holds more Sangraha, and 20% of Sangraha sits in decay. Every language is in every phase. The smallest decay row is Kannada at 5,865,390,234. The smallest warmup row is Kannada at 3,013,603,895.

Fill order inside a language, stopping at the target: all eighteen specialized rows, that language's FineWeb-2 Latin census, FineWeb-2 native after its Latin count is removed, all of IndicCorp v2, and Sangraha; then all of that language's v2.1 `High-Quality`; then all of its real v2.1 `High-Quality-DQA`; then v2 `High-Quality`; then that language's v2 `Diverse-QA` only if it is still short. Do not cross 500,000,000,000. Do not refill a short cell from medium quality, from `High-Quality-Synthetic`, from FinePDFs, from code, or from another language. Do not pad.

## Specialized subsegments

The nine `_source_config` values are the real ones in [indic-specialized-segment-layout.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-specialized-segment-layout.md). Native and Latin are separate rows. The exact token census is per language, not per subsegment. Native document counts from [indic-specialized-segment-counts.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-specialized-segment-counts.md): Math-Textbooks 18,983,422, Code-Concepts 28,058,409, Wiki-Rewrite 15,716,427, STEM-SFT 10,258,707, Multiple-Choice 6,448,500, Formal-Logic 898,780, RQA 692,084, Economics 632,453, Unconditional-Algorithmic 316,304. Those nine native counts sum to 82,005,086 documents. Latin document counts were not scanned. A config with no files for a subsegment contributes nothing. `hi-Latn-IN` has no Economics and no Unconditional-Algorithmic. `bn-Latn-IN` and `mr-Latn-IN` have no Unconditional-Algorithmic.

Each existing row is in warmup, stable, and decay at 3% / 82% / 15% of its own tokens, remainder in stable. Code-Concepts native and Code-Concepts Latin each use that rule. Code-Concepts is not piled into one phase, and it is not fed as a block before the rest of Specialized. The old draw that put warmup only on Wiki-Rewrite and Math-Textbooks is not this schedule.

| Subsegment | Script | Documents | Bytes | Tokens | Phase weight |
| --- | --- | ---: | ---: | --- | --- |
| `Math-Textbooks` | native | 18,983,422 | 186,237,289,934 | not counted | 3% / 82% / 15% |
| `Math-Textbooks` | Latin | not scanned | 15,902,221,221 | not counted | 3% / 82% / 15% |
| `Code-Concepts` | native | 28,058,409 | 157,101,174,048 | not counted | 3% / 82% / 15% |
| `Code-Concepts` | Latin | not scanned | 14,920,601,968 | not counted | 3% / 82% / 15% |
| `Wiki-Rewrite` | native | 15,716,427 | 70,153,732,535 | not counted | 3% / 82% / 15% |
| `Wiki-Rewrite` | Latin | not scanned | 7,784,683,556 | not counted | 3% / 82% / 15% |
| `STEM-SFT` | native | 10,258,707 | 133,411,672,993 | not counted | 3% / 82% / 15% |
| `STEM-SFT` | Latin | not scanned | 13,177,277,696 | not counted | 3% / 82% / 15% |
| `Multiple-Choice` | native | 6,448,500 | 22,657,813,689 | not counted | 3% / 82% / 15% |
| `Multiple-Choice` | Latin | not scanned | 2,508,810,853 | not counted | 3% / 82% / 15% |
| `Formal-Logic` | native | 898,780 | 930,066,288 | not counted | 3% / 82% / 15% |
| `Formal-Logic` | Latin | not scanned | 126,572,705 | not counted | 3% / 82% / 15% |
| `RQA` | native | 692,084 | 13,833,232,468 | not counted | 3% / 82% / 15% |
| `RQA` | Latin | not scanned | 4,473,219,246 | not counted | 3% / 82% / 15% |
| `Economics` | native | 632,453 | 914,428,721 | not counted | 3% / 82% / 15% |
| `Economics` | Latin | not scanned | 131,744,514 | not counted | 3% / 82% / 15% |
| `Unconditional-Algorithmic` | native | 316,304 | 1,507,605,104 | not counted | 3% / 82% / 15% |
| `Unconditional-Algorithmic` | Latin | not scanned | 91,004,880 | not counted | 3% / 82% / 15% |

Code-Concepts native is 28,058,409 documents and 157,101,174,048 bytes. Code-Concepts Latin is 14,920,601,968 bytes and 219 objects. The token totals are not in the index census. They are not estimated here. Phase cells in tokens for those two rows are therefore not assigned. The weight is 3% warmup, 82% stable, 15% decay of whatever the index sum is, separately for native and for Latin.

## Held out, and the DQA restore

Val tokens that sit inside a row this schedule still draws are masked at train time. Do not refill them. The census holdout is FineWeb-2 10,300,598, IndicCorp v2 1,155,338, Sangraha verified 9,701,494. Every language draws FineWeb-2 native, IndicCorp v2, and Sangraha, so those val documents stay inside the draw and are masked. The FineWeb-2 Latin count is not taken out of the val carve.

v2.1 `High-Quality-DQA` documents are restored: 17,425,910 rows, matching the census ([indic-cc-dqa-restore.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-cc-dqa-restore.md)). The tokens are the census in [indic-cc-dqa-token-counts.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/indic-cc-dqa-token-counts.md): Hindi 3,710,883,135, Bengali 3,561,623,454, Tamil 3,558,005,192, Telugu 3,826,993,087, Kannada 3,557,937,368, Marathi 3,629,897,801, Gujarati 3,701,554,906. If a language is short at launch, that language's row shrinks by the missing tokens, 70% of the loss in stable and 30% in decay. Do not backfill.

No benchmark scan and no global MinHash on this mix. The sources are used as released.

## Out

- Nemotron-CC-v2 `Medium-High-Quality`, counted 134,060,510,124.
- Nemotron-CC-v2.1 `Medium-High-Quality`, counted 9,279,276,642.
- Nemotron-CC-v2.1 `Medium-High-Quality-Synthetic`, counted 32,693,654,346.
- Nemotron-CC-v2.1 `High-Quality-Synthetic`, counted 52,887,676,757. Rephrases of high pages the schedule already trains.
- Nemotron-CC-v2 `Diverse-QA`, counted 183,859,414,061. No language draws it.
- `HuggingFaceFW/finepdfs-edu`, projected 21,720,083,734. It was excluded from the census.
- The unused 101,184,084,214 of v2 `High-Quality` (297,883,741,274 − 196,699,657,060). Not spent on Latin.
- Sangraha synthetic, Sangraha unverified, and Sangraha languages outside these seven. They are not in the exact 39,896,056,641.
- Personas-India. English side.
- A second epoch of any row, including Specialized Latin.

## Sources

- [Hu et al., MiniCPM](https://arxiv.org/abs/2404.06395) (2024)
- [Gemma Team, Gemma](https://arxiv.org/html/2403.08295v2) (2024)
- [Gemma Team, Gemma 2](https://arxiv.org/html/2408.00118) (2024)
- [Qwen Team, Qwen2.5 Technical Report](https://arxiv.org/html/2412.15115v2) (2025)
- [OLMo et al., OLMo 2](https://arxiv.org/abs/2501.00656) (2025)
- [Hoffmann et al., Chinchilla](https://arxiv.org/pdf/2203.15556.pdf) (2022)
- [Muennighoff et al., Scaling Data-Constrained Language Models](https://arxiv.org/abs/2305.16264) (2023)
- [Su et al., Nemotron-CC](https://arxiv.org/html/2412.02595v2) (2024)
- [Penedo et al., FineWeb](https://arxiv.org/html/2406.17557) (2024)
- [Penedo et al., FineWeb2](https://arxiv.org/abs/2506.20920) (2025)
- [Khan et al., IndicLLMSuite / Sangraha](https://aclanthology.org/2024.acl-long.843.pdf) (2024)
- [Doddapaneni et al., IndicCorp v2](https://aclanthology.org/2023.acl-long.693.pdf) (2023)
