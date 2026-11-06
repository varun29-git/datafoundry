# Indic specialized native segment counts

Document rows already stored under `s3://nemotron-training-data-us-east-1/datasets/nemotron-indic-specialized-v1/` for the seven native configs. Latin configs were not scanned.

Counted at 2026-10-31 10:24:49 UTC+05:30 (Asia/Calcutta) by projecting `_source_repo`, `_source_config`, and `_subset_key` from each parquet file. The text column was not read. Nothing was tokenized. No token count is given.

Language is the config folder. Segment is `_source_repo`. Subsegment is `_source_config`. One document is one parquet row.

Files scanned: 5,089 of 5,089. Failed files: 0.

## Documents by language, segment, and subsegment

| Language | Segment | Subsegment | `_subset_key` | Documents |
|---|---|---|---|---:|
| `hi-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Math-Textbooks` | `specialized_v1_math_textbooks` | 2,799,946 |
| `hi-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-RQA` | `specialized_v1_rqa` | 124,445 |
| `hi-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-STEM-SFT` | `specialized_v1_stem_sft` | 1,546,230 |
| `hi-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Wiki-Rewrite` | `specialized_v1_wiki_rewrite` | 2,313,790 |
| `hi-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Code-Concepts` | `specialized_v11_code_concepts` | 4,047,495 |
| `hi-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Economics` | `specialized_v11_economics` | 91,623 |
| `hi-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Formal-Logic` | `specialized_v11_formal_logic` | 130,527 |
| `hi-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Multiple-Choice` | `specialized_v11_multiple_choice` | 939,071 |
| `hi-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `specialized_v11_unconditional_algo` | 48,260 |
| `bn-Beng-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Math-Textbooks` | `specialized_v1_math_textbooks` | 2,695,087 |
| `bn-Beng-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-RQA` | `specialized_v1_rqa` | 98,742 |
| `bn-Beng-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-STEM-SFT` | `specialized_v1_stem_sft` | 1,513,230 |
| `bn-Beng-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Wiki-Rewrite` | `specialized_v1_wiki_rewrite` | 2,250,486 |
| `bn-Beng-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Code-Concepts` | `specialized_v11_code_concepts` | 3,964,790 |
| `bn-Beng-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Economics` | `specialized_v11_economics` | 89,731 |
| `bn-Beng-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Formal-Logic` | `specialized_v11_formal_logic` | 127,997 |
| `bn-Beng-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Multiple-Choice` | `specialized_v11_multiple_choice` | 916,373 |
| `bn-Beng-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `specialized_v11_unconditional_algo` | 29,078 |
| `ta-Taml-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Math-Textbooks` | `specialized_v1_math_textbooks` | 2,746,513 |
| `ta-Taml-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-RQA` | `specialized_v1_rqa` | 92,137 |
| `ta-Taml-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-STEM-SFT` | `specialized_v1_stem_sft` | 1,518,399 |
| `ta-Taml-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Wiki-Rewrite` | `specialized_v1_wiki_rewrite` | 2,175,219 |
| `ta-Taml-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Code-Concepts` | `specialized_v11_code_concepts` | 4,027,708 |
| `ta-Taml-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Economics` | `specialized_v11_economics` | 90,057 |
| `ta-Taml-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Formal-Logic` | `specialized_v11_formal_logic` | 126,155 |
| `ta-Taml-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Multiple-Choice` | `specialized_v11_multiple_choice` | 911,182 |
| `ta-Taml-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `specialized_v11_unconditional_algo` | 47,985 |
| `te-Telu-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Math-Textbooks` | `specialized_v1_math_textbooks` | 2,832,421 |
| `te-Telu-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-RQA` | `specialized_v1_rqa` | 99,157 |
| `te-Telu-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-STEM-SFT` | `specialized_v1_stem_sft` | 1,535,803 |
| `te-Telu-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Wiki-Rewrite` | `specialized_v1_wiki_rewrite` | 2,266,841 |
| `te-Telu-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Code-Concepts` | `specialized_v11_code_concepts` | 4,043,867 |
| `te-Telu-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Economics` | `specialized_v11_economics` | 91,091 |
| `te-Telu-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Formal-Logic` | `specialized_v11_formal_logic` | 127,651 |
| `te-Telu-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Multiple-Choice` | `specialized_v11_multiple_choice` | 924,241 |
| `te-Telu-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `specialized_v11_unconditional_algo` | 48,041 |
| `kn-Knda-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Math-Textbooks` | `specialized_v1_math_textbooks` | 2,505,951 |
| `kn-Knda-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-RQA` | `specialized_v1_rqa` | 84,121 |
| `kn-Knda-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-STEM-SFT` | `specialized_v1_stem_sft` | 1,265,325 |
| `kn-Knda-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Wiki-Rewrite` | `specialized_v1_wiki_rewrite` | 2,128,513 |
| `kn-Knda-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Code-Concepts` | `specialized_v11_code_concepts` | 3,921,232 |
| `kn-Knda-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Economics` | `specialized_v11_economics` | 87,277 |
| `kn-Knda-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Formal-Logic` | `specialized_v11_formal_logic` | 126,297 |
| `kn-Knda-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Multiple-Choice` | `specialized_v11_multiple_choice` | 890,319 |
| `kn-Knda-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `specialized_v11_unconditional_algo` | 47,401 |
| `mr-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Math-Textbooks` | `specialized_v1_math_textbooks` | 2,684,908 |
| `mr-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-RQA` | `specialized_v1_rqa` | 100,079 |
| `mr-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-STEM-SFT` | `specialized_v1_stem_sft` | 1,438,491 |
| `mr-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Wiki-Rewrite` | `specialized_v1_wiki_rewrite` | 2,299,390 |
| `mr-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Code-Concepts` | `specialized_v11_code_concepts` | 4,049,578 |
| `mr-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Economics` | `specialized_v11_economics` | 91,518 |
| `mr-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Formal-Logic` | `specialized_v11_formal_logic` | 130,239 |
| `mr-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Multiple-Choice` | `specialized_v11_multiple_choice` | 936,117 |
| `mr-Deva-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `specialized_v11_unconditional_algo` | 48,251 |
| `gu-Gujr-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Math-Textbooks` | `specialized_v1_math_textbooks` | 2,718,596 |
| `gu-Gujr-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-RQA` | `specialized_v1_rqa` | 93,403 |
| `gu-Gujr-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-STEM-SFT` | `specialized_v1_stem_sft` | 1,441,229 |
| `gu-Gujr-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1` | `Nemotron-Pretraining-Wiki-Rewrite` | `specialized_v1_wiki_rewrite` | 2,282,188 |
| `gu-Gujr-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Code-Concepts` | `specialized_v11_code_concepts` | 4,003,739 |
| `gu-Gujr-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Economics` | `specialized_v11_economics` | 91,156 |
| `gu-Gujr-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Formal-Logic` | `specialized_v11_formal_logic` | 129,914 |
| `gu-Gujr-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Multiple-Choice` | `specialized_v11_multiple_choice` | 931,197 |
| `gu-Gujr-IN` | `nvidia/Nemotron-Pretraining-Specialized-v1.1` | `Nemotron-Pretraining-Unconditional-Algorithmic` | `specialized_v11_unconditional_algo` | 47,288 |

