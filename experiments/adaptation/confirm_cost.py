"""Prospectively fixed fresh-cohort cost check, zero training."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import torch
from .run_pilot import dataset,evaluate
from .train_query_prefix import prefix_dataset,closure_graphs,closure_key
from .task import make_cases
from .model import HistoryPolicy


def confirm(root,output):
    output.mkdir(parents=True,exist_ok=False);torch.set_num_threads(2)
    a,b,_=dataset(1012);c,d,_=prefix_dataset(2712)
    excluded={closure_key(x.graph) for x in a+b+c+d}
    rng=np.random.default_rng(4812);graphs=closure_graphs(rng,256,excluded)
    assert len({closure_key(g) for g in graphs})==256
    assert not {closure_key(g) for g in graphs}&excluded
    cases=make_cases(graphs,rng,8,12);rows=[];savings=[];seed_stats=[]
    for seed in (11,29,47):
        checkpoint=torch.load(root/f"covered-query-s{seed}"/"policy.pt",map_location="cpu",weights_only=True)
        model=HistoryPolicy(hidden=96);model.load_state_dict(checkpoint["state_dict"])
        before={k:v.clone() for k,v in model.state_dict().items()};groups={}
        for mode in ("full","empty"):
            group=evaluate(model,cases,"different-goal-reset",mode)
            for r in group:r.update({"seed":seed,"train_variant":"covered-query"})
            groups[mode]=group;rows.extend(group)
        assert all(torch.equal(v,before[k]) for k,v in model.state_dict().items())
        assert all(r["success"] or (r["actions"]==12 and not r["premature_stop"]) for mode in groups for r in groups[mode])
        by_rule=[]
        for gid in range(256):
            paired=[int(e["actions"])-int(f["actions"]) for f,e in zip(groups["full"],groups["empty"]) if f["graph_id"]==gid]
            by_rule.append(float(np.mean(paired)))
        savings.append(by_rule)
        seed_stats.append({"seed":seed,"command_savings":float(np.mean(by_rule)),
                   "full_completion":float(np.mean([r["success"] for r in groups["full"]])),
                   "empty_completion":float(np.mean([r["success"] for r in groups["empty"]])),
                   "full_commands":float(np.mean([r["actions"] for r in groups["full"]])),
                   "empty_commands":float(np.mean([r["actions"] for r in groups["empty"]]))})
    by_rule=np.mean(savings,axis=0);boots=np.random.default_rng(731).integers(256,size=(4000,256))
    ci=np.quantile(by_rule[boots].mean(1),[.025,.975]).tolist()
    report={"scope":"fresh closure-disjoint confirmation of previously secondary conditional command benefit",
            "training_runs":0,"data_seed":4812,"independent_closures":256,"cases_per_rule":8,"evaluation_branches":len(rows),
            "command_savings":float(by_rule.mean()),"rule_bootstrap_95ci":ci,"seed_results":seed_stats,
            "mean_initial_support_commands":float(np.mean([len(c.history) for c in cases])),
            "cost_confirmation_gate":bool(ci[0]>0 and all(r["command_savings"]>0 for r in seed_stats)),
            "original_completion_support_gate":"FAILED; unchanged",
            "frozen_evaluation_verified":True,"STOP_failure_cost_invariant_verified":True,
            "cost_excludes_initial_collection":True,"robot_episodes":0,"device":"cpu","threads":2}
    with (output/"episodes.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (output/"result.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();confirm(a.root,a.output)
