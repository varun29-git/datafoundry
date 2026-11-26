# Data rights and provenance

## Scope

Apache-2.0 in `LICENSE` applies to the repository's original code. It does not relicense source corpora, quoted dataset text, upstream models or tokenizers, or third-party components of derived tokenizer artifacts. Access to a dataset, generation of a derivative, calculation of token counts, and redistribution rights are separate questions.

This repository contains research notes, aggregate counts, and small excerpts recorded during checks. It does not contain the source training corpora. It excludes both original and derived Sarvam tokenizer artifacts: no original Sarvam `tokenizer.model` or tokenizer JSON, no `docs/hf-tokenizer/` export, and no `docs/tokenizer-65k*.json` derived vocabulary is included.

The notes are historical evidence, not a complete rights audit of every upstream row. Follow the license and attribution information attached to the exact upstream revision before using or redistributing any data or derivative.

## CC BY 4.0 material

The [Nemotron Indic Specialized study](docs/nemotron-indic-specialized.md) records that Specialized-v1.1 and most Specialized-v1 subsets are offered under Creative Commons Attribution 4.0. This includes the mapped Math-Textbooks, STEM-SFT, Code-Concepts, Multiple-Choice, Formal-Logic, Economics, and Unconditional-Algorithmic material, subject to the exact dataset card and record provenance.

CC BY requires appropriate attribution, a license link, and an indication of changes. It does not remove other notices or permit a claim of upstream endorsement. The Apache code license is not a substitute for those attribution obligations.

Upstream references:

- <https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1>
- <https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Specialized-v1.1>
- <https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Indic-Specialized-v1>
- <https://creativecommons.org/licenses/by/4.0/>

## Share-alike material

Wiki-Rewrite and Scientific-Coding records are identified in the upstream Indic Specialized card as carrying **CC BY-SA 4.0 and GFDL 1.3** terms rather than the CC BY 4.0 terms used by most specialized subsets. Scientific-Coding was absent from the published sample discussed in the source study, but its conditional terms still matter if encountered in another revision.

Share-alike and documentation-license obligations continue to apply to covered adaptations and distributions. They are not converted into Apache-2.0 by inclusion in a curriculum, translation, tokenization, or derived dataset. Preserve source notices and evaluate the exact redistribution obligations before publishing such material.

References:

- <https://creativecommons.org/licenses/by-sa/4.0/>
- <https://www.gnu.org/licenses/fdl-1.3.html>

## Gated and restricted-access data

Nemotron-Pretraining-Indic-CC-v1 is manually gated and uses the NVIDIA Data Agreement for Model Training identified by its dataset card. The notes also identify FinePDFs-edu rows as carrying ODC Attribution License obligations. Several English seed datasets have their own gates and agreements.

Accepting a gate or obtaining credentials grants only the rights in the applicable agreement; it does not imply permission to redistribute raw data, derived rows, or token payloads in this repository. No gated corpus is bundled here. Do not use the generalized historical storage prefixes in the notes as an access mechanism or as provenance for a new redistribution.

References:

- <https://huggingface.co/datasets/nvidia/Nemotron-Pretraining-Indic-CC-v1>
- <https://huggingface.co/datasets/HuggingFaceFW/finepdfs-edu>

## Generated and synthetic data terms

Generated text is not a separate public-domain category. The applicable terms can combine the dataset card, source-record license, generating-model license, and use restrictions. Preserve fields such as `_source_repo`, `_source_config`, `_subset_key`, and `_source_file` when deriving data.

For example, the source study records a DeepSeek license notice for Multiple-Choice when a model trained on that subset is released. Other synthetic material may carry different generator-specific notices. Cosmopedia, Sangraha, FineWeb-2, IndicCorp, translations, rewrites, and code-generation outputs must be checked under their own exact upstream terms; this document does not assign them all one license.

Token counts and encode/decode observations are measurements about those sources, not permission to distribute the underlying text. Model-quality claims must not be inferred from synthetic-data provenance or tokenizer fertility.

## Sarvam Research License and tokenizer derivatives

The historical research notes mark the original Sarvam tokenizer material as licensed by Sarvam AI under the Sarvam AI Research License. They state that Indic piece strings were retained in the derived experiments and that the result was not an official Sarvam product.

The Apache-2.0 code license does not replace or broaden those terms. Original and derived Sarvam tokenizer artifacts are excluded from this repository, including `docs/hf-tokenizer/` and `docs/tokenizer-65k*.json`. The freeze, deployment, and compatibility notes remain only as historical research records; they do not include the derived vocabulary or Hugging Face export.

Because those artifacts are excluded, their redistribution clearance is not a publication blocker for this repository. Do not restore or fetch them to run the tests. `TOK65K_SARVAM_TOKENIZER_DIR` is an optional local integration-test input only; supplying a path does not grant redistribution rights. Anyone separately generating, obtaining, using, or redistributing a derived tokenizer must review the Sarvam Research License, preserve required notices, and confirm that the intended activity is permitted. Dataset and tokenizer rights must be assessed independently.
