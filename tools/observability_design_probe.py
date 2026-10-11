"""Disclosed symbolic task-design probe; no images, model or robot execution.

Two demonstrations specify which of two independent cues determines a bin.
Thirty cases cross five hand-authored post-grasp visibility conditions, three
knowledge states, and two demonstration rules. Classical controls deliberately
receive the same task inference and visibility table as the candidate scheduler.
"""
import json
import argparse
from pathlib import Path

DEMONSTRATIONS = {
    "A": [{"A": 0, "B": 0, "bin": 0}, {"A": 1, "B": 0, "bin": 1}],
    "B": [{"A": 0, "B": 0, "bin": 0}, {"A": 0, "B": 1, "bin": 1}],
}
# Cost is a supplied symbolic forecast, not measured robot time or geometry.
WORLDS = [
    {"A": 3, "B": 1}, {"A": 1, "B": 3}, {"A": 3, "B": 3},
    {"A": 1, "B": 1}, {"A": 2, "B": 1},
]


def infer_cue(demos):
    hypotheses = [(cue, invert) for cue in ["A", "B"] for invert in [0, 1]
                  if all((row[cue] ^ invert) == row["bin"] for row in demos)]
    assert len(hypotheses) == 1
    return hypotheses[0][0]


def run():
    rows = []
    for world_id, forecast in enumerate(WORLDS):
        for knowledge in ["unseen", "seen_in_history", "visible_now"]:
            for rule in ["A", "B"]:
                cue = infer_cue(DEMONSTRATIONS[rule])
                known = knowledge != "unseen"
                # The strict candidate only inspects early at a supplied deadline.
                candidate = "grasp" if known or forecast[cue] <= 1 else f"inspect_{cue}"
                # Classical task-conditioned uncertainty always resolves unknowns.
                active_perception = "grasp" if known else f"inspect_{cue}"
                alternatives = [("grasp", 0)] if known else [
                    (f"inspect_{cue}", 1), ("grasp", forecast[cue])]
                # This is a restricted two-schedule cost control, not a belief planner.
                optimal_cost = min(cost for _, cost in alternatives)
                optimal_actions = [action for action, cost in alternatives
                                   if cost == optimal_cost]
                candidate_cost = (0 if known else
                                  1 if candidate.startswith("inspect_") else forecast[cue])
                rows.append({
                    "case_id": f"case_{len(rows):02}", "world_id": world_id,
                    "knowledge_condition": knowledge,
                    "policy_packet": {
                        "demonstrations": DEMONSTRATIONS[rule],
                        "past_observed_cues": {"A": 1, "B": 0}
                        if knowledge == "seen_in_history" else {},
                        "currently_observed_cues": {"A": 1, "B": 0}
                        if knowledge == "visible_now" else {},
                        "predicted_post_grasp_inspection_cost": forecast,
                        "allowed_actions": ["inspect_A", "inspect_B", "grasp",
                                            "place_back", "regrasp"],
                        "recovery_allowed": True,
                        "budget_units": "extra observation/recovery cost; common grasp and transport excluded",
                    },
                    "evaluation_only": {"task_rule": rule, "A": 1, "B": 0,
                                         "correct_bin": 1 if cue == "A" else 0},
                    "candidate_first_action": candidate,
                    "classical_active_perception_first_action": active_perception,
                    "restricted_optimal_first_actions": optimal_actions,
                    "candidate_is_restricted_cost_optimal": candidate in optimal_actions,
                    "candidate_total_inspection_cost": candidate_cost,
                    "classical_total_inspection_cost": 0 if known else 1,
                    "restricted_two_schedule_optimal_cost": optimal_cost,
                    "grasp_first_cost_feasible_at_budgets": {
                        str(budget): (0 if known else forecast[cue]) <= budget
                        for budget in [1, 2, 3]},
                    "always_inspect_both_cost": 2,
                })
    paired_changes = sum(rows[i]["candidate_first_action"] != rows[i+1]["candidate_first_action"]
                         for i in range(0, len(rows), 2))
    return {"scope": "symbolic design/identifiability control only",
            "cases": len(rows), "paired_physical_contexts": len(rows)//2,
            "hand_authored_visibility_worlds": len(WORLDS),
            "knowledge_conditions": 3,
            "optimality_scope": "two declared schedules only; equally cheap first actions all accepted",
            "cost_semantics": {
                "pre_grasp_inspection": "one symbolic extra view action",
                "post_grasp_cost_1": "a still-available view after grasp",
                "post_grasp_cost_2": "reposition plus view",
                "post_grasp_cost_3": "place back, view, regrasp",
                "costs_are_not": "measured time, verified geometry or robot execution"},
            "rows_with_multiple_optimal_first_actions": sum(
                len(row["restricted_optimal_first_actions"]) > 1 for row in rows),
            "candidate_restricted_cost_optimal_cases": sum(
                row["candidate_is_restricted_cost_optimal"] for row in rows),
            "input_modality": "oracle symbolic cues, not RGB",
            "future_visibility": "supplied hand-authored forecast; not learned or geometrically verified",
            "robot_episodes": 0, "model_calls": 0, "gpu_hours": 0,
            "cue_rule_identified_in_declared_grammar": True,
            "candidate_and_classical_total_cost_equal_cases": sum(
                row["candidate_total_inspection_cost"] == row["classical_total_inspection_cost"] for row in rows),
            "only_demonstrations_change_within_pairs": all(
                {key: value for key, value in rows[i]["policy_packet"].items() if key != "demonstrations"} ==
                {key: value for key, value in rows[i+1]["policy_packet"].items() if key != "demonstrations"}
                for i in range(0, len(rows), 2)),
            "candidate_first_action_changes_with_demonstration_pairs": paired_changes,
            "interpretation": "The task has controllable demo-conditioned observation choices, but classical task-conditioned perception already matches the candidate cost in all constructed cases. No scheduler novelty, visual grounding, geometric visibility or robot gain is established.",
            "rows": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('observability-design-probe.json'))
    args = parser.parse_args()
    result = run()
    destination = args.output
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "rows"}))
