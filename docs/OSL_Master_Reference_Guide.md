# OSL Master Reference Guide
_When and where to reference each document during CLI implementation and beyond_

## Document Classification

### 🔵 PERMANENT CORE (Methodology)
These define the OSL learning system itself:
- **V3_Core.md** - The methodology
- **V3_Implementation_Guide.md** - How to implement the methodology
- **V3_Decision_History.md** - Why decisions were made

### 🟢 PERMANENT SPECIFICATIONS (Guardrails)
These must be referenced continuously to maintain system integrity:
- **OSL_AI_Boundaries.md** - Critical learning protection
- **OSL_Flashcard_Philosophy.md** - Generation effect protection
- **OSL_Governance_Standards.md** - Authoritative thresholds
- **OSL_State_Schema.md** - Data structure authority
- **OSL_Natural_Language_Balance.md** - User control protection

### 🟡 PERMANENT CLARIFICATIONS (Principles)
These resolve ambiguities and must be referenced for correctness:
- **OSL_Activation_Probe.md** - Prevents quiz confusion
- **OSL_Guardrails_Checklist.md** - Daily practice reminder
- **OSL_User_Interaction_Guide.md** - User experience patterns

### 🟠 IMPLEMENTATION REFERENCES (Semi-Permanent)
These guide implementation but could be absorbed into code:
- **OSL_Infrastructure_Spec.md** - Directory/file setup
- **OSL_Concept_Map_Implementation.md** - Feature implementation
- **OSL_Interleaving_Specification.md** - Feature implementation
- **OSL_Validation_Framework.md** - State machine logic
- **OSL_Parsing_Framework.md** - Input handling

### 🔴 IMPLEMENTATION FOCUSED (Could Sunset)
These are primarily for CLI development:
- **OSL_Automation_Spec.md** - CLI implementation blueprint
- **OSL_Implementation_Summary.md** - Gap fixes completed
- **OSL_Reconciliation_Summary.md** - Alignment confirmation

---

## Implementation Reference Map

### When Building Core CLI Commands

#### `osl init` - System Initialization
**Primary References:**
1. OSL_Infrastructure_Spec.md - Directory structure
2. OSL_State_Schema.md - Initial state files
3. OSL_Governance_Standards.md - Default thresholds

```python
def init_command():
    # See: OSL_Infrastructure_Spec.md Section "Directory Structure"
    create_directories()
    
    # See: OSL_State_Schema.md Section "1. Coach State"
    initialize_coach_state()
    
    # See: OSL_Governance_Standards.md Section "Authoritative Thresholds"
    set_default_governance()
```

#### `osl session start/end` - Session Management
**Primary References:**
1. OSL_State_Schema.md - Session state structure
2. OSL_Governance_Standards.md - Gate checking
3. OSL_Validation_Framework.md - State transitions

```python
def session_start():
    # See: OSL_Governance_Standards.md Section "Gate Actions"
    check_governance_gates()
    
    # See: OSL_State_Schema.md Section "2. Current Session State"
    create_session_state()
    
    # See: OSL_Validation_Framework.md Section "State Transitions"
    validate_transition('NONE', 'SESSION_INIT')
```

#### `osl microloop` - Micro-Loop Tracking
**Primary References:**
1. OSL_AI_Boundaries.md - When AI can interact
2. OSL_State_Schema.md - Micro-loop data structure
3. OSL_Natural_Language_Balance.md - Input preservation

```python
def microloop_complete():
    # See: OSL_Natural_Language_Balance.md Section "Verbatim Preservation"
    preserve_recall_text()
    
    # See: OSL_AI_Boundaries.md Section "AFTER Free Recall"
    if state == 'RECALL_COMPLETE':
        allow_ai_questions()
    
    # See: OSL_State_Schema.md Section "micro_loops" structure
    update_session_metrics()
```

#### `osl flashcard` - Flashcard Creation
**Primary References:**
1. OSL_Flashcard_Philosophy.md - ALL decisions here
2. OSL_Governance_Standards.md - Card limits
3. OSL_State_Schema.md - Storage format

```python
def flashcard_create():
    # See: OSL_Flashcard_Philosophy.md - ENTIRE DOCUMENT
    # This is non-negotiable - learner must author
    ensure_learner_authored()
    
    # See: OSL_Governance_Standards.md Section "New Cards Per Session"
    check_card_limit()
    
    # See: OSL_State_Schema.md Section "flashcards_created"
    store_with_hash()
```

#### `osl quiz` - Quiz Generation
**Primary References:**
1. OSL_AI_Boundaries.md - When AI can generate
2. OSL_Activation_Probe.md - Pre-reading limits
3. OSL_Parsing_Framework.md - Answer preservation

```python
def quiz_generate():
    # See: OSL_Activation_Probe.md - If pre-reading
    if timing == 'before_reading':
        limit_to_activation_probe()  # 3 items, 90 seconds
    
    # See: OSL_AI_Boundaries.md Section "Weekly Calibration Quiz"
    if timing == 'weekly':
        allow_ai_generation()  # 6-10 items OK
```

#### `osl synthesis` - Weekly Synthesis
**Primary References:**
1. OSL_Concept_Map_Implementation.md - Map creation
2. OSL_State_Schema.md - Synthesis tracking
3. V3_Core.md - Synthesis requirements

