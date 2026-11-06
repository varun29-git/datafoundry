"""The English fleet must store token ids and the index as two objects."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fleet_worker


class FleetWorkerTests(unittest.TestCase):
    def test_index_key_does_not_replace_the_uint16_object(self):
        with tempfile.TemporaryDirectory() as work:
            out = os.path.join(work, "out")
            bin_path = os.path.join(out, "code-v2-rewriting", "en", "part.tokens.uint16")
            index_path = os.path.join(out, "code-v2-rewriting", "en", "part.tokens.index.jsonl")
            os.makedirs(os.path.dirname(bin_path), exist_ok=True)
            bin_key, index_key = fleet_worker.shard_object_keys(
                "tokenized/tok65k-english-v1", out, bin_path, index_path
            )
            self.assertTrue(bin_key.endswith(".tokens.uint16"))
            self.assertTrue(index_key.endswith(".tokens.index.jsonl"))
            self.assertNotEqual(bin_key, index_key)

    def test_empty_rows_drop_and_a_leading_special_id_is_kept(self):
        self.assertFalse(fleet_worker.keep_document([]))
        self.assertTrue(fleet_worker.keep_document([1, 64, 100]))
        self.assertTrue(fleet_worker.keep_document([0]))

    def test_long_text_matches_one_whole_encode(self):
        from tokenizers import Tokenizer

        tok = Tokenizer.from_file(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "docs",
                "hf-tokenizer",
                "tokenizer.json",
            )
        )
        text = ("alpha\n    return " + ("x" * 3000) + "\nbeta")
        self.assertGreater(len(text), fleet_worker.ENCODE_BATCH)
        ids = fleet_worker.encode_docs(tok, [text, "", None])
        whole = tok.encode(text, add_special_tokens=False).ids
        batched = tok.encode_batch([text], add_special_tokens=False)[0].ids
        self.assertEqual(ids[0], whole)
        self.assertEqual(ids[0], batched)
        self.assertEqual(ids[1], [])
        self.assertEqual(ids[2], [])


if __name__ == "__main__":
    unittest.main()
