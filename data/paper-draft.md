# When Does Interaction History Help a New Goal? Separating Evidence Use from Control Coverage

Working paper, 12 October 2026. Status: experimental study in progress, not a submission-ready methods paper. Fifteen main checkpoints have been trained and evaluated; the primary support-completion criterion remains unmet. No evidence from earlier symbolic arithmetic probes is counted as learned-policy performance.

## Abstract

A successful task recovery does not establish that its experience improves later goals. We study historical-support use under physical reset using a controlled dependency-operation simulator and frozen history-conditioned policies. Nine common-history checkpoints first compare continuation, same-goal reset and changed-goal reset supervision. Reset-trained policies use support to improve their first decisions, yet their closed-loop completion is poor because training never covers progressing query states. A public-state action mask diagnoses repeated completed commands but does not produce a positive support-completion effect. Six further checkpoints hold histories and goals identical while changing only the supervised query-state arrangement. Ordinary query supervision at legal progressing states reaches 98.18% changed-goal completion with support and 97.79% without; the 0.39-point support difference has a rule-bootstrap 95% interval spanning zero. Support nevertheless reduces capped command cost by 1.020 commands per query. A prospectively declared evaluation of the same frozen policies on 256 fresh closure-disjoint rules confirms savings of 1.011 commands, with a conditional rule-bootstrap 95% interval of [0.922, 1.097]. The primary historical-support completion hypothesis fails, while evidence use appears in first decisions and conditional execution efficiency. These exploratory symbolic results identify a control-coverage confound and an established-method remedy, not a new algorithm, autonomous acquisition benefit or robot result.

## 1. Introduction

The motivating system is an agentic real–sim–real loop: an agent gathers attempts, a verifier records outcomes and recovery, a learner absorbs that experience, and deployment generates the next round of feedback. Its scientific question is not whether DP, offline RL, online RL and distillation can be connected. It is which information survives that loop as behavior in the eventual student. Verification can certify that an attempted recovery worked, but this does not certify that the student learned the underlying task relation or can reuse it for a new goal.

Consider a robot that discovers that an access operation is required before retrieving an item. It may complete the present task by following a corrective action. On the next task, with the scene reset and a different requested item, it must decide whether that interaction bears on the new goal. Three abilities are easily conflated: executing a correction now; repeating a known goal from a fresh state; and reusing relevant information for another goal. The last requires a behavioral test after reset, not a memory visualization or another successful continuation. This example motivates the study; the present pilot uses abstract operations and does not simulate access, grasping or contact.

The proposed empirical contribution is a controlled comparison of these abilities and their dependence on legal experience. We do not assume that existing methods only recover. DPT already trains decisions from historical interactions; DREAM already considers exploration useful for later goals; robot memory and correction methods are also relevant. The research opportunity is conditional: if common corrective histories carry useful information but a correction-trained consumer fails to exploit it after reset, identify the precise cause and test the simplest established remedy. If established methods already solve the problem, report that result rather than inventing a module.

Two hypotheses guide the experiment. H 1: the supervised query distribution can affect whether a fixed-capacity student uses prior experience after physical reset. H 2: an effective consumer of common experience can eventually motivate an autonomous acquisition strategy whose later task-flow benefit outweighs collection cost. The current experiment addresses H 1 only. A between-supervision performance gap alone is expected under distribution shift and is insufficient as a publishable finding.

## 2. Related work and novelty boundary

