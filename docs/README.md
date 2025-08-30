# OSL (Optimized System for Learning) - Implementation Guide

## 🎯 Purpose
This README serves as the **primary entry point** for implementing the OSL system. It provides complete context for developers or AI assistants to understand and build the OSL workflow from scratch.

## 📚 What is OSL?
OSL is a research-backed, AI-assisted learning system that optimizes comprehension, retention, and transfer through:
- **Retrieval practice** - Active recall, not passive reading
- **Spaced repetition** - Review at increasing intervals
- **Interleaving** - Mix topics to strengthen discrimination
- **Self-explanation** - Rephrase in your own words
- **Immediate feedback** - Correct errors quickly
- **Calibration** - Test predictions against performance
- **Transfer** - Apply knowledge through projects
- **Curiosity-driven questioning** - Use learner-generated questions

## 🏗️ Implementation Roadmap

### Phase 1: Core CLI Tool (Start Here)
Build the foundational command-line interface that enforces the OSL workflow.

#### Essential Commands
```bash
osl init                    # Initialize OSL directory structure
osl session start           # Begin learning session with governance checks
osl session end             # Close session and update state
osl microloop complete      # Track micro-loop completion
osl flashcard create        # Validate and store learner-authored cards
osl quiz generate           # Generate calibration quiz (weekly only)
osl governance check        # Check all governance gates
osl state show              # Display current learning state
```

#### Implementation Steps
1. **Setup Project Structure**
   ```
   osl-cli/
   ├── src/
   │   ├── commands/       # CLI command implementations
   │   ├── state/          # State management
   │   ├── governance/     # Gate checking logic
   │   ├── ai/             # AI interaction boundaries
   │   └── validation/     # Input validation
   ├── tests/
   └── scripts/            # Helper scripts
   ```

2. **Core Dependencies**
   - Command-line parser (e.g., Click for Python, Commander for Node.js)
   - JSON schema validator
   - File system utilities
   - Optional: SQLite for state management

3. **Critical Implementation Documents** (Read in Order)
   - `OSL_Master_Reference_Guide.md` - Document navigation map
   - `OSL_Automation_Spec.md` - CLI architecture blueprint
   - `OSL_State_Schema.md` - Authoritative data structures
   - `OSL_Governance_Standards.md` - Thresholds and gates
   - `OSL_AI_Boundaries.md` - When/how AI can interact

### Phase 2: State Management System

#### Core State Files
```json
// coach_state.json - Persistent learning metrics
{
  "version": "3.0",
  "active_books": [],
  "performance_metrics": {},
  "governance_status": {},
  "review_schedule": {}
}

// current_session.json - Active session tracking
{
  "session_id": "uuid",
  "start_time": "ISO-8601",
  "micro_loops": [],
  "flashcards_created": []
}
```

#### Implementation Requirements
- **Atomic writes** - Prevent corruption during updates
- **Version migration** - Handle schema updates gracefully
- **Validation** - Enforce schema on every write
- **Backup** - Auto-backup before destructive operations

### Phase 3: Governance Engine

#### Gates to Implement
1. **Calibration Gate** (75-85%, default 80%)
   - Trigger: Weekly retrieval accuracy below threshold
   - Action: Pause new content, force remediation

2. **Card Debt Gate** (1.5×-2.5×, default 2.0×)
   - Trigger: Due cards exceed daily throughput multiplier
   - Action: Block new card creation

3. **Transfer Gate** (per book/topic)
   - Trigger: Completed book without transfer project
   - Action: Require project before new material

#### Key Files
- `OSL_Governance_Standards.md` - Authoritative thresholds
- `OSL_Validation_Framework.md` - State transition rules

### Phase 4: AI Integration Layer

#### AI Roles (Strictly Bounded)
1. **Extractor** - Cited bullet points only (no summaries)
2. **Tutor** - Questions AFTER free recall (2-3 per micro-loop)
3. **Coach** - Schedule management and gate enforcement

#### Critical Restrictions
- ❌ **NEVER** generate flashcards for learner
- ❌ **NEVER** generate permanent notes
- ❌ **NEVER** generate curiosity questions
- ✅ **ONLY** generate quiz items for weekly calibration
- ✅ **ONLY** ask questions AFTER learner's free recall

#### Key Files
- `OSL_AI_Boundaries.md` - Complete AI restrictions
- `OSL_Flashcard_Philosophy.md` - Why learner must author
- `OSL_Natural_Language_Balance.md` - User control preservation

### Phase 5: User Workflow Integration

#### Directory Structure (Created by `osl init`)
```
osl/
├── obsidian/               # Notes vault
│   ├── 10_books/           # Per-book workspaces
│   ├── 20_synthesis/       # Weekly essays
│   └── 30_projects/        # Transfer artifacts
├── anki/                   # Flashcard exports
├── ai_state/               # State management
│   ├── coach_state.json
│   ├── session_logs/
│   └── memory/
└── config/                 # User configuration
    └── osl_config.yaml
```

#### Daily Workflow
1. **Start Session** → Check governance gates
2. **Preview & Question** → Generate 5 curiosity questions
3. **Micro-loops** → Read → Recall → Explain → Feedback
4. **Create Flashcards** → Learner authors ≤8 cards
5. **End Session** → Update state, check gates

#### Weekly Workflow
1. **Calibration Quiz** → 6-10 items (AI-generated)
2. **Synthesis Essay** → 1-page integration
3. **Concept Map** → 5-minute visual (learner-created)
4. **Review Schedule** → Update based on performance

