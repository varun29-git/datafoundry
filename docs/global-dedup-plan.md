# Global dedup on one m7i.8xlarge

This is the job that is executing. It writes a drop list. It does not tokenize, and it does not train.

Parent rules: [tokenize run plan](/cursor/stores/bc-3ba733cf-aea0-4cb0-a71b-053ddf16e5ee/docs/tokenize-run-plan.md). Where that note names a threshold and leaves the band layout open, the locked choices for this run are in the MinHash section below.

## Machine

One instance: `i-0676987ec61af5f49`, `m7i.8xlarge`, `us-east-1`, 32 vCPU, 128 GiB. Name `tokenizer-65k`.

`i-0c6550d199294585f` stays stopped. No `c7i` fleet.

Scratch: grow the gp3 volume so at least 500 GiB is free before the MinHash pass. Signatures spill to that disk. Same-region reads and writes on `s3://nemotron-training-data-us-east-1/`. Source prefixes are read. Nothing under `datasets/` or `translations/` is deleted or overwritten.

Stop this instance when the drop list and the count file are on S3.

## What is in the run

English text that is already in the bucket:

| Source | Prefix |
| --- | --- |
| ClimbMix | `datasets/nemotron-climbmix/karpathy-400b-shuffle/` |
| Math 4+ | `datasets/nemotron-cc-math-v1/4plus/` |
| MIND | `datasets/nemotron-cc-math-v1/4plus_MIND/` |
| RQA | `datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-RQA/` |
| Fact-Seeking | `datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/` |
| Specialized v1.1 | `datasets/Nemotron-Pretraining-Specialized-v1.1/` |
| InfiniByte | `datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-InfiniByte-Reasoning/` |
| CodeAlchemy | `datasets/codealchemy/` |
| Nemotron Code v2 | `datasets/nemotron-code-v2/` |
| Genesis III | `datasets/genesis-iii/` |

Indic text, seven languages only (Hindi, Bengali, Tamil, Telugu, Kannada, Marathi, Gujarati):

| Source | Prefix |
| --- | --- |
| Sangraha | `datasets/sangraha/verified/`, `synthetic/`, `unverified/` |
| FineWeb 2 | `datasets/fineweb2-indic/{hin_Deva,ben_Beng,tam_Taml,tel_Telu,kan_Knda,mar_Deva,guj_Gujr}/` |
| IndicCorp v2 | `datasets/indiccorp-v2/` |
| BhashaWiki | `datasets/bhashawiki/` |
| Cosmopedia | `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v5-20260906/` plus v4 rows whose source id is absent from v5 |
| Indic HQ-synthetic | `translations/Cosmopedia-v2/Krutrim/krutrim-nemotron-cc-v21-hq-synth-v1-20260906/` |
| Indic Fact-Seeking | `translations/.../fact-seeking-70shard-10lang-r16-20260903/` |

Text column is `text`, except Code v2 uses `content`, and CodeAlchemy uses `text` or else `text_with_placeholders`. IndicCorp is one document per non-empty line. Translation chunks read `translated_documents.parquet` only.

Resident text in the parent note is about 4–6 TB. The five new slices add about 690 GB and 342 million documents: CodeAlchemy 139 GB / 5.2M, Code v2 176 GB / 60.1M, Genesis 194 GB / 38.6M, IndicCorp 171 GB / 237.4M, BhashaWiki 9.2 GB / 1.0M.

## Rows that never enter a pass

- Empty text.
- Translation ids listed in that chunk’s `quarantine_manifest.jsonl`.
- Cosmopedia v4, salvage, and checkpoint rows whose source id is already in v5. `translation-staging/` stays out.
- Sangraha `*_Latn`, `verified/eng`, and every language outside the seven.
- Genesis rows whose `pipeline` is not option-level, and any Genesis file that does not say which pipeline it is. Those rows are absent from training. They are not drop-list entries.
- BhashaWiki has no Telugu and no Marathi. Kannada has no Indic HQ-synthetic.

## Identity and the exact-hash key

Document id, in order: `doc_id`, else `uuid`, else `{parquet key}:{row}`. IndicCorp uses `{object key}:{line}`.

Exact-hash key, locked for this run:

1. Unicode NFC.
2. CR and CRLF become LF.
3. Trailing spaces and tabs on each line are removed.
4. The hash is blake2b-256 of those bytes.

Code indentation stays. The hash is case-sensitive. A document shorter than one non-whitespace character is already empty and stays out.

## Pass 1 — exact duplicates

Stream every in-scope document once. On a repeated hash, one survivor stays and the other ids go to the drop list with reason `exact`.

Survivor when the two copies are in a named pair:

