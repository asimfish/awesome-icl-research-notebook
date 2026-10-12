"""Rule-level paired pilot summaries; fixed checkpoints, no test tuning."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from .run_pilot import VARIANTS


def summarize(root, output, train_variants=VARIANTS):
    output.mkdir(parents=True, exist_ok=False)
    records = []
    reports = []
    for variant in train_variants:
        for seed in (11,29,47):
            path = root / f"{variant}-s{seed}"
            reports.append(json.loads((path / "result.json").read_text()))
            with (path / "episodes.csv").open() as f:
                records.extend(list(csv.DictReader(f)))
    rows = []
    seed_rows = []
    bootstrap = np.random.default_rng(731)
    for variant in train_variants:
        for query in VARIANTS:
            success = {}
            optimal = {}
            seed_values = []
            for seed in (11,29,47):
                modes = {}
                for mode in ("full", "empty"):
                    group = [r for r in records if r["train_variant"] == variant
                             and r["query"] == query and r["history"] == mode
                             and int(r["seed"]) == seed]
                    gid = sorted({int(r["graph_id"]) for r in group})
                    success[seed,mode] = np.array([np.mean([int(r["success"]) for r in group
                                                  if int(r["graph_id"]) == g]) for g in gid])
                    optimal[seed,mode] = np.array([np.mean([int(r["first_optimal"]) for r in group
                                                  if int(r["graph_id"]) == g]) for g in gid])
                    active = [r for r in group if not int(r["initially_complete"])]
                    modes[mode] = float(np.mean([int(r["success"]) for r in group]))
                    seed_rows.append({"train_variant": variant, "query": query, "seed": seed,
                                      "history": mode, "success": modes[mode],
                                      "nonterminal_success": float(np.mean([int(r["success"]) for r in active])),
                                      "first_optimal": float(optimal[seed,mode].mean()),
                                      "actions": float(np.mean([int(r["actions"]) for r in group])),
                                      "failures": float(np.mean([int(r["failures"]) for r in group])),
                                      "premature_stop": float(np.mean([int(r["premature_stop"]) for r in group]))})
                seed_values.append(modes["full"]-modes["empty"])
            graph_deltas = np.mean([success[s,"full"]-success[s,"empty"] for s in (11,29,47)], axis=0)
            sampled = bootstrap.integers(len(graph_deltas), size=(4000,len(graph_deltas)))
            ci = np.quantile(graph_deltas[sampled].mean(axis=1), [.025,.975]).tolist()
            first_delta = np.mean([optimal[s,"full"]-optimal[s,"empty"] for s in (11,29,47)],axis=0)
            first_ci = np.quantile(first_delta[sampled].mean(axis=1), [.025,.975]).tolist()
            fulls = [success[s,"full"].mean() for s in (11,29,47)]
            empties = [success[s,"empty"].mean() for s in (11,29,47)]
            rows.append({"train_variant":variant,"query":query,
                         "success_full_mean":float(np.mean(fulls)),"success_full_seed_sd":float(np.std(fulls,ddof=1)),
                         "success_empty_mean":float(np.mean(empties)),"success_empty_seed_sd":float(np.std(empties,ddof=1)),
                         "historical_support_benefit":float(graph_deltas.mean()),"rule_bootstrap_95ci":ci,
                         "seed_support_benefits":seed_values,
                         "first_optimal_full":float(np.mean([optimal[s,"full"].mean() for s in (11,29,47)])),
                         "first_optimal_empty":float(np.mean([optimal[s,"empty"].mean() for s in (11,29,47)])),
                         "first_optimal_benefit":float(first_delta.mean()),"first_optimal_rule_95ci":first_ci})
    output_json = {"status":"exploratory mechanism pilot", "scope":"symbolic dependency operations; zero robot episodes",
                   "training_runs":len(reports), "training_updates":sum(r["training_updates"] for r in reports),
                   "evaluation_episodes":len(records), "training_seconds":sum(r["training_seconds"] for r in reports),
                   "evaluation_seconds":sum(r["evaluation_seconds"] for r in reports),
                   "independent_heldout_rule_instances":reports[0]["counts"]["test_graphs"],
                   "cases_per_rule":8,"training_seeds":[11,29,47],
                   "interval_scope":"paired bootstrap of rules, averaging fixed3 checkpoints; not full training-seed uncertainty",
                   "objective_stats":[{"variant":r["config"].get("variant",r["config"].get("condition")),"seed":r["config"]["seed"],**r["objective_stats"]} for r in reports],
                   "rows":rows,"seed_rows":seed_rows}
    (output / "summary.json").write_text(json.dumps(output_json,indent=2))
    with (output / "seed_metrics.csv").open("w") as f:
        w = csv.DictWriter(f,fieldnames=list(seed_rows[0]));w.writeheader();w.writerows(seed_rows)
    lines = [("# Matched-history query-state pilot" if "covered-query" in train_variants else "# First learned-policy pilot results"), "", "Exploratory dependency-operation mechanism pilot; no robot evidence.", "",
             "| Training query | Evaluation query | Full support success | Empty support success | Support gain [rule95% CI] | First-action support gain |", "|---|---|---|---|---|---|"]
    for r in rows:
        lo,hi = r["rule_bootstrap_95ci"]
        lines.append(f'| {r["train_variant"]} | {r["query"]} | {100*r["success_full_mean"]:.2f}% ± {100*r["success_full_seed_sd"]:.2f} seed SD | {100*r["success_empty_mean"]:.2f}% | {100*r["historical_support_benefit"]:+.2f} pp [{100*lo:.2f},{100*hi:.2f}] | {100*r["first_optimal_benefit"]:+.2f} pp |')
    lines.extend(["", "Intervals bootstrap independent rules, conditional on the three checkpoints. Seed effects are listed separately in summary.json/seed_metrics.csv; trials are paired and do not count as independent robots.", "",
                  f'Actual main runs:{len(reports)}; training updates:{output_json["training_updates"]}; evaluation branches:{len(records)}; independent held-out graphs:128; total training seconds:{output_json["training_seconds"]:.3f}.', "",
                  "STOP target fractions: " + "; ".join(f'{r["config"].get("variant",r["config"].get("condition"))}: {100*r["objective_stats"]["terminal_label_fraction"]:.2f}%' for r in reports[::3]) + ".",
                  "", "Initially empty support still allows feedback from the query itself. Other-world/irrelevant-history stress is separate. A query-distribution advantage by itself does not establish algorithmic novelty or relation recovery."])
    (output / "RESULTS.md").write_text("\n".join(lines)+"\n")
    print(json.dumps({"training_runs":len(reports),"evaluation_episodes":len(records),
                      "new_goal_rows":[r for r in rows if r["query"] == "different-goal-reset"]}))


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--root",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    p.add_argument("--variants",default=",".join(VARIANTS))
    a=p.parse_args();summarize(a.root,a.output,tuple(a.variants.split(",")))
