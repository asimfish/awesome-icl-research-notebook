# awesome ICL — public research notebook

Static, bilingual research website examining whether robot correction training teaches reusable in-context adaptation. Earlier A3 sensing probes and frozen-PIM audits remain historical. No build dependencies, external fonts, trackers, embedded policy weights, or private experiment payloads.

Repository: [asimfish/awesome-icl-research-notebook](https://github.com/asimfish/awesome-icl-research-notebook).

## Preview

From this directory:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/?lang=en&view=overview`. Supported views: `overview`, `proposal`, `evidence`, `timeline`. HTTP is required to load the JSON snapshot; double-clicking the HTML file is insufficient.

## Update

Edit `data/progress.json` using verified saved reports. Preserve the distinction between planned formal experiments, diagnostic executions, incomplete records, and qualified evidence. Review counts are not sample sizes. `updated_at` is the public snapshot time. An unknown count stays unknown. Never export raw `.aris`, `results`, machine paths, credentials, process addresses, or private arrays. Set `repository_url` only after the actual public repository is known.

The revised plan is at `research-plan.html?lang=en`. Sixteen complete candidates received individual review. The current hypothesis asks whether correction experience teaches reusable adaptation after a physical reset and changed goal. [Full story](data/research-reframe.md), [direct priors](data/literature-reframe.md), and [experiment design](data/experiment-reframe.md) distinguish standard meta-RL/DPT objectives from an untested training finding. 15 CPU policy checkpoints have now completed. Symbolic control and conditional command costs are measured; robot episodes remain zero and the primary retention-completion criterion failed. See [results](data/pilot-results.md), [paper PDF](assets/paper-draft.pdf), and [paper draft](data/paper-draft.md). Reviews are same-family/provisional.

The A3 sensing pilot is archived inside an expandable section on that page; its earlier 16-call first probe and 120-call cap are historical constraints, not an active execution plan. Symbolic results remain analytical controls, not adaptation evidence.

The historical proposal remains at `?view=proposal`; its frozen parameters, nominal calibration R₀, memory-transplantation scope and disabled success replay remain unchanged. Full restoration B, physical C, matched-observation C and formal query evaluation are still unqualified.

## GitHub Pages

Publish **only this directory** in a dedicated repository. The workflow stages only `index.html`, `styles.css`, `app.js`, the three `research-plan` HTML/CSS/JS files, `.nojekyll`, `assets/`, and `data/`; it never packages the parent research workspace. In the repository's **Settings → Pages**, select **GitHub Actions**. The provided workflow deploys pushes to `main` or a manual dispatch. Adjust that branch if the actual repository uses another default branch.

The repository uses GitHub Actions for Pages publication. Deploy pushes to the unprotected main branch, then verify the completed workflow and actual site. Only a successful workflow and checked public URL count as a publication result.

## References

Content is derived from this project's saved design and execution records. Presentation references supplied by the user: [interactive report](https://anonymous-report-421.github.io/public-website/?lang=en&view=), [RoboDojo report](https://robodojo-benchmark.com/report/gpt-6-astra-eval), and [Awesome Astra Embodied AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI). The site uses original copy, layout, and SVG artwork; it does not import their assets or results.

## Validate public files

```sh
python3 tools/validate_public_site.py
```

The validator checks the public snapshot, local assets, publication workflow and secret/private-path boundary. Git checkout metadata is excluded. Research diagnostics and formal qualification retain their reported status after publication.

## Reproduce the CPU design controls

```sh
python3 tools/observability_design_probe.py --output /tmp/observability-design-probe.json
python3 tools/prepare_observability_stimuli.py --output /tmp/observability-stimuli
```

Compare the first output with `data/observability-design-check.json`. The second
regenerates `data/visual-stimuli/`. Both use Python standard-library only and zero
model/robot/GPU calls. The symbolic solver evaluates only two declared schedules,
accepting all ties; it is not a complete belief-space planner. Never serialize
evaluation-only fields, pack IDs or context IDs to the policy. The structured
prompt uses disclosed oracle parsing, not an implemented perception model.

## Archived A3 idea deepening

The [deepening report](data/idea-deepening.md) narrows the question to demonstration-conditioned sensing selection. Direct priors include See2Act, ActiveUMI and CIVIL. The 144 finite decision conditions expose unnecessary observation by a global-feature coverage extension in 24 conditions; these are not model trials or failure rates. Six typed pairs contain 12 records but only 10 unique inputs, without RGB or demonstrated sensing traces. Complete rule tables and manually declared observation effects are solved by classical decision trees. This remains a bounded capability probe, not an established benchmark or new method.

```sh
python3 tools/decision_relevance_probe.py --output /tmp/decision-relevance-probe.json
python3 tools/prepare_deepening_cases.py --output /tmp/critical-decision-cases.json
```

Compare with `data/decision-relevance-check.json` and `data/critical-decision-cases.json`. The original eight-pack / 16-call first gate and total 120-call cap are preserved as historical records; neither probe is the current plan. These archived probes used zero policy calls, robot episodes and GPU hours.

## Learned-policy reproduction

The repository includes `experiments/adaptation/` and `tests/test_adaptation_pilot.py`. The local evidence used Python 3.10, Torch 2.13.0+cu130 on CPU and NumPy 2.2.6; 2 Torch threads. Training needs Torch/NumPy. No pretrained model or GPU is required.

```sh
python3 -m pytest -q tests/test_adaptation_pilot.py
python3 -m experiments.adaptation.run_pilot --output results/current-s11 --variant current-correction --seed 11
python3 -m experiments.adaptation.train_query_prefix --output results/covered-query-s11 --condition covered-query --seed 11
```

Use seeds 11/29/47, original variants `current-correction`, `same-goal-reset`, `different-goal-reset`, and revised conditions `covered-query`, `zero-query`. Both main queues evaluate `full,empty` support; the original checkpoints each evaluate all three query arrangements. Main counts exclude diagnostic mask replays and reviewer replays. Output directories must be new. Aggregate source arrays, private traces and trained weights are not published. Public summaries distinguish support collection from query execution; existing-history efficiency is not net autonomous acquisition benefit.
