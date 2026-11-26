# The 65,536-token tokenizer

This is the plan to build. It does not train the model, and it does not start a machine.

## What we are building

The model does not read letters. It reads whole numbers. A **tokenizer** turns text into those numbers and turns the numbers back into the same text. Each number is one **token**. The full list of tokens is the **vocabulary**.

We will build one vocabulary of exactly 65,536 tokens. That is 2 to the 16th power, so each number fits in 16 bits. A later model can use it. That model is a 1.2 billion parameter decoder, hidden size 2,048, with the input table and the output table tied (one shared table, not two). The shared table is 65,536 × 2,048 = 134,217,728 parameters. This document stops at the tokenizer. It does not train that model.

The languages are English (including code and math), Hindi, Marathi, Kannada, Telugu, Tamil, Gujarati, and Bengali.

Indian sentences must break into the same pieces as the original Sarvam-1 tokenizer. Sarvam-1 is a SentencePiece model: a trained vocabulary that writes a space as the special character ▁ (U+2581, the space mark) instead of a normal space. Its vocabulary has 68,096 pieces, which does not fit in 16 bits. English, code, and math are trained into the numbers we free by dropping the Sarvam pieces we do not need.

Two checks define “the same text comes back.” **Round trip** means decode(encode(text)) equals the original text, character for character. **Fertility** means tokens per word. Lower is better. A word is a stretch split only on a space, a tab, or a newline.

## The decision, and why it is the safest high-quality choice

Use a **script router**. A router is a front door. It looks at the text and sends each span to one encoder. Indian-script spans go to the original Sarvam-1 model, unchanged. English, code, and math go to a new encoder trained only on those. Both encoders share one vocabulary of 65,536 ids. No token contains letters from two scripts.

This is the safest way to meet both hard requirements at once. Indian text keeps Sarvam’s own pieces, including the space mark ▁, so a sentence splits the way Sarvam splits it. Code keeps real spaces, real newlines, and real indentation, because code never passes through Sarvam’s space mark.

### Why the other constructions fail

**Calling Sarvam on everything, including code.** Sarvam writes spaces as ▁. Its normal whitespace rules are the known danger for code: indentation is spaces and newlines, and those must survive. We also want English fertility better than Sarvam’s English. Keeping Sarvam’s English pieces spends the slots we need for that.

**One byte-level model for every language.** A byte-level model starts from raw bytes (the 256 possible values in a file) and glues frequent pairs. Sarvam’s pieces were learned with ▁ in them. A byte-level pre-tokenizer never produces ▁, so Sarvam’s merges do not fire. The earlier byte-level trainer also glued raw bytes across an **akshara** boundary. An akshara is one written syllable: a consonant plus the vowel mark that belongs to it. In `training-fault-analysis.md`, that trainer splits the vowel sign `े` inside `नमस्ते` into the broken bytes `e0 a5` and `87`. `stage1-fertility.json` records the result on our holdout: Hindi 2.55 tokens per word, and 94,191 illegal akshara cuts. That trainer is not the Indic path.

**Rebuilding Sarvam’s merges from the finished token strings.** This already failed. Original Sarvam encodes `नमस्ते` as `▁नम` + `स्ते`. The rebuilt file `tokenizer-sarvam.json` encodes it as `न` + `म` + `स्` + `ते` (`training-fault-analysis.md`). The rebuild dropped the ▁ piece with the English bucket, then split whatever was left at the first cut it could make. Long strings that survived still gave Hindi 1.545 tokens per word on our holdout (`sarvam-fertility.json`). That number is not original Sarvam, and it is not a pass. Do not rebuild merges from strings. Do not replay a merge whose left side is ▁ unless the original SentencePiece model is the thing doing the encode.

**A joint train on mixed English and Indic text.** That is the stage-1 file. It does not match Sarvam’s cuts, and its English score on our holdout is 1.514 tokens per word (`stage1-fertility.json`). The full retrain is the same kind of file (English 1.500, Hindi 2.569, `full-fertility.json`). `stage1-language-counts.json` shows the slots were not Sarvam’s slots either (Latin 18,328 pieces in that file).

