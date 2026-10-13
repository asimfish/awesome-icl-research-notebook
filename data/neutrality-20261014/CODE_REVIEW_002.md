# B1 protocol/code re-review — PASS

1. **Verdict: PASS for the scoped B1 protocol/code gate.** Both verified cohort defects are repaired. The independent six-test run and the single authorized bounded smoke pass. This remains a same-family provisional review; it does not accept a new-method efficacy or novelty claim.

2. **Dimensions.**
- Functional achievement: **Pass**. The public CLI completed all four modes and all planned padding budgets on all three frozen checkpoints.
- Correctness/reliability: **Pass**. Six tests pass; saved receipts/events independently reproduce causal factual flags, costs, paired denominators and dedup first-decision equality.
- Architecture/API/maintainability: **Pass within scope**. The repair directly reconstructs the required graph sets; model and guard inputs remain public. No additional machinery is necessary.
- Performance: **Pass for the bounded smoke**. CPU,2Torchthreads,1.488s under the120s cap. The full main-grid runtime is not measured by this review.

3. **Blocking findings:** None remaining.
- **F1 resolved:** `experiments/adaptation/evidence_neutrality.py:76` reconstructs original1012, coverage2712, confirmation4812 and own-stream6412 graph draws, preserving759/1015/1271 closure checks.
- **F2 resolved:** reconstruction uses graph/closure functions only. The added regression test at `tests/adaptation-neutrality/test_evidence_neutrality.py:9` forbids historical receipt-generation paths and checks exclusions, new-class disjointness and distinct source/query goals.

4. **Non-blocking improvements:** None.

5. **Minimum required repair:** None for this gate. The original `CODE_REVIEW.md` and `CODE_REVIEW.json` remain unchanged as the first-round BLOCKED record.

Independent command evidence:

- `python3 -m unittest discover -s tests/adaptation-neutrality -v`: exit0;6 tests,0 failures/errors;0.142s.
- `python3 -m experiments.adaptation.evidence_neutrality --output refine-logs/20261014-evidence-neutrality/reviewer-smoke --rules 4 --streams 1 --timeout 120`: exit0;1.487987s;CPU2threads; no training.
- Read-only audit of saved artifacts: pass; record in `reviewer-smoke/reviewer-invariants.json`. No model/simulator rollout was repeated during this audit.

Smoke accounting:

| Quantity | Actual |
|---|---:|
| Source histories / eligible histories |12 /9|
| Query branches / recorded query commands |156 /970|
| Source transitions / padding retries |15 /117|
| Per-branch reset charges |156|
| All-case paired denominator |12|
| Repetition paired denominator for each k=1,4,8 |9|
| Maximum initial / final / model-input receipts |9 /21 /20|
| Forward batches / decisions |480 /985|

The zero-padding state-only and factual controls each complete12/12 queries and use61 total capped query commands, so the observed incremental factual-control effect in this smoke is zero. Raw completes12/12 with65 commands; dedup completes11/12 with65 capped commands. These counts document execution and denominators only. They do not establish a science result. All planned repetition outcomes are retained in `reviewer-smoke/result.json`; repetition intervals explicitly report11 zero-denominator bootstrap draws.

The reviewed information boundary is correct: the model sees factual receipts, visible state and goal; factual guards infer independent per-action parent supports from those same receipts. The hidden graph serves the simulator/cohort construction and never supplies eligibility, true failure causes, oracle action labels or query outcomes to the live policy or guards. Sixteen parent subsets per action form exact independent supports under the observation model; omitted DAG correlations prevent calling this joint Bayes.

All zero-padding pairs enter the four modes. Positive padding selects only observed noncompleted-command failures, with the same eligible k0 cases used for matched comparisons. Sources stop at their first nontrivial failure, goal completion, STOP or four commands; this is deliberately short source collection, not completed required-task streaming. Each query starts at zero and gets no query feedback before its first decision. State and fact controls share full initial histories and basic progress masks; fact adds only public-evidence impossibility masks. Later branch trajectories may diverge, so their outcomes compare whole policies.

Information neutrality is restricted to deterministic, stationary, fully observed monotone consequences. Repeating an identical blocked command adds no model constraint, but tokens can still affect neural computation. Output sensitivity alone does not prove harmful transfer; dedup equality is an implementation invariant, not a promised repair. These established guard controls cannot establish algorithm novelty.

The declared history bound is valid: source<=4 plus retries<=8 gives initial<=12; query<=12 gives final<=24, without truncation. Incomplete queries cost12 even after STOP, actual commands remain separate, and each branch charges source+k+query+one reset. Simulator counters count shared source/padding preparation once; per-branch charges describe separate interventions and do not claim free deployment branching. Checkpoint/case keys preserve pairs. The4000-resample rule bootstrap resamples selected-case numerators and denominators jointly and conditions on checkpoints11/29/47. Frozen state dictionaries and checkpoint files pass the existing runtime equality checks.

Scope and reviewer identity: the requested reviewer was `gpt-6-astra` with `ultra` reasoning via adapted collaboration. Visible identity is a Codex agent described as GPT-6-based; exact backend/configuration is not independently exposed. The same delegated reviewer continued round two. The applicable research-review skill was read at `/tmp/aris-icl-source/skills/research-review/SKILL.md`, including its restrictions against speculative security/compatibility machinery and invented findings. No cross-family certificate is asserted.

No main grid, training, GPU, install, network or credential operation was performed. The four rules are development checks from the main-seed graph prefix; this smoke invocation draws its goals after four graph draws, and is not pristine final-test evidence. Do not change the method/hypothesis by its outcome sign. Full128-rule4-stream runtime and scientific conclusions remain unobserved here.

All eight requested sources were read across the two-round review; unchanged files retain their first-round review and matching hashes. Updated hashes were verified again after smoke:

| Source | Actual SHA256 |
|---|---|
| `experiments/adaptation/evidence_neutrality.py` | `92a64933add1c7e18f1611d4f7a50b3f48a10991ddf3aafaa73baa0f87543521` |
| `experiments/adaptation/model.py` | `c4958075471d2eccc6b43c8808e2044e9eaec3e3f6a1cd6bfa0ab3c893f84861` |
| `experiments/adaptation/task.py` | `6b584444089035d7c9a579fdbe7441fb50d88d87300e7bd41f22ebc3b6b93eea` |
| `experiments/adaptation/task_stream.py` | `884c7472c69676b245d7d3a86c9f74fff27d0d7a4d8f4f71433bd2529d140a5d` |
| `experiments/adaptation/train_query_prefix.py` | `3e911133c17544632ffc2a3a3a7795725ec0fb5603e3125da48cb72cb5db27d4` |
| `experiments/adaptation/run_pilot.py` | `9c735139e8db01fd5c5e72d52f30468755a7a482d7a2d9119894ab56307ba2c0` |
| `tests/adaptation-neutrality/test_evidence_neutrality.py` | `2dc812a54c4e0a88009d9b2ceca467ea2e020692c71e4783d1f15f42efe7fe0a` |
| `refine-logs/20261014-evidence-neutrality/PROTOCOL.md` | `6b83e1462ddb362a8b7643d6eb103413394044e5ac329f1da6ac788f34cf232c` |

Immutable anchor: `refine-logs/20261014-evidence-neutrality/PROBLEM_ANCHOR.md`; SHA256 `cd77951380d6505570f924927ec590ffdf255163b75c265a21551e1f5b23b832`. Git metadata is unavailable, so review is restricted to the explicit file manifest.
