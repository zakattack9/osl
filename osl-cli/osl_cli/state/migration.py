"""Schema migration system for OSL state files.

This module handles versioning and migration of state schemas,
ensuring backward compatibility and smooth upgrades.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
from abc import ABC, abstractmethod


class Migration(ABC):
    """Abstract base class for migrations."""
    
    @property
    @abstractmethod
    def from_version(self) -> str:
        """Source version for this migration."""
        pass
    
    @property
    @abstractmethod
    def to_version(self) -> str:
        """Target version for this migration."""
        pass
    
    @abstractmethod
    def migrate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply migration to data.
        
        Args:
            data: State data to migrate
            
        Returns:
            Migrated data
        """
        pass
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate data after migration.
        
        Args:
            data: Migrated data to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass


class MigrationV1ToV2(Migration):
    """Migration from version 1.0 to 2.0."""
    
    @property
    def from_version(self) -> str:
        return "1.0"
    
    @property
    def to_version(self) -> str:
        return "2.0"
    
    def migrate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add real-time metrics to version 1.0 data."""
        # Add performance metrics if not present
        if "performance_metrics" not in data:
            data["performance_metrics"] = {
                "7d_avg_retrieval": 0.0,
                "7d_avg_prediction_accuracy": 0.0,
                "current_card_debt_ratio": 0.0,
                "daily_review_throughput": 60,
                "cards_due": 0,
                "cards_completed_today": 0,
                "last_transfer_project": None,
                "interleaving_sessions_week": 0,
                "total_permanent_notes": 0,
                "total_flashcards": 0,
                "misconceptions_active": 0,
                "misconceptions_resolved": 0
            }
        
        # Add review schedule if not present
        if "review_schedule" not in data:
            data["review_schedule"] = {
                "next_interleaving": None,
                "next_calibration": None,
                "next_synthesis": None,
                "next_project_due": None,
                "daily_review_time": "07:00"
            }
        
        # Update version
        data["version"] = self.to_version
        data["last_migration"] = datetime.now().isoformat()
        
        return data
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate v2.0 structure."""
        required_keys = ["version", "performance_metrics", "review_schedule"]
        return all(key in data for key in required_keys)


class MigrationV2ToV3(Migration):
    """Migration from version 2.0 to 3.0."""
    
    @property
    def from_version(self) -> str:
        return "2.0"
    
    @property
    def to_version(self) -> str:
        return "3.0"
    
    def migrate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add misconception tracking and content hashing to v2.0 data."""
        # Ensure governance thresholds have proper structure
        if "governance_thresholds" in data:
            for threshold_name, threshold_data in data["governance_thresholds"].items():
                if isinstance(threshold_data, (int, float)):
                    # Convert simple value to threshold object
                    data["governance_thresholds"][threshold_name] = {
                        "min": threshold_data * 0.8,
                        "current": threshold_data,
                        "max": threshold_data * 1.2,
                        "last_adjusted": datetime.now().isoformat()
                    }
        else:
            # Add default governance thresholds
            data["governance_thresholds"] = {
                "calibration_gate": {
                    "min": 75,
                    "current": 80,
                    "max": 85,
                    "last_adjusted": datetime.now().isoformat()
                },
                "card_debt_multiplier": {
                    "min": 1.5,
                    "current": 2.0,
                    "max": 2.5,
                    "last_adjusted": datetime.now().isoformat()
                },
                "max_new_cards": {
                    "min": 4,
                    "current": 8,
                    "max": 10,
                    "last_adjusted": datetime.now().isoformat()
                },
                "interleaving_per_week": {
                    "min": 1,
                    "current": 2,
                    "max": 3,
                    "last_adjusted": datetime.now().isoformat()
                }
            }
        
        # Ensure governance status exists
        if "governance_status" not in data:
            data["governance_status"] = {
                "calibration_gate": "passing",
                "card_debt_gate": "passing",
                "transfer_gate": "passing",
                "overall_state": "NORMAL",
                "last_gate_trigger": None,
                "remediation_active": False
            }
        
        # Add state history tracking if in session data
        if "session_id" in data and "state_history" not in data:
            data["state_history"] = []
        
        # Add content hash tracking placeholders
        if "session_id" in data:
            if "content_hashes" not in data:
                data["content_hashes"] = {
                    "recall_texts": [],
                    "feynman_texts": [],
                    "flashcard_contents": []
                }
        
        # Update version
        data["version"] = self.to_version
        data["last_migration"] = datetime.now().isoformat()
        
        return data
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate v3.0 structure."""
        # Check for proper governance structure
        if "governance_thresholds" in data:
            for threshold in data["governance_thresholds"].values():
                if not isinstance(threshold, dict):
                    return False
                if not all(k in threshold for k in ["min", "current", "max"]):
                    return False
        
        return data.get("version") == "3.0"


