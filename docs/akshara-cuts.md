# Akshara cuts in the frozen 65,536-token tokenizer

The piece strings and ids are unchanged. The encoder pre-segments into Unicode extended grapheme clusters and merges clusters only into pieces that already exist and that themselves end on cluster boundaries. `का` stays one unit (`का` | `र`). `क` | `ा` | `र` is not produced. A cluster with no covering piece is a counted byte fallback, not a cut through a matra or a virama.

On the same IndicCorp v2 lines as the previous measurement (leading complete lines, NFC text of at least 5,000,000 code points per language), the share of clusters that are split is:

| Language | Clusters split | Fallback clusters |
| --- | ---: | ---: |
| Hindi | 1.737% (58,065 / 3,342,331) | 58,747 |
| Marathi | 2.671% (82,990 / 3,107,367) | 83,909 |
| Kannada | 3.803% (125,456 / 3,298,809) | 129,583 |
| Telugu | 6.966% (197,154 / 2,830,031) | 199,740 |
| Tamil | 0.881% (28,866 / 3,274,727) | 32,097 |
| Gujarati | 2.863% (93,093 / 3,252,041) | 114,257 |
| Bengali | 4.299% (138,159 / 3,214,072) | 141,509 |

A fallback cluster is spelled with `<0xHH>` bytes. Single-code-point fallbacks have no between-code-point boundary, so the fallback count is higher than the split count. A walk of every piece boundary on these lines found no subword piece that starts or ends inside a cluster. The splits above are the byte boundaries inside uncovered clusters.

The boundary rate, with the same denominator as the previous measurement (between-code-point token boundaries, plus the junction between a line-final newline and the next line), is:

| Language | Boundaries inside a cluster |
| --- | ---: |
| Hindi | 8.397% (137,001 / 1,631,637) |
| Marathi | 11.811% (202,355 / 1,713,296) |
| Kannada | 8.669% (175,145 / 2,020,296) |
| Telugu | 21.133% (455,441 / 2,155,162) |
| Tamil | 1.947% (29,753 / 1,528,044) |
| Gujarati | 10.659% (203,976 / 1,913,717) |
| Bengali | 15.222% (306,558 / 2,013,963) |

Byte fallback of a long cluster places a boundary between every code point, so this rate can rise while the cluster-split rate falls. Hindi's two halves are 8.336% and 8.457% of boundaries, and 1.724% and 1.750% of clusters. Bengali is the widest cluster gap (4.215% vs 4.382%). The line counts and the NFC code-point totals match the previous sample exactly.

Normalization, applied before routing, is NFC, Unicode space separators folded to U+0020, curly quotes and unicode dashes folded onto ASCII pieces already in the vocabulary, and zero-width format characters removed except U+200C and U+200D. Tab, newline, and carriage return stay. No piece was added. A single ordinary space attaches to the following word, so `English शब्द` is `Eng` | `lish` | ` शब्द` and does not gain a separate cut between the space and `श`.

## Previous encoder

The previous encoder did cut inside Unicode extended grapheme clusters. On about 5 million characters of real text per language, the share of between-code-point token boundaries that fall inside a cluster, and the share of clusters that are split, are:

| Language | Boundaries inside a cluster | Clusters split |
| --- | ---: | ---: |
| Hindi | 5.018% (70,632 / 1,407,645) | 1.987% (66,408 / 3,342,428) |
| Marathi | 9.198% (129,835 / 1,411,524) | 4.028% (125,151 / 3,107,401) |
| Kannada | 17.392% (269,390 / 1,548,967) | 8.111% (267,694 / 3,300,463) |
| Telugu | 17.136% (268,007 / 1,564,006) | 9.115% (258,016 / 2,830,818) |
| Tamil | 12.064% (166,577 / 1,380,830) | 5.078% (166,296 / 3,274,950) |
| Gujarati | 7.834% (128,839 / 1,644,587) | 3.808% (123,838 / 3,252,119) |
| Bengali | 16.870% (261,065 / 1,547,543) | 7.845% (252,162 / 3,214,189) |

Matra splits were the majority of those bad boundaries in every language. Virama and conjunct splits are the next large class in Devanagari, Telugu, and Gujarati. Tamil and Kannada show fewer virama splits, because in Unicode 18 a Kannada or Tamil virama does not join the following consonant into the same extended grapheme cluster.

The two halves of each sample differ by at most 0.25 percentage points on the boundary rate and 0.18 points on the cluster rate. Bengali is the widest gap (16.746% vs 16.991% of boundaries). The others stay inside 0.15 points.

## What was counted

