# What the tokenizer is, in plain words

This is the explanation. The exact rules, the regex, and the pass numbers live in the [tokenizer plan](tokenizer-plan.md). If the two ever disagree, the plan is the one to follow.

## The decision

Train stage 1 first, on one mixed 15 GB sample. It is one akshara-constrained byte-pair encoding, not one train per script.

1. Build a tokenizer with **65,536** entries, including 32 special markers and 256 bytes. Spaces stay. A space is the first character of the next chunk (`the` + ` ram`). A stage-1 token does not cross a space. Save this file as `tokenizer-stage1.json`. Never overwrite it. It is the fallback. Write `stage1-language-counts.json` beside it.
2. Copy that file to `tokenizer-stage2.json`. The vocabulary stays **65,536**. No id above 65,535. A new piece joins exactly two stage-1 chunks, and only when the second starts with a space or a tab. It replaces a rare learned piece of the same script only when it is more frequent than that piece. Ceilings, not quotas: Latin 2,000, including code and math; Bengali, Gujarati, Tamil, Telugu, and Kannada up to 500 each; Hindi and Marathi up to 500 each, freeing the rarest Devanagari pieces (1,000 if both earn them), identical strings stored once. Do not pad. Mixed-script pairs get no bucket. Do not overwrite `tokenizer-stage1.json`. Picky stays off. Write `stage2-language-counts.json` beside the finished stage-2 file.
3. Score both files. Ship stage 2 only if every language’s tokens per word is less than or equal to stage 1. Otherwise ship stage 1.
4. If stage 1 misses the engineering bar, build a tokenizer with **81,920** entries and measure that one. That backup is not a stand-in for stage 2, and stage 2 is not a stand-in for a failed stage 1.

81,920 is the number behind “81.9k”. It is 80 × 1,024. The extra 16,384 entries, if we ever need them, go to English, code, math, and LaTeX. The Indic budgets stay the same. We do not train the bigger one “just in case” before stage 1 has a score.

## What we are trying to do

The model cannot read letters. It only reads whole numbers. The tokenizer is the program that turns text into those numbers, and turns the numbers back into the same text.

A **word** should become one number, or a few numbers. Not one number per letter.

**Fertility** is how many numbers we spend per word. Lower is better. If Hindi costs 6 numbers per word, a fixed training budget contains fewer Hindi words, and each sentence fills more of the context window with scraps.

We need one tokenizer that does all of this at once:

- English, code, math, and LaTeX stay compact.
- Hindi, Marathi, Kannada, Telugu, Tamil, Gujarati, and Bengali stay compact too.
- The list of numbers is small enough for a 1.2 billion parameter model. 65,536 is that size. 81,920 is the backup if 65,536 cannot hit the fertility bar.

Hindi and Marathi use the same script, Devanagari. They still get two fertility scores. A good Hindi number does not excuse a bad Marathi number.

## Why this is hard

Most English tokenizers cut a word at every character that is not a “letter.” In these Indic scripts the vowels are not letters. They are marks attached to letters.

`हिन्दी` looks like one word. To a letters-only cutter it is six pieces: the letters, then the vowel signs and the virama that glues a conjunct. The same thing happens to `स्कूल`, `தமிழ்`, and `ಕನ್ನಡ`.

Once the cutter has split the word, no amount of training data and no bigger vocabulary can glue it back. Merges are only allowed inside one piece. That first cut is the whole game. People call it the **pre-tokenizer**, or the preprocessing step. It is not a spell-checker and it is not a translation. It is a pair of scissors.

## What we are copying, and what we are not

Nobody has shipped this exact tokenizer. Several groups already measured the pieces. We copy the pieces that worked on their files. We do not copy their files, their scores, or their vocabularies.

