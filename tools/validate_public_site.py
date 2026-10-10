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

# Git metadata belongs to the checkout, not the public publishing surface.
paths = sorted(p for p in ROOT.rglob('*') if '.git' not in p.relative_to(ROOT).parts)
files = [p for p in paths if p.is_file()]
check('no_symlinks', not any(p.is_symlink() for p in paths))
secret = re.compile(r'Bearer\s+[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{15,}|github_pat_[A-Za-z0-9_]{15,}|ct-[a-f0-9]{24,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----')
for path in files:
    if path.suffix not in ['.png']:
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
