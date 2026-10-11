"""Twelve typed conceptual decision cases; not new visual packs or robot data."""
import argparse
import json
from pathlib import Path
from decision_relevance_probe import infer_rules, possible_destinations, optimal_sensing, support

RULE_A = (0, 0, 1, 1)
RULE_B = (0, 1, 0, 1)
RULE_AND = (0, 0, 0, 1)
COMMON_ACTIONS = ['look_left', 'look_right', 'act_0', 'act_1', 'defer']


def make(identifier, pair, demos, current, history=None, access=None):
    history = history or {}
    access = access or {'look_left': 'A', 'look_right': 'B'}
    knowledge = tuple(current.get(cue, history.get(cue)) for cue in 'AB')
    hypotheses = infer_rules(demos)
    destinations = possible_destinations(hypotheses, knowledge)
    if len(destinations) == 1:
        actions, cost = [f'act_{destinations[0]}'], 0.0
    elif len(hypotheses) == 1:
        cost, abstract_actions = optimal_sensing(hypotheses[0], knowledge)
        actions = [action for action, cue in access.items() if f'inspect_{cue}' in abstract_actions]
    else:
        assert None not in knowledge  # ambiguity pair has a fully seen current world
        actions, cost = ['defer'], None
    return {'case_id': identifier, 'pair_id': pair,
            'input': {'demonstrations': demos, 'current_observed_values': current,
                      'legal_same_object_history': history,
                      'demonstrator_sensing_action': 'look_left',
                      'learner_observation_access': access,
                      'allowed_actions': COMMON_ACTIONS,
                      'observation_action_cost': 1,
                      'objective': 'Complete the task correctly for every state and rule compatible with legal evidence, with minimum expected observation cost. Defer only if no allowed world observation can resolve the current destination.',
                      'action_semantics': 'look reveals one declared cue; act sorts; defer declines an unidentifiable task',
                      'visibility_origin': 'manual typed contract, not visual or geometric prediction'},
            'evaluation_only': {'compatible_task_count': len(hypotheses),
                                'possible_destinations': destinations,
                                'acceptable_first_actions': actions,
                                'minimum_expected_observation_cost': cost}}


def prepare(destination):
    ambiguous = [{'A': 0, 'B': 0, 'destination': 0}, {'A': 1, 'B': 1, 'destination': 1}]
    rows = [
        make('case_00', 'task_rule', support(RULE_A), {'A': 1}),
        make('case_01', 'task_rule', support(RULE_B), {'A': 1}),
        make('case_02', 'learner_history', support(RULE_B), {'A': 1}),
        make('case_03', 'learner_history', support(RULE_B), {'A': 1}, {'B': 0}),
        make('case_04', 'observation_route', support(RULE_B), {'A': 1},
             access={'look_left': 'B', 'look_right': 'A'}),
        make('case_05', 'observation_route', support(RULE_B), {'A': 1}),
        make('case_06', 'conditional_relevance', support(RULE_AND), {'A': 1}),
        make('case_07', 'conditional_relevance', support(RULE_AND), {'A': 0}),
        make('case_08', 'task_ambiguity', ambiguous, {'A': 0, 'B': 1}),
        make('case_09', 'task_ambiguity', ambiguous, {'A': 0, 'B': 0}),
        make('case_10', 'fresh_label_binding', support(RULE_A), {'A': 1, 'B': 0}),
        make('case_11', 'fresh_label_binding', support(tuple(1-v for v in RULE_A)), {'A': 1, 'B': 0}),
    ]
    changed = {'task_rule': 'demonstrations', 'learner_history': 'legal_same_object_history',
               'observation_route': 'learner_observation_access',
               'conditional_relevance': 'current_observed_values', 'task_ambiguity': 'current_observed_values',
               'fresh_label_binding': 'demonstrations'}
    pair_checks = []
    for index in range(0, len(rows), 2):
        first, second = rows[index:index+2]
        field = changed[first['pair_id']]
        shared_first = {key: value for key, value in first['input'].items() if key != field}
        shared_second = {key: value for key, value in second['input'].items() if key != field}
        assert shared_first == shared_second
        pair_checks.append({'pair': first['pair_id'], 'only_changed_input_field': field, 'passed': True})
    result = {'schema': 'awesome-icl.typed-deepening-cases.v1', 'scope': 'typed conceptual inputs; no RGB or robot execution',
              'cases': len(rows), 'pairs': 6,
              'unique_inputs': len({json.dumps(row['input'], sort_keys=True) for row in rows}),
              'pair_checks': pair_checks,
              'demonstrator_action_is': 'a diagnostic nuisance annotation, not an observed video trace',
              'model_input_excludes': ['case_id', 'pair_id', 'evaluation_only'],
              'sampled_task_prior': 'uniform over 16 Boolean functions when only partial supports are given',
              'fresh_binding_limits': 'two inverted bindings are a paired control, not a large unseen task distribution',
              'first_model_probe_unchanged': 'existing eight visual packs, two prompts, at most 16 calls',
              'total_model_call_cap_unchanged': 120,
              'frozen_policy_model_calls': 0, 'robot_episodes': 0, 'gpu_hours': 0,
              'rows': rows}
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    return {key: value for key, value in result.items() if key != 'rows'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.output)))
