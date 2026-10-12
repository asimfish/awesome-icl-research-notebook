"""Frozen own-attempt experience stream; no new learning algorithm or training."""
import argparse
import csv
import json
from pathlib import Path
from time import perf_counter

import numpy as np
import torch
from .model import HistoryPolicy, inputs
from .run_pilot import dataset
from .train_query_prefix import prefix_dataset, closure_graphs, closure_key
from .task import make_cases, transition, receipt


def stream_dataset(count=256, per_rule=8):
    a, b, _ = dataset(1012)
    c, d, _ = prefix_dataset(2712)
    excluded = {closure_key(x.graph) for x in a+b+c+d}
    rng_old = np.random.default_rng(4812)
    previous = closure_graphs(rng_old, 256, excluded)
    excluded |= {closure_key(g) for g in previous}
    if len(excluded) != 1015:
        raise RuntimeError(f"historical exclusion count changed: {len(excluded)}")
    rng = np.random.default_rng(6412)
    graphs = closure_graphs(rng, count, excluded)
    if len({closure_key(g) for g in graphs}) != count or {closure_key(g) for g in graphs} & excluded:
        raise RuntimeError("stream cohort is not closure-disjoint")
    rules, ids, schedules = [], [], []
    for gid, graph in enumerate(graphs):
        for sid in range(per_rule):
            masks = rng.choice(np.arange(1, 32), size=6, replace=False)
            goals = np.array([[(int(m) >> j) & 1 for j in range(5)] for m in masks], dtype=np.float32)
            rules.append(graph); ids.append((gid, sid)); schedules.append(goals)
    return rules, ids, np.array(schedules), len(excluded)


@torch.no_grad()
def rollout(model, rules, ids, goals, retain, max_commands=12, memory_window=12):
    count, n = len(rules), model.n
    past = [np.zeros((0, 4*n+1), dtype=np.float32) for _ in rules]
    rows = []
    model.eval()
    for task in range(goals.shape[1]):
        states = np.zeros((count, n), dtype=np.float32)
        initial = [h[-memory_window:].copy() if retain else np.zeros((0, 4*n+1), dtype=np.float32) for h in past]
        histories = [h.copy() for h in initial]
        complete, stopped = np.zeros(count, dtype=bool), np.zeros(count, dtype=bool)
        issued, blocked, repeats = [np.zeros(count, dtype=int) for _ in range(3)]
        first = np.full(count, -1, dtype=int)
        own = [[] for _ in rules]
        for step in range(max_commands):
            active = np.flatnonzero(~(complete | stopped))
            if not len(active): break
            logits = model(*inputs([histories[i] for i in active], states[active], goals[active, task], n))
            actions = logits.argmax(dim=1).numpy()
            for i, action in zip(active, actions):
                action = int(action)
                if step == 0: first[i] = action
                if action == n:
                    stopped[i] = True
                    continue
                issued[i] += 1; repeats[i] += int(states[i, action] > 0)
                after, success = transition(rules[i], states[i], action)
                blocked[i] += int(not success)
                token = receipt(states[i], action, after, success, goals[i, task])
                own[i].append(token)
                histories[i] = np.concatenate([histories[i], token[None]], axis=0)
                states[i] = after
                complete[i] = bool(np.all(after[goals[i, task].astype(bool)]))
        for i in range(count):
            if retain:
                current = np.array(own[i], dtype=np.float32).reshape(-1, 4*n+1)
                past[i] = np.concatenate([past[i], current], axis=0)[-memory_window:]
            gid, sid = ids[i]
            rows.append({"graph_id": gid, "stream_id": sid, "task_index": task,
                         "retain": int(retain), "goal_mask": int(sum(int(x)*(1 << j) for j, x in enumerate(goals[i, task]))),
                         "success": int(complete[i]), "actual_commands": int(issued[i]),
                         "capped_commands": int(issued[i]) if complete[i] else max_commands,
                         "blocked_commands": int(blocked[i]-repeats[i]),
                         "repeated_completed_commands": int(repeats[i]), "premature_stop": int(stopped[i]),
                         "initial_receipts": len(initial[i]), "final_query_receipts": len(histories[i]),
                         "first_action": int(first[i]), "between_task_reset": int(task > 0),
                         "initialization": int(task == 0)})
            if len(histories[i]) > memory_window+max_commands:
                raise RuntimeError("query history exceeds declared envelope")
    return rows


