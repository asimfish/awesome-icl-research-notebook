"""Exhaustive finite thought-experiment controls; no image/model/robot inference.

All 16 Boolean routing tables are identified by four crossed demonstrations.
Compare a global-feature coverage extension with decision-relevant sensing.
The latter is an exact deterministic observation-tree cost calculation for this
finite grammar, not a new algorithm or a robotics result. Unknown cue values
are uniform; costs are declared. Task-hypothesis ambiguity is tested separately.
"""
import argparse
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

WORLDS = tuple(product((0, 1), repeat=2))
RULES = tuple(tuple((code >> index) & 1 for index in range(4)) for code in range(16))
KNOWLEDGE = ((None, None), (0, None), (1, None), (None, 0), (None, 1),
             (0, 0), (0, 1), (1, 0), (1, 1))


def compatible_worlds(knowledge):
    return [world for world in WORLDS if all(k is None or k == w for k, w in zip(knowledge, world))]


def output(rule, world):
    return rule[WORLDS.index(world)]


def support(rule):
    return [{'A': world[0], 'B': world[1], 'destination': output(rule, world)} for world in WORLDS]


def infer_rules(demos):
    return tuple(rule for rule in RULES if all(output(rule, (row['A'], row['B'])) == row['destination'] for row in demos))


def possible_destinations(hypotheses, knowledge):
    return sorted({output(rule, world) for rule in hypotheses for world in compatible_worlds(knowledge)})


def global_dependencies(rule):
    return [axis for axis in (0, 1) if any(output(rule, world) != output(rule, tuple(1-value if index == axis else value
                                for index, value in enumerate(world))) for world in WORLDS)]


@lru_cache(None)
def optimal_sensing(rule, knowledge):
    destinations = possible_destinations((rule,), knowledge)
    if len(destinations) == 1:
        return 0.0, (f'act_{destinations[0]}',)
    values = {}
    for axis in (0, 1):
        if knowledge[axis] is not None:
            continue
        expected = 0.0
        for value in (0, 1):
            updated = tuple(value if i == axis else k for i, k in enumerate(knowledge))
            expected += 0.5 * optimal_sensing(rule, updated)[0]
        values[f'inspect_{"AB"[axis]}'] = 1.0 + expected
    best = min(values.values())
    return best, tuple(action for action, cost in values.items() if cost == best)


def run():
    rows = []
    for index, rule in enumerate(RULES):
        demos = support(rule)
        assert infer_rules(demos) == (rule,)
        for knowledge in KNOWLEDGE:
            best, actions = optimal_sensing(rule, knowledge)
            missing = [axis for axis in global_dependencies(rule) if knowledge[axis] is None]
            coverage_cost = float(len(missing))
            rows.append({'case_id': f'case_{len(rows):03}',
                         'policy_input': {'demonstrations': demos,
                                          'current_knowledge': dict(zip('AB', knowledge)),
                                          'allowed_actions': ['inspect_A', 'inspect_B', 'act_0', 'act_1'],
                                          'observation_costs': {'inspect_A': 1, 'inspect_B': 1},
                                          'unknown_cues': 'uniform binary; inspection reveals exactly one cue'},
                         'evaluation_only': {'truth_table_id': index,
                                              'global_dependencies': ['AB'[axis] for axis in global_dependencies(rule)],
                                              'possible_destinations': possible_destinations((rule,), knowledge),
                                              'optimal_first_actions': list(actions),
                                              'optimal_expected_observation_cost': best,
                                              'global_feature_coverage_cost': coverage_cost,
                                              'coverage_excess': coverage_cost - best}})
    ambiguous_demos = [{'A': 0, 'B': 0, 'destination': 0}, {'A': 1, 'B': 1, 'destination': 1}]
    compatible = infer_rules(ambiguous_demos)
    assert len(compatible) == 4
    ambiguity = []
    for world in WORLDS:
        destinations = possible_destinations(compatible, world)
        ambiguity.append({'world_fully_known': dict(zip('AB', world)),
                          'compatible_task_hypotheses': len(compatible),
                          'possible_destinations': destinations,
                          'world_inspection_can_resolve_task': False,
                          'correct_behavior': f'act_{destinations[0]}' if len(destinations) == 1 else 'defer_task_ambiguous'})
    # Same cue can be acquired through a different physical-action alias.
    # This is declared remapping, not validated camera motion or robot geometry.
    relocated = [{'teacher_action': 'look_left', 'teacher_reveals': 'B',
                  'learner_access': {'look_left': 'A', 'look_right': 'B'},
                  'learner_A_known': 1, 'learner_B_known': None,
                  'task': support((0, 1, 0, 1)),
                  'teacher_action_replay': 'look_left',
                  'correct_learner_action': 'look_right'}]
    return {'scope': 'finite symbolic counterexamples to task-design assumptions only',
            'task_rules': len(RULES), 'knowledge_patterns': len(KNOWLEDGE), 'cases': len(rows),
            'full_crossed_support_identifies_each_rule': True,
            'global_coverage_suboptimal_cases': sum(row['evaluation_only']['coverage_excess'] > 0 for row in rows),
            'action_already_determined_but_global_cue_unknown_cases': sum(
                row['evaluation_only']['optimal_expected_observation_cost'] == 0 and
                row['evaluation_only']['global_feature_coverage_cost'] > 0 for row in rows),
            'max_global_coverage_excess': max(row['evaluation_only']['coverage_excess'] for row in rows),
            'ambiguity_support': ambiguous_demos,
            'fully_known_worlds_with_unresolved_task': sum(len(row['possible_destinations']) > 1 for row in ambiguity),
            'task_ambiguous_but_action_determined_worlds': sum(len(row['possible_destinations']) == 1 for row in ambiguity),
            'ambiguity_cases': ambiguity, 'access_remapping_case': relocated,
            'frozen_policy_model_calls': 0, 'robot_episodes': 0, 'gpu_hours': 0,
            'not_evidence_for': ['new algorithm', 'frozen-model deficit', 'visual understanding', 'physical camera access'],
            'rows': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key not in ['rows', 'ambiguity_cases', 'access_remapping_case']}))
