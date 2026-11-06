---
cursor:
  subagentId: "bc-209970fa-5834-5abc-ace3-2bace1f46148"
---
# Dataset roundtrip smoke
`aws` credentials on this machine. Stock tokenizer `docs/hf-tokenizer`, `encode(..., add_special_tokens=False)`, no `<eod>` appended, then `decode` with the same tokenizer. A document counts as a match only when the decoded string is exactly the original. Gzip is level 6 with `mtime=0`. Under 512 bytes is mid and is not compressed. Easy is under 35%, mid is 35% through 65% including both ends, hard is over 65%.
Checked again with `Tokenizer.decode` on this same `tokenizer.json`. A newline, a tab, and repeated spaces come back as themselves. Rows below that call a newline the character `Ċ` are that marker still sitting in the decoded string from the smoke script. They are not lost text under the stock decoder.

What does not come back: a curly apostrophe becomes `'`, an en dash or em dash becomes `-`, `°` is a vocab piece that decodes to U+FFFD, and a few Hindi nukta spellings fold to NFC (`बड़ी` to `बड़ी`). Those are real.

Each row is about 40 documents from the first data page of one object (a dictionary page plus that page when the column is dictionary-encoded). Multi-GB objects were not downloaded. `datasets/nemotron-code-v2/synthetic-code-review/part_00005.parquet` was not read again. `translation-staging/` was not read. Smoke and pilot Fact-Seeking prefixes were not read.
| Source | Docs | Exact matches | Mismatches | Tokens | Bytes/token | Easy/mid/hard | Encode s | Gzip s | Decode s | Id violations |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| IndicCorp v2 | 40 | 31 | 9 | 2,569 | 9.675 | 3/37/0 | 0.062 | 0.002 | 0.119 | out 0, low 0 |
| ClimbMix | 40 | 24 | 16 | 20,281 | 4.358 | 0/40/0 | 0.468 | 0.003 | 0.122 | out 0, low 0 |
| Math 4+ | 40 | 30 | 10 | 36,429 | 3.007 | 4/36/0 | 0.945 | 0.004 | 0.119 | out 0, low 0 |
| MIND | 40 | 32 | 8 | 43,065 | 3.284 | 9/31/0 | 1.439 | 0.005 | 0.117 | out 0, low 0 |
| RQA | 40 | 0 | 40 | 182,295 | 3.307 | 2/38/0 | 24.268 | 0.019 | 0.171 | out 0, low 0 |
| Fact-Seeking | 40 | 32 | 8 | 4,112 | 3.012 | 0/40/0 | 0.021 | 0.000 | 0.114 | out 0, low 0 |
| Specialized v1.1 | 40 | 5 | 35 | 22,515 | 3.203 | 1/39/0 | 0.867 | 0.003 | 0.116 | out 0, low 0 |
| CodeAlchemy | 40 | 0 | 40 | 338,073 | 2.901 | 36/4/0 | 97.834 | 0.033 | 0.227 | out 0, low 0 |
| Nemotron Code v2 | 40 | 39 | 1 | 27,006 | 3.427 | 4/36/0 | 0.723 | 0.003 | 0.114 | out 0, low 0 |
| HQ synth | 40 | 24 | 16 | 23,134 | 4.721 | 0/40/0 | 0.647 | 0.004 | 0.110 | out 0, low 0 |
| Genesis III | 40 | 1 | 39 | 60,583 | 3.152 | 0/40/0 | 2.760 | 0.007 | 0.131 | out 0, low 0 |
| InfiniByte | 10 | 0 | 10 | 97,218 | 3.277 | 9/1/0 | 62.853 | 0.012 | 0.150 | out 0, low 0 |
| Sangraha verified | 40 | 0 | 40 | 28,995 | 8.681 | 35/5/0 | 7.437 | 0.015 | 0.131 | out 0, low 0 |
| Sangraha synthetic | 40 | 0 | 40 | 16,011 | 8.383 | 25/15/0 | 1.638 | 0.008 | 0.128 | out 0, low 0 |
| Sangraha unverified | 40 | 0 | 40 | 28,385 | 9.028 | 37/3/0 | 5.039 | 0.016 | 0.139 | out 0, low 0 |
| FineWeb 2 hin | 40 | 0 | 40 | 30,372 | 9.048 | 29/11/0 | 11.468 | 0.018 | 0.137 | out 0, low 0 |
| FineWeb 2 ben | 40 | 0 | 40 | 49,732 | 7.900 | 35/5/0 | 17.035 | 0.027 | 0.145 | out 0, low 0 |
| FineWeb 2 tam | 40 | 0 | 40 | 38,447 | 9.883 | 40/0/0 | 10.334 | 0.022 | 0.136 | out 0, low 0 |
| FineWeb 2 tel | 40 | 2 | 38 | 84,981 | 8.017 | 31/9/0 | 52.586 | 0.045 | 0.150 | out 0, low 0 |
| FineWeb 2 kan | 40 | 1 | 39 | 36,094 | 8.783 | 37/3/0 | 8.276 | 0.019 | 0.136 | out 0, low 0 |
| FineWeb 2 mar | 40 | 0 | 40 | 30,797 | 8.945 | 34/6/0 | 8.642 | 0.018 | 0.137 | out 0, low 0 |
| FineWeb 2 guj | 40 | 0 | 40 | 47,364 | 7.541 | 33/7/0 | 19.665 | 0.026 | 0.237 | out 0, low 0 |
| BhashaWiki hin | 40 | 40 | 0 | 31,623 | 9.114 | 20/20/0 | 18.029 | 0.020 | 0.129 | out 0, low 0 |
| Cosmopedia v5 | 40 | 0 | 40 | 37,444 | 10.973 | 40/0/0 | 7.267 | 0.028 | 0.145 | out 0, low 0 |
| Cosmopedia v4 | 40 | 0 | 40 | 37,837 | 9.718 | 40/0/0 | 6.300 | 0.024 | 0.139 | out 0, low 0 |
| Indic HQ-synthetic | 40 | 10 | 30 | 30,060 | 9.626 | 39/1/0 | 4.651 | 0.017 | 0.133 | out 0, low 0 |
| Fact-Seeking Indic | 40 | 0 | 40 | 3,572 | 6.347 | 1/39/0 | 0.050 | 0.001 | 0.119 | out 0, low 0 |

Id violations are ids outside 0–65535 (`out`) and ids in 0–31 (`low`), counted across every id of the documents in that row. Decode seconds include one load of `tokenizer.json` in that process, then the decode of these ids. Gzip seconds are only the level-6 compress used for the band. Encode seconds are the successful encodes only. A document that did not return inside 20 seconds is not in the row.

## What was read

| Source | Object | Column | Bytes pulled | Note |
| --- | --- | --- | ---: | --- |
| IndicCorp v2 | `datasets/indiccorp-v2/hin_Deva/hi-1.txt` | `lines` | 523,970 | hin_Deva head |
| ClimbMix | `datasets/nemotron-climbmix/karpathy-400b-shuffle/shard_00000.parquet` | `text` | 1,071,541 |  |
| Math 4+ | `datasets/nemotron-cc-math-v1/4plus/part_000000.parquet` | `text` | 274,826 |  |
| MIND | `datasets/nemotron-cc-math-v1/4plus_MIND/part_000000.parquet` | `text` | 326,072 |  |
| RQA | `datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-RQA/part_000000.parquet` | `text` | 257,032 |  |
| Fact-Seeking | `datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/part_000000.parquet` | `text` | 262,142 |  |
| Specialized v1.1 | `datasets/Nemotron-Pretraining-Specialized-v1.1/Nemotron-Pretraining-Code-Concepts/part_000000.parquet` | `text` | 170,642 | Code-Concepts |
| CodeAlchemy | `datasets/codealchemy/code-qa/train-00016-of-00031.parquet` | `text` | 41,347,473 | code-qa |
| Nemotron Code v2 | `datasets/nemotron-code-v2/synthetic-question-answering/part_00005.parquet` | `content` | 548,433 | synthetic-question-answering |
| HQ synth | `translations/Cosmopedia-v2/Krutrim/source-snapshots/Nemotron-CC-v2.1/High-Quality-Synthetic/part_000000.parquet` | `text` | 388,800 | v2.1 English text |
| Genesis III | `datasets/genesis-iii/college_maths/train-00001-of-00026.parquet` | `text` | 178,805 | college_maths pipeline values on this page: option_level×71, failure_analysis×57. Kept 40 option-level rows. |
| InfiniByte | `datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-InfiniByte-Reasoning/part_000000.parquet` | `text` | 1,051,475 | Encode timed out after 20s on 8 documents (character lengths 63445, 128067, 78531, 103909, 131866, 66835, 77552, 77890). 22 further documents over 30,000 characters were not sent after those timeouts. |
| Sangraha verified | `datasets/sangraha/verified/hin/data-0.parquet` | `text` | 2,101,875 | hin |
| Sangraha synthetic | `datasets/sangraha/synthetic/hin_Deva/wiki_hin_Deva_0000_of_0063.parquet` | `text` | 398,573 | hin_Deva |
| Sangraha unverified | `datasets/sangraha/unverified/hin/data-0.parquet` | `text` | 2,513,165 | hin |
| FineWeb 2 hin | `datasets/fineweb2-indic/hin_Deva/train/000_00000.parquet` | `text` | 1,425,928 |  |
| FineWeb 2 ben | `datasets/fineweb2-indic/ben_Beng/train/000_00000.parquet` | `text` | 2,118,779 |  |
| FineWeb 2 tam | `datasets/fineweb2-indic/tam_Taml/train/000_00000.parquet` | `text` | 2,279,131 |  |
| FineWeb 2 tel | `datasets/fineweb2-indic/tel_Telu/train/000_00000.parquet` | `text` | 2,983,780 |  |
| FineWeb 2 kan | `datasets/fineweb2-indic/kan_Knda/train/000_00000.parquet` | `text` | 2,044,401 |  |
| FineWeb 2 mar | `datasets/fineweb2-indic/mar_Deva/train/000_00000.parquet` | `text` | 1,862,343 |  |
| FineWeb 2 guj | `datasets/fineweb2-indic/guj_Gujr/train/000_00000.parquet` | `text` | 2,452,787 |  |
| BhashaWiki hin | `datasets/bhashawiki/hin_Deva/train-002-of-11.parquet` | `text` | 1,886,013 | smallest shard |
| Cosmopedia v5 | `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v5-20260906/language=mar_Deva/source=09b2e3f7a5a90612bfeda8e69b047ed9bb4811efa502b1d43740c6dd830b5c07/chunk=11d1bcaf56495c5989963eec76d915768a1642cfa00a07f2f750997b59c46c58/translated_documents.parquet` | `translation` | 2,403,911 | mar_Deva |
| Cosmopedia v4 | `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v4-20260905/language=hin_Deva/source=0c2b4d7f39a75370128f69a68b722315b7a913a2b9a9bd18510e6ca89cac1716/chunk=02dbd057a8502613cd8e3a443741b70f2bc06a9e5066fd78d735b320a8dc96a6/translated_documents.parquet` | `translation` | 2,376,089 | hin_Deva |
| Indic HQ-synthetic | `translations/Cosmopedia-v2/Krutrim/krutrim-nemotron-cc-v21-hq-synth-v1-20260906/language=hin_Deva/source=152b99982edf6d2f3846da7761e32c9ddbea67fc5ee68af2bf93e19b80168ddd/chunk=08cad0315f5ddbe80c2be95e1a0d7749c9180b138bdf8db22a777c1f52b967cf/translated_documents.parquet` | `translation` | 1,641,782 | hin_Deva |
| Fact-Seeking Indic | `translations/Nemotron-Pretraining-Specialized-v1.2/Fact-Seeking/indictrans2-en-indic-dist-200M-beam1-20260902/fact-seeking-70shard-10lang-r16-20260903/language=hin_Deva/source=18e67b6d4a372383a93b/chunk=00c5f47ee4e2eeeb507e1059777541f688a22c6b4c4e26f0d062448f5b6dea02/files/hin_Deva/translated_documents.parquet` | `translation_sha256` | 256,290 | hin_Deva; the column named translation is a hex digest, Hindi text is in translation_sha256 |

