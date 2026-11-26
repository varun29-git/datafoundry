# Would a stage-two pass help the 65,536 tokenizer?

This is a plan for one feasibility test. It does not change the tokenizer. It does not train a model. It does not start a machine. Run the checklist later, not now.

The shipped file is `docs/tokenizer-65k.json`. `docs/tokenizer-65k-freeze.md` records what that file is. It has exactly 65,536 pieces. K = 40059 Indic and shared pieces. The English tail is 25189 pieces. That is 65,536 − 32 − 256 − 40059. Indic spans call the original `sarvamai/sarvam-1` model. English spans use our byte-level merges. `नमस्ते` is `▁नम` + `स्ते`. All seven gates passed.

## What stage two is

The finished tokenizer already has short pieces. Stage two learns a limited number of longer pieces after that.

A longer piece is a frequent two-word phrase. The two words already exist as pieces. One ordinary space sits between them. The phrase becomes one token.

The vocabulary stays 65,536. The new phrase takes a slot from the English tail. Indic ids stay where they are.

This is the second stage of SuperBPE (Liu et al., 2025). SuperBPE learns those longer pieces after ordinary subword pieces exist, and it lets a piece cross a space. MUTANT-Indic, from Krutrim, is the Indic use of that idea. This test copies that idea inside our existing file. It does not copy a 131,072-piece tokenizer. It does not train a tokenizer from scratch. It does not rebuild Indic merges.

## Indic phrases, the same idea

Yes. The same second stage can run on the Indian languages. It joins two whole words. It does not recut a word.

Sarvam already decides the pieces inside a word. `नमस्ते` stays `▁नम` + `स्ते`. Stage two runs after that. If two neighboring words are a saved pair, those two pieces become one token. `अमेरिकी राष्ट्रपति` can become one token. The letters that come back must still be `अमेरिकी राष्ट्रपति`.

The second Sarvam piece starts with ▁. That mark is how Sarvam writes the space. An Indic phrase is allowed to be those two pieces. An English phrase is not allowed to contain ▁. The two bans are different.

A phrase stays inside one script. Hindi and Marathi share Devanagari, so a Devanagari pair can fire in either language. A Hindi pair cannot fire inside Kannada. A pair cannot join a Hindi word to an English word.

The slots still come from the end of the English tail. The 40,059 Indic ids do not move. The vocabulary stays 65,536.

This is a second candidate, not a replacement for the English one.

- Candidate A: up to 1,000 English phrases. No Indic letters.
- Candidate B: up to 1,000 Indic phrases. No Latin letters. At most 170 pairs per script, so Devanagari cannot take the whole budget. The scripts are Devanagari, Bengali, Gujarati, Tamil, Telugu, and Kannada.
- Candidate C is built only if A and B each pass on their own. It keeps the winning phrases from both, still inside 1,000 slots, and drops that many English-tail pieces once.

Count Indic pairs on Indic training text only, after Sarvam has encoded it. Leave the held-out sentences out of the count. Skip a pair that is not two word pieces. Skip a pair that contains a newline, a tab, two spaces, or a second script.

On a pure Indic sentence, the pieces before any join must still match original Sarvam, in order. After the join, the token list may be shorter. That shorter list is the gain. A join that is not in the saved list is a fail. `नमस्ते`, `हिन्दी`, and `ಕನ್ನಡ` stay the original pieces, because each is one word.

The pass bar for candidate B, on the same 40 documents per language already used for the router check:

| Language | Must be under |
| --- | ---: |
| Hindi | 1.486 |
| Marathi | 1.957 |
| Kannada | 2.509 |
| Telugu | 2.367 |
| Tamil | 2.472 |
| Gujarati | 2.014 |
| Bengali | 2.093 |

Those are the rates after the router cut. An equal or higher rate on any language fails. English, code, and math must not get worse than 1.4254, 2.0299, and 1.8574, because B deleted English-tail pieces to make room. Round-trip mismatches must be zero.

## A gap this test leaves alone

If a paragraph contains a Latin letter, an ordinary space before an Indic word can become an extra token. The agreed repair is a router cut. Indic words separated by one ordinary space stay one Sarvam span.

`docs/tokenizer-65k-freeze.md` says the vocabulary file did not change for that rule. The cut is not a new piece inside `docs/tokenizer-65k.json`. Stage two is a different change. This test leaves the router as it is. It does not rewrite training files so the gap disappears.

## Why it might help

