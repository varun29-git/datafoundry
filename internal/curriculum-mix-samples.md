# What the two mixes actually contain

Sampled 1 October 2026 from this Mac. No EC2, no full-dataset download, no training. Excerpts are the first zstd page of a `text` column (or a public preview file when the bucket has no prefix). A few hundred characters each. Sizes are full listings, not guesses from one shard.

## Genesis III, from a local checkout

The checkout does not say what Genesis III is. Its commit is `fd777c55` (“Initialize project”) and `git ls-tree` of `HEAD` is empty. The only files on disk are an untracked copy of Karpathy’s nanochat in a `nanochat/` subdirectory. That tree talks about ClimbMix (`nanochat/dev/LOG.md`, `nanochat/nanochat/dataset.py`). A search of the checkout for “Genesis” finds nothing.

An empty Hugging Face cache for `datasets--qvac--GenesisIII` (snapshot `b7a894a7`, 0 bytes of data) contained empty folders for `college_maths`, `professional_medicine`, `machine_learning`, `high_school_physics`, and `college_computer_science`. Neither `s3://<research-data-bucket>/` nor `s3://<research-pack-bucket>/` has a Genesis prefix. The description below is the public dataset card `qvac/GenesisIII` plus five 16 KB `preview.parquet` files, not a file in the local checkout and not a bucket object.

The card says QVAC Genesis III is a synthetic English STEM corpus: **159,646,553 documents, about 191 billion tokens**, 19 domains, CC BY-NC 4.0. The card’s total is the whole release. It does not publish a separate option-level token count, so the sheet’s 109B is not something this sample can confirm from the card.

How it is built, from the card’s “Dataset Creation” section:

1. Seed passages from FineFineWeb, kept if the Ultra-FineWeb classifier marks them high quality, then mapped onto curriculum domains.
2. QwQ-32B writes a four-option multiple-choice question.
3. Qwen3-1.7B-Base answers. CompassJudger-2-32B-Instruct extracts the letter. A bad or unreadable answer goes to failure analysis. A correct answer goes to option-level reasoning.
4. QwQ-32B writes the document in one of four styles: educational textbook, web article, question-answer, or dialogue.

Each preview file has 8 rows and both pipelines. Columns are `text`, `domain`, `pipeline`, `style`. Option-level rows are still multiple-choice explainers. They are not web pages and they are not source code.

Option-level excerpts from the preview files:

1. `college_maths` / `educational_textbook` (5,117 characters): “# Analysis of Ground State Energy in an Infinite Square Well When Width is Halved … Calculate the ground state energy of a particle in an infinite square well if the width is halved…”
2. `college_maths` / `web_article` (5,395): “# The Coin Flip Conundrum: Cracking the Probability Puzzle … If a fair coin is flipped three times, what is the probability of getting exactly two heads? Options: A. 1/4 B. 3/8 C. 1/2 D. 1/3”
3. `professional_medicine` / `web_article` (5,460): “# Mastering Medical Device Definitions: A Deep Dive into FDA’s Single-Use Rule … What is a key characteristic of a single-use medical device as defined by the FDA?”
4. `machine_learning` / `qa` (3,393): “What is the primary purpose of applying feature scaling in machine learning models? A. To normalize input data distributions B. To increase model training speed…”
5. `high_school_physics` / `web_article` (5,212): “What energy conversion occurs when a laser beam is directed onto water to generate underwater sound? A. Light to sound B. Sound to light…”

Failure-analysis rows sit in the same files (college maths dialogue about the sequence 2, 4, 8, 16; a student who guessed 24). A draw that does not filter `pipeline == option_level` mixes the two.

## Bucket prefixes

`s3://<research-data-bucket>/` top level: `_tokenizer_scratch/`, `artifacts/`, `bootstrap/`, `datasets/`, `source-snapshots/`, `translation-benchmark/`, `translation-staging/`, `translations/`.