Plan rows that were missing on 1 October and are present now were smoked: CodeAlchemy, Nemotron Code v2, Genesis III, IndicCorp v2, BhashaWiki. English HQ is the v2.1 text snapshot in this bucket, not the TinyLlama `uint16` pack in the other bucket. IndicCorp v2 here is a newline-separated text file; the slice is the first 512 KiB of `hi-1.txt`, split on blank lines. Telugu and Marathi BhashaWiki folders are absent. Kannada has no Indic HQ-synthetic folder in the listing used here.

## Mismatches

A row is a mismatch when the decoded string is not exactly the original. NFC means the decode equals the NFC form of the original. Whitespace means folding U+010A `Ċ` back to a newline (and the same for tab, carriage return, and U+0120 `Ġ` to a space), or dropping whitespace, makes the strings equal. Anything else is lost text, including a newline left as `Ċ` when some other character also changed.

The same few changes show up across sources. Newlines often come back as the character `Ċ` instead of a line break, sometimes with a space added after it. Typographic apostrophes and dashes become ASCII (`’` to `'`, `–` and `—` to `-`). A degree sign, a copyright sign, or a middle dot sometimes comes back as U+FFFD. IndicCorp also rewrites a few nukta forms to NFC (`बड़ी` to `बड़ी`). None of those were counted as matches.

| Source | Mismatch kinds |
| --- | --- |
| IndicCorp v2 | 9 of 40: NFC 5, lost text 4 |
| ClimbMix | 16 of 40: lost text 14, whitespace 2 |
| Math 4+ | 10 of 40: lost text 10 |
| MIND | 8 of 40: lost text 8 |
| RQA | 40 of 40: lost text 30, whitespace 10 |
| Fact-Seeking | 8 of 40: lost text 8 |
| Specialized v1.1 | 35 of 40: lost text 34, whitespace 1 |
| CodeAlchemy | 40 of 40: lost text 40 |
| Nemotron Code v2 | 1 of 40: lost text 1 |
| HQ synth | 16 of 40: lost text 13, whitespace 3 |
| Genesis III | 39 of 40: lost text 39 |
| InfiniByte | 10 of 10: lost text 3, whitespace 7 |
| Sangraha verified | 40 of 40: whitespace 40 |
| Sangraha synthetic | 40 of 40: whitespace 40 |
| Sangraha unverified | 40 of 40: whitespace 40 |
| FineWeb 2 hin | 40 of 40: lost text 10, whitespace 30 |
| FineWeb 2 ben | 40 of 40: lost text 18, whitespace 22 |
| FineWeb 2 tam | 40 of 40: whitespace 30, lost text 10 |
| FineWeb 2 tel | 38 of 40: lost text 16, whitespace 22 |
| FineWeb 2 kan | 39 of 40: whitespace 35, lost text 4 |
| FineWeb 2 mar | 40 of 40: whitespace 28, lost text 12 |
| FineWeb 2 guj | 40 of 40: lost text 16, whitespace 24 |
| Cosmopedia v5 | 40 of 40: whitespace 38, lost text 2 |
| Cosmopedia v4 | 40 of 40: whitespace 39, lost text 1 |
| Indic HQ-synthetic | 30 of 40: whitespace 28, lost text 2 |
| Fact-Seeking Indic | 40 of 40: whitespace 39, lost text 1 |

Eight windows, taken at the first differing character. The window is not the whole document.

### IndicCorp v2

Looks like **NFC**. First difference at character 23. Original length 568, decoded length 571.

Original:

```
बुधवार सुबह 10.30 बजे बड़ी संख्या में एबीवीपी के छात्र नेता कॉले
```

Decoded:

```
बुधवार सुबह 10.30 बजे बड़ी संख्या में एबीवीपी के छात्र नेता कॉल
```

### ClimbMix

Looks like **lost text**. First difference at character 61. Original length 470, decoded length 470.

Original:

```
ques have been developed to improve wool’s washability by making the fiber more 
```

Decoded:

```
ques have been developed to improve wool's washability by making the fiber more 
```

### Math 4+

Looks like **lost text**. First difference at character 74. Original length 2026, decoded length 2026.

Original:

```
0 cm high and whose vertical angle is 60° is cut into two parts at the middle of
```

Decoded:

```
0 cm high and whose vertical angle is 60� is cut into two parts at the middle of
```

### RQA

Looks like **lost text**. First difference at character 741. Original length 11370, decoded length 11297.

Original:

```
 structure in the underlying primitive.  

Critically evaluate the following cla
```

Decoded:

```
 structure in the underlying primitive. ĊĊCritically evaluate the following clai
```

### CodeAlchemy

Looks like **lost text**. First difference at character 5. Original length 23136, decoded length 22227.

Original:

```
User:
**Problem – Counting pairs under a powe
```

Decoded:

```
User:Ċ**Problem - Counting pairs under a powe
```

### Sangraha verified

Looks like **whitespace**. First difference at character 261. Original length 2478, decoded length 2479.

Original:

```
न यह है कि स्पेस से वोटिंग होती कैसे है?
 इंटरनेशनल स्पेस स्टेशन (ISS) धरती से 2
```

Decoded:

```
न यह है कि स्पेस से वोटिंग होती कैसे है?Ċ इंटरनेशनल स्पेस स्टेशन (ISS) धरती से 2
```

### FineWeb 2 hin

Looks like **lost text**. First difference at character 488. Original length 1945, decoded length 1951.

Original:

```
काला और राज्य में सर्वत्र खुशहाली छा गई.
राजा ने लाओ-त्ज़ु से ची युंग की बड़ी ता
```

Decoded:

```
काला और राज्य में सर्वत्र खुशहाली छा गई.Ċ राजा ने लाओ-त्ज़ु से ची युंग की बड़ी त
```

### HQ synth

Looks like **lost text**. First difference at character 1509. Original length 5759, decoded length 5759.

Original:

```
atologists do more than examine the skin—they interpret it as a clinical map. Ma
```

Decoded:

```
atologists do more than examine the skin-they interpret it as a clinical map. Ma
```


## Excerpts

Two documents per source. Each pair is a short prefix of the original and the same span of the decode of that whole document.

### IndicCorp v2

17 documents were under 512 bytes and counted as mid without a gzip call.

Document 0 in this slice, 10 tokens, exact match.

Raw:

```
लोगों को बिलों संबंधी सुविधा देना ही उनका काम
```

Decoded:

```
लोगों को बिलों संबंधी सुविधा देना ही उनका काम
```

Document 15 in this slice, 119 tokens, exact match.

Raw:

```
उसका चेक नंबर 36 दर्शाया जा रहा है। व्यापारी ने बताया कि हमारे खाते में इस क्रमांक की कोई भी चेक जारी नहीं हुई हैद्ध यह किसी ने फर्जी तरीके से हमारे अकाउंट से चेक के माध्यम से पैसे निकाल कर अपने अकाउंट में जमा किए हैं। जिसकी सूचना व्यापारी ने बैंक ऑफ बड़ौदा शाखा प्रबंधक मैगलगंज को दी है। बैंक ऑफ बड़ौदा के शाखा प्रबंधक नीरज त्रिपाठी से बात की गई उन्होंने बताया सीतापुर की शाखा से
…
```

Decoded:

```
उसका चेक नंबर 36 दर्शाया जा रहा है। व्यापारी ने बताया कि हमारे खाते में इस क्रमांक की कोई भी चेक जारी नहीं हुई हैद्ध यह किसी ने फर्जी तरीके से हमारे अकाउंट से चेक के माध्यम से पैसे निकाल कर अपने अकाउंट में जमा किए हैं। जिसकी सूचना व्यापारी ने बैंक ऑफ बड़ौदा शाखा प्रबंधक मैगलगंज को दी है। बैंक ऑफ बड़ौदा के शाखा प्रबंधक नीरज त्रिपाठी से बात की गई उन्होंने बताया सीतापुर की शाखा से
…
```

### ClimbMix

4 documents were under 512 bytes and counted as mid without a gzip call.

Document 0 in this slice, 224 tokens, exact match.

Raw:

```
Protect your business and employee's during flu seaon

Starting in 2005, the Center for Disease Control (CDC) established the National Influenza Vaccination week "to highlight the importance of continuing flu vaccination through the holiday season and beyond." In 2017, by the end of November only about 41% of the recommended US population had been vaccinated.

…
```

Decoded:

```
Protect your business and employee's during flu seaon

Starting in 2005, the Center for Disease Control (CDC) established the National Influenza Vaccination week "to highlight the importance of continuing flu vaccination through the holiday season and beyond." In 2017, by the end of November only about 41% of the recommended US population had been vaccinated.

…
```

Document 15 in this slice, 649 tokens, exact match.

Raw:

```
Boost Coding Productivity
How To Get Value From Text File In Python
Reading from text files is an essential operation in Python. Text files are one of the most common ways to store data, and Python provides many ways to read data from them. In this tutorial, we will show you how to get value from a text file using Python.
Steps:
Step 1: Open the Text File
…
```

