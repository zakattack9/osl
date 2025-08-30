# OSL Infrastructure Specification
_Minimal viable structure for OSL implementation_

## Directory Structure

```
osl/
├── ai_state/                    # All AI and session state
│   ├── coach_state.json        # Central governance and metrics
│   ├── current_session.json    # Active session data
│   ├── session_logs/           # Historical sessions
│   │   └── YYYYMMDD_HHMMSS.json
│   ├── misconceptions.json     # Tracked misconceptions
│   └── backups/                # Automatic state backups
│
├── quiz_bank/                   # Hybrid quiz storage
│   ├── {book_name}/            # Per-book organization
│   │   ├── chapter_1/
│   │   │   ├── quiz_001.md    # Human-readable
│   │   │   ├── quiz_001.json  # Machine-parseable
│   │   │   └── results.json   # Performance tracking
│   │   └── synthesis/
│   │       └── week_3_quiz.md
│   └── index.json              # Master quiz index
│
├── obsidian/                    # Note-taking vault
│   └── [standard structure per Implementation Guide]
│
├── anki/                        # Flashcard integration
│   └── [standard structure per Implementation Guide]
│
├── scripts/                     # Essential automation
│   ├── session_start.py        # Session initialization
│   ├── session_end.py          # Session completion
│   ├── calculate_metrics.py    # Metric calculations
│   ├── check_governance.py     # Gate validation
│   └── backup_state.py         # State preservation
│
└── temp/                        # Temporary files
    ├── .session_timer          # Current session timing
    └── .quiz_state.json        # Quiz state machine
```

## State File Specifications

### 1. coach_state.json (Authoritative)
```json
{
  "version": "3.0",
  "last_updated": "2025-01-29T10:30:00Z",
  "active_books": [
    {
      "id": "deep_work_2025",
      "title": "Deep Work",
      "author": "Cal Newport",
      "start_date": "2025-01-15",
      "current_page": 147,
      "total_pages": 296,
      "sessions_completed": 12,
      "avg_retrieval_score": 82
    }
  ],
  "governance_thresholds": {
    "calibration_gate": {"min": 75, "current": 80, "max": 85},
    "card_debt_multiplier": {"min": 1.5, "current": 2.0, "max": 2.5},
    "max_new_cards": {"min": 4, "current": 8, "max": 10},
    "interleaving_per_week": {"min": 1, "current": 2, "max": 3}
  },
  "governance_status": {
    "calibration_gate": "passing",
    "card_debt_gate": "passing",
    "transfer_gate": "passing",
    "overall_state": "NORMAL"
  },
  "performance_metrics": {
    "7d_avg_retrieval": 82,
    "7d_avg_prediction_accuracy": 78,
    "current_card_debt_ratio": 1.3,
    "daily_review_throughput": 60,
    "last_transfer_project": "2025-01-01",
    "interleaving_sessions_week": 2
  },
  "review_schedule": {
    "next_interleaving": "2025-01-30",
    "next_calibration": "2025-02-01",
    "next_synthesis": "2025-02-01",
    "next_project_due": "2025-02-15"
  }
}
```

### 2. current_session.json (Real-time)
```json
{
  "session_id": "20250129_103000",
  "book": "Deep Work",
  "start_time": "2025-01-29T10:30:00Z",
  "state": "READING",
  "pages_read": "45-55",
  "curiosity_questions": [
    {
      "id": 1,
      "question": "How does deep work relate to flow?",
      "created": "10:32:00",
      "resolved": true,
      "answer": "Different concepts - one is practice, other is experience",
      "page_found": 48
    }
  ],
  "micro_loops_completed": [
    {
      "loop_id": 1,
      "pages": "45-50",
      "recall_quality": "complete",
      "confidence": 4,
      "gaps_identified": ["4-hour limit"],
      "tutor_questions_answered": 3,
      "correct_answers": 3
    }
  ],
  "flashcards_created": 5,
  "permanent_notes_created": 2,
  "misconceptions_identified": 1,
  "real_time_retrieval_rate": 87
}
```

