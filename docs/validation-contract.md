# Pretraining validation contract, 2026-11-06

The evaluation freeze and actual data were recorded in an external readiness
bundle that is not included in this repository. Its documented entry points are
`README.md`, `contract.json`, `weights.json`, `cell-budgets.json`,
`monitoring-policy.json` and a sealed validation manifest. The referenced
reusable build/scoring code is CI-1 `production/validation_data.py`,
`validation_evaluate.py` and `validation_generated.py`; those files are also
not included. No paid GPU was launched for this preparation.

The reference is the current one-trillion curriculum: 500B English and 500B
Indic, with Hindi 100B and the other six languages sharing 400B. Validation
weights follow the exact source/subsegment integer budgets and remain fixed
across data phases, LR changes, dense training and QAT. Parent sum rows are not
additional sources. Personas-India remains unallocated until a measured count
and equal English budget reduction exist.

The raw uint16 census now resolves all stored Indic specialized subsegment
counts: their sum is exactly 142,351,065,175. `raw-uint16-census.json` records
the cells, file counts and content tokens, calculated from even raw-bin byte
lengths. `cell-budgets.json` uses these exact subsegment counts. Their phase
floors cause small differences from the older language-level floors; the
Gujarati CC-v2 HQ adjustment is recomputed there to preserve phase totals.

## Holdout correction

Validation documents must be excluded completely before sequence packing.
Masking their targets still exposes their text as attention context. Every
existing `.val` document stays out of training, and all newly reserved indexed
documents in `training-exclusions.jsonl` stay out of every phase. Group equal
published origin IDs across languages/scripts/sources. Unknown translation
families with different IDs remain unresolved and are explicitly recorded.

The supplied index filter produces retained document spans. The packer must
read only those spans; reading the old bin unchanged is wrong. Bins remain
immutable. Actual packed-corpus exclusion application and its provenance must
be audited before training readiness can be claimed. Recompute usable source
draws after holdouts; follow the existing no-refill/no-second-epoch rules.
Nominal pool counts that include validation are not training capacity.

## Evaluation roles and scores

Development is for monitoring, candidate comparisons and checkpoint selection.
Final is for predeclared reporting checkpoints, with explicit access, and must
not choose the LR. The seal keeps identical published families in one role.
This is bounded source-file/window sampling, not a full population-random
sample or a complete near-duplicate/translation-family audit.

Primary: exact curriculum-weighted next-token NLL with all required cells.
Report each language, source and subsegment, native versus translated web,
native versus Latin specialized, macro loss and sample-token-weighted loss.
Missing cells cannot disappear through renormalization. Diagnostic incomplete
scores are allowed only with their missing coverage clearly labelled.

Generated capability data are pinned by upstream revision and SHA256:
GSM8K math, MBPP development/HumanEval final executable code, and IndicQA
context-based comprehension in the seven Indic languages. Scoring uses math
answer EM, QA normalized EM/token F1 and executable pass@1. These are separate
from NLL. Unknown benchmark overlap is explicitly unaudited, preserving the
existing preference to skip benchmark corpus scans and global MinHash.
Qualitative reviews use heldout sentence continuations, not factual quizzes.

## Production decisions still separate

The 50B data-phase warmup is not an authorization to replace the selected
1,006,632,960-token LR warmup. The sheet's 1M-real-token reference batch is not
the current 2,097,152-target global batch. Reconcile phase/update boundaries,
content-token versus EOD/target accounting, dense/QAT allocation and the funded
horizon when compiling the final production manifest. This evaluation freeze
changes no architecture, learning rate or global batch.

CC-Code-v1's planned 32B slice has no committed token shards at the configured
path and remains the missing validation cell. RQA and other nominal-all-source
draws require an after-holdout availability reconciliation. Native AMD scoring,
generation, telemetry and measured evaluation overhead still need the actual
hardware. The validation freeze does not certify a month-long production run.
