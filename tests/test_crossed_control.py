import unittest
import numpy as np
from experiments.coupled_rollouts.crossed_control import joint,joint_from_marginals,crossed_readout,PATTERNS,A_INDEX,B_INDEX
from experiments.coupled_rollouts.recovery_contrast import sigmoid,offset


class CrossedControlTests(unittest.TestCase):
    def test_conditioned_margin_patterns_and_independent_joint(self):
        admissible=[]
        for i,y in enumerate(PATTERNS):
            table=y.reshape(2,2)
            if np.all(table.sum(0)==1) and np.all(table.sum(1)==1):admissible.append(i)
        self.assertEqual(set(admissible),{A_INDEX,B_INDEX})
        probs,p=joint(-1.,.7,-.7,2.,1.)
        explicit=np.array([np.prod([p[j] if v else 1-p[j] for j,v in enumerate(y)]) for y in PATTERNS])
        np.testing.assert_allclose(probs,explicit,atol=1e-14,rtol=1e-13)
        self.assertAlmostEqual(probs.sum(),1.,places=13)

    def test_nuisance_cancellation_and_selection(self):
        for eta,ua,uc,motor,effect in [(-3.,.7,-.7,2.,1.),(2.,-.7,.7,-2.,0.),(4.,.7,.7,1.,-2.)]:
            probs,_=joint(eta,ua,uc,motor,effect)
            q,mass,info=crossed_readout(probs,1.,.3)
            self.assertAlmostEqual(q,float(sigmoid(effect+offset(1.,.3))),places=13)
            self.assertGreater(mass,0.);self.assertAlmostEqual(info,mass*q*(1-q),places=13)

    def test_target_alias_and_violations(self):
        p1,m1=joint(0.,0.,0.,0.,1.)
        p2,m2=joint(0.,0.,0.,1.,0.)
        np.testing.assert_array_equal(m1[:2],m2[:2])
        self.assertGreater(np.abs(p1-p2).sum()/2,.2)
        for kappa,delta in [(1.,0.),(0.,1.)]:
            probs,_=joint(0.,.7,-.7,.5,0.,kappa,delta)
            q,_,_=crossed_readout(probs)
            self.assertAlmostEqual(q,float(sigmoid(delta-kappa)),places=13)

    def test_invalid_joint_and_support(self):
        probs,_=joint(0.,0.,0.,0.,0.)
        for a,b in [(0.,1.),(1.,0.),(1.1,1.)]:
            with self.assertRaises(ValueError):crossed_readout(probs,a,b)
        with self.assertRaises(ValueError):crossed_readout(np.ones(16))
        with self.assertRaises(ValueError):joint(np.nan,0.,0.,0.,0.)

    def test_shared_physical_multiplier_does_not_imply_parallel_logit_response(self):
        p=np.array([.9*.4,.9*.8,.4*.4,.4*.8])
        probabilities=joint_from_marginals(p)
        q,_,_=crossed_readout(probabilities)
        logits=np.log(p)-np.log1p(-p)
        contrast=logits[1]+logits[2]-logits[0]-logits[3]
        self.assertGreater(abs(q-.5),.1)
        self.assertAlmostEqual(q,float(sigmoid(contrast)),places=13)


if __name__=='__main__':unittest.main()
