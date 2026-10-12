"""Exact subset extended formulation of an established grand-coupling objective.

The objective (expected distinct outcomes) is prior work. Formulation priority
is pending. All methods preserve marginals, but their return covariances differ.
"""
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from itertools import permutations
from time import perf_counter

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def validate(probabilities):
    p = np.asarray(probabilities, dtype=float)
    if p.ndim != 2 or min(p.shape) < 1 or not np.isfinite(p).all():
        raise ValueError("expected a finite K by A probability matrix")
    if (p < 0).any() or not np.allclose(p.sum(axis=1), 1, atol=1e-10, rtol=0):
        raise ValueError("rows must be nonnegative probability distributions")
    return p


def _allocation_flow(weights, subsets, probabilities):
    """Floating-capacity bipartite transportation, without integer rounding."""
    q, a = len(weights), len(probabilities)
    source, sink = q+a, q+a+1
    graph = [[] for _ in range(sink+1)]

    def add(u, v, capacity):
        forward = [v, float(capacity), len(graph[v])]
        reverse = [u, 0., len(graph[u])]
        graph[u].append(forward); graph[v].append(reverse)
        return forward

    links = []
    for s, subset in enumerate(subsets):
        add(source, s, weights[s])
        for act in subset:
            edge = add(s, q+act, 1.)
            links.append((s, act, edge))
    for act in range(a):
        add(q+act, sink, probabilities[act])
    sent = 0.
    # Edmonds-Karp is enough for this small action diagnostic. The mathematical
    # formulation has no claim of this implementation being runtime-optimal.
    while True:
        parent = [None]*len(graph); parent[source] = (-1, -1)
        queue = [source]
        for u in queue:
            for i, (v, capacity, _) in enumerate(graph[u]):
                if capacity > 0 and parent[v] is None:
                    parent[v] = (u, i); queue.append(v)
            if parent[sink] is not None:
                break
        if parent[sink] is None:
            break
        amount, v = 1., sink
        while v != source:
            u, i = parent[v]; amount = min(amount, graph[u][i][1]); v = u
        v = sink
        while v != source:
            u, i = parent[v]; edge = graph[u][i]
            edge[1] -= amount; graph[v][edge[2]][1] += amount; v = u
        sent += amount
    if sent < 1-1e-7:
        raise RuntimeError(f"Hall-feasible transportation incomplete: {sent}")
    allocation = np.zeros((q, a))
    for s, act, edge in links:
        # Flow is the capacity on the paired reverse edge, avoiding subtractive
        # cancellation for small flows from a unit artificial capacity.
        allocation[s, act] = graph[edge[0]][edge[2]][1]
    return allocation


@lru_cache(maxsize=32)
def structure(k, a):
    subsets = [tuple(i for i in range(a) if mask >> i & 1)
               for mask in range(1, 1 << a)]
    q = len(subsets)
    entries = [(g, s, act) for g in range(k)
               for s, subset in enumerate(subsets) for act in subset]
    row, col, data = [], [], []
    for s in range(q):
        row.append(0); col.append(s); data.append(1.)
        for g in range(k):
            row.append(1 + g*q + s); col.append(s); data.append(-1.)
    for j, (g, s, act) in enumerate(entries, q):
        row.extend([1+g*q+s, 1+k*q+g*a+act])
        col.extend([j, j]); data.extend([1., 1.])
    matrix = coo_matrix((data, (row, col)), shape=(1+k*q+k*a, q+len(entries))).tocsr()
    objective = np.zeros(q+len(entries))
    objective[:q] = [len(s) for s in subsets]
    return subsets, entries, matrix, objective


@dataclass
class SubsetCoupling:
    weights: np.ndarray
    conditional: np.ndarray
    objective: float
    solve_seconds: float
    residual: float

    def sample(self, rng, count=1):
        subsets = rng.choice(len(self.weights), size=count, p=self.weights)
        # Independent conditional actions are sufficient; the LP random subset
        # carries the coupling. This is not independent unconditional sampling.
        cdf = np.cumsum(self.conditional[subsets], axis=-1)
        cdf[..., -1] = 1.
        uniforms = rng.random(cdf.shape[:-1])[..., None]
        return (uniforms >= cdf).sum(axis=-1)


