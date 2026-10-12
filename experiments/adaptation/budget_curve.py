"""Exploratory full command-budget curves, not a revised primary endpoint."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np


def curve(root,output):
    rows=[]
    for seed in (11,29,47):
        with (root/f"covered-query-s{seed}"/"episodes.csv").open() as f:
            rows.extend(r for r in csv.DictReader(f) if r["query"]=="different-goal-reset")
    values=[]
    for budget in range(1,13):
        for mode in ("full","empty"):
            seed_values=[]
            for seed in (11,29,47):
                group=[r for r in rows if r["history"]==mode and int(r["seed"])==seed]
                seed_values.append(float(np.mean([int(r["success"]) and int(r["actions"])<=budget for r in group])))
            values.append({"commands_budget":budget,"history":mode,"completion":float(np.mean(seed_values)),"seed_values":seed_values})
    report={"scope":"exploratory cumulative completion curve from fixed D2 traces; all horizons1–12 shown",
            "primary_budget_unchanged":12,"primary_support_completion_go":"failed",
            "validity":"actor/STOP policy has no budget input; success/actions reconstruct earlier completion from unchanged traces; failures remain censored at12",
            "not_claimed":"preselected tight-budget gain, net collection benefit, robotics or algorithm novelty","rows":values}
    output.write_text(json.dumps(report,indent=2)+"\n")


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();curve(a.root,a.output)
