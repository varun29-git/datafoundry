---
cursor:
  subagentId: "bc-28b76c37-ae46-5ec5-abf1-c8a0f418c78f"
---

# Tokenizer trainer status

Trainer: `/Users/varundaiya/Data Complete/tokenizer-slices/trainer/`

`tokenizer.json`: not written yet. Export runs only after latin, hindi, marathi, tamil, telugu, kannada, bengali, and gujarati models all exist.

Pipeline: PID 50203, parent PID 1, log `trainer/cpu-log.txt`, choices in `trainer/choices.json` (Picky skipped, 81,920 not trained, 150M proxy not run). Corpus builder PID 48356 was left running and was not reniced.

## Segments

Counted: `english/climbmix` (1,917,026 types, 26 MB pickle, smoke 1.169 pre-tokens per word on 3,000 docs).

In progress at last check: `english/nemotron-cc-v2.1-hq-synth` (smoke 1.183, one counter).

Not trained yet: every script. Latin waits for english, math, and code counts. Hindi waits until every finished Hindi slice is counted.

## CPU schedule in use

`hw.physicalcpu` 8, `hw.ncpu` 8. While the corpus process is alive, usable cores are 6. Pre-tokenization is one worker on slices of 800 MB or more, because free RAM stayed near 1.7–2.4 GB. Script merges stay serial per script. Parallel trainers are capped at 1 while available RAM is under 2.5 GB, and at 2 once it is at least 3.5 GB. Idle checks sleep 20 seconds. Climbmix counter RSS peaked near 210 MB.
