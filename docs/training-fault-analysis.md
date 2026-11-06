# Why the BPE scores badly

The fertility number and the token-per-word number are two different failures.

`tokenizer-full.json` is almost the same model as stage 1, so it gets almost the same score. The merge loop does update pair counts, and the regex does not split matras. The akshara rule that training actually runs is not the check the scorer runs. Training's `Symbols.allow` only looks at a boolean flag. The scorer's `illegal_akshara` then flags every learned token that ends in a virama, including the truncated halant that `legal_token` explicitly accepts. On the Hindi holdout, all 2,204 illegal cuts from `tokenizer-full.json` are that case. Export makes it worse: `plan_chain` writes byte merges that `allow` never sees, and those merges split the vowel sign `े` into two invalid byte pieces.

`tokenizer-sarvam.json` has better tokens per word because the long Indic strings are still in the vocab. It has worse akshara cuts because many of those strings start with a vowel sign, which `illegal_akshara` rejects. It is not an improved Sarvam. The original Sarvam file encodes `नमस्ते` as `▁नम` + `स्ते`. The rebuilt file encodes it as `न` + `म` + `स्` + `ते`.

Logs used: `full.log` and `train.log` on `i-0676987ec61af5f49`, `sarvam-build.log` on `i-0c6550d199294585f`. No tokenizer file was rewritten.

## 1. Pair counts are updated after every merge

They are not frozen. `train_bpe` counts pairs on the in-memory sequences, and after each accepted merge it subtracts the old pairs and adds the pairs of the rewritten sequence.

```33:50:tokenizer-slices/trainer/bpe.py
def add_seq(wi: int, seq: array, weight: int, sign: int) -> None:
    local_buf.clear()
    n = len(seq)
    for i in range(n - 1):
        pair = (seq[i], seq[i + 1])
        local_buf[pair] = local_buf.get(pair, 0) + 1
    for pair, mult in local_buf.items():
        pair_count[pair] += sign * mult * weight
```

```87:130:tokenizer-slices/trainer/bpe.py
for wi in touched:
    seq = seqs[wi]
    ...
    for p, mult in old_local.items():
        if p == pair:
            continue
        pair_count[p] = pair_count.get(p, 0) - mult * weight
        ...
    seqs[wi] = out
    ...
    for p, mult in new_local.items():
        pair_count[p] = pair_count.get(p, 0) + mult * weight
        pair_words[p].add(wi)
        if pair_count[p] >= min_freq:
            heapq.heappush(heap, (-pair_count[p], p[0], p[1]))
```

The heap keeps stale entries. A popped pair is kept only when `pair_count[pair] == -neg` (`bpe.py` lines 68–72). That is a lazy heap, not a frozen table. `train_full.py` calls this same function (`train_full.main` → `t.train_bpe`). The full log reached `bpe 80000/80000` and then `bpe returned 80000 merges`, which is the loop above running to the reserve, not one pass over the initial counts.

## 2. The akshara rule can fail open, and the scorer is a different check

Training rejects a pair only here:

```359:368:tokenizer-slices/trainer/train_one.py
def allow(self, a: int, b: int) -> bool:
    if merge_crosses_space(self.surface[a], self.surface[b]):
        return False
    if self.ends[a] or self.ends[b]:
        return bool(self.ends[b])
    return True
```

`self.ends` is false for all 256 bytes. It becomes true only for an interned akshara (`intern_akshara`) and is then copied from the right-hand symbol (`on_merge` does `self.ends.append(self.ends[b])`). If both sides are bytes, `allow` returns true and never looks at the string. `train_bpe` records that pair as rejected only when `allow` returns false (`bpe.py` lines 73–77). A byte-byte merge is never rejected.

The scorer does not call `allow`. It calls `illegal_akshara`:

```71:92:tokenizer-slices/trainer/fertility.py
def illegal_akshara(text: str) -> bool:
    ...
    if is_dependent_char(body[0], script):
        return True
    if ends_with_dangling_virama(body, script):
        return True
    return not legal_token(text, script)
```

`legal_token` says the opposite about a trailing virama:

```247:250:tokenizer-slices/trainer/akshara.py
if script != "tamil" and ends_with_dangling_virama(body, script):
    # Truncated halant is a closed piece. It is legal as its own token.
    return True
```

So a token the trainer is allowed to keep is exactly what the scorer counts. `score_tokenizer` increments once per learned id whose decoded form fails that check (`fertility.py` lines 256–264). Bytes and the 32 specials are skipped (`N_PROTECTED = 288`).

