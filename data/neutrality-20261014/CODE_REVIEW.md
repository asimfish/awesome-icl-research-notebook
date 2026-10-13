# B1 protocol/code review — BLOCKED

1. **Verdict: BLOCKED.** The current cohort constructor fails before any controller rollout. This is a scoped protocol/code gate, not an efficacy pilot or a novelty review.

2. **Dimensions.**
- Functional achievement: **Fail**. `fresh_dataset(4,1)` raises `RuntimeError: historical exclusions changed` at `experiments/adaptation/evidence_neutrality.py:83`.
- Correctness/reliability: **Fail** for cohort reconstruction; five documented semantic tests pass (5 tests,0 failures/errors,0.051s).
- Architecture and API: **Pass within inspected scope**. Hidden graph is absent from `model.inputs` and factual guards; policy receives receipts/state/goal. Version spaces are independent per-action supports, not joint Bayes.
- Maintainability: **Pass within inspected scope**; no material additional structure finding.
- Performance/bounds: **Unable to determine end-to-end** because smoke is withheld; graph-only preparation promise is violated by historical `make_cases` calls (F2).

3. **Blocking findings.**
- **F1 — Missing confirmation exclusions** (`experiments/adaptation/evidence_neutrality.py:79-83`). The union includes base759 closure classes and own-stream256, omitting the confirmation256 produced with seed4812 inside `task_stream.stream_dataset`. Its size is1015, so the required1271 assertion fails. Focused runtime reproduction confirms the failure. Lowering the count would admit historical classes and is not a repair.
- **F2 — Historical rollout reconstruction contradicts protocol** (`experiments/adaptation/evidence_neutrality.py:79-81`; `run_pilot.py:20`; `train_query_prefix.py:39`; `task.py:80`). These dataset helpers call `make_cases`, which actually executes old simulator transitions and builds receipts. The protocol says reconstruct graph lists only. Reconstruct the same graph sets without historical receipt generation, including the missing confirmation set.

4. **Non-blocking improvements:** None.

5. **Minimum required repair and verification.** Reconstruct the original/base, coverage, confirmation and own-stream exclusion graph lists with original seeds/order, without old rollouts, and keep the1271/disjointness checks. Then rerun `python3 -m unittest discover -s tests/adaptation-neutrality -v` and the single authorized `python3 -m experiments.adaptation.evidence_neutrality --output refine-logs/20261014-evidence-neutrality/reviewer-smoke --rules 4 --streams 1 --timeout 120`. No source/checkpoint fixes were made by this reviewer.

The remaining static paths match the stated diagnostic: all k0 cases enter raw/state/fact/dedup; repetitions use only source-failure-eligible cases; first query action sees no query outcome; source stops early and is not a completed task stream. State and fact controls share histories and progress masks. Exact factual inference retains the true parent set; duplicate failures add no support restriction under the declared deterministic channel. Neural computation can nevertheless change, so an action change alone is not harmful transfer. Initial history is at most12 and query adds at most12. Incomplete queries cost12, actual commands are separate, and branch accounting includes one reset. Pair keys include checkpoint/case; rule-cluster bootstrap resamples conditional-ratio numerators and denominators together. The three frozen checkpoints remain a fixed conditioning set.

Smoke was **not run** because its prerequisite fails. Actual smoke branches:0; state-only versus fact comparison denominator/effects: unavailable. No main grid, training, GPU, installs or network work was run. The focused cohort reproduction itself exposed F2; it performed no learned-controller rollout.

Requested reviewer: `gpt-6-astra`, reasoning `ultra`, via adapted collaboration. Visible actual identity: Codex agent described as GPT-6-based; exact backend/configuration is not independently exposed. This fresh review is same-family provisional and does not certify cross-model independence. Git metadata is unavailable; review covers the explicit current-file manifest.

All eight requested files were read and their SHA256 values match `ops/prelaunch-source.json` at review time:

| Source | Actual SHA256 |
|---|---|
| `experiments/adaptation/evidence_neutrality.py` | `a5ca54a4b2b2734b741d1fdd543c50dbd656df7f673025617554a95e9e36b820` |
| `experiments/adaptation/model.py` | `c4958075471d2eccc6b43c8808e2044e9eaec3e3f6a1cd6bfa0ab3c893f84861` |
| `experiments/adaptation/task.py` | `6b584444089035d7c9a579fdbe7441fb50d88d87300e7bd41f22ebc3b6b93eea` |
| `experiments/adaptation/task_stream.py` | `884c7472c69676b245d7d3a86c9f74fff27d0d7a4d8f4f71433bd2529d140a5d` |
| `experiments/adaptation/train_query_prefix.py` | `3e911133c17544632ffc2a3a3a7795725ec0fb5603e3125da48cb72cb5db27d4` |
| `experiments/adaptation/run_pilot.py` | `9c735139e8db01fd5c5e72d52f30468755a7a482d7a2d9119894ab56307ba2c0` |
| `tests/adaptation-neutrality/test_evidence_neutrality.py` | `d183741ad445a2a18b89aa62ac5075241f6c41f0d3d51f3313cc11633d85caa8` |
| `refine-logs/20261014-evidence-neutrality/PROTOCOL.md` | `6b83e1462ddb362a8b7643d6eb103413394044e5ac329f1da6ac788f34cf232c` |

Immutable anchor read: `refine-logs/20261014-evidence-neutrality/PROBLEM_ANCHOR.md`; SHA256 `cd77951380d6505570f924927ec590ffdf255163b75c265a21551e1f5b23b832`.

The machine-readable record includes command outcomes, hashes, scope limits, and evidence paths. No new algorithm, joint-Bayes planner, SOTA replication, robotic result, or pristine final-test claim is accepted by this review.