**Shipping BrahmicTokenizer-131K.** The paper (arXiv 2605.29379) and the file `theschoolofai/BrahmicTokenizer-131K` froze OpenAI’s o200k English and code merges, deleted unused scripts, trained only the missing script, appended those merges at the end, and banned any merge that joins two scripts. English sentences stayed about 96.8% identical. That rule is what we copy. Their budget is what we do not copy. They added about 2,372 Indic slots, Sarvam-1 still beats them on Indic by about 12.7% (their report), and their vocabulary is 131,072. We cannot ship 131,072 ids. We also cannot freeze o200k inside 65,536 and still keep Sarvam’s Indic list. Their pre-tokenizer stayed GPT-2 byte-level, so they never had to cross Sarvam’s ▁ and a real space. We do. The router is how we cross it.

The copied rule, in our direction: freeze the strong Indic side (original Sarvam, not a string rebuild), append a new English side into the freed slots, ban cross-script pieces, and prove it with a sentence match. Their small Indic graft is the opposite budget.

### How the router cuts a string

These rules are the spec. A later test table in Gate 1 and Gate 5 locks them.

An **Indic letter or mark** is a character in one of these Unicode blocks. Devanagari also includes the two extra blocks used when the Sarvam pieces were counted (`tokenizer-plan.md`).

| Script | Blocks |
| --- | --- |
| Devanagari | U+0900–U+097F, U+1CD0–U+1CFF, U+A8E0–U+A8FF |
| Bengali | U+0980–U+09FF |
| Gujarati | U+0A80–U+0AFF |
| Tamil | U+0B80–U+0BFF |
| Telugu | U+0C00–U+0C7F |
| Kannada | U+0C80–U+0CFF |

ZWJ (U+200D, zero-width joiner) and ZWNJ (U+200C, zero-width non-joiner) are invisible characters that change how Indic letters connect. They count as Indic when the nearest letter on either side is Indic. Elsewhere they stay with English.

A **Latin letter** is a letter in the Latin script (Unicode categories Lu, Ll, Lt, Lm, Lo). A digit is not a Latin letter. A punctuation mark is not a Latin letter.

**Protected whitespace** is a maximal run of spaces, tabs, and newlines that is not exactly one ordinary space (U+0020). One ordinary space is a **soft space**. Protected whitespace is always an English span. Sarvam never sees a tab, a newline, or two spaces in a row.

Then, for each remaining stretch:

1. No Latin letter and no Indic letter or mark: English. This is a number, punctuation, or a LaTeX command.
2. No Latin letter: one Indic span, soft spaces included. Send that whole stretch to original Sarvam. A Hindi sentence with ordinary spaces, dandas (।), and digits takes this path. This is the path Gate 1 checks.
3. No Indic letter or mark: one English span.
4. Both Latin letters and Indic letters: mixed. Split on soft spaces, then cut each word:
   - No Latin letter: Indic. `नमस्ते123` and `123नमस्ते` stay one Indic span, so a number glued to a Hindi word is Sarvam’s job.
   - No Indic letter or mark: English.
   - Both: cut where an Indic run meets a Latin-letter run. A digit or a punctuation mark sticks to the run on its left. If the word starts with digits or punctuation, they stick to the run on their right. `helloनमस्ते` is English `hello` plus Indic `नमस्ते`. `नमस्ते123hello` is Indic `नमस्ते123` plus English `hello`. `hello123नमस्ते` is English `hello123` plus Indic `नमस्ते`.

   Then join a run of Indic words back together with the single ordinary spaces between them, and send that whole run to original Sarvam. A space that touches a Latin word stays an English span, a real space character, not ▁. A newline, a tab, or two spaces in a row stay English and are never joined back.

Hinglish `main जा रहा hoon` is English `main`, English space, Indic `जा रहा`, English space, English `hoon`. The Hindi words and the space between them are one Sarvam call, so that space is ▁, the same as in a Hindi sentence. The spaces next to `main` and `hoon` stay real space tokens, because Sarvam’s Latin pieces are deleted. The whole line still does not match Sarvam. Matching Sarvam is required for sentences with no Latin letters, and for Indic words that sit next to each other inside a mixed line.

Encode never runs the English model on a string that still contains an Indic letter. Encode never runs Sarvam on a string that contains a Latin letter. That is what stops a new English piece from cutting an Indian word.

### How a span becomes numbers

