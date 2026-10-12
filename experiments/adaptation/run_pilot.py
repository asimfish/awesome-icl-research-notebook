"""CPU-only, common-history training and closed-loop frozen evaluation."""
import argparse
import csv
import hashlib
import json
import time
from pathlib import Path
import numpy as np
import torch
from .task import make_graphs, make_cases, query, optimal_actions, transition, receipt
from .model import HistoryPolicy, inputs

VARIANTS = ("current-correction", "same-goal-reset", "different-goal-reset")


def dataset(seed, train_graphs=256, test_graphs=128, train_cases=32, test_cases=8, n=5):
    rng = np.random.default_rng(seed)
    train = make_graphs(rng, train_graphs, n)
    test = make_graphs(rng, test_graphs, n, [g.tobytes() for g in train])
    return (make_cases(train, rng, train_cases, 12),
            make_cases(test, rng, test_cases, 12),
            {"train_graphs": train_graphs, "test_graphs": test_graphs,
             "train_cases": train_graphs*train_cases, "test_cases": test_graphs*test_cases,
             "train_graph_sha256": hashlib.sha256(b"".join(g.tobytes() for g in train)).hexdigest(),
             "test_graph_sha256": hashlib.sha256(b"".join(g.tobytes() for g in test)).hexdigest(),
             "graph_overlap": 0})


def altered_histories(cases, mode):
    if mode == "full":
        return [c.history.copy() for c in cases]
    if mode == "empty":
        return [c.history[:0].copy() for c in cases]
    if mode == "other-world":
        # Fixed cyclic donor with a DIFFERENT graph; not a surgical causal edit.
        return [next(cases[(i+j) % len(cases)].history.copy()
                     for j in range(1, len(cases))
                     if not np.array_equal(c.graph, cases[(i+j) % len(cases)].graph))
                for i, c in enumerate(cases)]
    if mode == "irrelevant":
        # Same commands/source goal/length, actual receipts in an unrelated edgeless world.
        histories = []
        for c in cases:
            state = np.zeros_like(c.state)
            rows = []
            for token in c.history:
                action = int(token[len(state):2*len(state)].argmax())
                after, success = transition(np.zeros_like(c.graph), state, action)
                rows.append(receipt(state, action, after, success, c.source_goal))
                state = after
            histories.append(np.array(rows, dtype=np.float32).reshape(-1, 4*len(state)+1))
        return histories
    raise ValueError(mode)


@torch.no_grad()
def evaluate(model, cases, query_variant, history_mode, max_actions=12, mask_completed=False):
    model.eval()
    states, goals = map(list, zip(*(query(c, query_variant) for c in cases)))
    histories = altered_histories(cases, history_mode)
    target = np.array([optimal_actions(c.graph, s, g) for c,s,g in zip(cases, states, goals)])
    first_logits = model(*inputs(histories, states, goals, model.n))
    if mask_completed:
        first_logits[:, :model.n].masked_fill_(torch.tensor(np.array(states), dtype=torch.bool), -torch.inf)
    first = first_logits.argmax(1).numpy()
    first_optimal = target[np.arange(len(cases)), first] > 0
    initially_complete = target[:, model.n] > 0
    complete = initially_complete.copy()
    stopped = np.zeros(len(cases), dtype=bool)
    actions = np.zeros(len(cases), dtype=int)
    failures = np.zeros(len(cases), dtype=int)
    repeated_completed = np.zeros(len(cases), dtype=int)
    shortest = np.zeros(len(cases), dtype=int)
    # Exact shortest length: deterministic monotone DAG requires closure once.
    for i, c in enumerate(cases):
        s = states[i].copy()
        while not np.all(s[goals[i].astype(bool)]):
            action = int(optimal_actions(c.graph, s, goals[i]).argmax())
            s, _ = transition(c.graph, s, action)
            shortest[i] += 1
    for step in range(max_actions):
        active = np.flatnonzero(~(complete | stopped))
        if not len(active):
            break
        logits = model(*inputs([histories[i] for i in active],
                               [states[i] for i in active],
                               [goals[i] for i in active], model.n))
        if mask_completed:
            logits[:, :model.n].masked_fill_(torch.tensor(np.array([states[i] for i in active]), dtype=torch.bool), -torch.inf)
        selected = logits.argmax(1).numpy()
        for i, a in zip(active, selected):
            if a == model.n:
                stopped[i] = True
                continue
            actions[i] += 1
            repeated_completed[i] += int(bool(states[i][a]))
            after, success = transition(cases[i].graph, states[i], int(a))
            failures[i] += int(not success)
            row = receipt(states[i], int(a), after, success, goals[i])
            histories[i] = np.concatenate([histories[i], row[None]], axis=0)
            states[i] = after
            complete[i] = np.all(after[goals[i].astype(bool)])
    rows = []
    for i, c in enumerate(cases):
        rows.append({"case_id": i, "graph_id": c.graph_id, "query": query_variant,
                     "history": history_mode, "success": int(complete[i]),
                     "initially_complete": int(initially_complete[i]),
                     "first_optimal": int(first_optimal[i]), "actions": int(actions[i]),
                     "failures": int(failures[i]), "shortest_actions": int(shortest[i]),
                     "premature_stop": int(stopped[i]), "initial_history_length": len(c.history)})
        rows[-1].update({"repeated_completed_commands":int(repeated_completed[i]),
                         "blocked_commands":int(failures[i]-repeated_completed[i]),
                         "completed_action_mask":int(mask_completed)})
    return rows


