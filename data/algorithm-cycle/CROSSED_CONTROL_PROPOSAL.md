# Crossed execution controls for reusable correction evidence — full revision

Date: 2026-10-12. Status: proposed second revision of recovery contrast, pre-experiment. No novelty or physical claim. The initial conditional-logistic filter and sequential gate were found to have exact statistical/operational priors; they remain recorded, not renamed as new contributions.

## Problem Anchor, verbatim

机器人能否从自己的纠正经验中学到可复用的任务关系，并把这些关系用于此前没有执行过的新目标？

研究当前纠正、独立重置后的同目标适应与不同目标关系复用。测试参数冻结、教师退出；学生只见部署可得观测、命令及后果。未来目标监督、配对收益与任务图推断均有前作，不预先承诺新算法。

本轮先导是学得策略的受控机制实验，不是具身验证。通过真实反向传播训练历史条件模型，检查未知关系实例上的经验利用；正面或负面结果都写入论文。随后才开展自主采集、E-RL²/DREAM、物理控制与第二任务族。

旧A3退出主线；U3冻结方案、正式query0与历史材料保持。用户已授权实验编排、验证与迭代。先使用现有本地CPU，不修复共享GPU驱动，不购买云算力或执行真机动作。

## One dominant thesis

Successful corrections should supervise a reusable relation only after removing the part of their improvement shared with a task-inert execution control. The candidate operation is a crossed-control replay protocol and the resulting scoped relation context. The conditional likelihood used to read the controls is established mathematics; there is no claim to invent conditional logistic regression, negative controls, or sequential testing.

## Why the first filter is insufficient

Two target-option outcomes at x and prepared x′ have logits L0 and L1. With unknown preparation-induced motor change μ, their difference is θ+μ. The worlds (θ=d,μ=0) and (θ=0,μ=d) have identical target-only distributions, including arbitrarily many independent repetitions. A target-only filter or larger history encoder cannot identify this decomposition from those records without structural assumptions. Recovery validation can improve behavior in both worlds but only the first world supports the intended task-relational interpretation.

The four-corner protocol adds an actual task-inert control c, executed under the same two prescribed states and matched execution regime. It does not create an oracle label saying a is eligible. The new observation is a negative-control outcome, and every comparator has the same access and cost.

## Contract and full model

Precommit a source-visited state pair (x,x′), target option a, control c, and four execution innovations before their outcomes. Each option execution starts from a restored snapshot, so one outcome cannot change a later state. The original pair's source outcomes can propose the contrast; they are not reused as fresh evidence after proposal selection.

Conditional on quadruple i, independent Bernoulli outcomes have logits:

L_a0=η_i+u_ai;
L_a1=η_i+u_ai+μ_i+θ;
L_c0=η_i+u_ci;
L_c1=η_i+u_ci+μ_i.

η_i, the option-specific intercepts u_ai,u_ci, and the preparation motor shift μ_i may vary arbitrarily between quadruples. The control is task-inert for this registered relation; the motor preparation shift is the SAME additive log-odds shift for target and control. This is a parallel-response/exclusion restriction. It is not identified by the four binary labels, nor guaranteed merely by calling c a calibration action. A control affected by θ or a differential motor shift leaves confounding. Even a shared multiplicative physical success factor can produce option-specific LOGIT shifts: if p_jk=r_j*m_k, the motor logit difference depends on r_j. Shared perturbation labels alone therefore do not enforce the required model. A prelaunch sensitivity control fixes r_a=.9,r_c=.4,m0=.4,m1=.8 with unchanged task efficacy and exposes this failure. No imaginary task-null simulator that makes a physically impossible option executable is allowed.

The initial CPU study deliberately enforces this model as a diagnostic; a physical implementation would need a credible measured control family (e.g., an available calibration interaction sharing the relevant execution condition). If no such family can be realized, the route stops. Shared-uniform simulator noise does not yield the likelihood below; use independent innovations conditional on the quadruple nuisances. The earlier direction-only e-process could handle shared randomness, but would not identify θ versus μ.

## Conditional readout

Condition on every option having one success over its two executions and every state column having one success over its two options. There are exactly two possible patterns:

A: (Ya0,Ya1,Yc0,Yc1)=(0,1,1,0);
B: (Ya0,Ya1,Yc0,Yc1)=(1,0,0,1).

Their probability ratio is exp(La1+Lc0−La0−Lc1)=exp(θ). Thus P(A|A or B)=sigmoid(θ), regardless of η,u_a,u_c,μ and their common mixing distribution. This is a classical conditional likelihood in a crossed binary-response design. A full inclusion-odds offset is required if the two patterns have different retention probabilities. The first diagnostic collects all four corners and retains all patterns, so the offset is zero; filtering only improved recoveries would invalidate it.