Decoded:

```
Boost Coding Productivity
How To Get Value From Text File In Python
Reading from text files is an essential operation in Python. Text files are one of the most common ways to store data, and Python provides many ways to read data from them. In this tutorial, we will show you how to get value from a text file using Python.
Steps:
Step 1: Open the Text File
…
```

### Math 4+

Document 0 in this slice, 907 tokens, exact match.

Raw:

```
# Jane Street

This employer has taken extra steps to respond to reviews and provide job seekers with accurate company information, photos, and reviews. Interested for your company? Learn More.

- Overview
- Reviews
- Salaries
- Interviews
- Jobs
- Photos
- Benefits

18 Reviews | 54 Salaries | 465 Interviews

## Interview Question

### Trader Intern Interview, New York, NY

…
```

Decoded:

```
# Jane Street

This employer has taken extra steps to respond to reviews and provide job seekers with accurate company information, photos, and reviews. Interested for your company? Learn More.

- Overview
- Reviews
- Salaries
- Interviews
- Jobs
- Photos
- Benefits

18 Reviews | 54 Salaries | 465 Interviews

## Interview Question

### Trader Intern Interview, New York, NY

…
```

Document 15 in this slice, 946 tokens, mismatch.

Raw:

```
# Nonograms Puzzle Guide

## How to Play Nonograms

Nonograms are picture logic puzzles that involve coloring a grid based on numerical clues. Below is a step-by-step guide on how to approach and solve these puzzles.

### Puzzle Overview

…
```

Decoded:

```
# Nonograms Puzzle Guide

## How to Play Nonograms

Nonograms are picture logic puzzles that involve coloring a grid based on numerical clues. Below is a step-by-step guide on how to approach and solve these puzzles.

### Puzzle Overview

…
```

### MIND

Document 0 in this slice, 923 tokens, mismatch.

Raw:

```
**Debate on NonEuclidean Geometry Concepts**

**Participant A:** Let's focus on the Hyperbolic Geometry example first. The model describes a scenario where given a line \( l \) and a point \( P \), the lines \( PX \) and \( PY \) are parallels through \( P \) to \( l \). This is because they intersect the boundary circle at points \( X \) and \( Y \). 

…
```

Decoded:

```
**Debate on NonEuclidean Geometry Concepts**

**Participant A:** Let's focus on the Hyperbolic Geometry example first. The model describes a scenario where given a line \( l \) and a point \( P \), the lines \( PX \) and \( PY \) are parallels through \( P \) to \( l \). This is because they intersect the boundary circle at points \( X \) and \( Y \). 

…
```

Document 15 in this slice, 986 tokens, exact match.

Raw:

```
**Interviewer:** Let's start by discussing the sequence of functions \( f_n(x) \) defined in the problem. Can you describe the behavior of these functions on the interval \([0, 1]\)?

**Subject Matter Expert:** Certainly. The sequence of functions \( f_n(x) \) is defined piecewise. For \( x \) in the interval \([0, 1/n]\), \( f_n(x) = 1 - nx \). For \( x \) in \([1/n, 1]\), \( 
…
```

Decoded:

```
**Interviewer:** Let's start by discussing the sequence of functions \( f_n(x) \) defined in the problem. Can you describe the behavior of these functions on the interval \([0, 1]\)?

**Subject Matter Expert:** Certainly. The sequence of functions \( f_n(x) \) is defined piecewise. For \( x \) in the interval \([0, 1/n]\), \( f_n(x) = 1 - nx \). For \( x \) in \([1/n, 1]\), \( 
…
```

### RQA

Document 0 in this slice, 3114 tokens, mismatch.

Raw:

```
Question: Consider an asymmetric encryption scheme Π proven IND-CCA2 secure in the random oracle model under the assumption that a trapdoor permutation family F is *partial-domain one-way* (PDOW). Suppose a subsequent analysis demonstrates that for the specific instantiation using permutation f, PDOW(f) is computationally equivalent to the standard one-wayness (OW) of f. Howeve
…
```

Decoded:

```
Question: Consider an asymmetric encryption scheme Π proven IND-CCA2 secure in the random oracle model under the assumption that a trapdoor permutation family F is *partial-domain one-way* (PDOW). Suppose a subsequent analysis demonstrates that for the specific instantiation using permutation f, PDOW(f) is computationally equivalent to the standard one-wayness (OW) of f. Howeve
…
```

Document 15 in this slice, 4307 tokens, mismatch.

Raw:

```
Question: In a coalescent analysis of three geographically structured populations (A, B, and C) of a marine invertebrate species with planktonic larval dispersal, the posterior probability density for the migration rate (m) between populations A and B is completely flat across the entire parameter space, while migration rates between A and C and B and C show well-constrained un
…
```

Decoded:

```
Question: In a coalescent analysis of three geographically structured populations (A, B, and C) of a marine invertebrate species with planktonic larval dispersal, the posterior probability density for the migration rate (m) between populations A and B is completely flat across the entire parameter space, while migration rates between A and C and B and C show well-constrained un
…
```

### Fact-Seeking

38 documents were under 512 bytes and counted as mid without a gzip call.

Document 0 in this slice, 48 tokens, exact match.

Raw:

```
How many times was the 10th Tank Corps formed during its history in the Red Army?
A. Once
B. Three times
C. Twice
D. Four times
Answer: C. Twice
```

Decoded:

```
How many times was the 10th Tank Corps formed during its history in the Red Army?
A. Once
B. Three times
C. Twice
D. Four times
Answer: C. Twice
```

Document 15 in this slice, 118 tokens, exact match.

Raw:

```
In January 1940, how did the Red Army command evaluate the performance of large tank corps, including the 10th Tank Corps?
A. They were deemed too small for modern warfare and needed expansion.
B. They were considered highly effective in combat operations.
C. They were judged to be unsatisfactory and led to disbandment.
…
```

Decoded:

```
In January 1940, how did the Red Army command evaluate the performance of large tank corps, including the 10th Tank Corps?
A. They were deemed too small for modern warfare and needed expansion.
B. They were considered highly effective in combat operations.
C. They were judged to be unsatisfactory and led to disbandment.
…
```

### Specialized v1.1

Document 0 in this slice, 1117 tokens, mismatch.

Raw:

```
from typing import List, Tuple

def detect_no_dup_range_gcd_mod(nums: List[int], queries: List[Tuple[int, int]], mod: int) -> List[int]:
    """Return the GCD modulo `mod` for each subarray [l, r] in `queries` if the subarray contains no duplicate values; otherwise return 0 for that query.

    The function expects 0‑based indices in `queries`.  
…
```

Decoded:

```
from typing import List, Tuple

def detect_no_dup_range_gcd_mod(nums: List[int], queries: List[Tuple[int, int]], mod: int) -> List[int]:
    """Return the GCD modulo `mod` for each subarray [l, r] in `queries` if the subarray contains no duplicate values; otherwise return 0 for that query.

    The function expects 0-based indices in `queries`.  
…
```

Document 15 in this slice, 832 tokens, mismatch.

Raw:

```
from typing import List, Tuple

def convex_hull_palindrome_transform(points_str: str) -> str:
    """
    Given a string of 2‑D points encoded as ``x,y;`` (the final ';' is optional),
    find the convex hull of all points, concatenating the hull coordinates *in
    the order returned by the hull algorithm*.  If the resulting character
…
```

Decoded:

```
from typing import List, Tuple

def convex_hull_palindrome_transform(points_str: str) -> str:
    """
    Given a string of 2-D points encoded as ``x,y;`` (the final ';' is optional),
    find the convex hull of all points, concatenating the hull coordinates *in
    the order returned by the hull algorithm*.  If the resulting character
…
```

### CodeAlchemy

Document 0 in this slice, 9017 tokens, mismatch.

Raw:

````
User:
**Problem – Counting pairs under a power constraint**

For a given positive integer `N` and an exponent `K` (`1 ≤ K ≤ 5`) we consider all ordered pairs
`(a, b)` of positive integers that satisfy  

```
a · b^K ≤ N .
```

How many such pairs exist?  
Print the answer modulo `998 244 353`.

--------------------------------------------------------------------

#### Input
…
````

Decoded:

````
User:Ċ**Problem - Counting pairs under a power constraint**ĊĊFor a given positive integer `N` and an exponent `K` (`1 ≤ K ≤ 5`) we consider all ordered pairsĊ`(a, b)` of positive integers that satisfy ĊĊ```Ċa · b^K ≤ N .Ċ```ĊĊHow many such pairs exist? ĊPrint the answer modulo `998 244 353`.ĊĊ--------------------------------------------------------------------ĊĊ#### InputĊThe f
…
````

Document 15 in this slice, 11498 tokens, mismatch.

Raw:

````
User:
**Permutation – Lehmer code and GCD**

For a permutation `p = (p₁ , p₂ , … , pₙ)` of the numbers `1 … n` define its
*Lehmer code* `L = (L₁ , L₂ , … , Lₙ)` by  

```
L_i = #{ j > i | p_j < p_i }      (0 ≤ L_i ≤ n‑i)
```

It is well known that the map `p ↔ L` is a bijection between permutations of
size `n` and sequences `L` satisfying the above bounds.

…
````

Decoded:

````
User:Ċ**Permutation - Lehmer code and GCD**ĊĊFor a permutation `p = (p₁ , p₂ , … , pₙ)` of the numbers `1 … n` define itsĊ*Lehmer code* `L = (L₁ , L₂ , … , Lₙ)` by ĊĊ```ĊL_i = #{ j > i | p_j < p_i }   (0 ≤ L_i ≤ n-i)Ċ```ĊĊIt is well known that the map `p ↔ L` is a bijection between permutations ofĊsize `n` and sequences `L` satisfying the above bounds.ĊĊFor a given integer `k` 
…
````

### Nemotron Code v2

Document 0 in this slice, 1025 tokens, exact match.

Raw:

```
You are tasked with implementing a simple fine-tuning of a pre-trained BERT (Bidirectional Encoder Representations from Transformers) model for a binary text classification task.

Assume that you have a labeled dataset of movie reviews with positive (1) and negative (0) sentiments. The dataset is available as a CSV file with two columns: 'text' (string) and 'label' (0 or 1). Yo
…
```

Decoded:

```
You are tasked with implementing a simple fine-tuning of a pre-trained BERT (Bidirectional Encoder Representations from Transformers) model for a binary text classification task.

Assume that you have a labeled dataset of movie reviews with positive (1) and negative (0) sentiments. The dataset is available as a CSV file with two columns: 'text' (string) and 'label' (0 or 1). Yo
…
```

