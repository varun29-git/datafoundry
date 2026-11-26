# Corpus handoff — local jobs stopped

Checked 2026-09-28 13:05 local. Corpus, trainer code, counts, and logs were left in place. Nothing was restarted.

## Processes

Gone. `ps` has no `build_15gb_corpus`, no `tokenizer-slices/trainer/pipeline.py`, no `train_worker.py`, and no `_count_range` children. `ps -p 48349,48356,50203,52749,52750` prints no rows.

SIGTERM stopped:

| PID | What |
| ---: | --- |
| 48356 | `build_15gb_corpus.py` |
| 48349 | zsh parent of that builder |
| 50203 | `pipeline.py` (`trainer/pipeline.pid`) |
| 52749 | child `_count_range` |
| 52750 | child `_count_range` |

`train_worker.py` was not running.

## Disk

`du -sh` corpus-15gb: **8.8G**

- english 3.5G
- hindi 1.6G
- kannada 1.0G
- marathi 1.3G
- telugu 1.3G

## Closed slices

22 `*.stats.json`. 21 have a jsonl. `kannada/translated-nemotron` is a missing-source marker (0 text bytes, no jsonl).

| stats.json | jsonl bytes |
| --- | ---: |
| english/climbmix.jsonl.stats.json | 2,248,253,599 |
| english/nemotron-cc-v2.1-hq-synth.jsonl.stats.json | 1,122,485,491 |
| english/rqa.jsonl.stats.json | 377,385,248 |
| hindi/fineweb2.jsonl.stats.json | 331,269,610 |
| hindi/sangraha-verified.jsonl.stats.json | 828,269,032 |
| hindi/translated-cosmopedia.jsonl.stats.json | 165,723,085 |
| hindi/translated-fact-seeking.jsonl.stats.json | 169,273,084 |
| hindi/translated-nemotron.jsonl.stats.json | 165,698,700 |
| marathi/fineweb2.jsonl.stats.json | 280,917,970 |
| marathi/sangraha-verified.jsonl.stats.json | 702,534,073 |
| marathi/translated-cosmopedia.jsonl.stats.json | 140,592,359 |
| marathi/translated-fact-seeking.jsonl.stats.json | 144,773,606 |
| marathi/translated-nemotron.jsonl.stats.json | 140,576,252 |
| telugu/fineweb2.jsonl.stats.json | 272,832,259 |
| telugu/sangraha-verified.jsonl.stats.json | 682,760,690 |
| telugu/translated-cosmopedia.jsonl.stats.json | 136,558,877 |
| telugu/translated-fact-seeking.jsonl.stats.json | 139,596,054 |
| telugu/translated-nemotron.jsonl.stats.json | 136,527,072 |
| kannada/sangraha-verified.jsonl.stats.json | 657,713,841 |
| kannada/translated-cosmopedia.jsonl.stats.json | 131,511,086 |
| kannada/translated-fact-seeking.jsonl.stats.json | 134,399,977 |
| kannada/translated-nemotron.jsonl.stats.json | none |

Unclosed, no stats file: `kannada/fineweb2.jsonl` is 146,278,704 bytes (cut mid-write).
