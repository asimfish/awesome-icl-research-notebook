# Shared formal setting and controls

This setting is a known partially observable/adaptive control problem, not a novelty claim. It makes forty algorithm candidates comparable.

A deployment world has fixed reusable relation parameters Θ (skill preconditions, consequences and interactions) and possibly time-varying execution/observation nuisance η_t. The controller observes o_t, executes an ordinary command a_t, and receives observable consequence y_t, including actual failures. It receives neither Θ nor an eligibility vector or hidden failure-cause label. The factual history is H_t=(o_0,a_0,y_0,...,o_t). A public goal g is a predicate/program evaluated by an independent measurement interface.

Frozen pretrained parameters φ implement memory update m_{t+1}=U_φ(m_t,o_t,a_t,y_t) and decisions π_φ(a|o_t,g,m_t). External memory, a posterior, a cache or a particle set may update at deployment; neural parameter optimization does not. Any privileged offline supervision is disclosed and given to competing learned baselines under the same budget. Generated continuation branches are offline training/model computations, never extra factual deployment evidence.

A later query g′ is selected after collecting H_t but before feedback from executing g′. Its first decision therefore tests reuse of prior consequences rather than recognition of g′ from a solved demonstration. We distinguish an unseen goal description, unseen goal composition, unseen action binding, unseen latent relation and a shifted nuisance channel. They are separate evaluation axes, not one undifferentiated 'OOD' split.

An exact finite reference uses b_t(Θ,η)=p(Θ,η|H_t) and the same legal observation likelihood, action set, goal prior and total physical costs. It is a correctness reference, not a scalable target to weaken. If equal-budget standard inference or planning achieves the entire claimed result, the proposal must become an efficiency/approximation contribution with measured tradeoffs or lose its algorithm claim.

Physical costs include preparation, diagnostic commands, failed commands, restoration and resets; computation includes all model likelihood evaluations, continuation tests, catalogue construction, replay, fallback and training supervision. Memory includes catalogue/partition metadata and retained ancestry, not only visible latent vectors. Fixed-particle comparisons must also report bytes and likelihood-call counts.

There are two distinct memory comparisons. Present-query adequacy compares π(g,m(H)) with the full-history decision. Future-update adequacy compares π(g′,U(m(H),e)) with the full-history decision after the SAME legal next observation e. The latter asks whether compression preserves information relevant to learning, but PSR, bisimulation and Bayesian filtering are direct priors; the distinction itself is not a new algorithm.

Minimum evaluation: (1) no-feedback first attempt, (2) causal adaptation on own feedback, (3) first attempt on an unexecuted later goal, (4) irrelevant-goal regressions, (5) reset-memory control, (6) standard update/inference controls with equal records and compute. Matched records isolate representation effects; own-policy closed loops then measure practical acquisition effects. Do not combine their estimates or call replay a live robot experiment.

Candidate acceptance requires a precise operation, a meaningful same-information failure of a named practical reference, and a falsifiable equal-budget comparison. New findings about an existing method can motivate a paper, but a symbolic oracle construction alone cannot establish robotic impact or a new learned algorithm.
