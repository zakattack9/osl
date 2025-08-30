"""SHA256 content hashing for verbatim preservation.

This module provides cryptographic hashing to ensure learner-generated
content is preserved exactly as entered, with no AI modification.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime


class ContentHasher:
    """Handles SHA256 hashing and verification of content."""
    
    def __init__(self):
        """Initialize the content hasher."""
        self.hash_algorithm = "sha256"
        
    def hash_text(self, text: str) -> str:
        """Generate SHA256 hash of text content.
        
        Args:
            text: Text to hash
            
        Returns:
            Hex digest of SHA256 hash
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def hash_file(self, file_path: Path) -> str:
        """Generate SHA256 hash of file contents.
        
        Args:
            file_path: Path to file
            
        Returns:
            Hex digest of SHA256 hash
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            # Read in chunks for memory efficiency
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def verify_text(self, text: str, expected_hash: str) -> bool:
        """Verify text matches expected hash.
        
        Args:
            text: Text to verify
            expected_hash: Expected SHA256 hash
            
        Returns:
            True if hash matches, False otherwise
        """
        actual_hash = self.hash_text(text)
        return actual_hash == expected_hash
    
    def verify_file(self, file_path: Path, expected_hash: str) -> bool:
        """Verify file contents match expected hash.
        
        Args:
            file_path: Path to file
            expected_hash: Expected SHA256 hash
            
        Returns:
            True if hash matches, False otherwise
        """
        if not file_path.exists():
            return False
        
        actual_hash = self.hash_file(file_path)
        return actual_hash == expected_hash
    
    def create_content_record(
        self, 
        content: str, 
        content_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a content record with hash.
        
        Args:
            content: Content to record
            content_type: Type of content (recall, feynman, flashcard, etc.)
            metadata: Optional metadata to include
            
        Returns:
            Content record with hash
        """
        content_hash = self.hash_text(content)
        
        record = {
            "content": content,
            "content_type": content_type,
            "hash": content_hash,
            "hash_algorithm": self.hash_algorithm,
            "created_at": datetime.now().isoformat(),
            "modified": False,
            "verbatim": True
        }
        
        if metadata:
            record["metadata"] = metadata
        
        return record
    
    def detect_modification(
        self, 
        original: str, 
        current: str
    ) -> Dict[str, Any]:
        """Detect if content has been modified.
        
        Args:
            original: Original content
            current: Current content to check
            
        Returns:
            Dictionary with modification detection results
        """
        original_hash = self.hash_text(original)
        current_hash = self.hash_text(current)
        
        if original_hash == current_hash:
            return {
                "modified": False,
                "hash_match": True,
                "original_hash": original_hash,
                "current_hash": current_hash
            }
        
        # Detect type of modification
        modification_analysis = self._analyze_modification(original, current)
        
        return {
            "modified": True,
            "hash_match": False,
            "original_hash": original_hash,
            "current_hash": current_hash,
            "modification_type": modification_analysis["type"],
            "details": modification_analysis["details"]
        }
    
    def _analyze_modification(self, original: str, current: str) -> Dict[str, Any]:
        """Analyze the type of modification made.
        
        Args:
            original: Original text
            current: Modified text
            
        Returns:
            Analysis of modification type
        """
        # Check for AI modification patterns
        ai_patterns = [
            "The user said:",
            "They mentioned:",
            "According to:",
            "In summary,",
            "To summarize,",
            "paraphrased:",
            "In other words:",
        ]
        
        for pattern in ai_patterns:
            if pattern in current and pattern not in original:
                return {
                    "type": "ai_paraphrase",
                    "details": f"AI pattern detected: '{pattern}'"
                }
        
        # Check for whitespace changes
        if original.strip() == current.strip():
            return {
                "type": "whitespace_only",
                "details": "Only whitespace differences"
            }
        
        # Check for truncation
        if current in original:
            return {
                "type": "truncation",
                "details": f"Content truncated from {len(original)} to {len(current)} characters"
            }
        
        # Check for expansion
        if original in current:
            return {
                "type": "expansion",
                "details": f"Content expanded from {len(original)} to {len(current)} characters"
            }
        
        # General modification
        return {
            "type": "general_modification",
            "details": "Content has been altered"
        }