def run(root, output, count=256, per_rule=8):
    output.mkdir(parents=True, exist_ok=False); torch.set_num_threads(2)
    start = perf_counter(); rules, ids, goals, excluded = stream_dataset(count, per_rule)
    rows, differences, seed_results = [], [], []
    for seed in (11, 29, 47):
        saved = torch.load(root/f"covered-query-s{seed}"/"policy.pt", map_location="cpu", weights_only=True)
        model = HistoryPolicy(hidden=96); model.load_state_dict(saved["state_dict"])
        before = {k: v.clone() for k, v in model.state_dict().items()}
        groups = {mode: rollout(model, rules, ids, goals, mode) for mode in (False, True)}
        for mode, group in groups.items():
            for row in group: row["seed"] = seed
            rows.extend(group)
        assert all(torch.equal(v, before[k]) for k, v in model.state_dict().items())
        assert len(groups[False]) == len(groups[True]) == count*per_rule*6
        assert all(all(left[k] == right[k] for k in ("first_action", "success", "actual_commands", "capped_commands", "premature_stop"))
                   for left, right in zip(groups[False], groups[True]) if left["task_index"] == 0)
        delta = np.zeros((count, 2))
        for left, right in zip(groups[False], groups[True]):
            assert (left["graph_id"], left["stream_id"], left["task_index"], left["goal_mask"]) == (right["graph_id"], right["stream_id"], right["task_index"], right["goal_mask"])
            delta[left["graph_id"], 0] += (left["capped_commands"]-right["capped_commands"])/per_rule
            delta[left["graph_id"], 1] += (right["success"]-left["success"])/(per_rule*6)
        differences.append(delta)
        seed_results.append({"seed": seed, "stream_command_savings": float(delta[:, 0].mean()),
                             "completion_delta": float(delta[:, 1].mean()),
                             "retain_completion": float(np.mean([x["success"] for x in groups[True]])),
                             "erase_completion": float(np.mean([x["success"] for x in groups[False]]))})
        print(json.dumps(seed_results[-1]), flush=True)
    paired = np.mean(differences, axis=0)
    boot = np.random.default_rng(6531).integers(count, size=(4000, count))
    intervals = np.quantile(paired[boot].mean(axis=1), [.025, .975], axis=0)
    report = {"scope": "own required-attempt frozen learned-policy transfer diagnostic",
              "training_runs": 0, "robot_episodes": 0, "evaluation_branches": len(rows),
              "rules": count, "streams_per_rule": per_rule, "required_tasks_per_stream": 6,
              "unique_goals_within_stream": True, "data_seed": 6412, "excluded_closures": excluded,
              "bootstrap_seed": 6531, "bootstrap_unit": "rule after averaging streams and checkpoints",
              "stream_command_savings": float(paired[:, 0].mean()), "rule_bootstrap_95ci_commands": intervals[:, 0].tolist(),
              "completion_delta": float(paired[:, 1].mean()), "rule_bootstrap_95ci_completion": intervals[:, 1].tolist(),
              "seeds": seed_results, "first_task_identity_verified": True, "frozen_weights_verified": True,
              "own_feedback_in_both_arms": True, "STOP_failure_charged_full_budget": True,
              "actual_seconds": perf_counter()-start, "device": "cpu", "threads": 2,
              "limits": ["No new acquisition training, relation identification or algorithm novelty",
                         "Whole-stream policy intervention; histories later differ",
                         "No retrospective noninferiority margin; report cost and completion jointly",
                         "Selected-method development cohort; cannot become a later final test"]}
    with (output/"episodes.csv").open("w") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    (output/"result.json").write_text(json.dumps(report, indent=2)); print(json.dumps(report), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True); parser.add_argument("--rules", type=int, default=256)
    parser.add_argument("--streams-per-rule", type=int, default=8)
    args = parser.parse_args(); run(args.root, args.output, args.rules, args.streams_per_rule)
