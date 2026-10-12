import unittest
import numpy as np
import torch
from experiments.adaptation.task_stream import rollout


class FixedPolicy:
    n = 2
    def __init__(self, stop=False): self.stop = stop
    def eval(self): return self
    def __call__(self, tokens, lengths, states, goals):
        logits = torch.zeros((len(states), 3))
        for i, state in enumerate(states):
            logits[i, 2 if self.stop else 0 if state[0] == 0 else 1] = 1
        return logits


class StreamContracts(unittest.TestCase):
    def test_first_task_same_and_only_own_past_retained(self):
        graph = np.array([[False, True], [False, False]])
        goals = np.array([[[0, 1], [1, 0]]], dtype=np.float32)
        full = rollout(FixedPolicy(), [graph], [(0, 0)], goals, True)
        empty = rollout(FixedPolicy(), [graph], [(0, 0)], goals, False)
        self.assertEqual(full[0], {**empty[0], "retain": 1})
        self.assertEqual(full[1]["initial_receipts"], 2)
        self.assertEqual(empty[1]["initial_receipts"], 0)
        self.assertEqual(full[1]["capped_commands"], 1)
        self.assertEqual(full[1]["between_task_reset"], 1)

    def test_early_stop_does_not_escape_failure_charge_or_future_tasks(self):
        graph = np.zeros((2, 2), dtype=bool)
        goals = np.array([[[0, 1], [1, 0]]], dtype=np.float32)
        rows = rollout(FixedPolicy(stop=True), [graph], [(0, 0)], goals, True)
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["actual_commands"] == 0 and r["capped_commands"] == 12 and r["premature_stop"] == 1 for r in rows))


if __name__ == "__main__": unittest.main()
