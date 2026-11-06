"""Load docs/hf-tokenizer with the stock Hugging Face tokenizer.

Transformers and vLLM read that directory. This module does not implement
a grapheme encoder and does not vendor a second vocabulary.
"""

from __future__ import annotations

from pathlib import Path

_default: Tokenizer | None = None


def stock_dir() -> Path:
    """The docs/hf-tokenizer directory next to this package in the store."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "docs" / "hf-tokenizer"
        if (candidate / "tokenizer.json").is_file() and (candidate / "tokenizer_config.json").is_file():
            return candidate
    raise RuntimeError("docs/hf-tokenizer was not found. Pass that directory to load().")


def json_path() -> Path:
    """tokenizer.json inside the stock Hugging Face directory."""
    return stock_dir() / "tokenizer.json"


class Tokenizer:
    """Stock fast tokenizer. encode returns ids. decode returns text."""

    def __init__(self, backend) -> None:
        self._backend = backend

    def encode(self, text: str) -> list[int]:
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        return list(self._backend.encode(text, add_special_tokens=False))

    def decode(self, ids) -> str:
        if isinstance(ids, (str, bytes)) or not hasattr(ids, "__iter__"):
            raise TypeError("ids must be a sequence of ints")
        seq: list[int] = []
        for item in ids:
            if isinstance(item, bool) or not isinstance(item, int):
                raise TypeError("ids must be a sequence of ints")
            seq.append(item)
        return self._backend.decode(seq, skip_special_tokens=False)

    def tokenize(self, text: str) -> list[str]:
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        return list(self._backend.tokenize(text))


def load(path: str | Path | None = None) -> Tokenizer:
    """Load docs/hf-tokenizer, or another directory with the same files.

    Uses AutoTokenizer.from_pretrained. vLLM reads this same directory.
    """
    global _default
    if path is None and _default is not None:
        return _default
    directory = stock_dir() if path is None else Path(path)
    if not directory.is_dir():
        raise RuntimeError(f"{directory} is not the docs/hf-tokenizer directory")
    tokenizer_json = directory / "tokenizer.json"
    if not tokenizer_json.is_file() or not (directory / "tokenizer_config.json").is_file():
        raise RuntimeError(f"{directory} is not a Hugging Face tokenizer directory")
    from transformers import AutoTokenizer

    backend = AutoTokenizer.from_pretrained(str(directory))
    tok = Tokenizer(backend)
    if path is None:
        _default = tok
    return tok


def encode(text: str) -> list[int]:
    """Encode text with the stock tokenizer in docs/hf-tokenizer."""
    return load().encode(text)


def decode(ids) -> str:
    """Decode ids with the stock tokenizer in docs/hf-tokenizer."""
    return load().decode(ids)
