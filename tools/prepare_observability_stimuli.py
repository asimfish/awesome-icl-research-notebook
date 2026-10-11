"""Create eight discrete visual query packs, not simulated or real robot footage.

Standard-library, CPU-only. Future costs and visibility are declared, not inferred
from SVG geometry. Raw prompts contain no answer cue/rule IDs. Shared-evidence
prompts are a disclosed oracle-parsing control, not an implemented visual parser.
"""
from pathlib import Path
import argparse
import json

COLORS = {0: '#4b74c7', 1: '#c85148'}


def image(color, symbol, visible, bin_label=None):
    mark = ('<circle cx="326" cy="186" r="19" fill="none" stroke="#203e33" stroke-width="5"/>'
            if symbol == 0 else '<path d="M326 164 L346 205 L306 205 Z" fill="none" stroke="#203e33" stroke-width="5"/>')
    caption = 'PROGRAM-DRAWN STIMULUS / NOT ROBOT FOOTAGE'
    label = f'Demonstrated destination: {bin_label}' if bin_label else 'Query object'
    side = mark if visible else '<path d="M291 160 L363 140 L363 219 L291 239 Z" fill="#737970"/><text x="315" y="198" font-size="24" fill="white">?</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="320" viewBox="0 0 640 320">
<rect width="640" height="320" fill="#fcfaf4"/><text x="25" y="32" font-family="sans-serif" font-size="13" fill="#596451">{caption}</text>
<text x="25" y="62" font-family="sans-serif" font-size="20" fill="#203e33">{label}</text>
<path d="M220 119 L292 100 L363 140 L291 160 Z" fill="#e9d9c4" stroke="#8c846d"/>
<path d="M220 119 L291 160 L291 239 L220 199 Z" fill="{COLORS[color]}" stroke="#8c846d"/>
<path d="M291 160 L363 140 L363 219 L291 239 Z" fill="#efe3cf" stroke="#8c846d"/>{side}
<text x="25" y="280" font-family="sans-serif" font-size="17" fill="#203e33">Front visible; side {'visible' if visible else 'occluded / not read'}.</text></svg>'''


def prepare(destination):
    destination.mkdir(parents=True, exist_ok=True)
    assets = destination / 'images'
    assets.mkdir(exist_ok=True)
    files = {'support_00.svg': image(0, 0, True, 'LEFT'),
             'support_01.svg': image(1, 0, True, 'RIGHT'),
             'support_02.svg': image(0, 1, True, 'RIGHT'),
             'query_hidden.svg': image(1, 0, False),
             'query_visible.svg': image(1, 0, True),
             'history_visible.svg': image(1, 0, True),
             'inspection_result.svg': image(1, 0, True)}
    for name, content in files.items():
        (assets / name).write_text(content + '\n')
    contexts = [
        ('unknown_costly', False, False, 3),
        ('unknown_equal_cost', False, False, 1),
        ('history_known', False, True, 3),
        ('currently_visible', True, False, 3),
    ]
    rows = []
    for context, visible, history, after_cost in contexts:
        for rule in ['front', 'side']:
            cue_known = rule == 'front' or visible or history
            correct = 'RIGHT' if rule == 'front' else 'LEFT'
            optimum = (['grasp'] if cue_known else ['inspect_side', 'grasp']
                       if after_cost == 1 else ['inspect_side'])
            raw = ("Infer which object feature determines LEFT versus RIGHT from the two demonstrations. "
                   "Return JSON with inferred_feature (front appearance or side mark), next_action "
                   "(grasp or inspect_side), and destination (LEFT, RIGHT or unknown). "
                   "If the required mark has not been observed, destination may be unknown before inspection. "
                   "This is a discrete visual decision, not robot execution. Current front is visible. "
                   f"After grasp, acquiring the side cue costs {after_cost} extra units; "
                   "before grasp it costs one. Costs are explicitly supplied, not predicted from images. "
                   "Place-back, inspection and regrasp are allowed; all mandatory transport costs are shared. "
                   "Prior images, if provided, show the same query object. Accept every equally optimal action.")
            evidence = (f"Shared parser/evidence control: the relevant feature is {rule}; "
                        f"the relevant cue is {'known' if cue_known else 'unseen'}. "
                        + (f"Its observed value implies {correct}." if cue_known else
                           "Its value and destination remain unknown; inspect to obtain it."))
            packet = {'support_images': ['images/support_00.svg', 'images/support_01.svg'
                       if rule == 'front' else 'images/support_02.svg'],
                      'current_image': 'images/query_visible.svg' if visible else 'images/query_hidden.svg',
                      'history_images': ['images/history_visible.svg'] if history else [],
                      'declared_post_grasp_side_cost': after_cost,
                      'raw_prompt': raw,
                      'same_evidence_prompt': raw + '\n' + evidence,
                      'same_evidence_origin': 'oracle symbolic parsing / disclosed upper-bound control'}
            rows.append({'pack_id': f'pack_{len(rows):02}', 'context': context,
                         'model_input': packet,
                         'evaluation_only': {'rule': rule, 'cue_known': cue_known,
                                             'latent_destination': correct,
                                             'preinspection_acceptable_destination': [correct] if cue_known else ['unknown'],
                                             'acceptable_cost_optimal_first_actions': optimum,
                                             'minimum_extra_cost': 0 if cue_known else 1}})
    shared = ['current_image', 'history_images', 'declared_post_grasp_side_cost', 'raw_prompt']
    paired = all(all(rows[i]['model_input'][key] == rows[i+1]['model_input'][key]
                    for key in shared) for i in range(0, len(rows), 2))
    result = {'schema': 'awesome-icl.discrete-visual-packs.v1', 'scope': 'program-drawn offline stimuli only',
              'visual_packs': 8, 'paired_contexts': 4, 'shared_asset_files': len(files),
              'raw_pairs_only_support_images_change': paired,
              'unknown_destination_is_not_exposed_to_policy': True,
              'future_costs': 'hand-authored and explicitly supplied',
              'shared_evidence_control': 'oracle parsing; not an implemented perception model',
              'evaluation_fields_must_not_be_serialized_to_policy': True,
              'robot_episodes': 0, 'model_calls': 0, 'gpu_hours': 0,
              'unverified': ['cue extraction by a frozen model', 'physical occlusion',
                             'reachable camera poses', 'measured recovery time'],
              'first_model_probe_max_calls': 16, 'all_model_probes_total_max_calls': 120,
              'rows': rows}
    assert paired
    (destination / 'packs.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    (destination / 'README.md').write_text('''# Eight discrete visual input packs

These SVGs are program-drawn information-structure stimuli, not robot images.
Four contexts are paired under two crossed demonstrations. Model input consists
only of images and the selected prompt; pack IDs, context IDs and evaluation fields
must not be included. Convert SVG to pixels with an existing browser before using
an image-only model; do not assume an API accepts SVG. Conversion does not make
these physical observations.

`same_evidence_prompt` uses oracle symbolic parsing to locate the bottleneck. It
is not an implemented deployable visual parser. Both raw and structured settings
receive the same declared future-cost contract. Unknown side marks and the latent
destination are withheld until inspection. Inspecting reveals the shared
`inspection_result.svg`; fixed images do not validate a feasible robot action.

First compare the raw and same-evidence conditions on all eight packs: at most
16 requests, included in the total 120-call cap. Each request returns rule and
next action together. Costs tied at one permit either inspect or grasp. Known
history and current-visible controls should need no extra view. No model has run.
''')
    return {key: value for key, value in result.items() if key != 'rows'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.output)))