**Indic span.** Load the original `sarvamai/sarvam-1` SentencePiece model (`tokenizer.model`). Call it. Read the piece strings (the call that returns `▁नम`, not a fresh BPE). Ignore a single leading `<s>` and a single trailing `</s>` if the file adds them. Our encode does not add begin or end markers. The dataloader, the program that later packs text for the model, can add those later. Map each piece string to our id. If a piece is not in the keep set, stop. That is a failed Gate 1. Do not fall back to letters, and do not invent a merge.

**English span.** Use the English encoder from the training section. It emits ids from the byte alphabet and from the new English tail only.

**Decode.** Walk the ids. A maximal run of ids that have a Sarvam piece attached is decoded by the original SentencePiece model (`DecodePieces` on those pieces). Every other id emits its own text. Concatenate. Do not run the whole id list through SentencePiece, and do not run an Indic run through the English byte decoder. The ▁ rule stays inside SentencePiece, where `नमस्ते` was learned.

Shared pieces (a comma, a digit) have a Sarvam piece attached, so inside a Hindi sentence they stay inside the SentencePiece run. A raw space used by code does not have a Sarvam piece. It emits a real space. That is how `राम, श्याम` keeps the comma inside Sarvam, and how a Python indent keeps real spaces.

### Build order

Do the steps in this order. Do not start step 6 until Gate 1 has passed.

1. Read the license shipped with `sarvamai/sarvam-1`. If it forbids a derived vocabulary, stop and tell the requester. Do not rewrite pieces to dodge the license.
2. Load the original model. Confirm the vocabulary size is 68,096. Confirm `EncodeAsPieces("नमस्ते")` is `▁नम`, `स्ते`, ignoring `<s>` and `</s>`. If it is not, stop. The model on disk is the authority. Do not “fix” it to match a note.
3. Classify every piece with the keep rules below. Confirm the fingerprint counts. Assign ids. The English tail is reserved and empty.
4. Implement the router and the Indic encode and decode. English spans can return a clear “not trained yet” error. Do not train English to debug the router.
5. Run Gate 1. On a pass, freeze the Indic ids and write their sha256. A sha256 is a fingerprint of the file bytes. After this step those ids do not move.
6. Train English, code, and math into the reserved tail only.
7. Run Gates 2 through 7 in order. A failure retrains English only. It does not edit the frozen Indic ids.
8. Record the freeze file named in “How we know it is done.”

## What we keep from Sarvam, what we delete, and the slot budget

The counts below are the count of `sarvamai/sarvam-1` `tokenizer.json` already written in `tokenizer-plan.md`. They sum to 67,650 named pieces. The file has 68,096 pieces, so 446 pieces are not in that table. Re-count on the loaded file. If a named count disagrees with the table, stop and report both numbers. Do not train on a different file and hope.

The earlier build log dropped `english=14034`. That bucket is wider than the 13,591 Latin-letter pieces in the table. It took the space mark with it, which is why `नमस्ते` fell apart. Do not use that drop list.

### Delete

| Bucket | Pieces | Why |
| --- | ---: | --- |
| Latin-letter pieces (Sarvam English) | 13,591 | Freed for our English, code, and math |
| Gurmukhi (Punjabi) | 4,751 | Language we are not keeping |
| Malayalam | 3,592 | Language we are not keeping |
| Oriya (Odia) | 1,956 | Language we are not keeping |
| `<<reserved_token_*>>` | 4,096 | Empty ids. We do not keep a hole |
| **Named deletes** | **27,986** | |

Also delete Sarvam’s control pieces `<unk>`, `<s>`, `</s>`, and `<pad>` if they sit in the unnamed 446. We add our own 32 markers. Do not keep two copies.

### Keep

| Bucket | Pieces | Why |
| --- | ---: | --- |
| Devanagari (Hindi and Marathi together) | 12,126 | One script, two languages |
| Telugu | 5,916 | |
| Kannada | 5,693 | Not pooled with Telugu |
| Bengali | 5,299 | |
| Gujarati | 5,274 | |
| Tamil | 5,100 | |
| Sarvam byte pieces (`<0xHH>`) | 256 | So a rare character in an Indic span still round-trips |
| **Named keeps** | **39,664** | |

From the 446 unnamed pieces, keep a piece when every character is a digit, a punctuation mark, a symbol, or the space mark ▁, and the piece has no Latin letter and no character in Gurmukhi, Oriya, or Malayalam. Hindi uses those. Drop the rest, and write down each dropped string. Let **U** be how many of the 446 we keep.

