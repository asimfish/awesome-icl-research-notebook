"""Exact finite diagnostic of an established-identity estimator specialization.

Not a robot episode, learned collector, novelty certificate, or runtime speedup.
"""
import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import numpy as np


@dataclass
class Leaf:
    probability: float
    commands: int
    full_weight: float
    prefix_control: float
    balanced_target: float
    balanced_control: float


@dataclass
class CoupledLeaf:
    probability: float
    retained_commands: int
    erased_commands: int
    transition_calls: int
    scoring_calls: int


def policy(prior, epsilon=.1):
    return np.array([(1-epsilon)*prior+epsilon/2,
                     (1-epsilon)*(1-prior)+epsilon/2])


def blocked_posterior(prior, action, reliability):
    likelihood0 = 1-reliability if action == 0 else 1.
    likelihood1 = 1-reliability if action == 1 else 1.
    denominator = prior*likelihood0+(1-prior)*likelihood1
    if denominator == 0:
        raise ValueError("conditioning on an impossible blocked observation")
    return prior*likelihood0/denominator


def leaves(rule, informative, reliability, horizon, epsilon=.1):
    """Enumerate retained paths, scoring erased policy on identical own receipts."""
    initial = float(rule == 0) if informative else .5
    output = []

    def visit(prior, erased, probability, weight, prefix_control, target_mix, control_mix, step):
        retained_prob, erased_prob = policy(prior, epsilon), policy(erased, epsilon)
        # Each command costs 1 BEFORE its action; this needs the previous prefix
        # ratio. Using the current-action ratio here is also unbiased but wastes
        # randomness; including future ratios needlessly worsens variance.
        next_control = prefix_control+weight
        # Trajectory proposal is .5*q_retained + .5*q_erased (one component
        # chosen ONCE per query), not a fresh per-step policy mixture.
        next_target_mix = target_mix+2/(1+weight)
        next_control_mix = control_mix+2*weight/(1+weight)
        for action in range(2):
            next_weight = weight*erased_prob[action]/retained_prob[action]
            action_probability = probability*retained_prob[action]
            success_probability = reliability if action == rule else 0.
            if success_probability:
                output.append(Leaf(action_probability*success_probability, step+1,
                                   next_weight, next_control, next_target_mix, next_control_mix))
            blocked_probability = 1-success_probability
            if blocked_probability:
                blocked_mass = action_probability*blocked_probability
                if step+1 == horizon:
                    output.append(Leaf(blocked_mass, horizon, next_weight, next_control,
                                       next_target_mix, next_control_mix))
                else:
                    visit(blocked_posterior(prior, action, reliability),
                          blocked_posterior(erased, action, reliability), blocked_mass,
                          next_weight, next_control, next_target_mix, next_control_mix, step+1)

    visit(initial, .5, 1., 1., 0., 0., 0., 0)
    if not np.isclose(sum(x.probability for x in output), 1., atol=1e-12, rtol=0):
        raise RuntimeError("query probability mass not normalized")
    return output


def moments(probabilities, values):
    mean = float(probabilities @ values)
    variance = float(probabilities @ ((values-mean)**2))
    return mean, variance


def coupled_leaves(rule, informative, reliability, horizon, epsilon=.1):
    """Valid shared-uniform actions/motor outcomes, own feedback per branch.

    Same-state/action/randomness transitions and identical belief-input policy
    evaluations are cached. This is an established CRN comparator, not new.
    """
    output = []
    initial = float(rule == 0) if informative else .5

    def visit(left, right, left_done, right_done, mass, lc, rc, calls, forwards, step):
        if left_done and right_done or step == horizon:
            output.append(CoupledLeaf(mass, lc, rc, calls, forwards)); return
        lp, rp = policy(left, epsilon), policy(right, epsilon)
        thresholds = [0., 1.]
        if not left_done: thresholds.append(lp[0])
        if not right_done: thresholds.append(rp[0])
        edges = sorted(set(thresholds))
        for lower, upper in zip(edges[:-1], edges[1:]):
            u = (lower+upper)/2
            la = int(u >= lp[0]) if not left_done else None
            ra = int(u >= rp[0]) if not right_done else None
            active = [x for x in (la, ra) if x is not None]
            next_calls = calls+len(set(active))
            evaluations = 1 if left_done or right_done or left == right else 2
            motor_edges = [0., reliability, 1.] if rule in active else [0., 1.]
            for vlo, vhi in zip(motor_edges[:-1], motor_edges[1:]):
                v = (vlo+vhi)/2
                ls = not left_done and la == rule and v < reliability
                rs = not right_done and ra == rule and v < reliability
                next_left = left if left_done or ls else blocked_posterior(left, la, reliability)
                next_right = right if right_done or rs else blocked_posterior(right, ra, reliability)
                visit(next_left, next_right, left_done or ls, right_done or rs,
                      mass*(upper-lower)*(vhi-vlo), lc+int(not left_done),
                      rc+int(not right_done), next_calls, forwards+evaluations, step+1)

    visit(initial, .5, False, False, 1., 0, 0, 0, 0, 0)
    if not np.isclose(sum(x.probability for x in output), 1., atol=1e-12, rtol=0):
        raise RuntimeError("coupled path mass is not normalized")
    return output


