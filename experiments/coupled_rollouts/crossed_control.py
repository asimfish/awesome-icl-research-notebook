"""Exact four-corner control diagnostic; no policy training or physical calls."""
import argparse
import csv
import itertools
import json
from pathlib import Path
from time import perf_counter

import numpy as np
from .recovery_contrast import sigmoid, offset


PATTERNS = np.array(list(itertools.product((0, 1), repeat=4)), dtype=int)
A_INDEX = next(i for i, y in enumerate(PATTERNS) if tuple(y)==(0,1,1,0))
B_INDEX = next(i for i, y in enumerate(PATTERNS) if tuple(y)==(1,0,0,1))


def joint_from_marginals(probabilities):
    p=np.asarray(probabilities, dtype=float)
    if p.shape != (4,) or not np.all(np.isfinite(p)) or np.any(p<=0) or np.any(p>=1):
        raise ValueError('four strictly interior finite probabilities required')
    return np.prod(np.where(PATTERNS, p[None,:], 1-p[None,:]),axis=1)


def joint(eta, ua, uc, motor_shift, effect, control_effect=0., target_motor_extra=0.):
    """Independent innovations conditional on the specified quadruple nuisances."""
    logits = np.array([eta+ua, eta+ua+motor_shift+effect+target_motor_extra,
                       eta+uc, eta+uc+motor_shift+control_effect], dtype=float)
    if not np.all(np.isfinite(logits)):
        raise ValueError('finite logits required')
    probabilities = np.exp(PATTERNS @ logits - np.logaddexp(0., logits).sum())
    return probabilities, sigmoid(logits)


def crossed_readout(probabilities, retain_a=1., retain_b=1.):
    probabilities = np.asarray(probabilities, dtype=float)
    if probabilities.shape != (16,) or not np.all(np.isfinite(probabilities)) or np.any(probabilities < 0):
        raise ValueError('16 nonnegative finite joint probabilities required')
    if not np.isclose(probabilities.sum(), 1., atol=1e-12, rtol=1e-12):
        raise ValueError('joint probabilities must sum to one')
    offset(retain_a, retain_b)  # full positive analyzed-pattern support, no epsilon
    a, b = probabilities[A_INDEX]*retain_a, probabilities[B_INDEX]*retain_b
    mass = a+b
    if mass == 0:
        return None, 0., 0.
    q = a/mass
    return float(q), float(mass), float(mass*q*(1-q))


