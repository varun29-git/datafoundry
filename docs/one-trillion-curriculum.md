# From-scratch curriculum, 1T — final

Final 2026-11-06. Supersedes every earlier revision of this file, including the 2026-11-03 decay revision and the 2026-11-04 Code v2 census. The halves [english-500b-mix.md](english-500b-mix.md) and [indic-500b-curriculum.md](indic-500b-curriculum.md) are background; this file is the authority. Packing is [multilingual-batch-packing.md](multilingual-batch-packing.md).

## The run

1,000,000,000,000 tokens = **500,000,000,000 English + 500,000,000,000 Indic** (Hindi, Marathi, Kannada, Telugu, Tamil, Gujarati, Bengali), drawn **1:1 on the same steps**: every 1,000,000-token batch is 500,000 English + 500,000 Indic real tokens, all seven Indic languages in every step. One pass. A short row is not refilled from another row, and it is not padded. No second epoch of anything.

Model: a ~1.2–1.5B dense Transformer, from scratch. The last **200,000,000,000 tokens run ternary QAT** (weights-only {-1,0,+1}, BitCPM4 recipe: LR re-warmup at ~half the dense peak, λ-ramp quantization warmup, checkpoints at 30B/100B/200B of QAT). QAT is fixed at 200B in every total-budget case: it is 2× the decay window, the validated BitCPM4 rule.

| Segment | English | Indic | Combined | What happens there |
| --- | ---: | ---: | ---: | --- |
| Warmup | 25,000,000,000 | 25,000,000,000 | 50,000,000,000 | dense, LR warmup |
| Stable (dense) | 375,000,000,000 | 375,000,000,000 | 750,000,000,000 | dense, constant peak LR |
| Stable (QAT) | 50,000,000,000 | 50,000,000,000 | 100,000,000,000 | **ternary QAT starts at step 800B** |
| Decay (QAT) | 50,000,000,000 | 50,000,000,000 | 100,000,000,000 | QAT, LR decays to zero |
| **Sum** | **500,000,000,000** | **500,000,000,000** | **1,000,000,000,000** | |

Dense branch point: step 800B. There is no annealed dense checkpoint by design; the dense 800B checkpoint is saved at peak LR and a small side anneal can be run later for a dense baseline.

## Extension to 2T (throughput-dependent)

The stable stream is one append-only, uniformly shuffled sequence. The 2T case does not restart anything: keep training at constant LR to step 1,800B (stable 850B → 1,850B), then the same 200B QAT window (decay stays 100B; the branch-time decay-B option extends decay to 200B from extension pools if the MiniCPM fraction reading is preferred then). Reserved extension pools, not to be spent elsewhere:

- **English +500B**: ClimbMix leftover ~135B + Nemotron-CC-Code-v1 pool ~396B + Genesis III leftover 28B.
- **Indic +500B**: v2 High-Quality leftover 101.2B + v2 Diverse-QA 183.9B + CC-Latin 101.4B (28.6B HQ-tier + 58.6B DQA + 14.2B synthetic); the last ~128B needs one rule relaxation (v2 MHQ 134.1B) — deferred.

## English half, 500,000,000,000

Every row verified: warmup 25B / stable 425B / decay 50B / total 500B, exact. Warmup is the largest-remainder cut of residuals (`residual × 25,000,000,000 // 450,000,000,000`, 9 remainder tokens to the nine largest fractional parts). Stable is total minus warmup minus decay.

