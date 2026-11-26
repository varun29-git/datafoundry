"""Unit tests use a synthetic BPE; real Sarvam integration is opt-in."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

PROJECT = Path(__file__).resolve().parents[1]
SARVAM_DIR = os.environ.get("TOK65K_SARVAM_TOKENIZER_DIR")

FOUR = ("नमस्ते", "हिन्दी", "ಕನ್ನಡ", "English शब्द")
HINDI = ["Ġह", "िन्", "दी"]


def _write_minimal_fixture(directory: Path) -> None:
    from tokenizers import Tokenizer, decoders, models, normalizers, pre_tokenizers

    pieces = [
        "<unk>",
        "<s>",
        "</s>",
        "<pad>",
        "E",
        "n",
        "g",
        "l",
        "i",
        "s",
        "h",
        "Ġ",
        "ह",
        "ि",
        "न",
        "्",
        "द",
        "ी",
        "श",
        "ब",
        "क",
        "म",
        "स",
        "त",
        "े",
        "ಕ",
        "ನ",
        "್",
        "ಡ",
        "ಮ",
        "ಸ",
        "ತ",
        "ೆ",
        "En",
        "Eng",
        "li",
        "lis",
        "lish",
        "िन",
        "िन्",
        "दी",
        "शब",
        "शब्",
        "शब्द",
        "Ġह",
        "Ġशब्द",
        "ĠE",
        "ĠEn",
        "ĠEng",
        "ĠEngl",
        "ĠEngli",
        "ĠEnglis",
        "ĠEnglish",
    ]
    vocab = {piece: index for index, piece in enumerate(pieces)}
    merge_strings = [
        "E n",
        "En g",
        "l i",
        "li s",
        "lis h",
        "Ġ ह",
        "ि न",
        "िन ्",
        "द ी",
        "श ब",
        "शब ्",
        "शब् द",
        "Ġ शब्द",
        "Ġ E",
        "ĠE n",
        "ĠEn g",
        "ĠEng l",
        "ĠEngl i",
        "ĠEngli s",
        "ĠEnglis h",
    ]
    merges = [tuple(item.split(" ", 1)) for item in merge_strings]
    tokenizer = Tokenizer(models.BPE(vocab=vocab, merges=merges, unk_token="<unk>"))
    tokenizer.normalizer = normalizers.NFC()
    tokenizer.pre_tokenizer = pre_tokenizers.Metaspace(replacement="Ġ", prepend_scheme="always")
    tokenizer.decoder = decoders.Metaspace(replacement="Ġ", prepend_scheme="always")
    directory.mkdir(parents=True, exist_ok=True)
    tokenizer.save(str(directory / "tokenizer.json"))
    config = {
        "tokenizer_class": "PreTrainedTokenizerFast",
        "unk_token": "<unk>",
        "bos_token": "<s>",
        "eos_token": "</s>",
        "pad_token": "<pad>",
        "add_bos_token": False,
        "add_eos_token": False,
        "clean_up_tokenization_spaces": False,
    }
    (directory / "tokenizer_config.json").write_text(json.dumps(config), encoding="utf-8")
    specials = {key: config[key] for key in ("unk_token", "bos_token", "eos_token", "pad_token")}
    (directory / "special_tokens_map.json").write_text(json.dumps(specials), encoding="utf-8")


class EncodeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(PROJECT))
        from tok65k import load
        from tokenizers import Tokenizer

        cls.load = staticmethod(load)
        cls._tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls._tmp.cleanup)
        cls.root = Path(cls._tmp.name).resolve()
        cls.fixture_dir = cls.root / "docs" / "hf-tokenizer"
        _write_minimal_fixture(cls.fixture_dir)
        cls.tok = load(cls.fixture_dir)
        cls.fast = Tokenizer.from_file(str(cls.fixture_dir / "tokenizer.json"))

    def test_fixture_is_synthetic_and_self_contained(self):
        spec = json.loads((self.fixture_dir / "tokenizer.json").read_text(encoding="utf-8"))
        self.assertLess(len(spec["model"]["vocab"]), 64)
        self.assertNotIn("grapheme", json.dumps(spec))
        self.assertFalse((PROJECT / "tok65k" / "tokenizer-65k.json").exists())

    def test_four_strings_match_stock_and_package(self):
        for text in FOUR:
            ids = self.tok.encode(text)
            encoded = self.fast.encode(text, add_special_tokens=False)
            self.assertEqual(ids, encoded.ids, text)
            self.assertEqual(self.tok.tokenize(text), encoded.tokens, text)
            self.assertEqual(self.tok.decode(ids), text, text)

    def test_hindi_has_the_synthetic_cut(self):
        self.assertEqual(self.fast.encode("हिन्दी").tokens, HINDI)
        self.assertEqual(self.tok.tokenize("हिन्दी"), HINDI)
        self.assertEqual(self.tok.decode(self.tok.encode("हिन्दी")), "हिन्दी")

    def test_default_encode_and_decode_use_discovered_directory(self):
        import tok65k.encoder as encoder

        with (
            mock.patch.object(encoder, "_default", None),
            mock.patch.object(encoder, "stock_dir", return_value=self.fixture_dir),
        ):
            ids = encoder.encode("English शब्द")
            self.assertEqual(ids, self.tok.encode("English शब्द"))
            self.assertEqual(encoder.decode(ids), "English शब्द")

    def test_stock_dir_discovers_a_repository_local_hf_directory(self):
        import tok65k.encoder as encoder

        fake_source = self.root / "package" / "tok65k" / "encoder.py"
        with mock.patch.object(encoder, "__file__", str(fake_source)):
            self.assertEqual(encoder.stock_dir(), self.fixture_dir)
            self.assertEqual(encoder.json_path(), self.fixture_dir / "tokenizer.json")

    def test_cli_encode_and_decode(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
        encoded = subprocess.run(
            [
                sys.executable,
                "-m",
                "tok65k",
                "encode",
                "--dir",
                str(self.fixture_dir),
                "English",
                "शब्द",
            ],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(encoded.returncode, 0, encoded.stderr)
        ids = json.loads(encoded.stdout)
        self.assertEqual(ids, self.tok.encode("English शब्द"))
        decoded = subprocess.run(
            [
                sys.executable,
                "-m",
                "tok65k",
                "decode",
                "--dir",
                str(self.fixture_dir),
                *[str(i) for i in ids],
            ],
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

    def test_input_validation(self):
        for value in (None, 1, b"text"):
            with self.subTest(value=value), self.assertRaises(TypeError):
                self.tok.encode(value)
        for value in ("1", b"1", 1, [True], ["1"]):
            with self.subTest(value=value), self.assertRaises(TypeError):
                self.tok.decode(value)
        with self.assertRaises(TypeError):
            self.tok.tokenize(None)


@unittest.skipUnless(
    SARVAM_DIR,
    "real Sarvam comparison disabled: set TOK65K_SARVAM_TOKENIZER_DIR to a user-supplied HF tokenizer directory",
)
class RealSarvamIntegrationTests(unittest.TestCase):
    def test_real_tokenizer_matches_its_stock_backend(self):
        sys.path.insert(0, str(PROJECT))
        from tok65k import load
        from tokenizers import Tokenizer

        directory = Path(SARVAM_DIR)
        packaged = load(directory)
        stock = Tokenizer.from_file(str(directory / "tokenizer.json"))
        for text in FOUR:
            with self.subTest(text=text):
                encoded = stock.encode(text, add_special_tokens=False)
                self.assertEqual(packaged.encode(text), encoded.ids)
                self.assertEqual(packaged.tokenize(text), encoded.tokens)
        self.assertEqual(packaged.tokenize("हिन्दी"), HINDI)


if __name__ == "__main__":
    unittest.main()
