import unittest
import mujoco
import numpy as np
from experiments.physics_controls.motor_only import model_for,execute


class PhysicsControlTests(unittest.TestCase):
    def test_reset_reproducibility_and_actual_steps(self):
        m=model_for(.6);d=mujoco.MjData(m)
        a=execute(m,d,6.);b=execute(m,d,6.)
        self.assertEqual(a,b);self.assertTrue(np.isfinite(a))
        self.assertAlmostEqual(d.time,.6,places=12)
        self.assertAlmostEqual(m.geom_friction[0,0],.6)
        self.assertAlmostEqual(m.geom_friction[1,0],.6)

    def test_force_actually_moves_object_and_invalid_inputs(self):
        m=model_for(.6);d=mujoco.MjData(m)
        resting=execute(m,d,0.);pushed=execute(m,d,12.)
        self.assertLess(abs(resting),1e-10);self.assertGreater(pushed,.2)
        for force in (-1.,np.nan):
            with self.assertRaises(ValueError):execute(m,d,force)
        with self.assertRaises(ValueError):model_for(0.)


if __name__=='__main__':unittest.main()