A piece with letters from two scripts is dropped, even if one script is Devanagari. A piece with any Gurmukhi, Oriya, or Malayalam character is dropped. A piece with a Latin letter is dropped.

### Our own rows

| Block | Ids | Count |
| --- | --- | --- |
| Special markers | 0–31 | 32 |
| English byte alphabet | next 256 | 256 |
| Kept Sarvam pieces, in ascending original Sarvam id | next | K |
| English, code, and math, in the order learned | through 65,535 | 65,536 − 32 − 256 − K |

**K** is the number of kept Sarvam pieces whose text is not already stored by a special or by an English byte. A comma is the character comma on both sides, so it gets one id, not two. The Sarvam id is stored as a link on that shared id. ▁ is not an English byte. It gets its own id.

Expected arithmetic, before measuring U: named keeps are 39,664, so if none of those strings collide with the English bytes, K = 39,664 + U, and the English tail has 65,536 − 32 − 256 − 39,664 − U = 25,584 − U tokens. U is at most 446, so the tail lands between 25,138 and 25,584 if the fingerprint matches. After the real count, the tail must be between 24,000 and 27,000. Outside that band, the classifier is wrong. Stop. Do not steal Indic pieces to widen English, and do not add empty reserved ids to fill a hole.

Special markers, fixed:

| Id | Piece | Job |
| --- | --- | --- |
| 0 | `<unk>` | Must not appear on real text |
| 1 | `<s>` | Start of sequence, added by the dataloader, not by this encode |
| 2 | `</s>` | End of sequence, same |
| 3 | `<pad>` | Pad |
| 4 | `<eod>` | Document boundary when several documents are packed |
| 5–31 | `<reserved_0005>` … `<reserved_0031>` | Unused room for a later chat template. Not Sarvam’s 4,096 |

### How the English bytes are written in the file

JSON cannot hold every raw byte as itself. Use the standard GPT-2 byte-to-unicode map: bytes from `!` through `~` stay the same character, and the other bytes (including space and newline) are written as a single private character. Decoding an English span converts those characters back to bytes and reads the bytes as UTF-8. UTF-8 is the usual way a file stores Unicode characters as bytes. The round-trip test compares real text, not the private characters in the file.

The map, so nobody invents a second one:

```python
def bytes_to_unicode():
    bs = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return dict(zip(bs, [chr(c) for c in cs]))
```

Compare pieces by the text they mean, not by the private glyph. The English token for comma is the same text as Sarvam’s comma, so it is one id. The English token for a space is not ▁.

## How English, code, and math are trained

Train only after Gate 1 has frozen the Indic ids. The trainer is a new byte-level byte-pair encoder for English spans. Byte-pair encoding starts from the 256 bytes and repeatedly glues the most frequent adjacent pair. This is not the old Indic trainer. Do not import its merge loop. That loop allowed every byte-byte pair.

### Data

Indic text is not in this sample. Of every 52 words, 33 are English, 12 are code, and 7 are math. That is the Latin mix already set in `tokenizer-plan.md` (33 + 12 + 7). A word is split on space, tab, and newline only.

Use text already on disk from these sources, and write down which ones were actually present:

- English: ClimbMix if it is present, otherwise the Nemotron CC HQ crawl named in `tokenizer-plan.md`.
- Code: CodeAlchemy and Nemotron Code, half and half if both exist. If only one exists, it fills the code share.
- Math and LaTeX: Nemotron Math 4+, the math textbooks, Finemath, and SwallowMath, split evenly across the ones that exist. There is no separate LaTeX corpus. The math slice is the LaTeX.

Take 4 GB of text, counted in UTF-8 bytes after NFC. NFC is the Unicode form that writes a character and its mark as one character when the standard has a single combined form. NFC is applied to this training sample only, so one word is not learned twice under two equal spellings. Do not use NFKC. NFKC is a stronger rewrite, and it can delete the invisible joiners. Carve the eval text out first, and do not let those document ids into the 4 GB. Cap a training document at 4,000 characters. Leave eval documents whole.

If a source is missing, write it down and rebalance inside that bucket. Do not fill the hole with Hindi.

### The scissors on an English span