### 3. misconceptions.json
```json
{
  "active_misconceptions": [
    {
      "id": "misc_001",
      "concept": "deep work vs flow",
      "wrong_understanding": "They are the same thing",
      "correct_understanding": "Deep work is practice, flow is experience",
      "identified_date": "2025-01-29",
      "identified_during": "session_20250129_103000",
      "resolved": false
    }
  ],
  "resolved_misconceptions": [
    {
      "id": "misc_000",
      "concept": "spacing intervals",
      "resolution_date": "2025-01-28",
      "resolution_method": "targeted_practice"
    }
  ]
}
```

### 4. quiz_bank/{book}/chapter_1/quiz_001.json
```json
{
  "quiz_id": "deep_work_ch1_001",
  "created": "2025-01-29",
  "type": "weekly_calibration",
  "questions": [
    {
      "id": 1,
      "type": "recall",
      "text": "What are the two core abilities for thriving in the new economy?",
      "answer": "1) Quickly master hard things, 2) Produce at elite level",
      "source": "p. 29",
      "tags": ["core_concept"]
    },
    {
      "id": 2,
      "type": "application",
      "text": "Design a deep work routine for an open office",
      "answer": "Varies - evaluate based on principle application",
      "source": "p. 34-40",
      "rubric": {
        "time_blocking": 1,
        "distraction_elimination": 1,
        "environment_design": 1
      }
    }
  ]
}
```

### 5. quiz_bank/{book}/chapter_1/quiz_001.md
```markdown
---
type: quiz
quiz_id: deep_work_ch1_001
book: Deep Work
chapter: 1
created: 2025-01-29
---

# Quiz: Deep Work Chapter 1

## Q1: Recall
**Question**: What are the two core abilities for thriving in the new economy?
**Answer**: 1) Quickly master hard things, 2) Produce at elite level
**Source**: p. 29
**Your Confidence**: ___/5
**Your Answer**: ________________________
**Correct?**: ___

## Q2: Application
**Question**: Design a deep work routine for an open office
**Answer**: [Open-ended - check principle application]
**Source**: p. 34-40
**Your Confidence**: ___/5
**Your Answer**: ________________________
**Score**: ___/3 (time-blocking, distraction-elimination, environment)
```

## Session Timer Implementation

### Simple File-Based Timer
```bash
# Start timer (writes timestamp)
echo $(date +%s) > osl/temp/.session_timer

# Check elapsed (read and calculate)
start=$(cat osl/temp/.session_timer)
now=$(date +%s)
elapsed=$((now - start))
echo "Session time: $((elapsed / 60)) minutes"

# Clear timer
rm osl/temp/.session_timer
```

### Alternative: In-Memory State
Store in `current_session.json`:
```json
{
  "timer": {
    "start": 1706527800,
    "last_check": 1706529600,
    "elapsed_seconds": 1800
  }
}
```

## Essential Scripts

### session_start.py
```python
#!/usr/bin/env python3
"""Initialize new OSL session with governance checks"""
import json
import os
from datetime import datetime
from pathlib import Path

def start_session(book=None):
    # Check governance gates
    with open('ai_state/coach_state.json') as f:
        state = json.load(f)
    
    if state['governance_status']['card_debt_gate'] == 'failing':
        return {"error": "Card debt too high", "action": "Review first"}
    
    # Create session
    session = {
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "book": book or state['active_books'][0]['title'],
        "start_time": datetime.now().isoformat(),
        "state": "READING"
    }
    
    # Save session
    with open('ai_state/current_session.json', 'w') as f:
        json.dump(session, f, indent=2)
    
    # Start timer
    Path('temp/.session_timer').write_text(str(datetime.now().timestamp()))
    
    return {"status": "success", "session_id": session['session_id']}
```

### calculate_metrics.py
```python
#!/usr/bin/env python3
"""Deterministic metric calculations"""

def calculate_retrieval_rate(successful, total):
    if total == 0:
        return 0.0
    return (successful / total) * 100

def calculate_calibration_score(predictions, actuals):
    """Brier score based calibration"""
    if len(predictions) != len(actuals):
        raise ValueError("Mismatched lengths")
    
    score = sum((p/5 - a)**2 for p, a in zip(predictions, actuals))
    return (1 - score/len(predictions)) * 100

def calculate_card_debt_ratio(due_cards, daily_throughput):
    if daily_throughput == 0:
        return float('inf')
    return due_cards / daily_throughput
```

