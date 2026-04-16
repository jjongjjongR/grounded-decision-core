# scripts/run_day4_reasoning_check.py
## 예측을 reasoning 해석까지 붙여서 출력하는 스크립트

from pathlib import Path
from labeling.day3_loader import load_day3_annotations, validate_day3_data
from labeling.day3_baseline_labeler import predict_target_and_subgoal, explain_reasoning_state

def main() -> None:
    candidates_path = Path("data/annotations/day3_candidates.jsonl")
    ground_truth_path = Path("data/annotations/day3_ground_truth.jsonl")

    candidates, ground_truth = load_day3_annotations(candidates_path, ground_truth_path)
    validate_day3_data(candidates, ground_truth)

    gt_map = {row["scene_id"]: row for row in ground_truth}

    print("=" * 70)
    print("Day4 Reasoning Check")
    print("=" * 70)

    for record in candidates:
        scene_id = record["scene_id"]
        gt = gt_map[scene_id]

        prediction = predict_target_and_subgoal(record)
        reasoning = explain_reasoning_state(prediction)

        print(f"[scene_id] {scene_id}")
        print(f"instruction: {record['instruction']}")
        print(f"pred_target_obj_id: {prediction['pred_target_obj_id']}")
        print(f"pred_subgoal_label: {prediction['pred_subgoal_label']}")
        print(f"consistency_score: {prediction['consistency_score']}")
        print(f"abstain: {prediction['abstain']}")
        print(f"reason: {prediction['reason']}")
        print(f"target_status: {reasoning['target_status']}")
        print(f"subgoal_meaning: {reasoning['subgoal_meaning']}")
        print(f"score_meaning: {reasoning['score_meaning']}")
        print(f"abstain_meaning: {reasoning['abstain_meaning']}")
        print(f"gt_target_obj_id: {gt['gt_target_obj_id']}")
        print(f"gt_subgoal_label: {gt['gt_subgoal_label']}")
        print(f"gt_should_abstain: {gt['gt_should_abstain']}")
        print("-" * 70)

if __name__ == "__main__":
    main()