import unittest
import numpy as np
from experiments.coupled_rollouts.recovery_contrast import (
    cell, discordant_masses, offset, orientation, sigmoid)


class ConditionalEvidenceTests(unittest.TestCase):
    def test_exact_full_inclusion_identity(self):
        for eta in (-7., -1., 4.):
            for effect in (-3., 0., 2.):
                m01, m10 = discordant_masses(eta, effect)
                q, mass, _ = orientation(m01, m10, .7, .1, .6, .3)
                self.assertGreater(mass, 0)
                self.assertAlmostEqual(q, float(sigmoid(effect+offset(.7,.1,.6,.3))), places=13)

    def test_no_information_without_reverse_orientation(self):
        for effect in (-3., 0., 4.):
            c = cell(effect, 0., 0.)
            self.assertEqual(c['observed_orientation_probability'], 1.)
            self.assertEqual(c['conditional_information_per_first_attempt'], 0.)
            self.assertIsNone(c['corrected_prediction'])
            with self.assertRaises(ValueError): offset(1., 0.)

    def test_marginals_are_insufficient_and_nuisance_drift_is_confounding(self):
        m01, m10 = discordant_masses(0., 2., shared_uniform=True)
        q, _, _ = orientation(m01,m10,1.,1.)
        self.assertEqual(q, 1.)
        self.assertGreater(abs(q-float(sigmoid(2.))), .1)
        m01, m10 = discordant_masses(0., 0., second_nuisance_shift=1.)
        q, _, _ = orientation(m01,m10,1.,1.)
        self.assertAlmostEqual(q, float(sigmoid(1.)), places=13)
        self.assertGreater(abs(q-.5), .2)

    def test_invalid_probabilities(self):
        for v in (0., -1., 1.1, np.nan):
            with self.assertRaises(ValueError): offset(1., v)
        with self.assertRaises(ValueError): orientation(.2, .3, -1., 1.)


if __name__ == '__main__': unittest.main()
