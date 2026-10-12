"""Predeclared finite marginal diagnostic, including construction overhead."""
import argparse
import csv
import json
from pathlib import Path
from time import perf_counter

import numpy as np
from .coupling import sample, solve_subset, optimal_uniform_order


METHODS = ("independent", "uniform", "ordered-uniform", "gumbel", "list", "subset-lp")


def run(output, cases=8, draws=2000):
    output.mkdir(parents=True, exist_ok=False)
    rng = np.random.default_rng(6512)
    rows = []
    for k in (4, 16, 31):
        for case in range(cases):
            alpha = .2 if case % 2 == 0 else 2.
            p = rng.dirichlet(np.full(6, alpha), size=k)
            scores = rng.normal(size=p.shape)
            truth = float((p*scores).sum(axis=1).mean())
            solution = solve_subset(p)
            ordering_start = perf_counter()
            order, uniform_optimum = optimal_uniform_order(p)
            ordering_seconds = perf_counter()-ordering_start
            for j, method in enumerate(METHODS):
                random = np.random.default_rng(6513+100*k+10*case+j)
                begin = perf_counter()
                actions = sample(p, method, random, count=draws,
                                 coupling=solution if method == "subset-lp" else None,
                                 order=order if method == "ordered-uniform" else None)
                sampling = perf_counter()-begin
                construction = solution.solve_seconds if method == "subset-lp" else 0.
                if method == "ordered-uniform":
                    construction = ordering_seconds
                distinct = np.array([len(set(x)) for x in actions])
                values = scores[np.arange(k)[None], actions].mean(axis=1)
                marginals = np.stack([(actions == a).mean(axis=0) for a in range(6)], axis=1)
                rows.append({"goals": k, "case": case, "alpha": alpha, "method": method,
                             "draws": draws, "mean_distinct": float(distinct.mean()),
                             "exact_optimum": solution.objective,
                             "ordered_uniform_exact_objective": uniform_optimum,
                             "max_marginal_error": float(np.abs(marginals-p).max()),
                             "mean_value": float(values.mean()), "true_mean_value": truth,
                             "squared_mean_error": float((values.mean()-truth)**2),
                             "single_draw_value_variance": float(values.var(ddof=1)),
                             "variance_of_mean": float(values.var(ddof=1)/draws),
                             "construction_seconds": construction,
                             "sampling_seconds": sampling,
                             "seconds_per_draw_amortized": (construction+sampling)/draws})
            print(json.dumps({"goals": k, "case": case, "exact_optimum": solution.objective,
                              "solver_seconds": solution.solve_seconds}), flush=True)
    with (output/"cases.csv").open("w") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    summaries = []
    boot_rng = np.random.default_rng(6521)
    for k in (4, 16, 31):
        for method in METHODS:
            group = [r for r in rows if r["goals"] == k and r["method"] == method]
            summaries.append({"goals": k, "method": method,
                              **{key: float(np.mean([r[key] for r in group])) for key in
                                 ("mean_distinct", "exact_optimum", "single_draw_value_variance",
                                  "squared_mean_error", "construction_seconds", "sampling_seconds",
                                  "seconds_per_draw_amortized")}})
            indices = boot_rng.integers(len(group), size=(4000, len(group)))
            for key in ("mean_distinct", "single_draw_value_variance", "squared_mean_error",
                        "seconds_per_draw_amortized"):
                values = np.array([r[key] for r in group])
                summaries[-1][key+"_matrix_bootstrap_95ci"] = np.quantile(values[indices].mean(axis=1), [.025, .975]).tolist()
    report = {"scope": "arbitrary categorical marginal diagnostic; NOT learned adaptation",
              "training_runs": 0, "robot_episodes": 0, "data_seed": 6512,
              "sampling_base_seed": 6513, "matrices": 3*cases, "draws_per_matrix_method": draws,
              "bootstrap_seed": 6521, "bootstrap_unit": "independent marginal matrix",
              "methods": list(METHODS), "threads": 2, "summaries": summaries,
              "scientific_limits": ["No transition cache or policy inference in this marginal diagnostic",
                                    "Construction is amortized over 2000 fixed-marginal draws; rollout marginals change",
                                    "Independent scores test a counterexample risk, not the actual training objective",
                                    "Distinct-outcome objective is established prior work; solver priority pending"]}
    (output/"result.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cases", type=int, default=8)
    parser.add_argument("--draws", type=int, default=2000)
    args = parser.parse_args(); run(args.output, args.cases, args.draws)
