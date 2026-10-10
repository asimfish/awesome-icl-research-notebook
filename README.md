# awesome ICL — public research notebook

Static, bilingual research website for the frozen-PIM experience audit. No build dependencies, external fonts, trackers, embedded policy weights, or private experiment payloads.

Repository: [asimfish/awesome-icl-research-notebook](https://github.com/asimfish/awesome-icl-research-notebook).

## Preview

From this directory:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/?lang=en&view=overview`. Supported views: `overview`, `proposal`, `evidence`, `timeline`. HTTP is required to load the JSON snapshot; double-clicking the HTML file is insufficient.

## Update

Edit `data/progress.json` using verified saved reports. Preserve the distinction between planned formal experiments, diagnostic executions, incomplete records, and qualified evidence. Review counts are not sample sizes. `updated_at` is the public snapshot time. An unknown count stays unknown. Never export raw `.aris`, `results`, machine paths, credentials, process addresses, or private arrays. Set `repository_url` only after the actual public repository is known.

The website is a public summary. Research source protocols remain unchanged. The current proposal is conditioned on shared nominal calibration R₀, frozen parameters, researcher-controlled memory transplantation, and disabled success replay. Full restoration B, physical C, matched-observation C, and formal query evaluation remain unqualified.

## GitHub Pages

Publish **only this directory** in a dedicated repository. The workflow stages only `index.html`, `styles.css`, `app.js`, `.nojekyll`, `assets/`, and `data/`; it never packages the parent research workspace. In the repository's **Settings → Pages**, select **GitHub Actions**. The provided workflow deploys pushes to `main` or a manual dispatch. Adjust that branch if the actual repository uses another default branch.

The repository uses GitHub Actions for Pages publication. Deploy pushes to the unprotected main branch, then verify the completed workflow and actual site. Only a successful workflow and checked public URL count as a publication result.

## References

Content is derived from this project's saved design and execution records. Presentation references supplied by the user: [interactive report](https://anonymous-report-421.github.io/public-website/?lang=en&view=), [RoboDojo report](https://robodojo-benchmark.com/report/gpt-6-astra-eval), and [Awesome Astra Embodied AI](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI). The site uses original copy, layout, and SVG artwork; it does not import their assets or results.

## Validate public files

```sh
python3 tools/validate_public_site.py
```

The validator checks the public snapshot, local assets, publication workflow and secret/private-path boundary. Git checkout metadata is excluded. Research diagnostics and formal qualification retain their reported status after publication.
