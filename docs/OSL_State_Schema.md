# OSL State Schema
_Authoritative data structures with versioning and migration support_

## Schema Version: 3.0

All state files include version for migration support:
```json
{
  "version": "3.0",
  "last_migration": "2025-01-29T10:00:00Z"
}
```

## 1. Coach State (Authoritative Central State)

**File:** `ai_state/coach_state.json`  
**Purpose:** Central governance, metrics, and scheduling  
**Update Frequency:** End of session, weekly rollups  

```json
{
  "version": "3.0",
  "last_updated": "2025-01-29T10:30:00Z",
  
  "active_books": [
    {
      "id": "deep_work_2025",
      "title": "Deep Work",
      "author": "Cal Newport", 
      "start_date": "2025-01-15T08:00:00Z",
      "current_page": 147,
      "total_pages": 296,
      "sessions_completed": 12,
      "total_hours": 9.5,
      "avg_retrieval_score": 82,
      "last_session": "2025-01-29T10:30:00Z"
    }
  ],
  
  "governance_thresholds": {
    "calibration_gate": {
      "min": 75,
      "current": 80,
      "max": 85,
      "last_adjusted": "2025-01-15T08:00:00Z"
    },
    "card_debt_multiplier": {
      "min": 1.5,
      "current": 2.0,
      "max": 2.5,
      "last_adjusted": "2025-01-15T08:00:00Z"
    },
    "max_new_cards": {
      "min": 4,
      "current": 8,
      "max": 10,
      "last_adjusted": "2025-01-15T08:00:00Z"
    },
    "interleaving_per_week": {
      "min": 1,
      "current": 2,
      "max": 3,
      "last_adjusted": "2025-01-15T08:00:00Z"
    }
  },
  
  "governance_status": {
    "calibration_gate": "passing",
    "card_debt_gate": "passing", 
    "transfer_gate": "passing",
    "overall_state": "NORMAL",
    "last_gate_trigger": null,
    "remediation_active": false
  },
  
  "performance_metrics": {
    "7d_avg_retrieval": 82,
    "7d_avg_prediction_accuracy": 78,
    "current_card_debt_ratio": 1.3,
    "daily_review_throughput": 60,
    "cards_due": 78,
    "cards_completed_today": 45,
    "last_transfer_project": "2025-01-01T12:00:00Z",
    "interleaving_sessions_week": 2,
    "total_permanent_notes": 47,
    "total_flashcards": 412,
    "misconceptions_active": 3,
    "misconceptions_resolved": 12
  },
  
  "review_schedule": {
    "next_interleaving": "2025-01-30T09:00:00Z",
    "next_calibration": "2025-02-01T10:00:00Z",
    "next_synthesis": "2025-02-01T11:00:00Z",
    "next_project_due": "2025-02-15T23:59:59Z",
    "daily_review_time": "07:00"
  }
}
```

## 2. Current Session State (Real-time)

**File:** `ai_state/current_session.json`  
**Purpose:** Active session tracking with real-time metrics  
**Update Frequency:** After each micro-loop, immediate  
**Cleared:** At session end (archived to session_logs)  