def run(output):
    output.mkdir(parents=True, exist_ok=False); start=perf_counter()
    cells=[]
    for effect, motor, eta, ua, uc in itertools.product((-2.,0.,2.), (-2.,0.,2.),
                                                      (-2.,0.,2.), (-.7,.7), (-.7,.7)):
        probabilities, p=joint(eta,ua,uc,motor,effect)
        q,mass,information=crossed_readout(probabilities)
        m01, m10=(1-p[0])*p[1], p[0]*(1-p[1])
        target_q=float(m01/(m01+m10))
        cells.append(dict(effect=effect,motor_shift=motor,eta=eta,ua=ua,uc=uc,
                          crossed_orientation=q,crossed_predicted=float(sigmoid(effect)),
                          crossed_error=abs(q-float(sigmoid(effect))),
                          target_only_orientation=target_q,
                          target_only_task_only_prediction=float(sigmoid(effect)),
                          target_only_confounded_error=abs(target_q-float(sigmoid(effect))),
                          informative_pattern_mass=mass,
                          information_per_four_option_executions=information,
                          information_per_option_execution=information/4,
                          target_information_per_two_option_executions=float((m01+m10)*target_q*(1-target_q)),
                          full_joint_normalization_error=abs(float(probabilities.sum())-1)))
    mixtures=[]
    nuisances=[(-3.,-.7,.7,2.),(0.,.7,-.7,-2.),(2.,.7,.7,1.),(4.,-.7,-.7,-1.)]
    for effect in (-2.,0.,2.):
        probability=np.array([.1,.2,.3,.4]) @ np.array([joint(*v,effect)[0] for v in nuisances])
        q,mass,info=crossed_readout(probability)
        mixtures.append(dict(effect=effect,probability=q,expected=float(sigmoid(effect)),
                             error=abs(q-float(sigmoid(effect))),informative_mass=mass,
                             information_per_four_executions=info))
    p1,marg1=joint(0.,0.,0.,0.,1.)
    p2,marg2=joint(0.,0.,0.,1.,0.)
    alias=dict(world1=dict(effect=1.,motor_shift=0.),world2=dict(effect=0.,motor_shift=1.),
               target_marginal_max_difference=float(np.abs(marg1[:2]-marg2[:2]).max()),
               four_corner_total_variation=float(np.abs(p1-p2).sum()/2),
               crossed_world1=crossed_readout(p1)[0],crossed_world2=crossed_readout(p2)[0])
    violations=[]
    for name,kappa,delta in [('control_task_contamination',1.,0.),('differential_motor_shift',0.,1.)]:
        probabilities,_=joint(0.,.7,-.7,.5,0.,kappa,delta)
        q,mass,_=crossed_readout(probabilities)
        violations.append(dict(scenario=name,true_task_effect=0.,control_effect=kappa,
                               differential_motor_shift=delta,observed_orientation=q,
                               actual_effect_prediction=float(sigmoid(delta-kappa)),
                               actual_effect_error=abs(q-float(sigmoid(delta-kappa))),
                               unconfounded_claim_error=abs(q-.5),informative_mass=mass))
    p=np.array([.9*.4,.9*.8,.4*.4,.4*.8])
    q,mass,_=crossed_readout(joint_from_marginals(p))
    logits=np.log(p)-np.log1p(-p)
    effective=float(logits[1]+logits[2]-logits[0]-logits[3])
    violations.append(dict(scenario='constant_task_efficacy_common_multiplicative_motor_change',
                           task_efficacies=[.9,.4],motor_factors=[.4,.8],
                           task_efficacy_changed=False,observed_orientation=q,
                           induced_logit_interaction=effective,
                           actual_effect_prediction=float(sigmoid(effective)),
                           actual_effect_error=abs(q-float(sigmoid(effective))),
                           mistaken_no_interaction_error=abs(q-.5),informative_mass=mass))
    probabilities,_=joint(.5,.7,-.7,2.,1.)
    q,mass,_=crossed_readout(probabilities,1.,.3)
    retention=dict(retain_a=1.,retain_b=.3,orientation=q,
                   corrected_prediction=float(sigmoid(1.+offset(1.,.3))),
                   corrected_error=abs(q-float(sigmoid(1.+offset(1.,.3)))),
                   error_ignoring_retention=abs(q-float(sigmoid(1.))),analyzed_mass=mass)
    result=dict(scope='exact crossed-control identification diagnostic; classical conditional readout',
                cells=cells,grid_cells=len(cells),mixtures=mixtures,
                target_only_alias=alias,violations=violations,retention_control=retention,
                maximum_crossed_error=max(x['crossed_error'] for x in cells),
                maximum_target_only_task_error=max(x['target_only_confounded_error'] for x in cells),
                informative_mass_range=[min(x['informative_pattern_mass'] for x in cells),
                                        max(x['informative_pattern_mass'] for x in cells)],
                option_calls_per_complete_quadruple=4,
                runtime_seconds=perf_counter()-start,trained_models=0,sampled_episodes=0,physical_episodes=0,
                limits=['No novel statistical identity, identified physical task graph, or policy benefit',
                        'Task-inert control and equal additive motor shift are enforced model restrictions',
                        'All 16 patterns charged; only the two crossed patterns inform this conditional likelihood',
                        'Four option executions exclude reset/preparation/control matching costs',
                        'Target-only information estimates the combined task-plus-motor coefficient',
                        'A finite-grid identity is not a nuisance-shift learning experiment'])
    with (output/'cells.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(cells[0]));w.writeheader();w.writerows(cells)
    (output/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False))
    print(json.dumps({k:v for k,v in result.items() if k not in ('cells','mixtures')}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