A bad cut is a token boundary that falls between code points of one extended grapheme cluster (`\X`). Clusters come from the `regex` module 2026.9.29, whose `\X` follows Unicode 18.0.0 (UCD dated 2026-08-07). Checked against that UCD: Devanagari, Bengali, Gujarati, and Telugu viramas are `InCB=Linker`, so consonant + virama + consonant is one cluster (`क्ष` is one cluster). Kannada and Tamil viramas are `InCB=Extend`, and their consonants are `InCB=None`, so `ಕನ್ನಡ` is four clusters (`ಕ`, `ನ್`, `ನ`, `ಡ`) and `தமிழ்` is three (`த`, `மி`, `ழ்`).

Each line was normalized to NFC, then passed through `Encoder.encode` in `internal/build-65k.py` with `docs/tokenizer-65k.json`. Neither file was modified. No Hugging Face tokenizer export was used.

Ids were not placed by guessing from the vocabulary. The encoder's router spans were walked on the original NFC string. Indic pieces were aligned to the normalized span (one leading `Ġ` is the dummy prefix; every other `Ġ` is a space). English pieces were aligned from the seed match or from the byte spans inside `Encoder.bpe`. Each piece was then decoded and had to equal that slice: a leading `Ġ` is stripped only when it is the dummy prefix, other `Ġ` characters become spaces, and `<0xHH>` is that byte. The id sequence had to equal `Encoder.encode` on the same string.

`Encoder.decode` is not a safe way to recover those offsets. On mixed Latin lines it can drop a space (300 of 1,427 Hindi lines that contain an ASCII letter do not round-trip). The piece alignment above still rebuilds those lines.

The boundary denominator is every between-code-point token boundary, including the boundary between a line-final newline and the first token of the next line. A newline is its own cluster, so that junction is never a bad cut. There are 32,422 to 46,266 such junctions per language. Boundaries that fall inside a UTF-8 code point are not in either rate. Their counts are below.

A cluster is split when at least one bad boundary lies strictly inside it. Spaces, digits, and Latin letters are clusters too, and they are rarely split, so the all-cluster rate is lower than the rate on clusters that contain a character of that language's block:

| Language | Script clusters split | Script characters |
| --- | ---: | ---: |
| Hindi | 2.989% (66,341 / 2,219,625) | 77.49% |
| Marathi | 5.641% (125,141 / 2,218,490) | 82.19% |
| Kannada | 10.682% (267,616 / 2,505,402) | 83.73% |
| Telugu | 12.800% (257,959 / 2,015,333) | 82.98% |
| Tamil | 6.670% (165,577 / 2,482,492) | 84.12% |
| Gujarati | 5.521% (123,828 / 2,242,933) | 79.80% |
| Bengali | 10.932% (249,138 / 2,278,878) | 81.21% |

## Matra splits and virama splits

A bad boundary is a matra split when the code point on the right is `Indic_Syllabic_Category=Vowel_Dependent`, or both sides are. It is a virama/conjunct split when either side is a virama or pure killer, when either side is ZWJ/ZWNJ inside a cluster that contains a virama, or when both sides are consonants inside a cluster that contains a virama. A boundary that is both is counted in both columns. The overlap is small. Everything else (mostly bindu/anusvara, nukta, or visarga) is "other".

| Language | Matra | Virama/conjunct | Both | Other | Clusters with a matra split | Clusters with a virama split |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Hindi | 44,317 | 16,138 | 25 | 10,202 | 44,286 | 13,956 |
| Marathi | 75,626 | 27,872 | 3 | 26,340 | 75,610 | 26,293 |
| Kannada | 208,580 | 30,185 | 32 | 30,657 | 208,455 | 29,516 |
| Telugu | 134,751 | 77,927 | 5 | 55,334 | 134,747 | 75,231 |
| Tamil | 159,005 | 6,340 | 1 | 1,233 | 158,909 | 6,328 |
| Gujarati | 72,027 | 37,602 | 55 | 19,265 | 71,917 | 35,533 |
| Bengali | 215,901 | 33,562 | 7 | 11,609 | 215,855 | 32,396 |

The common matra cut is consonant followed by a vowel sign (`consonant|matra`): 42,243 of Hindi's matra splits, 74,555 Marathi, 208,244 Kannada, 134,696 Telugu, 158,560 Tamil, 71,214 Gujarati, 207,223 Bengali. The common virama cuts are `consonant|virama` (the halant is detached from the consonant) and `virama|consonant` (the conjunct is broken after the halant). The second of those is inside the cluster only for scripts whose virama is a linker. In Kannada the largest virama class is `virama|joiner` (17,999), a ZWJ or ZWNJ still inside the `C + virama` cluster.

