"""Tests for OSL state management."""

import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime

from osl_cli.state.schemas import (
    CoachState,
    SessionState,
    GovernanceThresholds,
    GovernanceThreshold,
    GovernanceStatus,
)
from osl_cli.state.manager import StateManager


class TestStateManager(unittest.TestCase):
    """Test state management functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.osl_path = self.temp_path / "osl"
        self.osl_path.mkdir()
        (self.osl_path / "ai_state").mkdir()
        
        self.state_manager = StateManager(self.osl_path)
    
    def test_coach_state_save_load(self):
        """Test saving and loading coach state."""
        # Create coach state
        now = datetime.now()
        thresholds = GovernanceThresholds(
            calibration_gate=GovernanceThreshold(min=75, current=80, max=85, last_adjusted=now),
            card_debt_multiplier=GovernanceThreshold(min=1.5, current=2.0, max=2.5, last_adjusted=now),
            max_new_cards=GovernanceThreshold(min=4, current=8, max=10, last_adjusted=now),
            interleaving_per_week=GovernanceThreshold(min=1, current=2, max=3, last_adjusted=now),
        )
        
        status = GovernanceStatus(
            calibration_gate="passing",
            card_debt_gate="passing",
            transfer_gate="passing",
            overall_state="NORMAL",
            remediation_active=False,
        )
        
        coach_state = CoachState(
            version="3.0",
            governance_thresholds=thresholds,
            governance_status=status,
        )
        
        # Save state
        self.state_manager.save_coach_state(coach_state)
        
        # Load state
        loaded_state = self.state_manager.load_coach_state()
        
        # Verify
        self.assertEqual(loaded_state.version, "3.0")
        self.assertEqual(loaded_state.governance_status.overall_state, "NORMAL")
        self.assertEqual(loaded_state.governance_thresholds.calibration_gate.current, 80)
    
    def test_session_state_lifecycle(self):
        """Test session state creation, update, and archival."""
        # Create session
        session = SessionState(
            session_id="test_session_001",
            book_id="test_book",
            book_title="Test Book",
            start_time=datetime.now(),
            last_activity=datetime.now(),
            session_type="standard",
        )
        
        # Save session
        self.state_manager.save_current_session(session)
        self.assertTrue(self.state_manager.has_active_session())
        
        # Load session
        loaded_session = self.state_manager.load_current_session()
        self.assertEqual(loaded_session.session_id, "test_session_001")
        
        # Archive session
        self.state_manager.archive_session(session)
        archive_path = self.state_manager.session_logs_path / "test_session_001.json"
        self.assertTrue(archive_path.exists())
        
        # Clear session
        self.state_manager.clear_current_session()
        self.assertFalse(self.state_manager.has_active_session())
    
    def test_atomic_write(self):
        """Test atomic write prevents corruption."""
        test_path = self.temp_path / "test.json"
        
        # Initial write
        data1 = {"version": "1.0", "data": "initial"}
        self.state_manager._atomic_write(test_path, data1)
        
        with open(test_path) as f:
            loaded = json.load(f)
        self.assertEqual(loaded["data"], "initial")
        
        # Update with atomic write
        data2 = {"version": "1.0", "data": "updated"}
        self.state_manager._atomic_write(test_path, data2)
        
        # Check backup was created
        backup_path = test_path.with_suffix(".bak")
        self.assertTrue(backup_path.exists())
        
        # Verify update
        with open(test_path) as f:
            loaded = json.load(f)
        self.assertEqual(loaded["data"], "updated")


class TestGovernanceGates(unittest.TestCase):
    """Test governance gate checking."""
    
    def setUp(self):
        """Set up test environment."""
        from osl_cli.governance.gates import GovernanceChecker
        
        now = datetime.now()
        thresholds = GovernanceThresholds(
            calibration_gate=GovernanceThreshold(min=75, current=80, max=85, last_adjusted=now),
            card_debt_multiplier=GovernanceThreshold(min=1.5, current=2.0, max=2.5, last_adjusted=now),
            max_new_cards=GovernanceThreshold(min=4, current=8, max=10, last_adjusted=now),
            interleaving_per_week=GovernanceThreshold(min=1, current=2, max=3, last_adjusted=now),
        )
        
        status = GovernanceStatus(
            calibration_gate="passing",
            card_debt_gate="passing",
            transfer_gate="passing",
            overall_state="NORMAL",
            remediation_active=False,
        )
        
        self.coach_state = CoachState(
            version="3.0",
            governance_thresholds=thresholds,
            governance_status=status,
        )
        
        self.checker = GovernanceChecker(self.coach_state)
    
    def test_calibration_gate_passing(self):
        """Test calibration gate when passing."""
        self.coach_state.performance_metrics.avg_retrieval_7d = 82
        result = self.checker.check_calibration_gate()
        
        self.assertTrue(result["passing"])
        self.assertEqual(result["status"], "Passing")
    
    def test_calibration_gate_failing(self):
        """Test calibration gate when failing."""
        self.coach_state.performance_metrics.avg_retrieval_7d = 70
        result = self.checker.check_calibration_gate()
        
        self.assertFalse(result["passing"])
        self.assertEqual(result["status"], "Failing")
        self.assertIn("Pause new content", result["action"])
    
    def test_card_debt_gate(self):
        """Test card debt gate checking."""
        self.coach_state.performance_metrics.daily_review_throughput = 60
        self.coach_state.performance_metrics.cards_due = 100
        
        result = self.checker.check_card_debt_gate()
        self.assertTrue(result["passing"])  # 100 < 60 * 2.0
        
        self.coach_state.performance_metrics.cards_due = 150
        result = self.checker.check_card_debt_gate()
        self.assertFalse(result["passing"])  # 150 > 60 * 2.0


if __name__ == "__main__":
    unittest.main()