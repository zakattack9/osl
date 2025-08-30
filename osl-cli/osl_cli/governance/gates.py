"""Governance gate checking implementation."""

from typing import Dict, Any
from datetime import datetime, timedelta

from osl_cli.state.schemas import CoachState


class GovernanceChecker:
    """Checks governance gates and enforces thresholds."""
    
    def __init__(self, coach_state: CoachState):
        """Initialize governance checker.
        
        Args:
            coach_state: Current coach state
        """
        self.coach_state = coach_state
        self.thresholds = coach_state.governance_thresholds
        self.metrics = coach_state.performance_metrics
    
    def check_calibration_gate(self) -> Dict[str, Any]:
        """Check if retrieval accuracy meets threshold.
        
        Returns:
            Gate status dictionary
        """
        threshold = self.thresholds.calibration_gate.current
        current_accuracy = self.metrics.avg_retrieval_7d
        
        passing = current_accuracy >= threshold
        
        return {
            "passing": passing,
            "status": "Passing" if passing else "Failing",
            "current_value": f"{current_accuracy:.1f}%",
            "threshold": f"{threshold}%",
            "message": (
                f"7-day average retrieval: {current_accuracy:.1f}% "
                f"(threshold: {threshold}%)"
            ),
            "action": None if passing else "Pause new content, focus on review"
        }
    
    def check_card_debt_gate(self) -> Dict[str, Any]:
        """Check if card debt is within acceptable range.
        
        Returns:
            Gate status dictionary
        """
        multiplier = self.thresholds.card_debt_multiplier.current
        throughput = self.metrics.daily_review_throughput
        cards_due = self.metrics.cards_due
        
        max_allowed = throughput * multiplier
        passing = cards_due <= max_allowed
        
        return {
            "passing": passing,
            "status": "Passing" if passing else "Failing", 
            "current_value": f"{cards_due} cards",
            "threshold": f"{max_allowed:.0f} cards",
            "message": (
                f"Cards due: {cards_due} "
                f"(max: {throughput} × {multiplier} = {max_allowed:.0f})"
            ),
            "action": None if passing else "Block new card creation"
        }
    
    def check_transfer_gate(self) -> Dict[str, Any]:
        """Check if transfer projects are up to date.
        
        Returns:
            Gate status dictionary
        """
        # Check if any books are completed without transfer project
        books_needing_transfer = []
        
        for book in self.coach_state.active_books:
            # Check if book is near completion (>80% read)
            progress = (book.current_page / book.total_pages) * 100
            
            if progress > 80:
                # Check if transfer project exists for this book
                # In full implementation, would check project directory
                last_project = self.metrics.last_transfer_project
                
                if not last_project or (datetime.now() - last_project).days > 30:
                    books_needing_transfer.append(book.title)
        
        passing = len(books_needing_transfer) == 0
        
        return {
            "passing": passing,
            "status": "Passing" if passing else "Needs Attention",
            "current_value": f"{len(books_needing_transfer)} books",
            "threshold": "0 books",
            "message": (
                "All books have transfer projects" if passing
                else f"Books needing projects: {', '.join(books_needing_transfer)}"
            ),
            "action": None if passing else "Complete transfer project before new material"
        }
    
    def check_interleaving_frequency(self) -> Dict[str, Any]:
        """Check if interleaving sessions are sufficient.
        
        Returns:
            Gate status dictionary  
        """
        min_sessions = self.thresholds.interleaving_per_week.current
        current_sessions = self.metrics.interleaving_sessions_week
        
        passing = current_sessions >= min_sessions
        
        return {
            "passing": passing,
            "status": "On Track" if passing else "Below Target",
            "current_value": f"{current_sessions} sessions",
            "threshold": f"{min_sessions} sessions",
            "message": (
                f"Interleaving sessions this week: {current_sessions} "
                f"(target: {min_sessions})"
            ),
            "action": None if passing else "Schedule interleaving session"
        }
    
    def check_all_gates(self) -> Dict[str, Dict[str, Any]]:
        """Check all governance gates.
        
        Returns:
            Dictionary of gate statuses
        """
        gates = {
            "calibration": self.check_calibration_gate(),
            "card_debt": self.check_card_debt_gate(),
            "transfer": self.check_transfer_gate(),
            "interleaving": self.check_interleaving_frequency(),
        }
        
        # Update overall governance status
        any_failing = any(not g["passing"] for g in gates.values() if g)
        
        if any_failing:
            critical_failing = (
                not gates["calibration"]["passing"] or 
                not gates["card_debt"]["passing"]
            )
            
            self.coach_state.governance_status.overall_state = (
                "BLOCKED" if critical_failing else "REMEDIATION"
            )
            self.coach_state.governance_status.remediation_active = True
            self.coach_state.governance_status.last_gate_trigger = datetime.now()
        else:
            self.coach_state.governance_status.overall_state = "NORMAL"
            self.coach_state.governance_status.remediation_active = False
        
        # Update individual gate statuses
        self.coach_state.governance_status.calibration_gate = (
            "passing" if gates["calibration"]["passing"] else "failing"
        )
        self.coach_state.governance_status.card_debt_gate = (
            "passing" if gates["card_debt"]["passing"] else "failing"
        )
        self.coach_state.governance_status.transfer_gate = (
            "passing" if gates["transfer"]["passing"] else "failing"
        )
        
        return gates