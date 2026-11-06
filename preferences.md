# Preferences

- Skip global MinHash dedup on this pretraining mix. The sources are separate products, and leftover copies of high-quality text are acceptable. Added 2026-10-05.
- Do not scan these datasets for benchmark overlap. They are published corpora, used as released. No GSM8K, MATH, MMLU, HumanEval, MBPP, or DS-1000 filter in tokenization. Updated 2026-10-06.
- Deploy the tokenizer as stock Hugging Face BPE, Sarvam score order, even though that cuts inside some Indic letters. Grapheme locking is dropped. Updated 2026-10-05.
- For the 1.5B data mix, use MiniCPM, Gemma, and Qwen as the reference. Do not use SmolLM 2 or SmolLM 3. Added 2026-10-19.
- The English mix is proportions of the datasets already tokenized. Do not replace them with new sources. Added 2026-10-19.
