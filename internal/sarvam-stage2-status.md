# Sarvam build status

An `m7i.4xlarge` on-demand Linux instance had a list price of $0.8064 per hour. No other instance was launched.

Checked on 2026-09-28. The Sarvam Python process is **not alive**.

`tokenizer-sarvam.json` is already on disk, 6,389,108 bytes. The run that wrote it logged `wrote tokenizer-sarvam.json vocab=65536`. Drop line from that run: `dropped=28429 pieces malayalam=3592 odia=1956 punjabi=4751 english=14034 reserved=4096`.

The process was not running at the check, so a start was issued. It exited immediately. Latest log line: `refusing to overwrite <tokenizer-workdir>/trainer/tokenizer-sarvam.json`. `tokenizer-stage2.json` was not written.
