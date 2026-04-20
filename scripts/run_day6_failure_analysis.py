# scripts/run_day6_failure_analysis.py
# 2026-04-20 신규: Day6 failure analysis 실행 스크립트 추가

from pathlib import Path

from eval.day6_failure_analyzer import analyze_failure
from labeling.day3_baseline_labeler import predict_target_and_subgoal
from labeling.day3_loader import load_day3_annotations, validate_day3_data


# 2026-04-20 신규: Day5 mobile scene을 기반으로 실패 유형을 분석하는 메인 함수 추가
def main() -> None:
    candidates_path = Path("data/annotations/day5_mobile_candidates.jsonl")
    ground_truth_path = Path("data/annotations/day5_mobile_ground_truth.jsonl")

    candidates, ground_truth = load_day3_annotations(candidates_path, ground_truth_path)
    validate_day3_data(candidates, ground_truth)

    gt_map = {row["scene_id"]: row for row in ground_truth}

    print("=" * 80)
    print("Day6 Failure Analysis")
    print("=" * 80)

    total_count = 0
    target_match_count = 0
    subgoal_match_count = 0
    abstain_match_count = 0

    failure_counter: dict[str, int] = {}

    for record in candidates:
        scene_id = record["scene_id"]
        gt = gt_map[scene_id]

        prediction = predict_target_and_subgoal(record)
        analysis = analyze_failure(record, prediction, gt)

        total_count += 1
        target_match_count += int(analysis["target_match"])
        subgoal_match_count += int(analysis["subgoal_match"])
        abstain_match_count += int(analysis["abstain_match"])

        for failure_type in analysis["failure_types"]:
            failure_counter[failure_type] = failure_counter.get(failure_type, 0) + 1

        print(f"[scene_id] {analysis['scene_id']}")
        print(f"instruction: {analysis['instruction']}")
        print(f"pred_target_obj_id: {analysis['pred_target_obj_id']}")
        print(f"gt_target_obj_id: {analysis['gt_target_obj_id']}")
        print(f"pred_subgoal_label: {analysis['pred_subgoal_label']}")
        print(f"gt_subgoal_label: {analysis['gt_subgoal_label']}")
        print(f"pred_abstain: {analysis['pred_abstain']}")
        print(f"gt_should_abstain: {analysis['gt_should_abstain']}")
        print(f"consistency_score: {analysis['consistency_score']}")
        print(f"target_match: {analysis['target_match']}")
        print(f"subgoal_match: {analysis['subgoal_match']}")
        print(f"abstain_match: {analysis['abstain_match']}")
        print(f"failure_types: {', '.join(analysis['failure_types'])}")
        print("-" * 80)

    print("[summary]")
    print(f"total_count: {total_count}")
    print(f"target_match_count: {target_match_count}/{total_count}")
    print(f"subgoal_match_count: {subgoal_match_count}/{total_count}")
    print(f"abstain_match_count: {abstain_match_count}/{total_count}")
    print(f"failure_counter: {failure_counter}")


if __name__ == "__main__":
    main()