- Math 4+ keeps the row. ClimbMix drops.
- Math 4+ keeps the row. An HQ-synth page drops.
- ClimbMix keeps the row. An HQ-synth page drops.
- A MIND row whose hash matches its Math 4+ page drops.

Any other pair: keep the copy whose source is earlier in the tables above, English block first, then Indic. Inside one source, keep the lexicographically smaller document id.

The hash map spills to a disk sort when it no longer fits in RAM. One 16-byte digest plus the id is the record.

## Pass 2 — MinHash

Word 5-grams on the same normalized text. A word is a maximal run of non-whitespace. Documents with fewer than 5 words get no signature and can drop only on the exact hash or on decontamination.

Locked layout, because the parent note sets Jaccard and the gram size and leaves the bands open:

- 128 permutations, 64-bit, seed `65k-dedup-v1`.
- 16 bands of 8 rows.
- Web and math edge: estimated Jaccard at least 0.8.
- Code edge: estimated Jaccard at least 0.7.

Edges that are actually compared:

- ClimbMix, Math 4+, MIND, and Indic HQ-synthetic, each against the others in that set.
- CodeAlchemy against itself, Nemotron Code v2 against itself, and each against the other.

English HQ text is not in the bucket. The TinyLlama 15B pack is a later retokenize step, so it is not in this MinHash.

On a hit, the same winners as pass 1. A MIND row at 0.8 or above against its Math 4+ page drops even when the other pairs would have kept MIND. Code has no cross-source winner named in the parent note: inside a code pair, keep the lexicographically smaller document id and drop the other. A code document that also matches a web document is left alone by this pass. Those two families are separate graphs.

Implementation on this box: one band at a time. Write `(band, bucket, source, doc_id)` sorted on disk, group the bucket, confirm the Jaccard estimate on the signatures, then apply the winner. Do not hold every source’s full signature matrix in the 128 GiB. IndicCorp alone, if it were signed at 128 by 4 bytes, is about 120 GiB, and it is not on a MinHash edge.

## Pass 3 — benchmark decontamination

After the drop list from passes 1 and 2 exists, scan the survivors.

A document drops with reason `benchmark` when both are true against GSM8K test, MATH test, MMLU test, or MMLU-Pro:

- it shares a word 13-gram with an item in that test, and
- the longest common subsequence of words, divided by the shorter word count, is at least 0.6.

CodeAlchemy, Nemotron Code v2, and Specialized Code-Concepts also drop with reason `benchmark` when the document contains a HumanEval, MBPP, or DS-1000 prompt or solution.

The test sets are small enough to keep in RAM. This pass is one more read of the survivors.

## Gzip bands in this same job

ClimbMix, Math 4+, MIND, RQA, Fact-Seeking, and Specialized v1.1 already have zstd scores. CodeAlchemy, Code v2, Genesis III, IndicCorp v2, and BhashaWiki already have gzip level-6 scores. Those files are not scored again.

While a document from any other in-scope source is in memory, record gzip level 6, `mtime=0`, text bytes only, ratio = compressed / original. Under 512 bytes is mid. Easy is under 35%. Mid is 35% through 65%, including both ends. Hard is over 65%. Write those ratios beside the source, under `gzip6/`, in the same shape as the five finished slices. The sampler reads the ratio later. This job does not sort training bins.

## Output

Bucket `s3://nemotron-training-data-us-east-1/tokenized/tok65k/`. New keys only:

```
tokenized/tok65k/drop-list/
  exact/{source}.ids
  minhash/{source}.ids
  benchmark/{source}.ids
  counts.json
```

One document id per line. `counts.json` has, per source: documents read, excluded before the passes, dropped by `exact`, dropped by `minhash`, dropped by `benchmark`, survivors. A document in any drop file is a drop. The tokenize job skips those ids and does not refill the tokens.

## Time and cost

On this one machine, about a day and a half. A Python MinHash stretches that toward two days. The exact-hash pass is a few hours. The band-at-a-time MinHash is most of the clock. Decontamination is one more scan, a few hours.

`m7i.8xlarge` at the $1.61/hour rate in the parent note is about **$58–$77** of compute. The extra scratch disk for a day or two is about a dollar. Same-region S3 traffic is not a separate bill that matters next to the instance.

## Finished when

- Every in-scope object has a line in the pass log.
- Every id in the drop list was read from that source.
- No survivor id is also in a drop file.
- `counts.json` is on S3 and matches the line counts of the id files.
- `i-0676987ec61af5f49` is stopped. `i-0c6550d199294585f` is still stopped.

## After this, still not started

Token shards, the val split, the TinyLlama HQ retokenize, warmup / stable / annealing assignment, and the training run. Those wait until this drop list is the input.
