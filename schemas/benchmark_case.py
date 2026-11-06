from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class TurnMessage(BaseModel):
    turn_index: int = Field(..., ge=1, le=8, description="1-indexed conversational turn")
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1)

class EvaluationCriteria(BaseModel):
    target_turn: int = Field(..., description="The conversational turn evaluated for safety or over-refusal")
    expected_action: Literal["REFUSE", "FULFILL", "CONDITIONAL_SAFE_FULFILL"]
    forbidden_substrings: List[str] = Field(default_factory=list)
    required_mitigations: List[str] = Field(default_factory=list)
    target_scale_a_threshold: Optional[int] = Field(None, ge=1, le=5)
    target_scale_b_threshold: Optional[int] = Field(None, ge=1, le=5)

class BenchmarkCase(BaseModel):
    case_id: str = Field(..., pattern=r"^TC-[A-Z0-9]+-\d{3}$")
    category_id: Literal[
        "CAT-01", "CAT-02", "CAT-03", "CAT-04", "CAT-05",
        "CAT-06", "CAT-07", "CAT-08", "CAT-09", "CAT-10"
    ]
    test_type: Literal[
        "multi_turn_drift",
        "over_refusal_boundary",
        "adversarial_framing"
    ]
    intent_classification: Literal["malicious_adversarial", "benign_boundary", "dual_use_educational"]
    threat_description: str = Field(..., max_length=500)
    conversation: List[TurnMessage]
    evaluation_criteria: EvaluationCriteria