import itertools
import numpy as np
from experiments.adaptation.task import make_graphs, make_cases, transition, optimal_actions
from experiments.adaptation.run_pilot import dataset, query
from experiments.adaptation.model import inputs
from experiments.adaptation.train_query_prefix import closure_key, training_queries


def test_known_dependency_and_failure():
    graph = np.zeros((3,3), dtype=bool)
    graph[0,2] = graph[1,2] = True
    state = np.zeros(3, dtype=np.float32)
    after, ok = transition(graph, state, 2)
    assert not ok and np.array_equal(state, after)
    goal = np.array([0,0,1], dtype=np.float32)
    np.testing.assert_array_equal(optimal_actions(graph, state, goal), [.5,.5,0,0])
    for a in [1,0,2]:
        state, ok = transition(graph, state, a)
        assert ok
    np.testing.assert_array_equal(optimal_actions(graph, state, goal), [0,0,0,1])


def test_oracle_against_exhaustive_shortest_paths():
    rng = np.random.default_rng(4)
    for graph in make_graphs(rng, 15, 3):
        for mask in range(1,8):
            goal = np.array([(mask >> i)&1 for i in range(3)], dtype=np.float32)
            shortest = None
            first_actions = set()
            for length in range(1,4):
                for path in itertools.permutations(range(3), length):
                    state = np.zeros(3, dtype=np.float32)
                    for a in path:
                        state, _ = transition(graph, state, a)
                    if np.all(state[goal.astype(bool)]):
                        shortest = length
                        first_actions.add(path[0])
                if shortest is not None:
                    break
            assert set(np.flatnonzero(optimal_actions(graph, np.zeros(3), goal))) == first_actions


def test_commands_rule_independent_and_receipts_replayable():
    graph1 = np.zeros((5,5), dtype=bool)
    graph2 = graph1.copy()
    graph2[0,4] = True
    one = make_cases([graph1], np.random.default_rng(99), 32, 12)
    two = make_cases([graph2], np.random.default_rng(99), 32, 12)
    for a,b in zip(one,two):
        np.testing.assert_array_equal(a.history[:,5:10], b.history[:,5:10])
        np.testing.assert_array_equal(a.source_goal, b.source_goal)
        np.testing.assert_array_equal(a.new_goal, b.new_goal)
        state = np.zeros(5, dtype=np.float32)
        for token in b.history:
            action = token[5:10].argmax()
            after, ok = transition(graph2, state, int(action))
            np.testing.assert_array_equal(token[:5], state)
            np.testing.assert_array_equal(token[10:15], after)
            assert token[15] == float(ok)
            state = after


def test_disjoint_worlds_reset_and_no_graph_in_policy_input():
    train, test, counts = dataset(42, 16, 8, 2, 2)
    assert not ({c.graph.tobytes() for c in train} & {c.graph.tobytes() for c in test})
    for c in test:
        state, goal = query(c, "different-goal-reset")
        assert not state.any() and np.array_equal(goal, c.new_goal)
        tensors = inputs([c.history], [state], [goal], 5)
        assert tensors[0].shape[2] == 21
        assert tensors[2].shape == tensors[3].shape == (1,5)
        altered = c.graph.copy()
        c.graph = ~altered
        again = inputs([c.history], [state], [goal], 5)
        assert all(np.array_equal(a.numpy(), b.numpy()) for a,b in zip(tensors, again))
        c.graph = altered


def test_redundant_edges_do_not_create_new_behavioral_rule():
    chain = np.zeros((5,5), dtype=bool)
    chain[0,1] = chain[1,2] = True
    redundant = chain.copy(); redundant[0,2] = True
    assert not np.array_equal(chain,redundant)
    assert closure_key(chain) == closure_key(redundant)
    for commands in itertools.permutations(range(5)):
        states = [np.zeros(5,dtype=np.float32),np.zeros(5,dtype=np.float32)]
        for a in commands:
            one,ok1 = transition(chain,states[0],a)
            two,ok2 = transition(redundant,states[1],a)
            assert ok1 == ok2 and np.array_equal(one,two)
            states = [one,two]


def test_coverage_arms_share_receipts_and_active_labels():
    rng = np.random.default_rng(314)
    cases = make_cases(make_graphs(rng,8,5),rng,8,12)
    full = training_queries(cases,"covered-query")
    zero = training_queries(cases,"zero-query")
    assert full[3:] == zero[3:]
    assert any(np.any(s) for s in full[1])
    for c,h,s,g,h0,s0,g0 in zip(cases,*full[:3],*zero[:3]):
        np.testing.assert_array_equal(h,h0)
        np.testing.assert_array_equal(g,g0)
        assert not s0.any()
        assert not np.all(s[g.astype(bool)])
        assert optimal_actions(c.graph,s,g)[-1] == optimal_actions(c.graph,s0,g0)[-1] == 0
        prefix=h[len(c.history):]
        replay=np.zeros(5,dtype=np.float32)
        for token in prefix:
            action=int(token[5:10].argmax())
            np.testing.assert_array_equal(token[:5],replay)
            replay,ok=transition(c.graph,replay,action)
            np.testing.assert_array_equal(token[10:15],replay)
            assert token[15] == float(ok)
        np.testing.assert_array_equal(replay,s)
