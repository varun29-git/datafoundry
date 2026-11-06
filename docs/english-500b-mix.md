# English mix, 500B

**Superseded 2026-11-06 by the final curriculum in [one-trillion-curriculum.md](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/one-trillion-curriculum.md) — that file is the authority (Code-v1 dropped, Rewriting and UltraData-Code L3 added, ClimbMix resized, Personas counted). The rows below are kept as history.**

Decided 2026-10-19. Decay composition revised 2026-11-03: the window is now 40% web. This is the English half of the run. Indic is a separate 500B of Nemotron Indic v1. Draws are one pass. A short census is not refilled from another row.

| Dataset | Use | Share |
| --- | ---: | ---: |
| ClimbMix | 268.8B of 380.16B | 53.8% |
| Math 4+ | 61.4B, all of it | 12.3% |
| Nemotron Code v2 | 55.2B, all of it | 11.0% |
| Nemotron-CC-Code-v1 | 32B of 427.9B | 6.4% |
| InfiniByte | 22.5B, all of it | 4.5% |
| Genesis III, option-level | 15B of 43B | 3.0% |
| RQA | 14.4B | 2.9% |
| Specialized v1.1 | 11.1B, all of it | 2.2% |
| CodeAlchemy, `code-dev` and `code-enhance` | 10B | 2.0% |
| Fact-Seeking | 9.6B, all of it | 1.9% |
| Nemotron-Personas-India | all of it, size not counted yet | |

The counted rows still sum to 500.0B. Personas-India is in the mix on top of that until its token count is known and another row is cut by the same amount.

## Decay

The last 50B, while the learning rate decays:

| Dataset | Use |
| --- | ---: |
| ClimbMix | 20B |
| Math 4+ | 9B |
| Nemotron Code v2 | 6B |
| Nemotron-CC-Code-v1 | 3B |
| InfiniByte | 3B |
| Genesis III, option-level | 3.5B |
| RQA | 2.5B |
| Specialized v1.1 | 2B |
| Fact-Seeking | 1B |

Revised 2026-11-03: ClimbMix raised 12B to 20B so the window is 40% web, matching the Blakeney, OLMo 2, and SmolLM anneal recipes, which keep a large web share in decay. Funded by trimming decay Math 4+ (10 to 9), Code v2 (8 to 6), CC-Code-v1 (4 to 3), InfiniByte (4 to 3), Genesis (5 to 3.5), RQA (3.5 to 2.5), and Fact-Seeking (1.5 to 1).

The other 450B is whatever remains of the table above.

## Out

- HQ synthetic. Rephrases of web already represented in ClimbMix.
- MIND. Dialogues written from the Math 4+ pages. Not a replacement for those pages.
- Genesis failure analysis. That split quotes a wrong answer, and the benchmark echoes that were found sat there.
- CodeAlchemy `code-dialogue` and `code-qa`.
- CodeTrace. It was not downloaded.
## Not in the bins yet

- Nemotron-CC-Code-v1. The 32B slice still has to be downloaded. Gated under the same NVIDIA training agreement as Code v2. https://huggingface.co/datasets/nvidia/Nemotron-CC-Code-v1
- RQA. 9.4B is already tokenized. The other 5B still has to be tokenized from the RQA files already stored.