Document 15 in this slice, 898 tokens, exact match.

Raw:

```
You are working with a cloud storage system where each file can belong to multiple folders. In this system, a file's parent folders are represented as a list of unique folder IDs. Your task is to implement a function that simulates moving a file into a new folder. The function must check whether the file is already in the target folder. If it is, the function should return the 
…
```

Decoded:

```
You are working with a cloud storage system where each file can belong to multiple folders. In this system, a file's parent folders are represented as a list of unique folder IDs. Your task is to implement a function that simulates moving a file into a new folder. The function must check whether the file is already in the target folder. If it is, the function should return the 
…
```

### HQ synth

Document 0 in this slice, 338 tokens, exact match.

Raw:

```
The Knitting Pilgrim is a one-man show by Kirk Dunn, an actor and knitter from Toronto, which is touring in British Columbia for the first time in April with performances in several cities. Dunn began creating three large knitted tapestries in 2003, each representing the Abrahamic religions of Judaism, Christianity, and Islam, and completed them in 2018. Unable to find a galler
…
```

Decoded:

```
The Knitting Pilgrim is a one-man show by Kirk Dunn, an actor and knitter from Toronto, which is touring in British Columbia for the first time in April with performances in several cities. Dunn began creating three large knitted tapestries in 2003, each representing the Abrahamic religions of Judaism, Christianity, and Islam, and completed them in 2018. Unable to find a galler
…
```

Document 15 in this slice, 200 tokens, exact match.

Raw:

```
A vintage postcard shows Houdini's actual Hollywood home. The comments discuss the remnants of the house, noting that the entire hillside where it stood was graded back, leaving nothing of the original structure. However, a few pilers from another demolished house on the same hill remain. There are currently three or four pilers left standing, often decorated with graffiti by a
…
```

Decoded:

```
A vintage postcard shows Houdini's actual Hollywood home. The comments discuss the remnants of the house, noting that the entire hillside where it stood was graded back, leaving nothing of the original structure. However, a few pilers from another demolished house on the same hill remain. There are currently three or four pilers left standing, often decorated with graffiti by a
…
```

### Genesis III

Document 0 in this slice, 1483 tokens, mismatch.

Raw:

```
# Cracking the Code: How to Solve That Tricky Polygon Question (And Why It Matters!)

## The Question That Will Test Your Geometry Instincts  
**What is the number of sides of a regular polygon with each interior angle measuring 160 degrees?**  
A. 10  
B. 12  
C. 16  
D. 18  

…
```

Decoded:

```
# Cracking the Code: How to Solve That Tricky Polygon Question (And Why It Matters!)ĊĊ## The Question That Will Test Your Geometry Instincts Ċ**What is the number of sides of a regular polygon with each interior angle measuring 160 degrees?** ĊA. 10 ĊB. 12 ĊC. 16 ĊD. 18 ĊĊThe answer? **D. 18**. But how do you get there? Let's break it down-and learn why mastering multiple-choic
…
```

Document 15 in this slice, 1316 tokens, mismatch.

Raw:

```
**Q:** Find the variance of a random variable \( X \) which takes the value 1 with probability 0.5 and 3 with probability 0.5.  
**Options:**  
A. 0.5  
B. 2  
C. 1  
D. 3  

**A:** The correct answer is **C. 1**. Let’s break down why and why the others are wrong.  

---

### **Why is the correct answer C (1)?**  
**Step-by-Step Analysis:**  
…
```

Decoded:

```
**Q:** Find the variance of a random variable \( X \) which takes the value 1 with probability 0.5 and 3 with probability 0.5. Ċ**Options:** ĊA. 0.5 ĊB. 2 ĊC. 1 ĊD. 3 ĊĊ**A:** The correct answer is **C. 1**. Let's break down why and why the others are wrong. ĊĊ---ĊĊ### **Why is the correct answer C (1)?** Ċ**Step-by-Step Analysis:** Ċ1. **Calculate the expected value \( E[X] \)
…
```

### InfiniByte

Document 0 in this slice, 9395 tokens, mismatch.

Raw:

```
Question: You are tasked with analyzing a batch of zinc oxide powder for purity before using it in the production of rubber. The purity of the zinc oxide is crucial for the quality of the final product. However, the presence of impurities like lead can affect the outcome. To ensure the zinc oxide meets the required standards, you need to verify if a given amount can be represen
…
```

Decoded:

```
Question: You are tasked with analyzing a batch of zinc oxide powder for purity before using it in the production of rubber. The purity of the zinc oxide is crucial for the quality of the final product. However, the presence of impurities like lead can affect the outcome. To ensure the zinc oxide meets the required standards, you need to verify if a given amount can be represen
…
```

Document 9 in this slice, 9277 tokens, mismatch.

Raw:

```
Question: Little Shino is interested in the fighting tournaments and their underlying dynamics. She notices that the strength of fighters can be influenced by external factors similar to how chemical reactions can be influenced by temperature and pressure. In a particular tournament, there are N fighters, each represented by i, with distinct strengths. The rules of the tourname
…
```

Decoded:

```
Question: Little Shino is interested in the fighting tournaments and their underlying dynamics. She notices that the strength of fighters can be influenced by external factors similar to how chemical reactions can be influenced by temperature and pressure. In a particular tournament, there are N fighters, each represented by i, with distinct strengths. The rules of the tourname
…
```

### Sangraha verified

1 documents were under 512 bytes and counted as mid without a gzip call.

Document 0 in this slice, 706 tokens, mismatch.

Raw:

```
अमेरिकी राष्ट्रपति चुनाव (US Presidential Election) के दिन नासा (NASA) की एस्ट्रॉनॉट केट रूबिन्स (Kate Rubins) अंतरिक्ष से वोट देंगी. 1997 में नासा के डेविड वूल्फ पहले एस्ट्रॉनॉट थे, जिन्होंने स्पेस से वोटिंग की थी. प्रश्न यह है कि स्पेस से वोटिंग होती कैसे है?
…
```

Decoded:

```
अमेरिकी राष्ट्रपति चुनाव (US Presidential Election) के दिन नासा (NASA) की एस्ट्रॉनॉट केट रूबिन्स (Kate Rubins) अंतरिक्ष से वोट देंगी. 1997 में नासा के डेविड वूल्फ पहले एस्ट्रॉनॉट थे, जिन्होंने स्पेस से वोटिंग की थी. प्रश्न यह है कि स्पेस से वोटिंग होती कैसे है?Ċ इंटरनेशनल स्पेस स्टेशन (ISS) धरती से 200 मील दूर स्थित है और पृथ्वी की कक्षा में 17000 मील प्रति घंटे से चक्कर लगाता 
…
```

Document 15 in this slice, 1097 tokens, mismatch.

Raw:

```
देश में कोरोना टीकाकरण (वैक्सीनेशन) अभियान की शुरुआत हो चुकी है. हालांकि, वैक्सीन को लेकर अभी लोगों के मन में कई तरह के सवाल हैं. दिल्ली में वैक्सीनेशन ड्राइव की शुरुआत धीमी रही, जिसे लेकर 'आजतक' ने कुछ हेल्थकेयर वर्कर्स से बातचीत की. जिसमें सामने आया कि वैक्सीनेशन ड्राइव की धीमी शुरुआत की एक वज़ह हेल्थकेयर वर्कर्स के मन में वैक्सीन को लेकर उठ रहे सवाल और डर है. कुछ को पिछले दि
…
```

Decoded:

```
देश में कोरोना टीकाकरण (वैक्सीनेशन) अभियान की शुरुआत हो चुकी है. हालांकि, वैक्सीन को लेकर अभी लोगों के मन में कई तरह के सवाल हैं. दिल्ली में वैक्सीनेशन ड्राइव की शुरुआत धीमी रही, जिसे लेकर 'आजतक' ने कुछ हेल्थकेयर वर्कर्स से बातचीत की. जिसमें सामने आया कि वैक्सीनेशन ड्राइव की धीमी शुरुआत की एक वज़ह हेल्थकेयर वर्कर्स के मन में वैक्सीन को लेकर उठ रहे सवाल और डर है. कुछ को पिछले दि
…
```

### Sangraha synthetic

6 documents were under 512 bytes and counted as mid without a gzip call.

Document 0 in this slice, 274 tokens, mismatch.

Raw:

```

मिनोलिया गिलवोस्प्लेंडेंस

मिनोलिया गिलवोस्प्लेंडेंस समुद्री घोंघे की एक प्रजाति है, जो सोलारीलिडे परिवार में एक समुद्री गैस्ट्रॉपोड मोलस्क है।
वर्णन।
खोल की ऊँचाई 6.5 मिमी और इसका व्यास 8 मिमी हो जाता है। चमकते, हल्के-सफेद खोल का आकार शंक्वाकार होता है और यह गहराई से नाभि वाला होता है। खोल में पाँच चक्कर होते हैं। छिद्र रैखिक है। स्तंभाकार सीमा कोने में संक्षेप में परिलक्षित 
…
```

Decoded:

```
Ċ मिनोलिया गिलवोस्प्लेंडेंसĊĊ मिनोलिया गिलवोस्प्लेंडेंस समुद्री घोंघे की एक प्रजाति है, जो सोलारीलिडे परिवार में एक समुद्री गैस्ट्रॉपोड मोलस्क है।Ċ वर्णन।Ċ खोल की ऊँचाई 6.5 मिमी और इसका व्यास 8 मिमी हो जाता है। चमकते, हल्के-सफेद खोल का आकार शंक्वाकार होता है और यह गहराई से नाभि वाला होता है। खोल में पाँच चक्कर होते हैं। छिद्र रैखिक है। स्तंभाकार सीमा कोने में संक्षेप में परिलक्
…
```

Document 15 in this slice, 439 tokens, mismatch.

Raw:

```

इरविंग एल्बरी

सर इरविंग जेम्स एल्बरी (12 मई 1879-14 नवंबर 1967) यूनाइटेड किंगडम में एक रूढ़िवादी पार्टी के राजनेता थे जिन्होंने 1924 से 1945 तक कब्रों के लिए संसद सदस्य (एमपी) के रूप में कार्य किया।
जीवनी।
…
```

Decoded:

