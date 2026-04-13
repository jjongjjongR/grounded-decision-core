from __future__ import annotations

from typing import Any, Dict, List


SUBGOAL_PREPARE_PICK = "PREPARE_PICK"
SUBGOAL_REFINE_VIEW = "REFINE_VIEW"
SUBGOAL_ABSTAIN = "ABSTAIN_DECISION"


def simple_keyword_match_score(instruction: str, candidate: Dict[str, Any]) -> int:
    instruction = instruction.lower()
    score = 0

    if candidate["category"].lower() in instruction:
        score += 2

    if candidate["color"].lower() in instruction:
        score += 2

    notes = candidate.get("notes", "").lower()
    if notes and any(token in instruction for token in notes.split("_")):
        score += 1

    if candidate["visibility"] == "clear":
        score += 1
    elif candidate["visibility"] == "partial":
        score -= 1
    elif candidate["visibility"] == "hard":
        score -= 2

    return score


def predict_target_and_subgoal(record: Dict[str, Any]) -> Dict[str, Any]:
    instruction = record["instruction"]
    candidates: List[Dict[str, Any]] = record["candidate_objects"]

    if not candidates:
        return {
            "pred_target_obj_id": "",
            "pred_subgoal_label": SUBGOAL_ABSTAIN,
            "consistency_score": 0.0,
            "abstain": True,
            "reason": "No candidate objects were provided."
        }

    scored = []
    for candidate in candidates:
        score = simple_keyword_match_score(instruction, candidate)
        scored.append((score, candidate))

    scored.sort(key=lambda x: x[0], reverse=True)

    best_score, best_candidate = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else -999

    if best_score <= 0:
        return {
            "pred_target_obj_id": "",
            "pred_subgoal_label": SUBGOAL_ABSTAIN,
            "consistency_score": 0.1,
            "abstain": True,
            "reason": "No candidate matched the instruction well enough."
        }

    margin = best_score - second_score

    if best_candidate["visibility"] == "hard":
        subgoal = SUBGOAL_ABSTAIN
        abstain = True
        consistency_score = 0.25
        reason = "Best candidate exists, but visibility is too poor."
    elif margin <= 1:
        subgoal = SUBGOAL_REFINE_VIEW
        abstain = False
        consistency_score = 0.55
        reason = "A candidate exists, but ambiguity remains among similar objects."
    else:
        subgoal = SUBGOAL_PREPARE_PICK
        abstain = False
        consistency_score = 0.85
        reason = "A clear candidate matches the instruction."

    return {
        "pred_target_obj_id": best_candidate["obj_id"],
        "pred_subgoal_label": subgoal,
        "consistency_score": consistency_score,
        "abstain": abstain,
        "reason": reason,
    }