Bindu cuts are the bulk of "other". Hindi has 4,320 `consonant|bindu` and 3,526 `matra|bindu`. They leave the vowel sign on the consonant and split off anusvara. That is not counted as a matra split.

Token boundaries inside a code point, excluded from both rates:

| Language | Mid-code-point boundaries |
| --- | ---: |
| Hindi | 2,347 |
| Marathi | 2,257 |
| Kannada | 50,610 |
| Telugu | 80,735 |
| Tamil | 10,355 |
| Gujarati | 48,615 |
| Bengali | 19,752 |

## Sample

The training bucket `s3://<research-data-bucket>/datasets/indiccorp-v2/` was not reachable from this environment. There were no cloud credentials. The text is the public Hugging Face release of the same corpus, [ai4bharat/IndicCorpV2](https://huggingface.co/datasets/ai4bharat/IndicCorpV2), which is the corpus copied into that bucket. Hindi is `data/hi-1.txt` (one of the three Hindi files). The other languages are `data/mr.txt`, `data/kn.txt`, `data/te.txt`, `data/ta.txt`, `data/gu.txt`, and `data/bn.txt`.

Each sample is the leading complete lines of that file, not a draw from the vocabulary and not a random slice of the file. Lines were kept whole until the NFC text reached at least 5,000,000 code points.

| Language | File | File size (bytes) | Code points measured | UTF-8 bytes measured | Lines | Lines NFC changed | NFC code-point delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Hindi | `data/hi-1.txt` | 26,661,096,882 | 5,000,297 | 12,764,339 | 33,797 | 2,503 | +4,779 |
| Marathi | `data/mr.txt` | 14,553,660,884 | 5,000,482 | 13,235,711 | 35,003 | 313 | +384 |
| Kannada | `data/kn.txt` | 19,582,655,935 | 5,000,173 | 13,426,370 | 46,267 | 2,273 | −9,987 |
| Telugu | `data/te.txt` | 15,760,603,733 | 5,000,326 | 13,381,855 | 35,365 | 617 | −1,219 |
| Tamil | `data/ta.txt` | 11,790,368,869 | 5,000,060 | 13,429,214 | 32,423 | 279 | −908 |
| Gujarati | `data/gu.txt` | 14,130,326,225 | 5,000,028 | 12,988,822 | 39,867 | 0 | 0 |
| Bengali | `data/bn.txt` | 15,992,871,652 | 5,000,176 | 13,253,774 | 32,951 | 10,995 | +78,534 |

NFC matters because the Indic cutter normalizes each Indic span to NFC before BPE. The rates are on that string. Bengali grows because `U+09DF` BENGALI LETTER YYA canonically decomposes to YA + nukta and does not recompose. `নয়া` in the file is `নয়া` (YA + nukta) in the text that was cut. Gujarati did not change under NFC.

## Real bad cuts

`Ġ` is U+0120, the Indic space mark. A piece surface that starts with a space is the space before the word: that space lives in the same token as the first letters. Ids are the indexes in `pieces`.

### Hindi

**अडिग.** Cluster `डि` is ड + ि. The boundary between ड and ि is a matra split.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` अड` | `Ġअड` | 10708 |
| `िग` | `िग` | 12908 |

**किन्तु.** Cluster `न्तु` is न + ् + त + ु. The cut after न is a virama split. The cut after त is a matra split.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` किन` | `Ġकिन` | 8206 |
| `्त` | `्त` | 1317 |
| `ु` | `ु` | 40066 |

**चित्त.** Cluster `त्त` is त + ् + त. The cut is between त and ्.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` चित` | `Ġचित` | 21327 |
| `्त` | `्त` | 1317 |

### Marathi

**लसनिर्मिती.** Cluster `नि` is न + ि. The vowel sign is its own token.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` ल` | `Ġल` | 571 |
| `सन` | `सन` | 2125 |
| `ि` | `ि` | 40000 |
| `र्म` | `र्म` | 1345 |
| `िती` | `िती` | 2445 |

**घट्ट.** Cluster `ट्ट` is ट + ् + ट. The cut is between ट and ्.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` घट` | `Ġघट` | 2704 |
| `्ट` | `्ट` | 881 |

**रुग्णाच्या.** Cluster `ग्णा` is ग + ् + ण + ा. The cut is between ् and ण.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` रुग्` | `Ġरुग्` | 16849 |
| `णाच्या` | `णाच्या` | 18579 |

### Kannada

**ಶಾಂತಿಯ.** Cluster `ತಿ` is ತ + ಿ. The vowel sign starts the next token.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` ಶಾಂತ` | `Ġಶಾಂತ` | 18695 |
| `ಿಯ` | `ಿಯ` | 739 |

**ಕಳ್ಸಿದ್ರು.** Cluster `ಳ್` is ಳ + ್. The virama is its own token. The following ಸ is a separate cluster under Unicode 18, so the boundary between ್ and ಸ is not a bad cut.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` ಕಳ` | `Ġಕಳ` | 18307 |
| `್` | `್` | 40002 |
| `ಸ` | `ಸ` | 40069 |
| `ಿದ್ರು` | `ಿದ್ರು` | 38274 |

**ಸ್ವೀಕರಿಸಲು.** Cluster `ವೀ` is ವ + ೀ.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` ಸ್ವ` | `Ġಸ್ವ` | 3149 |
| `ೀಕ` | `ೀಕ` | 4802 |
| `ರಿಸಲು` | `ರಿಸಲು` | 6634 |

### Telugu

**రాముడికి.** Cluster `రా` is ర + ా.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` ర` | `Ġర` | 858 |
| `ాము` | `ాము` | 5393 |
| `డికి` | `డికి` | 15992 |

**నాథ్.** Cluster `థ్` is థ + ్. The virama is its own token.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` నా` | `Ġనా` | 2570 |
| `థ` | `థ` | 40263 |
| `్` | `్` | 40005 |

**భద్రాద్రి.** Cluster `ద్రా` is ద + ్ + ర + ా, and cluster `ద్రి` is ద + ్ + ర + ి. Both are cut between the consonant and the virama. Because Telugu virama is a linker, each of those is one cluster, so the boundary after the virama would also be inside it. Here the virama stays with the following consonant.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` భ` | `Ġభ` | 1313 |
| `ద` | `ద` | 40099 |
| `్రా` | `్రా` | 2469 |
| `ద` | `ద` | 40099 |
| `్రి` | `్రి` | 1716 |

### Tamil

**நாடுகளுக்கு.** Cluster `டு` is ட + ு.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` நாட` | `Ġநாட` | 7369 |
| `ுகளுக்கு` | `ுகளுக்கு` | 7090 |

**முக்தி.** Cluster `க்` is க + ் (virama split). Cluster `தி` is த + ி (matra split). The boundary between ் and த is a cluster boundary, not a bad cut.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` முக` | `Ġமுக` | 9673 |
| `்த` | `்த` | 562 |
| `ி` | `ி` | 40020 |

**இந்நாட்களில்.** Cluster `ந்` is ந + ். The virama is its own token.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| `இ` | `Ġஇ` | 653 |
| `ந` | `ந` | 40120 |
| `்` | `்` | 39997 |
| `நா` | `நா` | 21899 |
| `ட்க` | `ட்க` | 3626 |
| `ளில்` | `ளில்` | 1461 |

### Gujarati

**ઠેકાઓ.** Cluster `ઠે` is ઠ + ે. The vowel sign is its own token.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` ઠ` | `Ġઠ` | 12566 |
| `ે` | `ે` | 40018 |
| `કા` | `કા` | 1444 |
| `ઓ` | `ઓ` | 40192 |

**જથ્થો.** Cluster `થ્થો` is થ + ્ + થ + ો. The cut is between ્ and થ.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` જ` | `Ġજ` | 652 |
| `થ્` | `થ્` | 12441 |
| `થો` | `થો` | 17448 |

**કોંગ્રેસ.** Cluster `ગ્રે` is ગ + ્ + ર + ે. The cut is between ગ and ્.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` કોંગ` | `Ġકોંગ` | 20384 |
| `્રેસ` | `્રેસ` | 16827 |

### Bengali

**সচিন.** Cluster `চি` is চ + ি.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` সচ` | `Ġসচ` | 22066 |
| `িন` | `িন` | 1016 |

**আনুগত্য.** Cluster `নু` is ন + ু (matra split; ু is its own token). Cluster `ত্য` is ত + ্ + য (virama split).

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| ` আন` | `Ġআন` | 7901 |
| `ু` | `ু` | 40132 |
| `গত` | `গত` | 4227 |
| `্য` | `্য` | 609 |

**বাংলাদেশে.** Cluster `বাং` is ব + া + ং. The anusvara is its own token. That boundary has the matra on the left and bindu on the right, so it is an "other" cut, not a matra split: `বা` stayed together. The final `ে` is a separate matra split of `শে`.

| Surface | Vocab piece | Id |
| --- | --- | ---: |
| `বা` | `Ġবা` | 1437 |
| `ং` | `ং` | 40178 |
| `লা` | `লা` | 2374 |
| `দেশ` | `দেশ` | 5817 |
| `ে` | `ে` | 40017 |

The same `বা` / `ং` / `লা` cut is the freeze-note example for `বাংলা`. It shows up here inside a corpus word, not as a vocabulary lookup.
