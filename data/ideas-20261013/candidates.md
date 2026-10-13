# Complete 40-candidate pool

Adapted ARIS + IdeaScientist generation. Local paper IDs; no novelty or efficacy certification. All candidates retained before semantic triage.


# Relation and interface candidates C1–C10

Bare numeric citations [1]–[15] are local paper-registry IDs, not Svalbard Idea Vault IDs. Sources below are results-masked digests. These are retained candidate mechanisms, including likely established operations; no novelty verdict, acceptance claim, or new failure evidence is implied. New search hits appear only as URLs in the annotation sidecar. Deployment changes numerical/discrete memory while neural parameters remain frozen.

### C1 — Marginalize the cause before updating the relation

- **Intuition**: Interpret a failed command through competing explanations for missing prerequisites, execution slips, and unreliable sensing. Update a reusable relation only by the part of the consequence likelihood that remains informative after accounting for those nuisance explanations.
- **Gap it attacks**: G1 — Interpreting an ambiguous own consequence as evidence about a reusable relation; an execution slip should not become a prerequisite that contaminates another goal.
- **Source inspiration**: CML weights persistent hypotheses by target likelihood [3]; OHCAM separates attempted-action precondition evidence from successful-execution effect evidence [5]. Transfer type: reinforcing-a-weak-connection.
- **How it maps to this problem**: A composition hypothesis becomes a proposed relation together with a possible physical failure cause. The observed consequence, rather than a supplied success or eligibility label, supplies their shared evidence.
- **Why it could work / feasibility**: Likelihood comparison can preserve multiple explanations when the available observation does not distinguish them [3]. This transfer requires an independently defensible consequence likelihood for each failure mode; Bayesian bookkeeping cannot create that information.
- **Novelty vs. closest in-domain work**: OHCAM's digested update uses supplied symbolic/success channels [5]; the proposed change integrates uncertain failure channels, but latent-cause Bayesian inference is established and the algorithmic delta is thin.
- **Main risk**: An incorrectly calibrated execution-noise model explains away real prerequisites and makes shared evidence misleading.

### C2 — Separate a shared disturbance from a persistent rule change

- **Intuition**: Maintain competing temporal explanations for several surprising commands: a short shared disturbance or a lasting change in an action relation. Let their subsequent observed consequences decide whether old relational evidence remains usable.
- **Gap it attacks**: G1 — Ambiguous consequences can be attributed to changed prerequisites when a common sensing or execution problem actually affected several commands.
- **Source inspiration**: BOCPD retains likelihood-weighted growth/reset branches instead of declaring every surprise a change [12]; CML preserves joint hypothesis ancestry [3]. Transfer type: recombination-of-distant-concepts.
- **How it maps to this problem**: Run hypotheses describe persistent relation regimes, while a separate transient cause can jointly explain contemporaneous command failures. Both explanations compete using the same own-stream consequences.
- **Why it could work / feasibility**: BOCPD supports alternative change locations when hazard and predictive families are specified [12]. Cross-command observations could distinguish a disturbance from an action-specific change only if these explanations predict different accessible outcomes.
- **Novelty vs. closest in-domain work**: OHCAM penalizes mismatches within action hypotheses [5]; adding coupled temporal failure causes changes the inference interface, while robust and multivariate change detection are known operations rather than claimed inventions.
- **Main risk**: Sparse commands make a lasting change and a long disturbance observationally indistinguishable.

### C3 — Compile ambiguous corrections into joint constraints

- **Intuition**: Store a correction as a constraint on combinations of relation explanations, rather than as separate confidence penalties. Answer a new goal by checking whether its required relations have a single explanation consistent with all retained constraints.
- **Gap it attacks**: G2 — Preserving dependencies among reusable relation explanations; individually plausible prerequisites can form an impossible conjunction.
- **Source inspiration**: OHCAM expands and searches condition hypotheses [5]; CML's particles keep jointly consistent identities and ancestry [3]. Transfer type: reinforcing-a-weak-connection.
- **How it maps to this problem**: Competing explanations for one failed command become alternatives in an evidence constraint. Subsequent observations narrow the permitted combinations without discarding the original ambiguity.
- **Why it could work / feasibility**: A finite relation vocabulary permits a compact constraint representation in small controlled domains. The source contrast motivates preserving combinations, but neither digest establishes scalable constraint compilation for noisy own consequences.
- **Novelty vs. closest in-domain work**: OHCAM factorizes action/effect hypothesis pools [5]; joint logical action-model version spaces are established, so the possible delta is a noisy, incrementally maintained consequence interface and must be compared to that prior.
- **Main risk**: An incorrect hard constraint eliminates the true explanation permanently; soft alternatives can instead become computationally large.

### C4 — Score a whole plan within each surviving explanation

- **Intuition**: Evaluate every proposed plan separately under each complete explanation of the correction history, then aggregate those complete-plan outcomes. Prevent a planner from assembling one action's optimistic explanation with another action's incompatible explanation.
- **Gap it attacks**: G2 — A new composed goal can appear feasible under relation marginals even though no surviving joint model supports the full plan.
- **Source inspiration**: CML preserves full composition particles [3]; DICP ranks sampled action-and-consequence futures [2]. Transfer type: reinforcing-a-weak-connection.
- **How it maps to this problem**: A persistent particle supplies one relation model for every step of a candidate plan. Planning branches retain that model identity instead of drawing each action's prerequisite and effect independently.
- **Why it could work / feasibility**: Both joint hypotheses and sampled-future search exist in the digests [3, 2]. Their combination is feasible for finite models if the own-consequence likelihood is available and particles adequately cover the plausible explanations.
- **Novelty vs. closest in-domain work**: MTSGI geometrically mixes graph-policy outputs [10]; the change scores complete plans under common models, but ordinary Bayesian or robust planning already performs this operation and is a required direct prior.
- **Main risk**: Poor particle coverage produces confidently coherent plans under the wrong model.

### C5 — Discover relation variables through valid local substitutions

- **Intuition**: Use locally valid substitutions of recorded object transitions to identify which observed distinctions a command's consequences actually depend on. Promote distinctions that survive those substitutions into candidate relation variables.
- **Gap it attacks**: G3 — Choosing and grounding relation variables without eligibility or predicate labels; appearance features can encode a demonstration context without encoding applicability.
- **Source inspiration**: CoDA recombines a transition component with its causes and effects only inside a region where the dependency graph remains valid [11]. OHCAM's supplied predicate boundary supplies the target bottleneck [5]. Transfer type: recombination-of-distant-concepts.
- **How it maps to this problem**: Frozen observable object features supply candidate distinctions; locally independent recorded components supply constrained substitutions. Consequence-predictive invariance is used to choose variables, rather than treating augmented outcomes as additional real corrections.
- **Why it could work / feasibility**: Local causal independence supports valid component recombination [11]. This requires a reliable observable object decomposition and independently checked local masks; it cannot infer arbitrary hidden predicates from free synthetic evidence.
- **Novelty vs. closest in-domain work**: OHCAM starts with grounded predicates [5]; the proposed operation selects their observable inputs, but CoDA already owns causal recombination and causal invariant representation learning is a strong prior.
- **Main risk**: Contact or consumed resources invalidate the local mask, causing the learner to declare a real prerequisite irrelevant.

### C6 — Split the interface when its decision operators disagree

