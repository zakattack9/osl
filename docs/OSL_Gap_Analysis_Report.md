# OSL Gap Analysis Report
_Full analysis of V3 Core, Implementation Guide, Automation Spec, and User Interaction Guide_

## Critical Violations Requiring Immediate Fix

### 1. AI Must Not Generate Learning Content
**Current Problem**: 
- osl-tutor generates retrieval questions
- System suggests flashcards based on gaps
- AI creates weekly quizzes

**Core Principle Violated**: Retrieval practice, Self-explanation, Curiosity-driven questioning

**Required Changes**:
```markdown
# osl-tutor.md (REVISED)
The tutor ONLY:
- Asks questions PROVIDED by the learner or from pre-made banks
- Gives feedback on learner's answers with citations
- Tracks what the learner self-identifies as gaps

The tutor NEVER:
- Generates new questions
- Suggests what should become a flashcard
- Decides what concepts are important
```

### 2. Flashcard Creation Must Be Learner-Driven
**Current Problem**: AI suggests cards based on "missed" content

**Required Changes**:
```python
# CLI Implementation
def create_flashcard(self, args):
    # Learner provides full card content
    # AI only helps with:
    # - Formatting (cloze syntax)
    # - Citation verification
    # - Checking against 8-card limit
    
    if self.session_cards_count >= 8:
        return self.error_with_suggestion(
            "Card limit (8) reached for this session",
            "Review existing cards or save for next session"
        )
```

### 3. Quiz Questions from Banks, Not AI Generation
**Current Problem**: AI generates quiz questions

**Required Changes**:
- Maintain question banks per topic in `quiz_bank/`
- Learner can contribute questions to banks
- AI only selects and administers questions
- OR learner writes their own quiz questions

## Inconsistencies to Resolve

### 1. State Schema Standardization
**Use Implementation Guide L3 as authoritative**:
```json
{
  "last_updated": "YYYY-MM-DD HH:MM",
  "active_books": [...],
  "review_schedule": {...},
  "performance_metrics": {...},
  "governance_status": {...}
}
```

### 2. Include Tuning Ranges
**All governance parameters need ranges**:
- Calibration Gate: 75-85% (default 80%)
- Card Debt: 1.5x-2.5x (default 2x)
- New Cards: 4-10 (default 8)
- Interleaving: 1-3x/week (default 2x)

### 3. Standardize Micro-Loop Triggers
**Consistent across all documents**:
- Technical books: 5-10 pages
- Literature: 1 scene or chapter
- Dense material: 3-5 pages
- User decides based on natural breaks

## Missing Implementation Details

### 1. Curiosity Question Tracking
**Add to CLI**:
```bash
osl questions add --question "How does X relate to Y?"
osl questions list --session current
osl questions resolve --id 1 --answer "Found on page 45: ..."
osl questions pending  # Shows unresolved questions
```

**Add to Session State**:
```json
{
  "curiosity_questions": [
    {
      "id": 1,
      "question": "How does X relate to Y?",
      "created": "timestamp",
      "resolved": false,
      "answer": null,
      "page_found": null
    }
  ]
}
```

### 2. Misconception Workflow
**Clear identification process**:
1. During micro-loop Q&A, learner notices confusion
2. Learner explicitly flags: "I was wrong about X"
3. CLI: `osl misconception add --concept "X" --wrong "my understanding" --correct "actual"`
4. Tracked for targeted review

### 3. Per-Micro-Loop Retrieval Tracking
**Immediate self-assessment**:
```python
# After each micro-loop
osl micro-loop complete \
  --pages "45-50" \
  --recall-quality "partial" \
  --confidence 3 \
  --gaps "concept-x, formula-y"
```

### 4. Card Creation Limits
**Enforce at CLI level**:
```python
def check_card_limit(self):
    if self.session_cards >= 8:
        if self.governance['calibration'] < 80:
            return 4  # Reduced limit
        return 8
    return 8 - self.session_cards
```

## Workflow Clarifications Needed

### 1. Permanent Note Link Discovery
**Current**: AI finds related notes
**Should be**: 
- Learner searches for connections
- AI can show list of existing notes by title
- Learner decides what links to create

### 2. Citation Auto-filling
**Current**: System auto-fills
**Should be**:
- Learner types citation (reinforces source awareness)
- System can verify format
- System can suggest format template

### 3. Session Metrics Collection
**Current**: Collected at end
**Should be**:
- Continuous collection during session
- Each micro-loop updates metrics
- End-of-session is just summary

## Recommended Additions

### 1. Verbatim Preservation for All Learning Activities
```python
# Preserve exactly what learner wrote
def preserve_recall(self, user_text):
    return {
        'raw': user_text,
        'hash': hashlib.sha256(user_text.encode()).hexdigest(),
        'timestamp': datetime.now().isoformat(),
        'type': 'free_recall'
    }
```

### 2. Explicit Learning/Admin Boundary
```python
# In every command, clearly mark:
class CLICommand:
    def __init__(self):
        self.type = "LEARNING" | "ADMIN"
        # LEARNING = requires human cognition
        # ADMIN = can be automated
```

### 3. Session State Machine Enhancement
Add states for curiosity questions:
- `QUESTIONS_PENDING`: After preview, before reading
- `QUESTION_RESOLVED`: When learner finds answer
- `QUESTIONS_REVIEW`: End of session check

## Summary of Required Actions

1. **Revise osl-tutor subagent** - Remove all generation capabilities
2. **Update flashcard workflow** - Learner creates, AI formats
3. **Fix quiz system** - Use question banks, not generation
4. **Standardize schemas** - Single source of truth
5. **Add curiosity question tracking** - Full lifecycle support
6. **Implement per-micro-loop metrics** - Real-time calibration
7. **Enforce card limits** - CLI-level validation
8. **Clarify misconception workflow** - Learner-driven identification
9. **Preserve all learning inputs** - Verbatim with hashing
10. **Document learning/admin boundary** - Explicit in every component

## Validation Checklist

Before proceeding to implementation, ensure:
- [ ] No AI generates learning content
- [ ] All learner inputs preserved verbatim
- [ ] State machine enforces proper sequence
- [ ] CLI validates all limits and gates
- [ ] Curiosity questions tracked throughout
- [ ] Metrics collected in real-time
- [ ] Clear learning vs admin boundaries
- [ ] All schemas consistent across docs
- [ ] Tuning ranges included everywhere
- [ ] User Guide matches implementation exactly