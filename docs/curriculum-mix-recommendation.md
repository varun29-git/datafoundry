---
cursor:
  subagentId: "bc-7cdf97f4-9b0a-5527-8ba6-df44b7b7b7f2"
---

# English mix for a 1.5B model: left, right, or a small edit

Use a small edit of the left mix. Keep the math textbooks, SwallowMath-v2, the larger RQA allocation, and the larger Fact-Seeking allocation. Add about 50B tokens from the QVAC Genesis III option-level split. Do not train the right mix’s 109B of Genesis, and do not drop those four rows to pay for it.

This note is the English sheet only. It does not change the Indic share, the phase gates, or the tokenizer. Those stay in [English-Indic curriculum](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/curriculum-plan.md) and [Training curriculum](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/training-curriculum.md). The programming-code rows are the same on both sides. This is not a CodeAlchemy versus Nemotron Code choice.

The model in this note is 1.5B dense, from scratch. Five hundred tokens per parameter is 750B tokens. The right mix is 755B, about 503 tokens per parameter of English. The left mix is 701B, about 467. The 54B gap is real. It is also smaller than the difference in what those tokens are.

The written curriculum still describes a 1.2B model and a 710B English sheet. That 710B includes a 9B Finemath-4plus row that neither mix here has. Its printed 755B also counted a 45B crop with no source. Neither mix revives that crop. Finemath-4plus is about 9.6B tokens, and Nemotron-CC-Math-4+ was built as the larger successor of that band, so leaving Finemath out of both mixes is reasonable. Do not put it back to fill the gap.

## The two sheets

Left, actual sum 701B. A 755 label on this sheet is wrong.

| Row | Billions |
| --- | ---: |
| ClimbMix 400B | 400 |
| Nemotron Math 4+ | 52 |
| Nemotron MIND 72B | 35 |
| Math Textbooks 25B | 10 |
| SwallowMath-v2 32B | 15 |
| Nemotron-CC v2.1 HQ Synth | 50 |
| CodeAlchemy 55B | 40 |
| Nemotron Code v2 45B | 45 |
| RQA 40B | 30 |
| Fact-Seeking 35B | 15 |
| Specialized v1.1 9B | 9 |
| **Sum** | **701** |

Right, sum 755B.

| Row | Billions |
| --- | ---: |
| ClimbMix 400B | 400 |
| Nemotron Math 4+ | 52 |
| Nemotron MIND 72B | 35 |
| RQA 40B | 10 |
| Fact-Seeking 35B | 5 |
| Specialized v1.1 9B | 9 |
| CodeAlchemy 55B | 40 |
| Nemotron Code v2 45B | 45 |
| Nemotron-CC v2.1 HQ Synth | 50 |
| Genesis III | 109 |
| **Sum** | **755** |

Shared rows are 646B once the overlapping RQA 10B and Fact-Seeking 5B are counted once: ClimbMix 400, Math 4+ 52, MIND 35, HQ synth 50, CodeAlchemy 40, Nemotron Code v2 45, Specialized 9, RQA 10, Fact-Seeking 5.

The fork is Genesis III 109B against Math Textbooks 10 + SwallowMath-v2 15 + the extra RQA 20 + the extra Fact-Seeking 10. That opposing bundle is 55B. Left is 54B shorter because 109 − 55 = 54.

Names such as “72B” and “40B” are sheet labels. Published sizes below are the public corpora. The inventory sizes in the training-curriculum note are what was listed in the bucket on 27 September 2026. Where those three numbers disagree, the bucket census wins, and the last section says which rows that affects.

## What each named set is

### ClimbMix, 400B in both