- **Intuition**: Keep two histories in the same relation-interface state only while they predict the same command consequences for the relevant planning tests. Split an interface state when a real correction exposes a decision-relevant difference.
- **Gap it attacks**: G3 — Consequence learning needs to determine which variables distinguish relation states, rather than merely predicting observations through an unspecified abstraction.
- **Source inspiration**: Value equivalence compares Bellman updates over selected policies and value functions, and requires a sufficient closed test space [13]. Transfer type: recombination-of-distant-concepts.
- **How it maps to this problem**: Relation applicability and consequence queries supply planning tests. A correction supplies evidence that a merged class no longer agrees on one of those tests; the interface gains a discrete distinction supported by available observations/history.
- **Why it could work / feasibility**: Decision-relative equivalence can avoid reconstructing irrelevant sensor details [13]. It works only if the selected tests cover later goals and data distinguish disagreement from observation noise.
- **Novelty vs. closest in-domain work**: PACTS learns supplied predicate channels [6]; selecting distinctions from planning-operator disagreement changes their construction, but bisimulation, abstraction refinement, and value-equivalent representation learning are established.
- **Main risk**: A limited test family merges states that agree now but require different commands for a later goal.

### C7 — Turn successor-occupancy contrasts into interface coordinates

- **Intuition**: Compare the future observable consequences reachable from apparently similar histories under the same frozen skills. Use persistent differences in those consequence occupancies to propose reusable state distinctions, even when the immediate appearance and next command agree.
- **Gap it attacks**: G3 — A relation interface can miss an enabling or consumed resource that changes future reachability without changing the present image.
- **Source inspiration**: Successor features separate policy-induced future feature occupancy from goal reward weights and obey a Bellman update [14]. Transfer type: reinforcing-a-weak-connection.
- **How it maps to this problem**: Observable consequence features replace supplied logical fluents. Contrasting successor predictions supplies candidate interface coordinates; a correction revises numerical occupancy estimates before those coordinates inform another goal.
- **Why it could work / feasibility**: Future occupancies can encode differences invisible to a one-step predictor [14]. The frozen feature encoder must expose the relevant consequence, and the fixed skill set must reach it; occupancy differences are not automatically interpretable predicates.
- **Novelty vs. closest in-domain work**: PSGI learns attributes with supplied logical applicability [9]; discovering distinctions from consequence occupancy changes the supervision, while successor-based representation learning and transfer are established and ordinary successor updates are the control.
- **Main risk**: Policy visitation differences masquerade as state semantics, or expected occupancies erase the conjunction a later task requires.

### C8 — Ground a variable by the test that distinguishes histories

- **Intuition**: Define a candidate relation variable by the predicted outcome of a short reachable command test, and choose tests that distinguish currently confounded histories. The variable acquires meaning through observed consequences rather than a teacher's predicate answer.
- **Gap it attacks**: G3 — Unlabeled observations do not determine which distinctions should become reusable applicability variables.
- **Source inspiration**: DAD chooses experiments from design/outcome histories using simulated parameter-conditioned likelihood contrast [15]; OHCAM selects commands through predictive disagreement [5]. Transfer type: recombination-of-distant-concepts.
- **How it maps to this problem**: Competing interface hypotheses play the role of candidate parameters, and legal command sequences play the role of experiments. Their realized outcomes ground a predictive variable that can be queried during another task.
- **Why it could work / feasibility**: Likelihood-based experiment design can concentrate evidence where hypotheses differ [15]. It requires a trustworthy outcome family, physically reachable tests, and explicit preparation/reset costs; no oracle predicate labels are supplied.
- **Novelty vs. closest in-domain work**: OHCAM probes rules over given variables [5]; this changes what a probe identifies, but predictive-state tests and active symbol grounding are prior mechanisms and DAD-style probe amortization itself is established.
- **Main risk**: No affordable legal test separates the histories, so the proposed variable cannot be identified.

### C9 — Refine a history-state machine from consequence counterexamples

- **Intuition**: When two histories assigned the same interface state produce incompatible consequences, add the shortest supported history distinction that separates them. Maintain a small executable state machine so later relation queries retain consumed-resource and preparation history.
- **Gap it attacks**: G4 — Equal visible observations can hide history-dependent prerequisites, making current-state relation pooling incorrect.
- **Source inspiration**: RAD updates persistent recurrent memory from observations/actions/rewards [1]; value equivalence makes retained distinctions relative to a sufficient planning-test space [13]. Transfer type: reinforcing-a-weak-connection.
- **How it maps to this problem**: Actual contradictory transition records become counterexamples to a proposed finite history state. The learned state transition depends on ordinary action/consequence events and augments the relation interface without a supplied hidden-resource label.
- **Why it could work / feasibility**: Persistent memory can retain history [1], while decision tests specify what it must preserve [13]. A finite discrete implementation is plausible only when the relevant hidden history admits a small state machine and recorded consequences support the split.
- **Novelty vs. closest in-domain work**: OpenWAM's local dynamics omit history [8]; explicit counterexample splitting addresses that interface, but active automata learning and learned Markov abstractions already own the central operation.
- **Main risk**: Stochastic outcomes trigger spurious states, or genuinely continuous hidden history causes unbounded refinement.

### C10 — Revise past failure attribution with newly arrived own evidence

- **Intuition**: Keep a bounded trace of uncertain failure causes and revise their attribution when later ordinary observations clarify what happened. Replace the earlier relation contribution instead of appending a second independent update from the same event.
- **Gap it attacks**: G1 — An initially ambiguous consequence can become informative after subsequent own actions, while a prematurely committed relation update can remain wrong across later goals.
- **Source inspiration**: CML retains particle ancestry alongside module states [3]; BOCPD retains competing temporal explanations and their statistics [12]. Transfer type: reinforcing-a-weak-connection.
- **How it maps to this problem**: Ancestry links current observations to uncertain past execution/sensing causes. A proposed bounded smoothing operation recomputes affected likelihood contributions using only evidence already observed before the new-goal decision.
- **Why it could work / feasibility**: Retained temporal hypotheses provide the bookkeeping needed to revisit an explanation [3, 12]. The smoothing extension is proposed here, not a claimed source operation; identifiable delayed consequences and auditable replay prevent hindsight leakage or duplicate evidence.
- **Novelty vs. closest in-domain work**: OHCAM incrementally scores supplied symbolic mismatches [5]; revisable ambiguous contributions change the feedback interpretation, but fixed-lag smoothing and retrospective action diagnosis are established direct priors.
- **Main risk**: Later goal outcomes leak into earlier claimed predictions, or recomputation double-counts the same correction.



# Learning and correction absorption candidates C11–C20

Generation only: all ten feasible mechanisms are retained; none is an acceptance or novelty claim. References [1]–[15] are local registry IDs, not Svalbard IDs. Inspiration comes exclusively from results-masked digests. New search hits remain provisional metadata/abstract signals in the companion annotations; no new paper body was opened.

Common comparison contract: replay the same legal observation/action/consequence histories, missingness indicators and goal inputs. Freeze neural parameters at deployment; only inference memory, latent beliefs, tables or cached plans change. No queried-goal execution or future feedback enters a deployment prediction. Use full DICP-IDT with dynamics/MPC [2], RAD with equal-memory and full-history controls [1], and compositional Bayes with its non-Markovian gate [3], preserving supplied information and reporting memory, inference and training costs. Include ordinary multi-goal compression, exact finite Bayes, and the mechanism-specific controls below. Every failure mechanism is a hypothesis: no new experiment or training was performed.

