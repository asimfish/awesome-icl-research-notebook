"""Plot saved numeric results in the installed system Matplotlib runtime.

Run /usr/bin/python3 -s -m experiments.adaptation.plot_pilot --input <analysis-dir>
System NumPy1.21.5 + Matplotlib3.5.1; no Torch imports or environment mutation.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot(output):
    rows = json.loads((output / "summary.json").read_text())["rows"]
    fig, ax = plt.subplots(1,2,figsize=(10,4),layout="constrained")
    selected = [r for r in rows if r["query"] == "different-goal-reset"]
    x = np.arange(len(selected))
    label_map = {"current-correction":"Current correction","same-goal-reset":"Same-goal reset","different-goal-reset":"Different-goal reset","covered-query":"Covered query states","zero-query":"Reset-only queries"}
    labels = [label_map[r["train_variant"]] for r in selected]
    ax[0].bar(x-.16,[100*r["success_full_mean"] for r in selected],.32,label="Retained support")
    ax[0].bar(x+.16,[100*r["success_empty_mean"] for r in selected],.32,label="Initially empty")
    ax[0].set(ylim=(0,100),ylabel="New-goal completion (%)",title="Frozen policy, physical state reset")
    ax[0].legend(fontsize=8)
    delta = np.array([100*r["historical_support_benefit"] for r in selected])
    ci = np.array([r["rule_bootstrap_95ci"] for r in selected])*100
    ax[1].errorbar(x,delta,yerr=np.stack([delta-ci[:,0],ci[:,1]-delta]),fmt="o",capsize=4)
    ax[1].axhline(0,color="gray",linewidth=1)
    ax[1].set(ylabel="Paired support benefit (percentage points)",title="Rule-bootstrap95% intervals")
    for a in ax:
        a.set_xticks(x,labels,rotation=15,ha="right");a.spines[["top","right"]].set_visible(False)
    fig.suptitle("Controlled symbolic pilot · 128 held-out rules · 3 training seeds",fontsize=11)
    fig.savefig(output / "pilot-new-goal.png",dpi=180)
    fig.savefig(output / "pilot-new-goal.pdf")

if __name__ == "__main__":
    p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True)
    plot(p.parse_args().input)