An English piece stops at a space today. A common pair still costs two tokens. One piece for that pair makes English text shorter. Code and math repeat pairs too. The slots come from the 25,189-piece English tail in the freeze note, so the vocabulary stays 65,536.

## Why it can hurt this tokenizer

Every new phrase deletes an English piece. The deleted piece may be a rare word, a bit of code, or a math command that the held-out files still use. English can get shorter while code or math gets longer. Those three files share one tail.

`docs/tokenizer-plan.md` records what happened on MUTANT’s own file when English phrases took slots from a shared list. English went from about 1.33 to about 1.12 tokens per word. Tamil went from about 2.07 to about 2.12. Kannada and Telugu moved with Tamil. Those numbers are from their file, as cited in `docs/tokenizer-plan.md`. They are not measurements of `docs/tokenizer-65k.json`. This test keeps every Indic id, so that shared-list loss is refused. The loss still to measure is on our English, code, and math files.

A phrase that contains a newline, a tab, or an indent would break code. A phrase that contains ▁ would put Sarvam’s space mark into an English piece. A phrase that joins two scripts would break the rule that an Indic sentence stays on Sarvam’s pieces.

## The one test

One candidate file. One budget. The budget is 1,000 phrases.

1,000 is the size of this test. It is a cap we chose so the tail is sampled, not rebuilt. No file records a measured best size. 1,000 slots are 1,000 of the 25189 English-tail pieces in `docs/tokenizer-65k-freeze.md`. The test tries this one size.

The candidate is a new file. `docs/tokenizer-65k.json` stays as it is.

### What we would add

Up to 1,000 new pieces. Each piece is two pieces that already exist, with exactly one ordinary space between them.

Count those pairs on the English, code, and math training text named in `docs/tokenizer-65k-freeze.md`. Keep the most frequent pairs. Skip a pair that is already in the vocabulary. Skip a pair that contains ▁, a newline, a tab, or two spaces in a row. Skip a pair that contains an Indic letter, or letters from two scripts. Count pairs on the training text only. Leave the held-out files out of the count.

A new piece contains one ordinary space. This test does not chain three words into one piece.

If fewer than 1,000 pairs are legal, add only the legal ones. Do not invent pieces to fill the cap.

On the candidate only, an English span may join two neighboring pieces when the join is one of these saved phrases and the boundary is one ordinary space. A Sarvam span stays a Sarvam span. A newline, a tab, or two spaces in a row stay unjoined.

### What we would remove

Remove the same number of pieces that we add. Take them from the end of the English tail. Those are the pieces learned last.

Skip any piece that Gate 2 in `docs/tokenizer-65k-freeze.md` needs. That is the newline and indent pieces, and every LaTeX command that note lists as one token. If a skipped piece sits in the removal range, take the next earlier English-tail piece instead.

The 32 special markers stay. The 256 English bytes stay. The 40059 Indic and shared pieces stay.

The new phrase reuses the id of the piece it replaces. Every other id stays put. The file still has ids 0 through 65,535, with no hole.

### What we would not touch

- `docs/tokenizer-65k.json`
- The K = 40059 Indic and shared ids
- The original Sarvam merges, and the call that encodes an Indic span
- The router, including the separate cut for Indic words with one ordinary space between them
- The English scissors on the shipped file
- The training files
- The seven gates already recorded for the shipped file
- The machines, and the 1.2B training run

### What we would measure

Measure the same held-out files that `docs/tokenizer-65k-freeze.md` already scores, labeled there as en, code, and math. `internal/build-65k.py` writes them as `data/eval-en.jsonl`, `data/eval-code.jsonl`, and `data/eval-math.jsonl`.

The freeze note’s counts, which are the baseline:

- English: 1.4254 tokens per word (117091 tokens / 82147 words)
- Code: 2.0299 tokens per word (136908 tokens / 67446 words)
- Math: 1.8574 tokens per word (157362 tokens / 84722 words)

A word is a stretch split only on a space, a tab, or a newline. That is the freeze note’s rule. If a file’s word count is not 82147, 67446, or 84722, it is the wrong file. Stop.

Also run the seven-language check in that freeze note. That is 100 sentences each for Hindi, Marathi, Kannada, Telugu, Tamil, Gujarati, and Bengali, with no Latin letters. Also check `नमस्ते`, `हिन्दी`, and `ಕನ್ನಡ`.

## Pass and fail

A pass needs every rule below. The baseline is our file, from `docs/tokenizer-65k-freeze.md`. Lower is better.