Only A/B records update this conditional relation belief. Every noninformative pattern, failed control/preparation, and reset still counts toward acquisition cost. A shared motor shift cancels, while task effect contamination in the control κ or a differential motor shift δ yields θ−κ+δ. These violations must appear as explicit negative controls in the numerical experiment.

## Executable first belief and use

A finite-grid posterior over θ for a registered local preparation/target/context triple starts from the same documented prior for all methods. On A or B, multiply by its conditional likelihood; no deployed network parameter update is required. Target-only inference is an ablation; the exact ordinary crossed conditional filter is a mandatory reference because it is the same readout, not a method to claim superiority over.

The candidate algorithmic contribution, if any, must therefore be producing affordable admissible controls and enforcing the scope of the learned effect in a new-goal consumer. The filter itself is not the contribution. If the intended reuse is under an unchanged execution regime, calibrated total preparation effects may suffice without separating θ; the motivating advantage requires an independently specified motor shift between acquisition and deployment while task relations persist. A first controlled use has two equal-cost prepared alternatives for a target option in an unchanged local context, for a macro-goal not assigned during acquisition. Use posterior evidence to select between them only when the comparison supports the selected alternative AND their deployment motor preparation effects are equal, or calibrated through public execution controls with those costs charged; otherwise use the existing consumer. Equal preparation cost alone is insufficient: target success depends on θ_b+μ_b, not θ_b. The first controlled policy diagnostic would enforce μ_b=0 for both alternatives at use time and disclose that restriction; a physical system would need measured/bounded differential motor effects or abstention. Equal preparation cost removes only the command-cost difference, not motor-effect confounding. A future unequal-cost planner needs absolute success calibration and an explicit expected-cost model; those are not identified by the contrast.

Reusing an effect for the SAME local option/context while changing the macro-goal is a legitimate limited transfer target. Reusing it for unseen geometry, control implementation, object binding, or motor regime is a separate transport claim. The procedure identifies an extra success-odds effect relative to the control, not a necessary-prerequisite edge.

## Optional amortization — gated, not implemented

If controls give useful transfer at matched total cost, train one history adapter to predict the scoped effect belief from the student's own public receipts. Teacher posterior targets come from the crossed audits, not simulator relation labels. The teacher may use additional controlled replay data at training; deploy uses no control oracle or audit labels absent from its history. Predict the teacher's distribution rather than a single forced edge, evaluate leave-task-out relation instances, and include uncertainty preservation. This is a candidate training recipe; generic amortized posterior distillation is also established. No encoder is added before the control/data contribution is shown.

## Strong references and novelty gate

Must compare: target-only paired inference; direct joint success modeling with explicit option/state nuisances on the SAME quadruples; the ordinary crossed conditional model; retained raw-history consumer on the same audit records; and recovery-validation behavior supervision. A nuisance-informed full likelihood is an information ceiling when it sees actual nuisance values; matched-information nuisance estimates are the practical baseline. Universal superiority to an oracle full likelihood is not required.

Primary-source audit must check robot negative-control probes, difference-in-differences/control-action causal representation, crossed/Rasch conditional likelihood, and correction-to-context distillation. MAGMA-GEN already provides replay and validated recovery SFT; PSGI already provides task relation reuse with observed eligibility; PACE already provides paired evidence admission. Those operations are occupied. The possibly useful remaining operation is motor-matched, task-inert replay evidence that teaches a scoped relation belief under withheld eligibility. No claim of first implementation without an exact audit.

## Three-block validation

X0, exact model: enumerate all 16 outcomes across θ∈{−2,0,2}, μ∈{−2,0,2},η∈{−2,0,2}, option offsets±.7. Check crossed identity, arbitrary nuisance mixtures, target-only θ/μ alias, known selection offset, and control contamination/differential motor shift. Report informative-pattern rate and Fisher information per 4 EXECUTIONS, not per retained record alone. Fresh code review first.

X1, only after operational review: same-budget effect-belief learning from synthesized actual own-state controls, with unseen motor-shift distribution and ordinary crossed/direct joint-model references. Fixed priors and audit/control costs; no claim of physical realism or posterior fit as a new-goal result.

X2, only if affordable control acquisition survives: own required-task streams, precommitted new macro-goals, frozen consumer/weights, scoped equal-cost preparation selection, matched raw data and all reset/control/calibration costs. Then physical control validity, a second task family, and amortized adapter training. The deterministic five-operation family is almost solved; no extra module on it without a noise/ambiguity necessity result.

## Refutation and limits

Reject as principal algorithm if controls cannot share the required motor shift, pattern rarity makes control acquisition cost exceed reuse gain, ordinary full nuisance modeling on the same data suffices, or the scope-aware new-goal interface does not improve behavior. Do not reinterpret rejected transport or confounded effects as a discovered task graph.
