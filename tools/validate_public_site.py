"""Check the public publishing boundary and static site's data contract."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from datetime import datetime
import json
import re

ROOT = Path(__file__).resolve().parents[1]
checks = []


def check(name, condition):
    checks.append({'name': name, 'passed': bool(condition)})
    if not condition:
        raise AssertionError(name)


data = json.loads((ROOT / 'data/progress.json').read_text())
check('known_schema', data['schema'] == 'awesome-icl.public-progress.v1')
datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
records = data['records']
check('unique_record_ids', len({r['id'] for r in records}) == len(records))
check('known_record_states', all(r['status'] in ['verified', 'blocked', 'in_progress'] for r in records))
check('planned_condition_families_total_12', sum(r['count'] for r in data['groups']) == 12)
check('four_counterfactual_conditions', set(data['conditions']) == {'H11', 'H10', 'H01', 'H00'})
policy = data['publication_policy']
check('public_only_without_private_payloads', policy['public_only'] and not any(policy[k] for k in
      ['includes_private_payloads', 'includes_machine_paths', 'includes_credentials']))
check('formal_scope_not_promoted', policy['formal_queries_completed'] == 0 and not any(policy[k] for k in
      ['full_restore_B_qualified', 'physical_C_qualified', 'matched_C_qualified', 'reviewer_fresh']))
for row in records:
    datetime.fromisoformat(row['date'])
    for field in ['title', 'summary', 'metric_label', 'limits', 'next']:
        check('bilingual:' + row['id'] + ':' + field, set(row[field]) == {'zh', 'en'} and all(row[field].values()))
    for item in row['observations']:
        check('bilingual_observation:' + row['id'], set(item) == {'zh', 'en'} and all(item.values()))
    provenance = row['provenance']
    if 'review_checks' in provenance:
        checked, passed = provenance['review_checks']
        check('review_counts:' + row['id'], isinstance(checked, int) and isinstance(passed, int) and 0 <= passed <= checked)
    for key, value in provenance.items():
        if key.endswith('sha256'):
            check('full_SHA256:' + row['id'], re.fullmatch('[a-f0-9]{64}', value) is not None)
check('HTTPS_references', all(urlsplit(r['url']).scheme == 'https' for r in data['references']))


class Resources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.paths = [], []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'id' in values:
            self.ids.append(values['id'])
        for key in ['src', 'href']:
            if key in values:
                self.paths.append(values[key])


html = (ROOT / 'index.html').read_text()
parser = Resources()
parser.feed(html)
check('unique_HTML_ids', len(parser.ids) == len(set(parser.ids)))
for name in parser.paths:
    parts = urlsplit(name)
    if parts.scheme:
        check('only_HTTPS_external_links', parts.scheme == 'https')
        continue
    path = unquote(parts.path)
    if not path:
        continue
    resource = (ROOT / path).resolve()
    check('relative_resource_within_public_root:' + path, not path.startswith('/') and ROOT in resource.parents)
    check('resource_exists:' + path, resource.is_file())
check('no_remote_scripts_or_stylesheets', 'src="https://' not in html and 'href="https://' not in html)
check('CSP_no_eval_or_inline_script_permission', "script-src 'self'" in html and 'unsafe-eval' not in html and 'unsafe-inline' not in html)

# New plan: verify its publishing resources and science/evidence boundary.
plan = json.loads((ROOT / 'data/research-plan.json').read_text())
check('plan_schema', plan['schema'] == 'awesome-icl.research-plan.v1')
check('six_controls', len(plan['baselines']) == 6)
check('three_counterfactual_examples', len(plan['example']['cases']) == 3)
check('model_and_robot_counts_zero', [m['value'] for m in plan['metrics'][-2:]] == [0, 0])
for item in plan['baselines']:
    check('bilingual_control', set(item['name']) == set(item['purpose']) == {'zh', 'en'})
plan_html = (ROOT / 'research-plan.html').read_text()
plan_parser = Resources()
plan_parser.feed(plan_html)
check('unique_plan_HTML_ids', len(plan_parser.ids) == len(set(plan_parser.ids)))
for name in plan_parser.paths:
    parts = urlsplit(name)
    if parts.scheme:
        check('plan_HTTPS_external_links', parts.scheme == 'https')
        continue
    path = unquote(parts.path)
    if not path:
        continue
    resource = (ROOT / path).resolve()
    check('plan_resource:' + path, not path.startswith('/') and ROOT in resource.parents and resource.is_file())
check('plan_CSP', "script-src 'self'" in plan_html and 'unsafe-eval' not in plan_html and 'unsafe-inline' not in plan_html)
active = data['active_research']
check('reframe_review_without_scientific_promotion', active['candidate_count'] == 16 and
      active['scientific_status'] == 'REVISE' and active['review_independence'] == 'same-family' and
      active['acceptance_status'] == 'provisional')
pilot = json.loads((ROOT / 'data/learned-pilot.json').read_text())
check('learned_pilot_counts_match_evidence', active['learned_policy_evaluation_episodes'] == pilot['main_evaluation_branches'] and active['training_runs'] == pilot['training_runs'] == 15 and active['robot_episodes'] == pilot['robot_episodes'] == 0)
check('learned_pilot_not_promoted', pilot['original_primary_completion_support_gate'] == 'FAILED' and pilot['GPU_hours'] == 0 and 'symbolic' in pilot['scope'])
check('learned_pilot_novelty_and_collection_limits', '不是' in (ROOT / 'data/paper-story-zh.md').read_text() and pilot['fresh_cost_confirmation']['cost_excludes_initial_collection'])
check('old_primary_explicitly_archived', active['previous_primary'] == 'A3' and
      active['previous_primary_archived'] and
      '<details class="section" id="archived-probe">' in plan_html)
story = (ROOT / 'data/research-reframe.md').read_text()
check('standard_objective_novelty_boundary', '不是新损失' in story and '差分沿历史相消' in story)
check('independent_query_and_information_boundary', '核心查询采样器不依赖隐藏z' in story and
      '知情行为不能伪装' in story and '不进入测试输入' in story)
check('revised_documents_have_strong_priors', all(name in story for name in ['DPT', 'DREAM', 'E-RL²']))
probe = json.loads((ROOT / 'data/observability-design-check.json').read_text())
check('symbolic_negative_control_not_promoted', probe['cases'] == 30 and
      probe['candidate_and_classical_total_cost_equal_cases'] == 30 and
      probe['model_calls'] == probe['robot_episodes'] == probe['gpu_hours'] == 0)
check('all_tied_actions_accepted', probe['rows_with_multiple_optimal_first_actions'] == 5 and
      all(row['candidate_first_action'] in row['restricted_optimal_first_actions'] for row in probe['rows']))
packs = json.loads((ROOT / 'data/visual-stimuli/packs.json').read_text())
check('eight_drawn_packs_not_physical', packs['visual_packs'] == 8 and packs['paired_contexts'] == 4 and
      packs['model_calls'] == packs['robot_episodes'] == packs['gpu_hours'] == 0)
check('raw_visual_pairs_only_demos_change', packs['raw_pairs_only_support_images_change'])
check('oracle_parsing_disclosed', 'oracle' in packs['shared_evidence_control'])
for row in packs['rows']:
    packet = row['model_input']
    for image in packet['support_images'] + [packet['current_image']] + packet['history_images']:
        check('stimulus_asset_exists:' + image, (ROOT / 'data/visual-stimuli' / image).is_file())
check('new_plan_workflow_allowlist', 'cp research-plan.html research-plan.css research-plan.js _site/' in
      (ROOT / '.github/workflows/pages.yml').read_text())
decision = json.loads((ROOT / 'data/decision-relevance-check.json').read_text())
check('deepening_finite_counterexample_scope', decision['cases'] == 144 and
      decision['global_coverage_suboptimal_cases'] == 24 and
      decision['frozen_policy_model_calls'] == decision['robot_episodes'] == decision['gpu_hours'] == 0)
typed = json.loads((ROOT / 'data/critical-decision-cases.json').read_text())
check('typed_cases_not_independent_samples', typed['cases'] == 12 and typed['unique_inputs'] == 10 and
      len({json.dumps(row['input'], sort_keys=True) for row in typed['rows']}) == 10)
check('typed_pair_and_budget_boundary', typed['pairs'] == 6 and
      all(row['passed'] for row in typed['pair_checks']) and typed['total_model_call_cap_unchanged'] == 120 and
      typed['frozen_policy_model_calls'] == typed['robot_episodes'] == typed['gpu_hours'] == 0)

# Git metadata belongs to the checkout, not the public publishing surface.
paths = sorted(p for p in ROOT.rglob('*') if '.git' not in p.relative_to(ROOT).parts)
files = [p for p in paths if p.is_file()]
check('no_symlinks', not any(p.is_symlink() for p in paths))
secret = re.compile(r'Bearer\s+[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{15,}|github_pat_[A-Za-z0-9_]{15,}|ct-[a-f0-9]{24,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----')
for path in files:
    if path.suffix == '.pdf':
        check('PDF_signature:' + str(path.relative_to(ROOT)), path.read_bytes().startswith(b'%PDF-'))
    if path.suffix not in ['.png', '.pdf']:
        text = path.read_text()
        check('no_credentials:' + str(path.relative_to(ROOT)), secret.search(text) is None)
        # The validator's own patterns are not deployed; do not mistake them for payloads.
        if path != Path(__file__).resolve():
            check('no_machine_path:' + str(path.relative_to(ROOT)), not any(v in text for v in ['/mnt/', '/home/', 'file://']))
workflow = (ROOT / '.github/workflows/pages.yml').read_text()
check('workflow_public_artifact_allowlist', 'cp index.html styles.css app.js .nojekyll _site/' in workflow
      and 'cp -r assets data _site/' in workflow and 'path: _site' in workflow and 'path: .' not in workflow)
check('workflow_minimal_publication_permissions', all(v in workflow for v in ['contents: read', 'pages: write', 'id-token: write']))
check('workflow_no_credential_persistence', 'persist-credentials: false' in workflow)
print(json.dumps({'checked': len(checks), 'passed': sum(r['passed'] for r in checks),
                  'public_records': len(records), 'public_source_files': len(files),
                  'public_source_bytes': sum(p.stat().st_size for p in files),
                  'formal_queries_completed': 0, 'remote_publication_verified': False, 'checks': checks}, indent=2))
