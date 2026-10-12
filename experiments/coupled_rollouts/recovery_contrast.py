"""Exact identification diagnostic, not a trained or physical robot algorithm."""
import argparse
import csv
import json
from pathlib import Path
from time import perf_counter

import numpy as np


def sigmoid(value):
    return np.exp(-np.logaddexp(0., -np.asarray(value, dtype=float)))


def discordant_masses(eta, effect, second_nuisance_shift=0., shared_uniform=False):
    """Return P(0,1),P(1,0); marginal means alone do not specify these."""
    p0, p1 = float(sigmoid(eta)), float(sigmoid(eta+effect+second_nuisance_shift))
    if shared_uniform:
        return max(p1-p0, 0.), max(p0-p1, 0.)
    return (1-p0)*p1, p0*(1-p1)


def orientation(m01, m10, s0, s1, r01=1., r10=1.):
    """Full analyzed-sample masses; a zero orientation has no finite offset."""
    values = np.array([m01, m10, s0, s1, r01, r10], dtype=float)
    if not np.all(np.isfinite(values)) or np.any(values < 0) or np.any(values > 1):
        raise ValueError("masses and acquisition/retention probabilities must be in [0,1]")
    a, b = m01*s0*r01, m10*s1*r10
    if a+b == 0:
        return None, 0., 0.
    q = a/(a+b)
    return q, a+b, (a+b)*q*(1-q)


def offset(s0, s1, r01=1., r10=1.):
    values = np.asarray([s0, s1, r01, r10], dtype=float)
    if not np.all(np.isfinite(values)) or np.any(values <= 0) or np.any(values > 1):
        raise ValueError("both orientations need positive reconstructible inclusion probabilities")
    return float(np.log(s0)+np.log(r01)-np.log(s1)-np.log(r10))


def cell(effect, eta, s1):
    m01, m10 = discordant_masses(eta, effect)
    q, mass, info = orientation(m01, m10, 1., s1)
    identified = s1 > 0
    predicted = float(sigmoid(effect+offset(1., s1))) if identified else None
    naive = float(sigmoid(effect))
    p0 = float(sigmoid(eta))
    return dict(effect=effect, eta=eta, audit_success_probability=s1,
                observed_orientation_probability=q, analyzed_discordance_mass=mass,
                conditional_information_per_first_attempt=info,
                expected_option_executions=1+(1-p0)+p0*s1,
                identified_by_conditional_orientation=identified,
                corrected_prediction=predicted,
                corrected_error=abs(q-predicted) if identified else None,
                uncorrected_error=abs(q-naive) if q is not None else None,
                conditional_score_at_truth=q-predicted if identified else None)


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    start = perf_counter()
    cells = [cell(d, eta, s) for d in (-2., 0., 2.) for eta in (-4., 0., 4.)
             for s in (0., .05, .2, 1.)]
    mixtures = []
    for d in (-2., 0., 2.):
        masses = [discordant_masses(eta, d) for eta in (-6., -2., 1., 5.)]
        m01, m10 = np.array([.1, .2, .3, .4]) @ np.array(masses)
        q, mass, info = orientation(m01, m10, 1., .2)
        prediction = float(sigmoid(d+offset(1., .2)))
        mixtures.append(dict(effect=d, eta_values=[-6., -2., 1., 5.],
                             eta_weights=[.1, .2, .3, .4], success_audit=.2,
                             observed_orientation_probability=q,
                             predicted_orientation_probability=prediction,
                             error=abs(q-prediction), discordance_mass=mass,
                             conditional_information_per_first_attempt=info))
    violations = []
    # All scenarios fixed before execution; these are failures of assumptions.
    for name, effect, drift, shared, r01, r10 in (
            ("shared_uniform_innovations", 2., 0., True, 1., 1.),
            ("nuisance_changes_with_preparation", 0., 1., False, 1., 1.),
            ("outcome_dependent_retention", 0., 0., False, 1., .3)):
        m01, m10 = discordant_masses(0., effect, drift, shared)
        q, mass, info = orientation(m01, m10, 1., .2, r01, r10)
        incomplete_prediction = float(sigmoid(effect+offset(1., .2)))
        full_retention_prediction = float(sigmoid(effect+offset(1., .2, r01, r10)))
        violations.append(dict(scenario=name, true_task_effect=effect,
                               nuisance_drift=drift, shared_uniform=shared,
                               retention01=r01, retention10=r10,
                               observed_orientation_probability=q,
                               incomplete_model_prediction=incomplete_prediction,
                               incomplete_model_error=abs(q-incomplete_prediction),
                               full_retention_offset_prediction=full_retention_prediction,
                               full_retention_offset_error=abs(q-full_retention_prediction),
                               discordance_mass=mass,
                               analyzed_mass_times_orientation_variance=info))
    supported = [c for c in cells if c['identified_by_conditional_orientation']]
    result = dict(scope="exact conditional-identification diagnostic; classical likelihood",
                  grid_cells=len(cells), positive_support_cells=len(supported),
                  failure_only_cells=len(cells)-len(supported), nuisance_mixture_cells=len(mixtures),
                  predefined_assumption_violation_cells=len(violations),
                  maximum_supported_error=max(c['corrected_error'] for c in supported),
                  maximum_mixture_error=max(c['error'] for c in mixtures),
                  maximum_uncorrected_positive_support_error=max(c['uncorrected_error'] for c in supported),
                  all_failure_only_information_zero=all(c['conditional_information_per_first_attempt']==0
                                                        for c in cells if not c['identified_by_conditional_orientation']),
                  cells=cells, mixtures=mixtures, violations=violations,
                  runtime_seconds=perf_counter()-start,
                  trained_models=0, physical_episodes=0, sampled_episodes=0,
                  limits=["Exact chosen Bernoulli model, not physical validity or algorithm novelty",
                          "Failure-only nonidentification applies to this conditional likelihood",
                          "Success odds contrast does not certify a necessary prerequisite",
                          "No unseen-goal policy or empirical nuisance-robust transfer result",
                          "Information and option counts are exact model expectations, not measured simulator work",
                          "Violation-row mass times orientation variance is not Fisher information in a misspecified model"])
    with (output/'cells.csv').open('w') as f:
        w=csv.DictWriter(f, fieldnames=list(cells[0])); w.writeheader(); w.writerows(cells)
    (output/'result.json').write_text(json.dumps(result, indent=2, allow_nan=False))
    print(json.dumps({k:v for k,v in result.items() if k not in ('cells','mixtures','violations')}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path, required=True)
    run(p.parse_args().output)