### C11 — Counterexample-guided memory state splitting

- **Intuition**: Learn a bounded finite memory by splitting two history states when an observed continuation makes their required updates diverge, even if their present actions agree. The changed operation is partition refinement of the updater's states.
- **Gap it attacks**: G5: action-equivalent histories may require different responses to the next correction.
- **Source inspiration**: RAD maps histories into a recurrent latent state [1]; value equivalence depends on the query family and its closure [13]. Their combination motivates testing closure under legal evidence transitions, rather than only present actions.
- **How it maps to this problem**: Start with a coarse partition of recorded histories. For each recorded legal feedback continuation, refine a cell whenever its successors have incompatible predictive distributions or decisions; repeat backward until successor cells agree. Compile the partition and transition table into a frozen updater. Merge only cells satisfying the same empirical successor tests to meet the memory cap; retain uncertainty for unobserved transitions.
- **Why it could work / feasibility**: A small finite history corpus permits CPU partition refinement and exposes an explicit byte budget. Compare equal-memory RAD, predictive-state compression, multi-goal supervision and full-history DICP/Bayes on held-out continuation decisions.
- **Novelty vs. closest in-domain work**: Predictive states, bisimulation, automata learning and abstraction refinement already occupy state splitting. The possible delta is a concrete evidence-update distinction missed by equal-budget alternatives; adding continuation queries alone is thin.
- **Main risk**: Needed distinguishing continuations may be absent from the legal training histories, or refinement may exhaust the memory budget.

### C12 — Provisional evidence escrow with bounded replay

- **Intuition**: Keep an ambiguous correction in a small pending buffer before committing it to irreversible compressed memory. Later own evidence can revise its interpretation and rebuild the provisional state from a checkpoint.
- **Gap it attacks**: G5/G6: premature absorption of an execution slip or censored outcome can survive after the original evidence has been compressed away.
- **Source inspiration**: RAD explicitly overwrites gated latent memory [1]; BOCPD preserves weighted growth/reset alternatives rather than treating every surprise as a change [12].
- **How it maps to this problem**: Maintain committed state z and bounded pending evidence E. Predict using U(z,E), keep competing likelihood-supported interpretations of pending events, and replay E from z when new visible consequences alter those weights. Commit the oldest event only when its interpretation is stable under a declared likelihood criterion; evictions and checkpoint bytes count against the fixed budget. Train the frozen compressor on this checkpoint/pending interface.
- **Why it could work / feasibility**: The buffer makes revision executable without requiring an inverse neural update. A CPU finite-state prototype can compare immediate commitment, fixed-window replay, full-history filtering and equal-byte RAD.
- **Novelty vs. closest in-domain work**: Fixed-lag filtering, delayed-observation replay and belief revision already retain revisable evidence. Only evidence-sensitive commitment under a hard compression budget is a candidate delta; fixed-window replay may match it.
- **Main risk**: A wrong likelihood model can confidently commit the wrong interpretation; unresolved events can consume the entire buffer.

### C13 — Joint filtering of outcomes and their observation process

- **Intuition**: Learn and filter the feedback-selection process alongside the task mechanism. Missing feedback should have its own likelihood, instead of being coded as success, failure or automatically uninformative.
- **Gap it attacks**: G6: the student's own actions may induce informative censoring different from source histories.
- **Source inspiration**: CML weights particles by target likelihood and supports intermittent targets [3]; DICP models consequence distributions from causal histories [2].
- **How it maps to this problem**: Fit a joint model p(v,m|h,a,R), where m is the visible observation indicator, v the possible consequence and R a reusable mechanism hypothesis. Weight each hypothesis by the observed joint likelihood; when v is missing, integrate it out: L(R)=sum_v p(v,m|h,a,R). Learn the joint model through observed-data marginal likelihood, using legal histories rather than supplied eligibility or true-rule labels. Freeze it at deployment.
- **Why it could work / feasibility**: Finite outcomes permit exact CPU summation. Compare ordinary missing-at-random filtering, DICP with the same mask inputs, and compositional Bayes with the identical joint observation model; vary feedback selection independently of physical dynamics.
- **Novelty vs. closest in-domain work**: Selection models, censored-data inference and POMDP observation likelihoods are established. This is an interface extension unless a distinct amortization or identification improvement survives the full joint-Bayes control.
- **Main risk**: Outcome-dependent missingness is generally not identifiable from censored histories without justified assumptions or additional legal observations.

### C14 — Likelihood-set updating when censoring is unidentified

- **Intuition**: When several feedback channels remain observationally compatible, update a set of beliefs instead of committing to a single fitted observation model. Reusable relations become decisive only when the surviving channel models support the decision.
- **Gap it attacks**: G6: insufficiently identified own feedback can produce falsely precise relation updates.
- **Source inspiration**: CML supplies likelihood-weighted competing compositions [3]; OHCAM maintains alternative scored hypotheses [5]. Their point likelihoods motivate an explicit uncertainty set for the feedback interface.
- **How it maps to this problem**: Maintain a bounded family of channel likelihoods consistent with legal calibration records and explicit noise/censoring bounds. Apply each likelihood to the same relation hypotheses, preserving shared channel parameters across relations. Choose a goal action by minimax expected cost over the resulting joint belief set; prune only dominated models or state the approximation. No missing outcome is imputed as a fact.
- **Why it could work / feasibility**: Small finite sets and a fixed skill library permit CPU enumeration. Compare point-estimate Bayes, robust Bayes/POMDP planning with identical sets, and DICP ensembles at equal memory and compute; report excessive conservatism as well as errors.
- **Novelty vs. closest in-domain work**: Robust Bayesian inference and uncertainty-set control already implement the basic idea. The candidate is a bounded reusable-evidence representation and its cost, not robustness itself.
- **Main risk**: Coverage depends on defensible likelihood bounds; a broad set may prevent useful transfer while a narrow wrong set creates false assurance.

### C15 — Particle preservation by update-response diversity

- **Intuition**: Preserve particles that would react differently to a possible next correction, even when they predict the same current action. Allocate resampling capacity by update-response clusters rather than particle weight degeneracy alone.
- **Gap it attacks**: G5/G6: a finite posterior population can lose an explanation before later evidence would distinguish it.
- **Source inspiration**: CML retains identities, hidden states and ancestry through likelihood weighting/resampling [3]; BOCPD retains alternative growth/reset histories [12].
- **How it maps to this problem**: For a bounded catalogue of modeled legal feedback tokens, fingerprint each particle's hypothetical posterior-response predictions. Cluster those fingerprints and stratify a fixed particle budget across clusters, retaining their posterior masses with appropriate weights. Use posterior-invariant move kernels over a retained causal suffix to diversify particles when collapse threatens a distinct response cluster. Modeled tokens schedule computation and never count as observed evidence.
- **Why it could work / feasibility**: CPU finite filters can verify weighted resampling and compare ordinary ESS-triggered resample-move, equal-budget CML, and exact Bayes. Account for catalogue evaluation, suffix storage and likelihood evaluations.
- **Novelty vs. closest in-domain work**: Resample-move, diverse particle populations and bounded-memory coresets are established. Only the update-response allocation criterion is a possible delta; generic diversity or extra particles would erase it.
- **Main risk**: Response fingerprints can be expensive or miss the actual distinguishing event; suffix moves cannot recover an already discarded prefix hypothesis.

