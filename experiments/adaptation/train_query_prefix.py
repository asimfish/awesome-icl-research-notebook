"""Exploratory state-support repair, using ordinary query-action supervision."""
import argparse
import csv
import hashlib
import json
import time
from pathlib import Path
import numpy as np
import torch
from .task import make_graphs, make_cases, query, transition, receipt, optimal_actions
from .model import HistoryPolicy, inputs
from .run_pilot import dataset, evaluate, VARIANTS


def closure_key(graph):
    closure = graph.copy()
    for k in range(len(graph)):
        closure |= closure[:, k:k+1] & closure[k:k+1, :]
    return closure.tobytes()


def closure_graphs(rng, count, excluded):
    seen = set(excluded)
    result=[]
    while len(result)<count:
        graph=make_graphs(rng,1,5)[0]
        key=closure_key(graph)
        if key not in seen:
            seen.add(key);result.append(graph)
    return result


def prefix_dataset(seed=2712):
    old_train,old_test,_=dataset(1012)
    seen={closure_key(c.graph) for c in old_train+old_test}
    rng=np.random.default_rng(seed)
    train=closure_graphs(rng,256,seen)
    test=closure_graphs(rng,128,seen|{closure_key(g) for g in train})
    train_cases=make_cases(train,rng,32,12)
    test_cases=make_cases(test,rng,8,12)
    return train_cases,test_cases,{"train_graphs":256,"test_graphs":128,
             "train_cases":8192,"test_cases":1024,"graph_overlap":0,"closure_overlap":0,
             "closure_overlap_with_previous_train_and_test":0,
             "train_graph_sha256":hashlib.sha256(b"".join(g.tobytes() for g in train)).hexdigest(),
             "test_graph_sha256":hashlib.sha256(b"".join(g.tobytes() for g in test)).hexdigest()}


def training_queries(cases,condition,seed=2713,prefix_max=12):
    rng=np.random.default_rng(seed)
    histories=[];states=[];goals=[];lengths=[];collection_lengths=[]
    for c in cases:
        state,goal=query(c,"different-goal-reset")
        length=int(rng.integers(prefix_max+1))
        commands=rng.integers(5,size=length)
        history=c.history.copy();candidates=[(history.copy(),state.copy(),0)]
        actual_commands=0
        for action in commands:
            if np.all(state[goal.astype(bool)]):break
            after,success=transition(c.graph,state,int(action))
            token=receipt(state,int(action),after,success,goal)
            history=np.concatenate([history,token[None]],axis=0)
            state=after
            actual_commands+=1
            if not np.all(state[goal.astype(bool)]):
                candidates.append((history.copy(),state.copy(),actual_commands))
        chosen=int(rng.integers(len(candidates)))
        history,state,retained_length=candidates[chosen]
        if condition=="zero-query":state=np.zeros_like(state)
        elif condition!="covered-query":raise ValueError(condition)
        histories.append(history);states.append(state);goals.append(goal)
        lengths.append(retained_length);collection_lengths.append(actual_commands)
    return histories,states,goals,lengths,collection_lengths


def run(args):
    out=Path(args.output);out.mkdir(parents=True,exist_ok=False)
    torch.set_num_threads(2);torch.manual_seed(args.seed);torch.use_deterministic_algorithms(True)
    train,test,counts=prefix_dataset(args.data_seed)
    histories,states,goals,prefix_lengths,collection_lengths=training_queries(train,args.condition,args.data_seed+1)
    targets=np.array([optimal_actions(c.graph,s,g) for c,s,g in zip(train,states,goals)])
    model=HistoryPolicy(hidden=96);initial_state_weights=model.head[0].weight[:,96:101].detach().clone()
    optimizer=torch.optim.Adam(model.parameters(),lr=.001)
    rng=np.random.default_rng(args.seed);losses=[];start=time.monotonic()
    for step in range(600):
        if time.monotonic()-start>600:raise TimeoutError("Training budget exceeded")
        ix=rng.integers(len(train),size=128)
        logits=model(*inputs([histories[i] for i in ix],[states[i] for i in ix],[goals[i] for i in ix],5))
        loss=-(torch.from_numpy(targets[ix])*logits.log_softmax(-1)).sum(-1).mean()
        if not torch.isfinite(loss):raise FloatingPointError("Nonfinite loss")
        optimizer.zero_grad(set_to_none=True);loss.backward();optimizer.step()
        if step%20==0 or step==599:losses.append({"step":step+1,"loss":float(loss.detach())})
    elapsed=time.monotonic()-start
    config={**vars(args),"steps":600,"batch":128,"hidden":96,"lr":.001,"train_graphs":256,"test_graphs":128,"train_cases":32,"test_cases":8,"prefix_max":12}
    torch.save({"state_dict":model.state_dict(),"config":config},out/"policy.pt")
    before={k:v.clone() for k,v in model.state_dict().items()};rows=[];start_eval=time.monotonic()
    for variant in VARIANTS:
        for mode in ("full","empty"):
            rows.extend(evaluate(model,test,variant,mode))
    assert all(torch.equal(v,before[k]) for k,v in model.state_dict().items())
    for r in rows:r.update({"train_variant":args.condition,"seed":args.seed})
    with (out/"episodes.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    stats={"terminal_label_fraction":float(targets[:,-1].mean()),"mean_target_distribution":targets.mean(0).tolist(),
           "mean_history_length":float(np.mean([len(h) for h in histories])),
           "mean_query_state":np.array(states).mean(0).tolist(),"query_state_weights_changed":not torch.equal(model.head[0].weight[:,96:101].detach(),initial_state_weights),
           "additional_training_prefix_commands_retained":sum(prefix_lengths),
           "additional_training_prefix_commands_collected":sum(collection_lengths),
           "initial_support_commands":sum(len(c.history) for c in train)}
    result={"status":"complete","scope":"exploratory symbolic query-state support repair",
            "config":config,"counts":counts,"objective_stats":stats,"loss_trace":losses,
            "parameters":sum(p.numel() for p in model.parameters()),"training_updates":600,
            "supervised_labels_seen":76800,"unique_teacher_target_distributions":8192,
            "training_seconds":elapsed,"evaluation_seconds":time.monotonic()-start_eval,
            "evaluation_episodes":len(rows),"frozen_evaluation_verified":True,"torch_version":torch.__version__,"device":"cpu","threads":2}
    (out/"config.json").write_text(json.dumps(config,indent=2));(out/"result.json").write_text(json.dumps(result,indent=2))
    print(json.dumps({"condition":args.condition,"seed":args.seed,"training_seconds":elapsed,"evaluation_episodes":len(rows)}))


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True);p.add_argument("--condition",choices=("covered-query","zero-query"),required=True)
    p.add_argument("--seed",type=int,default=11);p.add_argument("--data-seed",type=int,default=2712)
    run(p.parse_args())