| Who | What they showed | What we take | What we leave |
| --- | --- | --- | --- |
| Regmi, Pudasaini, and Pun, “Vowel Signs Are Not Letters” | At 65,536 tokens, fixing the scissors dropped Hindi from 3.36 numbers per word to 1.32 on their FLORES file. Bengali 4.73 to 1.50. Tamil 6.85 to 1.77. English barely moved. | The scissors must keep vowel marks inside the word. | Their setup was bilingual. They say that is optimistic for a real mix of many languages. We do not treat their scores as ours. |
| MUTANT, also called IndicSuperTokenizer | The same training, two scissors. The letters-only scissors shattered Indic. The mark-aware scissors did not. English and code barely changed. Their second stage glues neighboring words after the word-level tokenizer. On their file that shortened English from about 1.33 to 1.12 tokens per word, and made Tamil worse, from about 2.07 to 2.12. Kannada and Telugu moved with Tamil. A careless stack of per-script lists also made Hindi worse (1.21 alone, 1.55 after the stack). | The scissors. One mixed train, not a stack of per-script lists. A light copy of their cross-word stage: start from the saved word-level tokenizer and append merges of two neighboring chunks. | Their vocabulary is about 200,000. We do not copy the part of stage 2 that fills the last 10% of a fixed list with English phrases. That spend is why Tamil got worse. We do not build three-word chains. |
| Sarvam-1 | A real Indic tokenizer. In their published vocab file, one script occupies about 5,100 to 5,916 entries. Hindi and Marathi together occupy 12,126, because they share Devanagari. Their English and code are weaker than a big English tokenizer. | Those counts are our Indic budgets. They are a shelf size, not a score we are trying to tie. | We do not load their tokenizer. We do not keep Malayalam, Odia, or Punjabi. We do not keep their 4,096 empty reserved numbers. We do not keep their space-marker encoder. |
| Qwen3.5’s published word pattern | A word can be marks as well as letters, with one optional character in front. | That shape, plus two invisible joiners (ZWJ and ZWNJ), plus a rule that a danda cannot stick to the next word. | We do not load Qwen’s vocabulary. |
| akshara-tokenizer v1.2 | Cutting every word into syllables, and spending almost the whole 64k list on those syllables, gets a decent Indic number and a bad English number (about 2.15 on their report, against Qwen around 1.26). | The warning. | We do not pre-cut words into syllables. |
| Llama 3, Llama 4, TinyLlama, Qwen2.5 | Strong English lists. Several of them still use the letters-only scissors, or never spent entries on these scripts. Llama 4’s scissors are in the right family, and the shipped Llama 4 list still scored Tamil at 5.87 on MUTANT’s file. | They are baselines we measure against. | We do not start from their merge lists. A good pair of scissors is not a good Tamil vocabulary. |
| BrahmicTokenizer | A script with zero entries is not “a bit worse.” It cannot spell the language. They also found Sarvam’s English, code, and math behind a tokenizer that kept a large English list. | After training, every script must contain real learned words, not only the alphabet. | We do not retrofit someone else’s English tokenizer. |
| Picky BPE (Chizhov and co., 2024) | During training, throw away pieces that stopped being useful, and keep the slots for real words. | Nothing. Picky stays off. | We do not delete pieces by hand from a finished list and hope the merges still mean the same thing. Stage 2 may replace a rare learned piece in `tokenizer-stage2.json` only. It does not edit `tokenizer-stage1.json`. |

## Preprocessing, from a raw file to a number

Five steps. Steps 1 and 2 are the scissors. Step 3 is the only place the computer “learns” pieces. Steps 4 and 5 just assemble the list.

### 1. Do not rewrite the text on the way in

When the model later reads a prompt, the text is not lowercased, not stripped of accents, and not converted to a compatibility form. `Return` and `return` stay different, because code cares. `ड` and `ड़` stay different, because the dot changes the letter. Invisible joiners stay, because deleting them changes the word.

The one rewrite is on the **training sample only**: NFC. That makes two Unicode spellings of the same word look like one word, so we do not learn it twice. NFC does not delete vowel marks or joiners. We never use NFKC. NFKC is the rewrite that can delete those joiners and then pretend the text got shorter.

### 2. Cut the text into chunks

This is the preprocessing people cannot see. A pattern tries these rules in order. The first one that matches takes the next chunk. Then it repeats.

