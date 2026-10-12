# X0-P physical-control result

The prospectively specified full grid completed once, after the fresh code Pass. Normal /usr/bin/python3, MuJoCo3.3.7, NumPy2.2.6, one CPU process/two threads, no rendering or environment changes. 12,000 primitives; 12,000 resets; 1,440,000 MuJoCo steps; runtime5.7262646s. No learned robot controller, policy updates, GPU or hardware episodes.

At force mean6N, target371/1500→1163/1500, control755/1500→1392/1500. Target-minus-control logit shift posterior mean−.1934852,95% posterior interval[−.4736153,.0836455]. At8N, target937→1436, control1284→1486, each/1500; difference mean−.2805498, interval[−.9176917,.3184862]. Both intervals include zero. Neither validates nor rejects parallel logit response for this control pair. No threshold retuning, repeat grid or significance selection.

Intervals are coordinate-wise Jeffreys-binomial posterior summaries from10,000 draws, not frequentist confidence intervals or simultaneous guarantees. The8N control has only14failures atlowfriction, so high saturation reduces precision. Prior smoothing never creates conditional-outcome support.

Task-inert here means the same task conditions and force process, different distance success predicate. It is a sliding primitive with direct friction configuration, not a demonstrated correction or feasible robot preparation. The result cannot be a task-relation-learning or new-goal-transfer result. Counts and all trials remain in results-physics-control/result.json and trials.csv.

Decision: retain the mathematical misspecification counterexample; leave physical-control validity unresolved. Do not promote this evidence to X1/X2, a relation graph or a new algorithm claim. Further work needs a concrete matched control construction and cost-based admission criterion, not merely more neural training.
