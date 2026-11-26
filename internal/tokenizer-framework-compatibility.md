# Is the 65k tokenizer usable by Transformers and the usual stacks?

No. `docs/tokenizer-65k.json` is a private runtime file. It is not a Hugging Face `tokenizer.json`, not a SentencePiece `tokenizer.model`, and not a tiktoken file. The only loader that implements its rules is `Encoder` in `internal/build-65k.py` (`load_runtime`). That loader does not open `tokenizer.model`.

`tokenizers.Tokenizer.from_file` on this file fails immediately: `Exception: expected ',' or '}' at line 1 column 14`. `PreTrainedTokenizerFast` and `AutoTokenizer` read that same schema, so they fail the same way. Nothing else in the usual set can load it either: vLLM, SGLang, TGI, TensorRT-LLM, and llama.cpp all want a fast Hugging Face tokenizer or a SentencePiece model.

## What the file actually is

65,536 unique piece strings, ids 0–65535. Top-level keys are `vocab_size`, `K`, `U`, `english_tail`, `pieces`, `indic_model`, `indic_normalizer`, `indic_scores`, `bytes_to_unicode`, `english_merges`, `english_scissors`, `english_seeds`, `tokenizer_spec`. There is no `version`, no `model.vocab`, no `model.merges` in the Hugging Face shape, no `added_tokens`, no `decoder`.

`indic_model` is the string `"BPE"`. That is not the Rust BPE model. Indic text is cut by walking scores: highest `indic_score` merges first, equal scores take the leftmost pair. The span is NFC'd, a leading `Ġ` (U+0120) is added, and each ordinary space becomes `Ġ`. A character with no piece becomes the literal tokens `<0xHH>`.

English text is a second algorithm. UTF-8 bytes sit at ids 32–287 using the GPT-2 byte-to-unicode map (`Ā` is byte 0, `Ġ` is byte 0x20, `Ċ` is newline). `english_merges` has 25,189 pairs, and each pair's concatenation is the piece at `40347 + rank`. A longest-match seed trie (340 strings: indents and LaTeX commands) runs on the raw span before the regex. The regex is an Oniguruma `Split`, not Python `re`.

A Python router sends each stretch one way or the other. Indic letters with no Latin letters, including digits, punctuation, and single spaces, stay Indic. A newline, tab, carriage return, or two spaces stay English and split the stretch. Mixed words split so digits and punctuation stick to the run on their left. `main जा रहा hoon` is English, a real space, Indic `जा रहा`, a real space, English.

## Why a wrapper will not make the ids safe

One piece string is two meanings. Id 64 is the string `Ġ`, and its Indic score is `-63114`. That same id is English byte 0x20, because the byte rows are `32 + byte` and the space byte's GPT-2 character is `Ġ`. `load_runtime` requires piece strings to be unique, so there cannot be a second space piece. Decode decides which meaning to use with `_indic_mask`, looking at neighboring ids. A framework that detokenizes from the string table will turn that id into the wrong characters on mixed lines.

Forty-one of the byte-character strings also carry an Indic score. Those are aliases: the Indic path owns them when the mask says so, and the English path owns them as raw bytes otherwise. Ids 288–543 are a second byte alphabet, the literal pieces `<0x00>` through `<0xFF>`, used only when the Indic scorer has no character piece.

The English merges are internally consistent (every merge side is a piece, and piece `40347 + n` equals the concatenation). They still cannot be dropped into a stock BPE file. The seed trie can consume a prefix the regex would have kept inside a longer chunk, and the router is not a pretokenizer. `tokenizer_spec` is mostly prose. `load_runtime` checks a fixed list of strings against `route()` and refuses to load if the prose and the code disagree. That check is not something `tokenizers` can run.

## What “usable” would require

A tokenizer the usual stacks can load is one file: one vocabulary, one merge list, one pretokenizer, one decoder, and no id whose string depends on its neighbors. `tokenizers.Tokenizer.from_file` then works, and Transformers, vLLM, and llama.cpp follow. This JSON is not that file. Exporting it by renaming keys would preserve the collision and the router, and the ids would still mean the wrong text.

A `trust_remote_code` slow tokenizer could call `Encoder.encode` / `Encoder.decode` from Python Transformers. Training code that already imports `build-65k.py` can do that today. The fast path, and every Rust or C++ server, would still be on a different tokenizer. The plan’s line that Hugging Face `tokenizers` is the encoder the dataloader will call describes the akshara trainer that was not what got frozen. The frozen file is the Sarvam score table plus the English tail.

## Terminus ModelTunnel v2

The expected ModelTunnel v2 checkout was on an unmounted macOS filesystem, so the Linux cloud worker could not read that tree. A local search confirmed only that the checkout was absent from the worker. See [modeltunnelv2-mac-search.md](modeltunnelv2-mac-search.md).

The only file a previous run recorded inside it is `data/tokenizer/rwkv-7-world/rwkv_vocab_v20230424.txt`. That is the RWKV World vocab, a separate format, not a Hugging Face tokenizer. S3 also has the prefix `data/modeltunnelv2_tokensets_20261001/`, which is packed token data, not the encoder. The encode/decode code in that folder was not read, so nothing from it was copied.
