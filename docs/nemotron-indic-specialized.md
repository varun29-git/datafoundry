# Nemotron Indic: specialized release for seven languages

Checked against the live Hugging Face cards on 30 October 2026. No corpus files were downloaded. Sizes below are copied from the cards or from Table 3.1 / Table 3.2 of the companion report. Where a source does not publish a number, the cell says so.

The seven languages are Hindi, Bengali, Tamil, Telugu, Kannada, Marathi, and Gujarati. All seven sit in the twelve-language priority group (with Malayalam, Nepali, Odia, Punjabi, and Urdu).

## 1. What the open release actually is

The corpus name in the report and the blog is **Nemotron-Pretraining-Indic-v1** (the blog also writes Nemotron-pretraining-Indic-v1). It is translated English, not text originally written in Indian languages. “Native script” means the Indic writing system. “Romanized” means that Indic text written in Latin script, not an English gloss. ([Hugging Face blog, 16 October 2026](https://huggingface.co/blog/nvidia/scaling-indic-pretraining); [companion report](https://arxiv.org/html/2610.26006))

Hugging Face now ships that corpus as two repos plus the report. The blog post still says “releasing soon” and does not name the repo ids. The cards are the later source: the specialized repo was created on 26 October 2026, and both data repos were last modified on 29 October 2026.

| Piece | URL | Access | What it is |
| --- | --- | --- | --- |
| Specialized half | [nvidia/Nemotron-Pretraining-Indic-Specialized-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Indic-Specialized-v1) | Public. API `gated: false`. No approval. | Translations whose `_source_repo` is [Specialized-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1) or [Specialized-v1.1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1.1). |
| Crawl half (“CC-v1”) | [nvidia/Nemotron-Pretraining-Indic-CC-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Indic-CC-v1) | Manually gated. | The other records. The two repos do not overlap. |
| Companion report | [nvidia/nemotron-indic-pretraining-report](https://huggingface.co/datasets/nvidia/nemotron-indic-pretraining-report) and [arXiv:2610.26006](https://arxiv.org/abs/2610.26006) | Public. Card license `cc-by-4.0`. | *Scaling Synthetic Pre-training Data and Evaluation for Indic LLMs*, NVIDIA and AI4Bharat. |

Both data cards use the same layout: 34 language–script configs, one `train` split, parquet at `data/<language>-<script>-IN/train-*`, and a 21-field schema. The text field is `text`. Provenance is `_source_repo`, `_source_config`, `_subset_key`, `_tier`, and `_source_file`. Both cards date the collection 3 September 2026 and call the version `v1`.

### License

The specialized card’s YAML says `license: other`. The body assigns terms by source record, not by language:

- Specialized-v1.1, and most of Specialized-v1: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- Wiki-Rewrite and Scientific-Coding, if a record comes from those subsets: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) and [GFDL 1.3](https://www.gnu.org/licenses/fdl-1.3.html).
- The card says the set is ready for commercial or non-commercial use, subject to those source terms.

The CC-v1 card is the [NVIDIA Data Agreement for Model Training](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Indic-CC-v1) (the card cites the version dated 19 December 2025). The click-through asks for company, institutional email, and a checkbox that use is for model training only. FinePDFs-edu rows also carry the ODC Attribution License.

### Token counts: report versus the two cards

The report and the blog describe one corpus. The cards describe the two repos that were actually uploaded. The totals do not match. Both use a Gemma-4 tokenizer. The cards name `google/gemma-4-31B-it` and count the `text` field. Input tokens are English `token_count_source` and are not added to the output size.

| Accounting | Native-script output | Romanized output | Total output | Documents |
| --- | --- | --- | --- | --- |
| Report Table 3.1, all 22 languages | 2,601.0B (2,273.8B in the 12 priority languages + 327.2B in the other 10) | 224.6B (12 languages only) | 2,825.6B | 2,440.8M |
| Blog Figure 1 | 2,601.0B | 224.6B | same 2.83T headline | not stated |
| Specialized card only | 242.8B priority native + 9.2B for the other 10 | 43.8B | 295.8B | 167,954,507 rows |
| CC-v1 card only | 1,732.7B priority native + 289.6B for the other 10 | 133.4B | 2,155.8B | 1,933,876,906 rows |
| Specialized + CC-v1 cards | 2,274.3B | 177.2B | 2,451.6B | 2,101,831,413 rows |

The uploaded pair is about 374B output tokens and about 339M rows short of Table 3.1. This report does not explain the gap. The blog’s “2.8 trillion” is the paper total, not the specialized repo.

Romanized text is extra script coverage of translated material, not a second body of facts. The report says each romanized config is a transliteration of a subset of the accepted native translations, about a tenth of the native volume. The specialized card is slightly weaker: native and romanized configs for the same language are not necessarily the same source samples. The ten lower-resource languages have no romanized configs.

Stored parquet, from the cards: specialized 1,253,140,731,121 bytes (10,959 shards, ~1.14 TiB); CC-v1 9,508,173,264,936 bytes (72,262 shards, ~8.65 TiB). The CC-v1 page also shows a repo file size of 9.51 TB.

### The seven languages in the full report corpus

Table 3.1 is the combined corpus, not the specialized repo. Target tokens are Gemma-4 billions. “1st pass” and “Rewrite” are the two retained paths. Docs are millions.

| Language | Config | Target tokens (B) | 1st pass + rewrite (B) | Docs (M) | English source tokens (B) |
| --- | --- | --- | --- | --- | --- |
| Hindi | `hi-Deva-IN` | 149.3 | 142.0 + 7.3 | 171.8 | 118.1 |
| Hindi | `hi-Latn-IN` | 18.4 | 16.9 + 1.5 | 17.2 | 12.8 |
| Bengali | `bn-Beng-IN` | 138.9 | 124.9 + 14.0 | 166.3 | 114.0 |
| Bengali | `bn-Latn-IN` | 19.0 | 15.6 + 3.4 | 16.7 | 12.2 |
| Tamil | `ta-Taml-IN` | 157.5 | 112.9 + 44.6 | 163.6 | 110.5 |
| Tamil | `ta-Latn-IN` | 20.0 | 16.3 + 3.7 | 16.0 | 10.9 |
| Telugu | `te-Telu-IN` | 192.4 | 161.8 + 30.6 | 168.6 | 115.3 |
| Telugu | `te-Latn-IN` | 18.8 | 17.0 + 1.8 | 16.9 | 12.2 |
| Kannada | `kn-Knda-IN` | 180.5 | 116.2 + 64.3 | 156.3 | 103.5 |
| Kannada | `kn-Latn-IN` | 19.1 | 16.4 + 2.7 | 16.7 | 11.3 |
| Marathi | `mr-Deva-IN` | 152.8 | 140.4 + 12.4 | 167.7 | 114.4 |
| Marathi | `mr-Latn-IN` | 17.6 | 13.1 + 4.5 | 16.3 | 11.6 |
| Gujarati | `gu-Gujr-IN` | 196.4 | 168.8 + 27.6 | 169.3 | 115.5 |
| Gujarati | `gu-Latn-IN` | 17.2 | 15.2 + 2.0 | 16.5 | 12.0 |

None of these seven is absent from the report. First-pass acceptance of the English source tokens is lowest for Kannada native (57%) and Tamil native (67%), and highest for Hindi native (93%).

## 2. What “CC1” is, and what is still gated

**CC1 is the repo `nvidia/Nemotron-Pretraining-Indic-CC-v1`.** The id is the non-specialized half of Nemotron-Pretraining-Indic, version 1. It is not a Common Crawl snapshot id. The card’s English seeds are:

- [nvidia/Nemotron-CC-v2](https://huggingface.co/datasets/nvidia/Nemotron-CC-v2) — English Common Crawl web text and Diverse QA. Configs: `High-Quality`, `High-Quality-Synthetic`, `Medium-High-Quality`, `Medium-Quality`, `Diverse-QA`, `Translated-Diverse-QA`.
- [nvidia/Nemotron-CC-v2.1](https://huggingface.co/datasets/nvidia/Nemotron-CC-v2.1) — later crawl quality tiers, synthetic rephrases, and high-quality diverse QA. Configs include `High-Quality`, `High-Quality-Synthetic`, `High-Quality-DQA`, translated-to-English tiers, and their synthetic rephrases.
- [HuggingFaceFW/finepdfs-edu](https://huggingface.co/datasets/HuggingFaceFW/finepdfs-edu) — educational PDF text. This seed is not in the report’s Table 3.2.

The gate is manual. The raw README returns 401 without an accepted agreement. The dataset page still shows the card. API `gated` is `"manual"`. Fields requested: Company, Institutional Email, and “I agree to use this dataset for model training purposes ONLY.”

### Still gated versus open

| Repo | Gate | Role for this corpus |
| --- | --- | --- |
| [Nemotron-Pretraining-Indic-Specialized-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Indic-Specialized-v1) | Open | Indic translations of Specialized-v1 and v1.1. This is the set that needs no approval. |
| [Nemotron-Pretraining-Specialized-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1) and [v1.1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1.1) | Open | English seeds of that half. |
| [nemotron-indic-pretraining-report](https://huggingface.co/datasets/nvidia/nemotron-indic-pretraining-report) | Open | The paper PDF. |
| [Nemotron-Pretraining-Indic-CC-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Indic-CC-v1) | Manual | The crawl / FinePDFs half. This is the access request. |
| [Nemotron-CC-v2](https://huggingface.co/datasets/nvidia/Nemotron-CC-v2), [Nemotron-CC-v2.1](https://huggingface.co/datasets/nvidia/Nemotron-CC-v2.1) | Manual | English seeds named on the CC-v1 card. |
| [Nemotron-CC-Math-v1](https://huggingface.co/datasets/nvidia/Nemotron-CC-Math-v1) | Auto | In the report’s sample as `cc_math_v1_4plus` (8.65%). Not named as a seed on either Indic card. |
| [Nemotron-Pretraining-SFT-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-SFT-v1) | Manual | In the report’s sample as `pretraining_sft_v1` (12.03%). Configs `Nemotron-SFT-Code`, `Nemotron-SFT-General`, `Nemotron-SFT-MATH`. Not named on either Indic card. |
| [Nemotron-Pretraining-Code-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Code-v1), [Code-v2](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Code-v2), [Nemotron-CC-Code-v1](https://huggingface.co/datasets/nvidia/Nemotron-CC-Code-v1) | Manual | Not in Table 3.2 and not named on either Indic card. |

`HuggingFaceFW/finepdfs-edu` itself is public. Its Indic translations, if shipped, are inside the gated CC-v1 repo.

## 3. Specialized collection: subsets and the seven languages

The ungated repo is **not** split by content subset. It has 34 configs, one per language and script, and a single `train` split. Source subset is a column (`_source_config` / `_subset_key`), and the card says membership and proportions vary by configuration. No per-subset size by language is published. The sizes in the first table are the whole specialized repo for that language, mixed across every specialized source that was shipped.

### Published sizes for the seven languages

Output tokens are Gemma-4 billions on `text`. Input tokens are English source billions. Split is `train` for every row. ([Specialized card](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Indic-Specialized-v1))

| Language | Config | Rows | Input tokens (B) | Output tokens (B) |
| --- | ---: | ---: | ---: | ---: |
| Hindi | `hi-Deva-IN` | 12,041,387 | 13.9 | 17.4 |
| Hindi | `hi-Latn-IN` | 2,357,646 | 2.8 | 3.8 |
| Bengali | `bn-Beng-IN` | 11,685,514 | 13.4 | 16.5 |
| Bengali | `bn-Latn-IN` | 2,279,084 | 2.6 | 3.7 |
| Tamil | `ta-Taml-IN` | 11,735,355 | 13.5 | 18.5 |
| Tamil | `ta-Latn-IN` | 2,139,697 | 2.3 | 3.9 |
| Telugu | `te-Telu-IN` | 11,969,113 | 13.8 | 21.8 |
| Telugu | `te-Latn-IN` | 2,286,686 | 2.6 | 3.6 |
| Kannada | `kn-Knda-IN` | 11,056,436 | 12.3 | 20.1 |
| Kannada | `kn-Latn-IN` | 2,221,840 | 2.4 | 3.7 |
| Marathi | `mr-Deva-IN` | 11,778,571 | 13.3 | 17.4 |
| Marathi | `mr-Latn-IN` | 2,204,349 | 2.4 | 3.4 |
| Gujarati | `gu-Gujr-IN` | 11,738,710 | 13.4 | 21.3 |
| Gujarati | `gu-Latn-IN` | 2,312,913 | 2.6 | 3.5 |

All seven are present in native script and in Latin script. None is absent at the repo level.

### Which English subsets were translated

Table 3.2 of the report is the sampling plan for the whole Indic corpus. Shares are percent of the English sampling target, after dropping RQA and renormalizing. They are not Indic token counts. The eight specialized rows sum to 13.32% of that target.

| Report subset id | English config | Share of sampling target | In the ungated Indic repo’s seed list |
| --- | --- | ---: | --- |
| `specialized_v1_math_textbooks` | `Nemotron-Pretraining-Math-Textbooks` | 2.97% | Yes, Specialized-v1 |
| `specialized_v1_wiki_rewrite` | `Nemotron-Pretraining-Wiki-Rewrite` | 2.68% | Yes, Specialized-v1 |
| `specialized_v1_stem_sft` | `Nemotron-Pretraining-STEM-SFT` | 1.61% | Yes, Specialized-v1 |
| `specialized_v11_code_concepts` | `Nemotron-Pretraining-Code-Concepts` | 4.67% | Yes, Specialized-v1.1 |
| `specialized_v11_multiple_choice` | `Nemotron-Pretraining-Multiple-Choice` | 1.08% | Yes, Specialized-v1.1 |
| `specialized_v11_formal_logic` | `Nemotron-Pretraining-Formal-Logic` | 0.15% | Yes, Specialized-v1.1 |
| `specialized_v11_economics` | `Nemotron-Pretraining-Economics` | 0.10% | Yes, Specialized-v1.1 |
| `specialized_v11_unconditional_algo` | `Nemotron-Pretraining-Unconditional-Algorithmic` | 0.06% | Yes, Specialized-v1.1 |
| `specialized_v1_rqa` | `Nemotron-Pretraining-RQA` | dropped (was 1.00% before renormalizing) | English config exists; not in the translated sample |
| not listed | `Nemotron-Pretraining-InfiniByte-Reasoning` | not in Table 3.2 | English config exists; not in the translated sample |
| not listed | `Nemotron-Pretraining-Scientific-Coding` | not in Table 3.2 | English config exists; not in the translated sample |

The twelve-language workflow, which includes all seven languages, applied the same translation and repair path to every source it used. The card still warns that source mix varies by config, and it does not publish a subset-by-language count. For the eight sampled subsets, each of the seven languages is in that shared workflow. Per-subset size is not published. For RQA, InfiniByte, and Scientific Coding, the seven languages are absent from the published sample. File-level `_source_config` values were not scanned, because that would mean reading the corpus.

English token counts in the subset sections are the English seed cards, not Indic sizes.

### Math textbooks

Undergraduate-and-above textbook sections generated from Nemotron-CC-Math documents that were first classified by educational level. English seed: 25.1B tokens, Qwen3-30B-A3B and Qwen3-235B-A22B. License follows Specialized-v1, CC BY 4.0. ([Specialized-v1 card](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1))

| Language | Split | Configs | Size for this subset |
| --- | --- | --- | --- |
| Hindi | `train` | `hi-Deva-IN`, `hi-Latn-IN` | not published |
| Bengali | `train` | `bn-Beng-IN`, `bn-Latn-IN` | not published |
| Tamil | `train` | `ta-Taml-IN`, `ta-Latn-IN` | not published |
| Telugu | `train` | `te-Telu-IN`, `te-Latn-IN` | not published |
| Kannada | `train` | `kn-Knda-IN`, `kn-Latn-IN` | not published |
| Marathi | `train` | `mr-Deva-IN`, `mr-Latn-IN` | not published |
| Gujarati | `train` | `gu-Gujr-IN`, `gu-Latn-IN` | not published |

### Wiki rewrite

English Wikipedia articles rewritten with Qwen3-30B-A3B-Instruct-2507 for clarity and formatting. Disambiguation pages, redirects, and non-article sections are dropped. English seed: 7.9B tokens. The Indic card puts Wiki-Rewrite under CC BY-SA 4.0 and GFDL 1.3, unlike the CC BY 4.0 subsets.

| Language | Split | Configs | Size for this subset |
| --- | --- | --- | --- |
| Hindi | `train` | `hi-Deva-IN`, `hi-Latn-IN` | not published |
| Bengali | `train` | `bn-Beng-IN`, `bn-Latn-IN` | not published |
| Tamil | `train` | `ta-Taml-IN`, `ta-Latn-IN` | not published |
| Telugu | `train` | `te-Telu-IN`, `te-Latn-IN` | not published |
| Kannada | `train` | `kn-Knda-IN`, `kn-Latn-IN` | not published |
| Marathi | `train` | `mr-Deva-IN`, `mr-Latn-IN` | not published |
| Gujarati | `train` | `gu-Gujr-IN`, `gu-Latn-IN` | not published |

### STEM SFT

SFT-style STEM data used in Nemotron 3 Nano pretraining, refreshed rather than copied from the older SFT repo. English seed: 82.5B tokens, DeepSeek-R1-0528 and Qwen2.5-32B. CC BY 4.0.

| Language | Split | Configs | Size for this subset |
| --- | --- | --- | --- |
| Hindi | `train` | `hi-Deva-IN`, `hi-Latn-IN` | not published |
| Bengali | `train` | `bn-Beng-IN`, `bn-Latn-IN` | not published |
| Tamil | `train` | `ta-Taml-IN`, `ta-Latn-IN` | not published |
| Telugu | `train` | `te-Telu-IN`, `te-Latn-IN` | not published |
| Kannada | `train` | `kn-Knda-IN`, `kn-Latn-IN` | not published |
| Marathi | `train` | `mr-Deva-IN`, `mr-Latn-IN` | not published |
| Gujarati | `train` | `gu-Gujr-IN`, `gu-Latn-IN` | not published |

### Code concepts

Python problems and solutions built from combinations of programming-concept tags (algorithms, data structures, analytics, and so on). English seed: 7,294.5M tokens, gpt-oss-20b and gpt-oss-120b. CC BY 4.0. This is the largest specialized share in Table 3.2 (4.67%). ([Specialized-v1.1 card](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1.1); [code-concepts blog](https://huggingface.co/blog/nvidia/synthetic-code-concepts))

| Language | Split | Configs | Size for this subset |
| --- | --- | --- | --- |
| Hindi | `train` | `hi-Deva-IN`, `hi-Latn-IN` | not published |
| Bengali | `train` | `bn-Beng-IN`, `bn-Latn-IN` | not published |
| Tamil | `train` | `ta-Taml-IN`, `ta-Latn-IN` | not published |
| Telugu | `train` | `te-Telu-IN`, `te-Latn-IN` | not published |
| Kannada | `train` | `kn-Knda-IN`, `kn-Latn-IN` | not published |
| Marathi | `train` | `mr-Deva-IN`, `mr-Latn-IN` | not published |
| Gujarati | `train` | `gu-Gujr-IN`, `gu-Latn-IN` | not published |

### Multiple choice

Multiple-choice questions and answers on topics from MMLU `auxiliary_train`, generated with DeepSeek-v3 and Qwen3-235B-A22B. English seed: 1,609.2M tokens. CC BY 4.0, with a DeepSeek license note if a model trained on this subset is released.

| Language | Split | Configs | Size for this subset |
| --- | --- | --- | --- |
| Hindi | `train` | `hi-Deva-IN`, `hi-Latn-IN` | not published |
| Bengali | `train` | `bn-Beng-IN`, `bn-Latn-IN` | not published |
| Tamil | `train` | `ta-Taml-IN`, `ta-Latn-IN` | not published |
| Telugu | `train` | `te-Telu-IN`, `te-Latn-IN` | not published |
| Kannada | `train` | `kn-Knda-IN`, `kn-Latn-IN` | not published |
| Marathi | `train` | `mr-Deva-IN`, `mr-Latn-IN` | not published |
| Gujarati | `train` | `gu-Gujr-IN`, `gu-Latn-IN` | not published |

### Formal logic

Multiple-choice formal-logic items, with and without chain-of-thought: natural language to formal logic, the reverse, and truth-table problems. English seed: 128.0M tokens, Qwen3-235B-A22B-Thinking-2507. CC BY 4.0.

| Language | Split | Configs | Size for this subset |
| --- | --- | --- | --- |
| Hindi | `train` | `hi-Deva-IN`, `hi-Latn-IN` | not published |
| Bengali | `train` | `bn-Beng-IN`, `bn-Latn-IN` | not published |
| Tamil | `train` | `ta-Taml-IN`, `ta-Latn-IN` | not published |
| Telugu | `train` | `te-Telu-IN`, `te-Latn-IN` | not published |
| Kannada | `train` | `kn-Knda-IN`, `kn-Latn-IN` | not published |
| Marathi | `train` | `mr-Deva-IN`, `mr-Latn-IN` | not published |
| Gujarati | `train` | `gu-Gujr-IN`, `gu-Latn-IN` | not published |

### Economics

Multiple-choice economics questions and answers, with and without chain-of-thought. English seed: 73.4M tokens, Qwen3-235B-A22B-Thinking-2507. CC BY 4.0.

| Language | Split | Configs | Size for this subset |
| --- | --- | --- | --- |
| Hindi | `train` | `hi-Deva-IN`, `hi-Latn-IN` | not published |
| Bengali | `train` | `bn-Beng-IN`, `bn-Latn-IN` | not published |
| Tamil | `train` | `ta-Taml-IN`, `ta-Latn-IN` | not published |
| Telugu | `train` | `te-Telu-IN`, `te-Latn-IN` | not published |
| Kannada | `train` | `kn-Knda-IN`, `kn-Latn-IN` | not published |
| Marathi | `train` | `mr-Deva-IN`, `mr-Latn-IN` | not published |
| Gujarati | `train` | `gu-Gujr-IN`, `gu-Latn-IN` | not published |

### Unconditional algorithmic

Python samples in several formats from minimal prompts such as “Write a function.” English seed: 195.4M tokens, gpt-oss-120b and Qwen3-235B-A22B. CC BY 4.0. Smallest specialized share in Table 3.2 (0.06%).

| Language | Split | Configs | Size for this subset |
| --- | --- | --- | --- |
| Hindi | `train` | `hi-Deva-IN`, `hi-Latn-IN` | not published |
| Bengali | `train` | `bn-Beng-IN`, `bn-Latn-IN` | not published |
| Tamil | `train` | `ta-Taml-IN`, `ta-Latn-IN` | not published |
| Telugu | `train` | `te-Telu-IN`, `te-Latn-IN` | not published |
| Kannada | `train` | `kn-Knda-IN`, `kn-Latn-IN` | not published |
| Marathi | `train` | `mr-Deva-IN`, `mr-Latn-IN` | not published |
| Gujarati | `train` | `gu-Gujr-IN`, `gu-Latn-IN` | not published |

### RQA — absent from the sample

Long-form STEM reasoning questions. The generator reads a contiguous chunk of a topic-stratified STEM document, then writes a context-free reasoning trace and answer. English seed: 134.6B tokens. Table 3.2 says `specialized_v1_rqa` was dropped before sampling.

| Language | Split / config | Size |
| --- | --- | --- |
| Hindi, Bengali, Tamil, Telugu, Kannada, Marathi, Gujarati | absent from the published sample | not published |

### InfiniByte — absent from the sample

Cross-domain problems built by combining code, math, physics, chemistry, and other scientific material. English seed: 19.4B tokens. Not in Table 3.2.

| Language | Split / config | Size |
| --- | --- | --- |
| Hindi, Bengali, Tamil, Telugu, Kannada, Marathi, Gujarati | absent from the published sample | not published |

### Scientific coding — absent from the sample

Graduate- or research-level code-embedded articles and advanced Python problems, generated from Nemotron-CC STEM documents. English seed: 1.2B tokens. Not in Table 3.2. If any row were present it would carry CC BY-SA 4.0 and GFDL 1.3. The sample does not include it.

| Language | Split / config | Size |
| --- | --- | --- |
| Hindi, Bengali, Tamil, Telugu, Kannada, Marathi, Gujarati | absent from the published sample | not published |

## 4. How specialized differs from the translated crawl

The report’s sample has two groups. Specialized is the eight rows above (13.32% of the English sampling target). The crawl-side rows are the rest (86.68%):

| Report subset id | Share | What the English source is | Where the Indic card puts it |
| --- | ---: | --- | --- |
| `cc_v2_diverse_qa` | 40.40% | Synthetic diverse question-answer from Common Crawl. The largest slice. Nemotron-CC-v2 config `Diverse-QA`. | Named seed of gated CC-v1 (`Nemotron-CC-v2`) |
| `pretraining_sft_v1` | 12.03% | SFT-style code, general, and math. Repo configs `Nemotron-SFT-Code`, `Nemotron-SFT-General`, `Nemotron-SFT-MATH`. | In Table 3.2 only. Not named on either Indic card. |
| `cc_v2_english_cc` | 9.56% | English Common Crawl web text in the Nemotron-CC-v2 quality tiers. | Named seed of gated CC-v1 |
| `cc_math_v1_4plus` | 8.65% | Nemotron-CC-Math-v1 config `4plus`: math extracted from Common Crawl, equations kept and rendered as LaTeX. | In Table 3.2 only. Not named on either Indic card. |
| `cc_v21_hq_synthetic` | 7.46% | Synthetic rephrases of high-quality Nemotron-CC-v2.1 web text. | Named seed of gated CC-v1 (`Nemotron-CC-v2.1`) |
| `cc_v21_hq_organic` | 5.59% | High-quality organic web text in Nemotron-CC-v2.1. | Named seed of gated CC-v1 |
| `cc_v21_hq_dqa` | 2.99% | High-quality diverse QA in Nemotron-CC-v2.1 (`High-Quality-DQA`). | Named seed of gated CC-v1 |

The Nemotron-CC-v2 card’s own English inventory, which is the pre-Indic collection and not an Indic count, is 6,585.8B tokens: English Common Crawl 3,359.8B, synthetic crawl 1,257.3B, Diverse QA 692.9B, translated Diverse QA 558.2B, math 206.2B, math SFT 190.6B, synthetic code 174.9B, MMLU SFT 81.6B, code SFT 58.5B, general SFT 5.7B. ([Nemotron-CC-v2 card](https://huggingface.co/datasets/nvidia/Nemotron-CC-v2))

Practical differences:

- **Access.** Specialized Indic is public. CC-v1 is the gated agreement. An approval on CC-v1 does not change the specialized license, and the specialized download does not include the crawl.
- **Seeds.** Specialized Indic is only Specialized-v1 and v1.1. CC-v1’s card names Nemotron-CC-v2, Nemotron-CC-v2.1, and FinePDFs-edu. Diverse QA and web text are on the gated side. Code-concepts, unconditional algorithms, STEM SFT, and math *textbooks* are on the open side. The older SFT repo, CC-Math `4plus`, and the GitHub code repos are in a third state: present in the report’s sample or in the English collection, but not named on either Indic card.
- **Text.** Crawl rows are translated web pages, crawl-derived QA, and, on the card, educational PDFs. Specialized rows are translated synthetic textbooks, rewritten Wikipedia, STEM SFT, concept-seeded Python, logic, economics, and MMLU-style questions. Code, equations, URLs, and file paths are supposed to be left intact.
- **Size.** On the cards, specialized is 295.8B output tokens and CC-v1 is 2,155.8B. The report’s full mix is 2,825.6B. For these seven languages the open specialized native-script slices are 16.5B to 21.8B output tokens each, against report totals of 138.9B to 196.4B for the same native configs across the whole corpus.
- **License.** Specialized records are CC BY 4.0, except Wiki-Rewrite (and Scientific-Coding, which was not sampled) under CC BY-SA 4.0 and GFDL. CC-v1 is the NVIDIA training agreement, plus ODC-By for FinePDFs rows.
- **Pipeline.** Same twelve-language maker, checker, and rewriter for every source that entered that workflow: translate with Gemma-4-31B-it (mostly the RedHat FP8 checkpoint), keep scores of at least 75, rewrite once below that, then romanize a subset. The ten lower-resource languages use Bodhan Indic Translate, no rewrite, and no romanization. Those ten are outside these seven.

## Sources

- [Scaling Indic Pretraining: 2.8 Trillion Tokens and an Open Data Generation Pipeline](https://huggingface.co/blog/nvidia/scaling-indic-pretraining) (16 October 2026)
- [Scaling Synthetic Pre-training Data and Evaluation for Indic LLMs](https://arxiv.org/html/2610.26006) (arXiv:2610.26006; PDF also at [nvidia/nemotron-indic-pretraining-report](https://huggingface.co/datasets/nvidia/nemotron-indic-pretraining-report))
- [nvidia/Nemotron-Pretraining-Indic-Specialized-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Indic-Specialized-v1) (card; repo created 26 October 2026, modified 29 October 2026)
- [nvidia/Nemotron-Pretraining-Indic-CC-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Indic-CC-v1) (card text on the dataset page; files gated; modified 29 October 2026)
- [nvidia/Nemotron-Pretraining-Specialized-v1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1)
- [nvidia/Nemotron-Pretraining-Specialized-v1.1](https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1.1)
- [nvidia/Nemotron-CC-v2](https://huggingface.co/datasets/nvidia/Nemotron-CC-v2)
- [Code Concepts: A Large-Scale Synthetic Dataset Generated from Programming Concept Seeds](https://huggingface.co/blog/nvidia/synthetic-code-concepts)