### check_governance.py
```python
#!/usr/bin/env python3
"""Validate governance gates"""
import json

def check_all_gates():
    with open('ai_state/coach_state.json') as f:
        state = json.load(f)
    
    metrics = state['performance_metrics']
    thresholds = state['governance_thresholds']
    status = {}
    
    # Calibration gate
    if metrics['7d_avg_retrieval'] < thresholds['calibration_gate']['current']:
        status['calibration_gate'] = 'failing'
    else:
        status['calibration_gate'] = 'passing'
    
    # Card debt gate
    if metrics['current_card_debt_ratio'] > thresholds['card_debt_multiplier']['current']:
        status['card_debt_gate'] = 'failing'
    else:
        status['card_debt_gate'] = 'passing'
    
    # Transfer gate (monthly)
    days_since = (datetime.now() - datetime.fromisoformat(metrics['last_transfer_project'])).days
    if days_since > 30:
        status['transfer_gate'] = 'warning'
    else:
        status['transfer_gate'] = 'passing'
    
    return status
```

### backup_state.py
```python
#!/usr/bin/env python3
"""Automatic state backups before modifications"""
import shutil
from datetime import datetime
from pathlib import Path

def backup_state():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Backup coach state
    if Path('ai_state/coach_state.json').exists():
        shutil.copy(
            'ai_state/coach_state.json',
            f'ai_state/backups/coach_state_{timestamp}.json'
        )
    
    # Backup current session
    if Path('ai_state/current_session.json').exists():
        shutil.copy(
            'ai_state/current_session.json',
            f'ai_state/backups/session_{timestamp}.json'
        )
    
    # Clean old backups (keep last 10)
    backups = sorted(Path('ai_state/backups').glob('*.json'))
    if len(backups) > 10:
        for old_backup in backups[:-10]:
            old_backup.unlink()
```

## Initialization Script

```bash
#!/bin/bash
# init_osl_infrastructure.sh

echo "Creating OSL infrastructure..."

# Create directories
mkdir -p osl/{ai_state,quiz_bank,scripts,temp}
mkdir -p osl/ai_state/{session_logs,backups}

# Initialize state files
cat > osl/ai_state/coach_state.json << 'EOF'
{
  "version": "3.0",
  "last_updated": "",
  "active_books": [],
  "governance_thresholds": {
    "calibration_gate": {"min": 75, "current": 80, "max": 85},
    "card_debt_multiplier": {"min": 1.5, "current": 2.0, "max": 2.5},
    "max_new_cards": {"min": 4, "current": 8, "max": 10},
    "interleaving_per_week": {"min": 1, "current": 2, "max": 3}
  },
  "governance_status": {
    "calibration_gate": "passing",
    "card_debt_gate": "passing",
    "transfer_gate": "passing",
    "overall_state": "NORMAL"
  },
  "performance_metrics": {
    "7d_avg_retrieval": 0,
    "7d_avg_prediction_accuracy": 0,
    "current_card_debt_ratio": 0,
    "daily_review_throughput": 0,
    "last_transfer_project": "",
    "interleaving_sessions_week": 0
  },
  "review_schedule": {
    "next_interleaving": "",
    "next_calibration": "",
    "next_synthesis": "",
    "next_project_due": ""
  }
}
EOF

cat > osl/ai_state/misconceptions.json << 'EOF'
{
  "active_misconceptions": [],
  "resolved_misconceptions": []
}
EOF

echo "✅ Infrastructure created successfully"
```

## Key Design Decisions

1. **JSON for state**: Human-readable, git-friendly, universal
2. **Hybrid quiz format**: Markdown for humans, JSON for automation
3. **Simple timers**: File-based for portability
4. **Atomic writes**: Always backup before modification
5. **Flat structure**: Easy to navigate and understand