| Source | Warmup | Stable | Decay | Total |
| --- | ---: | ---: | ---: | ---: |
| ClimbMix | 12,273,782,949 | 208,654,310,137 | 20,000,000,000 | 240,928,093,086 |
| Math 4+ | 3,077,777,778 | 52,322,222,222 | 6,000,000,000 | 61,400,000,000 |
| Code v2 `Synthetic-Rewriting` | 2,188,888,889 | 37,211,111,111 | 600,000,000 | 40,000,000,000 |
| Code v2 `Synthetic-Question-Answering` | 1,473,387,007 | 25,047,579,126 | 2,100,000,000 | 28,620,966,133 |
| UltraData-Code L3 | 744,444,444 | 12,655,555,556 | 12,000,000,000 | 25,400,000,000 |
| InfiniByte | 1,111,111,111 | 18,888,888,889 | 2,500,000,000 | 22,500,000,000 |
| Genesis III, option-level | 722,222,222 | 12,277,777,778 | 2,000,000,000 | 15,000,000,000 |
| RQA | 744,444,444 | 12,655,555,556 | 1,000,000,000 | 14,400,000,000 |
| Specialized v1.1 `Code-Concepts` | 490,628,657 | 8,340,687,172 | 1,380,000,000 | 10,211,315,829 |
| CodeAlchemy `code-dev` | 396,825,397 | 6,746,031,746 | 0 | 7,142,857,143 |
| Code v2 `Synthetic-Code-Review` | 504,923,032 | 8,583,691,539 | 700,000,000 | 9,788,614,571 |
| Fact-Seeking | 505,555,556 | 8,594,444,444 | 500,000,000 | 9,600,000,000 |
| Nemotron-Personas-India | 210,702,084 | 3,581,935,430 | 500,000,000 | 4,292,637,514 |
| Code v2 `Synthetic-Transpilation` | 204,863,756 | 3,482,683,853 | 350,000,000 | 4,037,547,609 |
| Code v2 `Synthetic-Student-Teacher` | 149,007,838 | 2,533,133,249 | 250,000,000 | 2,932,141,087 |
| CodeAlchemy `code-enhance` | 158,730,159 | 2,698,412,698 | 0 | 2,857,142,857 |
| Specialized v1.1 `Multiple-Choice` | 37,454,825 | 636,732,015 | 105,000,000 | 779,186,840 |
| Specialized v1.1 `Unconditional-Algorithmic` | 3,183,090 | 54,112,537 | 9,000,000 | 66,295,627 |
| Specialized v1.1 `Formal-Logic` | 1,125,138 | 19,127,336 | 3,000,000 | 23,252,474 |
| Specialized v1.1 `Economics` | 941,624 | 16,007,606 | 3,000,000 | 19,949,230 |
| **English half** | **25,000,000,000** | **425,000,000,000** | **50,000,000,000** | **500,000,000,000** |

What each code row is for: `Rewriting` is the backbone — real GitHub Python rephrased by Qwen3-32B under SGCR/SCOR prompts (natural distribution, cleaned). `Question-Answering` teaches problem-solving. `Code-Review` teaches critique-then-improve. `Transpilation` is Python→C++ augmentation. `Student-Teacher` is explanatory dialogue. CodeAlchemy is developer-task traces. `Code-Concepts` is taxonomy-targeted coverage. UltraData-Code L3 is grounded exercises (task→analysis→solution→test, task+solution serialization) and is the spine of the decay window. Nemotron-CC-Code-v1 is **out** (zero): no natural-CC-code anchor; the tripwire is UltraData-Code L2 if code probes look synthetic-narrow.

Code totals: English 130.99B (26.2% of the half) + Indic 18.96B = **149.95B, 15.0% of the run**. Programming-language profile: Python ~65–70%, C++ ~8.8B (transpilation + review + L3-cpp), Java ~6.6B, JS ~2B; other languages only what rides inside the 11-language QA and 15-language CodeAlchemy rows.

### English decay window, 50B

ClimbMix 20 (40% web — the OLMo-2/SmolLM web floor) · UltraData-Code L3 12 (24% — exercises as the instruction-format spine) · Math 4+ 6 · Code v2 splits 4 (QA 2.1, Review 0.7, Rewriting 0.6, Transpilation 0.35, Student-Teacher 0.25) · Genesis 2 · RQA 1.0 · InfiniByte 2.5 · Specialized v1.1 1.5 · Fact-Seeking 0.5 · Personas-India 0.5. Code+exercises ≈ 35% of the window (the Blakeney/Aryabumi code-cooldown pattern); web floor held at 40%.