`datasets/` children: `Nemotron-Pretraining-Specialized-v1/`, `v1.1/`, `v1.2/`, `fineweb2-indic/`, `nemotron-cc-hq/`, `nemotron-cc-math-v1/`, `nemotron-cc-v2/`, `nemotron-climbmix/`, `sangraha/`.

A prefix walk to depth 3 of that bucket (257 prefixes) and of `s3://<research-pack-bucket>/` (28 prefixes) found no `swallow`, `alchemy`, `genesis`, or Nemotron Code v2 name.

| Name | In the bucket? |
| --- | --- |
| ClimbMix | Yes |
| Nemotron Math 4+ | Yes |
| Nemotron MIND | Yes |
| Math Textbooks | Yes |
| SwallowMath | Missing |
| Nemotron-CC v2.1 HQ Synth | English text missing. A tokenized Nemotron-CC-v2 pack is on the other bucket. A 1.8 MB Indic review uses the v2.1 name. |
| CodeAlchemy | Missing |
| Nemotron Code v2 | Missing. Public HF copy is gated. |
| RQA | Yes |
| Fact-Seeking | Yes |
| Specialized v1.1 | Yes |
| Genesis III | Missing |

`datasets/nemotron-cc-v2/Diverse-QA/` is 32 parquet files, 25.98 GiB. That is not Nemotron Code v2 and it was not sampled as one of the named rows.

## Sets that are in the bucket

### ClimbMix

`s3://<research-data-bucket>/datasets/nemotron-climbmix/karpathy-400b-shuffle/`

13,089 objects, **558.57 GiB**. 6,543 parquet shards (`shard_00000` through `shard_06542`), about 90 MB each. `SOURCE.json` says repository `karpathy/climbmix-400b-shuffle`, source `nvidia/Nemotron-ClimbMix`, status completed 2026-09-28. Schema is one `text` string. `shard_00000` has 86,016 rows.

This is ordinary web text, plus some docs and some spam. Not textbooks, not a code corpus.

1. `shard_00000`: “Protect your business and employee's during flu seaon … the Center for Disease Control (CDC) established the National Influenza Vaccination week…”
2. `shard_00000`: “Selective Use of Data Avoids Real Issues in Improving Public Education for All Children…”
3. `shard_00000`: “Mistletoes - biogeography … The northward separation of Australia from Antarctica commenced about 125 million years ago…”
4. `shard_00000`: “To apply optimization directives manually on templates when using config file commands, specify the template arguments and class…” (C++ compiler docs, 204 characters)
5. `shard_00200`: “Facts About r programming homework help Revealed…” (homework-help spam) and, nearby in the same shard, a short fashion blurb about a grey beanie and tobacco loafers.

### Nemotron Math 4+

`datasets/nemotron-cc-math-v1/4plus/`

46 objects, **57.92 GiB**. `part_000000` has 983,993 rows. Columns: `id`, `text`, `metadata` with WARC filename and id, FineMath scores, NemoCurator scores, category. This is scored web math, mixed quality.

1. A Jane Street careers page: “Trader Intern Interview, New York, NY.”
2. A lesson plan: “Homework - Section 1: Warm Up and Homework Check … Students will be able to use radians to measure angles.”
3. An NRICH-style page: “Benjamin and George discovered an interesting pattern when starting with 42 and using the rule: multiply by 2 and subtract by 5.”
4. A worked minimum-perimeter problem: “Suppose the area of a rectangle is 36 square inches…”
5. A page that already sounds like a generated textbook: “# Title: Advanced Calculus: A Comprehensive Guide … Chapter 1: Limits and Continuity.”

Row lengths on the first page of `part_000000` are about 2–4k characters. `part_000020` runs longer, up to about 15k.

### Nemotron MIND

`datasets/nemotron-cc-math-v1/4plus_MIND/`

90 objects, **84.13 GiB**. `part_000000` has 992,247 rows. Same score metadata as 4+, plus `warc_type`. The text is a two-person dialogue about a math page, not the page itself.

