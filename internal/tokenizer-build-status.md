---
cursor:
  subagentId: "bc-858a2ab5-a401-54fd-84f4-ab381ac112af"
---

All seven gates passed. The 1.2B model was not trained. Indic merges were not rebuilt. `नमस्ते` is `▁नम` + `स्ते`.

The router now joins Indic words separated by one ordinary space into one Sarvam span. A space next to a Latin word stays a real space. Newlines, tabs, and runs of two spaces stay English. The vocabulary file is unchanged.

`i-0676987ec61af5f49` (`m7i.8xlarge`, name `tokenizer-65k`) was stopped, was started, ran the English tail, and is stopped again. `i-0c6550d199294585f` stayed stopped. No new instance was rented.

Artifacts:

- `docs/tokenizer-65k.json` sha256 `1bd42dcd4337ad1972f3069530baf235e1dd8a82238985200e89b360f23441d4`
- `docs/tokenizer-65k-freeze.md`

65,536 pieces, ids 0 through 65,535, no empty slots, no duplicate piece text. K = 40059. U = 435. English tail = 25189. Sarvam links = 40099. Vowel-mark starts = 2702. Broken UTF-8 = 0. Round-trip mismatches = 0. Cross-script pieces = 0. `<unk>` on the eval files = 0.

The earlier indic-id file was not on disk. Its recorded sha256 was `555661c77c0ba23b8441726cb9ae15bf1b5d79e8a3c1cee74393e161165c3e2d`. The ids were assigned again from `tokenizer.model` sha256 `4cd33409a577e8b416247587b0f5bd7a3eec245a1f18d4ec7793ff299ad3fbe2`. The loaded file still gives K = 40059, U = 435, tail = 25189, Latin 13596, and the script fingerprint Devanagari 12126, Telugu 5916, Kannada 5693, Bengali 5299, Gujarati 5274, Tamil 5100. U+200D (Sarvam id 67958) stays. Newline, carriage return, and tab stay dropped. The sha256 of this assignment file is `d0eabf4c1458b8ac505bb62aa3ca32992a0638e41f6ee936ef583d24caf27ccd`.

Gate 1, on the instance, 100 round-tripping sentences each: Hindi, Marathi, Kannada, Telugu, Tamil, Gujarati, Bengali. Fixtures `नमस्ते`, `हिन्दी`, and `ಕನ್ನಡ` match original Sarvam.

Gate 3 tokens per word, same held-out files:

| File | Ours | Original Sarvam |
| --- | ---: | ---: |
| English | 1.4254 | 1.5328 |
| Code | 2.0299 | 2.3825 |
| Math | 1.8574 | 1.9336 |

Training text, 4,000,001,475 UTF-8 bytes after NFC, documents capped at 4,000 characters. Mix by words: English 398,536,878, code 144,922,690, math 84,538,425 (33 / 12 / 7).

- English: ClimbMix `s3://nemotron-training-data-us-east-1/datasets/nemotron-climbmix/karpathy-400b-shuffle/`. Nemotron CC HQ is in the bucket and was not used.
- Code: CodeAlchemy is not in the bucket. No dataset is named Nemotron Code. The code share is half `Nemotron-Pretraining-Code-Concepts` and half `Nemotron-Pretraining-Scientific-Coding`.
- Math: half `nemotron-cc-math-v1/4plus/` and half `Nemotron-Pretraining-Math-Textbooks`. Finemath and SwallowMath are not separate corpora in the bucket.

TinyLlama uint16 packs were not used. The trainer script is `internal/build-65k.py`.