class HashRegistry:
    """Registry for tracking content hashes across a session."""
    
    def __init__(self, session_id: str, base_path: Optional[Path] = None):
        """Initialize hash registry.
        
        Args:
            session_id: Current session ID
            base_path: Base path for storage (defaults to ./osl/ai_state)
        """
        self.session_id = session_id
        self.base_path = base_path or Path.cwd() / "osl" / "ai_state"
        self.registry_path = self.base_path / "hash_registry" / f"{session_id}.json"
        self.hasher = ContentHasher()
        self.registry: Dict[str, Any] = self._load_registry()
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load existing registry or create new one.
        
        Returns:
            Registry dictionary
        """
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        
        return {
            "session_id": self.session_id,
            "created_at": datetime.now().isoformat(),
            "hashes": {},
            "verification_count": 0,
            "modification_attempts": 0
        }
    
    def _save_registry(self) -> None:
        """Save registry to disk."""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def register_content(
        self, 
        content_id: str, 
        content: str, 
        content_type: str
    ) -> str:
        """Register content with hash.
        
        Args:
            content_id: Unique identifier for content
            content: Content to register
            content_type: Type of content
            
        Returns:
            Hash of registered content
        """
        content_hash = self.hasher.hash_text(content)
        
        self.registry["hashes"][content_id] = {
            "hash": content_hash,
            "content_type": content_type,
            "registered_at": datetime.now().isoformat(),
            "verified": False,
            "verification_count": 0
        }
        
        self._save_registry()
        return content_hash
    
    def verify_content(
        self, 
        content_id: str, 
        content: str
    ) -> Dict[str, Any]:
        """Verify content against registered hash.
        
        Args:
            content_id: Content identifier
            content: Content to verify
            
        Returns:
            Verification result
        """
        if content_id not in self.registry["hashes"]:
            return {
                "valid": False,
                "error": f"Content ID '{content_id}' not found in registry",
                "registered": False
            }
        
        registered = self.registry["hashes"][content_id]
        expected_hash = registered["hash"]
        actual_hash = self.hasher.hash_text(content)
        
        # Update verification count
        self.registry["verification_count"] += 1
        registered["verification_count"] += 1
        registered["last_verified"] = datetime.now().isoformat()
        
        if actual_hash == expected_hash:
            registered["verified"] = True
            self._save_registry()
            
            return {
                "valid": True,
                "hash_match": True,
                "content_id": content_id,
                "content_type": registered["content_type"]
            }
        else:
            # Track modification attempt
            self.registry["modification_attempts"] += 1
            registered["modification_detected"] = datetime.now().isoformat()
            self._save_registry()
            
            return {
                "valid": False,
                "hash_match": False,
                "error": "Content has been modified",
                "expected_hash": expected_hash,
                "actual_hash": actual_hash,
                "content_id": content_id,
                "content_type": registered["content_type"]
            }
    
    def get_registry_summary(self) -> Dict[str, Any]:
        """Get summary of hash registry.
        
        Returns:
            Summary statistics
        """
        total_hashes = len(self.registry["hashes"])
        verified_count = sum(
            1 for h in self.registry["hashes"].values() 
            if h.get("verified", False)
        )
        
        content_types = {}
        for hash_data in self.registry["hashes"].values():
            ct = hash_data["content_type"]
            content_types[ct] = content_types.get(ct, 0) + 1
        
        return {
            "session_id": self.session_id,
            "total_hashes": total_hashes,
            "verified_count": verified_count,
            "verification_rate": verified_count / total_hashes if total_hashes > 0 else 0,
            "total_verifications": self.registry["verification_count"],
            "modification_attempts": self.registry["modification_attempts"],
            "content_types": content_types
        }
    
    def export_hashes(self) -> Dict[str, str]:
        """Export all hashes for archival.
        
        Returns:
            Dictionary of content_id -> hash
        """
        return {
            content_id: data["hash"]
            for content_id, data in self.registry["hashes"].items()
        }