### Phase 6: Testing & Validation

#### Test Coverage Required
- [ ] State transitions (valid/invalid)
- [ ] Governance gate triggers
- [ ] AI timing restrictions
- [ ] Flashcard authorship validation
- [ ] Natural language interpretation layers
- [ ] Session continuity across restarts
- [ ] Data migration between versions

#### Key Validation Documents
- `OSL_Validation_Framework.md` - State machine rules
- `OSL_Parsing_Framework.md` - Input handling
- `OSL_Guardrails_Checklist.md` - Daily practice checklist

## 🚨 Critical Implementation Warnings

### Never Violate These Principles
1. **Generation Effect** - Learner MUST author all flashcards
2. **Testing Effect** - AI questions only AFTER free recall
3. **User Agency** - Never override explicit user input
4. **Governance Gates** - Never bypass when triggered

### Common Implementation Mistakes to Avoid
- ❌ Allowing AI to generate flashcards "for convenience"
- ❌ Running pre-reading quiz beyond 3-item probe
- ❌ Interpreting natural language without confirmation
- ❌ Ignoring governance gates "just this once"
- ❌ Creating features without Six-Gate Framework evaluation

## 📖 Document Hierarchy

### Core Methodology (Start Here for Context)
- `V3_Core.md` - The complete OSL methodology
- `V3_Implementation_Guide.md` - Practical templates and setup
- `V3_Decision_History.md` - Why decisions were made

### Authoritative Specifications (Reference During Implementation)
- `OSL_Master_Reference_Guide.md` - **START HERE** - Maps all documents
- `OSL_Automation_Spec.md` - CLI architecture blueprint
- `OSL_AI_Boundaries.md` - Critical AI restrictions
- `OSL_Governance_Standards.md` - Authoritative thresholds
- `OSL_State_Schema.md` - Version 3.0 data structures
- `OSL_Flashcard_Philosophy.md` - Generation effect protection
- `OSL_Natural_Language_Balance.md` - User control patterns

### Implementation Helpers
- `OSL_Guardrails_Checklist.md` - Quick validation checks
- `OSL_Activation_Probe.md` - Pre-reading probe limits
- `OSL_Concept_Map_Implementation.md` - 5-minute map specification
- `OSL_Interleaving_Specification.md` - Detection algorithm

## 🚀 Quick Start for Implementers

### If You're an AI Assistant
1. Read `OSL_Master_Reference_Guide.md` first
2. Read `OSL_Automation_Spec.md` for architecture
3. Read `OSL_AI_Boundaries.md` for your limits
4. Reference other docs as needed per Master Guide

### If You're a Developer
1. Read `V3_Core.md` to understand the methodology
2. Read `OSL_Automation_Spec.md` for technical architecture
3. Implement Phase 1 (Core CLI) first
4. Use `OSL_Master_Reference_Guide.md` to find specific answers

### First Implementation Task
```bash
# 1. Create project structure
mkdir osl-cli && cd osl-cli

# 2. Implement `osl init` command that creates:
osl/
├── obsidian/
├── anki/
├── ai_state/
│   └── coach_state.json (from OSL_State_Schema.md)
└── config/
    └── osl_config.yaml

# 3. Validate against OSL_Infrastructure_Spec.md
```

## 📊 Success Metrics

### Implementation Complete When
- [ ] All Phase 1 CLI commands functional
- [ ] State management follows Version 3.0 schema
- [ ] Governance gates trigger correctly
- [ ] AI boundaries enforced strictly
- [ ] User workflow documented and tested
- [ ] 90% test coverage achieved

### Quality Checks
- [ ] No AI generation of learner content
- [ ] Governance gates cannot be bypassed
- [ ] State persists across sessions
- [ ] Natural language requires confirmation
- [ ] Flashcard creation is learner-only

## 🔗 External Dependencies

### Required Tools (User-Installed)
- **Obsidian** - Note-taking application
- **Anki** - Spaced repetition software
- **Git** - Version control

### Optional Tools
- **Excalidraw** - Diagram creation
- **AI API** - For Tutor/Coach roles (OpenAI, Anthropic, etc.)

## 🤝 Contributing

### Before Adding Features
1. Review `V3_Decision_History.md` for past decisions
2. Apply Six-Gate Framework (see `V3_Implementation_Guide.md` Section N)
3. Document decision regardless of outcome
4. Update relevant specifications if approved

### Maintaining Consistency
- Single source of truth: `OSL_State_Schema.md` for data
- Single source of truth: `OSL_Governance_Standards.md` for thresholds
- Single source of truth: `OSL_AI_Boundaries.md` for AI limits
- When in doubt, check `OSL_Master_Reference_Guide.md`

## 📝 Version History

### Current Version: 3.4
- Reconciled all documentation inconsistencies
- Established authoritative specifications
- Created implementation blueprint
- Protected core learning principles

### Migration Notes
- Version 2.x states must be migrated to 3.0 schema
- See `OSL_State_Schema.md` for migration strategy

---

## 🎓 Remember: OSL's Purpose

OSL exists to maximize learning through evidence-based practices. Every implementation decision should ask:
1. Does this enhance learning or just add convenience?
2. Does this preserve learner agency and effort?
3. Does this have research backing?
4. Is the complexity worth the learning gain?

**When in doubt, favor learning over convenience.**

---

*This README is the authoritative entry point for OSL implementation. For specific details, follow the document hierarchy above. For navigation help, see `OSL_Master_Reference_Guide.md`.*