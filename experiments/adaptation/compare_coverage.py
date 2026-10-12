"""Matched D2 support-benefit interaction and command failure accounting."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np


def compare(root,output):
    rows=[];reports=[]
    for condition in ("covered-query","zero-query"):
        for seed in (11,29,47):
            directory=root/f"{condition}-s{seed}"
            reports.append(json.loads((directory/"result.json").read_text()))
            with (directory/"episodes.csv").open() as f:rows.extend(csv.DictReader(f))
    chosen=[r for r in rows if r["query"]=="different-goal-reset"]
    effects={};costs={};metrics=[]
    for condition in ("covered-query","zero-query"):
        for seed in (11,29,47):
            for mode in ("full","empty"):
                group=[r for r in chosen if r["train_variant"]==condition and int(r["seed"])==seed and r["history"]==mode]
                gids=sorted({int(r["graph_id"]) for r in group})
                effects[condition,seed,mode]=np.array([np.mean([int(r["success"]) for r in group if int(r["graph_id"])==g]) for g in gids])
                costs[condition,seed,mode]=np.array([np.mean([int(r["actions"]) for r in group if int(r["graph_id"])==g]) for g in gids])
                succeeded=[r for r in group if int(r["success"])]
                metrics.append({"condition":condition,"seed":seed,"history":mode,"success":float(np.mean([int(r["success"]) for r in group])),
                     "repeated_completed_commands":float(np.mean([int(r["repeated_completed_commands"]) for r in group])),
                     "blocked_commands":float(np.mean([int(r["blocked_commands"]) for r in group])),
                     "premature_stop":float(np.mean([int(r["premature_stop"]) for r in group])),
                     "commands_success_only":float(np.mean([int(r["actions"]) for r in succeeded])) if succeeded else None,
                     "all_command_mean":float(np.mean([int(r["actions"]) for r in group]))})
    seed_interactions=[];interactions=[]
    for seed in (11,29,47):
        difference=(effects["covered-query",seed,"full"]-effects["covered-query",seed,"empty"])-(effects["zero-query",seed,"full"]-effects["zero-query",seed,"empty"])
        interactions.append(difference);seed_interactions.append(float(difference.mean()))
    by_rule=np.mean(interactions,axis=0);rng=np.random.default_rng(731)
    samples=rng.integers(len(by_rule),size=(4000,len(by_rule)))
    ci=np.quantile(by_rule[samples].mean(1),[.025,.975]).tolist()
    first=reports[0]["objective_stats"]
    cost_seed_benefits=[costs["covered-query",s,"empty"]-costs["covered-query",s,"full"] for s in (11,29,47)]
    cost_by_rule=np.mean(cost_seed_benefits,axis=0)
    cost_ci=np.quantile(cost_by_rule[samples].mean(1),[.025,.975]).tolist()
    report={"scope":"exploratory matched-history query-state experiment, not robot evidence",
            "coverage_minus_zero_support_benefit":float(by_rule.mean()),"rule_bootstrap_95ci":ci,
            "seed_interactions":seed_interactions,"independent_closure_instances":128,
            "covered_history_command_savings":float(cost_by_rule.mean()),"command_savings_rule_95ci":cost_ci,
            "command_savings_by_training_seed":[float(v.mean()) for v in cost_seed_benefits],
            "command_metric_scope":"all-query actual commands capped12; all D2 new-goal failures use12 commands; STOP0; conditional on already supplied initial history, collection excluded",
            "collection_shared_across_arms_and_seeds":True,
            "unique_initial_collection_commands":first["initial_support_commands"],
            "unique_query_prefix_collection_commands":first["additional_training_prefix_commands_collected"],
            "retained_query_prefix_commands":first["additional_training_prefix_commands_retained"],
            "supervised_query_records_per_arm":8192,"sampled_label_exposures_per_checkpoint":76800,
            "paired_metrics":metrics,"interval_scope":"rule bootstrap conditional on3checkpoints per arm; seed interactions separately"}
    output.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ("coverage_minus_zero_support_benefit","rule_bootstrap_95ci","seed_interactions","unique_initial_collection_commands","unique_query_prefix_collection_commands")}))


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();compare(a.root,a.output)