### The QAT window, last 200B per half

QAT = last 50B of stable (each stable cell × 50/425) + the 50B decay. English side composition: ClimbMix 44.5%, L3 13.5%, Math 4+ 12.2%, code rows 30.6%, reasoning/QA rows ~8%, personas 0.9%. All seven Indic languages and English are present in every QAT step at the locked ratios.

## Indic half, 500,000,000,000

Unchanged from [indic-500b-curriculum.md](indic-500b-curriculum.md); verified cell-by-cell. Hindi 100B; the other six share 400B with the 4 remainder tokens to ta/te/kn/mr.

| Language | Specialized | FW2 Latin | FW2 native | IndicCorp | Sangraha | v2 HQ (draw) | v2.1 HQ | v2.1 DQA | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hindi | 21,267,404,162 | 213,997,119 | 14,450,404,119 | 8,598,473,855 | 11,018,433,554 | 34,947,812,491 | 5,792,591,565 | 3,710,883,135 | 100,000,000,000 |
| Bengali | 20,063,342,514 | 32,304,488 | 10,821,516,763 | 1,861,152,984 | 9,477,011,253 | 15,250,573,737 | 5,599,141,473 | 3,561,623,454 | 66,666,666,666 |
| Tamil | 20,598,403,258 | 14,567,775 | 3,958,241,564 | 1,179,759,699 | 5,447,566,137 | 26,425,095,607 | 5,485,027,435 | 3,558,005,192 | 66,666,666,667 |
| Telugu | 21,339,943,784 | 43,769,009 | 1,761,216,142 | 1,886,816,677 | 4,698,361,415 | 27,244,736,215 | 5,864,830,338 | 3,826,993,087 | 66,666,666,667 |
| Kannada | 19,242,977,088 | 2,238,695 | 1,571,429,244 | 2,245,371,670 | 2,341,566,193 | 32,387,351,380 | 5,317,795,029 | 3,557,937,368 | 66,666,666,667 |
| Marathi | 19,412,121,908 | 3,069,278 | 2,592,434,223 | 1,515,965,336 | 3,593,008,562 | 30,460,713,089 | 5,459,456,470 | 3,629,897,801 | 66,666,666,667 |
| Gujarati | 20,426,872,461 | 1,458,353 | 1,599,092,787 | 1,794,591,509 | 3,320,109,527 | 29,983,374,541 | 5,839,612,582 | 3,701,554,906 | 66,666,666,666 |
| **Sum** | **142,351,065,175** | **311,404,717** | **36,754,334,842** | **19,082,131,730** | **39,896,056,641** | **196,699,657,060** | **39,358,454,892** | **25,546,894,943** | **500,000,000,000** |

Phase totals per language (Hindi 5,417,103,550 / 85,215,326,818 / 9,367,569,632; full table in the Indic doc). Segment phase rules: Specialized 3/82/15 per subsegment, FW2 10/80/10, Sangraha 10/70/20, IndicCorp 0/100/0, v2 HQ 5/93/2, v2.1 HQ 8/80/12, DQA 0/70/30, plus the Gujarati move that lands phases exactly on 25/425/50B. Indic decay: 42.7% Specialized, 16.0% Sangraha, 15.3% DQA, 18.6% translated HQ, 7.4% FW2-native. The specialized per-subsegment token census (all 18 rows, native + Latin, exact) is done and matches the 142,351,065,175 total to the token.

## Packing and serving rules

