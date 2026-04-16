from pathlib import Path

from labeling.day3_loader import load_day3_annotations, validate_day3_data


def main() -> None:
    candidates_path = Path("data/annotations/day3_candidates.jsonl")
    ground_truth_path = Path("data/annotations/day3_ground_truth.jsonl")

    candidates, ground_truth = load_day3_annotations(candidates_path, ground_truth_path)
    validate_day3_data(candidates, ground_truth)

    gt_map = {row["scene_id"]: row for row in ground_truth}

    print(f"총 scene 개수: {len(candidates)}")
    print("-" * 60)

    for record in candidates:
        scene_id = record["scene_id"]
        gt = gt_map[scene_id]

        print(f"[{scene_id}]")
        print(f"instruction: {record['instruction']}")
        print(f"candidate object 수: {len(record['candidate_objects'])}")
        print(f"gt_target_obj_id: {gt['gt_target_obj_id']}")
        print(f"gt_subgoal_label: {gt['gt_subgoal_label']}")
        print(f"gt_should_abstain: {gt['gt_should_abstain']}")
        print("-" * 60)


if __name__ == "__main__":
    main()