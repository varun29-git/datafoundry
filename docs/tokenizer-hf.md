# Stock Hugging Face tokenizer

Load the directory `docs/hf-tokenizer` with the stock fast tokenizer. No custom Python class.

```python
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("docs/hf-tokenizer")
```

`tokenizers` 0.23.2 loads the same file with `Tokenizer.from_file("docs/hf-tokenizer/tokenizer.json")`. Transformers 5.18.0 returns `TokenizersBackend` (`PreTrainedTokenizerFast` is that class). The JSON uses only stock components: `NFC`, `Replace`, `Split`, `BPE` with `byte_fallback`, and a decoder sequence of `ByteFallback`, `Fuse`, `ByteLevel`, and `Replace`. That is the Rust tokenizer vLLM reads.

Indic encoding in `internal/build-65k.py` is Sarvam score BPE again. Characters are the atoms. The highest `indic_score` merges first. Equal scores would merge the leftmost pair; every score in this file is unique. A character with no piece becomes `<0xHH>`. The grapheme pre-segmentation rule is gone from the encoder and from `tokenizer_spec`. Piece strings and ids are the `pieces` array, unchanged: 65,536 ids, `<unk>` is 0, `Ġ` is 64.

## Match on the four strings

`Encoder.encode` and `AutoTokenizer.tokenize` produce the same pieces. Mismatch count: **0**.

| String | Pieces |
| --- | --- |
| नमस्ते | `Ġनम` \| `स्ते` |
| हिन्दी | `Ġह` \| `िन्` \| `दी` |
| ಕನ್ನಡ | `Ġಕ` \| `ನ್ನ` \| `ಡ` |
| English शब्द | `Eng` \| `lish` \| `Ġ` \| `Ġशब्द` |

`हिन्दी` is the Sarvam cut. All four round-trip through the stock decoder.

## What the stock file keeps

The normalizer is NFC, then the folds stock `Replace` can say: default-ignorable characters removed (U+200C and U+200D stay), curly quotes and unicode dashes fold onto ASCII, Unicode space separators become U+0020. Further `Replace` rules insert the Indic dummy `Ġ` and turn span spaces into `Ġ`, and map tab, newline, and carriage return to the GPT-2 byte characters `ĉ`, `Ċ`, and `č`. On the router fixtures below, that string matches the encoder’s routed stream.

The pretokenizer is `Split` on the English scissors regex. `UnicodeScripts` is not used: `Ġ` is U+0120, a Latin letter, so a script split cuts it off the Indic word and `Ġनम` cannot form. `ByteLevel` is not the pretokenizer: it rewrites Indic letters into UTF-8 byte characters, which are not the Indic pieces. It is only in the decoder, where it turns pure byte tokens such as `Ċ` back into newlines.

Merges are every split of a scored piece whose both sides are pieces, highest `indic_score` first, then `english_merges` in their saved order. A piece that is only `Ġ` repeated is not an Indic merge, same as the encoder. `<0xHH>` ids 288–543 are the byte fallback.

## Remaining mismatches

Three of 35 fixture strings differ. None of the four above do.

| String | Encoder | Stock file |
| --- | --- | --- |
| `C++में` | `C` \| `+` \| `+` \| `Ġमें` | `C` \| `++` \| `Ġमें` |
| `\frac{1}{2}` | `\frac` \| `{` \| `1` \| `}` \| `{` \| `2` \| `}` | `\frac` \| `{` \| `1` \| `}{` \| `2` \| `}` |
| `\n    return` | `ĊĠĠĠĠ` \| `return` | `ĊĠ` \| `ĠĠĠ` \| `return` |

`++` and `}{` are scored Indic pieces, so the one shared merge list joins them inside an English chunk. The encoder’s English path does not use Indic scores, and those pairs are not in `english_merges`. `\n    ` is an English seed. The stock model has no seed trie, so the whitespace merges stop early. The stock decode of that cut is still the text `\n    return`.

Two decoder gaps show up off those four strings. `राम\nश्याम` encodes the same pieces, and the fused string still contains Indic letters, so `ByteLevel` leaves `Ċ` in place (`रामĊ श्याम`). On `C++में` the dummy `Ġ` in `Ġमें` is the same character as a space, and the decoder turns it into a space (`C++ में`).
