# src/schemas/input_schema.py
### 입력 형식

from dataclasses import dataclass
from typing import List, Literal, Optional


VisibilityType = Literal["clear", "partial", "hard"]


@dataclass
class CandidateObject:
    obj_id: str
    category: str
    color: str
    bbox: List[int]   # [x_min, y_min, x_max, y_max]
    visibility: VisibilityType
    notes: Optional[str] = None


@dataclass
class InputSample:
    scene_id: str
    instruction: str
    candidate_objects: List[CandidateObject]