On the Hindi holdout, `tokenizer-full.json` produced 2,204 illegal cuts and all 2,204 were `legal_but_dangling`: `ends_with_dangling_virama` was true and `legal_token` was also true. On the Kannada holdout, 34,508 illegal cuts, of which 26,754 were that same legal-but-dangling case and 7,754 started on a dependent mark. Stage 1's total was 94,191 and the full retrain's total was 94,238. The rule being "on" does not constrain the thing the score measures.

Export opens a second hole. `plan_chain` splits a symbol into single byte-alphabet characters and `commit` writes those pairs. Neither function calls `allow`:

```447:465:tokenizer-slices/trainer/train_one.py
def plan_chain(token: str, have: set[str]) -> list[tuple[str, str]] | None:
    parts = list(token)
    ...
    for part in parts[1:]:
        ...
        if nxt not in produced:
            needed.append((cur, part))
            produced.add(nxt)
```

`train_full.py` saves through `t.export_tokenizer`, which is this function. The learned merge may be two akshara atoms. The file contains the byte pairs underneath them, and the encoder applies those byte pairs anywhere in the pretoken.

## 3. The regex does not split matras

One Hindi word and one Kannada word each come out of `pretoken_pieces` as one piece. The akshara parser then keeps the matra inside the atom.

Measured with `pretoken_pieces` and `parse_aksharas` on the first machine:

| Word | Regex pieces | Parser pieces |
| --- | --- | --- |
| `नमस्ते` | `['नमस्ते']` | atom `न`, atom `म`, atom `स्ते` |
| `ಕನ್ನಡ` | `['ಕನ್ನಡ']` | atom `ಕ`, atom `ನ್ನ`, atom `ಡ` |

`स्ते` includes `्` and `े`. `ನ್ನ` includes the virama. The pattern is one optional non-letter and then a run of letters and marks (`pretoken.py` lines 12–20). A dependent vowel is `\p{M}`, so it stays in the word. Training is able to see the whole word. The broken vowel sign in the tables below is produced by the encoder, not by the regex.

## 4. Why the full retrain matches stage 1

The cap and the quotas were not what filled the 65,536 slots.

Stage 1 cuts every document in `_count_range`:

```298:299:tokenizer-slices/trainer/train_one.py
if len(text) > TRAIN_CHAR_CAP:
    text = text[:TRAIN_CHAR_CAP]
```

`TRAIN_CHAR_CAP = 4000`. `train_full._count_range` has no such slice. The full log records that:

- `language_caps=off`, `char_cap=off`, `document_char_cap=none`
- `counted docs=4154146 characters=8502290869 pretoken_types=21180699`
- `sequences=8212882 skipped=4796 aksharas=55341`
- `bpe returned 80000 merges`
- `wrote tokenizer-full.json vocab=65536`

Stage 1's log, same merge reserve, smaller count: `pretoken types=16728634`, `sequences=6549215`, `aksharas=50939`, `bpe returned 80000 merges`. Both runs then keep the first 65,248 merges `export_tokenizer` can commit (`N_LEARNED`). There is no per-language quota in either path. `train_full.py` prints `reserved_5500=no` and `reserved_26748=no` and never reads a slot table.

The extra 4,452,065 pretoken types sit in the long tail. The merges that win the first 65,248 places are the frequent pairs, which already occur in the first 4,000 characters. Learned-piece overlap: 61,328 of 65,248 are shared (94.0%). 3,920 pieces differ each way. Of the pieces only the full file has, the decoded breakdown is Latin or other 2,479, Devanagari 228, Bengali 227, Tamil 159, Gujarati 122, Telugu 82, Kannada 71. Tamil's tokens per word moved (5.452 in stage 1, 4.370 in the full file). The other languages did not, because the vocab barely did.

The encoded words match, except where the full file split one stage-1 piece. `गया` is `ग` + `य` + the two broken bytes of `ा` in both files. `ಕನ್ನಡ` is `ಕನ್` + `ನ` + `ಡ` in both files.

## 5. The Sarvam file did train English, and it did change Indic

The 14,034 English pieces were deleted. They were not copied back. `sarvam-build.log`:

```
dropped=28429 pieces malayalam=3592 odia=1956 punjabi=4751 english=14034 reserved=4096
kept ... total=38902
indic_pieces=38921 merges=38921
latin_slots=26327
latin sequences=1835688
latin merges trained=30327
indic residual matched on 7 sentences
wrote tokenizer-sarvam.json vocab=65536
```

