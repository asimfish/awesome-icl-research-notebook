"""Known public-state masking diagnostic, not a learned method."""
import argparse
import csv
import json
from pathlib import Path
import torch
import numpy as np
from .run_pilot import dataset, evaluate, VARIANTS
from .model import HistoryPolicy


def diagnose(root, output):
    output.mkdir(parents=True,exist_ok=False)
    torch.set_num_threads(2)
    allrows=[]
    summary=[]
    for variant in VARIANTS:
        for seed in (11,29,47):
            checkpoint=torch.load(root/f"{variant}-s{seed}"/"policy.pt",map_location="cpu",weights_only=True)
            cfg=checkpoint["config"]
            _,cases,_=dataset(cfg["data_seed"],cfg["train_graphs"],cfg["test_graphs"],cfg["train_cases"],cfg["test_cases"])
            model=HistoryPolicy(hidden=cfg["hidden"]);model.load_state_dict(checkpoint["state_dict"])
            before={k:v.clone() for k,v in model.state_dict().items()}
            for mask in (False,True):
                for history in ("full","empty"):
                    rows=evaluate(model,cases,"different-goal-reset",history,mask_completed=mask)
                    for r in rows:r.update({"train_variant":variant,"seed":seed})
                    allrows.extend(rows)
                    summary.append({"train_variant":variant,"seed":seed,"history":history,
                                    "completed_action_mask":mask,"success":float(np.mean([r["success"] for r in rows])),
                                    "repeated_completed_commands":float(np.mean([r["repeated_completed_commands"] for r in rows])),
                                    "blocked_commands":float(np.mean([r["blocked_commands"] for r in rows]))})
            assert all(torch.equal(v,before[k]) for k,v in model.state_dict().items())
    with (output/"episodes.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(allrows[0]));w.writeheader();w.writerows(allrows)
    (output/"summary.json").write_text(json.dumps({"scope":"exploratory public-state control diagnostic",
                  "extra_training_runs":0,"extra_evaluation_branches":len(allrows),"independent_graphs":128,
                  "mask_information":"only observed already-completed operations; no prerequisite graph",
                  "rows":summary},indent=2))
    lines=["# Public-state mask diagnostic","","Known action mask, identical for all models; no training, no new algorithm.","",
           "| Training arrangement | Mask | Retained support completion | Empty support completion | Retained support repeated-done commands | Retained support blocked commands |","|---|---|---|---|---|---|"]
    for variant in VARIANTS:
        for mask in (False,True):
            f=[r for r in summary if r["train_variant"]==variant and r["completed_action_mask"]==mask and r["history"]=="full"]
            e=[r for r in summary if r["train_variant"]==variant and r["completed_action_mask"]==mask and r["history"]=="empty"]
            lines.append(f'| {variant} | {mask} | {100*np.mean([r["success"] for r in f]):.2f}% | {100*np.mean([r["success"] for r in e]):.2f}% | {np.mean([r["repeated_completed_commands"] for r in f]):.2f} | {np.mean([r["blocked_commands"] for r in f]):.2f} |')
    (output/"RESULTS.md").write_text("\n".join(lines)+"\n")
    print("\n".join(lines))


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();diagnose(a.root,a.output)