A **pre-tokenizer** cuts a span into chunks before any merge. Merges cannot cross a chunk. The pattern below is tried in order, on the English span only. It is a raw string: the backslashes must reach the regex engine. Use the regex engine inside Hugging Face `tokenizers` (Oniguruma on the 0.23 line), not Python’s `re`. Python’s `re` does not understand `\p{L}`.

```text
(?:\r\n|\n|\r)[ \t]*
|\\[A-Za-z]+
|[0-9]
|[^\r\n\p{L}\p{N}]?[\p{L}\p{M}]+(?:['\x{2019}][\p{L}\p{M}]+)*
|[^\s\p{L}\p{M}\p{N}]+
|[^\S\r\n]+
|[\s\S]
```

What each line keeps:

| Line | What it is | Why |
| --- | --- | --- |
| Newline plus the spaces or tabs after it | One chunk for the indent | Code keeps its shape |
| `\frac` and any `\letters` command | One chunk | So a command can be one token |
| One ASCII digit | `65` is `6` then `5` | Do not spend the tail on every integer |
| A word, with one optional character in front, and an apostrophe inside the word | `don't` is one chunk | A cut into `don` + `'t` cannot be undone later |
| A punctuation run | Symbols, not letters or digits | |
| Spaces that are not a newline | Ordinary spaces | They stay real spaces |
| One leftover character | The safety net | No character is dropped |

Before training, check this scissors on these strings. One mismatch and the pattern is wrong. Do not start the merge loop.

| String | Chunks |
| --- | --- |
| `don't` | one chunk |
| `\frac{1}{2}` | `\frac`, `{`, `1`, `}{`, `2`, `}` |
| `65` | `6`, `5` |
| a newline, four spaces, `return` | one newline-and-indent chunk, then `return` |

`use_regex` on a following byte-level step must be off. If it is on, the library applies a second, older cut and the table above is a lie.

### Seeds that are forced before frequency merges

Seeds occupy slots in the English tail. They are not added on top of 65,536. If the exact text is already in the vocabulary, skip it. A single newline is already one byte. The long indents are not.

Force these, shortest first:

- newline + 1 through 8 spaces
- newline + 1 through 4 tabs
- the two-space, four-space, and eight-space runs
- carriage-return + newline, if it is not already one token

Then force LaTeX commands. A command is a backslash plus letters. Take every command that occurs at least 50 times in the math training text, cap the list at 512, and always include every command that covers the top 90% of command occurrences in the math eval. `stage1-fertility.json` records five commands the old file split: `\partial` (2 tokens), `\circ` (2), `\overrightarrow` (3), `\subseteq` (4), `\setminus` (4). Those five are seeds even if a count comes in under 50. `\frac` is a seed. Match seeds longest-first, so `\textbf` is not eaten by `\text`.

### The merge loop

1. Turn each chunk into bytes. The 256 byte tokens already have ids.
2. Count adjacent pairs inside chunks.
3. Add the seeds first, in the order above, each as a real merge of shorter pieces that already exist.
4. Then, until the English tail is full, merge the pair with the highest count whose new text passes the ban below.
5. Ties break by the smaller left id, then the smaller right id. No randomness. Two runs on the same sample must match.
6. Stop at exactly the tail size. Do not go past id 65,535. Do not leave a hole. If the sample cannot fill the tail, add more English, code, and math text and run this loop again. Do not lower the vocabulary, and do not take an Indic id.

The ban. Reject the merge if any of these are true:

- The new text contains an Indic letter or mark, or a Gurmukhi, Oriya, or Malayalam character.
- The new text contains ▁ (U+2581).
- The new text is already in the vocabulary.
- Either side is a special marker.

Apply the ban while merging, not after. Deleting a finished merge and keeping the later merges is how a vocabulary silently changes meaning.

### What is saved for the English encoder

The inference encoder is this same procedure: route, then on an English span match seeds longest-first, then apply the pre-tokenizer, then apply the saved merges in order. It does not call Sarvam. It does not load the old `tokenizer-slices` trainer.

## The safety gates

Nothing proceeds past a failed gate. A failed gate stops the build. Gates 2 through 7 may retrain the English tail only. They must not change a frozen Indic id. Gate 1 may change the keep set, because the Indic ids are not frozen yet. After a Gate 1 pass, they are frozen.