def run(args):
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(2)
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    torch.use_deterministic_algorithms(True)
    train, test, counts = dataset(args.data_seed, args.train_graphs, args.test_graphs,
                                  args.train_cases, args.test_cases)
    model = HistoryPolicy(hidden=args.hidden)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    rng = np.random.default_rng(args.seed)
    queries = [query(c, args.variant) for c in train]
    targets = np.array([optimal_actions(c.graph, *q) for c,q in zip(train, queries)])
    objective_stats = {"terminal_label_fraction": float(targets[:, -1].mean()),
                       "mean_target_distribution": targets.mean(axis=0).tolist(),
                       "mean_history_length": float(np.mean([len(c.history) for c in train]))}
    (out / "config.json").write_text(json.dumps(vars(args), indent=2))
    losses = []
    start = time.monotonic()
    for step in range(args.steps):
        if time.monotonic() - start > args.time_limit:
            raise TimeoutError("Training budget exceeded; do not silently call this a full run")
        indices = rng.integers(len(train), size=args.batch)
        batch_input = inputs([train[i].history for i in indices],
                             [queries[i][0] for i in indices], [queries[i][1] for i in indices], 5)
        logits = model(*batch_input)
        target = torch.from_numpy(targets[indices])
        loss = -(target * logits.log_softmax(-1)).sum(-1).mean()
        if not torch.isfinite(loss):
            raise FloatingPointError("Nonfinite training loss")
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        if step % 20 == 0 or step == args.steps-1:
            losses.append({"step": step+1, "loss": float(loss.detach())})
    train_seconds = time.monotonic()-start
    torch.save({"state_dict": model.state_dict(), "config": vars(args)}, out / "policy.pt")
    frozen_before = {k: v.clone() for k,v in model.state_dict().items()}
    rows = []
    eval_start = time.monotonic()
    for variant in VARIANTS:
        for mode in args.history_modes.split(","):
            rows.extend(evaluate(model, test, variant, mode))
    assert all(torch.equal(v, frozen_before[k]) for k,v in model.state_dict().items())
    for row in rows:
        row.update({"train_variant": args.variant, "seed": args.seed})
    with (out / "episodes.csv").open("w") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {"status": "complete", "scope": "symbolic dependency-operation simulator",
              "config": vars(args), "counts": counts, "objective_stats": objective_stats,
              "parameters": sum(p.numel() for p in model.parameters()), "loss_trace": losses,
              "training_updates": args.steps, "supervised_labels_seen": args.steps*args.batch,
              "training_seconds": train_seconds, "evaluation_seconds": time.monotonic()-eval_start,
              "evaluation_episodes": len(rows), "frozen_evaluation_verified": True,
              "torch_version": torch.__version__, "device": "cpu", "threads": 2}
    (out / "result.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in ("status", "training_seconds", "evaluation_seconds", "evaluation_episodes")}))


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", required=True)
    p.add_argument("--variant", choices=VARIANTS, required=True)
    p.add_argument("--seed", type=int, default=11)
    p.add_argument("--data-seed", type=int, default=1012)
    p.add_argument("--steps", type=int, default=600)
    p.add_argument("--batch", type=int, default=128)
    p.add_argument("--hidden", type=int, default=96)
    p.add_argument("--lr", type=float, default=.001)
    p.add_argument("--train-graphs", type=int, default=256)
    p.add_argument("--test-graphs", type=int, default=128)
    p.add_argument("--train-cases", type=int, default=32)
    p.add_argument("--test-cases", type=int, default=8)
    p.add_argument("--time-limit", type=float, default=600)
    p.add_argument("--history-modes", default="full,empty")
    return p


if __name__ == "__main__":
    run(parser().parse_args())
