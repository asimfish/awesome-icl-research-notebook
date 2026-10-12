"""Test a physical control's parallel-logit assumption; not robot learning."""
import argparse
import csv
import json
from pathlib import Path
from time import perf_counter

import mujoco
import numpy as np


def model_for(friction):
    if not np.isfinite(friction) or friction <= 0:
        raise ValueError('positive friction required')
    return mujoco.MjModel.from_xml_string(f'''<mujoco>
    <option timestep="0.005" gravity="0 0 -9.81"/>
    <worldbody><geom type="plane" size="5 5 .1" friction="{friction} .005 .0001"/>
    <body pos="0 0 .06"><freejoint/><geom type="box" size=".05 .05 .05" mass="1"
    friction="{friction} .005 .0001"/></body></worldbody></mujoco>''')


def execute(model, data, force, settle_steps=20, driven_steps=100):
    if not np.isfinite(force) or force < 0 or settle_steps < 0 or driven_steps <= 0:
        raise ValueError('finite nonnegative force and valid step counts required')
    mujoco.mj_resetData(model,data)
    for _ in range(settle_steps): mujoco.mj_step(model,data)
    before=float(data.qpos[0]); data.xfrc_applied[1,0]=force
    for _ in range(driven_steps): mujoco.mj_step(model,data)
    if not np.all(np.isfinite(data.qpos)) or not np.all(np.isfinite(data.qvel)):
        raise RuntimeError('nonfinite physical state')
    return float(data.qpos[0]-before)


def posterior(regime_counts, rng):
    rates={k:rng.beta(n+0.5,1500-n+0.5,size=10000) for k,n in regime_counts.items()}
    logit=lambda x:np.log(x)-np.log1p(-x)
    target=logit(rates['target1'])-logit(rates['target0'])
    control=logit(rates['control1'])-logit(rates['control0'])
    contrast=target-control
    summary=lambda x:dict(posterior_mean=float(x.mean()),posterior_95_interval=np.quantile(x,[.025,.975]).tolist())
    return dict(target_logit_shift=summary(target),control_logit_shift=summary(control),
                logit_shift_difference=summary(contrast))


def run(output):
    output.mkdir(parents=True,exist_ok=False);start=perf_counter()
    count=1500;rng=np.random.default_rng(6651)
    cells=[]
    for mean in (6.,8.):
        for option,threshold in [('target',.20),('control',.02)]:
            for state,friction in [(0,.6),(1,.3)]:
                cells.append((mean,option,threshold,state,friction,np.maximum(0,rng.normal(mean,2.,size=count))))
    models={f:model_for(f) for f in (.6,.3)}
    data={f:mujoco.MjData(m) for f,m in models.items()}
    rows=[];statistics=[];regime_counts={6.:{},8.:{}}
    for mean,option,threshold,state,friction,forces in cells:
        successes=0
        for trial,force in enumerate(forces):
            displacement=execute(models[friction],data[friction],float(force))
            success=int(displacement >= threshold);successes+=success
            rows.append(dict(force_mean=mean,option=option,motor_state=state,friction=friction,
                             trial_id=trial,force_newtons=float(force),threshold_meters=threshold,
                             displacement_meters=displacement,success=success,resets=1,
                             settling_steps=20,driven_steps=100))
        statistics.append(dict(force_mean=mean,option=option,motor_state=state,friction=friction,
                               successes=successes,trials=count,rate=successes/count))
        regime_counts[mean][f'{option}{state}']=successes
        print(json.dumps(statistics[-1]),flush=True)
    analysis_rng=np.random.default_rng(6652)
    analysis={str(k):posterior(v,analysis_rng) for k,v in regime_counts.items()}
    report=dict(scope='motor-only parallel-logit control falsification; headless sliding physics',
                simulator='MuJoCo',version=mujoco.__version__,device='CPU',rendering=False,
                data_seed=6651,posterior_seed=6652,cells=statistics,analysis=analysis,
                uncertainty='coordinate-wise 95% Jeffreys-binomial posterior intervals, not frequentist or simultaneous',
                beta_prior=[.5,.5],posterior_draws=10000,primitive_executions=len(rows),
                resets=len(rows),mujoco_steps=sum(r['settling_steps']+r['driven_steps'] for r in rows),
                new_policy_training_runs=0,robot_episodes=0,real_hardware_episodes=0,
                runtime_seconds=perf_counter()-start,
                limits=['No learned policy, robot controller, prerequisite changes or new-goal result',
                        'No claim of a realizable physical preparation: friction is directly configured',
                        'Can disqualify this chosen control pair; cannot refute all control constructions',
                        'No hidden task relation label or eligibility inference in this run',
                        'Both probability and completion predicate shape the measured logit response',
                        'Prior smoothing for descriptive rate uncertainty is not outcome-support creation'])
    with (output/'trials.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (output/'result.json').write_text(json.dumps(report,indent=2,allow_nan=False))
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