`drop_bucket` classifies Sarvam English, the three dropped scripts, and `<<reserved_token_*>>`, and `select_indic` continues past those before any merge is built. `LatinSymbols.allow` only blocks a space in the middle of a merge. `latin_sequences` reads our English, code, and math jsonl and feeds `train_bpe`. That is a real BPE on our bytes: 1,835,688 sequences, 30,327 merges trained (`latin_slots + 4000`).

`assemble` places the 38,921 Indic pieces first (38,902 kept strings plus 19 byte scaffolds), then Latin merges, and stops at id 65,536. Leftover learned slots are `65248 - 38921 = 26327`. So 26,327 of the 30,327 trained English merges are in the file. The other 4,000 are the reserve past the cap. `65248` learned pieces are `26327 + 38921`.

A further 506 Indic pieces were not kept: the log's `regex_drop=506`. Devanagari in the Sarvam file is 12,126 before that filter and 11,953 kept. Those 506 are not part of the 14,034.

The Indic merge list is not Sarvam's merge list. `replay` copies a Sarvam pair only when both sides are kept Indic strings. A merge whose left side is `▁` fails that test, because the metaspace piece was dropped with English. `finish_unbuilt` then splits whatever is left at the first index where both sides already exist. `check_residual` only checks that seven sentences match this rebuilt Indic-only model after the English merges are appended. It does not load `sarvam/tokenizer.json`.

Original Sarvam versus `tokenizer-sarvam.json`, content pieces, ignoring the original file's leading `<s>`:

| Word | Original Sarvam | tokenizer-sarvam.json |
| --- | --- | --- |
| `नमस्ते` | `▁नम` `स्ते` | `न` `म` `स्` `ते` |
| `हिन्दी` | `▁ह` `िन्` `दी` | `ह` `िन्` `दी` |
| `ಕನ್ನಡ` | `▁ಕ` `ನ್ನ` `ಡ` | `ಕ` `ನ್ನ` `ಡ` |

`हिन्दी` and `ಕನ್ನಡ` survived. `नमस्ते` did not: two pieces became four. The rebuild is the reason. Tokens per word still beat `tokenizer-full.json` because the surviving pieces are long. The akshara total went to 195,530 because those pieces fail `illegal_akshara` for a different reason than the full model. On the Hindi holdout, 9,964 of the Sarvam file's illegal cuts start on a dependent mark (`िन्` is one). On the Kannada holdout, 34,006 of 42,906 start on a dependent mark. The original Sarvam encoder is the one that produced those cuts' strings. Our English BPE did not create them.

## Token sequences

`नमस्ते` is the bytes `e0 a4 a8  e0 a4 ae  e0 a4 b8 e0 a5 8d  e0 a4 a4  e0 a5 87`. The last unit is the vowel sign `े`.

`tokenizer-full.json`:

| Piece | Bytes | Note |
| --- | --- | --- |
| `न` | `e0a4a8` | |
| `म` | `e0a4ae` | |
| `स्` | `e0a4b8 e0a58d` | `स` plus virama. `illegal_akshara` is true. `legal_token` is true. |
| `त` | `e0a4a4` | |
| not UTF-8 | `e0a5` | first two bytes of `े` |
| not UTF-8 | `87` | last byte of `े` |

`tokenizer-sarvam.json` for the same word:

| Piece | Bytes | Note |
| --- | --- | --- |
| `न` | `e0a4a8` | |
| `म` | `e0a4ae` | |
| `स्` | `e0a4b8 e0a58d` | same dangling virama |
| `ते` | `e0a4a4 e0a587` | `त` plus `े`, one piece |

`ಕನ್ನಡ` is `ಕ` `ನ` virama `ನ` `ಡ`.

`tokenizer-full.json`:

| Piece | Bytes | Note |
| --- | --- | --- |
| `ಕನ್` | `e0b295 e0b2a8 e0b38d` | `ಕ` plus `ನ` plus virama. The conjunct is cut. |
| `ನ` | `e0b2a8` | the second `ನ`, left alone |
| `ಡ` | `e0b2a1` | |

`tokenizer-sarvam.json`:

| Piece | Bytes | Note |
| --- | --- | --- |
| `ಕ` | `e0b295` | |
| `ನ್ನ` | `e0b2a8 e0b38d e0b2a8` | the conjunct the parser built |
| `ಡ` | `e0b2a1` | |

Stage 1 emits the same `ಕನ್ನಡ` pieces as `tokenizer-full.json`.
