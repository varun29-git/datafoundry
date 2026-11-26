# Tokenizer deployment

Load the directory `docs/hf-tokenizer` with the stock fast tokenizer. That directory is what transformers and vLLM read. Indic text is Sarvam score BPE: characters are the atoms, and the highest `indic_score` merges first. `हिन्दी` is `Ġह` | `िन्` | `दी`. There is no grapheme pre-segmentation in this path.

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("docs/hf-tokenizer")
ids = tok.encode("हिन्दी", add_special_tokens=False)
```

`tokenizers` 0.23.2 loads the same file with `Tokenizer.from_file("docs/hf-tokenizer/tokenizer.json")`. Transformers 5.18.0 returns `TokenizersBackend`. The JSON uses stock components only: `NFC`, `Replace`, `Split`, `BPE` with `byte_fallback`, and a decoder sequence of `ByteFallback`, `Fuse`, `ByteLevel`, and `Replace`. That is the Rust tokenizer vLLM reads. Point vLLM at this directory; it does not need a custom Python encoder.

The package `tok65k` only finds that directory and calls the same stock tokenizer. It does not vendor a second vocabulary, and it does not cut on grapheme clusters.

```python
from tok65k import load

tok = load()  # AutoTokenizer on docs/hf-tokenizer
```

```bash
python -m tok65k encode हिन्दी
python -m tok65k encode English शब्द
```

`encode` prints a JSON list of ids. Separate words are joined with one space, so `encode English शब्द` is the line `English शब्द`. Piece strings and ids stay the `pieces` array in `docs/tokenizer-65k.json`: 65,536 ids, unchanged. The match against `Encoder.encode` is recorded in `docs/tokenizer-hf.md`.
