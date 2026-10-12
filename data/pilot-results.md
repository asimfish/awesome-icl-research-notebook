# Learned-policy cycle — 12 October2026

15 main checkpoints (3 seeds per condition), frozen-weight evaluation, CPU only. Symbolic dependency operations; no robot episodes. Scientific status REVISE; same-family review provisional.

# First learned-policy pilot results

Exploratory dependency-operation mechanism pilot; no robot evidence.

| Training query | Evaluation query | Full support success | Empty support success | Support gain [rule95% CI] | First-action support gain |
|---|---|---|---|---|---|
| current-correction | current-correction | 80.70% ± 0.98 seed SD | 74.54% | +6.15 pp [4.69,7.75] | +27.31 pp |
| current-correction | same-goal-reset | 42.64% ± 3.29 seed SD | 64.71% | -22.07 pp [-24.97,-19.17] | -19.82 pp |
| current-correction | different-goal-reset | 42.74% ± 1.98 seed SD | 64.52% | -21.78 pp [-24.61,-18.91] | -23.60 pp |
| same-goal-reset | current-correction | 28.45% ± 0.34 seed SD | 35.71% | -7.26 pp [-8.69,-5.86] | -13.80 pp |
| same-goal-reset | same-goal-reset | 14.19% ± 1.07 seed SD | 17.29% | -3.09 pp [-4.36,-1.82] | +25.29 pp |
| same-goal-reset | different-goal-reset | 13.67% ± 0.59 seed SD | 18.13% | -4.46 pp [-5.86,-3.09] | +23.01 pp |
| different-goal-reset | current-correction | 27.12% ± 0.15 seed SD | 35.58% | -8.46 pp [-9.96,-6.90] | -14.65 pp |
| different-goal-reset | same-goal-reset | 12.53% ± 0.72 seed SD | 16.54% | -4.00 pp [-5.37,-2.73] | +26.33 pp |
| different-goal-reset | different-goal-reset | 13.74% ± 0.37 seed SD | 17.51% | -3.78 pp [-5.08,-2.44] | +27.47 pp |

Intervals bootstrap independent rules, conditional on the three checkpoints. Seed effects are listed separately in summary.json/seed_metrics.csv; trials are paired and do not count as independent robots.

Actual main runs:9; training updates:5400; evaluation branches:55296; independent held-out graphs:128; total training seconds:38.851.

STOP target fractions: current-correction: 23.91%; same-goal-reset: 0.00%; different-goal-reset: 0.00%.

Initially empty support still allows feedback from the query itself. Other-world/irrelevant-history stress is separate. A query-distribution advantage by itself does not establish algorithmic novelty or relation recovery.

# Public-state mask diagnostic

Known action mask, identical for all models; no training, no new algorithm.

| Training arrangement | Mask | Retained support completion | Empty support completion | Retained support repeated-done commands | Retained support blocked commands |
|---|---|---|---|---|---|
| current-correction | False | 42.74% | 64.52% | 0.00 | 2.33 |
| current-correction | True | 42.74% | 64.52% | 0.00 | 2.33 |
| same-goal-reset | False | 13.67% | 18.13% | 8.58 | 0.77 |
| same-goal-reset | True | 88.35% | 92.74% | 0.00 | 2.43 |
| different-goal-reset | False | 13.74% | 17.51% | 8.66 | 0.77 |
| different-goal-reset | True | 86.78% | 90.20% | 0.00 | 2.63 |

# Matched-history query-state pilot

Exploratory dependency-operation mechanism pilot; no robot evidence.

| Training query | Evaluation query | Full support success | Empty support success | Support gain [rule95% CI] | First-action support gain |
|---|---|---|---|---|---|
| covered-query | current-correction | 98.60% ± 0.74 seed SD | 98.54% | +0.07 pp [-0.55,0.65] | +9.54 pp |
| covered-query | same-goal-reset | 98.27% ± 0.63 seed SD | 98.01% | +0.26 pp [-0.62,1.21] | +19.43 pp |
| covered-query | different-goal-reset | 98.18% ± 0.56 seed SD | 97.79% | +0.39 pp [-0.65,1.40] | +24.58 pp |
| zero-query | current-correction | 25.00% ± 0.26 seed SD | 34.86% | -9.86 pp [-11.49,-8.30] | -17.02 pp |
| zero-query | same-goal-reset | 8.76% ± 0.39 seed SD | 11.65% | -2.90 pp [-3.97,-1.89] | +28.74 pp |
| zero-query | different-goal-reset | 8.04% ± 0.44 seed SD | 9.77% | -1.73 pp [-2.70,-0.85] | +31.45 pp |

Intervals bootstrap independent rules, conditional on the three checkpoints. Seed effects are listed separately in summary.json/seed_metrics.csv; trials are paired and do not count as independent robots.

Actual main runs:6; training updates:3600; evaluation branches:36864; independent held-out graphs:128; total training seconds:40.539.

STOP target fractions: covered-query: 0.00%; zero-query: 0.00%.

Initially empty support still allows feedback from the query itself. Other-world/irrelevant-history stress is separate. A query-distribution advantage by itself does not establish algorithmic novelty or relation recovery.

## Conditional command costs

With covered query states, retained experience reduces all-query capped commands from6.336 to5.315; paired savings1.020, rule95% interval[0.890,1.149]. At the original12-command endpoint, historical-support completion gain remainsunestablished. The full1–12curve is exploratory; no favorable deadline selected. Prior collection cost is excluded.

## Prospective fresh-cohort cost confirmation

Frozen same3checkpoints;256freshclosure-disjoint rules,12288pairedbranches, newmodeltraining0. Command savings 1.0107, rule95% interval[0.9221964518229167, 1.0968465169270833]. Gate True. This confirms only conditional command efficiency; original completion hypothesis remainsFAILED. Mean initialsupport acquisition is 5.890commands, so collecting supportsolelyforonefuturequery has no establishednetbenefit.

[Full aggregates](learned-pilot.json) · [English paper draft](paper-draft.md) · [Chinese story](paper-story-zh.md) · [Paper PDF](../assets/paper-draft.pdf)

DPT querysupervision is a directprior; this is not anofficialDPTreproduction ornewmemoryalgorithm. No autonomous collection, causalgraph recovery, necessity of changed-goal training, verifierlearning, robotics orsim-to-real claim follows. Preserved earlyA3/U3 records are excluded from alllearnedpilotcounts.
