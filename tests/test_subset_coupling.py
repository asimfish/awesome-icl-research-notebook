import unittest
import numpy as np
from experiments.coupled_rollouts.coupling import solve_subset, solve_joint, sample, optimal_uniform_order


class CouplingContractTests(unittest.TestCase):
    def test_matches_independent_exact_joint_oracle(self):
        rng = np.random.default_rng(6512)
        for _ in range(12):
            p = rng.dirichlet(np.full(3, .5), size=3)
            solution = solve_subset(p)
            self.assertLess(solution.residual, 1e-7)
            self.assertAlmostEqual(solution.objective, solve_joint(p), places=7)
            self.assertAlmostEqual(solution.objective, solve_subset(p, "allocation").objective, places=7)

    def test_structural_extremes(self):
        p = np.repeat([[.2, .3, .5]], 7, axis=0)
        self.assertAlmostEqual(solve_subset(p).objective, 1., places=7)
        self.assertAlmostEqual(solve_subset(np.eye(3)).objective, 3., places=7)
        p = np.array([[.5, .5, 0], [0, .5, .5], [.5, 0, .5]])
        self.assertAlmostEqual(solve_subset(p).objective, 2., places=7)

    def test_cycle_gap_against_named_samplers(self):
        p = np.array([[.5, .5, 0, 0], [0, .5, .5, 0],
                      [0, 0, .5, .5], [.5, 0, 0, .5]])
        coupling = solve_subset(p)
        self.assertAlmostEqual(coupling.objective, 2., places=7)
        order, uniform_cost = optimal_uniform_order(p)
        self.assertAlmostEqual(uniform_cost, 2., places=7)
        expected = {"uniform": 3., "gumbel": 8/3, "list": 2.5, "subset-lp": 2.}
        for i, (method, value) in enumerate(expected.items()):
            actions = sample(p, method, np.random.default_rng(825+i), count=10000,
                             coupling=coupling if method == "subset-lp" else None)
            distinct = np.array([len(set(x)) for x in actions])
            self.assertLess(abs(distinct.mean()-value), .035, method)

    def test_tiny_positive_masses_are_not_dropped_by_flow(self):
        p = np.repeat([[1e-13, 1-1e-13]], 2, axis=0)
        solution = solve_subset(p)
        recovered = np.einsum("s,sga->ga", solution.weights, solution.conditional)
        self.assertTrue(np.isfinite(recovered).all())
        np.testing.assert_allclose(recovered, p, atol=1e-16, rtol=0)

    def test_all_sampler_marginals(self):
        p = np.array([[.05, .55, .4], [.2, 0, .8], [.5, .3, .2]])
        for i, method in enumerate(("independent", "uniform", "gumbel", "list", "subset-lp")):
            actions = sample(p, method, np.random.default_rng(6512+i), count=100000)
            observed = np.stack([(actions == a).mean(axis=0) for a in range(3)], axis=1)
            self.assertLess(float(np.abs(p-observed).max()), .008, method)

    def test_optimum_invariant_to_goal_and_action_permutations(self):
        p = np.random.default_rng(123).dirichlet(np.ones(4), size=5)
        reference = solve_subset(p).objective
        self.assertAlmostEqual(reference, solve_subset(p[::-1, [2, 0, 3, 1]]).objective, places=7)

    def test_invalid_marginals_rejected(self):
        for p in ([[1, 1]], [[-.1, 1.1]], [[np.nan, 1]], []):
            with self.assertRaises(ValueError):
                solve_subset(p)


if __name__ == "__main__":
    unittest.main()