def solve_subset(probabilities, formulation="hall"):
    p = validate(probabilities)
    k, a = p.shape
    start = perf_counter()
    subsets, entries, matrix, objective = structure(k, a)
    q = len(subsets)
    if formulation == "hall":
        # Projection of the allocation variables by the transportation Hall
        # inequalities. The optimum depends on min_g p_g(T) for every subset T.
        masks = np.arange(1, 1 << a)
        membership = ((masks[:, None] >> np.arange(a)) & 1).astype(float)
        capacities = (p @ membership.T).min(axis=0)
        contained = (masks[None, :] & masks[:, None]) == masks[None, :]
        result = linprog(objective[:q], A_ub=contained.astype(float), b_ub=capacities,
                         A_eq=np.ones((1, q)), b_eq=[1.], bounds=(0, None),
                         method="highs", options={"threads": 2})
        if not result.success:
            raise RuntimeError(result.message)
        all_weights = np.maximum(result.x, 0.)
        residual = max(float(np.max(contained @ all_weights - capacities)),
                       abs(float(all_weights.sum()-1)))
        active = all_weights > 0
        weights = all_weights[active]; selected = [subsets[i] for i in np.flatnonzero(active)]
        allocation = np.stack([_allocation_flow(weights, selected, pg) for pg in p], axis=1)
        conditional = allocation / weights[:, None, None]
        conditional /= conditional.sum(axis=-1, keepdims=True)
        weights /= weights.sum()
        recovered = np.einsum("s,sga->ga", weights, conditional)
        if residual > 1e-7 or not np.allclose(recovered, p, atol=1e-7, rtol=0):
            raise RuntimeError("invalid Hall LP solution or transport marginals")
        return SubsetCoupling(weights, conditional, float(result.fun),
                              perf_counter()-start, residual)
    if formulation != "allocation":
        raise ValueError(formulation)
    rhs = np.r_[1., np.zeros(k*q), p.ravel()]
    solution = linprog(objective, A_eq=matrix, b_eq=rhs, bounds=(0, None),
                       method="highs", options={"threads": 2})
    if not solution.success:
        raise RuntimeError(f"coupling LP failed: {solution.message}")
    residual = float(np.max(np.abs(matrix @ solution.x - rhs)))
    if residual > 1e-7 or np.min(solution.x) < -1e-8:
        raise RuntimeError(f"invalid numerical solution: residual={residual}")
    weights = np.maximum(solution.x[:q], 0)
    allocation = np.zeros((q, k, a))
    for value, (g, s, act) in zip(solution.x[q:], entries):
        allocation[s, g, act] = max(value, 0.)
    # Keep every positive subset mass; deleting tiny masses would change p.
    active = weights > 0
    weights = weights[active]
    conditional = allocation[active] / weights[:, None, None]
    conditional /= conditional.sum(axis=-1, keepdims=True)
    weights /= weights.sum()
    recovered = np.einsum("s,sga->ga", weights, conditional)
    if not np.allclose(recovered, p, atol=1e-7, rtol=0):
        raise RuntimeError("postprocessed coupling has incorrect marginals")
    return SubsetCoupling(weights, conditional, float(solution.fun),
                          perf_counter()-start, residual)


def solve_joint(probabilities):
    """Independent exponential-size exact oracle, only for tiny test cases."""
    p = validate(probabilities)
    k, a = p.shape
    assignments = np.array(list(product(range(a), repeat=k)))
    constraints = np.array([(assignments[:, g] == act).astype(float)
                            for g in range(k) for act in range(a)])
    cost = np.array([len(set(x)) for x in assignments], dtype=float)
    result = linprog(cost, A_eq=constraints, b_eq=p.ravel(), bounds=(0, None),
                     method="highs", options={"threads": 2})
    if not result.success:
        raise RuntimeError(result.message)
    return float(result.fun)


def list_sample(p, rng):
    """Recursive discrete list coupling, Phan et al. 2605.12807 Alg. 1.

    The unmatched variables have the specified residual marginals, and can
    themselves be coupled recursively. Matching partners are not fixed.
    """
    k, a = p.shape
    if k == 1:
        return np.array([rng.choice(a, p=p[0])])
    x = int(rng.choice(a, p=p[0]))
    others = p[1:]
    total = others.sum(axis=0)
    ratio = np.divide(p[0], total, out=np.ones(a), where=total > 0)
    inclusion = np.minimum(1., ratio)
    residual = others * (1. - inclusion)
    masses = residual.sum(axis=1)
    matched = rng.random() < min(1., total[x]/p[0, x])
    partner = int(rng.choice(k-1, p=others[:, x]/total[x])) if matched else None
    ids = [j for j in range(k-1) if j != partner]
    output = np.empty(k, dtype=int); output[0] = x
    if partner is not None:
        output[partner+1] = x
    if ids:
        if (masses[ids] <= 0).any():
            raise RuntimeError("sampled a zero-probability unmatched event")
        conditional = residual[ids]/masses[ids, None]
        output[np.array(ids)+1] = list_sample(conditional, rng)
    return output


def optimal_uniform_order(probabilities):
    """Exact enumeration of action orders for the shared inverse-CDF baseline.

    Intended only for A<=6; this has A! order-search cost, reported separately.
    The integral is exact apart from floating arithmetic, not estimated by MC.
    """
    p = validate(probabilities)
    _, a = p.shape
    best_cost, best_order = np.inf, None
    for order in permutations(range(a)):
        cdf = np.cumsum(p[:, order], axis=1); cdf[:, -1] = 1.
        edges = np.unique(np.r_[0., cdf.ravel()])
        mid = (edges[:-1]+edges[1:])/2
        choices = (mid[:, None, None] >= cdf[None]).sum(axis=-1)
        distinct = np.array([len(set(x)) for x in choices])
        cost = float(distinct @ np.diff(edges))
        if cost < best_cost:
            best_cost, best_order = cost, np.array(order)
    return best_order, best_cost


def sample(probabilities, method, rng, count=1, coupling=None, order=None):
    p = validate(probabilities)
    k, a = p.shape
    if method == "subset-lp":
        if coupling is None:
            coupling = solve_subset(p)
        return coupling.sample(rng, count)
    if method == "list":
        return np.stack([list_sample(p, rng) for _ in range(count)])
    if method == "gumbel":
        noise = rng.gumbel(size=(count, 1, a))
        logits = np.full_like(p, -np.inf)
        np.log(p, out=logits, where=p > 0)
        return (logits[None]+noise).argmax(axis=-1)
    if method == "ordered-uniform":
        if order is None:
            order, _ = optimal_uniform_order(p)
        ordered_actions = sample(p[:, order], "uniform", rng, count)
        return order[ordered_actions]
    if method not in ("independent", "uniform"):
        raise ValueError(method)
    uniforms = rng.random((count, k if method == "independent" else 1, 1))
    cdf = np.cumsum(p, axis=-1); cdf[:, -1] = 1.
    return (uniforms >= cdf[None]).sum(axis=-1)