1. “Debate on NonEuclidean Geometry Concepts. Participant A: … given a line \( l \) and a point \( P \), the lines \( PX \) and \( PY \) are parallels…”
2. “Participant A: Let's discuss … Big-O, Big-Omega, and Big-Theta…”
3. “Participant A: … \( a^{-n} = 1/a^n \). … \( x^{-3} \) can be simplified to \( 1/x^3 \).”
4. “Participant A: The context provides a clear illustration of how the number 1957 can be represented as a multiplier…” (the dialogue is reciting a multiplication table from the source page)
5. “Participant A: Let's discuss the convergence of the series \(\sum (x+2)^n\). … the ratio test…”

### Math Textbooks

`datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-Math-Textbooks/`

13 objects, **28.72 GiB**. `part_000000` has 1,000,000 rows. Schema: `text`, `license`, `metadata.category`, `metadata.models_used`, `uuid`. First-page documents are 6–10k characters. They are section prose with a heading, a definition, and LaTeX. They do not look like the Jane Street page or the homework-help spam.

1. “### Understanding Profit Models and Quadratic Functions … \( P(u) = au^2 + bu + c \) … profit (in riyals…)”
2. “A fundamental problem in graph theory involves finding a minimal spanning tree … Kruskal's algorithm…”
3. “# The Ford-Fulkerson Algorithm for Maximum Flow…”
4. “## Introduction to Acceleration and Deceleration in Physics…”
5. `part_000008`: “Understanding the Foundations of Probability Theory … statistics, physics, computer science, economics, and engineering.”

### RQA

`datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-RQA/`

175 objects, **171.88 GiB**. `part_000000` has 100,000 rows and one row group. Documents on the first page are 11–40k characters. Each one is a long multi-part question, not a short quiz item and not a textbook chapter.

1. “Question: Consider an asymmetric encryption scheme Π proven IND-CCA2 secure in the random oracle model…”
2. “Question: Consider a generic container type `C<T, Alloc>` adhering to the C++ standard library's sequence container requirements…”
3. “Question: In a time-triggered communication framework for distributed real-time systems…”
4. “Question: In high-throughput sequencing experiments for transcriptome analysis, count data often exhibit overdispersion…”
5. `part_000090`: “A palladium-catalyzed chain-walking reaction proceeds through a sequence of β-hydride elimination…”

The five questions are crypto, C++, real-time systems, RNA-seq, and organometallic chemistry. Same shape, different fields.

### Fact-Seeking

`datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/`

72 objects, **42.51 GiB**. `part_000000` has 8,000,000 rows. Documents are short. The first page of `part_000000` is 108–481 characters. The first page of `part_000040` is 101–200 characters.

They come in bursts about one article.

From `part_000000`, all about the 10th Tank Corps:

1. “How many times was the 10th Tank Corps formed during its history in the Red Army? A. Once B. Three times C. Twice D. Four times. Answer: C. Twice”
2. “On what date and location was the 107th Separate Air Liaison Flight formed…? Answer: C”
3. “What was the purpose of the 10th Tank Corps' movements to the Estonian and Latvian borders in September–October 1939?”
4. “On 10 October 1939, which unit was transferred from the 10th Tank Corps…? Answer: D. 18th Light Tank Brigade”
5. From `part_000040`, a different burst, all about the game A Monster's Expedition: “What feature of the game's music was specifically praised by reviewers? Answer: The music was praised for being synchronized to the player's actions.” Nearby rows ask what Jupiter Hadley said, the Metacritic score (92), and which critic wrote for Push Square.

### Specialized v1.1

`datasets/Nemotron-Pretraining-Specialized-v1.1/`

68 objects, **32.49 GiB**.

| Subset | Objects | GiB |
| --- | ---: | ---: |
| Code-Concepts | 61 | 29.89 |
| Multiple-Choice | 4 | 2.28 |
| Unconditional-Algorithmic | 1 | 0.19 |
| Formal-Logic | 1 | 0.07 |
| Economics | 1 | 0.06 |

