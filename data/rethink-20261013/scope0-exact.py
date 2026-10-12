"""Finite reference calculation; no learned policy or robot execution."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def observation_likelihood(rule, events):
    return int(all(int(clamped == 1 or rule[command] == 0) == outcome
                   for clamped, command, outcome in events))


def prior(rule, kind):
    if kind == "independent_uniform":
        return F(1, 8)
    if kind == "hierarchical_0.9_agreement":
        total = F(0)
        for latent in (0, 1):
            weight = F(1, 2)
            for bit in rule:
                weight *= F(9, 10) if bit == latent else F(1, 10)
            total += weight
        return total
    raise ValueError(kind)


def calculate():
    models = list(product((0, 1), repeat=3))
    histories = {
        "empty": [],
        "source_correction": [(0, 0, 0), (1, 0, 1)],
        "second_agrees": [(0, 0, 0), (1, 0, 1), (0, 1, 0), (1, 1, 1)],
        "second_differs": [(0, 0, 0), (1, 0, 1), (0, 1, 1)],
    }
    rows = []
    for kind in ("independent_uniform", "hierarchical_0.9_agreement"):
        assert sum(prior(rule, kind) for rule in models) == 1
        for name, events in histories.items():
            assert all(command != 2 for _, command, _ in events)
            weights = [prior(rule, kind) * observation_likelihood(rule, events)
                       for rule in models]
            normalizer = sum(weights)
            assert normalizer > 0
            posterior = [weight / normalizer for weight in weights]
            assert sum(posterior) == 1
            marginal = sum(p for rule, p in zip(models, posterior) if rule[2] == 1)
            compatible = [rule for rule, p in zip(models, posterior) if p > 0]
            assert {rule[2] for rule in compatible} == {0, 1}
            if events:
                assert all(rule[0] == 1 for rule in compatible)
            expected_count = {"empty": 8, "source_correction": 4,
                              "second_agrees": 2, "second_differs": 2}[name]
            assert len(compatible) == expected_count
            expected_marginal = (F(1, 2) if kind == "independent_uniform" else
                                 {"empty": F(1, 2), "source_correction": F(41, 50),
                                  "second_agrees": F(73, 82), "second_differs": F(1, 2)}[name])
            assert marginal == expected_marginal
            rows.append({
                "prior": kind, "history": name, "events": events,
                "compatible_model_count": len(compatible),
                "unexecuted_a2_requires_clamp": str(marginal),
                "unexecuted_a2_requires_clamp_decimal": float(marginal),
                "joint_posterior": [{"rule": rule, "probability": str(p)}
                                    for rule, p in zip(models, posterior)],
            })
    return {"diagnostic": "SCOPE0", "rows": rows, "enumerated_models": 8,
            "model_history_prior_scores": 64, "posterior_weight_entries": 64,
            "reference_model_only": True, "neural_training_runs": 0,
            "policy_rollouts": 0, "physics_executions": 0, "robot_episodes": 0,
            "new_algorithm_established": False}


if __name__ == "__main__":
    output = Path(__file__).with_name("scope0-results.json")
    assert not output.exists(), "Version existing results before rerun"
    payload = calculate()
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in payload.items() if key != "rows"}))