def cell(reliability, horizon, diagnostic_cost, acquisition_probability=.5):
    p = acquisition_probability
    retained = {(r, z): leaves(z, r == 1, reliability, horizon) for r in range(2) for z in range(2)}
    erased = {z: leaves(z, False, reliability, horizon) for z in range(2)}
    costs = [np.mean([sum(x.probability*x.commands for x in retained[r, z]) for z in range(2)])
             +1+diagnostic_cost*r for r in range(2)]
    true_gradient = p*(1-p)*(costs[1]-costs[0])
    rows = []
    identity_errors = []
    for r in range(2):
        for z in range(2):
            empty_value = sum(x.probability*x.commands for x in erased[z])
            group = retained[r, z]
            identity_errors.extend([
                abs(sum(x.probability*x.full_weight for x in group)-1),
                abs(sum(x.probability*x.commands*x.full_weight for x in group)-empty_value),
                abs(sum(x.probability*x.prefix_control for x in group)-empty_value)])
            mixture_mass = np.array([x.probability*(1+x.full_weight)/2 for x in group])
            ret_value = sum(x.probability*x.commands for x in group)
            identity_errors.extend([
                abs(mixture_mass.sum()-1),
                abs(sum(m*x.balanced_target for m, x in zip(mixture_mass, group))-ret_value),
                abs(sum(m*x.balanced_control for m, x in zip(mixture_mass, group))-empty_value)])
            for leaf in group:
                mass = .5*(p if r else 1-p)*leaf.probability
                rows.append([mass, r-p, 1+diagnostic_cost*r+leaf.commands,
                             leaf.full_weight*leaf.commands, leaf.prefix_control,
                             leaf.commands, 1+diagnostic_cost*r, leaf.commands*(1+r)])
    data = np.array(rows)
    mass, score, total, full, prefix, commands, acquisition_cost, extra_scoring = data.T
    target = score*total
    results = []

    def record(name, baseline_control=None, oracle=False, separate=False, coupled=False, balanced=False, target_only=False):
        if balanced:
            expanded = []
            for r in range(2):
                for z in range(2):
                    for leaf in retained[r, z]:
                        joint = .5*(p if r else 1-p)*leaf.probability*(1+leaf.full_weight)/2
                        expanded.append([joint, r-p, 1+diagnostic_cost*r+leaf.balanced_target,
                                         leaf.balanced_control, leaf.commands,
                                         1+diagnostic_cost*r, leaf.commands*(1+r)])
            probability, s, reward, control, work, acq_cost, forward_work = np.array(expanded).T
            response = s*reward
        elif coupled:
            expanded = []
            for r in range(2):
                for z in range(2):
                    for leaf in coupled_leaves(z, r == 1, reliability, horizon):
                        joint = .5*(p if r else 1-p)*leaf.probability
                        expanded.append([joint, r-p, 1+diagnostic_cost*r+leaf.retained_commands,
                                         leaf.erased_commands, leaf.transition_calls,
                                         1+diagnostic_cost*r, leaf.scoring_calls,
                                         leaf.retained_commands+leaf.erased_commands])
            probability, s, reward, control, work, acq_cost, forward_work, issued = np.array(expanded).T
            response = s*reward
        elif separate:
            expanded = []
            for r in range(2):
                for z in range(2):
                    for left in retained[r, z]:
                        for right in erased[z]:
                            joint = .5*(p if r else 1-p)*left.probability*right.probability
                            expanded.append([joint, r-p, 1+diagnostic_cost*r+left.commands,
                                             right.commands, left.commands+right.commands,
                                             1+diagnostic_cost*r])
            probability, s, reward, control, work, acq_cost = np.array(expanded).T
            response = s*reward
            forward_work = work
            issued = work
        else:
            probability, s, response = mass, score, target
            control = baseline_control
            work, acq_cost = commands, acquisition_cost
            forward_work = commands if control is None else extra_scoring
            issued = work
        if balanced:
            issued = work
        if name == "raw":
            estimate, coefficients = response, []
        elif name == "optimal-scalar" or target_only:
            coefficient = float((probability*s*response).sum()/(probability*s*s).sum())
            estimate, coefficients = response-coefficient*s, [coefficient]
        elif oracle:
            design = np.stack([s, s*control], axis=1)
            gram = design.T @ (probability[:, None]*design)
            rhs = design.T @ (probability*response)
            coefficients = np.linalg.lstsq(gram, rhs, rcond=None)[0]
            estimate = response-design @ coefficients
            coefficients = coefficients.tolist()
        else:
            estimate, coefficients = response-s*control, [0., 1.]
        mean, variance = moments(probability, estimate)
        if abs(mean-true_gradient) > 1e-10:
            raise RuntimeError(f"biased estimator {name}: {mean} != {true_gradient}")
        if control is not None and abs(float(probability @ (s*control))) > 1e-10:
            raise RuntimeError("counterfactual control has nonzero acquisition-score expectation")
        environment = float(probability @ (work+acq_cost))
        forwards = float(probability @ forward_work)
        results.append({"method": name, "gradient_mean": mean, "true_gradient": true_gradient,
                        "gradient_variance": variance,
                        "query_commands_expected": float(probability @ issued),
                        "simulator_transition_calls_expected": float(probability @ work),
                        "environment_cost_units_expected": environment,
                        "query_scoring_forwards_expected": forwards,
                        "variance_times_environment_work": variance*environment,
                        "variance_times_scoring_work": variance*forwards,
                        "coefficient_status": "exact oracle" if oracle or name == "optimal-scalar" or target_only else "fixed",
                        "coefficients": coefficients})
        for r in (0, 1):
            chosen = s > 0 if r else s < 0
            conditional = probability[chosen]/probability[chosen].sum()
            cm, cv = moments(conditional, estimate[chosen])
            results[-1][f"gradient_mean_given_r{r}"] = cm
            results[-1][f"gradient_variance_given_r{r}"] = cv

    record("raw")
    record("optimal-scalar")
    record("full-is-fixed", full)
    record("prefix-is-fixed", prefix)
    record("full-is-oracle", full, oracle=True)
    record("prefix-is-oracle", prefix, oracle=True)
    record("independent-erased-oracle", oracle=True, separate=True)
    record("coupled-erased-oracle", oracle=True, coupled=True)
    record("balanced-target-optimal-scalar", balanced=True, target_only=True)
    record("balanced-prefix-fixed", balanced=True)
    record("balanced-prefix-oracle", balanced=True, oracle=True)
    return {"reliability": reliability, "horizon": horizon, "diagnostic_cost": diagnostic_cost,
            "acquisition_probability": p, "mean_cost_no_information": float(costs[0]),
            "mean_cost_information": float(costs[1]), "true_gradient": float(true_gradient),
            "max_identity_error": max(identity_errors), "methods": results}


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    start = perf_counter()
    cells = [cell(q, t, .1, p) for q in (.5, .8, .95) for t in (2, 4, 6) for p in (.2, .5, .8)]
    report = {"scope": "exact constructed option-level estimator diagnostic",
              "cells": cells, "grid_cells": len(cells), "enumeration_seconds": perf_counter()-start,
              "training_runs": 0, "real_environment_rollouts": 0, "robot_episodes": 0,
              "limits": ["Optimal coefficients are exact oracle diagnostics, not a learned estimator",
                         "Work proxies are conceptual counts, not measured finite-budget or walltime efficiency",
                         "Frozen Bayesian consumer is not the previous learned history policy",
                         "Coupled erased comparator uses exact own-belief CRN and transition/policy caches",
                         "No claim of new IS/FC-PG identity or verified algorithm priority"]}
    (output/"result.json").write_text(json.dumps(report, indent=2))
    rows = [{"reliability": c["reliability"], "horizon": c["horizon"],
             "diagnostic_cost": c["diagnostic_cost"], "acquisition_probability": c["acquisition_probability"],
             **m} for c in cells for m in c["methods"]]
    with (output/"estimators.csv").open("w") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    print(json.dumps({"grid_cells": len(cells), "max_identity_error": max(c["max_identity_error"] for c in cells),
                      "enumeration_seconds": report["enumeration_seconds"]}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); run(args.output)
