import unittest
import numpy as np
from experiments.coupled_rollouts.erasure_credit import leaves, cell, blocked_posterior, coupled_leaves


class ErasureEstimatorTests(unittest.TestCase):
    def test_conditional_erasure_identities(self):
        for q, t in ((.5, 2), (.8, 4), (.95, 6)):
            for r in (False, True):
                for z in (0, 1):
                    paths = leaves(z, r, q, t)
                    empty = leaves(z, False, q, t)
                    target = sum(x.probability*x.commands for x in empty)
                    self.assertAlmostEqual(sum(x.probability*x.full_weight for x in paths), 1, places=10)
                    self.assertAlmostEqual(sum(x.probability*x.full_weight*x.commands for x in paths), target, places=10)
                    self.assertAlmostEqual(sum(x.probability*x.prefix_control for x in paths), target, places=10)

    def test_gradient_matches_finite_difference(self):
        theta, epsilon = .37, 1e-5
        p = 1/(1+np.exp(-theta))
        result = cell(.8, 4, .1, p)
        c0, c1 = result["mean_cost_no_information"], result["mean_cost_information"]
        def objective(x):
            probability = 1/(1+np.exp(-x))
            return (1-probability)*c0+probability*c1
        derivative = (objective(theta+epsilon)-objective(theta-epsilon))/(2*epsilon)
        for method in result["methods"]:
            self.assertAlmostEqual(method["gradient_mean"], derivative, places=8, msg=method["method"])

    def test_no_information_gives_unit_likelihood_ratios(self):
        for path in leaves(0, False, .8, 6):
            self.assertAlmostEqual(path.full_weight, 1, places=12)
            self.assertAlmostEqual(path.prefix_control, path.commands, places=12)

    def test_blocked_receipt_updates_both_consumers_by_same_legal_likelihood(self):
        self.assertAlmostEqual(blocked_posterior(.5, 0, .8), 1/6)
        self.assertAlmostEqual(blocked_posterior(.5, 1, .8), 5/6)
        self.assertEqual(blocked_posterior(1, 0, .8), 1)

    def test_coupled_comparator_preserves_both_query_marginals(self):
        for r in (False, True):
            paths = coupled_leaves(0, r, .8, 4)
            for branch, informative in (("retained_commands", r), ("erased_commands", False)):
                actual = np.array([sum(x.probability for x in paths if getattr(x, branch) == t)
                                   for t in range(1, 5)])
                independent = leaves(0, informative, .8, 4)
                expected = np.array([sum(x.probability for x in independent if x.commands == t)
                                     for t in range(1, 5)])
                np.testing.assert_allclose(actual, expected, atol=1e-12, rtol=0)
            if not r:
                self.assertTrue(all(x.retained_commands == x.erased_commands == x.transition_calls == x.scoring_calls
                                    for x in paths))

    def test_balanced_trajectory_mixture_has_correct_cost_targets(self):
        for z in (0, 1):
            paths = leaves(z, True, .8, 6)
            masses = np.array([x.probability*(1+x.full_weight)/2 for x in paths])
            self.assertAlmostEqual(masses.sum(), 1, places=10)
            retained_cost = sum(x.probability*x.commands for x in paths)
            empty_cost = sum(x.probability*x.commands for x in leaves(z, False, .8, 6))
            self.assertAlmostEqual(sum(m*x.balanced_target for m, x in zip(masses, paths)), retained_cost, places=10)
            self.assertAlmostEqual(sum(m*x.balanced_control for m, x in zip(masses, paths)), empty_cost, places=10)
            self.assertTrue(all(0 <= x.balanced_target <= 2*x.commands and
                                0 <= x.balanced_control <= 2*x.commands for x in paths))


if __name__ == "__main__":
    unittest.main()
