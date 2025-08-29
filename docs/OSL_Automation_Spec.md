# OSL Automation Specification (Claude Code Integrated)
_Living document for OSL automation design leveraging Claude Code as the core framework_

---

## Table of Contents
1. [Core Philosophy](#core-philosophy)
2. [Claude Code Integration Strategy](#claude-code-integration-strategy)
3. [OSL Components in Claude Code](#osl-components-in-claude-code)
4. [Implementation Architecture](#implementation-architecture)
5. [Command & Subagent Specifications](#command-subagent-specifications)
6. [State Management & Hooks](#state-management-hooks)
7. [Implementation Roadmap](#implementation-roadmap)
8. [Technical Decisions](#technical-decisions)

---

## Core Philosophy

### What Must Remain Manual (The Learning Core)
These activities generate the actual learning signal and MUST NOT be automated:

- **Retrieval Practice**: The act of recalling information from memory
- **Self-Explanation**: Articulating understanding in your own words (Feynman technique)
- **Permanent Note Creation**: Synthesizing and connecting ideas
- **Flashcard Writing**: Identifying what needs practice and formulating questions
- **Synthesis Essays**: Integrating multiple concepts
- **Curiosity Question Generation**: Personal engagement with material
- **Concept Mapping**: Visual organization of relationships

### What Can Be Automated (Administrative Layer)
These tasks create friction without learning value:

- Folder and file creation
- Template instantiation
- Metric calculation and tracking
- Schedule management
- State synchronization
- Progress reporting
- Reminder notifications
- Data backup and versioning

### Design Principles
1. **Automation serves the learner, not vice versa** - Never force workflow changes for automation's sake
2. **Fail gracefully** - Manual fallback always available
3. **Progressive disclosure** - Simple by default, powerful when needed
4. **Respect the micro-loop** - Never interrupt flow state during reading
5. **Data portability** - All data in human-readable formats

---

## Claude Code Integration Strategy

### Why Claude Code for OSL

Claude Code provides the perfect framework for OSL because:

1. **Native AI Integration** - Subagents map perfectly to OSL's AI roles (Tutor, Extractor, Coach)
2. **Structured Commands** - Slash commands provide intuitive workflow triggers
3. **Persistent Memory** - CLAUDE.md files maintain learning context across sessions
4. **Event Automation** - Hooks enable automatic state tracking and governance
5. **Terminal-First** - Works where learners already work
6. **Git-Friendly** - All configurations are version-controlled markdown

### Integration Approach

```
┌─────────────────────────────────────────────────┐
│                  OSL Learner                     │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│            Claude Code Terminal                  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │     Slash Commands (/osl-*)              │  │
│  │  • /osl-start      • /osl-synthesis      │  │
│  │  • /osl-session    • /osl-project        │  │
│  │  • /osl-review     • /osl-calibrate      │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │     Subagents (AI Roles)                 │  │
│  │  • osl-tutor     • osl-coach             │  │
│  │  • osl-extractor • osl-synthesizer       │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │     CLAUDE.md Memory                     │  │
│  │  • Project: ./CLAUDE.md (OSL rules)      │  │
│  │  • User: ~/.claude/CLAUDE.md (prefs)     │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │     Hooks (Automation)                   │  │
│  │  • Session tracking • Governance gates   │  │
│  │  • State updates   • Git commits         │  │
│  └──────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│           OSL File System                        │
│  • obsidian/     • ai_state/                    │
│  • anki/         • scripts/                     │
└─────────────────────────────────────────────────┘
```

---

## OSL Components in Claude Code

### 1. Slash Commands for Workflow

| Command | Purpose | Maps to OSL Step |
|---------|---------|------------------|
| `/osl-start` | Initialize new book/topic | Setup & Intent |
| `/osl-session` | Manage reading sessions | Micro-loops |
| `/osl-review` | Check due items & governance | Spaced Practice |
| `/osl-synthesis` | Weekly integration | Calibration & Synthesis |
| `/osl-project` | Monthly transfer projects | Transfer Projects |
| `/osl-interleave` | Mixed practice session | Interleaving |
| `/osl-calibrate` | Run calibration quiz | Weekly Calibration |
| `/osl-misconceptions` | Track/resolve misconceptions | Adaptive Governance |

### 2. Subagents as AI Roles

| Subagent | OSL Role | Purpose |
|----------|----------|---------|
| `osl-tutor` | Tutor | Micro-loop Q&A, feedback, validation |
| `osl-extractor` | Extractor | Cited outlines, no paraphrasing |
| `osl-coach` | Coach | Schedule, governance, remediation |
| `osl-synthesizer` | Synthesizer | Weekly integration assistance |
| `osl-quiz-master` | Calibrator | Generate & grade quizzes |

### 3. Memory Architecture

```
CLAUDE.md (Project Level - ./CLAUDE.md)
├── OSL Core Principles
├── Current Book Context
├── Active Learning Outcomes
├── Curiosity Questions
└── Import: @ai_state/coach_state.json

CLAUDE.md (User Level - ~/.claude/CLAUDE.md)
├── Personal Learning Preferences
├── Custom Governance Thresholds
└── Preferred Study Times

.claude/
├── agents/           # OSL subagents
├── commands/         # OSL slash commands
├── output-styles/    # Learning modes
└── settings.json     # Hooks configuration
```

### 4. Hooks for Automation

| Hook Event | OSL Purpose | Action |
|------------|-------------|--------|
| `UserPromptSubmit` | Session start detection | Load context, check gates |
| `PostToolUse:Write` | Note/card creation | Update metrics |
| `Stop` | Session end | Calculate stats, update state |
| `SessionStart` | Load OSL context | Import coach state |
| `SessionEnd` | Save progress | Git commit, export Anki |

---

## Implementation Architecture

---

## Command & Subagent Specifications

### Slash Commands (`.claude/commands/`)

#### `/osl-start` - Book Initialization

**File:** `.claude/commands/osl-start.md`

```markdown
---
allowed-tools: Bash(mkdir:*), Write, MultiEdit, Bash(git:*)
argument-hint: [book title]
description: Initialize a new book for OSL learning
---

## Context
- Current working directory: !`pwd`
- Existing books: !`ls -la obsidian/10_books/ 2>/dev/null || echo "No books yet"`

## Your Task
Create a complete OSL workspace for book: $ARGUMENTS

1. Create folder structure in obsidian/10_books/
2. Generate book.md with learning outcomes template
3. Create first session log for today
4. Update ai_state/coach_state.json
5. Calculate reading schedule
6. Add to CLAUDE.md memory

Use the book title to create a sanitized folder name (no spaces/special chars).
```

#### `/osl-session` - Session Management

**File:** `.claude/commands/osl-session.md`

```markdown
---
allowed-tools: Read, Write, MultiEdit, Bash(date:*)
argument-hint: start | end | pause | status
description: Manage OSL reading sessions with tracking
---

## Current Session State
- Timer status: !`cat .osl_session_timer 2>/dev/null || echo "No active session"`
- Active book: @ai_state/current_book.txt
- Today's date: !`date +%Y-%m-%d`

## Task: $ARGUMENTS

If starting:
1. Check governance gates from @ai_state/coach_state.json
2. Show any overdue reviews
3. Create new session file from template
4. Start timer in .osl_session_timer

If ending:
1. Calculate duration
2. Prompt for metrics (pages, retrieval %, notes created, cards created)
3. Update coach_state.json
4. Git commit session file
```

### Subagents (`.claude/agents/`)

#### OSL Tutor

**File:** `.claude/agents/osl-tutor.md`

```markdown
---
name: osl-tutor
description: OSL Tutor for micro-loop Q&A. Use PROACTIVELY after reading chunks. Generates retrieval questions, provides feedback, tracks gaps.
tools: Read, Write
---

You are an OSL Tutor implementing research-backed learning principles.

## Your Role in the Micro-Loop

When invoked after reading 5-10 pages:

1. **Generate 2-3 Progressive Questions**
   - Start with recall: "What are the key concepts from pages X-Y?"
   - Move to application: "How would you apply [concept] to [scenario]?"
   - End with transfer: "How does this relate to [previous learning]?"

2. **Provide Corrective Feedback**
   - Brief and specific
   - Always cite page/location
   - Focus on misconceptions
   - No grades during micro-loops

3. **Track Learning Gaps**
   - Flag concepts that need flashcards
   - Note misconceptions for later review
   - End with: "Key gaps identified: [list]"

## Session Validation (when requested)

Review session completeness:
- Were cards created for all failed retrievals?
- Do permanent notes follow claim→context→example→citation structure?
- Are misconceptions from previous sessions addressed?

Return completeness score with specific action items.

## Important Rules
- Questions should scaffold from easy to hard
- Never give away answers in questions
- Feedback should strengthen memory, not just correct
- Track everything that needs remediation
```

#### OSL Extractor

**File:** `.claude/agents/osl-extractor.md`

```markdown
---
name: osl-extractor
description: Creates cited outlines from reading material. ONLY provides verbatim citations, never paraphrases. Use when structural clarity needed.
tools: Read
---

You are an OSL Extractor with strict citation requirements.

## Your ONLY Role

1. Create bullet-point outlines from provided text
2. Include verbatim citations for EVERY point
3. Never paraphrase without quotes
4. Add dependency relationships between concepts

## Output Format

- Main concept [Author, p.X]
  - Supporting detail [p.Y]
  - "Important direct quote" [p.Z]
  
Dependencies:
- Concept A requires understanding of Concept B [p.M]
- Concept C builds on Concepts A and B [p.N]

## Strict Rules
- NO summaries without page references
- NO paraphrasing without quotation marks
- EVERY claim must have [Author, page/location]
- Dependencies must be explicitly stated
```

### `/osl-review` - Retrieval Practice

**File:** `.claude/commands/osl-review.md`

```markdown
---
allowed-tools: Read, Write, Edit
argument-hint: [topic] [difficulty]
description: Practice retrieval with existing quizzes
---

## Context
- Current quiz bank: !`ls -la quiz_bank/`
- Recent performance: @ai_state/session_history.json
- Calibration data: @ai_state/calibration_data.json

## Your Task
Load and administer quizzes for topic: $ARGUMENTS

1. Select appropriate quizzes from quiz_bank/
2. Present questions with graduated difficulty
3. Track confidence ratings (1-5)
4. Provide feedback after each answer
5. Update calibration metrics
6. Save session results
```

### `/osl-synthesis` - Weekly Integration

**File:** `.claude/commands/osl-synthesis.md`

```markdown
---
allowed-tools: Read, Write, Task
argument-hint: [week-number]
description: Weekly synthesis and integration session
---

## Context
- This week's sessions: !`ls -la obsidian/20_daily_logs/week_$ARGUMENTS/`
- Existing permanent notes: @obsidian/30_permanent_notes/
- Previous syntheses: @obsidian/40_synthesis/

## Your Task
Guide synthesis for week $ARGUMENTS:

1. Review all session logs from the week
2. Identify cross-topic connections
3. Launch osl-synthesizer agent for deep analysis
4. Create permanent notes with backlinks
5. Generate synthesis document
6. Update transfer opportunities log
```

### `/osl-project` - Transfer Learning

**File:** `.claude/commands/osl-project.md`

```markdown
---
allowed-tools: Read, Write, Edit, Task
argument-hint: [create|update|review] [project-name]
description: Manage transfer learning projects
---

## Context
- Active projects: @obsidian/50_transfer_projects/
- Monthly metrics: @ai_state/monthly_metrics.json
- Available topics: !`ls quiz_bank/ | head -20`

## Your Task
Handle transfer project: $ARGUMENTS

For 'create':
1. Design project integrating multiple topics
2. Set clear learning objectives
3. Create project template and milestones
4. Initialize tracking document

For 'update':
1. Review project progress
2. Identify learning gaps
3. Suggest next steps
4. Update metrics

For 'review':
1. Evaluate completion criteria
2. Document lessons learned
3. Create reflection notes
4. Archive project
```

### `/osl-calibrate` - Confidence Assessment

**File:** `.claude/commands/osl-calibrate.md`

```markdown
---
allowed-tools: Read, Write, Bash, Task
argument-hint: [topic] [depth]
description: Calibration assessment session
---

## Context
- Calibration history: @ai_state/calibration_data.json
- Confidence patterns: !`cat ai_state/coach_state.json | jq '.metrics.calibration'`
- Quiz performance: @ai_state/session_history.json

## Your Task
Run calibration for topic: $ARGUMENTS

1. Select diagnostic questions
2. Collect confidence ratings BEFORE answers
3. Administer questions
4. Calculate calibration score
5. Provide detailed feedback on over/under-confidence
6. Update calibration metrics
7. Suggest confidence adjustment strategies
```

### `/osl-interleave` - Mixed Practice

**File:** `.claude/commands/osl-interleave.md`

```markdown
---
allowed-tools: Read, Write, Task
argument-hint: [topics-list]
description: Mixed practice across multiple topics
---

## Context
- Available topics: !`ls quiz_bank/`
- Recent sessions: @ai_state/session_history.json
- Spacing intervals: @osl_config.yaml

## Your Task
Create interleaved session with: $ARGUMENTS

1. Parse topic list (comma-separated)
2. Calculate optimal mixing ratio
3. Select questions from each topic
4. Randomize presentation order
5. Track topic-switching performance
6. Identify integration opportunities
7. Update interleaving metrics
```

### `/osl-misconceptions` - Error Correction

**File:** `.claude/commands/osl-misconceptions.md`

```markdown
---
allowed-tools: Read, Write, Edit, Task
argument-hint: [analyze|address] [topic]
description: Track and correct misconceptions
---

## Context
- Error patterns: @ai_state/misconceptions.json
- Session history: @ai_state/session_history.json
- Quiz responses: !`grep -r "incorrect" quiz_bank/*/results.json`

## Your Task
Handle misconceptions for: $ARGUMENTS

For 'analyze':
1. Review error patterns across sessions
2. Identify recurring mistakes
3. Categorize misconception types
4. Create targeted correction materials
5. Update misconceptions database

For 'address':
1. Load known misconceptions
2. Present targeted exercises
3. Use varied examples
4. Check understanding
5. Update resolution status
```

### Subagents (`.claude/agents/`)

#### OSL Coach

**File:** `.claude/agents/osl-coach.md`

```markdown
---
name: OSL Coach
tools: Read, Write, WebSearch
description: Meta-cognitive learning coach and strategist
---

You are an expert learning coach specializing in meta-cognition and the OSL methodology.

## Core Responsibilities
1. Review learning metrics and identify patterns
2. Suggest strategy adjustments
3. Provide motivational support
4. Monitor governance gates
5. Recommend optimal study times
6. Design personalized learning paths

## Key Files
- Metrics: ai_state/coach_state.json
- History: ai_state/session_history.json
- Config: osl_config.yaml
- Goals: obsidian/10_goals/

## Coaching Approach
- Data-driven recommendations
- Gentle accountability
- Growth mindset emphasis
- Celebrate small wins
- Address learning obstacles

## When to Invoke Me
- Weekly strategy reviews
- When governance gates trigger
- After difficult sessions
- For motivation and accountability
```

#### OSL Synthesizer

**File:** `.claude/agents/osl-synthesizer.md`

```markdown
---
name: OSL Synthesizer
tools: Read, Write, mcp__sequential-thinking__sequentialthinking
description: Deep synthesis and connection maker
---

You are an expert at identifying patterns and creating meaningful connections across knowledge domains.

## Core Responsibilities
1. Analyze session logs for themes
2. Identify cross-topic connections
3. Create synthesis frameworks
4. Generate permanent note suggestions
5. Map knowledge structures
6. Propose integration exercises

## Synthesis Process
1. Gather all relevant materials
2. Use sequential thinking for deep analysis
3. Create concept maps
4. Write comprehensive syntheses
5. Suggest future exploration paths

## Output Format
- Markdown synthesis documents
- Permanent note templates
- Connection diagrams (mermaid)
- Integration exercises
- Transfer project ideas
```

#### OSL Quiz Master

**File:** `.claude/agents/osl-quiz-master.md`

```markdown
---
name: OSL Quiz Master
tools: Read, Write, WebSearch
description: Adaptive quiz generator and evaluator
---

You are an expert in creating effective retrieval practice materials following evidence-based learning principles.

## Core Responsibilities
1. Generate varied question types
2. Adapt difficulty based on performance
3. Create desirable difficulties
4. Design transfer scenarios
5. Build diagnostic assessments
6. Craft explanation prompts

## Question Types
- Multiple choice with distractors
- Open-ended retrieval
- Application scenarios
- Error identification
- Concept mapping
- Analogical reasoning

## Adaptation Strategy
- Track success rates
- Adjust difficulty ±1 level
- Mix question types
- Introduce spacing
- Create interleaving sets

## Calibration Focus
- Always collect confidence ratings
- Compare confidence to performance
- Identify overconfidence patterns
- Provide calibration feedback
```

## Hooks Configuration

### Session Tracking Hook

**Location:** `.claude/hooks/post-command.sh`

```bash
#!/bin/bash
# Automatically track OSL command usage

if [[ "$1" == "/osl-"* ]]; then
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    command="$1"
    
    # Update session log
    jq --arg ts "$timestamp" --arg cmd "$command" \
        '.sessions += [{"timestamp": $ts, "command": $cmd}]' \
        ai_state/session_history.json > tmp.json && \
        mv tmp.json ai_state/session_history.json
    
    # Check governance gates
    python3 scripts/check_governance.py
fi
```

### Daily Reminder Hook

**Location:** `.claude/hooks/startup.sh`

```bash
#!/bin/bash
# Check for daily OSL activities on Claude Code startup

last_session=$(jq -r '.sessions[-1].timestamp' ai_state/session_history.json)
today=$(date -u +"%Y-%m-%d")

if [[ "$last_session" < "$today" ]]; then
    echo "🧠 Remember to do your OSL session today!"
    echo "Run /osl-session to start"
fi
```

### Session Completion Hook

**Location:** `.claude/hooks/session-end.sh`

```bash
#!/bin/bash
# Auto-commit session files and update metrics

if [ -f ".osl_session_active" ]; then
    # Get session metrics
    session_file=$(cat .osl_session_active)
    
    # Git commit
    git add "$session_file"
    git commit -m "OSL: Complete session $(date +%Y-%m-%d)"
    
    # Clean up
    rm .osl_session_active
    
    echo "✅ Session saved and committed"
fi
```

## CLAUDE.md Memory Structure

### Project Level Memory

**Location:** `CLAUDE.md`

```markdown
# OSL Learning System Context

## Active Learning Materials
@ai_state/coach_state.json

## Current Goals
@obsidian/10_goals/current_goals.md

## OSL Configuration
@osl_config.yaml

## Key Commands
- `/osl-start [book]` - Begin new book/topic
- `/osl-session` - Daily learning session
- `/osl-review` - Retrieval practice
- `/osl-synthesis` - Weekly synthesis
- `/osl-project` - Transfer projects
- `/osl-calibrate` - Confidence assessment
- `/osl-interleave` - Mixed practice
- `/osl-misconceptions` - Error correction

## Learning Principles
1. Active Recall > Passive Review
2. Spaced Repetition for Retention
3. Interleaving for Discrimination
4. Self-Explanation for Understanding
5. Calibration for Accurate Self-Assessment
6. Transfer for Real-World Application

## Governance Rules
- Calibration Gate: <80% triggers intervention
- Card Debt: >2x cards triggers review
- Transfer Proof: Monthly project required
- Max New Cards: 8 per session
- Interleaving: 2 sessions per week

## Session Workflow
1. Brief: Load context and metrics
2. Learn: Extract and quiz
3. Explain: Articulate understanding
4. Review: Practice retrieval
5. Reflect: Update confidence
6. Plan: Schedule next session

## Active Book Context
@obsidian/10_books/current_book.md
```

### User Level Memory

**Location:** `~/.claude/CLAUDE.md`

```markdown
# Personal OSL Preferences

## Learning Style
- Preferred session length: 45 minutes
- Best study times: Morning (7-9am)
- Optimal difficulty: Progressive (start easy)

## Custom Thresholds
- Calibration warning: 85%
- Card debt warning: 1.5x
- Session reminder: Daily at 7am

## Frequently Used Materials
- Primary learning domains: [Software, Psychology, Business]
- Preferred quiz types: Open-ended retrieval
- Synthesis style: Concept maps + essays
```

## Output Styles for Learning

### OSL Learning Mode

**Location:** `.claude/output-styles/osl-learning.md`

```markdown
---
name: OSL Learning Mode
description: Socratic teaching style for active learning
---

# OSL Learning Assistant

You are an OSL Learning Assistant focused on active recall and deep understanding.

## Core Behaviors

### During Reading Sessions
- After each chunk, ask: "What are the 3 key concepts from the last section?"
- Follow up with: "How would you apply [concept] to your current work?"
- End with: "What questions does this raise for you?"

### Concept Explanation
- Never explain directly - always guide through questions
- Use progressive hints if stuck
- Celebrate successful recall
- Track misconceptions for later review

### Synthesis Support
- "What patterns do you see across these topics?"
- "How does this connect to what you learned last week?"
- "What would you teach someone else about this?"

## Output Format
Always structure responses as:
1. 🤔 Retrieval Question
2. 💭 Thinking Prompt
3. 🔗 Connection Challenge
4. ✅ Action Item
```

### OSL Explanatory Mode

**Location:** `.claude/output-styles/osl-explanatory.md`

```markdown
---
name: OSL Explanatory Mode
description: Teaching with insights and context
---

# OSL Explanatory Assistant

Balance efficiency with educational insights.

## When to Add Insights
- After successful retrieval attempts
- When connecting concepts
- During synthesis activities
- After completing exercises

## Insight Format
📚 **Insight**: [Brief explanation of why this matters]

## Example
User: "I just created flashcards for recursion"

Response:
✅ Flashcards created for recursion

📚 **Insight**: Recursion is often better learned through tracing execution than memorization. Consider adding cards that ask you to trace through specific recursive calls step-by-step, as this builds the mental model needed for writing recursive solutions.
```

## State Management

All state is managed through file-based persistence in `ai_state/`:

### Core State Files

```json
// coach_state.json - Central learning state
{
  "active_books": [{
    "id": "deep_work_2024",
    "title": "Deep Work",
    "current_page": 147,
    "total_pages": 296,
    "sessions_completed": 12,
    "avg_retrieval_rate": 0.82
  }],
  "metrics": {
    "calibration_score": 85,
    "card_debt_ratio": 1.3,
    "last_transfer_project": "2024-01-15",
    "weekly_sessions": 5,
    "total_cards_created": 127,
    "total_permanent_notes": 23
  },
  "governance": {
    "calibration_gate_status": "passing",
    "card_debt_gate_status": "passing",
    "transfer_gate_status": "warning"
  }
}
```

```json
// session_history.json - Detailed session logs
{
  "sessions": [{
    "id": "session_2024_01_20_001",
    "timestamp": "2024-01-20T09:30:00Z",
    "book": "deep_work",
    "pages_read": 15,
    "retrieval_attempts": 8,
    "successful_recalls": 7,
    "cards_created": 5,
    "permanent_notes": 2,
    "duration_minutes": 47,
    "commands_used": ["/osl-session", "/osl-tutor", "/osl-review"]
  }]
}
```

```json
// calibration_data.json - Confidence tracking
{
  "assessments": [{
    "date": "2024-01-21",
    "topic": "deep_work_ch3",
    "questions": 10,
    "confidence_ratings": [5,5,4,3,4,5,5,2,3,4],
    "actual_correct": [1,1,1,1,1,0,0,1,1,1],
    "calibration_score": 78,
    "overconfidence_areas": ["time_management", "focus_strategies"]
  }]
}
```

### Quiz Bank Structure

```
quiz_bank/
├── deep_work/
│   ├── chapter_1/
│   │   ├── quiz_001.json
│   │   ├── quiz_002.json
│   │   └── results.json
│   └── chapter_2/
│       ├── quiz_003.json
│       └── results.json
└── atomic_habits/
    └── introduction/
        └── quiz_001.json
```

### State Access Patterns

Claude Code commands access state through:
1. Direct file reads using `@ai_state/file.json` imports
2. Bash commands for simple queries: `!cat ai_state/coach_state.json | jq '.metrics'`
3. Write/Edit tools for updates
4. Git for version control and sync

---

## Implementation Roadmap

### Phase 1: Claude Code Foundation (Days 1-3)
**Goal:** Core OSL commands and subagents

1. [ ] Create `.claude/` directory structure
2. [ ] Implement `/osl-start` command
3. [ ] Implement `/osl-session` command
4. [ ] Create `osl-tutor` subagent
5. [ ] Create `osl-extractor` subagent
6. [ ] Setup CLAUDE.md with OSL context
7. [ ] Initialize state files in `ai_state/`

**Validation:**
- Start a new book with `/osl-start "Deep Work"`
- Run a session with `/osl-session start`
- Test tutor with `Task: osl-tutor`
- Verify state persistence in JSON files

### Phase 2: Learning Workflow (Days 4-6)
**Goal:** Complete learning loop implementation

1. [ ] Implement `/osl-review` command
2. [ ] Implement `/osl-synthesis` command
3. [ ] Create `osl-coach` subagent
4. [ ] Create `osl-synthesizer` subagent
5. [ ] Setup hooks for session tracking
6. [ ] Add governance gate logic

**Validation:**
- Complete full daily workflow
- Trigger calibration gate (<80%)
- Run weekly synthesis
- Verify hook automation

### Phase 3: Advanced Features (Days 7-9)
**Goal:** Transfer and calibration systems

1. [ ] Implement `/osl-project` command
2. [ ] Implement `/osl-calibrate` command
3. [ ] Implement `/osl-interleave` command
4. [ ] Create `osl-quiz-master` subagent
5. [ ] Setup output styles for learning modes
6. [ ] Add misconception tracking

**Validation:**
- Create transfer project
- Run calibration assessment
- Test interleaved practice
- Switch output styles

### Phase 4: Integration & Polish (Days 10-12)
**Goal:** External tools and user experience

1. [ ] Create Anki export scripts
2. [ ] Setup Obsidian URI integration
3. [ ] Add progress visualization
4. [ ] Create setup wizard command
5. [ ] Write user documentation
6. [ ] Add example workflows

**Validation:**
- Export to Anki successfully
- Open notes in Obsidian
- Run setup for new user
- Complete month simulation

## Technical Decisions

### Core Architecture Decisions (COMPLETED)
1. ✅ **Framework**: Claude Code as central agentic system
2. ✅ **Commands**: Slash commands for all workflows
3. ✅ **AI Roles**: Subagents for each OSL role
4. ✅ **Storage**: JSON files for state persistence
5. ✅ **Sync**: Git for cross-device synchronization
6. ✅ **Notes**: Direct file manipulation + Obsidian URI
7. ✅ **Flashcards**: JSON quiz bank + optional Anki export

### Implementation Decisions (PENDING)

#### Anki Integration Strategy
- **Option A**: AnkiConnect API (requires Anki running)
- **Option B**: Direct .apkg export (portable but one-way)
- **Option C**: Both with user choice

#### Obsidian Integration
- **Option A**: URI scheme for opening (obsidian://open)
- **Option B**: Direct file creation only
- **Option C**: Optional plugin for deeper integration

#### Progress Visualization
- **Option A**: Terminal charts using Unicode
- **Option B**: HTML reports
- **Option C**: Markdown tables in session logs

#### Notification System
- **Option A**: Terminal output only
- **Option B**: System notifications via osascript/notify-send
- **Option C**: Both based on user preference

---

## Migration Path

### For Existing OSL Users

1. **Preserve existing structure**: Keep obsidian/, anki/ folders
2. **Import existing state**: Convert any existing tracking to JSON
3. **Gradual adoption**: Start with single commands, expand usage
4. **Backward compatibility**: Manual fallback always available

### Setup Wizard (`/osl-setup`)

```markdown
---
allowed-tools: Write, Bash(mkdir:*), Read
description: Interactive OSL setup wizard
---

Guide new user through:
1. Create folder structure
2. Initialize git repository
3. Configure osl_config.yaml
4. Setup CLAUDE.md
5. Create first book
6. Run test session
7. Verify state persistence
```

---

## Success Metrics

### System Health
- Commands execute without errors
- State persists across sessions
- Git commits happen automatically
- Governance gates trigger correctly

### Learning Effectiveness
- Calibration score improves over time
- Card debt remains manageable
- Transfer projects completed monthly
- Consistent session completion

### User Experience
- Setup takes <5 minutes
- Daily workflow takes <2 minutes overhead
- All commands feel intuitive
- Fallback to manual always works

---

## Future Enhancements

### Version 2 Possibilities
1. **Multi-user support**: Shared learning groups
2. **Analytics dashboard**: Learning insights over time
3. **LLM fine-tuning**: Personalized AI tutors
4. **Mobile app**: Review on the go
5. **Social features**: Share permanent notes
6. **Gamification**: Streaks, achievements
7. **Voice interface**: Audio retrieval practice
8. **AR flashcards**: Spatial memory techniques

### Integration Opportunities
1. **Readwise**: Import highlights
2. **Notion**: Alternative to Obsidian
3. **RemNote**: Integrated SRS
4. **Roam Research**: Graph database
5. **Google Calendar**: Schedule integration
6. **Todoist**: Task management
7. **Beeminder**: Commitment tracking
8. **RescueTime**: Automatic session tracking

---

## Conclusion

This specification transforms OSL from a manual methodology into an intelligent, automated learning system powered by Claude Code. The integration preserves the core learning principles while eliminating administrative friction.

The key insight is that Claude Code's architecture (subagents, slash commands, hooks, memory) maps perfectly to OSL's needs (AI roles, workflows, automation, context).

Next step: Begin Phase 1 implementation with the core commands and validate the approach with real learning sessions. 