| What the scissors keep together | Example | Why |
| --- | --- | --- |
| A word with an apostrophe in the middle | `don't`, `it's`, and `I’m` are each one chunk | GPT-4o keeps the contraction on the word. GPT-4, Llama 3, and Qwen2 still cut `don't` into `don` and `'t`, and that cut cannot be undone. A quote around a word does not join: `'string'` is `'`, `string`, `'`. |
| A newline and the spaces or tabs after it | a new line, then four spaces, then `return` | Code indentation stays one chunk, so it can become one number. |
| A LaTeX command | `\frac` | The command can become one number. This rule has to run before punctuation, or the backslash is just a symbol. |
| A single digit | `65` becomes `6` and `5`. `६५` becomes `६` and `५` | A small model learns place value from single digits. We do not spend an entry on the number 2024. |
| A word, including its vowel marks, and one leading space or tab | `हिन्दी` is one chunk. ` गया` is one chunk, space included | This is the Indic fix. The space stays with the word so we do not pay an extra number for every space. |
| Punctuation | `गया।वह` becomes `गया`, `।`, `वह` | The danda (`।`) must not glue onto the next word. If it does, the vocabulary fills up with words that all start with a full stop. |
| Anything left over | one character | So no character is dropped. |

Things that look like cleanup and are not:

- We do not lowercase.
- We do not delete spaces. Deleting spaces looks efficient and destroys code.
- We do not split a word into syllables first. A four-syllable word could then never be one number.
- We do not split a word into roots and endings. That raises fertility. We want it lower.
- Stage 1 does not glue “of the” into one number. Stage 2 may replace a rare piece with exactly two chunks, under the ceilings above. On MUTANT’s file, spending a shared list on English phrases hurt the Dravidian languages. We do not let a Latin phrase replace another script’s piece.

A check before any training: `नमस्ते`, `स्कूल`, `संस्कृति`, `தமிழ்`, `ಕನ್ನಡ`, and `हिन्दी` must each be **one** chunk. `राम गया।वह आया` must be `राम`, ` गया`, `।`, `वह`, ` आया`. If a test splits these, stop. More data will not fix it.

The word stays one chunk, so a frequent word can still be one number. Inside that chunk, a learned piece may end only on a syllable boundary. For `हिन्दी` the only legal split is `हि` and `न्दी`. A piece must not start with a vowel mark, and must not stop on a halant that is still waiting for the next consonant. `स्कूल` may split only as `स्कू` and `ल`. The invisible joiners stay inside the syllable they belong to. English, code, math, and LaTeX are not cut this way. We do not cut the word into syllables before learning. Tamil’s pulli ends a syllable and does not glue the next consonant.

If a whole syllable is not in the list, spell its characters in order. If a character is not in the list, spell that character’s bytes in order. Those byte numbers are the 256 raw bytes, never the unknown-token id. Decoding the numbers puts the original text back. A vowel mark, a halant, or a joiner that shows up alone, or a conjunct cut off before its next consonant, does not crash the parser. The lone mark is spelled as its character, or as its bytes if that character is missing, and the parser returns a list of numbers.

### 3. Learn the frequent pieces on one mixed sample

Byte-pair encoding starts from single bytes and repeatedly glues the pair that shows up most. In stage 1 it can only glue inside a chunk from step 2. A token does not cross a space.

This is **one** mixed train on the 15 GB sample, not one train per script. Do not keep a separate pair table per language during BPE. Hindi and Marathi still get two fertility scores. Kannada and Telugu stay separate scores.

Both finished files get a language count. `stage1-language-counts.json` sits beside `tokenizer-stage1.json`. `stage2-language-counts.json` sits beside `tokenizer-stage2.json`. Each file has exact piece counts for Tamil, Telugu, Kannada, Bengali, Gujarati, Devanagari, and Latin, read from the characters of each piece. Each file also has the usage splits: Hindi-only, Marathi-only, and shared, and English-only, code-only, math-only, and shared. Specials, bytes, and punctuation, digits, and spaces stay unassigned.

For stage 1, the script counts are tallied as each merge is accepted. The Hindi/Marathi split and the English/code/math split are one read of the labeled slices after that file exists. For stage 2, both the script counts and those splits are taken from the finished file, after the slot replacements. The count files do not change the 65,536 list or the ceilings.

### 4. What is inside the 65,536

The train is one list, not a stack of per-script lists. The shelves below are what we count after that run. They are not separate trains.

| What | How many | Why this many |
| --- | ---: | --- |
| Special markers (unknown, start, end, padding, a few spares) | 32 | Sarvam kept 4,096 empty spares. We do not. |
| Raw bytes | 256 | Any text can be spelled, even a character we never trained on. |
| English, code, math, LaTeX | 25,840 | The leftover. This is the side a 5–6k-per-script tokenizer usually starves. |
| Devanagari, Hindi and Marathi | 12,126 | Sarvam’s count for that shared script. About 6,000 per language, not 6,000 for both. |
| Telugu | 5,916 | Sarvam’s count. |
| Kannada | 5,693 | Sarvam’s count. |
| Bengali | 5,299 | Sarvam’s count. |
| Gujarati | 5,274 | Sarvam’s count. |
| Tamil | 5,100 | Sarvam’s count. |
| **Total** | **65,536** | |

