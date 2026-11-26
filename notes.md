---
format: 2
description: Prepare a 1.5B multilingual pretraining mix for English and seven Indic languages.
taskPrefix: PT
---

## Tasks

### In Progress
- [ ] **PT-35** Import and tokenize Indic-CC Latin; no completed token census is linked

### Queued
- [ ] **PT-1** Serve the tokenizer in Transformers, vLLM, and llama.cpp
- [ ] **PT-3** Run the mass tokenization pass
- [ ] **PT-5** Tokenize the remaining CC-Code and RQA rows

### Done
- [x] **PT-34** Replace the Latin budget with the census [Curriculum](docs/one-trillion-curriculum.md)
- [x] **PT-33** Tokenize FineWeb-2 Latin prefixes [Counts](docs/indic-fineweb2-latin-token-counts.md)
- [x] **PT-32** Split every dataset row in the curriculum [Curriculum](docs/one-trillion-curriculum.md)
- [x] **PT-31** Raise Hindi to 100B in the curriculum [Curriculum](docs/one-trillion-curriculum.md)
- [x] **PT-25** Tokenize remaining Indic CC on Spot [Counts](docs/indic-cc-token-counts.md)
- [x] **PT-29** Design multilingual batch packing [Packing](docs/multilingual-batch-packing.md)
- [x] **PT-28** Tokenize restored High-Quality-DQA [Counts](docs/indic-cc-dqa-token-counts.md)
- [x] **PT-27** Write the 500B Indic curriculum [Curriculum](docs/indic-500b-curriculum.md)
- [x] **PT-26** Restore High-Quality-DQA on one on-demand box [Report](docs/indic-cc-dqa-restore.md)
- [x] **PT-23** Count FineWeb-2, IndicCorp, and Sangraha tokens [Counts](docs/indic-other-token-counts.md)
- [x] **PT-22** Drop v2.1 High-Quality-DQA from CC
- [x] **PT-21** Drop finepdfs-edu from the CC split
- [x] **PT-20** Tokenize specialized into the segment folders [Counts](docs/indic-specialized-token-counts.md)
- [x] **PT-19** Split CC into segment folders and project tokens [Projection](docs/indic-cc-token-projection.md)
- [x] **PT-18** Split specialized files into segment subfolders [Layout](docs/indic-specialized-segment-layout.md)
- [x] **PT-16** Copy seven native CC-v1 languages
- [x] **PT-17** Project specialized tokens per language and segment [Report](docs/indic-specialized-token-projection.md)
- [x] **PT-15** Count specialized documents per language and segment [Report](docs/indic-specialized-segment-counts.md)
- [x] **PT-14** Copy seven native specialized languages and 10B Latin to S3
- [x] **PT-12** Group Sangraha, FineWeb 2, and IndicCorp in S3
- [x] **PT-13** List specialized subsets for the seven languages [Report](docs/nemotron-indic-specialized.md)
- [x] **PT-4** Lock the English 500B mix [Mix](docs/english-500b-mix.md)
- [x] **PT-9** Check encode and decode on each source [Report](docs/dataset-roundtrip-smoke.md)
- [x] **PT-10** Save the first document from each source [Report](docs/dataset-first-samples.md)
- [x] **PT-11** Smoke one Nemotron Code page [Report](docs/nemotron-code-smoke.md)

### Canceled
- [x] **PT-30** Write the 1T curriculum file
- [x] **PT-6** Hold Personas-India for a later chat stage
- [x] **PT-24** Restore v2.1 High-Quality-DQA onto S3
- [x] **PT-2** Set aside global MinHash dedup [Plan](docs/global-dedup-plan.md)
- [x] **PT-7** Stop proxy mix decoding
- [x] **PT-8** Stop the stage-two feasibility pass [Report](docs/mutant-stage2-feasibility.md)
