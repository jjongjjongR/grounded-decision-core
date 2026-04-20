# src/eval/day6_failure_analyzer.py
# 2026-04-20 신규: Day6 failure analysis 유틸 함수 파일 추가

from __future__ import annotations

from typing import Any, Dict, List, Optional


# 2026-04-20 신규: candidate_objects에서 obj_id로 객체 하나를 찾는 함수 추가
def find_object_by_id(candidate_objects: List[Dict[str, Any]], obj_id: str) -> Optional[Dict[str, Any]]:
    for obj in candidate_objects:
        if obj["obj_id"] == obj_id:
            return obj
    return None


# 2026-04-20 신규: 예측 결과와 정답이 맞았는지 기본 매칭 정보를 계산하는 함수 추가
def compute_match_flags(prediction: Dict[str, Any], ground_truth: Dict[str, Any]) -> Dict[str, bool]:
    return {
        "target_match": prediction["pred_target_obj_id"] == ground_truth["gt_target_obj_id"],
        "subgoal_match": prediction["pred_subgoal_label"] == ground_truth["gt_subgoal_label"],
        "abstain_match": prediction["abstain"] == ground_truth["gt_should_abstain"],
    }


# 2026-04-20 신규: Day5 mobile-like scene에서 발생할 수 있는 실패 유형을 추론하는 함수 추가
def infer_failure_types(
    record: Dict[str, Any],
    prediction: Dict[str, Any],
    ground_truth: Dict[str, Any],
) -> List[str]:
    candidate_objects = record["candidate_objects"]

    pred_obj = find_object_by_id(candidate_objects, prediction["pred_target_obj_id"])
    gt_obj = find_object_by_id(candidate_objects, ground_truth["gt_target_obj_id"])

    failure_types: List[str] = []

    target_match = prediction["pred_target_obj_id"] == ground_truth["gt_target_obj_id"]
    subgoal_match = prediction["pred_subgoal_label"] == ground_truth["gt_subgoal_label"]
    abstain_match = prediction["abstain"] == ground_truth["gt_should_abstain"]

    # 2026-04-20 신규: target을 잘못 고른 경우 기본 실패 유형 추가
    if not target_match:
        failure_types.append("TARGET_MISMATCH")

    # 2026-04-20 신규: subgoal을 잘못 고른 경우 추가
    if not subgoal_match:
        failure_types.append("SUBGOAL_MISMATCH")

    # 2026-04-20 신규: abstain 판단이 정답과 다른 경우 추가
    if not abstain_match:
        if ground_truth["gt_should_abstain"] and not prediction["abstain"]:
            failure_types.append("MISSED_ABSTAIN")
        elif not ground_truth["gt_should_abstain"] and prediction["abstain"]:
            failure_types.append("WRONG_ABSTAIN")

    # 2026-04-20 신규: 틀렸는데도 높은 점수와 진행 판단을 낸 경우 추가
    if not target_match and prediction["consistency_score"] >= 0.8 and not prediction["abstain"]:
        failure_types.append("OVERCONFIDENT_WRONG_DECISION")

    # 2026-04-20 신규: 정답 target은 잘 안 보이는데 예측 target은 잘 보이는 경우 추가
    if pred_obj and gt_obj:
        pred_visibility = pred_obj.get("visibility", "")
        gt_visibility = gt_obj.get("visibility", "")

        if not target_match and gt_visibility in {"partial", "hard"} and pred_visibility == "clear":
            failure_types.append("VISIBILITY_BIAS")

    # 2026-04-20 신규: 기준 물체를 target으로 착각했을 가능성이 있는 경우 추가
    if pred_obj and gt_obj and not target_match:
        pred_category = pred_obj.get("category", "")
        gt_category = gt_obj.get("category", "")

        if pred_category != gt_category:
            failure_types.append("REFERENCE_OBJECT_CONFUSION")

    # 2026-04-20 신규: far/end/near 같은 위치 단서 처리 실패 가능성 추가
    if pred_obj and gt_obj and not target_match:
        pred_notes = pred_obj.get("notes", "")
        gt_notes = gt_obj.get("notes", "")

        if ("far" in gt_notes or "end" in gt_notes) and ("near" in pred_notes or "front" in pred_notes):
            failure_types.append("DISTANCE_OR_DEPTH_MISUNDERSTANDING")

    # 2026-04-20 신규: unreachable/blocking 단서가 있는데 이를 고려하지 못한 경우 추가
    scene_has_reachability_issue = any(
        "unreachable" in obj.get("notes", "") or "blocking" in obj.get("notes", "")
        for obj in candidate_objects
    )

    if scene_has_reachability_issue and not prediction["abstain"]:
        failure_types.append("REACHABILITY_BLINDNESS")

    if not failure_types:
        failure_types.append("NO_FAILURE")

    return failure_types


# 2026-04-20 신규: scene 하나에 대한 종합 분석 결과를 만드는 함수 추가
def analyze_failure(
    record: Dict[str, Any],
    prediction: Dict[str, Any],
    ground_truth: Dict[str, Any],
) -> Dict[str, Any]:
    match_flags = compute_match_flags(prediction, ground_truth)
    failure_types = infer_failure_types(record, prediction, ground_truth)

    return {
        "scene_id": record["scene_id"],
        "instruction": record["instruction"],
        "pred_target_obj_id": prediction["pred_target_obj_id"],
        "gt_target_obj_id": ground_truth["gt_target_obj_id"],
        "pred_subgoal_label": prediction["pred_subgoal_label"],
        "gt_subgoal_label": ground_truth["gt_subgoal_label"],
        "pred_abstain": prediction["abstain"],
        "gt_should_abstain": ground_truth["gt_should_abstain"],
        "consistency_score": prediction["consistency_score"],
        "target_match": match_flags["target_match"],
        "subgoal_match": match_flags["subgoal_match"],
        "abstain_match": match_flags["abstain_match"],
        "failure_types": failure_types,
    }