NVIDIA’s Nemotron-ClimbMix is a 400B-token set released with CLIMB (Diao et al., 2025, [arXiv:2504.13161](https://arxiv.org/abs/2504.13161); [Hugging Face](https://huggingface.co/datasets/nvidia/Nemotron-ClimbMix)). It is built from Nemotron-CC and smollm-corpus. Documents are embedded, clustered with FAISS k-means into 1,000 clusters, pruned with fastText quality, educational, and advertisement scores, and merged by centroid distance into about 20 clusters. A proxy-model search then picks mixture weights, and the 400B set is drawn from that mixture. The companion ClimbLab release is the filtered pool, about 1.2T tokens.

The from-scratch comparison in the paper is against other pretraining sets at the same token budget. ClimbMix beat Nemotron-CC, SmolLM, DCLM-baseline, and FineWeb-Edu on that comparison. The often-quoted +2.0% over Llama-3.2-1B is a different run: continued training for 400B tokens on a 1B model that had already seen about 10T tokens of DCLM and TxT360. Do not treat that number as what a from-scratch 1.5B model gets from these 400B tokens.

License on the Hugging Face card is CC BY-NC 4.0. smollm-corpus includes Cosmopedia, so ClimbMix is not pure web. It already contains some synthetic textbook text. The released 400B is still the general mix, and one pass is the set’s design point. A second pass is the wrong way to add tokens. ClimbLab exists if more unique web is needed later.

Failure modes that matter here: the source Nemotron-CC paper says the crawl was not decontaminated ([arXiv:2412.02595](https://arxiv.org/abs/2412.02595)). ClimbMix inherits that. The mixture was searched for general reasoning, not for Indic and not for a 1.5B run that already adds separate math and code rows. No ClimbMix prefix was measured in the inventory.

### Nemotron Math 4+ and MIND, 52B and 35B in both

Nemotron-CC-Math (Mahabadi et al., 2025, [arXiv:2508.15096](https://arxiv.org/abs/2508.15096); [Hugging Face](https://huggingface.co/datasets/nvidia/Nemotron-CC-Math-v1)) is Common Crawl math from 98 snapshots, scored with a FineMath classifier. The 4+ split is scores 4 and 5: 52.32B tokens, 45.10M documents. The 3+ split is 133.26B. The paper says 4+ is 5.5× FineMath-4+ (6.70M documents, 9.60B tokens in their table). They MinHash-dedup at a Jaccard target of 0.8 and drop documents with cosine similarity above 0.9 to MMLU, MMLU-Pro, MATH, or GSM8K prompts or answers. That removal is under 0.002% of documents. The quality comparison is an annealing ablation on a mid-training Nemotron-T 8B checkpoint, not a from-scratch 1.5B run. Both mixes already take essentially one epoch of 4+. That is the right amount. Do not add the score-3 band, and do not add Finemath-4plus on top.

MIND is synthetic dialogue written over math web text. The original Nemotron-MIND card is about 138B tokens of dialogues from Nemotron-4-340B-Instruct over OpenWebMath, in seven styles ([Hugging Face](https://huggingface.co/datasets/nvidia/Nemotron-MIND)). The set that matches the bucket prefix `4plus_MIND` is the regeneration from Nemotron-CC-Math-4+: 73B tokens, 88.73M documents, also called Nemotron-MIND-v1 on the CC-Math card. The sheet label “72B” is that regeneration. Both mixes train 35B, about half an epoch.

On an 8B annealing comparison, the regenerated 73B set beat the older 126B OpenWebMath MIND on the card’s table (MATH-500 47.8 versus 33.4, GSM8K 84.5 versus 80.7). That is evidence for preferring 4plus_MIND over the older MIND, which both mixes already do. It is not evidence that a 1.5B model should see more than 35B of it. MIND restates the same 4+ documents. The 52B plus 35B is one pass of the pages and a half pass of dialogue about those pages, not 87B of independent math.

The inventory measured 57.92 GiB for `4plus/` and 84.13 GiB for `4plus_MIND/`. A single shard sample was about 3.3 KB and 3.1 KB of text per row. Those byte totals are not a token census. If the census comes in well under 52B or under 35B, stop at one epoch. Do not repeat either row to hit the sheet.

### Math Textbooks, 10B on the left only

`Nemotron-Pretraining-Math-Textbooks` is a subset of [Nemotron-Pretraining-Specialized-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1). NVIDIA’s card: 25.1B tokens, generated by Qwen3-30B-A3B and Qwen3-235B-A22B. Nemotron-CC-Math documents are classified by educational level, and undergraduate-and-higher pages are turned into textbook-style sections. The inventory lists this prefix at 28.72 GiB, with about 7.8 KB of text per row on the sampled shard. Ten billion is under one epoch if the published 25.1B is what is stored. The text is a rewrite of the same math-web family as the 4+ row, in a longer textbook shape. That is why 10B is useful and why taking all 25.1B on top of 52B of 4+ and 35B of MIND would pile a third view of similar pages onto a 1.5B model.

### SwallowMath-v2, 15B on the left only

[SwallowMath-v2](https://huggingface.co/datasets/tokyotech-llm/swallow-math-v2) is a 32B-token rewrite of FineMath-3+, Apache 2.0, from the Swallow project (Institute of Science Tokyo). Stage 1 cuts over-long pages. Stage 2 extracts math spans with Qwen3-32B. Stage 3 rewrites into two styles: textbook, 13,302,336 samples, 18.3B tokens; Q&A, 12,635,739 samples, 13.6B tokens. The v1 paper (Fujii et al., 2025, [arXiv:2505.02881](https://arxiv.org/abs/2505.02881)) is a different, smaller set: about 2.3B tokens rewritten from Finemath-4+, used in a 50B-token continual pretrain of Llama-3.1-8B, with reported gains of +12.4 on GSM8K and +7.6 on MATH against leaving the math slice as Finemath. v2 scales that recipe and changes the license. It was not a from-scratch 1.5B experiment.

FineMath-3+ is a lower band than Nemotron-CC-Math-4+, so Swallow is not a copy of the 52B row, but it is the same kind of web math, rewritten. Fifteen billion is about half of one epoch of the 32B release. The main failure mode is the rewriter inventing a wrong step. v1’s ablations say the rewrite is where the gain comes from, and also where a bad generation would enter. There is no Swallow prefix in the inventory.

### Nemotron-CC high-quality synthetic, 50B in both

Two different public sets use this name.

[Nemotron-CC-v2.1](https://huggingface.co/datasets/nvidia/Nemotron-CC-v2.1) High-Quality-Synthetic is 93.5B tokens. It is five-prompt rephrases, by Qwen3-30B-A3B, of the high-quality organic slice of v2.1. That organic slice is 26.0B tokens from three 2025 Common Crawl snapshots. So 93.5B synthetic tokens sit on 26B of web. Fifty billion is about half an epoch of the synthetic files and about two rephrases per organic token.

The counted pack in the training-curriculum note is not that release. It is `nvidia/Nemotron-CC-v2`, config `High-Quality-Synthetic`, tokenized with TinyLlama: 15,000,000,001 train tokens and 50,000,001 validation tokens. The written plan already caps that pack at two epochs, 30B on that tokenizer, and says not to manufacture the other 20B with a third pass. Nemotron-CC-v2’s Qwen3-30B-A3B synthetic total on the dataset card is 879.1B across synthetic subsets, not a measurement of this high-quality config alone.

Both candidate mixes still say 50B. If the bucket row is the 15B pack, that is 3.3 epochs. The Genesis 1.7B runs, below, got worse when Cosmopedia-v2 (about 27.5B unique tokens) was repeated from four epochs to seven. Repeating a 15B rephrase pack a third time is the same kind of mistake, at a smaller scale. The Nemotron-CC authors also say they did not decontaminate the crawl. Rephrases of that crawl keep whatever benchmark text the original pages had, in a new wording, which n-gram filters miss.

### CodeAlchemy and Nemotron Code v2, 40B and 45B in both

CodeAlchemy (IBM, [arXiv:2606.10087](https://arxiv.org/abs/2606.10087); [Hugging Face](https://huggingface.co/datasets/open-alchemy/code-alchemy)) rewrites public code into five synthetic forms: CodeEnhance 124.5B, CodeQA 31.3B, CodeDev 269.8B, CodeDialogue 544.7B, CodeTrace 6.3B. The card’s total is about 976.6B tokens, estimated as characters divided by four, across 15 languages and about 162M rows. CodeQA and CodeTrace are execution-checked. The other three are not. Their 3B experiments are continual pretraining, not a from-scratch 1.5B generalist. The sheet’s “55B” is not a published subset. Forty billion of a real 55B slice is under one epoch. Forty billion of the full 977B set is a small unique sample. Either way this row should not be repeated. There is no CodeAlchemy prefix in the inventory.

[Nemotron-Pretraining-Code-v2](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Code-v2) is an increment on Code-v1: metadata for 377M GitHub files missing from v1, cutoff 15 April 2025, about 340B tokens, plus synthetic question answering, code review, student–teacher dialogue, rewriting, and Python-to-C++ transpilation. The synthetic code is grounded in v1 and v2 source files. Rewrites use the SwallowCode SGCR and SCOR prompts plus an NVIDIA prompt. The card says v1 and v2 are meant to be used together, and much of the release is metadata rather than the raw files. The sheet’s “45B” is a slice, not the 340B increment. There is no Code v2 prefix in the inventory. Until a shard is opened, 45B might be source code, synthetic dialogue, or a mix.

Eighty-five billion code tokens is 12.1% of the left mix and 11.3% of the right mix, about 57 tokens per parameter either way. That is a normal code share for a small generalist. It is identical, so it does not decide the fork. Specialized v1.1 adds the same extra ~7.3B of synthetic Python on both sides. Count that as code-like if you want a stricter total: about 92B, still identical.

Shared code risks: token counts for CodeAlchemy are character estimates; synthetic dialogue can be narrow even when the seed repos are diverse; execution checks cover only some CodeAlchemy subsets; benchmark problems in public GitHub are a known leak into raw code, and a rewrite does not reliably remove them.

### RQA, 30B on the left and 10B on the right

`Nemotron-Pretraining-RQA` is in Specialized-v1. The card: 134.6B tokens, generated by Qwen3-235B-A22B-Thinking-2507 and gpt-oss-120b. Long-form STEM questions are built from contiguous chunks of topic-stratified STEM documents, then answered with context-free reasoning rollouts. The inventory prefix is 171.88 GiB, and the sampled shard is about 25.6 KB of text per row, so these are long documents. The sheet label “40B” is smaller than the public 134.6B. Thirty billion is 0.22 epoch of the public set, or 0.75 epoch if the bucket really only has 40B. Ten billion is 0.07 or 0.25 epoch on those same two readings. Neither allocation repeats the set. The left allocation is the one that gives the 1.5B model a real amount of long reasoning text.

### Fact-Seeking, 15B on the left and 5B on the right

`Nemotron-Pretraining-Fact-Seeking` is in [Specialized-v1.2](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1.2): 35,029.6M tokens, Qwen3-30B-A3B-Instruct-2507, CC-BY-4.0. The Nemotron 3 Ultra report ([arXiv:2606.15007](https://arxiv.org/html/2606.15007)) says questions are generated from FineWiki in two stages: pull a factual statement out of an article, then ask the model for a short answer or a multiple-choice question. On an intermediate Nemotron 3 Nano checkpoint, injecting this data over the last 100B tokens moved a multiple-choice rendering of SimpleQA from 40.24 to 50.16. The report says those scores are not the original SimpleQA metric. The ablation is continued training of a Nano model, not from-scratch training of a 1.5B model.

The inventory has 42.51 GiB, and a footer sample averaged about 264 text bytes per row. These are short documents. Fifteen billion of a 35B set is under one epoch. Five billion is also under one epoch, and it is a thin factual dose. Do not raise this row toward 35B to chase the Nano ablation. Short wiki questions are easy for a 1.5B model to memorize, and the evaluation NVIDIA reported was itself converted to multiple choice.

### Specialized v1.1, 9B in both

[Nemotron-Pretraining-Specialized-v1.1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1.1), published token counts:

| Subset | Tokens | What it is |
| --- | ---: | --- |
| Code-Concepts | 7.295B | Synthetic Python problems from a concept taxonomy. NVIDIA’s [Super 3 pretraining notes](https://docs.nvidia.com/nemotron/latest/nemotron/super3/pretrain.html) say the taxonomy is taken from HumanEval, about 15M problem–solution pairs. |
| Multiple-Choice | 1.609B | Multiple-choice questions on topics from MMLU `auxiliary_train`. Qwen3-235B writes questions, DeepSeek-V3 writes solutions. |
| Unconditional-Algorithmic | 0.195B | Short algorithmic text. |
| Formal-Logic | 0.128B | Logic items, with and without a written solution. |
| Economics | 0.073B | Economics multiple choice. |
| **Sum** | **9.30B** | |

The sheet’s 9B is one pass of this release, rounded. The inventory prefix is 32.49 GiB, of which Code-Concepts is 29.89 GiB. Drawing the 9B in proportion to bytes, as the written plan already says, puts about 92% of the row on Code-Concepts. The three subsets under 1 GiB stay under the existing epoch cap. Do not repeat the multiple-choice subset to make the row look larger. The HumanEval-taxonomy note and the MMLU `auxiliary_train` note are the leakage items. They are shared by both mixes. The later Ultra report’s statement that held-out test splits were not used as seeds applies to the v1.2 multiple-choice and generative sets, which are not this row.

### Genesis III, 109B on the right only

QVAC Genesis III (Tether / QVAC, COLM 2026; [arXiv:2609.19513](https://arxiv.org/html/2609.19513), [blog](https://huggingface.co/blog/qvac/genesis-iii), dataset `qvac/GenesisIII`) is a synthetic STEM corpus. It is not a web crawl.

Construction:

1. Seed passages come from FineFineWeb. Sampling continues until about 500,000 passages remain after the Ultra-FineWeb fastText classifier marks them positive.
2. QwQ-32B writes a self-contained four-option multiple-choice question for a target domain and difficulty.
3. A pretrained Qwen3-1.7B-Base answers it. CompassJudger-2-32B extracts the final letter. This student is only a router. The paper’s training runs start from random weights.
4. A correct, extractable answer goes to option-level text. Anything else, including an answer the parser cannot read, goes to failure-analysis text.
5. QwQ-32B writes the training document in one of four styles: textbook, web article, question-answer, or dialogue. The document includes the full question and all four options.

Published size:

| Split | Tokens | Documents | Tokens per document |
| --- | ---: | ---: | ---: |
| Option-level (OL) | 108.67B | 92,538,646 | about 1,170 |
| Failure analysis (FA) | 82.76B | 67,107,907 | about 1,230 |
| Total | 191.43B | 159,646,553 | about 1,200 |

The right mix’s 109B matches the option-level split rounded to the nearest billion (108.67). It does not match the full corpus, and it does not match failure analysis. Treat 109B as “all of OL” until a bucket row shows a different draw. Nineteen domains are mapped from FineFineWeb onto MMLU-style subject names (college and high-school biology, chemistry, physics, math, computer science, medicine, and so on). Three difficulty levels are high-school, college, and professional. OL math is 7.44B college maths plus 5.29B high-school mathematics, about 12.7B of the 108.67B. Medicine and biology are larger than math.

MinHash at 60-grams flagged 1,729 near-duplicate documents out of 159.6M, under 0.002%. Documents differ from each other. The underlying seeds do not. About 159.6M documents from about 500,000 seeds is on the order of 300 documents per retained seed. Option-level alone is on the order of 185 documents per seed if the seeds are shared. The corpus is many phrasings of a few hundred thousand web passages.

Decontamination, as reported by the authors, used AllenAI Decon. A document is marked contaminated at answer overlap of at least 60% with meaningful term matches, or passage overlap of at least 40%. They report 17 verified contaminated documents, all in the failure-analysis split, where GSM8K and MMLU questions were echoed during generation. The option-level split has zero verified hits under that rule. GSM8K test leakage is 0%. MMLU test leakage is 3 of 56,168, which they state as 0.005%. One hundred ninety SQuAD hits were checked by hand and called false positives. That scan does not cover every benchmark a 1.5B generalist will be scored on, and a 60% answer-overlap rule misses a question that was rewritten. The authors also say human review of factual correctness, pedagogical usefulness, and hallucinations is future work. The release license in the paper is CC-BY-NC-4.0, the same non-commercial class as ClimbMix.

The controlled experiment is a Qwen3-1.7B architecture, random initialization, one stage, no other data. Option-level for one epoch is 108.67B tokens, about 64 tokens per parameter, and it is the entire run. Failure analysis is 82.76B. The combined corpus is 191.43B, about 113 tokens per parameter. The baseline is Cosmopedia-v2 repeated to a similar budget: four epochs, about 109.7B, or seven epochs, about 192.4B. Unique Cosmopedia-v2 in that comparison is about 27.5B. They also compare with the public Cosmo-1B, which was trained on about 180B tokens of Cosmopedia plus code, math, and instruction data, so it is not a pure Cosmopedia control.

On their generation-plus-parser metric, option-level beat four-epoch Cosmopedia-v2 by +26.81 ARC-Easy, +15.25 ARC-Challenge, +10.11 GPQA Diamond, and +9.87 MMLU-STEM accuracy, with MMLU-STEM valid-answer rate 99.45% versus 72.71%. Failure analysis also beat Cosmopedia, by less, and lost to option-level on 18 of 19 MMLU-STEM domains. The seven-epoch Cosmopedia run scored worse than the four-epoch run. The authors read that as overfitting from repeating the same 27.5B tokens. Combined Genesis beat Cosmo-1B on ARC and on average MMLU-STEM. Cosmo-1B kept the lead on several formal subjects, including college physics, high-school physics, college computer science, and econometrics. Option-level college maths accuracy in their table is 27%, and high-school mathematics is 28.2%. Valid-answer rate near 100% means the model learned to emit a single option letter. The training text is option-by-option explanations of multiple-choice items, and the test is multiple-choice science. The QVAC writeup of the same result says these checkpoints saw Genesis and nothing else, and that a model needs much more data before it is a general model.

That experiment answers a narrow question: if a 1.7B model’s entire pretraining is synthetic STEM multiple choice, this corpus beats repeating Cosmopedia. It does not answer whether 109B of the same text should replace 55B of textbooks, rewritten math, long STEM rollouts, and short factual questions inside a 750B generalist mix that already has 400B of ClimbMix and 87B of math web plus dialogue.

## How the fork lands on a 1.5B model

Code is not the fork. Both mixes spend 85B on the two programming rows.

Math is the fork. Left spends 112B on math rows: 52B organic 4+, 35B dialogue over that web, 10B synthetic textbooks, 15B Swallow rewrites. That is 16.0% of 701B. Right spends 87B on the first two of those, 11.5% of 755B, and adds 109B of multi-domain STEM multiple choice, of which about 13B is the math domains. Right’s math is a smaller set of web pages and dialogues, plus option explanations. Left’s extra 25B is the part that looks like a worked textbook rather than a four-option item. The Genesis per-domain table is why that difference matters: a 1.7B model trained only on Genesis still trailed a Cosmopedia-plus-math-and-code model on the formal subjects.

Web versus synthetic, with each row in one bucket:

| Bucket | Left | Right |
| --- | ---: | ---: |
| ClimbMix | 400 | 400 |
| Organic web math (4+) | 52 | 52 |
| Synthetic dialogue over that math (MIND) | 35 | 35 |
| Textbook or rewrite math | 25 | 0 |
| Synthetic rephrase of high-quality web | 50 | 50 |
| Programming-code rows | 85 | 85 |
| Long-form STEM rollouts (RQA) | 30 | 10 |
| Short factual questions | 15 | 5 |
| Specialized v1.1 | 9 | 9 |
| Genesis III | 0 | 109 |
| **Sum** | **701** | **755** |

Left is 57% ClimbMix. Right is 53% ClimbMix and 14% Genesis. For a 1.5B model at this budget, the web mix should stay the largest single source, and one pass of ClimbMix already is that. The risk on the right is not that Genesis is low quality next to raw Common Crawl. The risk is that 109B of one generated format, grown from about 500,000 seeds, becomes a seventh of the English run. A 1.5B model will imitate that format. The paper’s 99.45% valid-answer rate is the measurement of that imitation.

Repetition, using published unique tokens. “Epoch” here means allocation divided by that published size. Sheet labels are in parentheses when they disagree with the publication.

| Source | Published unique | Left | Right |
| --- | ---: | ---: | ---: |
| ClimbMix | 400B | 1.0 | 1.0 |
| Math 4+ | 52.3B | 1.0 | 1.0 |
| MIND from 4+ | 73B | 0.5 | 0.5 |
| Math textbooks | 25.1B | 0.4 | 0 |
| SwallowMath-v2 | 32B | 0.5 | 0 |
| HQ synth, if it is v2.1 | 93.5B | 0.5 | 0.5 |
| HQ synth, if it is the counted v2 pack | 15.0B | 3.3 | 3.3 |
| CodeAlchemy | sheet label 55B; public estimate ~977B | under 1 of the label | same |
| Nemotron Code v2 | sheet label 45B; public GitHub increment ~340B | about 1 of the label | same |
| RQA | 134.6B, or the 40B label | 0.22 or 0.75 | 0.07 or 0.25 |
| Fact-Seeking | 35.0B | 0.4 | 0.1 |
| Specialized v1.1 | 9.3B | about 1 | about 1 |
| Genesis III OL | 108.67B | 0 | about 1 |

Left does not repeat the rows the right mix deletes. Those rows are partial epochs. The repetition problem both mixes share is the high-quality synthetic row, and only if the bucket still holds the 15B pack. Right’s 109B is not a second epoch of Genesis. It is the whole option-level split, which is a lot of unique strings and a narrow set of seeds.

Contamination that is actually documented:

- Genesis option-level: zero verified Decon hits under the authors’ thresholds. Failure analysis: 17 documents, GSM8K and MMLU echoes. Format overlap with ARC, MMLU, and GPQA is the larger issue, and it is by construction.
- Nemotron-CC-Math-4+: cosine filter at 0.9 against MMLU, MMLU-Pro, MATH, and GSM8K, under 0.002% of documents removed. This is the best-documented math decontamination of the sets in this mix. Textbooks are generated from these documents, so they inherit that filter only to the extent the generator does not put a benchmark item back.
- Nemotron-CC, and therefore ClimbMix and the high-quality rephrases: the authors say they did not decontaminate.
- Specialized v1.1 multiple choice: topics from MMLU `auxiliary_train`. Code-Concepts: a HumanEval concept taxonomy, according to NVIDIA’s Super 3 notes. Both mixes include the full 9B once.
- Fact-Seeking: built to move SimpleQA, and the reported score is SimpleQA rewritten as multiple choice. No public n-gram overlap figure. Fifteen billion is safer than thirty-five. Five billion does not remove the issue; it only reduces the dose.
- Code rows: no measured overlap in the inventory. Public GitHub and synthetic rewrites of public GitHub are the usual HumanEval and MBPP leak path. Same on both sides.

Nothing here is a 70B-model problem of “the model is large enough that a contaminated paragraph does not move the average.” A 1.5B model trained for about 500 tokens per parameter can memorize a short benchmark-shaped document that it sees even once. The practical rule is still one pass of the small sets, the math cosine filter kept, failure-analysis Genesis left out, and the MMLU-auxiliary multiple-choice subset not repeated.

## The edit

Start from the left mix. Change two things.

1. Add 50B from Genesis III option-level only. Do not add failure analysis. Fifty billion is under half an epoch of the 108.67B split, about 33 tokens per parameter, and about 6.6% of a 751B English run. That is enough to take the STEM signal the 1.7B ablation actually measured, without making option letters a seventh of pretraining. Keep the other half of OL unused so a later annealing pass can draw fresh documents instead of repeating the first 50B.
2. Keep the high-quality synthetic row at 50B only when the bucket’s unique tokens support 50B at two epochs or fewer. If the row is still the counted 15B Nemotron-CC-v2 pack, train 30B, which is the cap already written in the curriculum plan, and do not fill the missing 20B with a third pass.

Leave these at the left amounts: ClimbMix 400, Math 4+ 52, MIND 35, Math Textbooks 10, SwallowMath-v2 15, CodeAlchemy 40, Nemotron Code v2 45, RQA 30, Fact-Seeking 15, Specialized v1.1 9.

Resulting English total:

- If the high-quality synthetic row can honestly supply 50B: 701 + 50 = **751B**, about 501 tokens per parameter.
- If that row is cut from 50B to 30B: 681 + 50 = 731B. Raise SwallowMath-v2 from 15B to 32B, one epoch of the published set, which adds the unused 17B. The total is **748B**, about 499 tokens per parameter. Do this only after a sample shows the textbook and Q&A files are both present and are not the same text twice.

Put the Genesis 50B with the annealing sources in the existing phase plan, next to textbooks, Fact-Seeking, and high-quality synthetic. It is synthetic STEM, not warmup web. The phase percentages in the 1.2B plan do not have a Genesis row, so they have to be recomputed when the English total moves from 710B to this sheet. This note does not recompute them.

If the run will not add a row at all, take the left mix at 701B. Being 54B short of 755B is about 36 tokens per parameter. That is a better 1.5B mix than the right sheet, because the right sheet buys its extra length by deleting the textbook, rewrite, long-rollout, and factual rows and spending 109B on one multiple-choice format.

## What still depends on the bucket

A sample of the rows has to confirm the following before the billions above are final. This note does not start a listing job and does not retokenize anything.

- Genesis III. Confirm the files are QVAC Genesis III and not some other corpus with the same nickname. Confirm whether the 109B draw is the option-level split. Read a handful of documents: option-level text explains every choice; failure-analysis text also quotes a wrong student answer. If the stored 109B mixes the two splits, keep the option-level files and drop the failure-analysis files down to the 50B budget. If the stored set is much smaller than 50B, train one epoch and stop.
- High-quality synthetic. The row name says Nemotron-CC v2.1. The counted pack in the training-curriculum note is Nemotron-CC-v2, 15B train tokens. Those cannot both be the allocation. The census picks 50B or 30B.
- RQA. Public size 134.6B, sheet label 40B, disk 171.88 GiB. Thirty billion is safe on either token figure. It is not safe if the stored text is far below 30B. The 25 KB-per-row sample is one shard.
- Fact-Seeking. Published 35.0B, disk 42.51 GiB, sampled rows about 264 bytes. Fifteen billion is the allocation most likely to exceed the stored tokens. If it does, train one epoch and do not move the unused budget onto Hindi or onto ClimbMix.
- Math textbooks. Published 25.1B, disk 28.72 GiB. Ten billion is probably under one epoch. The census still has to count it.
- MIND and Math 4+. Disk is 84.13 GiB and 57.92 GiB against 35B and 52B allocations. Same rule: one epoch, then stop.
- SwallowMath-v2, ClimbMix, CodeAlchemy, and Nemotron Code v2 have no measured prefix in the 27 September inventory. If Swallow is absent, the left mix loses the 15B rewrite and the fallback that fills a short high-quality-synthetic row. If ClimbMix is under 400B unique, do not repeat it. If either code slice is smaller than its allocation, both mixes repeat code the same way; that still does not make Genesis the right substitute.
- Overlap between Genesis seeds and ClimbMix. The generated documents should be new text. The FineFineWeb seeds may sit inside Nemotron-CC. A MinHash between a Genesis sample and ClimbMix is the check. Overlap of seeds is acceptable at 50B. It is a worse trade at 109B.
- Specialized v1.1 multiple choice and Code-Concepts. Both mixes already include them. A spot check against MMLU `auxiliary_train` and HumanEval decides whether those two subsets stay at one epoch or get cut. It does not decide left versus right.

## Pick

Small edit of the left mix. Keep Math Textbooks at 10B, SwallowMath-v2 at 15B, RQA at 30B, and Fact-Seeking at 15B. Add 50B of Genesis III option-level text, not the 109B option-level split and not failure analysis. Cap the high-quality synthetic row at two epochs of whatever unique tokens are actually in the bucket, which is 30B if that row is still the counted 15B pack. The English total is then 751B, or 748B if the synthetic cap binds and the unused half of SwallowMath-v2 fills it.

The right mix is the wrong trade for a 1.5B generalist. It spends 109B, about one full pass of a multiple-choice explanation corpus grown from roughly 500,000 seeds, and it deletes the textbook, rewrite, long-rollout, and factual rows to do it. The 1.7B Genesis result supports a modest option-level supplement. It does not support making that supplement the whole STEM diet. The code rows stay as they are.