Words for the fertility gates are split on space, tab, and newline only. Do not lowercase. Do not strip punctuation. Do not NFC the eval text.

### Gate 1. Seven-language sentence match

Load original Sarvam. For each of Hindi, Marathi, Kannada, Telugu, Tamil, Gujarati, and Bengali, encode at least 100 held-out sentences that contain no Latin letters and no protected whitespace. If a language has fewer than 100 such sentences on disk, use all of them, and stop if a language has fewer than 20. Also encode these three words, which `training-fault-analysis.md` already recorded for original Sarvam:

| Word | Original Sarvam pieces |
| --- | --- |
| `नमस्ते` | `▁नम`, `स्ते` |
| `हिन्दी` | `▁ह`, `िन्`, `दी` |
| `ಕನ್ನಡ` | `▁ಕ`, `ನ್ನ`, `ಡ` |

Our piece strings, in order, must equal original Sarvam’s piece strings, in order. Ignore a leading `<s>` and a trailing `</s>` on Sarvam’s side. One mismatch fails the gate. `नमस्ते` as `न` + `म` + `स्` + `ते` is a failure. Do not patch that word by hand.

Before the 100 sentences, check that original Sarvam itself round-trips each sentence: decode(encode(sentence)) equals the sentence. If the original model does not, stop and report the sentence. Do not build a second Indic encoder to hide that.

On a pass, write the Indic id list and its sha256. That list is now frozen.

### Gate 2. Code indentation and LaTeX shape

Encode these strings with the full router. Each indent must be exactly one token. The token’s text must be real spaces or a real tab plus a newline. It must not contain ▁.

| String | Requirement |
| --- | --- |
| newline | one token |
| newline + two spaces | one token |
| newline + four spaces | one token |
| newline + one tab | one token |
| newline + four spaces + `return` | the indent is one token, then the word |

Also: every LaTeX command that covers the top 90% of command occurrences in the math eval is exactly one token. The five commands stage 1 split must be one token each.

A failure here means the seeds or the scissors are wrong. Fix those and retrain English. Indic ids stay.

### Gate 3. English fertility

On one English file, measure original Sarvam-1 and measure ours. Ours must be fewer tokens per word. Do the same on one code file and one math file. Ours must be lower on each.

Published anchors, not our scores, and not interchangeable:

- About 1.43 Sarvam-1 English tokens per word on FLORES is the published figure named for this project. It was not recomputed here.
- `tokenizer-plan.md` quotes a different FLORES table where Sarvam-1 English is 1.50 and Llama 3 is 1.24. Different file. Do not mix it with 1.43.
- Our old stage-1 file scored 1.514 English tokens per word on our holdout (`stage1-fertility.json`: 245,253 tokens, 161,941 words). That holdout is not FLORES. The code row there is 3.138 and the math row is 2.019. Those are the old trainer, not this one.

Beat original Sarvam on the same file. Do not require beating Llama 3. Llama 3’s table is much larger than the English tail we have. If this gate fails, add English, code, or math text and retrain the tail. Do not take Indic slots.

### Gate 4. Akshara check

An illegal new cut fails the gate. A cut original Sarvam itself makes does not.

On the Gate 1 sentences, every token must pass all three:

1. An English token contains no Indic letter or mark.
2. A Sarvam token is one of the pieces original Sarvam emitted on that same sentence.
3. No token is a broken UTF-8 sequence. The split of `े` into `e0 a5` and `87` fails here.

Write down how many frozen pieces start with a dependent vowel mark. Do not fail the gate on that count. `हिन्दी` is the known case: original Sarvam’s second piece is `िन्`, which starts with the vowel sign `ि`. Priority 1 says we keep that piece. “Fixing” it would change the sentence and fail Gate 1. The old scorer that flags every such piece is retired. It rejected Sarvam’s own strings (`training-fault-analysis.md`).

### Gate 5. Round trip

decode(encode(text)) equals text, with no Unicode normalization before the compare. Required on every Gate 1 sentence, every code eval file, every math eval file, and these fixtures:

