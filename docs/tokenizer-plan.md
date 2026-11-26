# Tokenizer plan: 65,536 tokens for the 1.2B decoder

Train this tonight. Do not start the 1.2B run until the gate at the end passes.

The model is a from-scratch 1.2B dense decoder. The languages are English, Hindi, Marathi, Kannada, Telugu, Tamil, Gujarati, and Bengali. Kannada and Telugu are separate scripts. Hindi and Marathi share Devanagari and do not share a fertility score. The train is two files, on one mixed 15 GB sample. Stage 1 is one akshara-constrained BPE. Its vocabulary is exactly **65,536**, including 32 specials and 256 bytes, so every id fits in `uint16`. Save it as `tokenizer-stage1.json` and never overwrite it. It is the fallback. `tokenizer-stage2.json` is also exactly **65,536**. It reuses rare learned slots. It does not add ids above 65,535. The rules are in [Stage 1 and stage 2](#stage-1-and-stage-2). A plain-language walkthrough is in [tokenizer explained](tokenizer-explained.md).

Score both files. Ship stage 2 only if every language’s tokens/word is less than or equal to stage 1. Otherwise ship stage 1. If stage 1 misses the engineering bar, train a second tokenizer at **81,920** (80 × 1,024, the 81.9k backup). That backup is not a substitute for stage 2, and stage 2 is not a substitute for it. Same regex, same sample, same Indic budgets. The extra 16,384 ids are Latin, so Latin learned goes from 26,748 to 43,132. Do not train the 81,920 model before the 65,536 score exists. Tied at hidden size 2048, 81,920 rows are 167,772,160 parameters, 33,554,432 more than 65,536. Stage 2 adds no rows. The embedding stays 65,536 × 2,048.

The curriculum’s 15% Indic share, the 710B English rows, and the phase weights are the **model** mixture. They are not this sample. A tokenizer trained on those weights spends its slots on English web.

---

## What was wrong in the first plan

The first plan reserved the Unicode letters and then trained SentencePiece Unigram on a character-balanced sample. That trains the right alphabet and the wrong cut.

A byte-level BPE tokenizer does not see raw text. A regex cuts the text into pre-tokens first. Merges happen only inside one pre-token. Nothing the trainer does can join two pre-tokens back together. More data does not help. A bigger vocabulary does not help. The floor is the regex.

The regex most English tokenizers still use treats a word as `\p{L}+`, one or more Unicode letters. In these scripts the vowels are not letters. They are marks. Devanagari `ि` is category Mc. The virama `्` is Mn. Nukta is Mn. `\p{L}+` stops at every one of them.

`हिन्दी` is six code points: ह (letter), ि (vowel sign), न (letter), ् (virama), द (letter), ी (vowel sign). A letters-only cut produces six pieces, `ह | ि | न | ् | द | ी`. The repaired cut produces one piece, the whole word. The same thing happens to `स्कूल`: the broken cut is `स | ् | क | ू | ल`. TinyLlama, Llama 2, Llama 3, and Qwen2.5 are in the broken family or in a family that never spent merges on these scripts. They are the wrong starting point. Do not append Indic pieces onto their merge lists.

SentencePiece avoids that particular regex, which is why it looked like a safe default. It is still the wrong tool for this model. Its normal preset collapses whitespace, which breaks code. It does not protect an English merge list, so a balanced Indic sample pushes English off the frontier. And it has no notion of an akshara, so a frequent byte pair can leave a virama at the end of a token.

Two published facts fix the target. They are other people’s measurements on other files. They are not our scores, and they are not the pass bar.

- Regmi, Pudasaini, and Pun, “Vowel Signs Are Not Letters,” trained 65,536-token tokenizers that differ by one character class. On FLORES-200 devtest, at a 50/50 byte split with English, the broken class scored Hindi 3.36 tokens/word, Bengali 4.73, Tamil 6.85. The repaired class (`[\p{L}\p{M}]+`) scored 1.32, 1.50, and 1.77. English moved by about 2%. Their own paper says those runs are bilingual and optimistic for a real multilingual mix. A flat mix of our eight languages would give a lot of that gain back.
- On the same FLORES English/Nepali files, their table lists Llama 3 English at 1.24 tokens/word and Sarvam-1 English at 1.50, with Nepali at 3.76 (Llama 3) and 2.66 (Sarvam-1). An akshara tokenizer at 64k (akshara-tokenizer v1.2, its own report) gets Indic near 1.4–2.1 and English at 2.15, against a Qwen English number of 1.26. That English number is what we will not ship. Spending the whole 64k table on aksharas throws English away.

So the job is both, at a hard 65,536: Indic at or below the best tokenizer we can actually load, English within a small distance of the best English tokenizer, code and math intact. The way to get both is below. The pieces are published. The combination this model needs is not a bilingual 65k toy and not a 256k Indic table.

---

## What a tokenizer does

The model does not read letters. The tokenizer turns a string into integers and the integers back into the same string. Fertility is **tokens per word**. Also report **tokens per character**, counted in Unicode code points, not UTF-8 bytes. **Lower is better.** Strong means the lowest tokens/word in the comparison set.

Indic letters are three UTF-8 bytes. If a letter is not its own token, it costs about three tokens before the vowel sign is even counted. A 1.2B model reads a fixed number of tokens per step. Shattered Indic text means fewer words per step, and the loss is computed on scraps. The same documents also fill more of each sequence than their share of the corpus, so the Indic fraction of steps drifts up and English drifts down relative to the curriculum.

There is a second, harder failure. Even after every letter is a token, a letters-only pre-tokenizer has already cut the word apart. The rest of this document is about not making that cut, and about not letting either English or Tamil spend the other one’s slots.

---

## Parameter cost at 1.2B

**Assumption, not a measured fact:** hidden size 2048. The inventory does not state a hidden size. If the real width differs, recompute `vocabulary × hidden size`. Do not change 65,536 to make the percentage look nicer.

| Piece | Calculation | Parameters | Share of 1.2×10⁹ |
| --- | --- | ---: | ---: |
| Input embedding, 65,536 | 65,536 × 2,048 | 134,217,728 | 11.18% |
| Output head **tied** | same matrix, counted once | 134,217,728 | 11.18% |
| Output head **untied** | a second copy | 268,435,456 | 22.37% |
| Input embedding, 96,000 | 96,000 × 2,048 | 196,608,000 | 16.38% |
| Input embedding, 131,072 | 131,072 × 2,048 | 268,435,456 | 22.37% |
| 128k, untied | two copies | 536,870,912 | 44.74% |

Tie the output head. Under this width that leaves about 1.066×10⁹ parameters for the rest of the network. A 128k tied table costs the same 268,435,456 parameters as the entire untied 65k pair. Those parameters are a large slice of a 1.2B model. This model needs them in the layers. 65,536 is the last vocabulary that fits in the `uint16` packing the old packs already use. Stage 1 and stage 2 both stay at that size. Ids above 65,535 are not added. Tied at hidden size 2048, stage 2 adds no rows, so it adds no embedding parameters.

96,000 was checked as a way to give Latin more than 25,840 learned pieces. Tied, 96,000 × 2,048 is 196,608,000 parameters, 16.38% of 1.2B. That is 62,390,272 parameters moved out of the layers if the model stays 1.2B, about 6% of the transformer, and the output projection grows by 96,000 / 65,536. The extra 30,464 ids would sit in Latin. Stage 1 stays at 65,536. Do not move to 96,000. 98,304 (96 × 1,024) is the same parameter decision, about 67 million parameters out of the layers. Stage 2 does not add ids above 65,535. The 81,920 backup, if stage 1 misses the engineering bar, is a different file and does not fit in `uint16`.

A larger vocabulary does put more text in each token. The same training-token budget then covers more words, and a 4,096-token window holds more of a document. That is the semantic-density effect, and it is real. It is also steepest while common words are still being split. The vowel-sign paper’s large Indic jump, Hindi 3.36 tokens/word down to 1.32, came from repairing the regex at a fixed 65,536. BPE spends its first slots on the frequent pieces, which are almost all of the token stream. The next 30,464 ids are rarer pieces, and a bigger table still cannot merge across the regex. The published English gap from that paper’s own 65,536 bilingual table to Llama 3 is 1.30 versus 1.24 on their FLORES file, about 5%, and they call the bilingual setup optimistic. A gain of that size is the same order as the layers those rows would replace. It is their number, on their file, not a measurement of 65,536 against 96,000 on ours.

`uint16` is a pack format, not a training or serving speed limit. Ids 0–65,535 fit in two bytes. 96,000 does not, so a stored token bin becomes `uint32` and any reader that casts to `uint16` truncates. The counted HQ-synth bin is 15,000,000,001 tokens, about 30 GB as `uint16` and about 60 GB as `uint32`. A fully materialized 835.294B-token curriculum would be about 1.67 TB versus 3.34 TB. The old TinyLlama bins are retokenized either way: the same width does not mean the same strings. On the step, the id tensor at 2×10⁶ tokens is 4 MB versus 8 MB, and the embedding lookup wants a wider integer index than `uint16` anyway. KV cache and the prompt buffer do not store the vocabulary. The cost that moves training and deployment is the wider embedding and the wider logit matmul, which come from the vocabulary size, not from the two extra bytes on disk.

A 32k English table (TinyLlama, Llama 2) does not have room for six Indic scripts. A 256k Indic table does not fit this model. The work is to spend 65,536 well. Stage 2 may reuse a rare learned slot inside that same list, and only if the ship rule passes.

---

## Design

Byte-level BPE. One regex in front of it. One mixed train, not a merge list per script. Hugging Face `tokenizers` is the trainer and the encoder the dataloader will call. On 0.23.2 the regex compiler inside that library is Oniguruma, not Python `re`. Stage 1 is saved as `tokenizer-stage1.json` and is never overwritten. Stage 2 is saved as `tokenizer-stage2.json`.

Byte-level means the alphabet is the 256 UTF-8 bytes, so any string can be encoded and `decode(encode(x))` can return `x`. The regex is what makes Indic fertility possible. The mixed sample is what keeps a rare script’s words in the same train as English. The slot table later in this plan is the diagnostic for that mix, not a set of separate trainers.

UTF-8 ranges of these scripts do not overlap, which is why a byte merge in one script is never a byte merge in another:

| Script | UTF-8 prefixes of the primary block |
| --- | --- |
| ASCII / English | bytes below `0x80` |
| Devanagari | `e0 a4`, `e0 a5` |
| Bengali | `e0 a6`, `e0 a7` |
| Gujarati | `e0 aa`, `e0 ab` |
| Tamil | `e0 ae`, `e0 af` |
| Telugu | `e0 b0`, `e0 b1` |
| Kannada | `e0 b2`, `e0 b3` |

A merge of English bytes is never a merge of Tamil bytes. The scripts compete for **slots**, not for the same strings. Stage 1 is one akshara-constrained BPE on the mixed sample, so those slots are filled by one merge list. ZWJ (`e2 80 8d`) and ZWNJ (`e2 80 8c`) sit outside those blocks. They are allowed inside an Indic token. They are not a reason to split the train by script.

### Pre-tokenizer

The pattern is a partition of the string. Alternatives are tried in this order. It is a raw Python string: `\p`, `\x`, `\n`, `\r`, `\s`, and `\S` must reach the engine, not Python.

```text
(?:\r\n|\n|\r)[ \t]*
|\\[A-Za-z]+
|[0-9\x{966}-\x{96F}\x{9E6}-\x{9EF}\x{AE6}-\x{AEF}\x{BE6}-\x{BEF}\x{C66}-\x{C6F}\x{CE6}-\x{CEF}]
|[^\r\n\p{L}\p{N}\x{964}\x{965}\x{2C}\x{3B}\x{3A}\x{2E}\x{3F}\x{21}\x{22}\x{27}\x{28}\x{29}\x{5B}\x{5D}\x{7B}\x{7D}]?[\p{L}\p{M}\x{200C}\x{200D}]+(?:[\x{27}\x{2019}][\p{L}\p{M}\x{200C}\x{200D}]+)*
|[^\s\p{L}\p{M}\p{N}\x{200C}\x{200D}]+
|[^\S\r\n]+
|[\s\S]
```

**Which engine.** Python’s `re` does not implement `\p{L}` or `\p{M}`. `re.compile` on this pattern raises `bad escape \p`. A smoke test written against `re` is not the cut `Split` will make. Hugging Face `tokenizers.Regex` is the compiler. On `tokenizers` 0.23.2 that compiler is Oniguruma: a bad pattern raises `Oniguruma error`, and `\u{0964}` raises `invalid code point value`. The Rust `regex` crate accepts `\u{0964}` and rejects lookaheads. This pattern uses neither `\u{...}` nor lookaheads. `\x{HHHH}` is the escape both of those engines accept. A literal `]` inside a class ends the class (`premature end of char-class`), so `[` and `]` are `\x{5B}` and `\x{5D}`.

Pass the raw string to `tokenizers.Regex`, then `Split(..., behavior="isolated")`. If `Regex` throws, stop. Do not train, and do not rewrite the classes for `re`.

`ByteLevel(add_prefix_space=False, use_regex=False)` comes after that `Split`, inside a `Sequence`. `use_regex=False` is load-bearing. On 0.23.2, the same `Split` followed by `ByteLevel(use_regex=True)` cuts `हिन्दी` into six pieces again. `use_regex=False` leaves one piece whose span is the whole word. The bytes display as latin-1 mojibake; judge the piece count and the span, not the glyphs. `add_prefix_space=False` because the word pattern already keeps one leading space. Confirm the flag names on the training pin. This pattern was compiled on 0.23.2 and produced the smoke table below. Re-run that table on the training pin before the long train.

The hex in the word prefix is the exclusion list, not the alphabet: `\x{964}` danda, `\x{965}` double danda, then comma, semicolon, colon, period, question mark, exclamation, double quote, apostrophe, parentheses, brackets, braces. Digit ranges are Devanagari `0966–096F`, Bengali `09E6–09EF`, Gujarati `0AE6–0AEF`, Tamil `0BE6–0BEF`, Telugu `0C66–0C6F`, Kannada `0CE6–0CEF`. `\x{200C}` is ZWNJ and `\x{200D}` is ZWJ.

What each line is for:

| Piece | Why |
| --- | --- |
| Newline plus the spaces or tabs that follow | One pre-token for the indent. Code keeps its shape. A newline in prose is just a newline. |
| A LaTeX command, `\frac` | The command is one pre-token, so it can become one token. This line has to come before punctuation, or the backslash is punctuation. |
| One digit | ASCII and the six Indic digit blocks. A digit never glues to the next digit. `65` is two pre-tokens, and so is `६५`. This is the math choice: a 1.2B model learns place value from single digits. Llama 3 groups digits by up to three. We do not copy that. Do not spend slots on integers like `2024`. The math gate scores this choice on digit-stripped text, so a glued-digit baseline cannot fail the run by itself. |
| A word | Letters, marks, ZWJ, and ZWNJ. The optional character in front may be a space or a tab, so ` गया` and a tab glued to the next word stay one pre-token. It may not be a newline, a letter, a digit, a danda, a double danda, or sentence punctuation (`, ; : . ? ! ' " ( ) [ ] { }`). Danda and double danda are category Po. The old prefix `[^\r\n\p{L}\p{N}]` matches them, so web text with no space (`गया।वह`) becomes the pre-token `।वह` and the vocabulary fills with punctuation-prefixed words. Space and tab stay allowed. A class written `[^ \t\r\n...]` isolates every space. BPE cannot merge across pre-tokens, so each word pays an extra token for the space in front of it. That is the wrong fix. Underscore is not in the exclusion list, so `foo_bar` is `foo` + `_bar`. Period is in the list, so `foo.bar` is `foo` + `.` + `bar` and `.method` is `.` + `method`. The code gate is where that cost shows up. An apostrophe or a right single quote between letters stays inside the word, so `don't`, `it's`, and `I’m` are one pre-token each. BPE may still split a rare contraction. It is allowed to keep a frequent one as one token. A leading or trailing quote does not join: `'string'` is `'`, `string`, `'`. The old GPT-2 rule matched `'t` before the word could, so `don't` was frozen as `don` plus `'t` and no merge could undo it. That rule is what GPT-4 (`cl100k`), Llama 3, and Qwen2 still ship. GPT-4o (`o200k`) stopped doing it: the suffix is an optional tail on the word, so `don't` is one pre-token. Ours is that newer cut, widened so any apostrophe between letters stays in the word, not only `'t`, `'s`, `'re`, `'ve`, `'ll`, `'d`, and `'m`. Vowel signs, virama, and nukta stay inside the word. `\p{M}` is the Indic repair. ZWJ and ZWNJ are category Cf, so they have to be named or they split the word. |
| A punctuation run, then spaces and tabs that are not a newline, then one character | The punctuation run must exclude letters, marks, **numbers**, ZWJ, and ZWNJ. Dropping `\p{N}` is the bug: `{1}{2}` becomes one pre-token, and the partition test still passes because the characters are all there. With `\p{N}` kept, `\frac{1}{2}` is `\frac`, `{`, `1`, `}{`, `2`, `}`. The two braces between the digits stay one punctuation chunk. BPE may still emit them as two tokens, because that cut is inside one pre-token. The space/tab line must not match a newline. If it does, a trailing space on a line of code swallows `\n    ` and the indent seed never sees it. `[^\S\r\n]` is that line: whitespace, and not CR, and not LF. |

**Semantic smoke test, before any train.** Run it through `Split` on `tokenizers.Regex`, not through Python `re`. A partition that concatenates back to the original string can still be the wrong cut. `{1}{2}` as one pre-token passes concatenation and fails math. These cuts are exact. One mismatch and the regex is wrong.

| String | Pre-tokens |
| --- | --- |
| `नमस्ते`, `स्कूल`, `संस्कृति`, `தமிழ்`, `ಕನ್ನಡ`, `हिन्दी` | each string is one pre-token |
| `don't`, `it's`, `I’m` | each string is one pre-token |
| `'string'` | `'`, `string`, `'` |
| `\frac{1}{2}` | `\frac`, `{`, `1`, `}{`, `2`, `}` |
| `65`, and `६५` | `6`, `5`, and `६`, `५` |
| `foo.bar` | `foo`, `.`, `bar` |
| `foo_bar` | `foo`, `_bar` |
| `राम गया।वह आया` | `राम`, ` गया`, `।`, `वह`, ` आया` |
| `गया।वह` | `गया`, `।`, `वह` |
| a newline, four spaces, then `return` | that newline-and-indent as one pre-token, then `return` |

The space in ` गया` and ` आया` is part of the word pre-token. A cut that isolates it (`राम`, ` `, `गया`, `।`, `वह`, ` `, `आया`) fails this table. The danda is its own pre-token either way. That is the bug being fixed. The space is not.

**Partition test, same strings and every eval string.** The pre-tokens concatenate back to the original. One failure and the regex is wrong. This test does not replace the table above.

**Shatter test, before any train.** On about 2,000 held-out words per language, compute pre-tokens per word with this regex. Indic should sit well under 2. A letters-only regex on the same words sits near 3 for Hindi and near 5–7 for Tamil. If any of our eight languages is above 2.0 pre-tokens per word, stop. Training cannot fix it. The published floors for the repaired class on FLORES, as pre-tokens per word, are about 1.12 Hindi, 1.16 Marathi, 1.15 Gujarati, 1.15 Bengali, 1.19 Tamil, 1.24 Telugu, 1.25 Kannada. Our regex also isolates digits and punctuation, so real text will sit a little higher. It will not sit at 3.

**ByteLevel check, same moment.** Pre-tokenize `हिन्दी` with the full `Sequence`. One piece, span covering the word. Six pieces means `use_regex=True` put the GPT-2 cut back after `Split`. The latin-1 glyphs ByteLevel prints are the UTF-8 bytes. They are not a second bug.

### What “akshara” means here

An akshara is an orthographic syllable. The pre-tokenizer does **not** cut the word into aksharas. the requester accepted this. If it did, a word of four syllables could never be one token, and fertility would be stuck there. The pre-tokenizer keeps the word, so a frequent word can still be one token. BPE cuts inside that chunk, and only on an akshara boundary. English, code, math, and LaTeX are unchanged.

Rules for the checker. Implement them directly. Do not call Unicode grapheme breaking and hope. This machine’s `unicodedata` is 15.0.0. The conjunct rule GB9c arrived in Unicode 15.1. An old `\X` splits `स्कूल` into `स्` + `कू` + `ल` and will lie to the checker.

**Conjunct scripts** (Devanagari, Bengali, Gujarati, Telugu, Kannada). A consonant plus virama plus the next consonant is one akshara, then the vowel sign, nukta, anusvara, visarga, or candrabindu that follows it. ZWJ and ZWNJ stay on that akshara. An independent vowel plus its marks is its own akshara.

**Tamil is not in that list.** Tamil pulli (U+0BCD) ends the akshara. It does not swallow the next consonant. `தமிழ்` is three aksharas, `த` + `மி` + `ழ்`. A token may end on the pulli. A token may not put the pulli on the following consonant, and it may not separate `ழ` from `்`. Applying the Devanagari conjunct rule to Tamil glues letters Tamil does not glue.

**Hard rule, inside an Indic chunk.** A BPE token may end only on an akshara boundary. For `हिन्दी` the only legal split is `हि` | `न्दी`. A token must not start with a dependent vowel mark, and must not end on a virama that is still waiting for the next consonant. `स्कूल` may split only as `स्कू` | `ल`. ZWJ and ZWNJ stay inside the akshara they belong to. A merge that would break this rule is not added. The old 0.5% allowance for a boundary inside an akshara is retired. A boundary between two whole aksharas is legal.

A token is illegal when:

- it is only a virama, a vowel sign, or a nukta
- it starts with a vowel sign or a nukta
- in a conjunct script, it ends in a virama and the next token begins with a consonant (the conjunct was cut)
- in Tamil, it ends in a consonant that the pulli was supposed to stay with

**Inference fallback.** This is mandatory on the encode path, for stage 1, for stage 2, and for the 81,920 backup if that one is trained. No `<unk>` on this path. Walk the chunk left to right in whole aksharas. Emit the longest vocab token that covers one or more whole aksharas and is itself in the vocabulary. When the next akshara is not covered by any such token, decompose that akshara to its characters, in code-point order, and emit each character’s own id if that character is in the vocabulary. When a character is not in the vocabulary, emit the ids of its UTF-8 bytes, in byte order. Those ids are the 256 byte rows, not `<unk>`. Example: `हि` missing as a whole, `ह` present, `ि` absent → the id of `ह`, then the three byte ids of U+093F (`E0 A4 BF`). Decode concatenates the token strings. Bytes rebuild the character, characters rebuild the akshara, so `decode(encode(x))` is `x`.

**Malformed input.** The akshara parser returns an id list. It does not throw. An isolated vowel sign, nukta, or virama with no base consonant is not glued onto a neighbor: emit that character’s id if it is in the vocabulary, otherwise its UTF-8 byte ids, in order. A truncated conjunct (a virama with no following consonant inside the chunk) does not invent a consonant and does not read past the chunk. Close the piece as the base plus that virama, plus any ZWJ or ZWNJ already taken, then use the same whole-piece, else character, else byte order. A stray ZWJ or ZWNJ that sits on a base stays inside that akshara. A stray ZWJ or ZWNJ with no base uses the character-then-byte path (ZWJ is `E2 80 8D`, ZWNJ is `E2 80 8C`).

**Akshara gate:** on each Indic eval set, zero tokens violate the hard rule above. If a language misses this and the regex shatter test passed, seed that script’s aksharas and retrain the one mixed stage-1 BPE into a new file. Do not overwrite `tokenizer-stage1.json`. The fallback still covers any akshara the seed list missed.

Seeding, only if the gate fails: from that script’s training sample, take the aksharas that cover 99.5% of akshara mass. Force them as early merges inside that script’s slot budget, built from its code points, which are themselves early merges of the three UTF-8 bytes. Then let free BPE fill the rest of the budget with words. Do not seed aksharas by deleting word tokens until the gate has actually failed. Forced aksharas that nobody merges into words are how a 64k table ends at English fertility 2.15.

### Normalization

The encode path does not normalize. `decode(encode(x)) == x` is byte-for-byte on the original string, including code and Indic.

NFC the **training sample only**, so the same word is not learned twice under two canonically equivalent spellings. NFC does not strip nukta, virama, ZWJ, or ZWNJ, and it does not rewrite ASCII code. Do not NFKC anything. NFKC folds compatibility characters and is how some multilingual tokenizers delete ZWJ and ZWNJ. Those tokenizers then look slightly more compressed on text they can no longer represent. They fail our round-trip.

| Item | Rule |
| --- | --- |
| Newlines, tabs, runs of spaces | Kept by the regex. Four spaces decode as four spaces. |
| Nukta | A mark, so it stays inside the word. It changes the letter. `ड` is not `ड़`. |
| ZWJ, ZWNJ | Named in the word class. Not spaces. Deleting either one changes the word. |
| Latin punctuation | Not folded onto curly quotes or the reverse. A lookalike that starts costing real English fertility can be added as its own seeded token inside the Latin budget. |
| Digits | One token each. All seven digit sets in the regex. |
| Case | Not folded. `Return` and `return` differ in code. |
| Multi-word tokens | Not in stage 1. A space or a tab stays the first character of the next chunk (`the` + ` ram`), and a stage-1 token does not cross that boundary. Stage 2 is the only place two stage-1 chunks are joined, and only under [Stage 1 and stage 2](#stage-1-and-stage-2). |
| Morphology / sandhi | Not used. Splitting a word into morphemes raises tokens per word. That is the wrong direction. |

### Seeds that are not left to chance

These come out of the budgets below. They are not added on top of 65,536.

Latin, forced before free merges:

- the 256 bytes
- newline, CRLF, and tab as their own tokens
- newline plus 1 through 8 spaces, and newline plus 1 through 4 tabs
- the bare runs of 2, 4, and 8 spaces

From the Nemotron Math 4+ text inside the math sample (`datasets/nemotron-cc-math-v1/4plus/`), every command that occurs at least 50 times, capped at 512 commands. A command is a backslash followed by letters. `\frac` has to be in this set. A read of that prefix and of `4plus_MIND/` found a LaTeX command in about 84% of sampled rows, and `\frac` in 304 of 549 rows of 4+. A seed list without `\frac` means the draw missed the math text.

Per Indic script, forced before word merges: every assigned letter, mark, and decimal digit in the primary Unicode block. Counted from `unicodedata` 15.0.0 on the machine that drafted this plan. Re-count on the training machine. They occupy slots **inside** that script’s budget.

| Script | Letters + marks + digits | Notes |
| --- | ---: | --- |
| Devanagari | 125, plus danda and double danda = 127 | Shared by Hindi and Marathi. Nukta U+093C and virama U+094D are inside the marks. |
| Bengali | 85 | Uses the Devanagari danda already counted. |
| Gujarati | 89 | |
| Tamil | 61 | No nukta in this block. Virama is inside the marks. |
| Telugu | 91 | |
| Kannada | 90 | |

Devanagari Extended (Vedic, U+A8E0–U+A8FF) is not seeded. Byte fallback covers it. That fallback is three tokens for a rare character, which is acceptable. It is not acceptable for a normal letter.

### Three models tonight

Not this train. Stage 1 is one mixed akshara-constrained BPE on the 15 GB sample. Picky stays off. Do not train U, S, or R, and do not run a second joint train beside stage 1. The ship rule is in [Stage 1 and stage 2](#stage-1-and-stage-2): ship stage 2 only if every language’s tokens/word is ≤ stage 1, otherwise ship stage 1. If stage 1 misses the engineering bar, the backup is 81,920, not stage 2. The table below is the comparison that was closed. Do not run it.

Same regex, same sample, same 65,536 cap. The notes say which of these would have been preferred. They are not steps.

| Candidate | What it is |
| --- | --- |
| **U, default** | Union of per-script BPEs with the slot table below. Each script is trained twice: vanilla BPE, and the same run with Picky refinement at T = 0.9. |
| **J, ablation** | One joint BPE on the mixed sample, no per-script cap. MUTANT found a joint 200k train beat a stacked merge of script tokenizers. Stage 1 is that shape, plus the akshara rule. U is not trained. 65,536 is still the stage-1 budget. The slot table is the starvation diagnostic, not a cap enforced during the merge. |
| **S, control** | SentencePiece Unigram, `vocab_size=65536`, `model_type=unigram`, `character_coverage=1.0`, `byte_fallback=True`, `split_digits=True`, `normalization_rule_name=identity`, `remove_extra_whitespaces=False`, `add_dummy_prefix=False`. Fed documents through `sentence_iterator`, because its file reader deletes newlines. This is the old plan. It is not trained. |
| **R, retrofit** | Sarvam-1’s Indic pieces for the seven languages, retargeted into this regex, with Malayalam, Odia, and Gurmukhi removed and the freed slots retrained on Latin, code, math, and LaTeX. Scored only if `sarvamai/sarvam-1`’s tokenizer file loads and its license allows a derivative. Otherwise R does not exist. |

Old ship rule, not used:

- If only one passes, ship it.
- If more than one passes, ship the one with the lower tokens/word on the worst Indic language, provided English, code, and math still pass, including the LaTeX command gate on the math eval. A tie on that worst language goes to the lower English tokens/word, then to U.
- If none pass, do not start the 1.2B run. Use the repair rule. Do not raise the vocabulary.

### Candidate R, if the file loads

The three languages Sarvam has and this model does not are Malayalam, Odia, and Punjabi. Those are three scripts (Malayalam, Oriya, Gurmukhi), and their UTF-8 blocks do not overlap Devanagari, Bengali, Gujarati, Tamil, Telugu, or Kannada. Hindi and Marathi stay. They share a script. Sarvam’s vocab is 68,096, with 4,096 described as reserved, so it does not fit in `uint16` until it is cut to 65,536.

Do not keep Sarvam’s encoder. It is SentencePiece: spaces become `▁` (U+2581), unknown bytes become `<0xHH>`, and the model file is `tokenizer.model`, not a byte-level merge list. That encoder is the code and math problem. A newline, a run of spaces, or a digit glued inside a SentencePiece normalizer cannot be repaired by swapping in a code token. BPE never sees a cut the normalizer already made.

What to keep is the strings, not the encoder.

**Counting.** A vocab entry belongs to a script, not to a language. Hindi and Marathi are both Devanagari, so no rule on the string can split them. Decode the piece (`▁` is a space, not a letter). Ignore `<0xHH>` bytes, `<unk>`, `<s>`, `</s>`, and the `<<reserved_token_*>>` ids. If every Indic character is in one Unicode block and there is no Latin letter, the piece is that script. Blocks: Devanagari `0900–097F` plus `A8E0–A8FF` and `1CD0–1CFF`, Bengali `0980–09FF`, Gurmukhi `0A00–0A7F`, Gujarati `0A80–0AFF`, Oriya `0B00–0B7F`, Tamil `0B80–0BFF`, Telugu `0C00–0C7F`, Kannada `0C80–0CFF`, Malayalam `0D00–0D7F`. A piece with two blocks is mixed. Do not count a raw byte: a lone `e0` is a scaffold, not a script. To separate Hindi from Marathi, encode held-out text of each language and count which ids fire. An id that fires in both belongs to both.

Counted on `sarvamai/sarvam-1` `tokenizer.json`, 68,096 pieces:

| Bucket | Pieces |
| --- | ---: |
| Latin | 13,591 |
| Devanagari (Hindi and Marathi together) | 12,126 |
| Telugu | 5,916 |
| Kannada | 5,693 |
| Bengali | 5,299 |
| Gujarati | 5,274 |
| Tamil | 5,100 |
| Gurmukhi (Punjabi) | 4,751 |
| Reserved | 4,096 |
| Malayalam | 3,592 |
| Oriya (Odia) | 1,956 |
| Bytes | 256 |

Malayalam + Oriya + Gurmukhi = 10,299. Dropping only those three leaves 57,797, which is still 2,261 over 65,536. Dropping the 4,096 reserved ids as well leaves 53,701, and the refill up to 65,536 is 11,835 new pieces, on top of the 13,591 Latin pieces already kept. That is the code and math budget. It is not a fertility score.

1. Load the file. Run the smoke table through Sarvam’s own encode/decode before changing anything. Record whether `\n    `, `65`, `\frac{1}{2}`, `don't`, and `गया।वह` round-trip and where they split. That table is a measurement of their encoder. It is not a template for ours.
2. Identify a piece by the Unicode blocks of its characters, as in the count above. Drop it when every Indic character is in Malayalam, Oriya, or Gurmukhi and it has no Latin letter. On this file that is 10,299 pieces. A kept string never contains one of those characters, and none of the 104,323 merges builds a kept piece out of a dropped side, so deleting them does not change how Hindi, Tamil, or English encode. Also drop the 4,096 `<<reserved_token_*>>` ids, any piece that contains a digit, and any piece with `▁` in the middle. Do not drop by id range. After the deletion, delete merges whose output was dropped, and renumber what remains from zero. Old Sarvam ids are not kept.
3. Re-express each kept string as byte-level merges under our regex, shorter pieces first, and only if our regex emits that string as one pre-token or as a slice of one. A Sarvam token our regex can never see is dead weight. Do not import it.
4. Count the kept pieces. Add the 256 bytes and the 32 specials. The remainder up to 65,536 is the new Latin, code, math, and LaTeX budget. Train it with our regex, on the Latin side of the sample only, so the new slots are not spent on Hindi again. If the kept Indic set plus bytes plus specials is already over 65,536, drop the least frequent kept Indic pieces until it fits. Do not drop seeded letters, marks, or digits.
5. No second cross-word recipe inside R. The only cross-word stage in this plan is [Stage 2](#stage-2): `tokenizer-stage2.json` stays at 65,536 and reuses rare learned slots of the same script. It does not add ids, and it does not overwrite `tokenizer-stage1.json`. MUTANT’s cross-word stage made Tamil, Kannada, and Telugu worse on their file because English phrases took slots from a shared list. Do not repeat that by letting a Latin phrase replace an Indic piece.

R still has to pass the same gate as U. A better Hindi number does not excuse a broken indent.

### How U is trained

Not this train. Stage 1 does not build a per-script union. The steps below are the union procedure this plan no longer runs.

Specials are added once, at union, not inside every script model.

1. **Latin model.** Train on English, code, math, and LaTeX only. `vocab_size = 256 + 25,840`. The 256 are the bytes. The 25,840 are learned Latin pieces, including the indent seeds and the LaTeX seeds. Code and math are not their own blocks. In Sarvam they sit inside Latin, and they sit inside Latin here.
2. **One model per Indic script.** Devanagari is trained on Hindi **and** Marathi, in the word proportions in the sample section. Telugu is not in the Kannada model. Tamil is not in anyone else’s model.
3. Indic trainer size is `256 + script budget + 2,000` of headroom. The headroom is throwaway. Indic text contains ASCII punctuation, and those merges must not take home a global slot.
4. From each Indic model, **keep** tokens that contain at least one byte `>= 0x80`, in that model’s merge order, until the script budget is full. Drop pure ASCII tokens. A leading-space Hindi token is kept, because it contains Devanagari bytes. It does not collide with an English token.
5. If a script cannot fill its budget, raise that trainer’s `vocab_size` and rerun only that script. Do not steal from Tamil to hide a short Bengali list.
6. Concatenate: 256 bytes once, 32 specials, Latin merges, then Devanagari, Tamil, Telugu, Kannada, Bengali, Gujarati, in that order. Within a script, the original order stays.
7. Assert the piece count is exactly 65,536. Assert each of the six script blocks contains learned tokens beyond its seeded letters, marks, and digits. Zero learned tokens in a script is a failed run. Assert a Devanagari sentence tokenizes the same under the union as under the Devanagari-only model (ASCII-only tokens aside), and do the same check for one sentence in each other script. A mismatch means the ranks were interleaved wrong. On the eval, if the union’s tokens/word on a language is worse than that script’s own model, that union is a failed stack. MUTANT’s stacked merge did this to Hindi on their file, 1.21 under the Hindi-script tokenizer and 1.55 after the stack. That regression is a broken union. It is why stage 1 is one mixed BPE, not a stack.

Specials, 32 ids, inside the 65,536:

| Id preference | Piece | Job |
| --- | --- | --- |
| 0 | `<unk>` | Must not appear on real text. Byte-level encoding has no unknown byte. |
| 1 | `<s>` | Beginning of sequence. |
| 2 | `</s>` | End of sequence. |
| 3 | `<pad>` | Pad. |
| 4 | `<eod>` | Document boundary when several documents are packed. |
| 5–31 | `<reserved_0005>` … `<reserved_0031>` | Unused. A later chat template can use them without growing past 65,536. |

If the library assigns different ids, the freeze file is the authority. The dataloader reads that freeze file. It does not hard-code this table.

### Picky refinement, inside each script

Picky stays off. Do not run it on stage 1, on stage 2, or on a per-script trainer. The notes below are what it would have done. They are not steps for tonight.

Do not add it to S. Unigram already throws pieces away by likelihood. Do not run it once on a union. A deleted Tamil scaffold would have had to free a Tamil slot, not an English one. That question does not come up, because Picky stays off.

Picky BPE (Chizhov, Arnett, Korotkova, and Yamshchikov, 2024) is vanilla BPE plus one check after every merge. For a merge of `x1` and `x2` into `x3`, Intersection over Self is the pair’s frequency divided by the token’s own frequency. If that ratio is at least `T`, the token is almost only ever seen inside this merge, so it is a scaffold (`entucky` inside `Kentucky`) and it is deleted. The slot is filled by a later merge. The final vocabulary size stays exactly the budget. Their `T = 1` is vanilla BPE. Their published compression change at 65,536 tokens and `T = 0.9` on English–German news text is about 0.2% fewer tokens, and about 1,149 tokens replaced. That is a cleanup of the table, not the fertility win. The regex is still the fertility win. Their own limitation section says the threshold starts high, and that they did not test Indic scripts.

Not used. Recorded so it is not reopened:

| Choice | Value |
| --- | --- |
| Threshold | **0.9 only.** Do not sweep 0.6, 0.7, or 0.8. Lower values delete useful tokens. Their paper says so. |
| Where | Not run. Not inside stage 1, and not inside stage 2. |
| Protected, never deleted | The 256 bytes, the 32 specials, every seeded letter, mark, and digit, the indent seeds, and the LaTeX command seeds. A virama’s IoS is near 1 because it almost never survives as its own token. Deleting it makes a rare conjunct fall back to three bytes. The protected list is the difference between their algorithm and a safe one for this model. |
| What may be deleted | An unprotected scaffold: a byte pair or a half-word that exists only so a longer token can be built, and that is not on the protected list. |
| Second chance | If a deleted token becomes frequent again later, their algorithm may merge it back. Keep that behavior. Do not invent a stricter one. |

If it were run, which it is not, the encoder would be their event log: merges and removals in the order they happened. Hugging Face BPE does not replay a removal. Their Appendix A shows the failure mode. Vanilla merges run to the end, then a deleted piece is split, and a merge that should have happened *after* the removal never fires. The string is different. The unused requirements were:

- Store the event log next to the vocab. The training dataloader uses that encoder.
- A conversion into `tokenizer.json` is allowed only if, on every eval string, the Hugging Face encode matches the event-log encode exactly, including token ids. One mismatch and the conversion is thrown away. Ship the event-log encoder.
- Do not “just drop the junk ids” from a vanilla merge list and call it Picky.

The old per-script ship test, not used: ship the Picky version of a script only when, against the vanilla version of **that same script**, tokens/word is better or equal on every language that uses the script, the akshara rate does not get worse, and round-trip still holds. Picky stays off, so this test is not run and no script is switched to Picky.

---

## Slot table

the requester’s target. Each language other than English gets 5,500 learned pieces. English gets every learned piece that remains. These counts sum to 65,536. `tokenizer-stage1.json` stays untouched. The new file is `tokenizer-balanced.json`, still exactly 65,536.

7 × 5,500 = 38,500. Learned pieces are 65,248, so English is 26,748. Code, math, LaTeX, digits, and punctuation sit inside English. Specials stay 32. Bytes stay 256. 26,748 + 38,500 + 256 + 32 = 65,536.

Hindi and Marathi share Devanagari. A piece both languages use is counted once, in the language where it is more common. The other language still uses it. The two 5,500 counts do not overlap, so Devanagari’s combined budget is 11,000.

| Block | Slots |
| --- | ---: |
| Specials | 32 |
| Bytes | 256 |
| English | 26,748 |
| Hindi | 5,500 |
| Marathi | 5,500 |
| Bengali | 5,500 |
| Gujarati | 5,500 |
| Tamil | 5,500 |
| Telugu | 5,500 |
| Kannada | 5,500 |
| **Total** | **65,536** |

Stage 2 is a separate file, running in parallel on a second machine. It keeps Sarvam’s Indic pieces after Malayalam, Odia, Punjabi, English, and reserved ids are removed, then trains our English into the slots that remain. That English block is about 25,840. It does not use the 5,500 caps. `tokenizer-stage1.json` stays untouched. The 5,500 rebalance is `tokenizer-balanced.json`.

The table below is the old Sarvam diagnostic. It is not the target anymore.

Targets for candidate U. They sum to 65,536. Learned counts include that script’s seeded letters. They are not added again.

Not this train’s allocation. Stage 1 is one mixed BPE with a vocabulary of 65,536. This table is the diagnostic: after that train, count pieces per script. Stage 2 does not add rows and does not move a slot from one script to another. It may reuse a rare learned piece inside the same script, under the ceilings in [Stage 2](#stage-2). Specials, the 256 bytes, and single-character pieces stay.

Indic stays at Sarvam’s own counts. Those counts are a slot budget, not a quality ceiling. The gate is still to beat the best tokenizer we can load, Sarvam included. A single script in their file is already 5,100–5,916 pieces. Beating them comes from the regex and from training the pieces on our sample, and from a Latin block of 25,840 against their 13,591, not from copying their fertility. Picky stays off. Scaling the Indic counts up would spend the new room on scripts that are not the weak side. Devanagari is the exception in their file: 12,126 pieces, because Hindi and Marathi share it, about 6,000 per language. It stays 12,126. It does not become 6,000 for both languages together.

Specials stay 32, not 4,096. Bytes stay 256. Code, math, and LaTeX stay inside Latin. The leftover is Latin’s: 65,536 − 32 − 256 − 39,408 = 25,840. Their Latin block was 13,591. Ours is larger because the 4,096 reserved ids and the three scripts we do not train are not copied, and because Indic was not inflated.

| Block | Slots | Role |
| --- | ---: | --- |
| Specials | 32 | The table above. Not Sarvam’s 4,096. |
| Bytes | 256 | The alphabet. Also the fallback. |
| Latin learned | 25,840 | English, code, math, LaTeX, indents, operators, LaTeX commands. This is where the spare budget goes. |
| Devanagari | 12,126 | Hindi and Marathi together. Sarvam’s count. One alphabet, two fertility rows. |
| Telugu | 5,916 | Sarvam’s count. Own script. |
| Kannada | 5,693 | Sarvam’s count. Own script. Not pooled with Telugu. |
| Bengali | 5,299 | Sarvam’s count. |
| Gujarati | 5,274 | Sarvam’s count. |
| Tamil | 5,100 | Sarvam’s count. Smallest of the six. The repair below can raise it. The first train does not. |
| **Total** | **65,536** | |

32+256+25,840+12,126+5,916+5,693+5,299+5,274+5,100 = 65,536.

There is no empty repair pool in the old union. Those moves are not stage 2, and they are not the mixed train. After a union score, which this train does not produce:

- If English, code, or math misses its rule, move 2,048 from Devanagari (12,126 → 10,078) onto Latin (25,840 → 27,888) and retrain those two. Do not touch Tamil, Telugu, or Kannada to buy English.
- If Tamil misses and Devanagari passes, move 816 from Devanagari onto Tamil so Tamil matches Telugu’s 5,916, and retrain those two.
- If another Indic language misses and Devanagari passes, move up to 2,048 from Devanagari to that script and retrain those two.
- If the akshara gate fails, seeding happens inside the failing script’s current budget.

Stage 1 ignores this table while training. The table is still the diagnostic: if stage 1 has under 2,000 pieces whose first non-space character is in a given script, that script was starved. That is a failed stage 1, not a reason to widen the vocabulary, and not a reason to ship stage 2.

### If the vocabulary is 96,000

Hindi and Marathi are separate budgets. They are not one Devanagari block. Hindi is 10,000. Latin is 40,000 learned pieces. Specials stay 32 and bytes stay 256, which leaves 45,712. That remainder is split across Marathi, Tamil, Telugu, Kannada, Bengali, and Gujarati. 45,712 = 6 × 7,618 + 4, so four of them get one extra id.

| Block | Slots | Role |
| --- | ---: | --- |
| Specials | 32 | Same 32. Not a reserved pool. |
| Bytes | 256 | The alphabet. |
| Latin learned | 40,000 | English, code, math, LaTeX. |
| Hindi | 10,000 | Hindi text only. Devanagari. |
| Marathi | 7,619 | Marathi text only. Devanagari. Not pooled with Hindi. |
| Tamil | 7,619 | Own script. |
| Telugu | 7,619 | Own script. |
| Kannada | 7,619 | Own script. |
| Bengali | 7,618 | Own script. |
| Gujarati | 7,618 | Own script. |
| **Total** | **96,000** | |

32+256+40,000+10,000+7,619+7,619+7,619+7,619+7,618+7,618 = 96,000.

Latin trainer: `vocab_size = 256 + 40,000`. Code and math stay inside that model. Against the Latin-side word mix the expected piece counts are English 25,384, code 9,231, math 5,385. The 3,846 that had been the LaTeX expectation are in the English count. A check, not a cap. Code under about 4,600 pieces means the Latin sample was too much English web. Retrain Latin on the same 40,000.

Hindi and Marathi each get their own trainer. Hindi’s trainer sees Hindi only and keeps 10,000 pieces. Marathi’s trainer sees Marathi only and keeps 7,619. The alphabet is the same script, so the same string will come out of both. Union by exact string: one string, one id. The ids saved by that intersection go back to the two trainers, next merges not already kept, in proportion 10,000 : 7,619, until the unique pieces from the two lists sum to 17,619. A shared string is one row in the table and it counts in both fertility scores. Nothing in the characters of a Devanagari string says Hindi or Marathi. The training text is the split.

Tied at hidden size 2048, 96,000 rows are 196,608,000 parameters.

Repair stays after the 15 GB score. This 96,000 table is not the train. Dead ids, pieces that never fire on the eval, move first. If one of the equal-budget languages misses and Hindi passes, move up to 2,048 from Hindi onto that language. Latin’s 40,000 is not the donor for an Indic miss. If English, code, or math misses, retrain Latin inside 40,000. Take from Hindi only if that retrain still misses and Hindi passed.

This 96,000 table is not the one to train on a mix that is about 750B English and 250B for the other languages together. Those Indic rows are 55,712 of 96,000, and every English token still multiplies by them. The run that matches this mix is the 65,536 table above: all seven languages, each script near the 5,100–5,916 floor, Devanagari split into a Hindi trainer and a Marathi trainer whose unique rows stay near 12,126, Latin at 25,840. Cutting a language is a product cut. It is not required to make the 250B affordable. A script budget near 2,000, which is what a 25% token share would assign, spends that 250B on fragments and lets those documents take extra positions from English.

---

## What other Indic tokenizers already measured

These numbers are theirs, on their files. None of them is our score. They change what we refuse to copy.

**The regex is the fertility win, and it is already prior art.** MUTANT trained one stage-1 BPE twice. GPT-2’s letters-only pattern scored Hindi 3.47, Bengali 4.72, Tamil 6.53, Telugu 5.61, Kannada 5.95, Gujarati 4.12, Marathi 4.86. The same train with a Llama-4 / mark-aware pattern scored 1.36, 1.74, 2.07, 1.83, 2.15, 1.83, and 1.61. English moved from 1.32 to 1.33. Code moved from 1.57 to 1.54. The vowel-sign paper’s census found the letters-only class in 63.3% of the most-downloaded text-generation repos, and found GPT-4o’s o200k pattern already mark-aware. Qwen3.5’s published word class is `[^\r\n\p{L}\p{N}]?[\p{L}\p{M}]+`. Ours is that family, plus ZWJ and ZWNJ (they are category Cf, so `\p{M}` does not keep them), plus the danda exclusion, plus one digit at a time. Do not load Llama 4’s vocabulary because its regex is the right family. On MUTANT’s file the shipped Llama 4 tokenizer still scores Tamil at 5.87. The regex and the merge list are different objects.

**A stacked merge can silently get worse.** MUTANT’s script-specific tokenizers, scored alone, beat the tokenizer they got by stacking those vocabularies (Hindi 1.21 alone, 1.55 stacked; Telugu 1.40 alone, 1.95 stacked). Their joint 200k train then landed near the alone numbers. This train is that joint shape: one mixed BPE, not a stack of per-script lists. Do not explain a gap as “multilingual interference” and keep a stack.

**Multi-word tokens buy English and do not buy Dravidian.** MUTANT’s stage 2, the SuperBPE curriculum, lets merges cross spaces after 90% of a 200k vocab, and it forbids merges across sentence boundaries and across danda. On their file English went from about 1.33 to 1.12 and code from 1.54 to 1.47. Tamil went from about 2.07 to 2.12, Kannada from about 2.15 to 2.19, Telugu from about 1.83 to 1.88. Kannada and Telugu moved with Tamil. Their 1B downstream comparison of stage 1 against stage 2 is mixed and small. That regression comes from letting English phrases take slots in a shared list. [Stage 2](#stage-2) does not do that. It stays at 65,536 and reuses a rare learned piece of the same script, and only when the pair is more frequent than the piece it replaces. A removed piece can raise tokens per word, so stage 2 ships only when every language is at or below stage 1. Danda as a hard boundary is already in our regex, which is the part of their stage-2 regex we keep. The English gate below does not use a multi-word baseline as the veto, and stage 2 does not loosen it.

**More data stops moving fertility before it gets large.** Same paper, stage 1, 200k, 22 languages: English is 1.33–1.34 from 1GB through 50GB. The average is flat after 10GB. Tamil does not improve from 1GB to 50GB on that file. Bengali does move from 1GB (2.32) to 10GB (1.74) and then stops. The mixed sample is 15 GB, which is past the point where their average stopped moving. A language that misses with a healthy shatter test gets more of its own words rather than a bigger mix.

**NFKC and morphology are not free compression.** Their NFC / NFD / NFKC fertility table differs in the fourth decimal place (Hindi 1.2250 NFC, 1.2239 NFKC). That is not a reason to NFKC, and NFKC can delete ZWJ. They tried a morphological pre-segmenter and left it out of the final tokenizer because of inference latency. We do not run one either.

**Specialist tables pay for their Indic score on English and code.** On MUTANT’s file Sarvam scores English 1.66 and code 2.14, against Llama 4 at 1.34 and 1.46. BrahmicTokenizer, comparing at its own 131k budget, reports Sarvam-1’s English 15.9% worse and its code and math 26–33% worse than a tokenizer that kept o200k’s English merges. akshara-tokenizer v1.2, which spends about 92% of a 64k table on aksharas, reports English at 2.151 against Qwen3 at 1.261 on FLORES, and says the native-script win is partly that specialization. It also loses on romanized Indic and on Hinglish, which are Latin-script text. We do not pre-split aksharas, we do not reserve 4,096 empty ids the way Sarvam does inside 68,096, and we do not inherit Sarvam, Sutra, o200k, or Llama 4 merges. Sutra’s own writeup is a SentencePiece model merged onto a pretrained English tokenizer. That is how a broken English regex survives into the Indic model.

**A script with no tokens is not a high fertility. It is a missing alphabet.** BrahmicTokenizer’s Odia gain came from adding 725 Oriya-block tokens to a tokenizer that had zero. After the 15 GB train, count learned tokens that never occur in that sample. A script with none, beyond its seeds, is a failed run. A script whose learned tokens mostly never fire gets more of its own text and a retrain of stage 1, into a new file, before a slot is taken from a script whose tokens do fire. Do not overwrite `tokenizer-stage1.json`.

---

## Sample

Three sizes. Same word shares, same held-out eval. Do not count any of them in model tokens. The token count is what the experiment is measuring, and a broken regex inflates it. The unit is UTF-8 bytes after NFC, after eval ids are removed.

| Run | Bytes | What it is allowed to decide |
| --- | ---: | --- |
| Plumbing | 2×10⁷ (20 MB) | Stage 1 lands on 65,536 on a scaled-down budget, round-trip, indent is one token, no `<unk>`. Picky stays off. Fertility on this file is noise. Gujarati is 5% of words and its block is 5,274. 20 MB does not give that bucket enough repeated words to fill it. |
| Decision | **2×10⁸ (200 MB)** | First real fertility table for the one mixed BPE. Score the full eval, not a smaller one. This can kill a regex, and it can kill a run that is still shattered or that starves a script. It cannot freeze, and it cannot stand in for stage 2. |
| Final | **1.5×10¹⁰ (15 GB)** | The one mixed sample. Train stage 1 here. Stage 2 counts candidate pairs on each language’s own slice of this sample, not on the shuffled mix. This is the run that may freeze. |

15 GB is the one mixed sample both stages train on, not a prelude to a bigger one. MUTANT’s sweep, at 200k and 22 languages, left English flat from 1GB to 50GB and the average flat after 10GB. Bengali on their file still moved between 1GB and 10GB, then stopped. 15 GB is past that plateau. It is not a claim that every language has saturated. A language that misses with a healthy shatter test gets more of its own words and a retrain of stage 1, written to a new file. That retrain does not overwrite `tokenizer-stage1.json`. More English text will not buy the missing pieces back from a 128k English table. This size is not a measured size of any source, and it is not the 710B model run. Do not stream the full corpus.

The 200 MB run exists so a bad regex or a starved script shows up before the 15 GB train. A gap of the size in the vowel-sign paper (Hindi around 3 tokens/word broken, around 1.3 repaired) cannot hide at 200 MB. A 1% argument between two healthy tokenizers can. That argument waits for 15 GB. Picky stays off, so this run is not a Picky comparison.

Shares are of **whitespace-delimited words**, not of characters and not of Sangraha bytes. An Indic word has more code points than an English word, so a character budget under-feeds Indic. A Sangraha byte budget over-feeds Hindi.

| Bucket | Share of words | Where it comes from |
| --- | ---: | --- |
| English | 33% | Half ClimbMix, half the English crawl. ClimbMix has no prefix and no measured size. The crawl that is actually in the bucket is `datasets/nemotron-cc-hq/` (1,110,302,262,436 bytes). That prefix is not ClimbMix. Its size is not this share. The extra 5 points are the old LaTeX bucket, drawn from these same two English sources. |
| Code | 12% | CodeAlchemy and Nemotron Code, half and half if both exist. Neither has a prefix or a measured size. If only one exists, it fills the 12%. Do not substitute Code-Concepts or Scientific-Coding. |
| Math | 7% | Even split across Finemath, Nemotron Math 4+ (`datasets/nemotron-cc-math-v1/4plus/`, 62,189,080,483 bytes stored), math textbooks (`.../Nemotron-Pretraining-Math-Textbooks/`, 30,841,263,255 bytes stored), and SwallowMath. Finemath and SwallowMath are not measured. If one of those two is missing, split its share across the two that are present and write that down. This is also the LaTeX text. A range read of 4+ and `4plus_MIND/` found a LaTeX command in 462 of 549 rows and 503 of 600 rows. There is no separate LaTeX bucket and no outside LaTeX corpus. |
| Hindi | 9% | Devanagari. See the Indic split. |
| Marathi | 7% | Devanagari. Own words. Not a Hindi duplicate. |
| Bengali | 7% | |
| Tamil | 8% | Highest published shatter in this set. Upsampled against Hindi on purpose. |
| Telugu | 6% | |
| Kannada | 6% | |
| Gujarati | 5% | |

33+12+7 = 52 on the Latin side. 9+7+7+8+6+6+5 = 48 on the Indic side. The old 5-point LaTeX row is inside the 33.

Inside each Indic language’s words:

| Slice | Share of that language | Source |
| --- | ---: | --- |
| Sangraha verified, native script | 50% | `verified/hin`, `mar`, `ben`, `tam`, `tel`, `kan`, `guj`. No `*_Latn`. No `verified/eng`. |
| IndicCorpV2 | 25% | No prefix and no measured size. Not `datasets/fineweb2-indic/`. If the files are absent, give this quarter to Sangraha verified and write it down. |
| Translated Cosmopedia | 25% | Higher-quality Indic. Preferred prefix `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v5-20260906/` (55,220,425,599 parquet bytes, all languages together). Per-language size was not measured. Drop quarantined rows. |

The curriculum cap that keeps Hindi at 25% of Indic **training** tokens does not apply here. Hindi’s 9% is already the cap for this sample.

Write a manifest: source, document id, byte length, word count, bucket. Land within 2% of each word share. If a language cannot fill its share, train with what you have and expect that language to fail. Do not give the shortfall to English.

Cap a training document at 4,000 characters, on a character boundary, in the tokenizer sample only. Eval documents stay whole.

---

## Eval

Carve these document ids before the sample. No id is in both. Do not copy a fertility number from a paper into the result table. The table starts empty.

| Set | Sampling target | Drawn from |
| --- | ---: | --- |
| English | 1,000,000 characters | The same source as the English sample, held out. 500,000 of these are the characters that had been reserved for a separate LaTeX collection. |
| Each of the other 7 languages | 500,000 characters | The same source as that language’s sample, held out |
| Math | 500,000 | Math 4+ and textbooks, held out. LaTeX command coverage is scored on this set. |
| Code | 500,000 | The same code source as the sample. If that text does not exist yet, the code cell is blocked. Do not silently swap in another code set. |

Fixed fixture, run every time, separate from the corpus: `ड़`, a ZWNJ, one Kannada word, one Telugu word, `\frac{1}{2}`, a newline followed by four spaces, a tab, `don't`, one Hinglish line, and one romanized Hindi line. The last two are Latin-script text. Score them with the English metric and write the number down. They are not a separate gate.

### Metrics

1. **Tokens per word.** Split words on space, tab, LF, and CR only. ZWJ and ZWNJ do not split a word. Do not lowercase. Do not strip punctuation. Skip a whitespace-only string for this ratio.
2. **Tokens per character.** Token ids divided by Unicode code points. An Indic letter is one character.
3. **Round-trip.** `decode(encode(x)) == x` with no Unicode normalization before the compare. Required on every code file and every Indic file. Record it on English and math too. Score fertility on the original string. Do not NFC the eval so that a baseline looks closer. If a baseline’s decode is NFC of the input rather than the input, record that and still count its tokens on the original string. Qwen3 has been reported to NFC inside the tokenizer. Confirm it on the file you load.
4. **Akshara split rate.** The checker above. Per Indic language.
5. **Pre-tokens per word.** The shatter test. This is a property of the regex, so U, J, and S can differ only if S is cutting differently. Record it anyway.

A baseline that throws, or that emits unknown-token ids, is a blank cell. It is not a fertility of zero.

### Baselines

Load the file. Record the repo id and the hash. Leave the row blank if the file is not obtainable. Do not type in a number from a model card.

| Baseline | Load | Note |
| --- | --- | --- |
| TinyLlama | `TinyLlama/TinyLlama-1.1B-Chat-v1.0`, revision `fe8a4ea1ffedaf415f4da2f062534de366a451e6` on the OpenHermes manifest | Already in the packs. |
| Llama 3, Llama 3.1, and Llama 4 | The tokenizer shipped with each weight release | Confirm the file is obtainable under Meta’s license. Do not assume the files match. Llama 4’s regex family is mark-aware. Its shipped vocabulary is a separate question: run the shatter test, and do not treat a good regex as a good Tamil number. |
| Gemma 2 and Gemma 3 | One checkpoint each | Confirm the file is obtainable. If only one is reachable, drop the other row. |
| Qwen2.5 | A base checkpoint, repo id recorded | If the file is a coder variant, label it. Published measurements put Qwen2.5 in the letters-only pre-tokenizer class. Confirm on the file you load by running the shatter test. |
| Sarvam-1 | The 68,096-token tokenizer if the file downloads. About 4,096 of those are described as reserved. | Confirm the file is obtainable. OpenHathi is a Llama-2 table extended mainly for Hindi. A good Hindi number from OpenHathi says nothing about Kannada or Telugu. Load it only if the file is there, and label it. |
| AI4Bharat IndicTrans2 | SentencePiece from `ai4bharat/indictrans2-en-indic-1B` | Confirm the vocab file is in the repo. |
| IndicBERT or IndicBERTv2 | The WordPiece vocab you can actually download | Encoder tokenizer. Fair as a compression baseline. A weak generative drop-in, because of whitespace. Confirm the file. |
| akshara-tokenizer v1.2, and the Arkios 65,536 tokenizer, if the files download | Public repos under those names | Closest published relatives. Confirm the file. Their English behavior is part of why we measure them. |

### Engineering acceptance bar

No fertility number in this section was measured on our files. Passing this bar is what “good enough to train” means. It does not establish state of the art. An empty result table is not state of the art. The second layer below is what has to be measured before anyone calls the tokenizer that.

| Gate | Rule |
| --- | --- |
| Hindi, Marathi, Kannada, Telugu, Tamil, Gujarati, Bengali | Tokens/word **at or below** the best baseline on that same file. No cushion. Kannada and Telugu are separate rows. Hindi and Marathi are separate rows. A large Indic gain does not relax this row, and it does not relax English either. |
| English | Tokens/word **≤ 1.08 ×** the best baseline on that same file that does not use multi-word tokens. The 8% is the acceptance rule. A multi-word token is one whose decoded form contains a space or a newline that is not a single leading space and not one of the indent seeds. Write the multi-word baselines down. They are not the veto. MUTANT’s stage 2 moved their English from about 1.33 to 1.12 and moved Tamil the wrong way, from about 2.07 to 2.12, on their file, because English phrases took slots from a shared list. Our stage 2 reuses rare Latin slots inside the same 65,536. It does not loosen this 8% rule, and a miss on this row is not repaired by shipping stage 2. The Latin budget is 30,002 learned pieces. Indic stays at Sarvam’s counts, and the spare slots are here. Llama 3’s table is 128k and Qwen2.5’s is about 152k, and most of the extra pieces are English and code. A 3% rule asks this list to land where a table three to four times larger lands. The published anchor we have is the vowel-sign paper’s own 65,536-token bilingual tokenizer: English 1.30 against Llama 3 at 1.24 on the same FLORES file, about 5%, and that paper says the bilingual setup is optimistic for a multilingual mix. Inside 8% ships. At or below the best non-multi-word baseline is better and is what the Latin budget is there to chase. Above 8% after the one repair retrain of stage 1 fails the candidate. |
| Math | The veto is tokens/word **≤ 1.05 ×** the best baseline after every maximal digit run is replaced by one space, the same replacement before every tokenizer. A digit run is one or more ASCII digits, or one or more digits from the six Indic blocks in the regex. Raw tokens/word on the unstripped math set is written down and does not veto. Llama 3, Gemma, and Qwen glue up to three digits, so single-digit pre-tokens lose that raw comparison on the digit spans by construction. Do not turn single-digit splitting off to win the raw number. |
| Code | Tokens/word **≤ 1.05 ×** the best baseline on raw text. Also write down the digit-stripped number, using the same replacement as math. If raw text is outside 5% and the stripped text is inside 5%, the row passes. A miss that is only the digit policy is not a failed tokenizer. |
| Round-trip | Exact on every code sample and every Indic sample. One mismatch fails the candidate. |
| `<unk>` | Zero on every eval set. |
| Akshara split | Zero tokens on each Indic language that break the hard rule: a token ends only on an akshara boundary, does not start with a dependent vowel mark, and does not end on a virama that is still waiting for the next consonant. The fallback path emits no `<unk>`. |
| Shatter | Under 2.0 pre-tokens per word on each of the 8 languages, measured before training. |
| Indents | Each of `\n`, `\n  `, `\n    `, and `\n\t` is exactly one token. |
| LaTeX commands | Every command that covers the top 90% of command occurrences in the math eval set is exactly one token. |

If a language fails fertility and its akshara rate is fine: add words from that language, from ids in neither the sample nor the eval, and retrain the one mixed stage-1 BPE into a new file. Do not overwrite `tokenizer-stage1.json`. Do not grow stage 1 past 65,536. Do not use stage 2’s reused slots as this repair.

If a language fails fertility and the shatter test is also bad: fix the regex. More text will not move the number. This is the failure the first plan would have misdiagnosed as “need more data.”

If code misses: add words from code and retrain stage 1. If the LaTeX command gate misses: add more Nemotron Math 4+ words and retrain stage 1. Do not open a separate LaTeX bucket. A repair retrain is a new file. It does not overwrite `tokenizer-stage1.json`.

Stage 1 is trained first. The 81,920 tokenizer is trained only if stage 1 misses this engineering bar. Stage 2 is not that backup. The 1.2B run waits on a pass here. It does not wait on the layer below.

### Second layer

Run this only after a tokenizer has passed the engineering acceptance bar. Do not call that tokenizer state of the art until these five parts are measured. No number below has been measured. Do not fill one in.

1. **Compression.** On the held-out fertility text, report tokens per word, tokens per Unicode character, and tokens per UTF-8 byte. One row per language (English, Hindi, Marathi, Kannada, Telugu, Tamil, Gujarati, Bengali) and one row each for code and math. LaTeX compression is the math row. Lower is better. Tokens per byte is written down. It is not a gate. Indic letters are three bytes, so a byte rate will flatter a tokenizer that still splits them.

2. **Structural correctness.** Invalid Indic boundaries at **0%**. That is the hard rule already in this plan: inside an Indic chunk, a token ends only on an akshara boundary, does not start with a dependent vowel mark, and does not end on a virama that is still waiting for the next consonant. 0% is the state-of-the-art structural target, not a tolerance. A boundary between two whole aksharas is legal. English, code, math, and LaTeX are not scored on this part.

3. **Robustness.** Held-out sets, separate from the fertility eval: unseen words, names, STEM terminology, code, LaTeX, numbers, URLs, mixed-script text, and Hinglish. Score tokens per word and the akshara rule on each set. Hinglish stays Latin-script text. Score it with the English metric. Do not add it as a training language.

4. **Vocabulary efficiency.** The state-of-the-art compression comparison is against strong baselines trained or truncated to the same vocabulary size, **65,536**. A comparison to Llama 3’s 128k table or Qwen’s about 152k table is reported beside it and is not the apples-to-apples number. The engineering bar’s 8% English rule is a distance from those larger tables. It is not a same-size win. Say that next to the number so the two are not swapped.

5. **LM quality.** Same small proxy architecture, same training tokens, same data, same compute budget, several tokenizers that already passed the engineering bar. Compare validation loss and perplexity. This is the test that the tokenizer makes the model learn better. It is not the 1.2B run. **Assumption, not a measured fact:** the proxy is a **150 million parameter** dense decoder, tied embeddings, and the shared budget is **20 billion tokens**. If the real proxy differs, recompute nothing else in this plan from these two numbers. No perplexity result exists yet. Do not write one down. The 1.2B train still waits only on the engineering bar.

The design those measurements sit on: we do not pre-cut words into syllables before learning, and learned pieces may end only on a legal akshara boundary. A frequent word can still be one token. Do not switch to a pre-cut akshara tokenizer.

---

## What this does to the existing packs

Some existing packs were tokenized with `TinyLlama/TinyLlama-1.1B-Chat-v1.0`. A new tokenizer means those packs must be retokenized. Same `uint16` width does not make the ids mean the same strings. Stage 1 and stage 2 both use ids 0–65,535 and fit in `uint16`. The 81,920 backup does not.

| Pack | Counted on TinyLlama | What to do |
| --- | --- | --- |
| `s3://<research-pack-bucket>/data/nemotron_cc_v2_hqsynth_tinyllama_15b_parallel_20260730T185305Z/` | 15,000,000,001 train tokens, 50,000,001 validation tokens, `seq_len` 2048 | Retokenize from the source text. The 15,000,000,001 figure is not the count under this tokenizer. Recompute the curriculum’s 2-epoch cap as `2 × T` after the recount. |
| `s3://<research-pack-bucket>/openhermes25_assistant_sft_20260803/` | 251,398,213 train tokens, 180,633,498 supervised tokens. Manifest revision `fe8a4ea1ffedaf415f4da2f062534de366a451e6` | Rebuild the loss mask from the source spans (assistant text and the trailing EOS). Old offsets do not point at those spans. |

The unfinished `20260730T1840Z` run and the `test16/` tarballs are the same kind of file. They are not a shortcut.

---

## Stage 1 and stage 2

These decisions are closed.

### Stage 1

One mixed 15 GB sample. One akshara-constrained BPE. The vocabulary is exactly 65,536, including the 32 specials and the 256 bytes. Spaces are kept. A space is the first character of the next chunk (`the` + ` ram`). A stage-1 token does not cross a space.

Save this file as `tokenizer-stage1.json`. Never overwrite it. It is the fallback. A later retrain, and the 81,920 backup, are different files.

Picky stays off.

### Language counts

Both finished files get this measurement. `stage1-language-counts.json` sits beside `tokenizer-stage1.json`. `stage2-language-counts.json` sits beside `tokenizer-stage2.json`. It is not a separate train. It does not change the 65,536 cap or the stage-2 ceilings. Neither count file modifies its tokenizer. Do not keep a separate pair table per language during BPE.

Each file reports exact piece counts, read from the characters of each piece, for Tamil, Telugu, Kannada, Bengali, Gujarati, Devanagari, and Latin. Tamil, Telugu, Kannada, Bengali, and Gujarati are exact: the script is the language. Devanagari is the exact Hindi-and-Marathi total. Latin is the exact English-code-and-math total.

Each file also reports the usage splits. Hindi versus Marathi, and English versus code versus math, are one read of the labeled slices after that tokenizer exists. Tokenize the Hindi slice and the Marathi slice with that file. A Devanagari piece seen only on the Hindi slice is Hindi-only, only on the Marathi slice is Marathi-only, and on both is shared. Tokenize the English, code, and math slices the same way. A Latin piece seen on only one of those slices takes that label. A Latin piece seen on more than one is shared.

Specials, bytes, and punctuation, digits, and spaces stay unassigned. A leading space on a word stays with that word. A piece that is only spaces is the space count. A piece that is only digits is the digit count.

For stage 1, the script counts are tallied as each merge is accepted. The usage splits are the slice read after `tokenizer-stage1.json` exists. That read does not run during BPE. For stage 2, both the script counts and the usage splits are taken from the finished `tokenizer-stage2.json`, after the slot replacements.

### Stage 2

This is a copy of MUTANT’s cross-word stage, kept light. MUTANT (IndicSuperTokenizer) follows SuperBPE. Stage 1 there is ordinary BPE after whitespace pre-tokenization, and it stops at a transition point inside a fixed vocabulary. Stage 2 resumes from that vocabulary with the whitespace constraint lifted, so BPE can merge across a word boundary and form multi-word pieces. Their published example is “in the morning.” Their transition is 90% of a 200,000-entry vocabulary, so the last 10% of a fixed list is the cross-word stage. Appendix C.7 of that paper adds three constraints to the stage-2 regex: do not merge across a sentence delimiter, treat danda and double danda as hard boundaries, and keep numeric segmentation under control.

Match that method where it fits the rules below. Do not invent a different algorithm and call it MUTANT.

What we keep from them:

- Start from the finished word-level tokenizer. Stage 2 does not re-learn stage 1.
- Add merges whose point is a word boundary, the space between two chunks.
- Do not merge across a sentence delimiter or a danda. Our stage-1 regex already isolates sentence punctuation, danda, and double danda as their own chunks, and it already isolates digits. Stage 2 never joins a chunk that does not start with a space or a tab, so those boundaries stay hard, and digits are not glued back together.

What we will not copy:

- We do not lift whitespace and continue byte-level BPE. Continued BPE is how “in the” then joins “ morning” and becomes three words. We do not build that chain.
- We do not let English phrases take another script’s slots. Their stage 2 replaced the tail of a shared 200,000-entry list. On their file English went from about 1.33 to 1.12 tokens/word and Tamil from about 2.07 to 2.12, and Kannada and Telugu moved with Tamil (Kannada about 2.15 to 2.19, Telugu about 1.83 to 1.88).

Our stage 2:

- `tokenizer-stage2.json` is also exactly 65,536. It reuses slots. It does not add ids above 65,535. `tokenizer-stage1.json` is not overwritten. Picky stays off.
- A new piece joins exactly two stage-1 chunks, and only where the second chunk starts with a space or a tab. No three-word chains. No merge inside a word. The new piece is not an input to a further stage-2 merge.
- The akshara rule is unchanged. Each half is already a legal stage-1 piece, and the join is at the space.
- A pair is added only when it is more frequent than the rare learned piece it replaces. Replace only a rare learned piece of the same script. Never replace a special, one of the 256 bytes, or a single-character piece.
- The ceilings are maximums, not quotas. Do not pad. Latin, including code and math, is 2,000. Bengali, Gujarati, Tamil, Telugu, and Kannada are up to 500 each, replaced inside that script.
- Hindi and Marathi candidates are counted on each language’s own slice, so the language is the slice label. They share Devanagari, so the slots they free are the rarest Devanagari pieces, up to 500 per language, 1,000 if both earn them. Identical strings are stored once. Mixed-script pairs get no bucket.
- This is not a second full byte-level BPE. Tied at hidden size 2048, stage 2 adds no rows.

Score both files. Ship stage 2 only if every language’s tokens/word is less than or equal to stage 1. The languages are English, Hindi, Marathi, Kannada, Telugu, Tamil, Gujarati, and Bengali. Otherwise ship stage 1.

The 81,920 backup is still only for a failed stage-1 engineering bar. It is not a substitute for stage 2. Stage 2 is not a substitute for that backup. If stage 1 misses the engineering bar, do not ship stage 2 in its place.

## Tonight

Do the steps in order. Steps 1–3 are the go/no-go. They are short on purpose.

1. **Install and pin.** `tokenizers`. Compile the pattern with `tokenizers.Regex`, not Python `re`. `\p{L}` and `\p{M}` must compile. `\u{0964}` must not be required. No lookaheads. If `Regex` throws, stop. Write the pattern string the engine actually compiled into one file and hash it.
2. **Four checks, then partition, then shatter.** All four go through `Split` + `ByteLevel(add_prefix_space=False, use_regex=False)`. One failure stops the night.
   - **Classes.** `नमस्ते`, `स्कूल`, `संस्कृति`, `தமிழ்`, `ಕನ್ನಡ`, and `हिन्दी` are each one pre-token.
   - **Danda.** `राम गया।वह आया` is `राम`, ` गया`, `।`, `वह`, ` आया`. `गया।वह` is `गया`, `।`, `वह`. The space stays on the next word.
   - **ByteLevel did not put the GPT-2 regex back.** `हिन्दी` through the full `Sequence` is one piece spanning the word, not six.
   - **The rest of the smoke table.** `don't` as one pre-token, `\frac` / `{` / `1` / `}{` / `2` / `}`, `6` + `5`, `foo` + `.` + `bar`, `foo` + `_bar`. Concatenation equals the original string. On about 2,000 words per language, any of the eight languages at or above 2.0 pre-tokens per word stops the night.
3. **Carve eval ids.** Then draw the mixed 15 GB sample from what remains. Same word shares. The sample contains no eval id. The 20 MB plumbing text and the 200 MB decision text are slices of that same mix, not a second recipe.
4. **Plumbing on 20 MB.** Prove stage 1 can land on 65,536 on a scaled-down budget, round-trip, indent is one token, and no `<unk>`. Picky stays off. Do not read fertility off this run.
5. **Decision check on 200 MB.** One mixed akshara-constrained BPE. Score it on the full eval, against every baseline whose file you could load. If shatter, round-trip, or `<unk>` fails, stop. If Indic is still in the broken band or a script is starved, fix that before the 15 GB train. Do not freeze. Do not train stage 2 on this slice.
6. **Stage 1 on the 15 GB sample.** One akshara-constrained BPE. Vocabulary exactly 65,536, including 32 specials and 256 bytes. Spaces are kept. A space is the first character of the next chunk (`the` + ` ram`). A token does not cross a space. Picky stays off. Do not keep a separate pair table per language during BPE. As each merge is accepted, tally that piece from its characters: exact counts for Tamil, Telugu, Kannada, Bengali, Gujarati, Devanagari, and Latin. Specials, bytes, and punctuation, digits, and spaces stay unassigned. Save `tokenizer-stage1.json`. Never overwrite it. After it exists, one read of the labeled slices adds the Hindi/Marathi split and the English/code/math split. Write `stage1-language-counts.json` beside the tokenizer.
7. **Score stage 1** on the engineering bar. This table is the stage-1 result. Blanks stay blank. Count learned tokens that never occur in the 15 GB sample, per script. A script with none beyond its seeds fails. A script whose learned tokens mostly never fire is retrained on more of its own text, into a new file, before any claim that the mix is fine. If stage 1 misses the engineering bar, the backup train is 81,920. Do not use stage 2 as that backup.
8. **Stage 2.** Copy the saved stage-1 vocabulary into `tokenizer-stage2.json`. The vocabulary stays exactly 65,536. Do not add ids above 65,535. Do not overwrite `tokenizer-stage1.json`. On each language’s own slice, count pairs of exactly two stage-1 chunks whose second chunk starts with a space or a tab. A pair replaces a rare learned piece of the same script only when it is more frequent than that piece. Never replace a special, a byte, or a single-character piece. Ceilings, not quotas: Latin 2,000, including code and math; Bengali, Gujarati, Tamil, Telugu, and Kannada up to 500 each; Hindi and Marathi up to 500 each, freeing the rarest Devanagari pieces, 1,000 if both earn them, identical strings stored once. Mixed-script pairs get no bucket. Do not pad. No three-word chains. Picky stays off. After `tokenizer-stage2.json` is finished, write `stage2-language-counts.json` beside it: the same exact script counts, the same Hindi/Marathi and English/code/math usage splits, and the same unassigned specials, bytes, and punctuation, digits, and spaces.
9. **Score both files.** Ship stage 2 only if every language’s tokens/word is less than or equal to stage 1. Otherwise ship stage 1.
10. **Freeze** the file that ships. Record sha256 of both files, regex, special-id map, sample-manifest hash, and both result tables. No quiet retrain after this. Never overwrite `tokenizer-stage1.json`. A repair retrain is a different file.
11. **Only then** retokenize training text, including the HQ-synth source and the OpenHermes source. Recount. Apply epoch caps in the shipped tokenizer’s tokens. Stage 1 and stage 2 both fit in `uint16`.

The 1.2B run waits on step 10. Its token budget is the curriculum’s, not one of the three sizes above.

### Do not do these tonight

- Do not start from TinyLlama, Llama 2, Llama 3, or Qwen merges.
- Do not compile this pattern with Python `re`. `\p{L}` is not a `re` class.
- Do not leave `ByteLevel`’s default regex on.
- Do not drop space or tab from the one leading character of a word. That isolates every space.
- Do not turn single-digit splitting off so math can match a baseline that glues digits.
- Do not NFKC. MUTANT’s own NFC-versus-NFKC table moves fertility in the fourth decimal place.
- Do not run MUTANT’s stage 2 as a continued byte-level BPE, and do not let a Latin phrase replace another script’s piece. Stage 2 reuses rare same-script slots inside 65,536. Do not pad the ceilings.
- Do not keep Sarvam’s SentencePiece encoder, and do not start from Sutra, o200k, or Llama 4 merges. A mark-aware regex is not a merge list. Candidate R may reuse Sarvam’s Indic strings only, under the rules above.
- Do not reserve thousands of empty ids. The 32 specials are the reserve.
- Do not run the indic-nlp normalizer, and do not pre-split on graphemes.
- Do not split aksharas in the pre-tokenizer. That caps fertility at syllables per word. Inside the chunk, do not keep a merge that ends off an akshara boundary.
- Do not emit `<unk>` for a missing akshara or a stray mark. Character ids, then UTF-8 byte ids. The parser returns. It does not throw.
- Do not run a morphological analyzer.
- Do not add a multi-word token inside stage 1. In stage 2, a new piece joins exactly two stage-1 chunks.
- Do not pool Kannada with Telugu, or drop Marathi into Hindi’s word share.
- Do not build the mixed sample from Hindi alone. Marathi keeps its own word share.
- Do not use the curriculum percentages as sample weights.
- Do not open the vocabulary to 96,000 or 256k because a paper used a bigger table. Stage 1 and stage 2 both stay at 65,536. Do not add ids above 65,535. The 81,920 file is only the failed stage-1 backup.
- Do not start the 1.2B run on a tokenizer that missed the gate.
- Do not run Picky. It stays off. Do not replace a special, a byte, or a single-character piece. Do not edit `tokenizer-stage1.json` to make room for stage 2.
- Do not keep a separate pair table per language during BPE. Script counts are the characters of each accepted merge. Hindi versus Marathi, and English versus code versus math, are one slice read after stage 1 exists.
- Do not replay Picky by deleting ids from a vanilla Hugging Face merge list.
- Do not treat 20 MB fertility as a result, and do not freeze from the 200 MB table.
- Do not grow the tokenizer sample past 15 GB to chase a gate.
- Do not overwrite `tokenizer-stage1.json`.