Those Indic counts are copied from a count of Sarvam’s vocabulary file. They are not copied from Sarvam’s merges. We train our own pieces, with our scissors, on our sample.

### 5. Only if 65,536 is not good enough

Same scissors. Same text. Same Indic shelves. Latin grows from 25,840 to 42,224. The total is 81,920.

That backup costs about 34 million extra parameters in the embedding, at the assumed hidden size of 2048. Those parameters come out of the rest of a 1.2B model. This is why the backup waits for a failed score instead of being the default.

## What “good enough” means

This is the engineering acceptance bar. Passing it means the 1.2B run may start. It does not mean the tokenizer is state of the art.

On text we held out before training:

- Each Indic language uses no more numbers per word than the best tokenizer we can actually load, Sarvam included.
- English is within 8% of the best tokenizer that does not glue two words across a space. A token for “of the” does not count as the bar. An apostrophe inside `don't` is not that glue. A 3% bar asks a 65k list to match Llama 3’s 128k English list. The vowel-sign paper’s own 65k English score was about 5% behind Llama 3, and they called that setup optimistic.
- Code is within 5% of the best. Math is judged after digits are blanked out, so a tokenizer that glues `2024` into one piece cannot win on a technicality. LaTeX commands are checked on that same math text: the commands that cover 90% of command occurrences are each one number.
- Encoding and decoding returns the original text, including code and Indic. No unknown token. No learned piece ends in the middle of a syllable.

If 65,536 misses, the first repair moves a couple of thousand entries between shelves and retrains those shelves. The 81,920 tokenizer is the step after that repair still misses the engineering bar.

## The second look

Run this only after the engineering bar has passed. Do not call the tokenizer state of the art until it has been measured. Nothing here has a score yet.

We do not pre-cut words into syllables before learning, and learned pieces may end only on a legal syllable boundary. That is the design.

- **Compression.** Numbers per word, per character, and per byte, for every language and for code and math. LaTeX is the math row.
- **Structure.** Illegal syllable cuts at 0%. That is the target, not a margin we are allowed to miss.
- **Rough text.** A separate pile from the fertility test: words the trainer never saw, names, science terms, code, LaTeX, numbers, URLs, mixed-script lines, and Hinglish. Score compression and the syllable rule on each. Hinglish stays Latin letters. It is not a new training language.
- **Same-size comparison.** The fair compression comparison is against strong tokenizers trained or cut down to 65,536 entries. Llama 3’s 128k list and Qwen’s roughly 152k list are written down next to that and are not the fair number. The 8% English rule above is a distance from those bigger lists. It is not a win at the same size.
- **Does the model learn better.** Train the same small stand-in model, on the same tokens, the same data, and the same compute, once per tokenizer that passed the engineering bar. Compare validation loss and perplexity. This is not the 1.2B run, and no perplexity number exists yet. The stand-in is an assumption: 150 million parameters and 20 billion tokens. The 1.2B train still waits only on the engineering bar.

## What the training text is

A small sample, not the trillion-token run. About 20 MB to prove the scissors and the round-trip. About 200 MB to see a real fertility table. The tokenizer itself is trained on one mixed **15 GB** sample. Both stages use that sample. Fertility on 20 MB is noise.

The mix of that sample is **not** the model’s mix. The model sees mostly English. The tokenizer sample is about half Latin and half Indic, so a rare script still gets repeated words. Latin words are English 33%, code 12%, and math 7%. There is no separate LaTeX pile: Nemotron Math 4+ and MIND already contain LaTeX commands in about 84% of sampled rows, and that 5% went to English. Inside each Indic language: half verified native text, a quarter IndicCorpV2, a quarter translated textbook-style text. No romanized Indic in the training sample. Romanized Hindi and Hinglish are a test, scored with the English number, not a separate bar.

The published papers already showed that making this sample 50 GB instead of a few GB does not keep improving fertility. A language that misses gets more of **its own** words, not a bigger pile of English.
