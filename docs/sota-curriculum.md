---
cursor:
  subagentId: "bc-ca53ddae-28ab-54fd-b093-b7406c85be26"
---

# English pretraining curriculum, 1.5B dense

This is the English sheet for a 1.5B dense model trained from scratch. It spends **717B** tokens, which is 478 tokens per parameter. Indic is not in these 717B. The tokenizer is unchanged.

The 717B is the right-hand mix from the [mix note](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/curriculum-mix-recommendation.md), with two edits: Genesis III is 52B, and InfiniByte Reasoning is added at 19B. Math Textbooks and SwallowMath-v2 are not on this sheet. The [phase plan](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/curriculum-plan.md) and the [inventory curriculum](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/training-curriculum.md) still describe a 1.2B run. The [1 October samples](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/internal/curriculum-mix-samples.md) are what the rows look like on disk.

## What changed

The dataset budgets are unchanged. The phase lengths are unchanged: 36B warmup, 537B stable, 144B annealing. No dataset was added. The locked rows already supply web, source math, code, and long reasoning.

Annealing ClimbMix rose from 24B to 71B, which is 49.3% of the cooldown. The previous 24B was 16.7% of the phase, a sharp drop away from the stable web mix. Blakeney et al. (2024, [arXiv:2406.03476](https://arxiv.org/abs/2406.03476)) kept filtered web at 30% of the final phase so the distribution would not jump, and they removed only the noisier crawl. SmolLM2 keeps English web at 58% of its decay, and SmolLM3 keeps web at 63% (Allal et al., 2025, [arXiv:2502.02737](https://arxiv.org/abs/2502.02737); [SmolLM3](https://huggingface.co/blog/smollm3)). MiniCPM mixes the high-quality decay data into the pretraining data rather than replacing it (Hu et al., 2024, [arXiv:2404.06395](https://arxiv.org/abs/2404.06395)). The 71B are unseen ClimbMix documents, one pass, shuffled in the same phase as the upweighted rows. The share is under SmolLM2’s 58% because Specialized v1.1, all 9B, sits in this phase.

Math 4+, both code rows, and the high-quality rephrases are a larger share of annealing than of stable. Hard Math 4+ stays in annealing. Hard MIND stays in stable. Genesis, Fact-Seeking, and InfiniByte sit mostly in stable, so the cooldown is not a quiz.

Multiple-choice and rollout text is capped at 10% of each phase. The four formats are Genesis, RQA, Fact-Seeking, and the Specialized multiple-choice subset. A 1.7B model trained on Genesis option-level text alone emitted an option letter on 99.45% of MMLU-STEM items (QVAC Genesis III, [arXiv:2609.19513](https://arxiv.org/abs/2609.19513)). SmolLM2 kept its synthetic textbook slice at 4% of the decay. Ten percent is the ceiling on the main schedule, and the main schedule sits under it. The 15B branch goes over that ceiling, because the 20B moved onto RQA is one of the four formats. The HQ section records that breach.

No cross-source dedup, and no benchmark scan, before the band split. The files are used as released.

Left out, on purpose. The cooldown stays at 20% of tokens. Hägele et al. (2024, [arXiv:2405.18392](https://arxiv.org/abs/2405.18392)) saw further cooldown length stop helping at about 20% of steps, and Blakeney et al. saw their best aggregate at 20% of training. SmolLM2 and SmolLM3 decay over the last 10%. A 10% cooldown here would be 72B, and Specialized v1.1 already takes 9B of annealing, so web could not stay the largest source while math and code also rose. Hägele’s 1-sqrt decay and MiniCPM’s exponential decay are not used, because SmolLM2 and SmolLM3 shipped a linear decay to zero. There is no second stable stage. SmolLM3 uses one, and math and code are already inside this run’s single stable mix. A long-context extension and a reasoning mid-training stay out. SmolLM3 runs both after the main pretraining, and there is still no length histogram. The 15B high-quality pack stays at two epochs. Muennighoff et al. (2023, [arXiv:2305.16264](https://arxiv.org/abs/2305.16264)) saw repetition gains fade by about four epochs, and the Genesis 1.7B run got worse when a 27.5B synthetic set went from four epochs to seven.

| Dataset | Billions |
| --- | ---: |
| ClimbMix | 400 |
| Nemotron Math 4+ | 52 |
| Nemotron MIND | 35 |
| RQA | 10 |
| Fact-Seeking | 5 |
| Specialized v1.1 | 9 |
| CodeAlchemy | 40 |
| Nemotron Code v2 | 45 |
| Nemotron-CC v2.1 HQ Synth | 50 |
| Genesis III | 52 |
| InfiniByte Reasoning | 19 |
| **Sum** | **717** |

The three tables at the end are the schedule. They assume the high-quality synthetic row really has 50B unique tokens. If that row is the counted 15B pack, use the replacement in the HQ section. That replacement keeps the same phase totals. Do not add it on top of the 50B tables.

## How a document gets a band

The ratio is compressed size divided by original size, on one document. A low ratio is repetitive text. A high ratio is text the compressor could not shrink.

Use gzip, DEFLATE, level 6. Compress the UTF-8 bytes of the `text` field only. Set the gzip timestamp to 0 so the header does not depend on the clock. No shared dictionary. One document per call.

- Easy: ratio under 35%.
- Mid: 35% through 65%, including both ends.
- Hard: ratio over 65%.

```python
import gzip
raw = text.encode("utf-8")
ratio = len(gzip.compress(raw, compresslevel=6, mtime=0)) / len(raw)
```

Yin et al. (2024, [arXiv:2407.06645](https://arxiv.org/abs/2407.06645)) define the ratio the other way, original divided by compressed, and they use DEFLATE. Under their definition a lower number is denser text. The bands in this sheet are the reciprocal: compressed divided by original. Do not feed their number into these cuts. A different codec, including zstd, moves documents across 35% and 65%. Stay on gzip level 6.

Documents under 512 UTF-8 bytes are mid, whatever the ratio says. The gzip header is large next to a short quiz item. These cuts are compression bands: a curriculum heuristic from the gzip level-6 ratio, not a measure of semantic difficulty. This floor is a planning rule.

These cuts are not the quantile bands in the pretraining-curriculum paper (arXiv:2506.11300, EACL 2026). That paper found compression ratio one of the stronger difficulty signals, and found a curriculum most useful as a warmup before ordinary shuffling. This sheet uses the phase change as the order. Inside a phase, shuffle. Do not sort a phase from easy to hard. Do not sort the whole 717B from easy to hard.

A band that is short does not get invented tokens. Move the missing billions to mid for that same dataset and that same phase. If the dataset itself is short, the run shrinks. ClimbMix does not grow past 400B to fill a hole. A short band is not filled from Genesis, RQA, Fact-Seeking, or Specialized multiple choice. That fill would break the format cap below.

## What each dataset is for

**ClimbMix, 400B.** General web, one pass. NVIDIA built it from Nemotron-CC and smollm-corpus by clustering and a proxy mixture search (Diao et al., 2025, [arXiv:2504.13161](https://arxiv.org/abs/2504.13161)). The samples are ordinary web: a flu-shot notice, a biogeography page, compiler docs, homework-help spam. It is the largest source in warmup, in stable, and in annealing. It is the dataset that can actually fill all three compression bands. The crawl was not decontaminated (Nemotron-CC, [arXiv:2412.02595](https://arxiv.org/abs/2412.02595)). Do not take a second pass. The annealing slice is unseen documents from this same 400B, which is how the cooldown keeps the stable web mix.

**Nemotron Math 4+, 52B.** The math pages. Common Crawl documents scored 4 or 5 by a FineMath classifier, 52.32B published tokens (Mahabadi et al., 2025, [arXiv:2508.15096](https://arxiv.org/abs/2508.15096)). One epoch. The samples mix a careers page, a radians lesson, a worked perimeter problem, and a page that already reads like a textbook chapter. This is the math the model should see as source text. The publisher already MinHash-deduped at Jaccard 0.8 and dropped documents with cosine similarity above 0.9 to MMLU, MMLU-Pro, MATH, or GSM8K prompts or answers. That removal was under 0.002% of documents. Keep those drops. The hard band of these pages, 12B, is held for annealing.

**Nemotron MIND, 35B.** Dialogue written over those same 4+ pages. The public regeneration is about 73B tokens, so 35B is about half a pass. The samples are two-person talks that restate a geometry page, a Big-O page, or a series test. MIND is a second view of the math web, not a second math corpus. Hard MIND and hard Math 4+ are not stacked in the same phase. The rule is below. Most of MIND is in stable. Annealing keeps a small easy and mid slice so the cooldown still hears dialogue, and it does not hear a second hard math dose.

**RQA, 10B.** Long reasoning. Questions are built from chunks of topic-stratified STEM documents, then answered with a context-free rollout. Public size 134.6B. The samples run 11k to 40k characters and cover crypto, C++, real-time systems, RNA-seq, and chemistry, in the same long question shape. Ten billion is a small slice of that set. It is in every phase. The hard band is split between stable and annealing, 1.5B each, so the rollout shape is not saved up for the cooldown.

**Fact-Seeking, 5B.** Short factual questions from wiki articles, often several items about one article. Published size is about 35.0B. The samples are 101 to 481 characters, many of them multiple choice. Five billion is a small dose on purpose. Every sampled document is under the 512-byte floor, so the whole row is mid. Do not repeat it, and do not relabel it hard. One billion of the five sits in annealing. The rest is earlier, where ClimbMix dilutes it.

**Specialized v1.1, 9B.** One pass, and only in annealing. The release is about 9.30B tokens. Most of the bytes are synthetic Python problems (Code-Concepts). The rest is benchmark-shaped multiple choice: topics from MMLU `auxiliary_train`, plus small formal-logic, economics, and algorithmic files. The sheet includes that multiple choice once. It does not get a second pass. NVIDIA’s Super 3 notes say the Code-Concepts taxonomy is taken from HumanEval. The file is used as released. This run does not scan it for test items.

Draw the 9B in proportion to stored bytes (32.49 GiB in the 27 September inventory):

| Subset | Billions |
| --- | ---: |
| Code-Concepts | 8.28 |
| Multiple-Choice | 0.63 |
| Unconditional-Algorithmic | 0.05 |
| Formal-Logic | 0.02 |
| Economics | 0.02 |
| **Sum** | **9.00** |

The hard cell in the band table is allowed to come only from Code-Concepts documents over 65%. The multiple-choice, economics, and formal-logic subsets stay mid. If Code-Concepts compresses under 65%, that hard cell moves to mid. Do not repeat multiple choice to fill it. The 0.63B multiple-choice subset counts toward the format cap.

**CodeAlchemy, 40B.** Synthetic code. The public release rewrites code into enhanced code, question-answer, development traces, dialogue, and execution traces, on the order of 977B tokens by a character estimate (IBM, [arXiv:2606.10087](https://arxiv.org/abs/2606.10087)). The sheet’s 40B is a slice. No bucket prefix was in the 1 October sample, and there is no excerpt. The 40B stays. Treat the band cells as a request to the sampler, not as a measurement.

**Nemotron Code v2, 45B.** The other code row. The public increment is metadata for GitHub files plus synthetic question answering, review, student-teacher dialogue, rewriting, and Python-to-C++ transpilation. The card is gated, and the 1 October sample found no prefix. The 45B stays, with the same caveat. Forty plus forty-five is 85B of code, about 12% of the run. Annealing takes 22B of that 85B, which is 15.3% of the cooldown, above the 11.2% code share of stable.

**Nemotron-CC v2.1 HQ synth, 50B in the main tables.** Rephrases of high-quality web pages. The public v2.1 high-quality synthetic set is 93.5B tokens, so 50B is about half a pass and the band split is real unique text. The only counted English pack in the inventory is a different object: Nemotron-CC-v2, config High-Quality-Synthetic, 15,000,000,001 train tokens on the TinyLlama tokenizer. The 1 October decodes of that pack are rephrased articles, and one window still contains the rewriter’s instruction. If the training data is that 15B pack, do not use the 50B band row. Use the replacement below.

**Genesis III, 52B.** Synthetic STEM, option-level text only. QwQ writes a four-option question from a FineFineWeb seed, a small model answers, and a correct answer is rewritten as a textbook section, a web article, a question-answer, or a dialogue. Published option-level is 108.67B tokens. Fifty-two billion is about half of that split. It is not the 109B full option-level split, and it is not the 82.76B failure-analysis split. The 1 October sample did not find Genesis in the bucket. The public preview files mix both pipelines in the same parquet. Prefer rows whose pipeline is option-level.

If the files cannot be separated, drop failure analysis and drop any file that does not show which pipeline it is. Failure analysis is the text that quotes a wrong student answer. Do not train a mixed file in order to reach 52B. Do not repeat option-level documents, and do not fill the hole with ClimbMix. Cut the shortfall from annealing Genesis first, then stable, then warmup. If nothing can be shown to be option-level, Genesis is zero and the run is 665B.

Eight billion of the 52B is in annealing. The other 44B is in warmup and stable, where web is the majority, so the four-option shape stays under the format cap.

**InfiniByte Reasoning, 19B.** Cross-domain problems. NVIDIA’s card for [Nemotron-Pretraining-Specialized-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1) calls it Synthetic InfiniByte: code, math, physics, chemistry, and scientific text are combined into multi-step problems. The generators are QwQ-32B and Qwen3-235B-A22B-Thinking-2507. The card lists **19.4B** tokens. The public viewer shows about 1.48M rows, each a long question that starts in one domain and continues in another. Nineteen billion is one pass of that release. Leave the other 0.4B out, by a hash of the document id, before the phase split.

The 27 September inventory measured `datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-InfiniByte-Reasoning/` at 28,345,959,943 bytes (26.40 GiB, 30 objects). That measurement is not a token count. If the census is under 19B, train one epoch of what is stored. These documents are long and specific, so the easy band may be thin. A missing easy or hard cell moves to mid. Do not repeat the set to fill a band. Most of the row is in stable (16.7B). Annealing keeps 1.5B. InfiniByte is outside the format cap. It is not a four-option item and it is not an RQA rollout. It is still shuffled with ClimbMix, so it does not become the style of the cooldown.

## Why three phases

The learning-rate schedule is warmup, then a constant peak, then a cooldown to zero. Hu et al. (2024, [arXiv:2404.06395](https://arxiv.org/abs/2404.06395)) call that warmup-stable-decay. Hägele et al. (2024, [arXiv:2405.18392](https://arxiv.org/abs/2405.18392)) found that a constant learning rate plus a cooldown matches a well-tuned cosine, and that lengthening the cooldown stops helping at about 20% of steps. On their long run, a shorter cooldown could match cosine. This run is 478 tokens per parameter, far shorter than SmolLM2’s 11T on a 1.7B model, so the cooldown stays at the 20% end of that plateau.

Current small models use that shape and change the mixture with it. The decay is a data-mix change, not only a learning-rate decay. SmolLM2, a 1.7B model, decays over the last 10% of tokens. That decay is 58% English web, 24% code, 14% math, and 4% Cosmopedia (Allal et al., 2025). Their math ablations annealed on 60B of the new set plus 40B of the pre-checkpoint mixture, so the new set was not the whole cooldown. SmolLM3 decays over the last 10% as well, about 1.1T of 11.1T, and raises math and code in steps while web stays the majority: web 85% then 75% then 63%, code 12% then 15% then 24%, math 3% then 10% then 13% ([SmolLM3](https://huggingface.co/blog/smollm3)). Their learning-rate warmup is 2,000 steps, not a separate data phase. Blakeney et al. (2024) upsampled domain data and cut the large crawl for the last 10% to 20% of a 7B run. That range was the useful one. Past 20%, math and code kept rising and the aggregate started to give way. In the final phase they still kept small-scale Common Crawl at 30%.

MiniCPM’s decay stage is a mixture of the pretraining data and the high-quality data (Hu et al., 2024). Their small-scale checks found a decay of about 10% of tokens enough to match cosine. The shipped SmolLM schedules are also 10%, and they can afford that because web is still about 60% of a three-way mix. This sheet has Specialized v1.1 locked to annealing. Nine billion inside a 72B cooldown would be 12.5% of the phase before math or code moved. The cooldown therefore stays 144B, 20.08% of 717B, the top of the range where both Hägele and Blakeney still saw a gain, and the mix inside it keeps ClimbMix as the largest source.

There is no fourth phase. SmolLM3’s long-context extension and reasoning mid-training come after the main run. This sheet does not add them. The inventory has no length histogram for these sources.

The learning-rate warmup is the first 4B tokens, inside the 36B data warmup. That is 2,000 steps at about 2M tokens per step, the same step count SmolLM uses and the same batch scale as the 1.2B plan. The other 32B of data warmup are already at the peak learning rate, on the easy mix. The peak stays constant through the rest of warmup and all of stable. It decays linearly to zero across the 144B. It does not warm back up. The peak value is not chosen here.

## Phase budgets

| Phase | Billions | Share of 717 |
| --- | ---: | ---: |
| Warmup | 36 | 5.02% |
| Stable | 537 | 74.90% |
| Annealing | 144 | 20.08% |
| **Sum** | **717** | **100%** |

Warmup is the easy phase. Its hard column is zero on every dataset. Stable is the long constant-learning-rate phase. ClimbMix is 56.4% of it. The hard column is 75B, 14.0% of the phase, and it is shuffled with the easy and mid documents. Annealing is the cooldown. ClimbMix is 71B, 49.3% of the phase, still the largest source. Math 4+ rises from 6.7% of stable to 9.7% of annealing. The two code rows together rise from 11.2% to 15.3%. HQ synth rises from 6.9% to 8.3%. The hard column is 55B, 38.2% of the phase, shuffled with 20.8B easy and 68.2B mid. That higher hard share is a mix difference. It is not an order.

Code, math, and reasoning are in all three phases. Hard Math 4+ is 12B, all in annealing. Hard MIND is 8B, all in stable. RQA hard is 1.5B in stable and 1.5B in annealing. InfiniByte hard is 2.5B in stable and 0.5B in annealing.

ClimbMix goes the other way from the upweighted rows: 17.8% of its tokens are in annealing, against 20% of the run. Genesis, MIND, Fact-Seeking, and InfiniByte also put less than 20% of their own tokens in annealing. That is the format cap and the hard-MIND rule, not a missing upweight. Math 4+, both code rows, HQ synth, and RQA each put more than 20% of their own tokens in annealing. Specialized v1.1 puts all of its tokens there.

Assign documents before training, after the holdouts. Band the documents that remain. Inside one band of one dataset, hash the document id into phases in the proportions in the third table. A document is in one phase. Shuffle inside the phase.

## Format cap

Genesis, RQA, Fact-Seeking, and Specialized multiple choice are one family of shapes: a question, often with options, often with a written answer. Count them together. In any phase their sum is at most 10% of that phase. On the full run the cap is the same 10%.

The schedule, in billions:

| Phase | Genesis | RQA | Fact-Seeking | Specialized MC | Sum | Share of phase |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Warmup | 1.5 | 0.5 | 0.2 | 0 | 2.2 | 6.1% of 36 |
| Stable | 42.5 | 7 | 3.8 | 0 | 53.3 | 9.9% of 537 |
| Annealing | 8 | 2.5 | 1 | 0.63 | 12.13 | 8.4% of 144 |
| **Run** | **52** | **10** | **5** | **0.63** | **67.63** | **9.4% of 717** |

Specialized multiple choice is 0.63B of the 9B row. The other Specialized subsets are code and short formal text. They do not count toward this cap. InfiniByte does not count toward this cap.

If a band is short, or a Genesis file is dropped, do not refill from these four. The cap is a maximum. The schedule is already under it, and stable is close to it, so there is no spare room in stable.

## MIND and Math 4+

MIND restates Math 4+ pages. Both prefixes carry WARC ids.

No phase contains both a hard Math 4+ draw and a hard MIND draw. Warmup has neither. Stable has 8B of hard MIND and no hard Math 4+. Annealing has 12B of hard Math 4+ and no hard MIND. Annealing MIND is 0.5B easy and 2.5B mid: a small dialogue dose during the cooldown, not a second hard math dose.

When the WARC id matches, a page and its dialogue do not both train as hard anywhere in the run. Keep the page in the hard Math 4+ draw. Train the dialogue in the mid MIND cell of the phase it was assigned to. The tokens do not disappear. The hard MIND cell shrinks by the same number, and the mid MIND cell grows. If the join cannot be done, keep the phase split above and do not also drop hard MIND.

A MIND document that is a near-copy of the page, rather than a dialogue about it, is handled in the dedup section. It drops. The page stays.

## Cross-source dedup

Math 4+, MIND, ClimbMix, and HQ synth can share pages. Math 4+ is scored Common Crawl. ClimbMix is drawn from Nemotron-CC and smollm-corpus, and Nemotron-CC is Common Crawl. MIND is generated from the 4+ pages. HQ synth is a rephrase of high-quality Nemotron-CC pages. Run this before banding.

Use MinHash on 5-grams of the normalized text, the same family of near-duplicate filter StarCoder used on code and Nemotron-CC-Math used on these math pages (Li et al., 2023, [arXiv:2305.06161](https://arxiv.org/abs/2305.06161); Mahabadi et al., 2025). The threshold for these four text sources is Jaccard 0.8, the Nemotron-CC-Math setting. StarCoder’s code threshold is 0.7. That lower cut stays on the code rows, below. It is not applied to web pages.

On a hit, keep one copy:

- Math 4+ wins over ClimbMix. The scored math page stays, and the ClimbMix copy drops.
- Math 4+ wins over an HQ document at Jaccard 0.8 or above. That HQ document is the page again, not a rephrase.
- ClimbMix wins over an HQ document at Jaccard 0.8 or above, for the same reason.
- An HQ document below 0.8 against the page it rephrases stays. The rephrase is the point of the row.
- A MIND document at Jaccard 0.8 or above against its Math 4+ page drops. The page is already in the run. A dialogue that only discusses the page, and lands below 0.8, stays.

Also drop an exact hash match after light normalization (case and whitespace). The same priority order applies.

The two code rows, once a prefix exists, get StarCoder’s setting inside each row and across the pair: 5-gram MinHash, drop at Jaccard 0.7. Until a prefix exists, that rule is waiting on the files. The budgets stay, and the rows stay flagged.

Dropped tokens are not refilled. ClimbMix does not grow. The format-cap rows do not grow. The run shrinks by the drops. The 20B move onto RQA, in the HQ section, is only for the case where the high-quality row is the 15B pack. It is not a refill for dedup.

## Benchmarks

This run does not scan the files for benchmark text. The sources are published datasets, used as released. There is no GSM8K, MATH, MMLU, MMLU-Pro, HumanEval, MBPP, or DS-1000 filter, and no second pass that looks for a test item inside a document.

## Holdouts

Carve these before the band split. Never train on them.

- The existing high-quality-synthetic validation bin of 50,000,001 tokens.
- The 0.4B InfiniByte remainder.
- 50 million tokens from ClimbMix.
- 5 million tokens from Nemotron Math 4+.
- 5 million tokens from whichever code source is tokenized first.

The 1.2B phase plan also holds out math textbooks. That row is not on this sheet. There is no textbook holdout here.

## High-quality synthetic, if unique tokens are 15B

The main tables use 50B unique. Use them only when the training tokenizer sees at least 50B unique tokens at two epochs or fewer. That is the public v2.1 high-quality synthetic set, 93.5B.

If the row is the counted 15B pack, the easy, mid, and hard cells in the main table are repeats of the same documents, not three piles of text. Cap the row at two epochs, 30B. Do not take a third pass. Muennighoff et al. (2023) is not a reason to take four epochs of this pack. The pack is 15B and synthetic, and the Genesis 1.7B run scored worse when a 27.5B synthetic set went from four epochs to seven.

The first epoch, 15B, is the unique text. Split it with gzip. Warmup takes 0.5B from the easy band of that epoch. Stable takes the other 14.5B, in whatever bands remain. Annealing takes the second epoch, the same 15B again, while the learning rate is decaying. The annealing band counts equal the unique band counts of that 15B. The second pass is the same documents. It is not a new hard pile.

The main annealing cell for this row is 12B. The second epoch is 15B. Move 3B of annealing ClimbMix into stable ClimbMix so the repeat fits in the cooldown. Annealing ClimbMix is then 68B, 47.2% of the phase, still the largest source. The 3B move is ClimbMix only. Every other dataset keeps its main-table phase except RQA, which receives the 20B.

The sheet’s 50B minus this 30B is 20B. Put those 20B on RQA. RQA is in the bucket (171.88 GiB) and the public set is 134.6B, so 30B of RQA is still under one epoch. ClimbMix stays at 400B.

| Dataset | Warmup | Stable | Annealing | Sum |
| --- | ---: | ---: | ---: | ---: |
| ClimbMix | 26 | 306 | 68 | 400 |
| Nemotron Math 4+ | 2 | 36 | 14 | 52 |
| Nemotron MIND | 1 | 31 | 3 | 35 |
| RQA | 1.0 | 26.5 | 2.5 | 30 |
| Fact-Seeking | 0.2 | 3.8 | 1 | 5 |
| Specialized v1.1 | 0 | 0 | 9 | 9 |
| CodeAlchemy | 1.5 | 28.5 | 10 | 40 |
| Nemotron Code v2 | 1.5 | 31.5 | 12 | 45 |
| HQ synth, two epochs of the 15B pack | 0.5 | 14.5 | 15 | 30 |
| Genesis III | 1.5 | 42.5 | 8 | 52 |
| InfiniByte Reasoning | 0.8 | 16.7 | 1.5 | 19 |
| **Sum** | **36** | **537** | **144** | **717** |

Warmup loses 0.5B of HQ and gains 0.5B of RQA. Stable loses 22.5B of HQ, gains 3B of ClimbMix, and gains 19.5B of RQA. Annealing gains 3B of HQ and loses 3B of ClimbMix. The phase totals stay 36, 537, and 144.

On this branch the four formats sum to 2.7B of warmup (7.5%), 72.8B of stable (13.6%), and 12.13B of annealing (8.4%). The run sum is 87.63B, 12.2% of 717B. Stable is over the 10% ceiling because the 20B taken off the high-quality pack lands on RQA, and RQA is one of the four formats. Once that 20B is added, the run itself is at 12.2%, so a 10% ceiling on every phase cannot close. The extra RQA stays in stable, next to 306B of ClimbMix. Annealing stays at 8.4%, so the cooldown does not become the quiz. Leave the extra on RQA. Do not move it onto Genesis or Fact-Seeking, and do not cut ClimbMix to hide the 13.6%.

RQA bands in this branch, in billions. The extra documents follow the same early-easy, late-hard split, and they sit in stable with the rest of that phase’s shuffle. Annealing RQA is unchanged. If RQA has too little easy text, the easy cell moves to mid in that phase.

| Phase | Easy | Mid | Hard | Sum |
| --- | ---: | ---: | ---: | ---: |
| Warmup | 0.6 | 0.4 | 0 | 1.0 |
| Stable | 4.0 | 16.0 | 6.5 | 26.5 |
| Annealing | 0.2 | 0.8 | 1.5 | 2.5 |
| **Sum** | **4.8** | **17.2** | **8.0** | **30** |

HQ bands in this branch, tokens seen. The unique 15B is planned at the main row’s band mix, 23.4% easy, 56.6% mid, 20% hard, which is 3.5 / 8.5 / 3.0. Warmup takes 0.5 easy. Stable takes the other 14.5 of the first epoch. Annealing repeats the full unique mix. Measure the pack and replace these cells. A short cell moves to mid. The annealing hard cell is the second view of the same hard documents.

| Phase | Easy | Mid | Hard | Sum |
| --- | ---: | ---: | ---: | ---: |
| Warmup | 0.5 | 0 | 0 | 0.5 |
| Stable | 3.0 | 8.5 | 3.0 | 14.5 |
| Annealing | 3.5 | 8.5 | 3.0 | 15 |
| **Sum** | **7.0** | **17.0** | **6.0** | **30** |

ClimbMix bands in this branch. The 3B move is mid text, from annealing to stable.

| Phase | Easy | Mid | Hard | Sum |
| --- | ---: | ---: | ---: | ---: |
| Warmup | 18 | 8 | 0 | 26 |
| Stable | 100 | 163 | 43 | 306 |
| Annealing | 15 | 33 | 20 | 68 |
| **Sum** | **133** | **204** | **63** | **400** |

The branch band totals, after those three row edits and with every other band cell taken from Table 3, are:

| Phase | Easy | Mid | Hard | Sum |
| --- | ---: | ---: | ---: | ---: |
| Warmup | 24.9 | 11.1 | 0 | 36 |
| Stable | 159.0 | 300.0 | 78.0 | 537 |
| Annealing | 23.3 | 67.7 | 53.0 | 144 |
| **Sum** | **207.2** | **378.8** | **131.0** | **717** |

If the RQA census cannot supply 30B, train one epoch of RQA and let the run shrink by the rest. Do not open a third HQ epoch.

## Code rows with no prefix

CodeAlchemy 40B and Nemotron Code v2 45B had no bucket prefix in the 1 October sample. The budgets stay. The band cells are unmeasured.

Code often compresses well, so the hard cells (ratio over 65%) may not exist. If a hard cell is short, move it to mid for that dataset and phase. The later phase still receives the code. It just does not receive a hard label the files do not support. If either row is smaller than its budget, train one epoch, scale that row’s three phase amounts by the same factor, and recompute bands on the files that exist. Do not repeat the row, and do not give the unused billions to ClimbMix.

## Other band fallbacks

These are the rows most likely to miss a cell. The fallback is the same: move the missing billions to mid inside the dataset and the phase, and do not invent documents.

- **Fact-Seeking.** Already applied. Easy and hard are zero. All 5B is mid.
- **InfiniByte.** Long composite questions. The 3.7B easy target may be high. Shortfall goes to mid.
- **RQA.** Same pattern. The 2.0B easy target in the main table may be high. In the 15B branch the easy target is 4.8B, and the same fallback applies.
- **Genesis.** Uniform generated style may land in one band. Shortfall goes to mid of option-level text. It does not go to failure analysis, and it does not go to another phase if that phase would cross the format cap.
- **Specialized v1.1.** The 2.0B hard target has to come from Code-Concepts. Otherwise it is mid. The multiple-choice subset is not repeated.
- **Math 4+.** One epoch, so the bands are a partition. If hard pages are under 12B, annealing hard shrinks and annealing mid grows.
- **ClimbMix.** This is the row that should fill all three bands. If it does not, the same mid fallback applies. It is not repeated.
- **HQ synth, 50B case.** If hard pages are under 10B, the shortfall moves to mid inside the phase that asked for it. In the 15B branch, use the branch band table instead of this 10B figure.

## Table 1. Phase totals

| Phase | Billions |
| --- | ---: |
| Warmup | 36 |
| Stable | 537 |
| Annealing | 144 |
| **Sum** | **717** |

The 15B branch uses these same phase totals.

## Table 2. Dataset by phase

Billions. Each row sums to the dataset budget. Each column sums to the phase budget. This is the 50B-unique HQ case.

| Dataset | Warmup | Stable | Annealing | Sum |
| --- | ---: | ---: | ---: | ---: |
| ClimbMix | 26 | 303 | 71 | 400 |
| Nemotron Math 4+ | 2 | 36 | 14 | 52 |
| Nemotron MIND | 1 | 31 | 3 | 35 |
| RQA | 0.5 | 7 | 2.5 | 10 |
| Fact-Seeking | 0.2 | 3.8 | 1 | 5 |
| Specialized v1.1 | 0 | 0 | 9 | 9 |
| CodeAlchemy | 1.5 | 28.5 | 10 | 40 |
| Nemotron Code v2 | 1.5 | 31.5 | 12 | 45 |
| HQ synth | 1 | 37 | 12 | 50 |
| Genesis III | 1.5 | 42.5 | 8 | 52 |
| InfiniByte Reasoning | 0.8 | 16.7 | 1.5 | 19 |
| **Sum** | **36** | **537** | **144** | **717** |

Share of the phase, from this table. Warmup is 72.2% ClimbMix. Stable is 56.4% ClimbMix. Annealing is 49.3% ClimbMix, 9.7% Math 4+, 15.3% code (CodeAlchemy plus Nemotron Code v2), 8.3% HQ synth, 6.3% Specialized v1.1, and 5.6% Genesis.

## Table 3. Easy, mid, and hard by phase

Billions. Gzip level 6, compressed size over original size. Easy is under 35%, mid is 35% to 65% including the ends, hard is over 65%. Warmup hard is zero. A row’s twelve band cells sum to the dataset budget. The bottom row sums to the phase budgets.

| Dataset | W easy | W mid | W hard | S easy | S mid | S hard | A easy | A mid | A hard | Easy | Mid | Hard | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ClimbMix | 18 | 8 | 0 | 100 | 160 | 43 | 15 | 36 | 20 | 133 | 204 | 63 | 400 |
| Nemotron Math 4+ | 1.6 | 0.4 | 0 | 12 | 24 | 0 | 0.5 | 1.5 | 12 | 14.1 | 25.9 | 12 | 52 |
| Nemotron MIND | 0.7 | 0.3 | 0 | 8 | 15 | 8 | 0.5 | 2.5 | 0 | 9.2 | 17.8 | 8 | 35 |
| RQA | 0.3 | 0.2 | 0 | 1.5 | 4 | 1.5 | 0.2 | 0.8 | 1.5 | 2.0 | 5.0 | 3.0 | 10 |
| Fact-Seeking | 0 | 0.2 | 0 | 0 | 3.8 | 0 | 0 | 1 | 0 | 0 | 5 | 0 | 5 |
| Specialized v1.1 | 0 | 0 | 0 | 0 | 0 | 0 | 0.4 | 6.6 | 2 | 0.4 | 6.6 | 2 | 9 |
| CodeAlchemy | 1.0 | 0.5 | 0 | 8 | 16.5 | 4 | 1 | 4 | 5 | 10 | 21 | 9 | 40 |
| Nemotron Code v2 | 1.0 | 0.5 | 0 | 9 | 18 | 4.5 | 1 | 5 | 6 | 11 | 23.5 | 10.5 | 45 |
| HQ synth | 0.7 | 0.3 | 0 | 10 | 22 | 5 | 1 | 6 | 5 | 11.7 | 28.3 | 10 | 50 |
| Genesis III | 1.0 | 0.5 | 0 | 12 | 24 | 6.5 | 1 | 4 | 3 | 14 | 28.5 | 9.5 | 52 |
| InfiniByte Reasoning | 0.5 | 0.3 | 0 | 3 | 11.2 | 2.5 | 0.2 | 0.8 | 0.5 | 3.7 | 12.3 | 3.0 | 19 |
| **Sum** | **24.8** | **11.2** | **0** | **163.5** | **298.5** | **75** | **20.8** | **68.2** | **55** | **209.1** | **377.9** | **130** | **717** |

Warmup is 24.8B easy and 11.2B mid. Stable is 163.5B easy, 298.5B mid, and 75B hard. Annealing is 20.8B easy, 68.2B mid, and 55B hard. Those three pairs are the phase budgets 36, 537, and 144.

Hard Math 4+ is only in annealing. Hard MIND is only in stable. Specialized v1.1 is only in annealing. Fact-Seeking is mid in every phase. CodeAlchemy and Nemotron Code v2 hard cells are the unverified ones. HQ synth hard cells are real only in the 50B-unique case. The 15B branch replaces the ClimbMix, RQA, and HQ rows with the band tables in the HQ section, and its phase band totals are the 24.9 / 11.1 / 0, 159.0 / 300.0 / 78.0, and 23.3 / 67.7 / 53.0 rows printed there.
