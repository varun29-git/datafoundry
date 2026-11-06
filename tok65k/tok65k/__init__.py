"""Load the stock Hugging Face tokenizer in docs/hf-tokenizer."""

from tok65k.encoder import Tokenizer, decode, encode, json_path, load, stock_dir

__all__ = [
    "Tokenizer",
    "decode",
    "encode",
    "json_path",
    "load",
    "stock_dir",
]

__version__ = "1.0.0"
