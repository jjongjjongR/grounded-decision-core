# src/schemas/output_schema.py
### 출력 형식

from dataclasses import dataclass
from typing import Literal


SubgoalLabel = Literal["PREPARE_PICK", "REFINE_VIEW", "ABSTAIN_DECISION"]


@dataclass
class OutputPrediction:
    pred_target_obj_id: str
    pred_subgoal_label: SubgoalLabel
    consistency_score: float
    abstain: bool
    reason: str