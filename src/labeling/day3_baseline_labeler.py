# src/labeling/day3_baseline_labeler.py

from __future__ import annotations

from typing import Any, Dict, List


SUBGOAL_PREPARE_PICK = "PREPARE_PICK"
SUBGOAL_REFINE_VIEW = "REFINE_VIEW"
SUBGOAL_ABSTAIN = "ABSTAIN_DECISION"

# 2026-04-12 이종헌 신규
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

# 2026-04-12 이종헌 신규
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

# 2026-04-13 이종헌 신규: Day4 reasoning 결과를 사람이 읽기 쉽게 해석하는 함수 추가
def explain_reasoning_state(prediction: Dict[str, Any]) -> Dict[str, str]:
    pred_target_obj_id = prediction["pred_target_obj_id"]
    pred_subgoal_label = prediction["pred_subgoal_label"]
    consistency_score = prediction["consistency_score"]
    abstain = prediction["abstain"]

    # 2026-04-13 신규: 사람이 읽기 쉬운 단계별 의미를 저장할 딕셔너리
    result: Dict[str, str] = {}

    # 2026-04-13 신규: target이 비어 있으면 후보를 제대로 못 고른 상태로 해석
    if not pred_target_obj_id:
        result["target_status"] = "target 없음"
    else:
        result["target_status"] = f"선택된 target: {pred_target_obj_id}"

    # 2026-04-13 신규: subgoal 라벨을 자연어 설명으로 변환
    if pred_subgoal_label == SUBGOAL_PREPARE_PICK:
        result["subgoal_meaning"] = "target이 비교적 명확하므로 다음 단계로 진행 가능"
    elif pred_subgoal_label == SUBGOAL_REFINE_VIEW:
        result["subgoal_meaning"] = "target 후보는 있지만 ambiguity가 남아서 한 번 더 확인 필요"
    elif pred_subgoal_label == SUBGOAL_ABSTAIN:
        result["subgoal_meaning"] = "현재 정보로는 판단 신뢰도가 낮아 진행 보류"
    else:
        result["subgoal_meaning"] = "알 수 없는 subgoal"

    # 2026-04-13 신규: consistency score를 구간별로 해석
    if consistency_score >= 0.80:
        result["score_meaning"] = "점수가 높아 비교적 신뢰 가능"
    elif consistency_score >= 0.60:
        result["score_meaning"] = "진행 가능하나 아주 강한 확신은 아님"
    elif consistency_score >= 0.40:
        result["score_meaning"] = "애매한 상태로 추가 확인이 필요"
    else:
        result["score_meaning"] = "신뢰도가 낮아 바로 진행하면 위험"

    # 2026-04-13 신규: abstain 최종 의미를 해석
    result["abstain_meaning"] = "보류" if abstain else "진행"

    return result