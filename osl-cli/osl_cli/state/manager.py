"""State management for OSL."""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

from osl_cli.state.schemas import CoachState, SessionState


class StateManager:
    """Manages OSL state files with atomic writes and versioning."""
    
    def __init__(self, base_path: Optional[Path] = None):
        """Initialize state manager.
        
        Args:
            base_path: Base OSL directory path. Defaults to ./osl
        """
        self.base_path = base_path or Path.cwd() / "osl"
        self.ai_state_path = self.base_path / "ai_state"
        self.coach_state_path = self.ai_state_path / "coach_state.json"
        self.current_session_path = self.ai_state_path / "current_session.json"
        self.session_logs_path = self.ai_state_path / "session_logs"
        
    def _atomic_write(self, path: Path, data: dict) -> None:
        """Write data atomically to prevent corruption.
        
        Args:
            path: File path to write
            data: Data to write as JSON
        """
        # Write to temp file first
        temp_path = path.with_suffix(".tmp")
        
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        
        # Create backup if file exists
        if path.exists():
            backup_path = path.with_suffix(".bak")
            shutil.copy2(path, backup_path)
        
        # Atomic rename
        temp_path.replace(path)
    
    def load_coach_state(self) -> CoachState:
        """Load coach state from disk.
        
        Returns:
            CoachState object
            
        Raises:
            FileNotFoundError: If coach_state.json doesn't exist
        """
        if not self.coach_state_path.exists():
            raise FileNotFoundError(
                f"Coach state not found at {self.coach_state_path}. "
                "Run 'osl init' first."
            )
        
        with open(self.coach_state_path) as f:
            data = json.load(f)
        
        # Parse datetime strings back to datetime objects
        return CoachState.model_validate(data)
    
    def save_coach_state(self, state: CoachState) -> None:
        """Save coach state to disk atomically.
        
        Args:
            state: CoachState to save
        """
        state.last_updated = datetime.now()
        self._atomic_write(self.coach_state_path, state.model_dump(mode="json"))
    
    def has_active_session(self) -> bool:
        """Check if there's an active session.
        
        Returns:
            True if current_session.json exists
        """
        return self.current_session_path.exists()
    
    def load_current_session(self) -> SessionState:
        """Load current session state.
        
        Returns:
            SessionState object
            
        Raises:
            FileNotFoundError: If no active session
        """
        if not self.has_active_session():
            raise FileNotFoundError("No active session found")
        
        with open(self.current_session_path) as f:
            data = json.load(f)
        
        return SessionState.model_validate(data)
    
    def save_current_session(self, session: SessionState) -> None:
        """Save current session state atomically.
        
        Args:
            session: SessionState to save
        """
        session.last_activity = datetime.now()
        self._atomic_write(self.current_session_path, session.model_dump(mode="json"))
    
    def clear_current_session(self) -> None:
        """Remove current session file."""
        if self.current_session_path.exists():
            # Back it up first
            backup_path = self.current_session_path.with_suffix(".last")
            shutil.move(self.current_session_path, backup_path)
    
    def archive_session(self, session: SessionState) -> None:
        """Archive session to session_logs.
        
        Args:
            session: Session to archive
        """
        # Ensure session_logs directory exists
        self.session_logs_path.mkdir(parents=True, exist_ok=True)
        
        # Create archive path with session ID
        archive_path = self.session_logs_path / f"{session.session_id}.json"
        
        # Write session data
        with open(archive_path, "w") as f:
            json.dump(session.model_dump(mode="json"), f, indent=2, default=str)
    
    def migrate_state_if_needed(self) -> None:
        """Check and migrate state files if version mismatch.
        
        This handles migration from version 2.x to 3.0
        """
        if not self.coach_state_path.exists():
            return
        
        with open(self.coach_state_path) as f:
            data = json.load(f)
        
        current_version = data.get("version", "2.0")
        
        if current_version == "3.0":
            return  # Already current
        
        # Perform migration
        print(f"Migrating state from version {current_version} to 3.0...")
        
        # Backup old state
        backup_path = self.coach_state_path.with_name(f"coach_state_v{current_version}.bak")
        shutil.copy2(self.coach_state_path, backup_path)
        
        # Migration logic would go here
        # For now, we'll require manual migration or fresh init
        print(f"Old state backed up to {backup_path}")
        print("Please run 'osl init --force' to create fresh v3.0 state")