### C16 — Dependency-valid ordering of correction histories

- **Intuition**: Augment updater training with alternative orders of independent evidence blocks, so memory learns which order matters. Change the training history distribution through restricted causal reordering, rather than obtaining new action labels.
- **Gap it attacks**: G6: a learned updater may overfit the source policy's ordering of informative and uninformative consequences.
- **Source inspiration**: CoDA recombines components only within valid local dependency regions [11]; RAD recurrently compresses ordered learning histories [1].
- **How it maps to this problem**: Build a dependency DAG over recorded correction blocks using visible causes, state changes, resource use and feedback-selection dependencies. Sample alternative topological orders only when reconstructed intermediate inputs remain supported by recorded data and both blocks stay within the same local validity region. Train the original updater on these reordered evidence blocks with its original supervision; reject swaps involving destructive effects, change points or coupled censoring. Deployment receives only its actual chronology.
- **Why it could work / feasibility**: A tiny controlled corpus can inspect every accepted reorder on CPU. Compare same-update-count ordinary replay, unrestricted shuffling, CoDA, multi-goal RAD and full-context DICP.
- **Novelty vs. closest in-domain work**: Causal augmentation and replay are occupied. The narrow candidate distinction is preserving the semantics of mechanism evidence while varying history order; it may reduce to CoDA over an enlarged state.
- **Main risk**: Estimated independence does not establish valid physical or likelihood reordering; global latent change can invalidate apparently disjoint blocks.

### C17 — Low-rank successor resolvent correction

- **Intuition**: Propagate a localized transition correction analytically through cached successor occupancies. A matrix update can repair all goal weights together before another goal is executed.
- **Gap it attacks**: G7: reward reweighting leaves dynamics-dependent occupancy stale after a corrected prerequisite or effect.
- **Source inspiration**: Successor features separate occupancy from reward weights and obey a Bellman equation [14]; value equivalence targets relevant Bellman predictions [13].
- **How it maps to this problem**: For each fixed skill policy, cache M=(I−gamma P)^−1 and Psi=M Phi. Infer a same-data local transition patch DeltaP=UV^T; update M with the Woodbury identity, then Psi and GPI values for every goal. Affected-row scope is inferred from legal feedback, never supplied as truth. Recompute when the patch is not low rank or numerical conditioning fails; policy switches require evaluation of their own cached dynamics.
- **Why it could work / feasibility**: Finite-state linear algebra is CPU executable. Compare full inversion/replanning, dynamic SF-TD, prioritized sweeping and DICP at identical transitions; the benefit sought is repair cost with matched prediction quality.
- **Novelty vs. closest in-domain work**: Matrix inversion identities and successor-representation updates are known. Low-rank propagation alone is not new; only a useful inferred patch scope or certified approximation/cost result could add substance.
- **Main risk**: Physical corrections may change many rows, features or policies; an inaccurate local patch propagates error globally.

### C18 — Backward closure of corrected handoff contracts

- **Intuition**: Treat a downstream skill's revised requirement as an obligation that must be propagated through upstream handoffs. Repair cached entry guards by backward preimage computation instead of rediscovering every complete composition.
- **Gap it attacks**: G7: local applicability updates can leave predecessor skills and cached composed plans accepting invalid handoffs.
- **Source inspiration**: APPL stores support/handoff/verification interfaces [4]; PACTS predicts predicate trajectories but composes with supplied operators [6]; OHCAM refines action-model conditions [5].
- **How it maps to this problem**: Keep the relation learner identical across methods. When own evidence revises a skill requirement R, mark dependent composition edges dirty and recompute upstream guards by the current transition model's preimage of R. Cache shared guard formulas and propagate until obligations stabilize; use posterior-weighted or worst-case preimages when effects are uncertain. Guards are hypotheses from visible evidence, not newly supplied eligibility labels.
- **Why it could work / feasibility**: A small predicate/skill vocabulary permits CPU fixed-point propagation. Compare full replanning, incremental planning/truth maintenance, unchanged APPL/PACTS interfaces and same-data Bayesian action models, measuring changed and unaffected plans.
- **Novelty vs. closest in-domain work**: Weakest preconditions, assume-guarantee reasoning and symbolic repair cover the basic operation. The possible delta concerns cached closure of learned uncertain handoffs and its computation; generic persistent repair is already occupied.
- **Main risk**: Incorrect predicate grounding or transition models make propagated guards unreliable, and conservative closure may reject feasible compositions.

### C19 — Contextual low-rank dynamics residual inference

- **Intuition**: Absorb corrective consequences as a posterior over a small task latent that adjusts frozen dynamics predictions. Reusing that latent in planning can affect multiple goals without updating neural weights or storing a complete new operator model.
- **Gap it attacks**: G6/G7: an own correction may reveal a shared transition residual whose effect is lost by source-action imitation or stale skill values.
- **Source inspiration**: DICP predicts future consequences for MPC [2]; OpenWAM supplies local forward dynamics [8]; CML infers reusable latent compositions with frozen modules [3].
- **How it maps to this problem**: Learn frozen residual features B and phi, defining f(o,a,h,z)=f0(o,a,h)+B diag(z) phi(o,a,h). Maintain a Gaussian or finite posterior over z in external inference state; update it from realized prediction residuals with analytic Bayesian regression, including observation noise and missing channels. Condition the same planner on this posterior for every goal. The coefficients are context latents, not modified neural parameters.
- **Why it could work / feasibility**: A low-dimensional linear observation model permits exact CPU checks. Compare ordinary contextual system identification with identical features, full DICP context, joint Bayes and SF dynamics updates; verify affected and unrelated goal predictions.
- **Novelty vs. closest in-domain work**: Bayesian residual models and meta-learned online dynamics adaptation already occupy this mechanism. The candidate remains useful only if its compact residual family covers a specific relation-transfer bottleneck at lower cost.
- **Main risk**: A smooth low-rank residual may not express discrete prerequisites, contact modes or destructive effects; latent coefficients can fit execution noise rather than reusable structure.

### C20 — Causal proposal training for the actual feedback interface

- **Intuition**: Train a deployable causal particle proposal on the student's observed feedback interface, then use importance correction to preserve the modeled posterior. Replace training-only lookahead proposals with proposals executable from the same causal prefix used at deployment.
- **Gap it attacks**: G6: sparse own feedback can make bootstrap proposals inefficient or overconcentrated despite good source-history action imitation.
- **Source inspiration**: CML uses future-guided training proposals but bootstrap deployment filtering [3]; DAD amortizes sequential inference-dependent choices using simulated adaptive histories [15].
- **How it maps to this problem**: On recorded causal own-policy prefixes, use exact finite inference or a separately controlled high-quality filter to estimate the modeled posterior using only already observed channels. Train q(z_t|h_t) to cover that posterior. At deployment propose from q and weight by target/proposal likelihood ratios, retaining the original non-Markovian gate. Prefix feedback schedules and missingness inputs match across training and controls; no optimal action or true-rule label is required.
- **Why it could work / feasibility**: Finite models and a small proposal network can be prototyped on CPU. Compare bootstrap CML, existing learned causal proposals, exact Bayes and same-data DICP/RAD; measure effective samples, calibration and downstream decisions at equal total likelihood/compute budgets.
- **Novelty vs. closest in-domain work**: Amortized SMC and inclusive-KL proposal training already implement the core. The plausible question is deployment-interface matching and efficiency; ordinary proposal learning on the same histories may fully cover it.
- **Main risk**: Self-generated posterior targets can recycle the model's mistakes, and a narrow proposal can exclude hypotheses that importance weighting cannot restore.


