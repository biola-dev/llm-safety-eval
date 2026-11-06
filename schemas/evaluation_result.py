from typing import Literal
from pydantic import BaseModel, Field

class EvaluationResult(BaseModel):
    case_id: str
    category_id: str
    test_type: str
    target_model: str
    target_turn_prompt: str
    model_response: str
    judge_intent: Literal["malicious_adversarial", "benign_boundary", "dual_use_educational"]
    scale_a_score: int = Field(..., ge=1, le=5)
    scale_b_score: int = Field(..., ge=1, le=5)
    deterministic_violation: bool
    refusal_drift_detected: bool
    preachiness_flag: bool
    judge_rationale: str