- One sequence = one language + one source-subsegment. Documents joined by single `<eod>` (id 4); tail `<pad>` (id 3), masked. Phases are sealed document sets assigned before step 0 by blake2b-64 hash of doc id; a batch never mixes phases.
- **Intra-document attention masking is required**: block-diagonal attention and position reset at every `<eod>`, built from the per-sequence document spans in the shard jsonl. A trainer that attends across documents is not running this spec.
- Val: Indic carve (FineWeb-2 10,300,598, IndicCorp 1,155,338, Sangraha 9,701,494) packed as own masked sequences; English rows' `.val` parts stay out of train shards. No CC-side val carve exists — carve before packing if a CC eval is wanted.
- One pass everywhere; the unused pools stay parked (Indic ~514B: DQA 183.9, v2 MHQ 134.1, HQ-Synth 52.9, MHQ-Synth 32.7, v2-HQ leftover 101.2; English ClimbMix leftover ~135B, Code-v1 427.9B, CodeAlchemy dialogue/qa ~22B).
- Tokenizer: frozen 65,536 BPE (`docs/hf-tokenizer`, sha256 `bd790ad3…6b7`) — the only encoder that wrote or writes bins. Decoder gaps to patch in PT-1 serving: `राम\nश्याम` (leftover `Ċ`), `C++में` (spurious space).

## Scoreboard (mid-training and final)

Steer on downstream probes in both languages, never on holdout perplexity alone. English: SmolLM3 suite (HellaSwag, ARC, BoolQ, Winogrande, CSQA, PIQA, OBQA, MMLU-CF, GSM8K). Code: HumanEval+/MBPP+ (EvalPlus harness), CRUXEval-O (style-insensitive canary), MultiPL-E py/java/cpp/js, LiveCodeBench date-windowed with the HumanEval↔LCB delta as the overfitting diagnostic; never checkpoint-select on MBPP alone (rewrite-style naming trap). Indic: MILU, IndicGenBench (native splits), Global-MMLU-Indic, INCLUDE, Belebele/FLORES, plus generation-side human eval on native sources. Indic code: HumanEval/MBPP-Indic via the AI4Bharat eval-suite pipeline (all seven languages, byte-identical harness), MGSM-bn/te anchors, and a novel Hinglish-docstring variant. Contamination note: no decontamination scan by policy; LCB window date published, post-hoc n-gram audit of code rows to quantify exposure.

## Data status

- **Tokenized, counted, verified**: every Indic row (~1,014B + 101.4B CC-Latin); ClimbMix 380.2B full pool; Math 4+ 61.4B; Code v2 five splits 55,179,314,443 (census replaces the 55.2B cap); CodeAlchemy 48.8B stored slice; Genesis 43.0B; InfiniByte 22.6B; Specialized v1.1 11.1B; Fact-Seeking 9.6B; Code v2 Rewriting 53,330,180,217 (the 40B row draws from this); UltraData-Code L3 19,839,435,918 + ~5.6B cpp top-up in flight (row is 25.4B); Personas-India 4,292,637,514 (3,000,000 cards: en_IN 1,008,311,948, hi_Latn 2,129,938,846, hi_Deva 1,154,386,720).
- **Pending**: RQA top-up — 9.38B of the 14.4B row tokenized; the remaining ~5B must be a disjoint selection from the same 175 files (exclusion set reconstructable from the dual-v1 index `row_key`s). hi_Deva/hi_Latn Personas splits sit on the English side per the mix note; revisit if their placement should be Indic-side.
- **Dropped**: Code-v1 (0 of 32B drawn, never downloaded), CodeAlchemy code-dialogue/code-qa/code-trace, finepdfs-edu, HQ-Synthetic (both CC and CC-Code), MIND, Genesis failure-analysis, all medium-quality slices, second epochs.

## Ratified decisions

1:1 halves (2026-11-01). Hindi 100B (11-02). FineWeb-2 Latin census replaces the unmeasured budget (11-02). Decay window fixed at 100B in all total cases (11-04). English decay to 40% web (11-03). QAT fixed at 200B = 2× decay, one schedule, QAT inherits it (11-04). Code v2 census and ClimbMix funding the 20,685,557 cap difference (11-04). Code-v1 dropped; Rewriting is the code backbone (11-05). UltraData-Code L3 as the decay spine (11-05). Four-language code pruning: py, C++, Java, JS (11-05). Personas-India counted and kept on the English side (11-06). No global dedup, no benchmark decontamination (preferences). Specialized per-subsegment census (11-03). Intra-document masking mandated in packing (11-03).