**Learning from histories.** RL² and Algorithm Distillation establish learned rapid adaptation through recurrent state or sequence context. [DPT](https://arxiv.org/abs/2306.14892) provides the closest supervision principle: predict optimal actions from interaction data and a query. Our GRU pilot uses this principle but is not an official transformer reproduction. Neither frozen deployment nor action cross-entropy is a new contribution.

**Experience acquisition for later tasks.** [DREAM](https://arxiv.org/abs/2008.02790) and [E-RL²](https://arxiv.org/abs/1803.01118) assign value to exploration through later exploitation. Future-goal adaptation is therefore not an unoccupied problem. A later acquisition experiment must give these methods the same task stream and future objectives; an immediate-reward-only recurrent baseline would be inadequate.

**Robot correction and memory.** [RoboTTT](https://arxiv.org/abs/2607.15275), [Zeva](https://arxiv.org/abs/2608.30880), [PhysMem](https://arxiv.org/abs/2602.20323) and [RoboICL](https://arxiv.org/abs/2609.34261) make correction, self-feedback or contextual robot memory direct neighbors. We do not attribute a general inability to reuse experience to these works. Test-time gradient updates and frozen-weight context computation should be declared separately, with their costs, rather than treated as synonymous.

**Dependencies and writable memory.** MSGI, MTSGI and [PSGI](https://ojs.aaai.org/index.php/AAAI/article/view/20718) already infer subtask structure. [Fast Weight Memory](https://arxiv.org/abs/2011.07831) already supports editable associations and compositional reads. Explicit slots or residual writes cannot provide novelty on their own. Such an implementation is justified only by a measured failure that survives equal-supervision controls.

**Research process.** [IdeaScientist](https://arxiv.org/abs/2610.04074) separates gap finding, structural transfer and proposal writing. We borrow the staged, inspectable ideation process and counterproposal review. We do not train its research agents, reproduce its proposal benchmark, or treat its judge scores as evidence of robot performance. ARIS orchestrates implementation, runtime witnesses and review; it is research tooling, not the deployed robot algorithm.

## 3. Problem formulation

Let an environment have an unknown persistent rule instance \(z\sim p(z)\), observable state \(s\), and goal \(g\). A command produces a legal receipt

\[
e_t=(s_t,a_t,s_{t+1},y_t,g_t),\qquad
(s_{t+1},y_t)\sim P_z(\cdot\mid s_t,a_t).
\]

The support history \(H=(e_1,\ldots,e_L)\) is produced by a behavior policy that can depend only on information available before each command. The student is

\[
m_t=F_\theta(H_t),\qquad a_t\sim\pi_\theta(\cdot\mid s_t,g_t,m_t).
\]

At deployment, \(\theta\) is fixed. History and computed context state may change; no teacher labels, hidden rule description, task ID or optimizer step enter the student. Physical reset changes \(s\), while retained support remains available. An unseen adjacency matrix need not define unseen reachable behavior; our revised experiments therefore separate rule instances by transitive closure within this declared family. This is not evidence of general unseen physical dynamics.

For a common \((z,H,g)\), define paired queries

\[
q_C=(s_H,g),\quad q_S=(s_0,g),\quad q_N=(s_0,g'),\qquad
g'\sim p(g'\mid g),\ g'\ne g.
\]

Here \(p(g'\mid g)\) is independent of \(z\); rejecting equality only uses the visible source goal. The initial support source goal is also sampled independently of \(z\). No oracle success or feasibility filter constructs the query distribution. Our monotone DAG family makes every goal feasible from \(s_0\).

Let \(\mathcal A_z^*(s,g)\) be the set of first actions in minimum-command solutions, with STOP for an already completed query. The training distribution for query arrangement \(v\in\{C,S,N\}\) changes only the query state/goal attached to common support records:

\[
\mathcal L_v(\theta)=
\mathbb E_{z,H,q_v}
\left[-\sum_a u_z(a\mid q_v)\log\pi_\theta(a\mid q_v,H)\right],
\quad u_z=\operatorname{Unif}(\mathcal A_z^*).
\]

The oracle is used for offline labels and evaluation; it never selects the support commands or deployment actions. The label distribution is deliberately tie-aware. Yet query arrangements can change STOP frequency and class difficulty. Equal label count is not equal label informativeness. We must report those differences and perform a targeted follow-up before attributing a gap to representational learning.

Define \(J_v(H)\) as success within a declared action budget for query family \(v\), including the student's subsequent legally obtained query feedback. The paired historical-support benefit is

\[
\Delta_v=\mathbb E[J_v(H)-J_v(\varnothing)].
\]

The empty condition removes initial support, while both branches can learn within the query. Thus \(\Delta_N\) measures the benefit of retained pre-query experience under this rollout protocol; it does not isolate an individual receipt or establish a causal graph representation. First-action optimality separately measures behavior before any new query outcome. Rule recovery would require discriminating legal counterfactual cases and successful simple relation queries before composition.

For the later autonomous task stream, a collector must be evaluated by the entire objective

\[
\mathbb E\left[\sum_{k=1}^K U(g_k,\pi,H_k)
-\lambda_a N_{\rm commands}-\lambda_r N_{\rm resets}
-\lambda_q N_{\rm teacher\ queries}\right],
\]

with all costs also reported separately. A difference of future returns is a measurement or conventional credit signal, not a new learning objective. Collectors and consumers should be crossed to separate evidence quality from consumer compatibility.

## 4. Controlled pilot

There are five abstract operations with a randomly permuted DAG of prerequisites. A command succeeds once if all its parents have completed; otherwise it leaves the observable state unchanged. There is no actuator noise, image ambiguity or learned low-level control. All operations have equal command cost. This intentionally strips away perception and execution to test evidence use; it also removes many reasons the method might fail on robots.

The fixed data seed is 1012. We generate 256 unique training graphs and 128 disjoint evaluation graphs, with 32 training and 8 evaluation histories per graph. Each history has uniformly sampled length 0–12; its entire command sequence is sampled before receipts. The behavior controller is an uninformed random controller, not the trained student. The model therefore consumes legally generated interaction, but this round does not establish useful autonomous acquisition.

All three arrangements share the GRU width 96, head, initializations paired by training seed, common history pool, Adam learning rate 0.001, batch 128 and 600 updates. Seeds are 11/29/47. We use the final checkpoint, not test-selected early stopping. The pilot test is exploratory evidence; any later choice informed by it requires a new development/test protocol. Empty histories are included in training support.

Each checkpoint is evaluated on all three query families with full and initially empty support. Rollouts have at most 12 commands; a premature STOP ends unsuccessfully. Goal completion ends successfully without requiring a separate STOP. Report completion, first-action optimality, command counts, failed commands and premature stops. Already-complete current queries are reported separately. Parameter equality before and after evaluation is checked.

Rule instances, not frames or query branches, are the statistical units. We report each training seed, variation across seeds, and rule-bootstrap intervals conditional on the three trained checkpoints. Paired interventions use identical graph/query cases. They are not independent physical trials. Same-length edgeless-world receipts and other-world histories are stress tests; their altered state/result distributions are not surgical causal interventions on feedback.

## 5. Results and interpretation

### 5.1 Original common-history pilot

All nine final 600-update checkpoints completed. Main evaluations contain 55,296 paired branches over 128 held-out adjacency graphs; the statistical units are graphs, not the number of rollouts. All six reset-trained checkpoints have positive first-action support effects but negative completion support effects. Current-task continuation benefits from support, while reset transfer of the current-trained consumer does not.

| Training arrangement | New-goal completion, full | New-goal completion, empty | First-action support gain |
|---|---|---|---|
| Current correction |42.74%|64.52%|−23.60 points|
| Same-goal reset |13.67%|18.13%|+23.01 points|
| Different-goal reset |13.74%|17.51%|+27.47 points|

The reset head's state-input weights remain bitwise equal to initialization in all six reset checkpoints: state inputs are alwayszero during training, so those columns receivezero gradient. Replays classify 26,360/26,616 completed-operation repeats in the same/different-reset full branches, respectively, across 3,072 cases per family. The current-trained policy instead makeszero completed-operation repeats and stops prematurely in 52.57% of full-support new-goal branches. Its STOP target fraction is 23.91%, versuszero for reset arrangements. These are distinct failure modes.

Masking commands whose public completed-state bit isone raises reset full-support completion to 88.35%/86.78%; corresponding empty-support completion is 92.74%/90.20%. The mask is a known control constraint applied equally to all policies, leaves STOP available, and does not consult hidden prerequisites. It diagnoses generic execution failure without satisfying the support-benefit criterion.

The original split is adjacency-disjoint, not closure-disjoint. An audit findsfour test graphs sharing a transitive closure with training. Restricting to 124 closure-unseen graphs retains all negative new-goal completion-support signs. This post hoc check does not turn the initial test into a new final benchmark. The follow-up corrects the split prospectively.

### 5.2 Matched-history query-state experiment

Following critical review, we run a cleaner two-arm intervention withsix additional final checkpoints. Both arms receive identical initial support and legal fresh-query prefix receipts, sampled using a random controller and public goal completion. Every base case and goal remains; only observed active prefix states are selected. Covered-query attaches the action label at that prefix's actual state; zero-query resets the physical state again and attaches the label at zero, retaining exactly the same history and goal. Thus context length, goal transition, prefix commands, label count, initialization and batch indices match between arms. Label difficulty changes with state. Both pools havezero STOP targets.

Data seed 2712 generates 256 training and 128 test rules, unique and disjoint by transitive closure and excluding all closures used in the original train/test cohorts. This remains an exploratory follow-up after observing the original pilot. Both arms use 600 updates, batch 128, width 96,45,126 parameters and seeds 11/29/47. Primary evaluation uses ordinary unmasked argmax, reset-to-zero new goals and subsequent self-generated query feedback.

| Training arrangement | Full-support completion | Empty-support completion | Paired support gain [rule 95% CI] | First-action support gain |
|---|---|---|---|---|
| Covered query states |98.18%|97.79%|+0.39 points [−0.65,+1.40]|+24.58 points|
| Zero query states |8.04%|9.77%|−1.73 points [−2.70,−0.85]|+31.45 points|

The between-arm change in support benefit is+2.12 points [0.72,3.55]. This does not imply positive support benefit in the covered arm; its interval spanszero and training-seed support effects are+1.27,−0.10 and 0.00 points. The preregistered completion-support criterion therefore remainsFAILED. An ordinary policy with visible state and access to within-query feedback nearly solves this small family without retained pre-query experience. We do not isolate the contribution of within-query feedback from its learned prior or public state.

### 5.3 Predeclared secondary command costs

For the covered-query policy, mean actual commands are 5.315 with support and 6.336 without. Paired savings are 1.020 commands, rule-bootstrap 95% interval [0.890,1.149]; all three training seeds agree. Failed queries use the full 12-command budget and premature STOP is zero, so this is not an artifact of saving commands by aborting. Mean prerequisite-blocked commands decrease from 2.373 to 1.390; completed-operation repeats decrease from 0.074 to 0.046. First-action evidence use and lower capped command costs are the narrower positive findings.

These savings condition on already supplied support. They do not pay for collecting that support. The shared D 2 dataset contains 49,425 initial support commands and 43,780 collected query-prefix commands;21,090 prefix commands enter the retained training histories. These are shared generated records across conditions/seeds, not six independent collections. Each arm has 8,192 annotated query records and each checkpoint sees 76,800 sampled target exposures; many records share the same numeric target distribution. Actual CPU training for the nine original and six revised checkpoints totals 79.390 seconds, excluding process startup, data construction, evaluation and reviewer replay. Main policy branches total 92,160; the separate mask diagnostic adds 36,864 replay branches and no training. Robot episodes and GPU-hours arezero.

We additionally plot the full exploratory completion curve for every command budget 1–12 from the unchanged covered-policy traces. The originally declared primary endpoint remains 12; we do not select a smaller horizon after seeing results and replace the failed primary hypothesis with it. The curve describes where the conditional command savings occur. Task-flow net utility requires a new experiment with all collection/reset/teacher costs, not this curve.

### 5.4 Fresh-cohort confirmation of the cost effect

Before inspecting additional outcomes, we freeze the three covered checkpoints,12-command horizon and paired capped-command question. A new data seed 4812 produces 256 closure-unique rules excluding all 759 closure classes previously used in the original and revised train/test pools. There is no new training, architecture selection or horizon change. The 12,288 paired frozen-policy branches confirm 1.011 commands saved with retained support, rule-bootstrap 95% interval [0.922,1.097]; seed savings are 1.063,0.974 and 0.995. Mean completion is 97.92% with support and 97.57% without. This confirms the narrower conditional-cost result, not the original failed completion criterion or a new method. Mean prior support collection costs 5.890 commands; the measured subsequent-query command saving does not repay the initial-support collection commands. Total main evaluation branches including this cohort are 104,448, with the separate 36,864 mask-diagnostic branches unchanged.

### 5.5 Claims revised by evidence

The pilot establishes a real training-support artifact, successful control under an established query-supervision recipe, first-decision historical-support use, and lower conditional execution cost. It does not establish a need for different-goal relabeling, semantic rule recovery, a new memory mechanism, autonomous evidence acquisition, independent verifier learning, physical robot adaptation or sufficient novelty for a methods paper. Stronger hypotheses are retained as future tests rather than asserted contributions. The dominant next question is whether legally acquired recovery experience produces net task-flow benefit when interactions are expensive and dependencies genuinely change.

## 6. From mechanism evidence to a robot paper

Four evidence blocks remain. First, student-distribution training and task-stream evaluation with full collection/reset/teacher costs. Second, same-future-objective DPT and E-RL²/DREAM baselines, plus appropriate subtask-inference methods; no comparison should deprive a baseline of the future goal. Third, simple versus composed queries, different graph sizes/depths and a second rule family. Fourth, embodied execution with deployment-visible outcome verification and independent success evaluation.

For embodiment, select a small set of reusable operation relations in an existing simulator, then separate changing object poses from changing task dependencies or goal combinations. The verifier's hidden state can determine evaluation success but cannot appear as student feedback unless the deployment sensor genuinely supplies it. Add realistic execution ambiguity only when it exists in the selected task. If commands can fail mechanically, test whether erroneous persistent rule updates occur under the same legal witnesses; do not inject arbitrary noise merely to justify a mixture module.

The agentic data engine, digital-twin calibration and DP/RL/distillation ladder are the larger system context. They should be expanded only when needed to test experience generation, admission or absorption. A method claim must point to one mechanism with decisive equal-information controls, not to the number of components in the system diagram.

## 7. Limitations

This pilot has abstract, fully observed monotone states, small graphs, random support acquisition and one recurrent architecture. It does not establish physical intelligence, safety, sim-to-real transfer, learned verification, autonomous experimentation or general compositional rule learning. The original adjacency holdout admits four shared closure classes; the revised split holds out closures. Neither split establishes generalization beyond the declared family. Final-checkpoint controls do not establish convergence or absence of distribution mismatch. Initial support removal changes context length; stress controls only partially address that concern. LLM reviewers are same-family and provisional; their assessment is not independent replication or scientific acceptance.

## 8. Reproducibility and evidence

Implementation: `experiments/adaptation/`; exact plan and data contract in this cycle directory. Each run preserves config, checkpoint, loss trace, objective composition, command-level episode aggregates and measured compute time. Fresh-agent runtime invocation and implementation review are saved separately. The experiment reuses the installed CPU runtime and does not repair the shared GPU environment. Earlier U3 documents and A3 probes remain archived and are excluded from the result count. IdeaScientist reading, mechanism proposals, reviewer requests and raw responses remain distinct from measured research evidence.