## Totals per language

| Language | Files | Documents |
|---|---:|---:|
| `hi-Deva-IN` | 634 | 12,041,387 |
| `bn-Beng-IN` | 675 | 11,685,514 |
| `ta-Taml-IN` | 727 | 11,735,355 |
| `te-Telu-IN` | 767 | 11,969,113 |
| `kn-Knda-IN` | 855 | 11,056,436 |
| `mr-Deva-IN` | 687 | 11,778,571 |
| `gu-Gujr-IN` | 744 | 11,738,710 |
| **All seven** | **5,089** | **82,005,086** |

## Segments present

A segment is a distinct `_source_repo` value.

- `nvidia/Nemotron-Pretraining-Specialized-v1`
- `nvidia/Nemotron-Pretraining-Specialized-v1.1`

No language is missing a segment. Every native folder contains the same set of `_source_repo` values.

No language is missing a subsegment. Every native folder contains the same set of `_source_config` values.

## `_subset_key`

- `Nemotron-Pretraining-Code-Concepts` maps to 1 `_subset_key` value(s): `specialized_v11_code_concepts`.
- `Nemotron-Pretraining-Economics` maps to 1 `_subset_key` value(s): `specialized_v11_economics`.
- `Nemotron-Pretraining-Formal-Logic` maps to 1 `_subset_key` value(s): `specialized_v11_formal_logic`.
- `Nemotron-Pretraining-Math-Textbooks` maps to 1 `_subset_key` value(s): `specialized_v1_math_textbooks`.
- `Nemotron-Pretraining-Multiple-Choice` maps to 1 `_subset_key` value(s): `specialized_v11_multiple_choice`.
- `Nemotron-Pretraining-RQA` maps to 1 `_subset_key` value(s): `specialized_v1_rqa`.
- `Nemotron-Pretraining-STEM-SFT` maps to 1 `_subset_key` value(s): `specialized_v1_stem_sft`.
- `Nemotron-Pretraining-Unconditional-Algorithmic` maps to 1 `_subset_key` value(s): `specialized_v11_unconditional_algo`.
- `Nemotron-Pretraining-Wiki-Rewrite` maps to 1 `_subset_key` value(s): `specialized_v1_wiki_rewrite`.
