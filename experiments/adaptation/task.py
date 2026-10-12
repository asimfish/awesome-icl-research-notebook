"""Task generator and exact shortest-action oracle, outside policy information."""
from dataclasses import dataclass
import numpy as np


@dataclass
class Case:
    graph: np.ndarray  # environment-only: graph[parent, child]
    history: np.ndarray
    state: np.ndarray
    source_goal: np.ndarray
    new_goal: np.ndarray
    graph_id: int


def sample_goal(rng, n):
    """Nonempty subset, independent of hidden graph or feasibility."""
    mask = int(rng.integers(1, 2 ** n))
    return np.array([(mask >> i) & 1 for i in range(n)], dtype=np.float32)


def make_graphs(rng, count, n, excluded=()):
    seen = set(excluded)
    graphs = []
    while len(graphs) < count:
        order = rng.permutation(n)
        graph = np.zeros((n, n), dtype=np.bool_)
        for i in range(n):
            for j in range(i + 1, n):
                graph[order[i], order[j]] = rng.random() < .3
        key = graph.tobytes()
        if key not in seen:
            seen.add(key)
            graphs.append(graph)
    return graphs


def transition(graph, state, action):
    after = state.copy()
    success = not bool(state[action]) and bool(np.all(state[graph[:, action]]))
    if success:
        after[action] = 1
    return after, success


def receipt(before, action, after, success, goal):
    n = len(before)
    onehot = np.zeros(n, dtype=np.float32)
    onehot[action] = 1
    return np.concatenate([before, onehot, after, [float(success)], goal]).astype(np.float32)


def optimal_actions(graph, state, goal):
    """Uniform set of shortest-solution first actions, STOP=n if complete."""
    n = len(state)
    target = np.zeros(n + 1, dtype=np.float32)
    if np.all(state[goal.astype(bool)]):
        target[n] = 1
        return target
    required = goal.astype(bool).copy()
    for _ in range(n):
        required |= np.any(graph[:, required], axis=1)
    eligible = [a for a in range(n) if required[a] and not state[a]
                and np.all(state[graph[:, a]])]
    if not eligible:
        raise ValueError("DAG oracle has no eligible action")
    target[eligible] = 1 / len(eligible)
    return target


def make_cases(graphs, rng, per_graph, max_history):
    cases = []
    for gid, graph in enumerate(graphs):
        n = len(graph)
        for _ in range(per_graph):
            goal = sample_goal(rng, n)
            new_goal = sample_goal(rng, n)
            # Equality rejection depends only on visible goals, never the graph.
            while np.array_equal(goal, new_goal):
                new_goal = sample_goal(rng, n)
            state = np.zeros(n, dtype=np.float32)
            history = []
            length = int(rng.integers(max_history + 1))
            # All commands sampled before any result: no oracle action selection.
            actions = rng.integers(n, size=length)
            for action in actions:
                after, success = transition(graph, state, int(action))
                history.append(receipt(state, int(action), after, success, goal))
                state = after
            cases.append(Case(graph, np.array(history, dtype=np.float32).reshape(-1, 4*n+1),
                              state, goal, new_goal, gid))
    return cases


def query(case, variant):
    if variant == "current-correction":
        return case.state.copy(), case.source_goal.copy()
    if variant == "same-goal-reset":
        return np.zeros_like(case.state), case.source_goal.copy()
    if variant == "different-goal-reset":
        return np.zeros_like(case.state), case.new_goal.copy()
    raise ValueError(variant)