class MigrationManager:
    """Manages state file migrations across versions."""
    
    # Supported schema versions
    CURRENT_VERSION = "3.0"
    SUPPORTED_VERSIONS = ["1.0", "2.0", "3.0"]
    
    def __init__(self, base_path: Optional[Path] = None):
        """Initialize migration manager.
        
        Args:
            base_path: Base OSL directory path
        """
        self.base_path = base_path or Path.cwd() / "osl"
        self.migrations: List[Migration] = [
            MigrationV1ToV2(),
            MigrationV2ToV3()
        ]
        self.migration_log_path = self.base_path / "ai_state" / "migration_log.json"
        self.migration_log = self._load_migration_log()
    
    def _load_migration_log(self) -> Dict[str, Any]:
        """Load migration history log.
        
        Returns:
            Migration log dictionary
        """
        if self.migration_log_path.exists():
            with open(self.migration_log_path, 'r') as f:
                return json.load(f)
        
        return {
            "migrations": [],
            "last_migration": None,
            "current_version": self.CURRENT_VERSION
        }
    
    def _save_migration_log(self) -> None:
        """Save migration log to disk."""
        self.migration_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.migration_log_path, 'w') as f:
            json.dump(self.migration_log, f, indent=2)
    
    def _log_migration(
        self, 
        file_path: Path, 
        from_version: str, 
        to_version: str,
        success: bool,
        error: Optional[str] = None
    ) -> None:
        """Log a migration attempt.
        
        Args:
            file_path: File that was migrated
            from_version: Source version
            to_version: Target version
            success: Whether migration succeeded
            error: Error message if failed
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "file": str(file_path),
            "from_version": from_version,
            "to_version": to_version,
            "success": success,
            "error": error
        }
        
        self.migration_log["migrations"].append(entry)
        
        if success:
            self.migration_log["last_migration"] = datetime.now().isoformat()
        
        self._save_migration_log()
    
    def get_version(self, data: Dict[str, Any]) -> str:
        """Get version from state data.
        
        Args:
            data: State data
            
        Returns:
            Version string, defaults to "1.0" if not present
        """
        return data.get("version", "1.0")
    
    def needs_migration(self, data: Dict[str, Any]) -> bool:
        """Check if data needs migration.
        
        Args:
            data: State data to check
            
        Returns:
            True if migration needed
        """
        current_version = self.get_version(data)
        return current_version != self.CURRENT_VERSION
    
    def get_migration_path(
        self, 
        from_version: str, 
        to_version: str
    ) -> List[Migration]:
        """Get sequence of migrations needed.
        
        Args:
            from_version: Starting version
            to_version: Target version
            
        Returns:
            List of migrations to apply in order
        """
        path = []
        current = from_version
        
        while current != to_version:
            # Find migration from current version
            migration = next(
                (m for m in self.migrations if m.from_version == current),
                None
            )
            
            if not migration:
                raise ValueError(f"No migration path from {from_version} to {to_version}")
            
            path.append(migration)
            current = migration.to_version
        
        return path
    
    def migrate_data(
        self, 
        data: Dict[str, Any], 
        target_version: Optional[str] = None
    ) -> Dict[str, Any]:
        """Migrate data to target version.
        
        Args:
            data: Data to migrate
            target_version: Target version (defaults to current)
            
        Returns:
            Migrated data
        """
        target = target_version or self.CURRENT_VERSION
        from_version = self.get_version(data)
        
        if from_version == target:
            return data  # Already at target version
        
        # Get migration path
        migrations = self.get_migration_path(from_version, target)
        
        # Apply migrations in sequence
        migrated_data = data.copy()
        for migration in migrations:
            migrated_data = migration.migrate(migrated_data)
            
            # Validate after each migration
            if not migration.validate(migrated_data):
                raise ValueError(
                    f"Migration from {migration.from_version} to "
                    f"{migration.to_version} failed validation"
                )
        
        return migrated_data
    
    def migrate_file(
        self, 
        file_path: Path, 
        backup: bool = True
    ) -> bool:
        """Migrate a state file to current version.
        
        Args:
            file_path: Path to state file
            backup: Whether to create backup
            
        Returns:
            True if migration succeeded
        """
        if not file_path.exists():
            return False
        
        # Load current data
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        from_version = self.get_version(data)
        
        if not self.needs_migration(data):
            return True  # Already current
        
        try:
            # Create backup if requested
            if backup:
                backup_path = file_path.with_suffix(f".v{from_version}.bak")
                shutil.copy2(file_path, backup_path)
            
            # Migrate data
            migrated_data = self.migrate_data(data)
            
            # Write migrated data
            with open(file_path, 'w') as f:
                json.dump(migrated_data, f, indent=2)
            
            # Log success
            self._log_migration(
                file_path, 
                from_version, 
                self.CURRENT_VERSION,
                success=True
            )
            
            return True
            
        except Exception as e:
            # Log failure
            self._log_migration(
                file_path,
                from_version,
                self.CURRENT_VERSION,
                success=False,
                error=str(e)
            )
            
            # Restore from backup if it was created
            if backup:
                backup_path = file_path.with_suffix(f".v{from_version}.bak")
                if backup_path.exists():
                    shutil.copy2(backup_path, file_path)
            
            return False
    
    def migrate_all_state_files(self) -> Dict[str, bool]:
        """Migrate all state files in the ai_state directory.
        
        Returns:
            Dictionary of file -> success status
        """
        ai_state_path = self.base_path / "ai_state"
        results = {}
        
        # Migrate coach_state.json
        coach_state_path = ai_state_path / "coach_state.json"
        if coach_state_path.exists():
            results[str(coach_state_path)] = self.migrate_file(coach_state_path)
        
        # Migrate current_session.json if exists
        current_session_path = ai_state_path / "current_session.json"
        if current_session_path.exists():
            results[str(current_session_path)] = self.migrate_file(current_session_path)
        
        # Migrate session logs
        session_logs_path = ai_state_path / "session_logs"
        if session_logs_path.exists():
            for session_file in session_logs_path.glob("*.json"):
                results[str(session_file)] = self.migrate_file(session_file)
        
        return results
    
    def get_migration_report(self) -> Dict[str, Any]:
        """Get report of migration history.
        
        Returns:
            Migration report
        """
        total_migrations = len(self.migration_log["migrations"])
        successful = sum(1 for m in self.migration_log["migrations"] if m["success"])
        failed = total_migrations - successful
        
        # Group by file
        by_file = {}
        for migration in self.migration_log["migrations"]:
            file_path = migration["file"]
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(migration)
        
        return {
            "current_version": self.CURRENT_VERSION,
            "total_migrations": total_migrations,
            "successful": successful,
            "failed": failed,
            "last_migration": self.migration_log["last_migration"],
            "files_migrated": len(by_file),
            "migration_history": by_file
        }