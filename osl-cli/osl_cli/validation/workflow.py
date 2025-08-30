"""Workflow state machine enforcement for OSL.

This module enforces the strict state transitions required by OSL's
learning methodology, ensuring no steps are skipped and prerequisites
are met before advancing.
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime


class SessionState(Enum):
    """Valid session states in the OSL workflow."""
    
    NONE = "NONE"
    SESSION_INIT = "SESSION_INIT"
    PREVIEW = "PREVIEW"
    READING = "READING"
    RECALL_PENDING = "RECALL_PENDING"
    RECALL_ACTIVE = "RECALL_ACTIVE"
    RECALL_COMPLETE = "RECALL_COMPLETE"
    FEYNMAN_PENDING = "FEYNMAN_PENDING"
    FEYNMAN_ACTIVE = "FEYNMAN_ACTIVE"
    FEYNMAN_COMPLETE = "FEYNMAN_COMPLETE"
    TUTOR_QA_PENDING = "TUTOR_QA_PENDING"
    TUTOR_QA_ACTIVE = "TUTOR_QA_ACTIVE"
    TUTOR_QA_COMPLETE = "TUTOR_QA_COMPLETE"
    CARDS_PENDING = "CARDS_PENDING"
    CARDS_ACTIVE = "CARDS_ACTIVE"
    CARDS_COMPLETE = "CARDS_COMPLETE"
    NOTES_PENDING = "NOTES_PENDING"
    NOTES_ACTIVE = "NOTES_ACTIVE"
    NOTES_COMPLETE = "NOTES_COMPLETE"
    SESSION_END = "SESSION_END"
    ARCHIVED = "ARCHIVED"


class GovernanceState(Enum):
    """Governance gate states."""
    
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"
    REMEDIATION = "REMEDIATION"
    RECOVERY = "RECOVERY"


class ValidationResult:
    """Result of a validation check."""
    
    def __init__(self, valid: bool, error: Optional[str] = None, 
                 suggestion: Optional[str] = None, allowed: Optional[List[str]] = None):
        self.valid = valid
        self.error = error
        self.suggestion = suggestion
        self.allowed = allowed or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "valid": self.valid,
            "error": self.error,
            "suggestion": self.suggestion,
            "allowed": self.allowed
        }


class OSLStateMachine:
    """Enforces valid OSL workflow transitions.
    
    This state machine ensures that the OSL learning methodology is followed
    strictly, with no skipping of steps and proper prerequisite checking.
    """
    
    # Valid state transitions
    VALID_TRANSITIONS: Dict[SessionState, List[SessionState]] = {
        SessionState.NONE: [SessionState.SESSION_INIT],
        SessionState.SESSION_INIT: [SessionState.PREVIEW, SessionState.READING],
        SessionState.PREVIEW: [SessionState.READING],
        SessionState.READING: [SessionState.RECALL_PENDING],
        SessionState.RECALL_PENDING: [SessionState.RECALL_ACTIVE],
        SessionState.RECALL_ACTIVE: [SessionState.RECALL_COMPLETE],
        SessionState.RECALL_COMPLETE: [SessionState.FEYNMAN_PENDING],
        SessionState.FEYNMAN_PENDING: [SessionState.FEYNMAN_ACTIVE],
        SessionState.FEYNMAN_ACTIVE: [SessionState.FEYNMAN_COMPLETE],
        SessionState.FEYNMAN_COMPLETE: [SessionState.TUTOR_QA_PENDING],
        SessionState.TUTOR_QA_PENDING: [SessionState.TUTOR_QA_ACTIVE],
        SessionState.TUTOR_QA_ACTIVE: [SessionState.TUTOR_QA_COMPLETE],
        SessionState.TUTOR_QA_COMPLETE: [SessionState.CARDS_PENDING],
        SessionState.CARDS_PENDING: [SessionState.CARDS_ACTIVE],
        SessionState.CARDS_ACTIVE: [SessionState.CARDS_COMPLETE],
        SessionState.CARDS_COMPLETE: [SessionState.READING, SessionState.NOTES_PENDING],
        SessionState.NOTES_PENDING: [SessionState.NOTES_ACTIVE],
        SessionState.NOTES_ACTIVE: [SessionState.NOTES_COMPLETE],
        SessionState.NOTES_COMPLETE: [SessionState.SESSION_END],
        SessionState.SESSION_END: [SessionState.ARCHIVED],
    }
    
    # Required inputs for completion states
    REQUIRED_INPUTS: Dict[SessionState, List[str]] = {
        SessionState.SESSION_INIT: ["book_id", "book_title"],
        SessionState.PREVIEW: ["curiosity_questions"],
        SessionState.READING: ["pages_read"],
        SessionState.RECALL_COMPLETE: ["recall_text", "duration_seconds", "text_hash"],
        SessionState.FEYNMAN_COMPLETE: ["explanation_text", "text_hash"],
        SessionState.TUTOR_QA_COMPLETE: ["answers", "confidence_ratings"],
        SessionState.CARDS_COMPLETE: ["cards_created", "from_misses"],
        SessionState.NOTES_COMPLETE: ["permanent_notes"],
        SessionState.SESSION_END: ["metrics_summary", "content_hashes"],
    }
    
    # Minimum requirements for states
    MINIMUM_REQUIREMENTS: Dict[str, Any] = {
        "recall_words": 50,
        "feynman_sentences": 3,
        "curiosity_questions": 3,
        "cards_from_misses_ratio": 0.6,  # 60% of cards from gaps
        "max_cards_per_session": 8,
        "min_pages_per_chunk": 3,
        "max_pages_per_chunk": 10,
    }
    
    # State timeouts in seconds
    STATE_TIMEOUTS: Dict[SessionState, int] = {
        SessionState.RECALL_ACTIVE: 300,  # 5 minutes
        SessionState.FEYNMAN_ACTIVE: 300,  # 5 minutes
        SessionState.TUTOR_QA_ACTIVE: 600,  # 10 minutes
        SessionState.CARDS_ACTIVE: 600,  # 10 minutes
    }
    
    def __init__(self):
        """Initialize the state machine."""
        self.transition_history: List[Dict[str, Any]] = []
    
    def validate_transition(
        self, 
        from_state: SessionState, 
        to_state: SessionState, 
        context: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """Validate a state transition.
        
        Args:
            from_state: Current state
            to_state: Desired next state
            context: Optional context with required inputs
            
        Returns:
            ValidationResult indicating if transition is valid
        """
        # Check if transition is allowed
        allowed_transitions = self.VALID_TRANSITIONS.get(from_state, [])
        
        if to_state not in allowed_transitions:
            return ValidationResult(
                valid=False,
                error=f"Invalid transition: {from_state.value} -> {to_state.value}",
                allowed=[s.value for s in allowed_transitions],
                suggestion=self._get_transition_suggestion(from_state, to_state)
            )
        
        # Check required inputs for the target state
        if context:
            validation = self._validate_required_inputs(to_state, context)
            if not validation.valid:
                return validation
        
        # Check minimum requirements
        if context:
            validation = self._validate_minimum_requirements(to_state, context)
            if not validation.valid:
                return validation
        
        # Record successful validation
        self.transition_history.append({
            "from": from_state.value,
            "to": to_state.value,
            "timestamp": datetime.now().isoformat(),
            "context": context
        })
        
        return ValidationResult(valid=True)
    
    def _validate_required_inputs(
        self, 
        state: SessionState, 
        context: Dict[str, Any]
    ) -> ValidationResult:
        """Validate required inputs for a state.
        
        Args:
            state: State to validate inputs for
            context: Context containing inputs
            
        Returns:
            ValidationResult
        """
        required = self.REQUIRED_INPUTS.get(state, [])
        missing = [r for r in required if not context.get(r)]
        
        if missing:
            return ValidationResult(
                valid=False,
                error=f"Missing required inputs for {state.value}: {missing}",
                suggestion=f"Provide the following before entering {state.value}: {', '.join(missing)}"
            )
        
        return ValidationResult(valid=True)
    
    def _validate_minimum_requirements(
        self, 
        state: SessionState, 
        context: Dict[str, Any]
    ) -> ValidationResult:
        """Validate minimum requirements for a state.
        
        Args:
            state: State to validate
            context: Context with values to check
            
        Returns:
            ValidationResult
        """
        # Check recall word count
        if state == SessionState.RECALL_COMPLETE:
            recall_text = context.get("recall_text", "")
            word_count = len(recall_text.split())
            min_words = self.MINIMUM_REQUIREMENTS["recall_words"]
            
            if word_count < min_words:
                return ValidationResult(
                    valid=False,
                    error=f"Recall text too short: {word_count} words (minimum: {min_words})",
                    suggestion=f"Continue recall until you have at least {min_words} words"
                )
        
        # Check Feynman explanation
        if state == SessionState.FEYNMAN_COMPLETE:
            explanation = context.get("explanation_text", "")
            sentences = [s.strip() for s in explanation.split(".") if s.strip()]
            min_sentences = self.MINIMUM_REQUIREMENTS["feynman_sentences"]
            
            if len(sentences) < min_sentences:
                return ValidationResult(
                    valid=False,
                    error=f"Explanation too brief: {len(sentences)} sentences (minimum: {min_sentences})",
                    suggestion=f"Expand your explanation to at least {min_sentences} complete sentences"
                )
        
        # Check flashcard requirements
        if state == SessionState.CARDS_COMPLETE:
            cards_created = context.get("cards_created", 0)
            from_misses = context.get("from_misses", 0)
            max_cards = self.MINIMUM_REQUIREMENTS["max_cards_per_session"]
            
            if cards_created > max_cards:
                return ValidationResult(
                    valid=False,
                    error=f"Too many cards created: {cards_created} (maximum: {max_cards})",
                    suggestion=f"Limit cards to {max_cards} per session"
                )
            
            if cards_created > 0:
                miss_ratio = from_misses / cards_created
                required_ratio = self.MINIMUM_REQUIREMENTS["cards_from_misses_ratio"]
                
                if miss_ratio < required_ratio:
                    return ValidationResult(
                        valid=False,
                        error=f"Insufficient cards from gaps: {miss_ratio:.0%} (minimum: {required_ratio:.0%})",
                        suggestion="Create more cards from identified knowledge gaps"
                    )
        
        return ValidationResult(valid=True)
    
    def _get_transition_suggestion(
        self, 
        from_state: SessionState, 
        to_state: SessionState
    ) -> str:
        """Get helpful suggestion for invalid transition.
        
        Args:
            from_state: Current state
            to_state: Attempted state
            
        Returns:
            Suggestion string
        """
        # Determine what needs to be completed
        if from_state == SessionState.READING and to_state == SessionState.CARDS_PENDING:
            return "Complete recall and Feynman explanation before creating flashcards"
        elif from_state == SessionState.SESSION_INIT and to_state == SessionState.RECALL_PENDING:
            return "Read material before attempting recall"
        elif to_state == SessionState.TUTOR_QA_PENDING and from_state.value.startswith("RECALL"):
            return "Complete both recall and Feynman explanation before AI questions"
        else:
            next_states = self.VALID_TRANSITIONS.get(from_state, [])
            if next_states:
                return f"Next valid action: {next_states[0].value.replace('_', ' ').lower()}"
            return f"Complete {from_state.value.replace('_', ' ').lower()} activities first"
    
    def get_next_actions(self, current_state: SessionState) -> List[str]:
        """Get list of valid next actions from current state.
        
        Args:
            current_state: Current state
            
        Returns:
            List of valid next action descriptions
        """
        next_states = self.VALID_TRANSITIONS.get(current_state, [])
        
        actions = []
        for state in next_states:
            if state == SessionState.RECALL_ACTIVE:
                actions.append("Start free recall (osl recall start)")
            elif state == SessionState.FEYNMAN_ACTIVE:
                actions.append("Begin Feynman explanation (osl feynman start)")
            elif state == SessionState.TUTOR_QA_ACTIVE:
                actions.append("Get AI questions (osl tutor questions)")
            elif state == SessionState.CARDS_ACTIVE:
                actions.append("Create flashcards (osl flashcard create)")
            elif state == SessionState.NOTES_ACTIVE:
                actions.append("Create permanent notes (osl notes create)")
            elif state == SessionState.SESSION_END:
                actions.append("End session (osl session end)")
            elif state == SessionState.READING:
                actions.append("Continue reading (osl reading continue)")
            else:
                actions.append(f"Proceed to {state.value.replace('_', ' ').lower()}")
        
        return actions
    
    def validate_timeout(
        self, 
        state: SessionState, 
        start_time: datetime
    ) -> ValidationResult:
        """Check if a state has exceeded its timeout.
        
        Args:
            state: Current state
            start_time: When the state was entered
            
        Returns:
            ValidationResult
        """
        if state not in self.STATE_TIMEOUTS:
            return ValidationResult(valid=True)
        
        timeout_seconds = self.STATE_TIMEOUTS[state]
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if elapsed > timeout_seconds:
            return ValidationResult(
                valid=False,
                error=f"State {state.value} timeout exceeded: {elapsed:.0f}s > {timeout_seconds}s",
                suggestion="Complete the current activity or save progress"
            )
        
        return ValidationResult(valid=True)


class GovernanceStateMachine:
    """Manages governance state transitions."""
    
    VALID_TRANSITIONS: Dict[GovernanceState, List[GovernanceState]] = {
        GovernanceState.NORMAL: [GovernanceState.WARNING, GovernanceState.BLOCKED],
        GovernanceState.WARNING: [GovernanceState.NORMAL, GovernanceState.BLOCKED],
        GovernanceState.BLOCKED: [GovernanceState.REMEDIATION],
        GovernanceState.REMEDIATION: [GovernanceState.RECOVERY],
        GovernanceState.RECOVERY: [GovernanceState.NORMAL, GovernanceState.WARNING],
    }
    
    def validate_transition(
        self, 
        from_state: GovernanceState, 
        to_state: GovernanceState,
        context: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """Validate governance state transition.
        
        Args:
            from_state: Current governance state
            to_state: Desired governance state
            context: Optional context with gate statuses
            
        Returns:
            ValidationResult
        """
        allowed = self.VALID_TRANSITIONS.get(from_state, [])
        
        if to_state not in allowed:
            return ValidationResult(
                valid=False,
                error=f"Invalid governance transition: {from_state.value} -> {to_state.value}",
                allowed=[s.value for s in allowed],
                suggestion=self._get_governance_suggestion(from_state, to_state)
            )
        
        return ValidationResult(valid=True)
    
    def _get_governance_suggestion(
        self, 
        from_state: GovernanceState, 
        to_state: GovernanceState
    ) -> str:
        """Get suggestion for governance transition.
        
        Args:
            from_state: Current state
            to_state: Attempted state
            
        Returns:
            Suggestion string
        """
        if from_state == GovernanceState.BLOCKED and to_state == GovernanceState.NORMAL:
            return "Must enter REMEDIATION first to address gate failures"
        elif from_state == GovernanceState.REMEDIATION and to_state == GovernanceState.NORMAL:
            return "Complete remediation activities and enter RECOVERY first"
        else:
            return "Follow the governance recovery process"