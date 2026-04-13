from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def load_jsonl(path: str | Path) -> List[Dict[str, Any]]:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"파일이 없습니다: {file_path}")

    rows: List[Dict[str, Any]] = []
    with file_path.open("r", encoding="utf-8") as f:
        for line_idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"{file_path}의 {line_idx}번째 줄 JSON 형식 오류: {e}") from e

    return rows


def load_day3_annotations(
    candidates_path: str | Path,
    ground_truth_path: str | Path,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    candidates = load_jsonl(candidates_path)
    ground_truth = load_jsonl(ground_truth_path)
    return candidates, ground_truth


def validate_candidate_record(record: Dict[str, Any]) -> None:
    required_top_keys = {"scene_id", "instruction", "candidate_objects"}
    missing_top_keys = required_top_keys - set(record.keys())
    if missing_top_keys:
        raise ValueError(f"candidate record 상위 키 누락: {missing_top_keys}")

    if not isinstance(record["candidate_objects"], list):
        raise ValueError("candidate_objects는 리스트여야 합니다.")

    for obj in record["candidate_objects"]:
        required_obj_keys = {"obj_id", "category", "color", "bbox", "visibility"}
        missing_obj_keys = required_obj_keys - set(obj.keys())
        if missing_obj_keys:
            raise ValueError(f"candidate object 키 누락: {missing_obj_keys}")

        if not isinstance(obj["bbox"], list) or len(obj["bbox"]) != 4:
            raise ValueError(f"bbox 형식 오류: {obj['bbox']}")


def validate_ground_truth_record(record: Dict[str, Any]) -> None:
    required_keys = {
        "scene_id",
        "gt_target_obj_id",
        "gt_target_bbox",
        "gt_subgoal_label",
        "gt_should_abstain",
    }
    missing_keys = required_keys - set(record.keys())
    if missing_keys:
        raise ValueError(f"ground truth 키 누락: {missing_keys}")


def validate_day3_data(
    candidate_rows: List[Dict[str, Any]],
    ground_truth_rows: List[Dict[str, Any]],
) -> None:
    for row in candidate_rows:
        validate_candidate_record(row)

    for row in ground_truth_rows:
        validate_ground_truth_record(row)

    candidate_scene_ids = {row["scene_id"] for row in candidate_rows}
    ground_truth_scene_ids = {row["scene_id"] for row in ground_truth_rows}

    if candidate_scene_ids != ground_truth_scene_ids:
        raise ValueError(
            "candidate와 ground truth의 scene_id 집합이 다릅니다. "
            f"candidate={candidate_scene_ids}, gt={ground_truth_scene_ids}"
        )