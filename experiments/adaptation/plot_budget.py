"""Standalone scientific figure from saved exploratory budget curve."""
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot(source,output):
    data=json.loads(source.read_text())
    fig,ax=plt.subplots(figsize=(6.8,4.3),layout="constrained")
    for mode,label in (("full","Retained prior experience"),("empty","Initially empty support")):
        rows=[r for r in data["rows"] if r["history"]==mode]
        ax.plot([r["commands_budget"] for r in rows],[100*r["completion"] for r in rows],marker="o",label=label)
    ax.set(xlabel="Command budget",ylabel="New-goal completion (%)",ylim=(0,102),xticks=np.arange(1,13),
           title="Covered-query policy: exploratory full budget curve")
    ax.axvline(12,color="gray",ls="--",lw=1,label="Predeclared primary endpoint")
    ax.legend(fontsize=8);ax.spines[["top","right"]].set_visible(False)
    fig.text(.5,.01,"128 closure-disjoint rules · 3 fixed checkpoints · collection cost excluded",ha="center",fontsize=8)
    fig.savefig(output.with_suffix(".png"),dpi=180);fig.savefig(output.with_suffix(".pdf"))


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();plot(a.input,a.output)