```
Ċ इरविंग एल्बरीĊĊ सर इरविंग जेम्स एल्बरी (12 मई 1879-14 नवंबर 1967) यूनाइटेड किंगडम में एक रूढ़िवादी पार्टी के राजनेता थे जिन्होंने 1924 से 1945 तक कब्रों के लिए संसद सदस्य (एमपी) के रूप में कार्य किया।Ċ जीवनी।Ċ अभिनेत्री और नाट्य प्रबंधक मैरी मूर (बाद में लेडी विंडहम) और अभिनेता जेम्स एल्बरी एल्बरी के तीन बेटों में सबसे बड़े, पहली बार 1923 के आम चुनाव में संसद के लिए खड़े हुए,
…
```

### Sangraha unverified

Document 0 in this slice, 373 tokens, mismatch.

Raw:

```
बनारस से प्रकाशित "पूर्वांचल आजकल" के बंद होने की चर्चा । No. 1 Indian Media News Portal\nबनारस से प्रकाशित "पूर्वांचल आजकल" के बंद होने की चर्चा\nबनारस से प्रकाशित सांध्य दैनिक के बंद होने की चर्चाएं हैं. अखबार पिछले कुछ दिनों से शहर में नहीं दिख रहा है. कई दिनों से अखबार लोगों को पढ़ने को भी नहीं मिला है, जिसके चलते लोग कयास लगा रहे हैं कि अखबार बंद होने जा रहा है. पांच महीने
…
```

Decoded:

```
बनारस से प्रकाशित "पूर्वांचल आजकल" के बंद होने की चर्चा । No. 1 Indian Media News Portal\n बनारस से प्रकाशित "पूर्वांचल आजकल" के बंद होने की चर्चा\n बनारस से प्रकाशित सांध्य दैनिक के बंद होने की चर्चाएं हैं. अखबार पिछले कुछ दिनों से शहर में नहीं दिख रहा है. कई दिनों से अखबार लोगों को पढ़ने को भी नहीं मिला है, जिसके चलते लोग कयास लगा रहे हैं कि अखबार बंद होने जा रहा है. पांच मही
…
```

Document 15 in this slice, 499 tokens, mismatch.

Raw:

```
*अमेठी*- अमेठी जनपद के जामो थानाक्षेत्र की रहने वाली सोफिया बानो और उनकी बेटी अफसाना बानो ने लखनऊ में लोकभवन के सामने खुद को आग लगाकर आत्महत्या करने की कोशिश की थी। जिसमें बुरी तरह से जल गई सोफिया बानो की इलाज के दौरान मृत्यु हो गई थी। जबकि उनकी बेटी अफसाना बानो 40 फीसदी के लगभग जली थी।
…
```

Decoded:

```
*अमेठी*- अमेठी जनपद के जामो थानाक्षेत्र की रहने वाली सोफिया बानो और उनकी बेटी अफसाना बानो ने लखनऊ में लोकभवन के सामने खुद को आग लगाकर आत्महत्या करने की कोशिश की थी। जिसमें बुरी तरह से जल गई सोफिया बानो की इलाज के दौरान मृत्यु हो गई थी। जबकि उनकी बेटी अफसाना बानो 40 फीसदी के लगभग जली थी।Ċ जिसका इलाज आज भी चल रहा है, बताया जाता है कि जमीनी विवाद को लेकर न्याय न मिलने से दर दर की 
…
```

### FineWeb 2 hin

Document 0 in this slice, 561 tokens, mismatch.

Raw:

```
चीन में एक समय चोरों का बड़ा आतंक था. राज्य की राजधानी में ची युंग नामक एक व्यक्ति था जो किसी भी व्यक्ति का चेहरा देखकर यह बता देता था कि वह व्यक्ति चोर है या नहीं. सामनेवाले व्यक्ति के मुखमंडल के कुछ लक्षणों और उसके मन में चल रहे भावों को पढने में उसे महारत हासिल थी. उसका यह कौशल देखकर वहां के राजा ने उसे राज्य के नागरिकों के निरीक्षण में लगा दिया. ची युंग ने हजारों नागरिकों क
…
```

Decoded:

```
चीन में एक समय चोरों का बड़ा आतंक था. राज्य की राजधानी में ची युंग नामक एक व्यक्ति था जो किसी भी व्यक्ति का चेहरा देखकर यह बता देता था कि वह व्यक्ति चोर है या नहीं. सामनेवाले व्यक्ति के मुखमंडल के कुछ लक्षणों और उसके मन में चल रहे भावों को पढने में उसे महारत हासिल थी. उसका यह कौशल देखकर वहां के राजा ने उसे राज्य के नागरिकों के निरीक्षण में लगा दिया. ची युंग ने हजारों नागरिकों क
…
```

Document 15 in this slice, 590 tokens, mismatch.

Raw:

```
हम अक्सर मूर्ख विकल्प यद्यपि हम बेहतर पता होना चाहिए. तड़ित झंझा बुरी बात यह काला कर क्षितिज बादलों. हम फिर भी एक छतरी के बिना बाहर जाने की वजह से हम विचलित हैं और भूल जाते हैं. लेकिन हम करते हैं? पर Neurobiologists सॉल्क इंस्टीट्यूट ऑफ बायोलॉजिकल अध्ययन के लिए बाहर किए गए प्रयोगों है कि पहली बार है कि मस्तिष्क याद के लिए साबित भी अगर हम नहीं और छाता के पीछे रहता है. वे के अक्त
…
```

Decoded:

```
हम अक्सर मूर्ख विकल्प यद्यपि हम बेहतर पता होना चाहिए. तड़ित झंझा बुरी बात यह काला कर क्षितिज बादलों. हम फिर भी एक छतरी के बिना बाहर जाने की वजह से हम विचलित हैं और भूल जाते हैं. लेकिन हम करते हैं? पर Neurobiologists सॉल्क इंस्टीट्यूट ऑफ बायोलॉजिकल अध्ययन के लिए बाहर किए गए प्रयोगों है कि पहली बार है कि मस्तिष्क याद के लिए साबित भी अगर हम नहीं और छाता के पीछे रहता है. वे के अक्त
…
```

### FineWeb 2 ben

Document 0 in this slice, 6156 tokens, mismatch.

Raw:

```
প্রবাসী লেখকদের কলাম
একালের বাংলা সাহিত্যের সবচেয়ে জননন্দিত লেখক সদ্য প্রয়াত হুমায়ূন আহমেদের বেশিরভাগ লেখায় তাঁর প্রথম স্ত্রী গুলতেকিন এবং সন্তান নোভা-শীলা-বিপাশা-নুহাশদের প্রতি অদ্ভুত ভালবাসা দেখা গেছে । আবার দ্বিতীয় বিয়ের পর তাঁর সাহিত্যে অভিনেত্রী শাওন ও তার দুই ছেলে নিষাদ-নিনিত`র উপস্থিতি ছিল প্রবল।
…
```

Decoded:

```
প্রবাসী লেখকদের কলামĊ একালের বাংলা সাহিত্যের সবচেয়ে জননন্দিত লেখক সদ্য প্রয়াত হুমায়ূন আহমেদের বেশিরভাগ লেখায় তাঁর প্রথম স্ত্রী গুলতেকিন এবং সন্তান নোভা-শীলা-বিপাশা-নুহাশদের প্রতি অদ্ভুত ভালবাসা দেখা গেছে । আবার দ্বিতীয় বিয়ের পর তাঁর সাহিত্যে অভিনেত্রী শাওন ও তার দুই ছেলে নিষাদ-নিনিত`র উপস্থিতি ছিল প্রবল।Ċ আর এসময় প্রথম পক্ষের স্ত্রী-সন্তানরা ক্রমশ তাঁর জীবন ও সাহিত্য থেক
…
```

Document 15 in this slice, 1882 tokens, mismatch.

Raw:

```


| সিটি করপোরেশন নির্বাচনে
বিএনপির জটিল সমীকরণএই নির্বাচনে শাসকদলকে ফাঁকা মাঠে গোল দিতে দেবে না প্রধান বিরোধী দল। তারা আনুষ্ঠানিকভাবে নির্বাচনে অংশ নেবে না, তবে প্রার্থী দেবে।যাযাদি রিপোর্ট আসন্ন সিটি করপোরেশন নির্বাচনে প্রধান বিরোধী দল বিএনপি 'ধরি মাছ না ছুঁই পানি' কৌশল গ্রহণ করেছে। দলের শীর্ষ নেতৃত্ব চাচ্ছে বর্তমান নির্বাচন কমিশনকে বৈধতা না দিয়েই নির্বাচনে অংশগ্রহণ করতে। আর
…
```

Decoded:

```
ĊĊ | সিটি করপোরেশন নির্বাচনেĊ বিএনপির জটিল সমীকরণএই নির্বাচনে শাসকদলকে ফাঁকা মাঠে গোল দিতে দেবে না প্রধান বিরোধী দল। তারা আনুষ্ঠানিকভাবে নির্বাচনে অংশ নেবে না, তবে প্রার্থী দেবে।যাযাদি রিপোর্ট আসন্ন সিটি করপোরেশন নির্বাচনে প্রধান বিরোধী দল বিএনপি 'ধরি মাছ না ছুঁই পানি' কৌশল গ্রহণ করেছে। দলের শীর্ষ নেতৃত্ব চাচ্ছে বর্তমান নির্বাচন কমিশনকে বৈধতা না দিয়েই নির্বাচনে অংশগ্রহণ করতে। 
…
```

### FineWeb 2 tam

Document 0 in this slice, 262 tokens, mismatch.

Raw:

```
ராமநாதபுரம் ஜில்லா போர்டு தலைவர் W.P.A. சவுந்தரபாண்டியன் அவர்கள் மோட்டார் கம்பெனி முதலாளிகளுக்குப் பின்வருமாறு ஒரு சுற்றுக் கடிதம் அனுப்பியிருக்கிறார்கள். அது வருமாறு:
இந்த ஜில்லாவிலுள்ள சில மோட்டார் கம்பெனி முதலாளிகள் ஆதி திராவிடர்களை தமது பஸ்களில் ஏற்றிக் கொண்டு போவதில்லையென்றும் டிக்கெட்டில், ஆதிதிராவிடர்களுக்கு டிக்கட்டு கொடுக்கப்பட மாட்டாது என்று நிபந்தனை ஏற்படுத்தியிருப்ப
…
```

Decoded:

```
ராமநாதபுரம் ஜில்லா போர்டு தலைவர் W.P.A. சவுந்தரபாண்டியன் அவர்கள் மோட்டார் கம்பெனி முதலாளிகளுக்குப் பின்வருமாறு ஒரு சுற்றுக் கடிதம் அனுப்பியிருக்கிறார்கள். அது வருமாறு:Ċ இந்த ஜில்லாவிலுள்ள சில மோட்டார் கம்பெனி முதலாளிகள் ஆதி திராவிடர்களை தமது பஸ்களில் ஏற்றிக் கொண்டு போவதில்லையென்றும் டிக்கெட்டில், ஆதிதிராவிடர்களுக்கு டிக்கட்டு கொடுக்கப்பட மாட்டாது என்று நிபந்தனை ஏற்படுத்தியிருப்
…
```