```json
{
  "version": "3.0",
  "session_id": "20250129_103000",
  "book_id": "deep_work_2025",
  "book_title": "Deep Work",
  "start_time": "2025-01-29T10:30:00Z",
  "last_activity": "2025-01-29T11:15:00Z",
  "duration_minutes": 45,
  "state": "READING",
  "state_history": [
    {"state": "SESSION_INIT", "timestamp": "10:30:00"},
    {"state": "READING", "timestamp": "10:32:00"}
  ],
  
  "curiosity_questions": [
    {
      "id": 1,
      "question": "How does deep work relate to flow state?",
      "created": "2025-01-29T10:32:00Z",
      "resolved": true,
      "answer": "Deep work is deliberate practice, flow is optimal experience",
      "page_found": 48,
      "resolved_at": "2025-01-29T10:45:00Z"
    },
    {
      "id": 2,
      "question": "What's the neuroscience behind attention residue?",
      "created": "2025-01-29T10:33:00Z",
      "resolved": false
    }
  ],
  
  "micro_loops": [
    {
      "loop_id": 1,
      "pages": "45-50",
      "chunk_type": "standard",
      "start_time": "2025-01-29T10:40:00Z",
      "end_time": "2025-01-29T10:47:00Z",
      
      "recall_data": {
        "duration_seconds": 90,
        "word_count": 147,
        "quality": "complete",
        "confidence": 4,
        "text_hash": "sha256:a3f2b8c9d4e5f6a7b8c9d0e1f2a3b4c5",
        "preserved_at": "2025-01-29T10:41:30Z"
      },
      
      "feynman_data": {
        "duration_seconds": 120,
        "word_count": 83,
        "text_hash": "sha256:b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9",
        "preserved_at": "2025-01-29T10:43:30Z"
      },
      
      "tutor_qa": {
        "questions_asked": 3,
        "questions_answered": 3,
        "correct_answers": 2,
        "confidence_ratings": [4, 3, 5],
        "actual_performance": [1, 1, 0],
        "feedback_provided": true
      },
      
      "gaps_identified": [
        "4-hour daily limit",
        "difference between deep work and shallow work"
      ],
      
      "retrieval_rate": 67
    }
  ],
  
  "flashcards_created": [
    {
      "card_id": "card_001",
      "created_at": "2025-01-29T10:48:00Z",
      "from_gap": "4-hour daily limit",
      "learner_authored": true,
      "content_hash": "sha256:c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9",
      "ai_assisted": false
    }
  ],
  
  "permanent_notes_created": [
    {
      "note_id": "note_001", 
      "created_at": "2025-01-29T11:10:00Z",
      "title": "Deep Work Time Limits",
      "links_created": 2
    }
  ],
  
  "misconceptions_identified": [
    {
      "misconception_id": "misc_001",
      "identified_at": "2025-01-29T10:45:00Z",
      "during_loop": 1
    }
  ],
  
  "real_time_metrics": {
    "pages_read": 10,
    "retrieval_attempts": 3,
    "successful_recalls": 2,
    "retrieval_rate": 67,
    "flashcards_count": 5,
    "flashcards_remaining": 3,
    "avg_confidence": 4,
    "avg_performance": 67
  }
}
```

## 3. Historical Session Log

**File:** `ai_state/session_logs/20250129_103000.json`  
**Purpose:** Permanent record of completed session  
**Created:** At session end from current_session.json  
**Immutable:** Never modified after creation  

```json
{
  "version": "3.0",
  "session_id": "20250129_103000",
  "book": "Deep Work",
  "date": "2025-01-29",
  "duration_minutes": 47,
  "pages_read": "45-55",
  
  "metrics_summary": {
    "micro_loops_completed": 2,
    "retrieval_rate": 75,
    "flashcards_created": 6,
    "permanent_notes": 2,
    "curiosity_questions_resolved": 3,
    "misconceptions_identified": 1
  },
  
  "governance_snapshot": {
    "calibration_gate": "passing",
    "card_debt_gate": "passing",
    "cards_remaining": 2
  },
  
  "content_hashes": {
    "recall_texts": [
      "sha256:a3f2b8c9d4e5f6a7b8c9d0e1f2a3b4c5",
      "sha256:d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9"
    ],
    "feynman_texts": [
      "sha256:b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9",
      "sha256:e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
    ],
    "flashcard_contents": [
      "sha256:c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9",
      "sha256:f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1"
    ]
  }
}
```

## 4. Misconceptions Tracking

**File:** `ai_state/misconceptions.json`  
**Purpose:** Track learning errors for targeted review  
**Update Frequency:** Real-time during sessions  