Code-Concepts (`part_000000`, 250,000 rows) is synthetic Python: a function signature, a docstring, and a problem. Two of the twelve decoded rows were the same function, `longest_palindrome_by_sorted_points`.

1. `detect_no_dup_range_gcd_mod(nums, queries, mod)` — “Return the GCD modulo `mod` for each subarray if the subarray contains no duplicate values.”
2. `count_divisible_gcd_duplicates` — “Count subarray ranges that contain at least one duplicated element and whose gcd divides `mod`.”
3. `longest_palindrome_by_sorted_points` — sort 2-D points, concatenate coordinates, find the longest palindromic substring.
4. The next decoded row is that same function again.
5. `longest_palindromic_point_sequence` — map point coordinates to letters and concatenate by distance from the origin.

Multiple-choice is bar-exam style hypotheticals (a robbery of Franklin, Alice suing Bob over a car accident), not code. Formal-logic is “Which of the given formulas of PL is the best symbolization…” with a printed answer. Economics is “The following are multiple choice questions (with answers) about economics” (Keynesian cross, Giffen goods). Unconditional-algorithmic is contest problems without a Python signature in the opening (“Maximum Weight Sub-set of Intervals with Capacity Constraint”).

### Nemotron-CC high-quality synthetic

No English text prefix for Nemotron-CC v2.1 High-Quality-Synthetic.

What is stored:

- `s3://<research-pack-bucket>/data/nemotron_cc_v2_hqsynth_tinyllama_15b_parallel_20260730T185305Z/` — 101 objects, **28.03 GiB**. `data_manifest.json` says dataset `nvidia/Nemotron-CC-v2`, config `High-Quality-Synthetic`, tokenizer `TinyLlama/TinyLlama-1.1B-Chat-v1.0`, `uint16`, seq_len 2048, **15,000,000,001 train tokens** and 50,000,001 validation tokens. This is token ids, not documents. It is v2, not v2.1.
- `translations/Nemotron-CC-v2.1/High-Quality-Synthetic/` — 155 objects, **1.84 MB**. A Krutrim review for Bengali and Hindi, not the English corpus.
- `data/nemotron-domain-classification/.../High-Quality-Synthetic/` — about 2 MB parquet parts whose columns are `id` and `domain_pred` only.

Five decodes of `worker_000_train.uint16.bin` with the cached TinyLlama sentencepiece model, 4,000 bytes at each offset:

1. Offset 0: “The Chronometric Micrometer, favored by amateur astronomers, leverages the apparent rotation of the celestial sphere…”
2. Offset 180,000,000: “2010 assessment revealed that countries with robust enabling environments demonstrated significant progress in sanitation coverage…”
3. Offset 360,000,000: “EMDR Intensives: EMDR intensives typically span 4-6 hours daily over 2-5 consecutive days…”
4. Offset 540,000,000: “offered in Ford Explorer V8 models from 2009 to 2010… the 6R80, rated for approximately 400 ft-lbs of torque…”
5. Offset 720,000,000: a geography paraphrase that then says “In this version, I've maintained the formal tone and detailed approach, using varied sentence structures and vocabulary to create a diverse paraphrase.”

That last one is a rephrase of a web passage with the rewriter’s instruction left in the text. The other four read as articles (astronomy hobby, sanitation policy, therapy, car transmissions). Not code, not a problem set.

## Named sets missing from the bucket

### SwallowMath

No prefix. Public card `tokyotech-llm/swallow-math-v2`: **32B tokens** rewritten from FineMath-3+ by Qwen3-235B, Apache 2.0. Textbook split 13,302,336 samples / 18.3B tokens. Q&A split 12,635,739 samples / 13.6B tokens. Two real lines from the public jsonl, first 12 KB only:

1. Textbook: “## Background: These problems involve key concepts in calculus and real analysis, particularly functional equations, continuity, piecewise functions, and optimization…”
2. Textbook, next line: “## Background: Statistical inference is a fundamental branch of statistics concerned with drawing conclusions about populations based on sample data…”
3. Q&A: “Question 1: Given a continuous function \( f \) satisfying \( f(3x) - f(x) = x \) for all real \( x \), and \( f(8) = 7 \), what is the value of \( f(14) \)? Answer 1: Assume a linear solution \( f(x) = \frac{1}{2}x + C \).”

Same rewritten-math voice as the Nemotron textbooks, but the openers are “Background” and “Question / Answer”, and the card says the source is FineMath-3+.

### CodeAlchemy

No prefix. Public card `open-alchemy/code-alchemy`: about **976.6B tokens**, 162M rows, five training configs (code-enhance 124.5B, code-qa 31.3B, code-dev 269.8B, code-dialogue 544.7B, code-trace 6.3B). The card says the `text` column is User/Assistant prompt-completion pairs and that raw source files are not in the release. Shards are about 1 GB and dictionary-encoded; a 1.5 MB range of `code-qa/train-00001-of-00031.parquet` did not yield a plain-text page, so there is no CodeAlchemy excerpt in this note.

### Nemotron Code v2

No prefix. `nvidia/Nemotron-Pretraining-Code-v2` on Hugging Face returned 401 GatedRepo, so no text was read. The card’s config names are `Nemotron-Code-Metadata`, `Synthetic-Question-Answering`, `Synthetic-Student-Teacher`, `Synthetic-Code-Review`, `Synthetic-Rewriting`, and `Synthetic-Transpilation`.

## What the fork actually is

The two mixes share ClimbMix, Math 4+, MIND, both code rows, HQ synth, and Specialized v1.1. The fork is Genesis III 109B against Math Textbooks 10B + SwallowMath-v2 15B + the extra 20B of RQA and extra 10B of Fact-Seeking.

From these samples:

- **Math Textbooks** are long synthetic sections (profit functions, Ford-Fulkerson, probability). About 6–10k characters. They are a third view of math, written as chapters.
- **SwallowMath** is also rewritten math, from FineMath-3+, in a textbook style and a Q&A style. It is not in the bucket. The three public lines are the same kind of prose as the Nemotron textbooks, with different headings.
- **RQA** is long multi-part questions across STEM, 11–40k characters. It is not a textbook and not a four-option item.
- **Fact-Seeking** is short quiz items, often many questions about one article (a tank corps, then a video game). Easy to repeat a topic even inside one shard.
- **Genesis III** is not in the bucket. The public previews are synthetic STEM multiple choice, rendered as a textbook section, a web article, a Q&A, or a dialogue. Option-level and failure-analysis are mixed in the same file. The card’s figure is about 191B tokens for both pipelines together.

Genesis III does not look like ClimbMix. ClimbMix is flu-shot ads, biogeography, compiler docs, and homework-help spam. Genesis looks like a blend of synthetic textbook, synthetic web article, and synthetic dialogue, all wrapped around a four-option question. It is not code.

Overlap you can see from the samples, and overlap you cannot:

- MIND dialogues sit on the same kind of math page as Math 4+ (a participant recites the source). They are not a second independent corpus.
- Some Math 4+ rows already look like textbook chapters (“Advanced Calculus: A Comprehensive Guide”). The Nemotron textbook rows are more uniform and longer. No shared paragraph showed up in these few pages.
- Swallow’s public lines resemble the Nemotron textbooks in voice. They are not the same documents in this sample.
- Fact-Seeking repeats a topic inside a shard. That is the duplicate pattern, not a copy of RQA or of Genesis.
- CodeAlchemy and Nemotron Code v2 cannot be compared. Neither prefix exists here, and the Code v2 files are gated. Specialized v1.1 Code-Concepts is a third thing: synthetic Python stubs, with a repeated function in the first page. It is not GitHub source and it is not the CodeAlchemy User/Assistant format described on that card.
- The HQ-synth token pack is rephrased web articles. One window still contains the line “create a diverse paraphrase.” That is not Genesis (no A/B/C/D question) and not the math textbooks.
