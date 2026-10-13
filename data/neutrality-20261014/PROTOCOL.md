# B1: factual-knowledge and information-neutral feedback diagnosis

Status: prelaunch; 2026-10-14. This is a baseline diagnostic, not an efficacy pilot for C15/C21/C12 or a claimed new algorithm. Original anchor stays in PROBLEM_ANCHOR.md.

## Actual available evidence

Prior own-stream CSVs contain aggregate command/action outcomes, not complete21-component receipts, so they cannot identify response-sufficiency or reproduce per-event belief transitions. Existing best-covered frozen GRU checkpoints11/29/47 remain available. They are project toy controllers, not replications of RAD/DICP/CML or state-of-the-art robot policies. The deterministic monotone-prerequisite task provides an exact observation model, enabling a narrow invariance/knowledge audit without changing it to create a new-method win.

## Fixed domain and information boundary

Five visible completion bits; unknown fixed DAG prerequisites; a successful command completes one bit, an unmet prerequisite blocks it without changing state. A completed command is also blocked. Goal subset, executed command, before/after state and success marker are public. No latent graph, eligibility vector, true failure cause or queried-goal outcome enters the model or guards. Parameters freeze throughout. All statements about neutral repetition require this deterministic, stationary, fully observed consequence channel; real stochastic failures can be informative.

For a non-completed command a that failed at visible state S, executing it again at the identical S yields the same observation and no new constraint on any compatible model. Under this channel, likelihood L_M(e) is0/1; repeating it leaves every compatible-model posterior unchanged. A known failed command at a state T⊆S is also ineligible under monotone prerequisites. This is standard action-model inference, not a new theorem.

## Fresh cohort locked before rollout

Generate128closure-unique rules and4source/query goal pairs per rule with seed814014. Exclude the1,015historical original/coverage/confirmation closure classes plus the256previous own-stream classes (1,271total). Reconstruct graph lists only, not old rollouts. Fail if counts or disjointness disagree. Goal pairs are distinct nonempty masks, sampled before any controller action, independently of the rule. Use the same cohort across3fixed checkpoints.

For each pair, execute up to4commands using the raw frozen policy toward the assigned source goal. Stop source collection at its first nontrivial blocked command, source-goal completion, STOP or4commands. Record all receipts. This deliberately short diagnostic source is not a completed required-task stream. All512pairs per checkpoint enter the zero-padding query comparison; no outcome-dependent task rejection.

A pair whose source ends at a nontrivial failure is eligible for the separate repetition comparison. Add k∈{0,1,4,8} actually simulated retries of that same command before resetting physical state to zero. Every retry is counted and its factual receipt checked against the source failure. The eligibility subset is explicitly conditioned on an observed failure; it is not a full-population transfer estimate. Source prefix≤4 and repeats≤8 gives initial history≤12; query budget12 gives total history≤24, within the existing evaluation envelope. No history truncation is introduced.

## Established controls, not new methods

- raw: original frozen policy on complete factual history.
- state_guard: same history, mask already-completed commands and premature STOP using only visible state and goal.
- fact_guard: state_guard plus exact finite per-action version space. Initialize16possible parent subsets per action, remove subsets contradicted by public non-completed-command successes/failures, and mask commands impossible under every remaining subset. This ignores DAG-induced cross-action correlations and is not full joint Bayes or a Bayes-adaptive planner. It never needs the true graph. It is a cheap standard inference/harness control.
- dedup: original policy, remove exact duplicate non-completed failure receipts from its input view; retain actual trials and all facts in logs. An informative negative is possible: fixed-input greedy policies may rely on repeated uninformative trials as a computational clock and can get stuck when duplicates are removed. Do not assume dedup is a repair.

Query target remains unexecuted before its first decision. Reset once between source and query; every query starts from zero. Each arm then executes its own causal12-command rollout. Histories may diverge, so later comparison is a whole-policy intervention. First-query padding sensitivity is a matched-evidence readout comparison; keep the interpretations separate.

## Endpoints and analysis

Primary audit: raw-query commands that the factual version space already entails impossible; repeated identical blocked states/actions; premature STOP; completed-action retries. A known-impossible repeated action has neither state/reward nor new information under the declared model, regardless of a joint prior. Neural computation may still change on the token, so output sensitivity alone is not harmful transfer.

Primary control comparison on ALLzero-padding pairs: fact_guard vs state_guard query completion and capped query-command cost. This isolates relation knowledge from basic visible progress masks. Also show raw vs state_guard. Incomplete queries are charged12 even after premature STOP. Report actual commands separately.

Separate failure-conditioned repetition comparison: k1/4/8 vs k0 first-action changes, subsequent completion/capped query costs, and actual source+k+query+one reset accounting. No presumption that changed output is an error. Dedup first-decision equality across k is an implementation invariant, not an efficacy result.

Average/checkpointstreampairedstatistics within independent rule. Use4,000rule-cluster bootstraps, seed814117; report intervals conditional on these3checkpoints, per-checkpoint effects and denominators. Ratios on selected cases bootstrap their numerator and denominator together. Keep allplannedrepeatbudgets, not best-of4.

## Decision gates and compute

No binary publication/readiness threshold. If fact_guard yields a practical advantage beyond state_guard and raw issues known-impossible commands, there is an actual learned-controller knowledge-use defect; do not infer a novel method. If a cheap guard closes it, C15/C21 memory machinery is not necessary for that defect. If negligible, do not add redundant tests to manufacture a result. A repetition effect without harmful cost or with improved query performance is computation-vs-information evidence, not a posterior-corruption proof.

One CPU science process,2Torchthreads,≤30minutes; no environment changes, GPU/cloud, newtraining or robot episodes. GPUavailability rechecked once (driver/library mismatch). Reuse existingCPUenv after finite frozen-forward witness. Fresh same-family ARIS protocol/code review plus finite truth-table and smoke invariants before main. Do not rerun a completed grid to chase sign. Final result must classify whether it advances an algorithm claim or rules out unnecessary complexity.