```json
{
  "version": "3.0",
  "last_updated": "2025-01-29T10:45:00Z",
  
  "active_misconceptions": [
    {
      "id": "misc_001",
      "concept": "deep work vs flow state",
      "wrong_understanding": "They are the same thing",
      "correct_understanding": "Deep work is deliberate practice, flow is optimal experience",
      "identified_date": "2025-01-29T10:45:00Z",
      "identified_session": "20250129_103000",
      "identified_book": "Deep Work",
      "review_count": 0,
      "scheduled_review": "2025-01-30T10:00:00Z"
    }
  ],
  
  "resolved_misconceptions": [
    {
      "id": "misc_000",
      "concept": "spacing intervals",
      "resolved_date": "2025-01-28T14:00:00Z",
      "resolution_method": "targeted_practice",
      "review_count": 3,
      "sessions_to_resolve": 2
    }
  ],
  
  "statistics": {
    "total_identified": 13,
    "currently_active": 1,
    "resolved_total": 12,
    "avg_reviews_to_resolve": 2.5,
    "most_common_category": "conceptual_confusion"
  }
}
```

## State Transitions

### Session Lifecycle
```
NONE → SESSION_INIT → READING → MICRO_LOOP* → NOTES → SESSION_END → ARCHIVED
```

### Micro-Loop States
```
READING → RECALL_PENDING → RECALL_ACTIVE → RECALL_COMPLETE →
FEYNMAN_PENDING → FEYNMAN_ACTIVE → FEYNMAN_COMPLETE →
TUTOR_QA_PENDING → TUTOR_QA_ACTIVE → TUTOR_QA_COMPLETE →
CARDS_PENDING → CARDS_ACTIVE → CARDS_COMPLETE → READING
```

### Governance States
```
NORMAL ←→ WARNING ←→ BLOCKED → REMEDIATION → RECOVERY → NORMAL
```

## Versioning and Migration

### Version History
- **1.0**: Initial schema
- **2.0**: Added real-time metrics
- **3.0**: Added misconceptions, verbatim hashes, state transitions

### Migration Strategy
```python
def migrate_state(state_data):
    current_version = state_data.get('version', '1.0')
    
    if current_version < '2.0':
        # Add real-time metrics
        state_data['real_time_metrics'] = {}
        
    if current_version < '3.0':
        # Add misconceptions tracking
        state_data['misconceptions_identified'] = []
        # Add content hashes
        state_data['content_hashes'] = {}
        
    state_data['version'] = '3.0'
    state_data['last_migration'] = datetime.now().isoformat()
    
    return state_data
```

## Validation Rules

### Required Fields
Every state file must have:
- `version`: Schema version
- `last_updated`: ISO timestamp
- Primary data structure for its type

### Data Integrity
- All timestamps in ISO 8601 format
- All hashes in SHA256
- All IDs unique within scope
- All percentages 0-100
- All counts >= 0

### Relationships
- Session IDs match pattern: `YYYYMMDD_HHMMSS`
- Book IDs are slugified: `deep_work_2025`
- Card IDs sequential: `card_001`, `card_002`
- Loop IDs sequential: 1, 2, 3

## Access Patterns

### Read Operations
- Load coach_state at session start
- Check current_session for state
- Query misconceptions for reviews

### Write Operations  
- Update current_session after each micro-loop
- Update coach_state at session end
- Archive to session_logs on completion
- Backup before any write

### Atomic Updates
```python
def safe_update_state(file_path, updates):
    # Backup
    backup_path = file_path.replace('.json', f'_{timestamp}.backup.json')
    shutil.copy(file_path, backup_path)
    
    # Load
    with open(file_path, 'r') as f:
        state = json.load(f)
    
    # Update
    state.update(updates)
    state['last_updated'] = datetime.now().isoformat()
    
    # Write atomically
    temp_path = file_path + '.tmp'
    with open(temp_path, 'w') as f:
        json.dump(state, f, indent=2)
    
    # Atomic rename
    os.rename(temp_path, file_path)
```

## Single Source of Truth

This document is the **authoritative schema** for OSL state management. All implementations must conform to these structures. Any deviations require:
1. Version increment
2. Migration code
3. Documentation update
4. Backward compatibility for 2 versions