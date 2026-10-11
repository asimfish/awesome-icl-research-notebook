# awesome ICL — public research notebook

Static, bilingual research website for a demonstration-conditioned pre-grasp inspection pilot. Earlier frozen-PIM audit records remain available as historical designs. No build dependencies, external fonts, trackers, embedded policy weights, or private experiment payloads.

Repository: [asimfish/awesome-icl-research-notebook](https://github.com/asimfish/awesome-icl-research-notebook).

## Preview

From this directory:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/?lang=en&view=overview`. Supported views: `overview`, `proposal`, `evidence`, `timeline`. HTTP is required to load the JSON snapshot; double-clicking the HTML file is insufficient.

## Update

Edit `data/progress.json` using verified saved reports. Preserve the distinction between planned formal experiments, diagnostic executions, incomplete records, and qualified evidence. Review counts are not sample sizes. `updated_at` is the public snapshot time. An unknown count stays unknown. Never export raw `.aris`, `results`, machine paths, credentials, process addresses, or private arrays. Set `repository_url` only after the actual public repository is known.

The current plan is at `research-plan.html?lang=en`: crossed demonstrations bind a color or side-symbol rule for the same object. All 30 symbolic cases match classical observation cost; eight program-drawn input packs are prepared. No frozen-model or robot pilot has run. The six controls include an explicit same-evidence prompt. The first model probe is at most 16 requests, included in the total 120-call cap. Drawn inputs and hand-authored future costs do not validate physical occlusion or view feasibility.

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