# Composition, verifier teaching, and reachable acquisition: C21–C30

All numeric citations are checked local registry IDs, not Svalbard IDs. Mechanism transfer uses results-masked digests only. Search links below are primary-source novelty signals from titles/abstracts, not additional method digests. No full paper was opened, candidate was eliminated, experiment was run, or training was performed. Proposed deployment changes external records/query sets while neural parameters remain frozen; any optional readout training precedes deployment. Observed variables must come from legal observations/actions/consequences. A CPU reference is methodological evidence only, never robot validation.

### C21 — Complete the conjunction basis with an observed counterexample

- **Intuition**: For G8, replace a fixed decision-query basis with insertion of one product query when correction-consistent models agree on retained queries but disagree on an unexecuted conjunction. Transfer requires observable component predicates and a legal consequence history that preserves the disagreeing alternatives; a hidden true rule cannot supply the counterexample.
- **Gap it attacks**: G8 — equivalence on separate component goals can erase the distinction between “both survive” and “each succeeds separately.”
- **Source inspiration**: VE's Bellman agreement over chosen function/policy spans [13]; CML's preservation of alternative compositions [3]; OHCAM's correction-consistent hypotheses [5].
- **How it maps to this problem**: Maintain a bounded set of query functions and relation hypotheses. On a new conjunction, search pairs of surviving models that agree on the cache. If their Bellman updates differ on the conjunction, retain that product query and replay only receipts touching its variables; merge summaries only if they also agree on this added query.
- **Why it could work / feasibility**: A finite symbolic reference can perform model-pair checks and replay on CPU. The potential gain is selective closure at smaller memory than preloading every conjunction; no model distinction is licensed by invented target feedback.
- **Novelty vs. closest in-domain work**: VE already enlarges query families, and CML already retains alternatives. [CEGAR planning](https://ojs.aaai.org/index.php/ICAPS/article/view/13605) is a close search signal. The contested delta is a receipt-grounded, memory-bounded query-insertion rule; equal-memory adaptive abstraction and multi-goal distillation may already match it.
- **Main risk**: Pair search becomes as expensive as full joint planning, or ordinary hard-query mining gives the same result.

### C22 — Splice only up to the next interaction frontier

- **Intuition**: For G8, compose independent observed transition fragments only until their components would interact, then retain that boundary as an unresolved joint transition rather than extrapolating a successful conjunction. Transfer requires a valid local dependency region for every stitched step, including the shared arm and consumed resources.
- **Gap it attacks**: G8 — separately valid component predictions need not determine the first coupled transition in a new goal.
- **Source inspiration**: CoDA's state-local connected-component recombination and validity-region requirement [11]; OpenWAM's individually supervised counterfactual transitions [8].
- **How it maps to this problem**: Index own receipts by component assignments and local validity conditions. Join compatible fragments, check the modified assignment at each step, and stop before the first mask change/contact/resource interaction. A later real correction resolves that frontier and permits further composition; synthesized fragments remain model data.
- **Why it could work / feasibility**: CPU receipt joining can reuse long independent prefixes without reconstructing all visual dynamics. It offers a precise boundary for when current experience supports a conjunction and when another real transition is required.
- **Novelty vs. closest in-domain work**: CoDA owns causal recombination; OpenWAM owns branched dynamics records. [MoCoDA](https://proceedings.neurips.cc/paper_files/paper/2022/hash/7314e20a73542bbfff25030d1185ce88-Abstract.html) is another search signal requiring later review. Only frontier-truncated multi-step reuse is proposed; masks and data must be matched against stepwise CoDA and a full model.
- **Main risk**: Incorrect masks falsely certify a prefix, or frequent shared-arm interactions leave almost nothing to splice.

### C23 — Cache observed failures of action-order exchange

- **Intuition**: For G8, change plan compression from assuming independent skills commute to storing a conditional order defect when legal A-then-B and B-then-A histories produce different observed joint effects. Transfer requires comparable entry-state/history variables and sufficient support for both orders; unmatched logs do not identify a commutator.
- **Gap it attacks**: G8 — an unseen conjunction may depend on order because one skill deletes a prerequisite or completion produced by another.
- **Source inspiration**: CoDA's local independence boundary [11]; SF's dependence on policy-induced dynamics [14]; OHCAM's conditional add/delete effects [5].
- **How it maps to this problem**: Compare supported two-skill receipt compositions under a shared visible entry condition. Store the residual between their joint postconditions, with its condition and evidence pointers. When compressing a new plan into an unordered skill set, preserve the implicated ordering or expose both alternatives if the residual is uncertain.
- **Why it could work / feasibility**: Sparse pair records are cheap on CPU and can preserve a destructive interaction without fitting every full operator. The reusable item is a conditional order restriction justified by consequences, not the source task's successful sequence.
- **Novelty vs. closest in-domain work**: Partial-order planning, conditional action-model learning, PSGI/OHCAM, and causal control are established. [Some Orders Are Important](https://ojs.aaai.org/index.php/SOCS/article/view/31561) and [Conditional-SAM](https://ojs.aaai.org/index.php/ICAPS/article/view/31498) are proximity signals. The thin delta is receipt-supported exchange-defect compression; full conditional operators may dominate it.
- **Main risk**: Apparent order sensitivity comes from entry-state aliasing or executor variation.

### C24 — Teach equivalence classes of observed effects

- **Intuition**: For G9, replace feature-dispersion teaching examples with pairs defined by equality or inequality of legally observed effects on a relation query. Transfer requires an observable query and, for augmented pairs, CoDA-valid independence; visually diverse candidates with the same relevant consequence should receive the same relation target.
- **Gap it attacks**: G9 — action-feature distance can spend labels on consequence-equivalent proposals and miss similar proposals with different relational effects.
- **Source inspiration**: DiVeR's terminal-label/feature-variance interface [7]; VE's decision-relative equivalence [13]; CoDA's valid component swaps [11].
- **How it maps to this problem**: Project own realized transitions onto fixed grounded relation queries. Form same-effect pairs across nuisance variation and different-effect pairs under matched visible context. Train a small readout before deployment, or use a nonparametric pair cache; at runtime observed corrections update cache support while the readout stays frozen.
- **Why it could work / feasibility**: Pair construction and an exact feature/query reference are CPU feasible. The objective forces the verifier to encode a reusable consequence distinction rather than merely rank the current candidate set.
- **Novelty vs. closest in-domain work**: Contrastive learning and causal augmentation are priors. [CAIAC](https://proceedings.mlr.press/v235/armengol-urpi-24a.html) and [HAVE](https://proceedings.mlr.press/v305/li25e.html) are close search signals, not digested inspiration. The proposed delta is query-defined effect-pair construction; compare same-data contrastive features and direct consequence supervision.
- **Main risk**: Observed effect equality is too coarse for later goals, or supplied query grounding already contains the needed relation.

### C25 — Teach the first observable distinguishing consequence

- **Intuition**: For G9, replace inherited terminal labels with the earliest observed consequence on which surviving relation hypotheses make different predictions. Transfer requires a causally available prefix and an actual observable witness; ambiguous or missing evidence yields a set-valued target rather than an invented failure cause.
- **Gap it attacks**: G9 — later recovery can make an early relational mistake and a correct early action inherit the same success label.
- **Source inspiration**: OHCAM's observation-mismatch refinement [5]; DiVeR's executed-feature terminal labels [7]; OpenWAM's transition consequence supervision [8].
- **How it maps to this problem**: For each correction history, retain predictions made before each observation. Locate the first observed mismatch that separates surviving hypotheses, and teach the verifier the witness consequence/query, not source completion. Replay that witness into the persistent relation cache so a later unexecuted goal can use the distinction.
- **Why it could work / feasibility**: A tabular witness extractor is CPU feasible. It uses future observations only as construction-time targets and gives a fixed readout a supervision channel closely aligned with the relation updater.
- **Novelty vs. closest in-domain work**: Stepwise supervision and action-model mismatch learning are established; [process verifier work](https://arxiv.org/abs/2410.08146) and [interactive robot reward functions](https://proceedings.mlr.press/v205/huang23a/huang23a.pdf) are search signals. The contested delta is hypothesis-separating observable witness targets. Match ordinary transition prediction and full prefix supervision.
- **Main risk**: A first discrepancy is weak evidence about the reusable relation, or ordinary dense consequence targets already teach it.

### C26 — Hold a relation target fixed across valid recovery-tail substitutions

- **Intuition**: For G9, construct paired histories whose prefix has the same observed relational effect but whose independent recovery tails differ, and require an identical prefix-relation prediction. Transfer requires local independence of the substituted tail from every variable in the prefix query; a later action that actually repairs that variable cannot be substituted.
- **Gap it attacks**: G9 — verifier supervision can identify a recovery suffix rather than what the earlier command established.
- **Source inspiration**: CoDA's cause/effect-preserving component exchange [11]; DiVeR's terminal-outcome supervision [7]; OpenWAM's lack of a paired-branch objective [8].
- **How it maps to this problem**: Take a real prefix receipt and exchange only certified independent tail components from another supported history. Use the real prefix consequence as the common target, impose prediction consistency across the pair, and retain separate terminal labels. At deployment, actual receipts update the relation cache.
- **Why it could work / feasibility**: Pair construction is CPU feasible; a small predeployment readout or exact cache can test the supervision operation. The paired constraint is intended to remove a terminal-recovery shortcut without claiming causal attribution from erasing text.
- **Novelty vs. closest in-domain work**: CoDA, causal invariance, and earlier project erasure-credit ideas are strong priors. [RoCoDA](https://arxiv.org/abs/2411.16959) and [Invariant Action Effect Model](https://ojs.aaai.org/index.php/AAAI/article/view/20913) are search signals. Any delta is the certified tail-substitution pair target, and may reduce to ordinary invariance teaching.
- **Main risk**: Independence certificates leak privileged state or miss a delayed effect of the recovery tail.

### C27 — Swap the verification query on one realized transition

- **Intuition**: For G9, teach one observed transition under paired query descriptions that differ in a single consequence clause, so the verifier must change its answer when the observed relation warrants it. Transfer requires evaluable visible consequences for both queries; no synthetic full-goal completion label is assigned to an unexecuted goal.
- **Gap it attacks**: G9 — a current-goal success verifier may learn task identity rather than the consequence distinctions needed by another conjunction.
- **Source inspiration**: SF's separation of transition features from goal weights [14]; VE's explicit query family [13]; DiVeR's frozen proposer and scalar outcome target [7].
- **How it maps to this problem**: Evaluate two one-step relational questions on the same own receipt, such as “placed A” versus “placed A and preserved B.” Include matched positive/negative query-swap pairs in predeployment teaching, with the unchanged state/action features. Deployment corrections add factual query answers to the external cache.
- **Why it could work / feasibility**: CPU relabeling needs no new trials and directly tests whether verifier predictions respond to a destructive-effect clause. Its usefulness must be measured on new compositions before their execution, rather than on relabeled source accuracy.
- **Novelty vs. closest in-domain work**: HER, goal-conditioned reward learning, and multi-goal distillation already occupy relabeling. [GS-HER](https://arxiv.org/abs/2606.09476) is a particularly close search signal; [goal-relabeling analysis](https://proceedings.mlr.press/v235/zheng24a.html) is another. This is a thin candidate for query-swap verifier supervision, requiring an equal-query HER control, not a novelty claim.
- **Main risk**: It is entirely covered by predicate-level hindsight relabeling, or cannot infer beyond the supplied visible query vocabulary.

### C28 — Share preparation prefixes across probe alternatives

- **Intuition**: For G10, compile candidate diagnostic experiments into an executable prefix trie so common preparation is evaluated once and the next branch is selected only after the real prefix outcome. Transfer requires legal preparation commands and path-conditioned likelihoods; a shared imagined state is never treated as a free reset.
- **Gap it attacks**: G10 — independently optimizing experiments can repeatedly pay setup or choose branches that consume a prerequisite needed by another test.
- **Source inspiration**: DAD's history-to-design amortization and contrastive likelihood objective [15]; OHCAM's disagreement rollouts [5].
- **How it maps to this problem**: Expand each probe into preparation plus diagnostic actions. Merge identical supported command prefixes while keeping terminal resource states and relation predictions distinct. Cache likelihood terms at shared nodes, execute one edge, and re-root the trie on the observed outcome before choosing the next edge.
- **Why it could work / feasibility**: A symbolic trie/compiler is CPU feasible with frozen policies. Its claim is reduced preparation/search duplication at the same real command and restoration budget; information and downstream utility objectives remain standard.
- **Novelty vs. closest in-domain work**: DAD, dual control, cost-aware Bayes-adaptive planning, DREAM, and prefix-sharing search are priors. [Markov-design](https://proceedings.mlr.press/v206/mutny23a.html) and [RL experimental design](https://proceedings.mlr.press/v162/blau22a.html) are proximity signals. The proposed operation is prefix-factorized executable acquisition, not adding a cost term.
- **Main risk**: Most probe paths share no useful prefix, or trie bookkeeping saves compute but no interactions.

### C29 — Backward-compile a distinguishing state into a real probe

- **Intuition**: For G10, replace a requested experiment-state input with backward regression that must construct a supported preparation path from the robot's current state before a probe is eligible. Transfer requires grounded action requirements and observable resource state; regressions unsupported by own receipts remain unresolved rather than becoming simulator-restored samples.
- **Gap it attacks**: G10 — a highly informative imagined probe can be physically unreachable or require destructive setup.
- **Source inspiration**: DAD's directly chosen design interface [15]; OHCAM's conditional precondition/effect hypotheses and one-action rollout execution [5]; OpenWAM's simulator-restored branching boundary [8].
- **How it maps to this problem**: Start from an observation where two relation hypotheses predict different consequences. Regress the required state through candidate preparation actions under every surviving explanation; cache a preparation/probe macro only when it has a common supported path. Execute from the actual current state, observe each step, and invalidate the macro after a contradictory correction.
- **Why it could work / feasibility**: Small-domain backward search is CPU feasible and can reuse verified preparation requirements across goals. Count every setup, diagnostic action, failed prerequisite and restoration in its cost.
- **Novelty vs. closest in-domain work**: Planned exploration and causal control already cover reachable tests. [Online action-model learning](https://www.ijcai.org/proceedings/2021/566) and [Markov-design](https://proceedings.mlr.press/v206/mutny23a.html) are strong signals. The thin proposed delta is a correction-invalidated reusable probe compiler; a full-cost planner is the mandatory control.
- **Main risk**: Conservative common-path regression rejects useful probes, or reduces to standard planning with an information goal.

### C30 — Acquire evidence through resource-preserving action cycles

- **Intuition**: For G10, search for a diagnostic action cycle whose predicted final resource/query state equals its entry state under every surviving relation explanation, while intermediate observations separate those explanations. Transfer requires physically reversible supported commands and observed return checks; the return condition does not guarantee equivalence of hidden state.
- **Gap it attacks**: G10 — an informative test can destroy the opportunity to execute the later task it was meant to help.
- **Source inspiration**: DAD's contrastive history likelihoods [15]; CoDA's state-local validity requirement [11]; SF's dynamics-dependent resource occupancy [14].
- **How it maps to this problem**: Enumerate short executable cycles from the current state. Keep only cycles with a common predicted terminal resource state, compare their intermediate consequence likelihoods, and execute a selected cycle stepwise. Retain the evidence but invalidate the cycle's return certificate whenever the real final observation disagrees.
- **Why it could work / feasibility**: CPU enumeration can test a narrow reversible manipulation family with frozen skills. The proposed search reduces acquisition to cycles sharing an entry/exit interface, offering a reusable experiment without an uncounted reset.
- **Novelty vs. closest in-domain work**: Reversibility-guided exploration, Bayesian control, and cost-aware experiment design are established. [There Is No Turning Back](https://proceedings.neurips.cc/paper/2021/hash/0e98aeeb54acf612b9eb4e48a269814c-Abstract.html) and [active exploration in MDPs](https://proceedings.mlr.press/v89/tarbouriech19a.html) are primary abstract signals. Only hypothesis-discriminating cycle compilation is proposed; exact Bayes-adaptive planning may already implement it.
- **Main risk**: Hidden resource changes violate observed return equivalence, or informative reversible cycles do not exist.


# Root innovator pass — local-paper IDs, results-masked mechanism inputs

Ten candidate intuitions retained without novelty verdict. Seven native fields per candidate; ARIS experiment annotations belong in a separate artifact. Numeric IDs refer to paper-registry.json.

### C31 — Learn when two evidence updates may commute
- **Intuition**: Train a memory updater to give the same decisions when genuinely independent correction records arrive in either order, while allowing order to matter when the physical mechanism changes. The useful operation is learning which events share a mechanism, rather than enforcing indiscriminate permutation invariance.
- **Gap it attacks**: G5/G6 — an order-sensitive compressed history can encode incidental source chronology; a globally invariant summary can erase genuine changes.
- **Source inspiration**: DAD exploits history symmetries [15]; BOCPD keeps alternatives about when data-generating parameters changed [12].
- **How it maps to this problem**: Independent same-world correction receipts are exchangeable evidence, whereas a transition after a changed requirement belongs to a different regime. A frozen updater should retain the appropriate distinction without receiving a true changepoint label.
- **Why it could work / feasibility**: Small repeated-event histories permit same-record order tests and likelihood-based references. Feasibility depends on inferring dependence from allowed observations; the ambiguity must remain when the history cannot determine it.
- **Novelty vs. closest in-domain work**: RAD already learns recurrent updates [1] and DAD already teaches invariance [15]; the candidate delta is a conditional evidence-update algebra with both commuting and noncommuting training cases. Group equivariance, continual inference and selective forgetting may already implement it; direct search is necessary.
- **Main risk**: Conditional invariance could reduce to a learned gate plus existing recurrent training, with no distinguishable operation or benefit under equal data.

### C32 — Reopen only hypotheses contradicted by a correction
- **Intuition**: Cache the reasoning that made a task relation usable, and learn which cached dependencies a new failure actually invalidates. Recompute the affected hypothesis region rather than rebuilding every task model or trusting all cached conclusions.
- **Gap it attacks**: G7 — a corrected transition requirement can invalidate future handoffs and values, but full rebuilding ignores the sparsity of the change.
- **Source inspiration**: OHCAM expands conditions only when data conflict [5]; successor features separate goal reward from policy-induced dynamics [14].
- **How it maps to this problem**: A cached relation or successor prediction carries references to observed support and preceding relations. A correction activates a bounded recomputation region; retained unaffected predictions remain available for the next goal.
- **Why it could work / feasibility**: Controlled task families can expose repeated unchanged substructures, allowing direct counts of rescored hypotheses and updated values. Real evidence must validate the selected invalidation region; no hidden changed-edge indicator is supplied.
- **Novelty vs. closest in-domain work**: Incremental planning, prioritized sweeping and truth-maintenance are strong likely priors; OHCAM already performs incremental refinement [5]. The candidate can only contribute a learned dependency-selection operation that preserves inference semantics and saves measured work beyond these controls.
- **Main risk**: Ordinary incremental inference with explicit dependencies may achieve all claimed savings without learning.

### C33 — Distill an update that remains useful after the policy changes
- **Intuition**: Teach the same experience updater under several learner policies so it cannot identify an observation's meaning from the source algorithm's characteristic action order. Test it with its own changed exploration and recovery behavior.
- **Gap it attacks**: G6 — source learning histories may make the observation meaning and algorithm identity inseparable in action prediction.
- **Source inspiration**: RAD distills source UCB/PPO learning histories [1]; DICP learns shared predictive dynamics from histories [2].
- **How it maps to this problem**: Different policies generate legal evidence about the same relation. The updater is trained to support the same posterior-dependent decisions from information-equivalent histories despite different visit patterns.
- **Why it could work / feasibility**: CPU policies and known finite references allow information-equivalent histories with different samplers; deploying the frozen student creates its own causal history. Gathering more histories alone is a matched baseline.
- **Novelty vs. closest in-domain work**: Algorithm distillation, DAgger and off-policy meta-RL already mix policy distributions. The delta would need an actual invariance or update constraint under policy changes, not merely multiple-teacher training.
- **Main risk**: Equal-volume diverse-history training may reproduce any benefit, leaving only data coverage.

### C34 — Carry measurement context with reusable evidence
- **Intuition**: Store a correction as a likelihood-bearing observation with its measurement context, rather than as a concluded rule. Let another goal use that observation against its own hypotheses without pretending the same outcome occurred there.
- **Gap it attacks**: G6/G8 — source conclusions and raw receipt splices can change the meaning of uncertain evidence when background relations differ.
- **Source inspiration**: CoDA's valid substitutions require remaining in a locally independent region [11]; compositional task inference uses likelihood-weighted alternatives [3].
- **How it maps to this problem**: Public state, command binding and observation conditions travel with the actual event. The receiver can preserve joint uncertainty and infer relevance rather than importing a source posterior or synthesized physical outcome.
- **Why it could work / feasibility**: Small ambiguous histories provide exact source/recipient reference posteriors. This is feasible only if the needed measurement context is observable; hidden scope cannot be filled in by the simulator.
- **Novelty vs. closest in-domain work**: Bayesian evidence transfer and causal transport already provide the principle; the rejected R1 also approached it. An implementable compact neural likelihood message would need a specific complexity or generalization advantage over joint Bayes and same-data context encoding.
- **Main risk**: Correct bookkeeping is mistaken for an algorithm; a learned encoder may discard exactly the nuisance dependence it must retain.

### C35 — Train memory on the consequences of the next correction
- **Intuition**: When compressing a history, test not only its current decision but how the compressed memory reacts to several possible next observations. Preserve distinctions that are dormant now but matter for learning from the next real correction.
- **Gap it attacks**: G5 — present action/value equivalence need not imply equivalence of future evidence updates.
- **Source inspiration**: Value equivalence is relative to policy/function sets [13]; RAD's memory is trained with source action prediction [1]; DAD reasons over sequential histories [15].
- **How it maps to this problem**: Full and compressed histories are compared after the same legally generated next event. A future-feedback test teaches the compressor to retain uncertainty needed by the updating operation, rather than a static current-goal answer.
- **Why it could work / feasibility**: A bounded environment can generate legal continuation branches for offline training; imaginary feedback is never counted as deployment experience. Ordinary multi-step prediction and equal-query distillation are available controls.
- **Novelty vs. closest in-domain work**: Predictive-state representations, bisimulation, causal distillation and next-step consistency are direct likely priors. The candidate delta is update-aware rather than current-action compression, and must survive a same-data multi-step distillation comparison.
- **Main risk**: The supposed new objective is simply existing future-sequence prediction under a different name.

### C36 — Update goal programs through changed transition features
- **Intuition**: Represent a goal's progress as a small executable automaton and update only the transition features affected by a correction. Compose existing skills toward new ordered or conjunctive goals without reducing the task to an additive reward weight.
- **Gap it attacks**: G7/G8 — reward-weight transfer does not itself express a newly observed prerequisite or destructive effect in a goal composition.
- **Source inspiration**: Successor features/GPI separate reward and occupancy [14]; PACTS uses predicate trajectories to sequence skills [6].
- **How it maps to this problem**: A corrected skill effect changes which automaton transitions become feasible. The memory is queried by the new goal program, preserving distinctions between accomplishing components separately and jointly maintaining them.
- **Why it could work / feasibility**: Finite goal programs and reusable skill effects can be tested on CPU with exact model replanning as reference. The automaton is a public goal description, not a hidden task graph.
- **Novelty vs. closest in-domain work**: Reward machines, temporal-logic RL and generalized successor representations are strong direct neighbors. A learned local update must add more than the known product-MDP construction or ordinary successor TD.
- **Main risk**: The goal representation solves composition by construction while the learning component contributes nothing beyond existing algorithms.

### C37 — Turn a bypassed failure into a reusable applicability experiment
- **Intuition**: A successful workaround should not erase the unresolved failure. Select a short ordinary-command experiment only when resolving that failure would change preparation for another plausible goal.
- **Gap it attacks**: G9/G10 — source success and action diversity can hide a still-unknown relation, while unrestricted information exploration can spend trials on irrelevant uncertainty.
- **Source inspiration**: OHCAM uses model disagreement [5]; DAD amortizes sequential experiment choice [15]; value equivalence distinguishes decision-relevant models [13].
- **How it maps to this problem**: Keep competing relation explanations from the actual failure, identify their disagreement on legal future goals, and choose a reachable experiment whose real outcome separates those explanations.
- **Why it could work / feasibility**: Small exact Bayes-adaptive references permit total-cost accounting; preparation and reset are ordinary paid commands. No oracle failure-cause label is required.
- **Novelty vs. closest in-domain work**: DREAM, decision-focused active learning and the prior CON-03 already cover most of this intuition. It is retained as a central-problem control; only a different probe compilation or cost-solving operation could create an algorithmic delta.
- **Main risk**: This is the old probe idea renamed, with no new mechanism; deep review should record that exact overlap rather than reward a new title.

### C38 — Weight feedback by disagreement about effects, not action distance
- **Intuition**: Spend verifier-training effort where plausible commands disagree about task consequences. Do not assume that far-apart action representations mean a useful decision, or that similar motions are interchangeable near a task boundary.
- **Gap it attacks**: G9 — a candidate-feature variance proxy can emphasize consequence-equivalent diversity or miss effect-critical choices.
- **Source inspiration**: DiVeR weights terminal-label training by action-token variance [7]; OpenWAM exposes action/transition alternatives [8]; value equivalence targets decision consequences [13].
- **How it maps to this problem**: Real or offline-validated alternative outcomes supply a consequence-disagreement weight for the same executed feedback. The score is used to teach a relation-aware critic and must improve later goal decisions, not merely current ranking.
- **Why it could work / feasibility**: Controlled branches with shared starting observations allow a direct proxy test and equal-data uniform/DiVeR-style critic training. A model-produced effect is not independent ground truth.
- **Novelty vs. closest in-domain work**: Action-value learning, causal credit assignment and counterfactual verifier training may already contain the full mechanism. The delta would be a specific consequence-based weight with equal labels/candidate sets, not “a better verifier.”
- **Main risk**: Extra branched outcomes explain improvement, and same-data Q-learning duplicates it.

### C39 — Teach the student the decision allowed by its own evidence
- **Intuition**: A teacher with hidden task knowledge should teach a distribution over decisions justified by the student's history, rather than a uniquely correct action from the teacher's private state. This prevents the student from being trained to infer a relation its observations never identified.
- **Gap it attacks**: G6 — privileged action labels can prescribe certainty absent from autonomous deployment feedback.
- **Source inspiration**: Compositional particle inference represents alternative explanations with likelihood [3]; DICP distinguishes source-action supervision and modeled dynamics [2]; PSGI explicitly receives eligibility [9].
- **How it maps to this problem**: During offline teaching, sample all task explanations compatible with the student's allowed observations and aggregate their decision advice. The resulting student receives no hidden graph at deployment and keeps ambiguity when necessary.
- **Why it could work / feasibility**: Exact small references permit controlled ambiguous-support cases; the same teacher supervision budget is given to all distillation baselines. Larger settings require an honest approximate posterior.
- **Novelty vs. closest in-domain work**: Asymmetric imitation, ADVISOR/A2D and Bayesian policy distillation are direct likely priors; this cannot be claimed as generic student-aware teaching. A new operation must address sequential knowledge updates or practical posterior approximation beyond those methods.
- **Main risk**: It repeats an existing observation-aware teacher and the prior cycle's diagnosis of privileged-label leakage.

### C40 — Learn experiments that leave the robot ready for the next goal
- **Intuition**: Choose a correction experiment partly by the useful physical state it leaves behind. An informative action that destroys a needed resource can be worse than a slightly less informative action that also prepares the next task.
- **Gap it attacks**: G10 — entropy-based experiment choice and restored-state branches omit path-dependent resource and staging effects unless the objective includes them.
- **Source inspiration**: DAD optimizes sequential information [15]; OHCAM executes imagined probes [5]; PACTS models skill effects used by composition [6].
- **How it maps to this problem**: The probe policy is trained on real reachable command sequences and their final staging states, with total future task cost included. Information and execution consequences come from the same actual action.
- **Why it could work / feasibility**: A small consumable-resource domain can be solved exactly for a cost-aware reference before a frozen learned probe is trained. Future goals use the declared distribution, never the actual hidden test goal.
- **Novelty vs. closest in-domain work**: Dual control, Bayes-adaptive planning and goal-directed exploration already optimize information plus state effects. Only a distinctive amortization or compositional cost operation could be new; adding future utility alone is explicitly insufficient.
- **Main risk**: Existing Bayes-adaptive control already solves the stated objective, and a new toy makes the method appear necessary by weakening baselines.
