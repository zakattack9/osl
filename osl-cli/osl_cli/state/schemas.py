"""State schemas for OSL - Version 3.0."""

from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class BookState(BaseModel):
    """Active book being studied."""
    id: str
    title: str
    author: str
    start_date: datetime
    current_page: int
    total_pages: int
    sessions_completed: int = 0
    total_hours: float = 0.0
    avg_retrieval_score: float = 0.0
    last_session: Optional[datetime] = None


class GovernanceThreshold(BaseModel):
    """Configurable governance threshold with min/max bounds."""
    min: float
    current: float
    max: float
    last_adjusted: datetime


class GovernanceThresholds(BaseModel):
    """All governance thresholds with tuning ranges."""
    calibration_gate: GovernanceThreshold
    card_debt_multiplier: GovernanceThreshold
    max_new_cards: GovernanceThreshold
    interleaving_per_week: GovernanceThreshold


class GovernanceStatus(BaseModel):
    """Current governance gate status."""
    calibration_gate: Literal["passing", "failing"]
    card_debt_gate: Literal["passing", "failing"]
    transfer_gate: Literal["passing", "failing"]
    overall_state: Literal["NORMAL", "REMEDIATION", "BLOCKED"]
    last_gate_trigger: Optional[datetime] = None
    remediation_active: bool = False


class PerformanceMetrics(BaseModel):
    """Performance tracking metrics."""
    avg_retrieval_7d: float = Field(alias="7d_avg_retrieval", default=0.0)
    avg_prediction_accuracy_7d: float = Field(alias="7d_avg_prediction_accuracy", default=0.0)
    current_card_debt_ratio: float = 0.0
    daily_review_throughput: int = 60
    cards_due: int = 0
    cards_completed_today: int = 0
    last_transfer_project: Optional[datetime] = None
    interleaving_sessions_week: int = 0
    total_permanent_notes: int = 0
    total_flashcards: int = 0
    misconceptions_active: int = 0
    misconceptions_resolved: int = 0

    class Config:
        populate_by_name = True


class ReviewSchedule(BaseModel):
    """Scheduled review activities."""
    next_interleaving: Optional[datetime] = None
    next_calibration: Optional[datetime] = None
    next_synthesis: Optional[datetime] = None
    next_project_due: Optional[datetime] = None
    daily_review_time: str = "07:00"


class CoachState(BaseModel):
    """Central coach state - authoritative state management."""
    version: str = "3.0"
    last_updated: datetime = Field(default_factory=datetime.now)
    active_books: List[BookState] = []
    governance_thresholds: GovernanceThresholds
    governance_status: GovernanceStatus
    performance_metrics: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    review_schedule: ReviewSchedule = Field(default_factory=ReviewSchedule)


class CuriosityQuestion(BaseModel):
    """Learner-generated curiosity question."""
    id: int
    question: str
    created: datetime
    resolved: bool = False
    answer: Optional[str] = None
    page_found: Optional[int] = None
    resolved_at: Optional[datetime] = None


class RecallData(BaseModel):
    """Free recall attempt data."""
    duration_seconds: int
    key_points: List[str]
    confidence_score: int
    verbatim_recall: str
    recall_hash: str


class FeynmanExplanation(BaseModel):
    """Self-explanation data."""
    explanation_text: str
    explanation_hash: str
    analogies_used: List[str]
    examples_created: List[str]
    duration_seconds: int


class TutorInteraction(BaseModel):
    """AI tutor questions and responses."""
    questions_asked: List[Dict[str, Any]]
    learner_responses: List[str]
    feedback_given: List[str]
    misconceptions_identified: List[str]


class FlashcardCreated(BaseModel):
    """Learner-authored flashcard."""
    card_id: str
    front: str
    back: str
    source_page: int
    created_from_gap: str
    learner_authored: bool = True
    verbatim_hash: str
    ai_assisted_formatting: bool = False


class MicroLoop(BaseModel):
    """Single micro-loop cycle."""
    loop_id: int
    pages: str
    chunk_type: Literal["standard", "difficult", "review"]
    start_time: datetime
    end_time: Optional[datetime] = None
    recall_data: Optional[RecallData] = None
    feynman_explanation: Optional[FeynmanExplanation] = None
    tutor_interaction: Optional[TutorInteraction] = None
    flashcards_created: List[FlashcardCreated] = []
    retrieval_score: Optional[float] = None
    notes: Optional[str] = None


class SessionState(BaseModel):
    """Current active session state."""
    version: str = "3.0"
    session_id: str
    book_id: str
    book_title: str
    start_time: datetime
    last_activity: datetime
    duration_minutes: int = 0
    state: Literal["SESSION_INIT", "PREVIEW", "READING", "RECALL", "EXPLAIN", "FEEDBACK", "FLASHCARD", "SESSION_END"]
    state_history: List[Dict[str, Any]] = []
    curiosity_questions: List[CuriosityQuestion] = []
    micro_loops: List[MicroLoop] = []
    flashcards_created: int = 0
    max_flashcards: int = 8
    session_type: Literal["standard", "interleaving", "review", "calibration"]
    governance_gates_checked: bool = False
    gates_status: Dict[str, str] = {}
    ai_interactions_count: int = 0
    total_recall_time: int = 0
    total_explanation_time: int = 0
    retrieval_scores: List[float] = []