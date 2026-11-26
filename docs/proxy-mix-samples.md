# Proxy mix samples

Checked 5 October 2026 on this machine. Nothing was tokenized. No EC2 instance was started. No token file was decoded, because none was reachable.

## What the store names

A search of the research workspace found no manifest, prefix, or note that names an already-tokenized proxy-model mix of about 10 billion tokens, and no list of that mix’s segments.

The only line that uses those words is the open task in `notes.md`. Nearby notes describe other things:

- [tokenizer-plan.md](tokenizer-plan.md) assumes a 150M proxy and a 20B-token budget, and says no perplexity result exists.
- [tokenizer-trainer-status.md](../internal/tokenizer-trainer-status.md) says the 150M proxy was not run. Its “segments” are tokenizer-training counts (`english/climbmix` counted, `english/nemotron-cc-v2.1-hq-synth` in progress), not a tokenized model mix.
- [training-curriculum.md](training-curriculum.md) tells the reader to run the written weights first and to start a proxy mixture search only if a later gate fails. Its 12B row is a planning budget, not a stored bin.

The new 65,536 tokenizer was not used. The mix never named a tokenizer, because the mix itself is not named.

## Buckets

Both buckets answer in `us-east-1` and refuse an anonymous list.

| Bucket | Request | Result |
| --- | --- | --- |
| `s3://<research-data-bucket>/` | `GET` `prefix=tokenized/` | HTTP 403 `AccessDenied` |
| `s3://<research-pack-bucket>/` | `GET` `prefix=data/` | HTTP 403 `AccessDenied` |

This machine had no AWS environment variables, credential files, instance-role metadata, AWS CLI, or boto3. The objects were not read.

## Local samples

No local token bin, `.uint16` part, or proxy-mix manifest is on this machine. The workspace was an empty git checkout. The store has tokenizer JSON files and notes, not token ids.

The 27 September inventory, quoted from [training-curriculum.md](training-curriculum.md), lists token packs that are not this mix and were not opened today:

| Pack | Tokenizer the inventory records | Why it is not the sample |
| --- | --- | --- |
| `data/nemotron_cc_v2_hqsynth_tinyllama_15b_parallel_20260730T185305Z/` | TinyLlama `uint16`, 15,000,000,001 train tokens | One source, 15B, not a ~10B mix. A 1 October Mac decode of five windows is already in [curriculum-mix-samples.md](../internal/curriculum-mix-samples.md). Those windows were not re-read here. |
| `openhermes25_assistant_sft_20260803/` | TinyLlama, 251,398,213 train tokens | Supervised pack, far under 10B. |
| `test16/nemotron_pretraining_fact_seeking_10b_tinyllama_tokenized_20260714.tar` | Filename says TinyLlama; 20,000,071,680 bytes | The inventory says the archive was not unpacked and that `10b` in the name is not a measured token count. |
| `test16/cosmo15b.bin` | Not opened | 30,000,441,182 bytes. Not described as a multi-segment mix. |
| `test16/fineweb_edu_score_4_dedup_tinyllama_tokenized_20260714.tar` | Filename says TinyLlama | Not unpacked. |
| `test16/test2_new_sources.summary.json` | — | Describes an older TinyStories plus Cosmopedia job. The inventory says it does not describe the large `test16` files. |

## Segments

There is no segment to judge. No document was decoded, so there is no excerpt, no id-range check, and no empty-or-unknown check.