The word counts stay fixed, so the token count decides it.

- English: fewer than 117091 tokens on 82147 words. The printed rate must be under 1.4254.
- Code: fewer than 136908 tokens on 67446 words. The printed rate must be under 2.0299.
- Math: fewer than 157362 tokens on 84722 words. The printed rate must be under 1.8574.

Print four decimal places, the same way the freeze note does. A higher token count on any file is a fail. An equal token count on any file is a fail. Pieces were deleted, and that file did not get shorter.

Original Sarvam on those same files is 1.5328, 2.3825, and 1.9336 in the freeze note. Those numbers are the old comparison. The bar for this test is our own token counts above.

Indic, on the pure sentences: piece strings stay identical to original Sarvam, in order. That is Gate 1 in the freeze note. Identical strings mean those sentences stay as good as original Sarvam. A different cut is a fail. `नमस्ते` stays `▁नम` + `स्ते`.

Also fail when any of these is true:

- The candidate does not have exactly 65,536 pieces.
- An Indic id moved or its text changed.
- A new piece contains ▁, a newline, a tab, two spaces, or two scripts.
- An indent in the freeze note’s Gate 2 list is no longer one token of real spaces or a real tab.
- A LaTeX command in that same list is no longer one token.
- Round-trip mismatches are not zero.
- A cross-script piece appears.

The Indic rule is the exact piece match from Gate 1. The freeze note gives no separate Indic tokens-per-word score for these sentences, so the test uses that match.

## What “feasible” means

Feasible means this one candidate passes every rule above. English, code, and math are shorter than `docs/tokenizer-65k.json` on the freeze-note files. The pure Indic sentences still match original Sarvam. Code indents and the listed LaTeX commands still pass.

A person may then decide whether to keep the candidate. This plan does not make that decision. It does not replace the shipped file.

Anything short of a full pass is not feasible. Keep the shipped file. Do not raise the 1,000 cap and try again inside this test. Do not take an Indic id and try again.

## What we will refuse, even if fertility drops

Fertility here means tokens per word. A lower number is the gain this test is looking for. We still refuse every item below when that number goes down.

- A vocabulary larger than 65,536. That includes 68,096, 81,920, 96,000, and 131,072.
- A new tokenizer trained from scratch.
- Rebuilt Indic merges, or any edit to the 40059 Indic and shared ids.
- A piece that joins two scripts.
- An English phrase that contains ▁. An Indic phrase is two Sarvam pieces, and the second of those already starts with ▁. That is the only ▁ a new piece may involve.
- A piece that contains a newline, a tab, or an indent.
- A phrase token used as the repair for spaces before Indic words in a paragraph that also has a Latin letter.
- Rewritten training files.
- A router change inside this test.
- Dropping the code check or the LaTeX check because English got shorter.
- Starting the two stopped tokenizer instances named in `docs/sarvam-safe-tokenizer-plan.md`.
- Starting the 1.2B training run.
- Overwriting `docs/tokenizer-65k.json` from this test.

## Checklist, for later

Do not run these steps now.

1. Copy `docs/tokenizer-65k.json` to a new candidate file. Leave the shipped file unchanged.
2. Check the copy. It has 65,536 pieces, K = 40059, English tail = 25,189, and `नमस्ते` = `▁नम` + `स्ते`.
3. Read the English, code, and math training text named in `docs/tokenizer-65k-freeze.md`. Leave those files as they are. If they are not reachable without starting a machine, wait. Do not rent a new machine, and do not rebuild the text.
4. Count pairs of English pieces separated by exactly one ordinary space. Drop pairs that break the bans above.
5. Keep the most frequent legal pairs, up to 1,000. Add only that many new pieces.
6. Remove that same count from the end of the English tail. Skip the Gate 2 seeds. Put each new phrase in a freed id.
7. Encode the three held-out files and the seven-language check. Confirm the word counts 82147, 67446, and 84722 before trusting a rate.
8. Apply the pass and fail rules. Write the three token counts, the Indic piece match, and the Gate 2 checks beside the freeze-note baselines.
9. Repeat steps 4 through 8 for candidate B, the Indic phrases. Count pairs per script after Sarvam encodes the Indic training text. Cap each script at 170. The pass bar is the seven language rates in the Indic section, and English, code, and math must not get longer.
10. Build candidate C only if A and B each pass. Keep at most 1,000 phrases in total. Run the same checks again.
11. Leave `docs/tokenizer-65k.json` in place either way. Leave the machines stopped.
