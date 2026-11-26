# DataFoundry

DataFoundry is a general research workspace for multilingual pretraining-data engineering: curriculum arithmetic, source mapping, tokenizer experiments, token censuses, integrity checks, and small reusable utilities. Its reference study covers English plus Hindi, Bengali, Tamil, Telugu, Kannada, Marathi, and Gujarati.

This is **not a trained-model release, a complete packed corpus, or a redistribution of the source datasets**. Most documents are dated research logs; the final curriculum supersedes earlier drafts where they disagree. In the public notes, cloud locations and account-specific details have been generalized, while the technical measurements and negative results are retained.

## Development timeline

| Date | Milestone |
| --- | --- |
| September 2026 | Multilingual source mapping, curriculum research, and 65K-tokenizer experiments developed. |
| October 2026 | Native/Romanized Indic token censuses, integrity checks, and the proposed one-trillion-token curriculum consolidated. |
| **27 November 2026** | **Research notes, reusable utilities, synthetic tests, and provenance published as the first open-source release under Apache-2.0; restricted tokenizer artifacts excluded.** |

## Research map

### Curriculum and source mapping

- [Final one-trillion-token curriculum](docs/one-trillion-curriculum.md) proposes 500B English tokens and 500B Indic tokens, split into warmup, stable, and decay phases. These are exact budget calculations, not evidence that a 1T-token training run occurred.
- [Multilingual batch-packing specification](docs/multilingual-batch-packing.md) defines language/source-homogeneous sequences, phase quotas, document spans, `<eod>`/`<pad>` handling, and required intra-document attention masking.
- [Nemotron Indic Specialized source study](docs/nemotron-indic-specialized.md) maps upstream Specialized-v1/v1.1 STEM, math, code, logic, economics, and rewritten-Wikipedia sources to native-script and Romanized configurations. Romanized means Indic text in Latin script, not an English translation; native and Romanized rows are not assumed to be paired documents.
- [Stored segment layout](docs/indic-specialized-segment-layout.md) and [segment document census](docs/indic-specialized-segment-counts.md) record the actual nine source configurations and eighteen native/Romanized subsegment streams used by this study.

### Token censuses

These are historical counts of stored token artifacts, not bundled data and not model-quality measurements.

| Census | Recorded scope | Result |
| --- | --- | ---: |
| [Indic Specialized](docs/indic-specialized-token-counts.md) | 14 language-script configurations, 8,768 indexes | 142,351,065,175 tokens; 88,275,650 documents |
| Native-script Specialized | Seven languages | 129,572,309,439 tokens |
| Romanized Specialized | Seven languages | 12,778,755,736 tokens |
| [FineWeb-2, IndicCorp v2, Sangraha verified](docs/indic-other-token-counts.md) | Native-script stored bins | 96,043,927,930 tokens |
| [Indic CC included slices](docs/indic-cc-token-counts.md) | 46,141 source files; exclusions stated in the note | 750,022,728,096 tokens |
| [Restored High-Quality-DQA](docs/indic-cc-dqa-token-counts.md) | Seven languages | 25,546,894,943 tokens |
| [FineWeb-2 Latin](docs/indic-fineweb2-latin-token-counts.md) | Seven Latin-script prefixes | 311,404,717 tokens |

The curriculum uses source-specific draws from these pools; the table must not be summed into a claimed trained-token total. Each report documents its date, inclusion rules, holdouts, and known gaps.

### Tokenizer research and checks

- [Tokenizer explanation](docs/tokenizer-explained.md), [freeze record](docs/tokenizer-65k-freeze.md), and [stock Hugging Face export checks](docs/tokenizer-hf.md) describe the 65,536-token BPE experiments, routing rules, fertility measurements, and encode/decode gates.
- [Dataset round-trip smoke tests](docs/dataset-roundtrip-smoke.md) and [Indic Specialized stored-id checks](docs/indic-specialized-roundtrip.md) preserve both passing checks and mismatches. In the latter, 56 of 56 sampled stored-id spans matched a fresh stock encode; that does not imply lossless text decoding.
- Known limitations remain: three of 35 tokenizer fixtures differ between the Python reference and stock export, and decoder gaps include a leftover `Ċ` in `राम\nश्याम` and a spurious space in `C++में`. NFC and punctuation folding also mean exact source-text round trips are not universal.
- [Validation contract](docs/validation-contract.md) records the intended holdout and evaluation rules. It is a contract and readiness analysis, not a completed validation result.

No original Sarvam `tokenizer.model` or original Sarvam tokenizer JSON is included. Derived Sarvam tokenizer artifacts are also **excluded**: `docs/tokenizer-65k*.json` and `docs/hf-tokenizer/` are not included. Historical notes describe those experiments, but the repository and its tests do not contain or require the derived vocabularies or exports. See [DATA_PROVENANCE.md](DATA_PROVENANCE.md).

## Incomplete components and non-results

The repository does **not** establish production training readiness:

- The sequence packer, packed-shard manifest, batch loader, and block-diagonal attention integration are specified but not implemented and tested here. No complete packed 1T corpus is included.
- The mass-tokenization pass and remaining source work are unfinished; the task log still lists tokenization work, and the final curriculum records an RQA top-up and other availability gaps.
- Validation exclusions have not been shown to be applied to the actual packed corpus with an auditable provenance trail. The referenced external validation manifests/scoring code are not included, and the validation note identifies missing cells and hardware-dependent work.
- Tokenizer deployment gaps and the documented normalization/decode mismatches are not all resolved.
- There are **no model-quality results**: no trained checkpoint, downstream benchmark results, model perplexity comparison, or evidence that the proposed curriculum improves a model. Token fertility and data-integrity checks are not model-quality evaluations.

## `tok65k` utility and tests

`tok65k` is a thin loader/CLI around a Hugging Face tokenizer directory. Its unit tests build a tiny synthetic BPE fixture locally; they neither need nor fetch a real Sarvam tokenizer, dataset, credential, or cloud resource.

From the repository root, with Python 3.11 or newer:

```bash
python -m pip install -e './tok65k[dev]'
python -m unittest discover -s tok65k/tests -v
ruff check --config tok65k/pyproject.toml tok65k internal/build-65k.py
```

Use an explicit tokenizer directory when running the utility:

```bash
python -m tok65k encode --dir /path/to/hf-tokenizer 'हिन्दी'
python -m tok65k decode --dir /path/to/hf-tokenizer 123 456
```

An optional integration test compares a user-supplied real Sarvam-derived Hugging Face tokenizer with its raw stock backend:

```bash
TOK65K_SARVAM_TOKENIZER_DIR=/path/to/hf-tokenizer \
  python -m unittest discover -s tok65k/tests -v
```

When that variable is absent, the integration test is skipped with an explicit reason. Do not commit the supplied tokenizer or use the test path to bypass its license.

## License and provenance

Original code is available under [Apache-2.0](LICENSE). That license does **not** relicense datasets, dataset excerpts, upstream tokenizer material, or any external derived artifacts. [DATA_PROVENANCE.md](DATA_PROVENANCE.md) separates attribution, share-alike, gated-data, generated-data, and Sarvam Research License obligations and records the exclusion of original and derived Sarvam tokenizer artifacts.
