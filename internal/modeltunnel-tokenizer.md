# Can terminus-modeltunnelv2 encode and decode the frozen tokenizer?

Yes. `docs/tokenizer-65k.json` loads, encodes, and decodes through the repo’s own JSON tokenizer. It is the file that code is pinned to.

Checked on this Mac, read-only. The repo was not copied, the tokenizer was not edited, and no EC2 instance was started.

## Which file loads a tokenizer

`terminus/tokenizer.py`, function `load_tokenizer(path)`, dispatches on the suffix:

| Suffix | Class | File |
| --- | --- | --- |
| `.txt` | `RWKVWorldTokenizer` | same file, `terminus/tokenizer.py` |
| `.json` | `Frozen65kTokenizer` | `terminus/tokenizer65k.py` |
| anything else | SentencePiece `SentencePieceProcessor` | expects a `.model` protobuf |

`load_tokenizer` is what `terminus/prepare_data.py`, `terminus/prepare_campaign_data.py`, `terminus/pack_tokens.py`, `scripts/tokenize_parallel.py`, and `scripts/evaluate_run.py` call. `scripts/roundtrip_scan.py` and the lean-run probe construct `Frozen65kTokenizer` directly. `encode` and `decode` live on that class. `encode_text` in `terminus/tokenizer.py` calls both and refuses the result unless decode matches NFC text.

`SOURCE_PROVENANCE.md` still says the JSON “is not yet integrated into the code at initialization.” That line is stale. The dispatcher and `Frozen65kTokenizer` are in the tree and are what the prepare and tokenize scripts import.

## What the JSON loader expects

`Frozen65kTokenizer.__init__` hashes the file first. The default, which `load_tokenizer` uses, must equal `c53e0e95cd19e2954a8c7114c0a580eeb16698b153fdf84c5d80a7187d778d29`. A different hash raises `ValueError` before parsing. Passing `expected_sha256=None` skips that check and then validates the schema.

The schema is this private runtime file, not a Hugging Face `tokenizer.json` and not SentencePiece. Required shape, enforced by `_validate_artifact`:

- Top-level keys include `vocab_size`, `K`, `U`, `english_tail`, `pieces`, `indic_model`, `indic_normalizer`, `indic_scores`, `bytes_to_unicode`, `english_merges`, `english_scissors`, `english_seeds`, `tokenizer_spec`.
- `vocab_size` is 65536. `pieces` and `indic_scores` are length 65536. Piece strings are unique.
- Ids 0–4 are `<unk>`, `<s>`, `</s>`, `<pad>`, `<eod>`. Ids 5–31 are `<reserved_NNNN>`. Ids 32–287 are the 256-entry `bytes_to_unicode` alphabet. Ids 288–543 are `<0x00>`…`<0xFF>`. Ids 40347–65535 are the `english_merges` concatenations in order (`english_tail` 25189). The Indic region is ids 544–40346 and must agree with `K` (40059).
- `indic_model` is the string `"BPE"`. `indic_normalizer` is NFC, dummy prefix on, space mark `Ġ` (U+0120).
- `tokenizer_spec.indic` must equal a fixed dict (NFC, dummy prefix, space mark, highest `indic_score` merges first, equal scores take the leftmost pair, unknown characters become `<0xHH>`). `tokenizer_spec.router` must contain the nine rule names, and `indic_letter` must name Bengali, Devanagari, Gujarati, Kannada, Tamil, and Telugu. `tokenizer_spec.specials.ids_0_4` must be the five specials above.

Encode never emits ids 0–31 for normal text. Decode raises on those ids unless `render_specials=True`.

## Does this JSON load?

Yes. The store file and `tokenizer/tokenizer-65k.json` in the repo are the same bytes: 1,951,352 bytes, SHA-256 `c53e0e95cd19e2954a8c7114c0a580eeb16698b153fdf84c5d80a7187d778d29`.

`load_tokenizer` on the store path returned `Frozen65kTokenizer` with vocab size 65536, unk 0, bos 1, pad 3, eos (`<eod>`) 4. Round trip through `encode` / `decode`, and through `encode_text`, matched the input for `The quick brown fox.` (5 ids), `नमस्ते` (2), `main जा रहा hoon` (7), a newline plus four spaces plus `return` (2), and `\frac` (1).

## The earlier RWKV-only claim

The claim that the tree only contains `data/tokenizer/rwkv-7-world/rwkv_vocab_v20230424.txt`, and that this text file is RWKV World rather than the frozen JSON, is half right.

That text file is RWKV-7 World, and it is not this JSON. `scripts/fetch_rwkv_world_tokenizer.py` pins it to BlinkDL `RWKV-LM` commit `aeda8a06fc4803655473c7e7359b1d7166e2c604`, path `RWKV-v7/rwkv_vocab_v20230424.txt`, SHA-256 `e6dee3d4e31b4d5c40ac99508ac6c701ceef4bed681bf2167ce9a908552bca89`. The file on disk matches that hash: 65,529 lines, ids 1 through 65529, first piece a single zero byte. `RWKVWorldTokenizer` accepts only that line format (`id`, a Python literal, a byte length) and rejects anything that is not the 65,529-piece World vocab. `load_tokenizer` sends it there because the suffix is `.txt`. It cannot load `tokenizer-65k.json`.

It is not the only tokenizer in the tree. Also present:

- `tokenizer/tokenizer-65k.json` — byte-identical to the frozen store file, loaded by `Frozen65kTokenizer`.
- `tokenizer/tokenizer-65k-freeze.md` — provenance note, not a loader.
- `terminus/tokenizer65k.py` and the `.json` branch of `terminus/tokenizer.py`.
- `data/tokenizer/sarvam-1/.cache/huggingface/download/` — Hugging Face download locks and metadata stubs only (`tokenizer.json`, `tokenizer.model`, `tokenizer_config.json`, `special_tokens_map.json`). No model payload and no second vocab file.

The “only that text file” note came from a run that could not read this Mac. Against the tree here, the frozen JSON and its encoder are both on disk.