| Fixture | What it locks |
| --- | --- |
| `नमस्ते` | Indic word, pieces `▁नम` + `स्ते`, text comes back |
| `राम, श्याम` | comma stays inside the Sarvam run, space survives |
| `main जा रहा hoon` | Hinglish. The space between the Hindi words stays inside Sarvam. The spaces next to the English words are real spaces. |
| `helloनमस्ते` | glued Latin and Hindi, no extra space invented |
| `नमस्ते123` | digits glued to Hindi, whole span through Sarvam |
| `123नमस्ते` | digits glued in front, same |
| `वर्ष 2024 में` | no Latin letters, so the whole line goes to Sarvam |
| newline + four spaces + `return` | indent round-trips as real spaces |
| `\frac{1}{2}` | command is one token, digits are single digits, text comes back |
| a line of Python with a four-space indent | the indent is one token and the line matches |

One mismatch fails. If a shared digit or comma is the cause, fix the decode grouping. Do not drop the Indic pieces.

### Gate 6. Exact vocabulary size

The file has exactly 65,536 pieces. Ids are 0 through 65,535 with no gaps and no duplicates. Two pieces must not share the same text. `<unk>` appears zero times on the eval files.

### Gate 7. No cross-script pieces

Scan every piece except the 32 specials and the 256 raw bytes. Letters in a piece come from at most one script family. The families are Latin, Devanagari, Bengali, Gujarati, Tamil, Telugu, Kannada, Gurmukhi, Oriya, and Malayalam. Digits, punctuation, ▁, and ordinary whitespace do not count as a family. ▁ plus Devanagari is legal (that is a Sarvam word). A Latin letter plus a Devanagari letter is not. A Gurmukhi, Oriya, or Malayalam letter is not, in any piece.

Also confirm the fingerprint: Devanagari 12,126, Telugu 5,916, Kannada 5,693, Bengali 5,299, Gujarati 5,274, Tamil 5,100, unless Gate 1’s re-count on the official file recorded a different fingerprint and the build stopped for a human to look. A quiet shortfall is a failure.

## What we will not do

- We will not rebuild Indic merges from token strings. `नमस्ते` stays `▁नम` + `स्ते` because the original model says so.
- We will not run the old byte-level trainer on Indic text. Its `allow` check returned true for every pair of raw bytes, and export then wrote those byte pairs under the merges.
- We will not send code, newlines, tabs, or runs of two or more spaces through Sarvam.
- We will not send an Indic letter through the English encoder.
- We will not add a token that joins two scripts.
- We will not keep Malayalam, Odia, Punjabi, Sarvam’s English words, or the 4,096 reserved ids.
- We will not drop digits, punctuation, or ▁ just because they are not Devanagari letters.
- We will not use a vocabulary of 68,096, 81,920, 96,000, or 131,072. There is no backup size in this plan.
- We will not freeze o200k, Llama, Qwen, or TinyLlama merges. The English tail is trained by us, into the counted slots.
- We will not copy BrahmicTokenizer’s 2,372-slot Indic graft or their 131,072 vocabulary.
- We will not continue the old stage-1 / stage-2 plan, and we will not turn on Picky.
- We will not NFKC, and we will not run a morphological splitter.
- We will not pre-cut words into aksharas. Sarvam already decided the Indic cuts.
- We will not start the 1.2B training run.
- We will not start or touch the two stopped tokenizer EC2 instances. They stay stopped. We will not change AWS, S3, or training code as part of this plan.

## How we know it is done

All seven gates have passed, in order, on the same frozen Indic ids.

The shipped artifact is one file, `tokenizer-65k.json`, plus a one-page freeze note beside it. The json holds the 65,536 pieces, the English merge list, the English scissors pattern, the byte-to-unicode map, and the link from each shared or Sarvam id back to the original Sarvam piece id. The freeze note holds:

- sha256 of the original Sarvam `tokenizer.model`
- sha256 of `tokenizer-65k.json`
- the value of K and of U, and the English tail size, which must equal 65,536 − 32 − 256 − K
- Gate 1: seven languages, sentence count per language, and the three fixture words with their piece strings
- Gate 2: the indent tokens and the LaTeX commands that failed in `stage1-fertility.json`, each shown as one token
- Gate 3: tokens per word for original Sarvam and for this file, on the same English file, the same code file, and the same math file
- Gate 4: broken-UTF-8 count is 0, and the written-down count of Sarvam pieces that start with a vowel mark
- Gate 5: round-trip mismatches are 0
- Gate 7: cross-script piece count is 0

A pass on fertility without a pass on Gate 1 is not done. The machines named above are still stopped. No model training has been started.
