# Direct-prior body audit for the three refinement priorities

As of2026-10-13. These are concrete occupied operations, not an exhaustive novelty certification. Root reads are indicated separately from delegated readers. No numerical paper outcomes enter idea generation.

## Optimized Auxiliary Particle Filters (Branchini and Elvira, UAI2021)

Verified publisher metadata and arXiv2011.09317. Root read §2.2, §3.1–3.4, Algorithm1, Eqs2–12 and theorem statement. [Primary full text](https://proceedings.mlr.press/v161/branchini21a/branchini21a.pdf).

The standard APF delays resampling until the actual incoming observation is available; ancestor weights use that observation's likelihood at predicted particle centers. Its correction divides by the auxiliary likelihood already used to select parents. Thus, comparing C15 only with eager bootstrap resampling would omit an important reference. The authors explicitly note that fully adapted APF has only local/one-step optimality.

OAPF uses a generic mixture proposal ψ=Σ_k λ_k q_k, decoupling kernel count from particle count. Eq6 weights each new sample using the approximate predictive mixture times actual observation likelihood divided by the full proposal mixture. Eq12 optimizes nonnegative mixture coefficients by a generic discrepancy between proposal values and approximate posterior at evaluation points; their implementation uses NNLS. Standard regularity conditions support unbiased normalizing-constant estimates and consistency, not an arbitrary finite-particle decision guarantee.

**Overlap:** optimized particle allocation/proposals, importance-correct weighting, measurement-aware lookahead and explicit computational degrees of freedom are already present. **Bounded distinction:** C15 asks to preserve future feedback-conditioned goal readouts before that future observation and goal occur, rather than matching the current filtering density. This is a changed target, not yet a proven non-obvious algorithm. Both can be combined; no impossibility claim against OAPF.

## Stratification and Optimal Resampling for SMC (Li, Wang, Deng, Liu)

Verified arXiv2004.01975; root read §2.3–2.4, §3, Theorems1–4 and the stated scope of multidimensional ordering. [Primary full text](https://arxiv.org/html/2004.01975).

The paper describes valid resampling matrices and alternative losses between original/resampled empirical measures. In one dimension ordered stratified resampling minimizes conditional variance and energy distance. Critically, for a target E[φ(X)], it explicitly orders particles by φ and then stratifies, minimizing variance for that integrand. Hilbert ordering bounds assume Lipschitz functions in a bounded Euclidean space; these bounds cannot be transferred to arbitrary robot-task fingerprints without establishing their conditions.

**Overlap:** task/test-aware resampling geometry and variance reduction are already natural operations. **Bounded distinction:** preserving a family of normalized post-feedback decision ratios is a different target family, but applying a different integrand to the known procedure is not automatically an algorithm contribution. The strongest comparison must use the same predicted L and LQ features, not force the baseline to sort only raw latent coordinates.

## Preserving Modes and Messages via Diverse Particle Selection (Pacheco et al., ICML2014)

Verified PMLR32(2):1152–1160. Root read §2.1–2.3, §3.1–3.2 and the message foundation/selection construction. [Primary full text](https://proceedings.mlr.press/v32/pacheco14.pdf).

D-PMP augments each particle set from N to αN using data-driven, neighbor and random-walk proposals, computes max-product messages, and selects N hypotheses to minimize message error on the augmented neighboring support. The integer-program/greedy selection goal produces diversity through message preservation rather than a manually tuned parameter distance. It is max-product mode inference: Eq6 uses a maximum, and §2.2 explicitly does not need sum-product importance weights.

**Overlap:** retain hypotheses according to the inference operation they must support after selection, not their current rank or parameter distance. **Important limit:** this is not an exact duplicate of mass-preserving Bayesian filtering or stochastic correction-conditioned expected-cost decisions. Moving from max to sum is a narrow candidate adaptation, not sufficient by itself to establish novelty.

## Particle-based adaptive-lag online marginal smoothing (Alenlöv and Olsson)

Verified arXiv1812.10939v2,2019-06-24; first submission2018-12-28. Root read §III.A, §IV.B–IV.C, Eqs3–5 and14–16, active-set stopping construction. [Primary full text](https://arxiv.org/html/1812.10939).

A bank of marginal estimators is recursively propagated using backward smoothing kernels. Fixed-lag methods have a bias/ancestry-variance tradeoff. The adaptive scheme evolves each estimator until a conditional/sample variance criterion is below tolerance; the estimator then exits the active set. The PaRIS-style random backward samples reduce the update cost relative to the full quadratic kernel sum. Forgetting/mixing assumptions justify the stopping interpretation; bounded asymptotic demands are not an arbitrary hard byte guarantee in any nonmixing model.

**Overlap:** data-dependent stopping of retrospective updates already precedes C12. **Bounded distinction:** C12 would need to choose which raw ambiguous event explanations remain reversible under a hard memory budget because of their effect on new-goal decisions, rather than merely freezing a settled marginal expectation. That specific commit/eviction rule is not yet fully specified or demonstrated. Delayed packet assimilation and logical evidence reinterpretation are distinct interfaces; neither distinction certifies novelty.

## Joint conclusion

C15 and C21 have specific approximation targets worth studying; C12 has an implementable but underspecified commitment problem. All remain **PROCEED WITH CAUTION for refinement**, not approved new methods. No named source here contains the full robot system result, so the novelty audit does not assert ABANDON on proximity alone. The forty-candidate triage can reject a draft's current sufficiency without proving that its entire research neighborhood is occupied.

The proposal-blind derivation independently reconstructs response-stratified, mass-correct SMC and update-closed PSR using standard techniques. This sharply limits claims based only on combining those parts. A useful next result must identify a concrete cost/accuracy advantage against same-test adaptive inference and establish that a deployed learned controller actually exhibits the failure.