```python
def synthesis_weekly():
    # See: OSL_Concept_Map_Implementation.md - ENTIRE DOCUMENT
    start_concept_map_timer(minutes=5)
    
    # Learner creates map - no AI generation
    # See: OSL_AI_Boundaries.md Section "Synthesis Essays"
```

#### `osl interleave` - Interleaving Sessions
**Primary References:**
1. OSL_Interleaving_Specification.md - ALL logic
2. OSL_Governance_Standards.md - Frequency settings
3. OSL_State_Schema.md - Tracking structure

```python
def interleave_detect():
    # See: OSL_Interleaving_Specification.md Section "Detection Algorithm"
    check_natural_interleaving()
    
    # See: OSL_Governance_Standards.md Section "Interleaving Frequency"
    check_weekly_target()
```

### When Implementing AI Interactions

#### Natural Language Processing
**Primary References:**
1. OSL_Natural_Language_Balance.md - ALL NLP decisions
2. OSL_AI_Boundaries.md - Timing restrictions
3. OSL_Parsing_Framework.md - Input preservation

```python
def process_user_input(text):
    # See: OSL_Natural_Language_Balance.md Section "Three-Layer Model"
    determine_layer(text)
    
    # See: OSL_Natural_Language_Balance.md Section "Confirmation Patterns"
    if requires_confirmation():
        show_interpretation()
    
    # See: OSL_Parsing_Framework.md Section "Verbatim Preservation"
    preserve_original(text)
```

#### AI Question Generation
**Primary References:**
1. OSL_AI_Boundaries.md - CRITICAL timing rules
2. OSL_Guardrails_Checklist.md - Quick validation

```python
def generate_questions():
    # See: OSL_AI_Boundaries.md Section "AFTER Free Recall"
    if state != 'RECALL_COMPLETE':
        raise ValueError("Cannot generate questions before recall")
    
    # Maximum 2-3 questions per micro-loop
    # Questions about material, not recall quality
```

### When Implementing Governance

#### Gate Checking
**Primary References:**
1. OSL_Governance_Standards.md - ALL thresholds
2. OSL_State_Schema.md - Metrics location

```python
def check_governance():
    # See: OSL_Governance_Standards.md - ENTIRE DOCUMENT
    # Every threshold, range, and action is here
    
    # See: OSL_State_Schema.md Section "governance_status"
    update_gate_status()
```

### When Handling State

#### State Management
**Primary References:**
1. OSL_State_Schema.md - AUTHORITATIVE structures
2. OSL_Validation_Framework.md - Transitions
3. OSL_Infrastructure_Spec.md - File locations

```python
def update_state():
    # See: OSL_State_Schema.md - Version 3.0 is authoritative
    validate_schema_version()
    
    # See: OSL_Validation_Framework.md Section "State Transitions"
    validate_transition()
    
    # See: OSL_Infrastructure_Spec.md Section "State File Specifications"
    write_to_correct_location()
```

---

## Quick Decision Trees

### "Should AI do this?"
→ Check **OSL_AI_Boundaries.md**

### "What's the governance threshold?"
→ Check **OSL_Governance_Standards.md**

### "How should flashcards work?"
→ Check **OSL_Flashcard_Philosophy.md** (entire document)

### "What's the data structure?"
→ Check **OSL_State_Schema.md**

### "How to handle user input?"
→ Check **OSL_Natural_Language_Balance.md**

### "Pre-reading quiz?"
→ Check **OSL_Activation_Probe.md** (minimal only!)

### "Concept map details?"
→ Check **OSL_Concept_Map_Implementation.md**

### "Interleaving logic?"
→ Check **OSL_Interleaving_Specification.md**

### "User experience?"
→ Check **OSL_User_Interaction_Guide.md**

---

## Document Permanence Recommendation

### Keep Permanent (Critical Guardrails)
These documents should remain permanent as they protect core learning principles:

1. **OSL_AI_Boundaries.md** - Prevents AI from destroying learning
2. **OSL_Flashcard_Philosophy.md** - Protects generation effect
3. **OSL_Governance_Standards.md** - Single source of truth for thresholds
4. **OSL_State_Schema.md** - Authoritative data structures
5. **OSL_Natural_Language_Balance.md** - Preserves learner control
6. **OSL_Activation_Probe.md** - Prevents quiz confusion

### Consider Merging Into Core
These could be absorbed into V3_Implementation_Guide.md:

1. **OSL_Concept_Map_Implementation.md** → Implementation Guide Section
2. **OSL_Interleaving_Specification.md** → Implementation Guide Section
3. **OSL_Infrastructure_Spec.md** → Implementation Guide Appendix

### Archive After Implementation
These served their purpose for reconciliation:

1. **OSL_Implementation_Summary.md** - Gap analysis complete
2. **OSL_Reconciliation_Summary.md** - Alignment achieved

---

## For the Implementing AI

**Start Here:**
1. Read this Master Reference Guide first
2. Read OSL_Automation_Spec.md for overall architecture
3. Then reference specific documents as you implement each component

**Critical Rule:**
When in doubt about ANY learning interaction, check:
- OSL_AI_Boundaries.md
- OSL_Flashcard_Philosophy.md
- OSL_Natural_Language_Balance.md

These three documents are your guardrails. Violating them breaks the learning system.

**Remember:**
The documents marked 🟢 PERMANENT SPECIFICATIONS are not suggestions - they are requirements that protect the integrity of the OSL learning system.