# Algorithm-search development evidence, 2026-10-12

Scientific status REVISE. No established new algorithm; no new training or robot episodes.
The prior paper and failed original single-query completion gate remain unchanged.

Read [candidate paper](../algorithm-candidate.md). Own-stream result is additional development evidence.
73728 symbolic policy evaluation branches; 12000 MuJoCo body-force primitives are separate units.
Analytic enumerations are not sampled robot episodes. Report all failures and negative results.

Run from the repository root into new, nonexistent output directories:

```sh
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 /usr/bin/python3 -m experiments.adaptation.task_stream --root data/algorithm-cycle/checkpoints --output /tmp/icl-own-stream-reproduction
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 /usr/bin/python3 -m experiments.physics_controls.motor_only --output /tmp/icl-control-reproduction
```

Observed environment: Python3.10, Torch2.13.0+cu130, NumPy2.2.6, MuJoCo3.3.7 on CPU.
No GPU or rendering required. Checkpoints are three previously trained ordinary covered-query policies; hashes in checkpoints.json. Their publication is not an additional training run.

The local legacy SciPy/Matplotlib installation needs system NumPy1.21.5 (`/usr/bin/python3 -s`) for the categorical LP experiment. That environment distinction is explicit; do not silently alter packages to reproduce results.

```sh
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 /usr/bin/python3 -s -m unittest discover -s tests -p 'test_subset_coupling.py'
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 /usr/bin/python3 -m unittest discover -s tests -p 'test_task_stream.py'
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 /usr/bin/python3 -m unittest discover -s tests -p 'test_physics_control.py'
```

Plans and raw JSON/CSV are included. Seeds and estimator definitions are fixed in their source/plan.
Rule bootstrap intervals are conditional on three frozen checkpoints. Physical rate intervals are coordinate-wise Jeffreys-binomial posterior intervals, not simultaneous or frequentist confidence guarantees.
