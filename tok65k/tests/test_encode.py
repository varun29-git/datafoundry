"""Stock tokenizer and Encoder.encode agree, and grapheme is not in the spec."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import types
import unittest
from pathlib import Path

STORE = Path(__file__).resolve().parents[2]
PROJECT = Path(__file__).resolve().parents[1]
SOURCE_JSON = STORE / "docs" / "tokenizer-65k.json"
BUILD = STORE / "internal" / "build-65k.py"
HF_DIR = STORE / "docs" / "hf-tokenizer"

FOUR = ("नमस्ते", "हिन्दी", "ಕನ್ನಡ", "English शब्द")
HINDI = ["\u0120ह", "िन्", "दी"]


def _reference():
    for name in ("pyarrow", "pyarrow.fs", "pyarrow.parquet", "sentencepiece"):
        sys.modules.setdefault(name, types.ModuleType(name))
    spec = importlib.util.spec_from_file_location("build65k_ref", BUILD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EncodeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(PROJECT))
        from tok65k import encode, load, stock_dir
        from tokenizers import Tokenizer

        cls.load = staticmethod(load)
        cls.encode = staticmethod(encode)
        cls.stock_dir = staticmethod(stock_dir)
        cls.tok = load()
        cls.fast = Tokenizer.from_file(str(HF_DIR / "tokenizer.json"))
        cls.ref = _reference().load_runtime(str(SOURCE_JSON))
        cls.doc = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))

    def pieces(self, ids):
        return [self.doc["pieces"][i] for i in ids]

    def test_grapheme_is_gone_from_tokenizer_spec(self):
        spec = self.doc["tokenizer_spec"]
        self.assertNotIn("grapheme", spec)
        self.assertEqual(spec["indic"]["atoms"], "characters")
        self.assertNotIn("grapheme", BUILD.read_text(encoding="utf-8"))
        self.assertFalse((PROJECT / "tok65k" / "tokenizer-65k.json").exists())

    def test_four_strings_match_stock_and_encoder(self):
        for text in FOUR:
            ids = self.tok.encode(text)
            self.assertEqual(ids, self.encode(text), text)
            self.assertEqual(ids, self.ref.encode(text), text)
            self.assertEqual(ids, self.fast.encode(text).ids, text)
            self.assertEqual(self.tok.tokenize(text), self.fast.encode(text).tokens, text)
            self.assertEqual(self.pieces(ids), self.fast.encode(text).tokens, text)

    def test_hindi_is_the_sarvam_cut(self):
        stock = self.fast.encode("हिन्दी").tokens
        encoder = self.pieces(self.ref.encode("हिन्दी"))
        package = self.tok.tokenize("हिन्दी")
        self.assertEqual(stock, HINDI)
        self.assertEqual(encoder, HINDI)
        self.assertEqual(package, HINDI)
        self.assertEqual(self.tok.decode(self.tok.encode("हिन्दी")), "हिन्दी")

    def test_stock_dir_is_the_hf_directory(self):
        self.assertEqual(self.stock_dir(), HF_DIR)

    def test_cli_encode_and_decode(self):
        env = dict(**{k: v for k, v in __import__("os").environ.items()})
        env["PYTHONPATH"] = str(PROJECT) + (":" + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
        encoded = subprocess.run(
            [sys.executable, "-m", "tok65k", "encode", "English", "शब्द"],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(encoded.returncode, 0, encoded.stderr)
        ids = json.loads(encoded.stdout)
        self.assertEqual(ids, self.ref.encode("English शब्द"))
        decoded = subprocess.run(
            [sys.executable, "-m", "tok65k", "decode", *[str(i) for i in ids]],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(decoded.returncode, 0, decoded.stderr)
        self.assertEqual(decoded.stdout.rstrip("\n"), "English शब्द")

    def test_load_rejects_a_directory_without_the_stock_files(self):
        with self.assertRaises(RuntimeError):
            self.load(PROJECT / "tests")


if __name__ == "__main__":
    unittest.main()