Document 15 in this slice, 486 tokens, mismatch.

Raw:

```
விடுதலைப் புலிகள் அமைப்பின் தலைவர் பிரபாகரன் அவர்களின் மகன் பாலச்சந்திரன் இலங்கை இராணுவத்தால் கொல்லப்பட்ட புகைப்படம் வெளியாகி பரபரப்பை ஏற்படுத்திக் கொண்டிருக்கும் நிலையில் ஜெனீவாவில் நடைபெற்று வரும் ஐ.நா. மனித உரிமை கவுன்சில் கூட்டத்தில் இலங்கைக்கு எதிராக அமெரிக்கா தீர்மானம் கொண்டுவர திட்டமிட்டுள்ளது.
…
```

Decoded:

```
விடுதலைப் புலிகள் அமைப்பின் தலைவர் பிரபாகரன் அவர்களின் மகன் பாலச்சந்திரன் இலங்கை இராணுவத்தால் கொல்லப்பட்ட புகைப்படம் வெளியாகி பரபரப்பை ஏற்படுத்திக் கொண்டிருக்கும் நிலையில் ஜெனீவாவில் நடைபெற்று வரும் ஐ.நா. மனித உரிமை கவுன்சில் கூட்டத்தில் இலங்கைக்கு எதிராக அமெரிக்கா தீர்மானம் கொண்டுவர திட்டமிட்டுள்ளது.Ċ இந்தத் தீர்மானத்தை இந்திய அரசு ஆதரிக்க வேண்டும், இலங்கை இறுதிப் போரின்போது ப
…
```

### FineWeb 2 tel

Document 0 in this slice, 187 tokens, exact match.

Raw:

```
టాలీవుడ్ లో కళ్యాణ్ హీరోగా వచ్చిన కత్తి సినిమాలో , ఆ తరువాత మంచు మనోజ్ హీరోగా వచ్చిన మిస్టర్ నూకయ్య చిత్రాలలో నటించిన హాట్ భామ సనాఖాన్ గత కొన్నాళ్ళ నుండి వెండితెర పై కనిపించడం లేదు. తాజాగా ఈమె బిగ్ బాస్ - 6షోలో ఛాన్స్ కొట్టేసి మళ్ళీ ప్రేక్షకుల ముందుకు వచ్చింది. సనా ఖాన్ కి ఇదే మంచి అవకాశం అనుకుంటే అంత కంటే ఎక్కువ మంచి అవకాశం కొట్టేసింది. అదేంటంటే... బాలీవుడ్ కండల వీరుడు సల్మాన్
…
```

Decoded:

```
టాలీవుడ్ లో కళ్యాణ్ హీరోగా వచ్చిన కత్తి సినిమాలో , ఆ తరువాత మంచు మనోజ్ హీరోగా వచ్చిన మిస్టర్ నూకయ్య చిత్రాలలో నటించిన హాట్ భామ సనాఖాన్ గత కొన్నాళ్ళ నుండి వెండితెర పై కనిపించడం లేదు. తాజాగా ఈమె బిగ్ బాస్ - 6షోలో ఛాన్స్ కొట్టేసి మళ్ళీ ప్రేక్షకుల ముందుకు వచ్చింది. సనా ఖాన్ కి ఇదే మంచి అవకాశం అనుకుంటే అంత కంటే ఎక్కువ మంచి అవకాశం కొట్టేసింది. అదేంటంటే... బాలీవుడ్ కండల వీరుడు సల్మాన్
…
```

Document 15 in this slice, 905 tokens, mismatch.

Raw:

```
(ఈ టపాలు ఈ పుస్తకం గురించి నేను రాసుకుంటున్న నోట్సు. ముందు భాగాలు – ఇక్కడ)
*****
7) Willard Van Orman Quine : Word and Object
(మొదలుపెట్టే ముందు మూడు డిస్ క్లెయిమర్లు)
1) వ్యాసరచయితకి క్వైన్ మీద అంత సదభిప్రాయం ఉన్నట్లు లేదు
2) క్వైన్ పుస్తకం పేరు word and object అయినా, నాకు అర్థమైనంతలో ఈ పుస్తకం logic గురించి.
…
```

Decoded:

```
(ఈ టపాలు ఈ పుస్తకం గురించి నేను రాసుకుంటున్న నోట్సు. ముందు భాగాలు - ఇక్కడ)Ċ*****Ċ7) Willard Van Orman Quine : Word and ObjectĊ (మొదలుపెట్టే ముందు మూడు డిస్ క్లెయిమర్లు)Ċ 1) వ్యాసరచయితకి క్వైన్ మీద అంత సదభిప్రాయం ఉన్నట్లు లేదుĊ 2) క్వైన్ పుస్తకం పేరు word and object అయినా, నాకు అర్థమైనంతలో ఈ పుస్తకం logic గురించి.Ċ 3) ఈ వ్యాసం చదివినా, క్వైన్ వికీ పేజీ చదివినా - నాకు ఈయన రచనల గు
…
```

### FineWeb 2 kan

Document 0 in this slice, 1430 tokens, mismatch.

Raw:

```
ಜಾಗತೀಕರಣದ ಅಬ್ಬರ ಮತ್ತು ಸ್ಥಳೀಯ ಮಾರುಕಟ್ಟೆಯಲ್ಲಿನ ವಿದೇಶಿ ಸ್ಪರ್ಧೆಗಳನ್ನು ಯಾವುದೇ ಭಾವಾವೇಶಕ್ಕೆ ಒಳಗಾಗದೆ ಭಾರತೀಯರು ಸಮರ್ಥವಾಗಿ ಉದ್ದಿಮೆಗಳನ್ನು ಮುನ್ನಡೆಸುತ್ತಿದ್ದಾರೆ.
ಕಳೆದ ಕೆಲವು ತಿಂಗಳುಗಳಿಂದ ಎಲ್ಲೆಲ್ಲೂ ಉದ್ಯಮಿ ವಿಜಯ್ ಮಲ್ಯರದ್ದೇ ಸುದ್ದಿ. ಉದ್ಯಮದಲ್ಲಿ ಅವರು ಎದುರಿಸುತ್ತಿರುವ ಸಂಕಷ್ಟ, ಇನ್ನೇನು ಅವರ ಕಥೆ ಮುಗಿದೇ ಹೋಯ್ತು ಎಂದು ಸಂತಾಪ ಸೂಚಿಸಿ ಅನೇಕರು ಪುಟಗಟ್ಟಳೆ ಬರೆದುಬಿಟ್ಟರು. ಅವರ ಪ್ರಮುಖ ಉದ್ದಿಮೆ ಯುನೈಟೆಡ್ ಸ್ಪಿರಿಟ್ಸ್ ನ ಬಹುತೇಕ ಷೇರ
…
```

Decoded:

```
ಜಾಗತೀಕರಣದ ಅಬ್ಬರ ಮತ್ತು ಸ್ಥಳೀಯ ಮಾರುಕಟ್ಟೆಯಲ್ಲಿನ ವಿದೇಶಿ ಸ್ಪರ್ಧೆಗಳನ್ನು ಯಾವುದೇ ಭಾವಾವೇಶಕ್ಕೆ ಒಳಗಾಗದೆ ಭಾರತೀಯರು ಸಮರ್ಥವಾಗಿ ಉದ್ದಿಮೆಗಳನ್ನು ಮುನ್ನಡೆಸುತ್ತಿದ್ದಾರೆ.Ċ ಕಳೆದ ಕೆಲವು ತಿಂಗಳುಗಳಿಂದ ಎಲ್ಲೆಲ್ಲೂ ಉದ್ಯಮಿ ವಿಜಯ್ ಮಲ್ಯರದ್ದೇ ಸುದ್ದಿ. ಉದ್ಯಮದಲ್ಲಿ ಅವರು ಎದುರಿಸುತ್ತಿರುವ ಸಂಕಷ್ಟ, ಇನ್ನೇನು ಅವರ ಕಥೆ ಮುಗಿದೇ ಹೋಯ್ತು ಎಂದು ಸಂತಾಪ ಸೂಚಿಸಿ ಅನೇಕರು ಪುಟಗಟ್ಟಳೆ ಬರೆದುಬಿಟ್ಟರು. ಅವರ ಪ್ರಮುಖ ಉದ್ದಿಮೆ ಯುನೈಟೆಡ್ ಸ್ಪಿರಿಟ್ಸ್ ನ ಬಹುತೇಕ ಷೇ
…
```

Document 15 in this slice, 1210 tokens, mismatch.

Raw:

```
ಹರಿದುಬಂತು ಗಣವೇಷಧಾರಿ ಜನಸಾಗರ: ಒಂದೆಡೆ ಮಂಗಳೂರು ಅಂತಾರಾಷ್ಟ್ರೀಯ ವಿಮಾನ ನಿಲ್ದಾಣ, ಇನ್ನೊಂದೆಡೆ ಕೊಂಕಣ ರೈಲು ಮಾರ್ಗ, ಮಗದೊಂದೆಡೆ ಹಸಿರು ಪರಿಸರ. ನಡುವೆ ಸಮತಟ್ಟುಗೊಳಿಸಿದ 65 ಎಕರೆ ಮೈದಾನಕ್ಕೆ ಹರಿದುಬಂದಿತ್ತು ಗಣವೇಷಧಾರಿ ರಾಷ್ಟ್ರೀಯ ಸ್ವಯಂ ಸೇವಕ ಸಂಘದ ಸ್ವಯಂ ಸೇವಕರ ಸಾಲು ಸಾಲು.
…
```

Decoded:

```
ಹರಿದುಬಂತು ಗಣವೇಷಧಾರಿ ಜನಸಾಗರ: ಒಂದೆಡೆ ಮಂಗಳೂರು ಅಂತಾರಾಷ್ಟ್ರೀಯ ವಿಮಾನ ನಿಲ್ದಾಣ, ಇನ್ನೊಂದೆಡೆ ಕೊಂಕಣ ರೈಲು ಮಾರ್ಗ, ಮಗದೊಂದೆಡೆ ಹಸಿರು ಪರಿಸರ. ನಡುವೆ ಸಮತಟ್ಟುಗೊಳಿಸಿದ 65 ಎಕರೆ ಮೈದಾನಕ್ಕೆ ಹರಿದುಬಂದಿತ್ತು ಗಣವೇಷಧಾರಿ ರಾಷ್ಟ್ರೀಯ ಸ್ವಯಂ ಸೇವಕ ಸಂಘದ ಸ್ವಯಂ ಸೇವಕರ ಸಾಲು ಸಾಲು.Ċ ಕೆಂಜಾರು ಬಳಿ ಭಾನುವಾರ ನಡೆದ ಆರ್ಎಸ್ಎಸ್ನ ಸಾಂಘಿಕ್ ಕಾರ್ಯಕ್ರಮ ಸಂಜೆ 4.30ಕ್ಕೆ ಪ್ರಾರಂಭಗೊಳ್ಳಬೇಕಾಗಿದ್ದರೂ, ಮಧ್ಯಾಹ್ನ 12 ಗಂಟೆಯಿಂದಲೇ ಹರಿದುಬರುತ್ತಿದ್ದರು. ಸಂಜೆ ಕಾರ
…
```

### FineWeb 2 mar

Document 0 in this slice, 238 tokens, mismatch.

Raw:

```
www.24taas.com, भोपाळ
मध्य प्रदेशात लाईव्ह एन्टाऊंटर नाट्य घडलं. त्याचं असं झालं की, दरोडेखोरांनी लूट करताना तीन लाख पळविले. मात्र, पोलिसांना माहिती मिळताच त्यांनी घेराव घातला. पोलिसांना शरण येण्याऐवजी लुटारूंनी गोळीबार केला आणि चकमक झाली.
…
```

Decoded:

```
www.24taas.com, भोपाळĊ मध्य प्रदेशात लाईव्ह एन्टाऊंटर नाट्य घडलं. त्याचं असं झालं की, दरोडेखोरांनी लूट करताना तीन लाख पळविले. मात्र, पोलिसांना माहिती मिळताच त्यांनी घेराव घातला. पोलिसांना शरण येण्याऐवजी लुटारूंनी गोळीबार केला आणि चकमक झाली.Ċ मध्यप्रदेशातल्या एका गावात तीन दरोडेखोरांनी एका ठिकाणी तीन लाख रुपयांची लूट केली होती. पोलिसांना याची माहिती मिळताच दरोडेखोरांनी पैसे घेऊन
…
```

Document 15 in this slice, 228 tokens, mismatch.

Raw:

```
हे विजेट आपल्या ब्लॉगवर लावून या websiteची माहिती आपल्या वाचकांना देऊ शकता.
कोड तुमच्या ब्लॉगवर लवण्यासाठी Ctrl+C व Ctrl+V चा वापर करा
फेसबूकवर आमचे चाहते बना!
ट्विटरवर आमचे चाहते बना!
तुमचा ब्लॉग आमच्याशी जोडा
आम्ही आधिच promise केल्यानूसार "तुमचा ब्लॉग आमच्याशी जोडा!" हा विभाग सुरू करीत आहोत. इथे आपला ब्लॉग जर जोडला जावा असे वाटत असेल तर इथे click करा :
…
```

Decoded:

```
हे विजेट आपल्या ब्लॉगवर लावून या website ची माहिती आपल्या वाचकांना देऊ शकता.Ċ कोड तुमच्या ब्लॉगवर लवण्यासाठी Ctrl+C व Ctrl+V चा वापर कराĊ फेसबूकवर आमचे चाहते बना!Ċ ट्विटरवर आमचे चाहते बना!Ċ तुमचा ब्लॉग आमच्याशी जोडाĊ आम्ही आधिच promise केल्यानूसार "तुमचा ब्लॉग आमच्याशी जोडा!" हा विभाग सुरू करीत आहोत. इथे आपला ब्लॉग जर जोडला जावा असे वाटत असेल तर इथे click करा :Ċ तुमचा ब्लॉग आमच
…
```

### FineWeb 2 guj

Document 0 in this slice, 745 tokens, mismatch.

Raw:

```
સાયબરજગતમાં ‘દો કિસ્મ કે લોગ હોતે હૈં - એક જો ટેક્નોલોજી કા સહી ઉપયોગ કરતે હૈં, ઔર દૂસરે જો...' આ ‘દૂસરે' ટાઇપના લોકોમાં વાયરસ, સ્પાયવેર્સ, એડવેર્સ, ટ્રોજન, કી-લોગર્સ વગેરે વગેરેનો ફેલાવો કરનારા લોકોનો સમાવેશ થાય છે.
આ બધાં નામ જેમને થોડાં અજાણ્યાં લાગ્યાં હોય એમના માટે જરા ક્વિક રેફરન્સ...
…
```

Decoded:

```
સાયબરજગતમાં 'દો કિસ્મ કે લોગ હોતે હૈં - એક જો ટેક્નોલોજી કા સહી ઉપયોગ કરતે હૈં, ઔર દૂસરે જો...' આ 'દૂસરે' ટાઇપના લોકોમાં વાયરસ, સ્પાયવેર્સ, એડવેર્સ, ટ્રોજન, કી-લોગર્સ વગેરે વગેરેનો ફેલાવો કરનારા લોકોનો સમાવેશ થાય છે.Ċ આ બધાં નામ જેમને થોડાં અજાણ્યાં લાગ્યાં હોય એમના માટે જરા ક્વિક રેફરન્સ...Ċ વાયરસ એટલે આપણી જાણ બહાર કમ્પ્યુટરમાં ઘૂસી જતો નાનો પ્રોગ્રામ. જે મેડિકલ વાયરસની જેમ જ
…
```

Document 15 in this slice, 170 tokens, mismatch.

Raw:

```
જ્ઞાનની દિશા દ્રષ્ટિ
વિશ્વકોશે ‘જ્ઞાનની દિશા દ્દષ્ટિ‘ અંતર્ગત પણ એક નવું સોપાન માંડ્યું છે. ગુજરાત વિશ્વકોશ ટ્રસ્ટ જ્ઞાનની દિશા દ્દષ્ટિ નામનો એક કાર્યક્રમનું શૈક્ષણિક સંસ્થાઓ અને ગુજરાતી વિશ્વકોશ વચ્ચે સેતુ સાધવાનું આયોજન કર્યું. સ્કૂલો અને કૉલેજોમાં જઈને વિદ્યાર્થીઓને વિશ્વકોશના લેખકો આ પ્રવૃત્તિનું શૈક્ષણિક મહત્ત્વ સમજાવે છે. તેમજ એની ઉપયોગિતાનો ખ્યાલ આપે છે. વિશ્વકોશની સર્વન
…
```

Decoded:

```
જ્ઞાનની દિશા દ્રષ્ટિĊ વિશ્વકોશે 'જ્ઞાનની દિશા દ્દષ્ટિ' અંતર્ગત પણ એક નવું સોપાન માંડ્યું છે. ગુજરાત વિશ્વકોશ ટ્રસ્ટ જ્ઞાનની દિશા દ્દષ્ટિ નામનો એક કાર્યક્રમનું શૈક્ષણિક સંસ્થાઓ અને ગુજરાતી વિશ્વકોશ વચ્ચે સેતુ સાધવાનું આયોજન કર્યું. સ્કૂલો અને કૉલેજોમાં જઈને વિદ્યાર્થીઓને વિશ્વકોશના લેખકો આ પ્રવૃત્તિનું શૈક્ષણિક મહત્ત્વ સમજાવે છે. તેમજ એની ઉપયોગિતાનો ખ્યાલ આપે છે. વિશ્વકોશની સર્વ
…
```

### BhashaWiki hin

1 documents were under 512 bytes and counted as mid without a gzip call.

Document 0 in this slice, 88 tokens, exact match.

Raw:

```
पुरापुड़ा भारत के केरल राज्य के इडुक्की ज़िले में स्थित एक गाँव है। थोडुपुड़ा से पुरापुड़ा 25 मिनट के भीतर बस द्वारा पहुँचा जा सकता है। यह केवल थोडुपुड़ा से दूर है। जनसांख्यिकी भारत की जनगणना, पुरापुड़ा की जनसंख्या 12373 थी जिसमें 6280 पुरुष और 6093 महिलाएँ थीं। ।
```

Decoded:

```
पुरापुड़ा भारत के केरल राज्य के इडुक्की ज़िले में स्थित एक गाँव है। थोडुपुड़ा से पुरापुड़ा 25 मिनट के भीतर बस द्वारा पहुँचा जा सकता है। यह केवल थोडुपुड़ा से दूर है। जनसांख्यिकी भारत की जनगणना, पुरापुड़ा की जनसंख्या 12373 थी जिसमें 6280 पुरुष और 6093 महिलाएँ थीं। ।
```

Document 15 in this slice, 966 tokens, exact match.

Raw:

```
रोगन चित्रकला गुजरात, पेशावर और सिंध में प्रचलित कपड़े की छपाई की एक कला है। इस शिल्प में, उबले हुए अरंडी के तेल या अलसी के तेल और वनस्पति रंगों से बने पेंट को स्टाइलस का उपयोग करके कपड़े पर रखा जाता है। इस तेल आधारित पेंट को कपड़े पर लगाने की प्रक्रिया गुजरात में मुस्लिम खत्री समुदाय के बीच शुरू हुई। हालांकि रोगन नाम (और कुछ पारंपरिक डिजाइन) भारतीय संस्कृति में एक उत्पत्ति का 
…
```

Decoded:

```
रोगन चित्रकला गुजरात, पेशावर और सिंध में प्रचलित कपड़े की छपाई की एक कला है। इस शिल्प में, उबले हुए अरंडी के तेल या अलसी के तेल और वनस्पति रंगों से बने पेंट को स्टाइलस का उपयोग करके कपड़े पर रखा जाता है। इस तेल आधारित पेंट को कपड़े पर लगाने की प्रक्रिया गुजरात में मुस्लिम खत्री समुदाय के बीच शुरू हुई। हालांकि रोगन नाम (और कुछ पारंपरिक डिजाइन) भारतीय संस्कृति में एक उत्पत्ति का 
…
```

### Cosmopedia v5

Document 0 in this slice, 861 tokens, mismatch.

Raw:

```
 अध्याय 5: कर्लिंग धोरण आणि युक्त्या-तुमच्या विरोधकांना बर्फावर पछाडणे!

तुम्ही कधी कर्लर्स बर्फावर दगड चढवत पाहिले आहेत का, तर त्यांचे सहकारी समोर रागाने झाडू मारतात? रणनीती, कौशल्य आणि सांघिक कार्य यांचा मेळ घालणारा हा एक आकर्षक हिवाळी खेळ आहे! कर्लिंगच्या रोमांचक जगात प्रवेश करूया आणि काही विजयी धोरणे आणि डावपेच जाणून घेऊया.

**विभाग 1: कर्लिंगची मूलभूत तत्त्वे**

…
```

Decoded:

```
 अध्याय 5: कर्लिंग धोरण आणि युक्त्या-तुमच्या विरोधकांना बर्फावर पछाडणे!ĊĊ तुम्ही कधी कर्लर्स बर्फावर दगड चढवत पाहिले आहेत का, तर त्यांचे सहकारी समोर रागाने झाडू मारतात? रणनीती, कौशल्य आणि सांघिक कार्य यांचा मेळ घालणारा हा एक आकर्षक हिवाळी खेळ आहे! कर्लिंगच्या रोमांचक जगात प्रवेश करूया आणि काही विजयी धोरणे आणि डावपेच जाणून घेऊया.ĊĊ **विभाग 1: कर्लिंगची मूलभूत तत्त्वे**ĊĊ कर्लिंग
…
```

Document 15 in this slice, 750 tokens, mismatch.

Raw:

```
 सारा तिच्या योग चटईवर पाऊल ठेवत, संध्याकाळची दिनचर्या सुरू करण्यापूर्वी एक दीर्घ श्वास घेत असताना धूपाचा सुगंध हवा भरून गेला. ती अलीकडे संघर्ष करत होती-काम तणावपूर्ण होते, नातेसंबंध ताणलेले होते आणि ती असंतोषाची प्रचंड भावना हलवू शकली नाही. तिच्या चिकित्सकाने तिच्या दैनंदिन माइंडफुलनेस सरावात जाणीवपूर्वक कृतज्ञता जर्नलिंगचा समावेश करण्याचा सल्ला दिला, आशा केली की यामुळे तिचा द
…
```

Decoded:

```
 सारा तिच्या योग चटईवर पाऊल ठेवत, संध्याकाळची दिनचर्या सुरू करण्यापूर्वी एक दीर्घ श्वास घेत असताना धूपाचा सुगंध हवा भरून गेला. ती अलीकडे संघर्ष करत होती-काम तणावपूर्ण होते, नातेसंबंध ताणलेले होते आणि ती असंतोषाची प्रचंड भावना हलवू शकली नाही. तिच्या चिकित्सकाने तिच्या दैनंदिन माइंडफुलनेस सरावात जाणीवपूर्वक कृतज्ञता जर्नलिंगचा समावेश करण्याचा सल्ला दिला, आशा केली की यामुळे तिचा द
…
```

### Cosmopedia v4

Document 0 in this slice, 967 tokens, mismatch.

Raw:

```
 अध्याय 10: भांग के साथ बागवानी-सही तनाव का चयन करना

क्या आपने कभी भांग के साथ बागवानी के बारे में सुना है? जिस तरह हम घर पर फूलों और सब्जियों की देखभाल करते हैं, उसी तरह मारिजुआना को भी प्यार और ध्यान की आवश्यकता होती है ताकि यह स्वस्थ पौधों में विकसित हो सके! अपना खुद का भांग उद्यान शुरू करते समय विचार करने के लिए एक महत्वपूर्ण बात यह है कि सही तनाव का चयन करना है। लेकिन इसक
…
```

Decoded:

```
 अध्याय 10: भांग के साथ बागवानी-सही तनाव का चयन करनाĊĊ क्या आपने कभी भांग के साथ बागवानी के बारे में सुना है? जिस तरह हम घर पर फूलों और सब्जियों की देखभाल करते हैं, उसी तरह मारिजुआना को भी प्यार और ध्यान की आवश्यकता होती है ताकि यह स्वस्थ पौधों में विकसित हो सके! अपना खुद का भांग उद्यान शुरू करते समय विचार करने के लिए एक महत्वपूर्ण बात यह है कि सही तनाव का चयन करना है। लेकिन इस
…
```

Document 15 in this slice, 1306 tokens, mismatch.

Raw:

```
 इस पाठ्यक्रम इकाई में, हम अन्वेषण और खोज के इतिहास के साथ कॉमिक्स और ग्राफिक उपन्यासों के प्रतिच्छेदन में गहराई से विचार करेंगे। हम यह पता लगाएंगे कि यह अनूठा माध्यम विज्ञान, समाज और मानव जिज्ञासा के बीच जटिल संबंधों पर कैसे प्रकाश डाल सकता है। वैज्ञानिक विषयों और अन्वेषण के ऐतिहासिक क्षणों से जुड़े हास्य पुस्तकों और ग्राफिक उपन्यासों के उल्लेखनीय उदाहरणों की जांच के माध्यम से
…
```

Decoded:

```
 इस पाठ्यक्रम इकाई में, हम अन्वेषण और खोज के इतिहास के साथ कॉमिक्स और ग्राफिक उपन्यासों के प्रतिच्छेदन में गहराई से विचार करेंगे। हम यह पता लगाएंगे कि यह अनूठा माध्यम विज्ञान, समाज और मानव जिज्ञासा के बीच जटिल संबंधों पर कैसे प्रकाश डाल सकता है। वैज्ञानिक विषयों और अन्वेषण के ऐतिहासिक क्षणों से जुड़े हास्य पुस्तकों और ग्राफिक उपन्यासों के उल्लेखनीय उदाहरणों की जांच के माध्यम से
…
```

### Indic HQ-synthetic

Document 0 in this slice, 462 tokens, mismatch.

Raw:

```
धोखेबाज़ों को एक उचित सौदा मिलता है लेकिन अंत में दूसरों को धोखा देता है। वे छोटे पैमाने पर काम कर सकते हैं, जैसे कि एक स्ट्रीट कॉन कलाकार, या बड़े पैमाने पर, जैसे एक कॉर्पोरेट धोखेबाज।  

"धोखेबाज" का उपयोग करने वाले वाक्यों के उदाहरणों में शामिल हैंः धोखेबाज ने अपने मुवक्किल के निवेश को दोगुना करने का वादा किया लेकिन पैसे के साथ गायब हो गया; नकली दान चलाने वाले धोखेबाज को आखि
…
```

Decoded:

```
धोखेबाज़ों को एक उचित सौदा मिलता है लेकिन अंत में दूसरों को धोखा देता है। वे छोटे पैमाने पर काम कर सकते हैं, जैसे कि एक स्ट्रीट कॉन कलाकार, या बड़े पैमाने पर, जैसे एक कॉर्पोरेट धोखेबाज। ĊĊ "धोखेबाज" का उपयोग करने वाले वाक्यों के उदाहरणों में शामिल हैंः धोखेबाज ने अपने मुवक्किल के निवेश को दोगुना करने का वादा किया लेकिन पैसे के साथ गायब हो गया; नकली दान चलाने वाले धोखेबाज को आखि
…
```

Document 15 in this slice, 577 tokens, mismatch.

Raw:

```
रस अपने पोषण लाभों, ऊर्जा बढ़ाने और पौधों पर आधारित खाद्य पदार्थों के सेवन में वृद्धि के लिए लोकप्रिय हो गया है। जब आप सब्जियों का रस लेते हैं, तो आप अपने शरीर को पोषक तत्वों का एक केंद्रित स्रोत प्रदान करते हैं, जिसकी कई लोगों को फलों और सब्जियों में कम आहार के कारण आवश्यकता होती है। हालांकि, जो पहले से ही संतुलित आहार लेते हैं, उनके लिए रस में विटामिन और खनिजों की उच्च सांद्र
…
```

Decoded:

```
रस अपने पोषण लाभों, ऊर्जा बढ़ाने और पौधों पर आधारित खाद्य पदार्थों के सेवन में वृद्धि के लिए लोकप्रिय हो गया है। जब आप सब्जियों का रस लेते हैं, तो आप अपने शरीर को पोषक तत्वों का एक केंद्रित स्रोत प्रदान करते हैं, जिसकी कई लोगों को फलों और सब्जियों में कम आहार के कारण आवश्यकता होती है। हालांकि, जो पहले से ही संतुलित आहार लेते हैं, उनके लिए रस में विटामिन और खनिजों की उच्च सांद्र
…
```

### Fact-Seeking Indic

19 documents were under 512 bytes and counted as mid without a gzip call.

Document 0 in this slice, 86 tokens, mismatch.

Raw:

```
मरम्मत के बाद, अटलांटिक तट पर प्रशिक्षण के बाद यूएसएस लुडलो किस तारीख को भूमध्य सागर में लौटा?
A. 20 अप्रैल 1943
B. 20 अप्रैल 1942
C. 20 अप्रैल 1945
D. 20 अप्रैल 1944
उत्तरः D. 20 अप्रैल 1944
```

Decoded:

```
मरम्मत के बाद, अटलांटिक तट पर प्रशिक्षण के बाद यूएसएस लुडलो किस तारीख को भूमध्य सागर में लौटा?ĊA. 20 अप्रैल 1943ĊB. 20 अप्रैल 1942ĊC. 20 अप्रैल 1945ĊD. 20 अप्रैल 1944Ċ उत्तरः D. 20 अप्रैल 1944Ċ
```

Document 15 in this slice, 99 tokens, mismatch.

Raw:

```
जापान के आत्मसमर्पण के बाद यूएसएस लुडलो का नया मिशन क्या था?
A. अलेउशियन द्वीप समूह में नौसेना कर्मियों को प्रशिक्षण
B. सिसिली के आक्रमण के दौरान अग्नि सहायता प्रदान करना
C. जापान में कब्जे वाले सैनिकों को ले जाने वाले एस्कॉर्टिंग जहाज
D. भूमध्य सागर में पनडुब्बी रोधी गश्त का संचालन
उत्तरः C जापान में कब्जे वाले सैनिकों को ले जाने वाले एस्कॉर्टिंग जहाज
```

Decoded:

```
जापान के आत्मसमर्पण के बाद यूएसएस लुडलो का नया मिशन क्या था?ĊA. अलेउशियन द्वीप समूह में नौसेना कर्मियों को प्रशिक्षणĊB. सिसिली के आक्रमण के दौरान अग्नि सहायता प्रदान करनाĊC. जापान में कब्जे वाले सैनिकों को ले जाने वाले एस्कॉर्टिंग जहाजĊD. भूमध्य सागर में पनडुब्बी रोधी गश्त का संचालनĊ उत्तरः C जापान में कब्जे वाले सैनिकों को ले जाने वाले एस्कॉर्टिंग जहाजĊ
```

