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

### Slash Commands (`.claude/commands/`) - Thin CLI Wrappers

#### `/osl-start` - Book Initialization

**File:** `.claude/commands/osl-start.md`

```markdown
---
allowed-tools: Bash(osl:*)
argument-hint: [book title]
description: Initialize a new book (wraps: osl book start)
---

## Your Task
Parse user input: $ARGUMENTS

Extract book title from natural language:
- "Deep Work" → book="Deep Work"
- "starting Deep Work by Cal Newport" → book="Deep Work", author="Cal Newport"
- "I want to read Atomic Habits" → book="Atomic Habits"

If book title missing:
Ask user: "What's the title of the book you want to start?"

Execute:
```bash
osl book start --book "$BOOK" --author "$AUTHOR"
```

If error occurs:
- Read the JSON error response
- Extract the "suggestion" field
- Try the suggested command
- If still fails, show error to user

Display success response directly to user.
```

#### `/osl-session` - Session Management

**File:** `.claude/commands/osl-session.md`

```markdown
---
allowed-tools: Bash(osl:*)
argument-hint: start | end | status
description: Manage reading sessions (wraps: osl session)
---

## Your Task
Parse intent: $ARGUMENTS

Map natural language:
- "start", "begin", "let's go" → start
- "end", "done", "finished" → end
- "status", "where am I" → status

### For START:
```bash
osl session start
```

### For END:
First ask user for metrics:
- Pages read?
- Retrieval attempts?
- Successful recalls?
- Cards created (max 8)?

Then:
```bash
osl session end --pages $P --retrieval $R --recalls $S --cards $C
```

### For STATUS:
```bash
osl session status
```

Handle errors by reading JSON and retrying with suggestions.
```

### Subagents (`.claude/agents/`)

#### OSL Tutor

**File:** `.claude/agents/osl-tutor.md`

```markdown
---
name: osl-tutor
description: OSL Tutor for micro-loop Q&A. Use PROACTIVELY after reading chunks. Generates retrieval questions AFTER learner's free recall, provides feedback, tracks gaps.
tools: Read, Write
---

You are an OSL Tutor implementing research-backed learning principles.

## Your Role in the Micro-Loop (AFTER learner's retrieval)

When invoked AFTER learner completes free recall and Feynman explanation:

1. **Generate 2-3 Progressive Questions** (Testing Effect)
   - Based on what learner just read and attempted to recall
   - Start with recall: "What are the key concepts from pages X-Y?"
   - Move to application: "How would you apply [concept] to [scenario]?"
   - End with transfer: "How does this relate to [previous learning]?"
   - Questions target material, NOT learner's recall quality

2. **Provide Corrective Feedback**
   - Brief and specific
   - Always cite page/location
   - Focus on misconceptions
   - No grades during micro-loops
   - Immediate feedback enhances the testing effect

3. **Track Learning Gaps**
   - Note what learner self-identifies as difficult
   - Track misconceptions for later review
   - End with: "Key gaps you identified: [list]"
   - DO NOT suggest flashcards - learner decides

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

## Hooks Configuration (CLI Tool Integration)

### Principle: Hooks Call CLI, Never Duplicate Logic

All hooks delegate to the OSL CLI tool to ensure single source of truth.

### Session Tracking Hook

**Location:** `.claude/hooks/track-osl.sh`

```bash
#!/bin/bash
# Track all OSL-related commands using CLI tool

if [[ "$1" == "/osl-"* ]]; then
    # Let CLI tool handle tracking
    osl metrics track --event "command" --data "$1" --timestamp "$(date -Iseconds)"
fi
```

### Startup Hook

**Location:** `.claude/hooks/osl-startup.sh`

```bash
#!/bin/bash
# Check OSL status on Claude Code startup

# Get due items from CLI
due_items=$(osl review due --format json)
count=$(echo "$due_items" | jq '.count')

if [ "$count" -gt 0 ]; then
    echo "🧠 OSL Reminder: You have $count items due today"
    echo "Run: /osl-review to see details"
fi

# Check governance status
governance=$(osl state query --key governance --format json)
if echo "$governance" | jq -e '.calibration_gate == "failing"' > /dev/null; then
    echo "⚠️ Calibration below 80% - review mode recommended"
fi
```

### Post-Session Hook

**Location:** `.claude/hooks/post-session.sh`

```bash
#!/bin/bash
# Auto-commit after session commands

if [[ "$1" == "/osl-session end" ]]; then
    # CLI already handled state updates, just commit
    osl git commit --message "Session completed"
fi
```

### Error Recovery Hook

**Location:** `.claude/hooks/error-handler.sh`

```bash
#!/bin/bash
# Handle OSL CLI errors gracefully

if [ "$2" -ne 0 ] && [[ "$1" == "osl "* ]]; then
    # Parse error JSON from CLI
    error_json=$(echo "$3" | jq -r '.suggestion // empty')
    
    if [ -n "$error_json" ]; then
        echo "💡 Suggestion: $error_json"
        echo "Would you like me to try that instead? (y/n)"
    fi
fi
```

### Configuration File

**Location:** `.claude/settings.json`

```json
{
  "outputStyle": "OSL Default",
  "hooks": {
    "enabled": true,
    "postCommand": ".claude/hooks/track-osl.sh",
    "sessionStart": ".claude/hooks/osl-startup.sh",
    "sessionEnd": ".claude/hooks/post-session.sh",
    "errorHandler": ".claude/hooks/error-handler.sh"
  },
  "tools": {
    "whitelist": ["Bash(osl:*)", "Read", "Write"],
    "requireConfirmation": false
  },
  "osl": {
    "cliPath": "/usr/local/bin/osl",
    "autoInvokeTutor": true,
    "reminderTime": "09:00",
    "defaultBook": null
  }
}
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

### OSL Default Style (Primary)

**Location:** `.claude/output-styles/osl-default.md`

```markdown
---
name: OSL Default
description: Guides users to correct OSL tools and enforces proper usage
---

# OSL Learning Assistant

You are the OSL interface that guides users through proper tool usage.

## Core Behaviors

### Tool Routing
When users express learning intent, guide them to the right tool:
- "I want to start reading" → Suggest: `/osl-session start`
- "What should I review?" → Suggest: `/osl-review`
- "Time for synthesis" → Suggest: `/osl-synthesis`

### Error Recovery
When tool calls fail:
1. Read the JSON error response
2. Extract the "suggestion" field
3. Show user: "Let me try: [suggestion]"
4. Execute suggested command
5. If still fails, explain the issue clearly

### Natural Language Processing
Users may say things naturally. Map to tools:
- "Beginning Deep Work" → `osl book start --book "Deep Work"`
- "Done with chapter 3" → `osl session end` (then collect metrics)
- "How am I doing?" → `osl metrics report --type progress`

### Proactive Guidance
- Morning: Check `osl review due` and remind if items pending
- After reading: Automatically invoke osl-tutor subagent
- End of week: Suggest `/osl-synthesis`
- Monthly: Remind about transfer project

## Output Format
Always be concise but helpful:
- Show what command is being run
- Display results clearly
- Suggest next logical action
- Keep responses under 3 lines when possible

## When Unsure
If you can't determine which OSL tool to use:
1. Run: `osl help` to show available commands
2. Ask user to clarify their intent
3. Never try to implement OSL logic yourself
4. Always defer to the CLI tool
```

**Settings Configuration:** `.claude/settings.json`
```json
{
  "outputStyle": "OSL Default",
  "hooks": {
    "enabled": true,
    "postCommand": ".claude/hooks/track-osl.sh",
    "sessionStart": ".claude/hooks/osl-startup.sh"
  }
}
```

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
// coach_state.json - Central learning state (AUTHORITATIVE)
{
  "last_updated": "YYYY-MM-DD HH:MM",
  "active_books": [{
    "id": "deep_work_2024",
    "title": "Deep Work",
    "author": "Cal Newport",
    "start_date": "2024-01-01",
    "current_page": 147,
    "total_pages": 296,
    "sessions_completed": 12,
    "avg_retrieval_score": 82
  }],
  "review_schedule": {
    "next_interleaving": "YYYY-MM-DD",
    "next_calibration": "YYYY-MM-DD",
    "next_synthesis": "YYYY-MM-DD",
    "next_project": "YYYY-MM-DD"
  },
  "performance_metrics": {
    "7d_avg_retrieval": 82,
    "7d_avg_prediction_accuracy": 85,
    "current_card_debt_ratio": 1.3,
    "daily_review_throughput": 60
  },
  "governance_status": {
    "calibration_gate": "passing",  // 75-85% range
    "card_debt_gate": "passing",     // 1.5x-2.5x range
    "transfer_gate": "warning",      // monthly requirement
    "remediation_active": false
  },
  "governance_thresholds": {
    "calibration_gate": {"min": 75, "default": 80, "max": 85},
    "card_debt_multiplier": {"min": 1.5, "default": 2.0, "max": 2.5},
    "max_new_cards": {"min": 4, "default": 8, "max": 10},
    "interleaving_per_week": {"min": 1, "default": 2, "max": 3}
  }
}
```

```json
// session_history.json - Detailed session logs with micro-loop tracking
{
  "sessions": [{
    "id": "session_2024_01_20_001",
    "timestamp": "2024-01-20T09:30:00Z",
    "book": "deep_work",
    "pages_read": 15,
    "curiosity_questions": [
      {
        "id": 1,
        "question": "How does deep work relate to flow state?",
        "created": "09:32:00",
        "resolved": true,
        "answer": "Deep work requires deliberate practice, flow is the experience",
        "page_found": 48
      }
    ],
    "micro_loops": [
      {
        "pages": "45-50",
        "start_time": "09:35:00",
        "recall_quality": "complete",
        "recall_text_hash": "a3f5d8c9...",  // SHA256 of verbatim text
        "feynman_text_hash": "b7e2a1d4...",
        "confidence": 4,
        "gaps_identified": ["4-hour limit"],
        "tutor_questions_asked": 3,
        "correct_answers": 3
      }
    ],
    "misconceptions": [
      {
        "concept": "deep work vs flow",
        "wrong_understanding": "They are the same",
        "correct_understanding": "Deep work is practice, flow is experience",
        "identified_during": "micro_loop_2"
      }
    ],
    "flashcards_created": [
      {
        "id": "card_001",
        "learner_authored": true,
        "content_hash": "c4d9e2f1...",
        "from_gap": "4-hour limit"
      }
    ],
    "permanent_notes": 2,
    "retrieval_rate_realtime": 87,  // Calculated during session
    "duration_minutes": 47
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

## AI Non-Determinism Framework

### Purpose
Establish systematic guardrails to ensure reliable OSL automation despite inherent AI non-determinism. This framework enables natural language interaction while guaranteeing deterministic outcomes through structured constraints and validation layers.

### Core Philosophy: Three-Layer Abstraction Model

**The OSL interaction hierarchy (increasing abstraction/non-determinism):**

1. **CLI Tool Layer** (Deterministic)
   - Direct command: `osl start --book "Deep Work"`
   - Full control, explicit parameters
   - Used by: Power users, scripts, automation

2. **Slash Command Layer** (Semi-Deterministic)
   - Claude command: `/osl-start "Deep Work"`
   - Thin wrapper over CLI with validation
   - Used by: Users wanting quick, reliable execution

3. **Natural Language Layer** (Non-Deterministic)
   - Conversation: "I'm starting Deep Work today"
   - AI interprets and maps to CLI tool
   - Used by: Users wanting natural interaction

**Core Rules:**
- The CLI tool is the **single source of truth** for all OSL operations
- Claude/AI layers are **thin interfaces** that translate to CLI commands
- All business logic, validation, and state management lives in the CLI tool
- AI never implements OSL logic, only translates intent to CLI calls

### The Seven Pillars of Deterministic AI Automation

#### 1. **CLI Tool as Source of Truth** [CRITICAL]
All OSL logic lives in the CLI tool, not in AI:
- User says: "I'm done reading chapter 3"
- AI interprets: End session with chapter context
- Execution: `osl session end --chapter 3`
- CLI handles: validation, calculations, state updates, error messages

#### 2. **State Isolation** [CRITICAL]
AI never directly modifies state files:
- ❌ AI writes JSON directly
- ✅ AI calls: `osl state update --metric retrieval --value 0.87`
- All state changes go through CLI's validated, atomic operations
- CLI provides rollback and backup automatically

#### 3. **Calculation Delegation** [CRITICAL]
AI never performs arithmetic or date calculations:
- ❌ AI calculates: "7/8 = 87.5%"
- ✅ AI calls: `osl metrics calculate --type retrieval --success 7 --total 8`
- CLI returns: `{"retrieval_rate": 0.875, "formatted": "87.5%"}`
- AI displays formatted result to user

#### 4. **Error Feedback Loop** [CRITICAL]
CLI provides clear, parseable error messages for AI self-correction:
```bash
$ osl session start
ERROR: No book selected. Use --book flag or run 'osl book select' first
SUGGESTION: osl session start --book "Deep Work"
EXIT_CODE: 1
```
AI reads error, extracts suggestion, retries with correction

#### 5. **Thin Wrapper Commands** [IMPORTANT]
Slash commands are minimal validators before CLI calls:
```markdown
---
allowed-tools: Bash(osl:*)
---
Parse $ARGUMENTS for book name
If missing: Ask user "Which book?"
Then: `osl start --book "$BOOK"`
Display CLI output directly
```

#### 6. **Hook Automation** [IMPORTANT]
Hooks call CLI tool, never duplicate logic:
```bash
# .claude/hooks/post-command.sh
if [[ "$1" == "/osl-"* ]]; then
    osl metrics track --command "$1" --timestamp "$(date -Iseconds)"
fi
```

#### 7. **Context Retrieval** [IMPORTANT]
Subagents use CLI to get context:
```bash
osl context get --type session --format json
osl summary generate --week 3 --output markdown
osl state query --metric calibration_score
```

### Implementation Patterns

#### Pattern 1: Contextual Command Execution
```markdown
# .claude/commands/osl-session.md
---
allowed-tools: Bash(python3:scripts/session_*.py), Read
argument-hint: start [book] | end | status
description: Natural language session management
---

## Context Loading (Deterministic)
- Current state: !`python3 scripts/get_session_state.py --format json`
- Active book: !`cat ai_state/current_book.txt 2>/dev/null || echo "none"`
- Governance: !`python3 scripts/check_governance.py --format json`

## Your Task
Interpret user intent from: $ARGUMENTS

Map to appropriate script:
- "start", "begin", "starting" → `python3 scripts/session_start.py`
- "end", "done", "finished" → `python3 scripts/session_end.py`
- "status", "where am I" → `python3 scripts/session_status.py`

NEVER:
- Calculate durations manually
- Parse dates yourself
- Make governance decisions
- Edit state files directly
```

#### Pattern 2: Validated State Updates
```python
# scripts/session_end.py
import json
import sys
from jsonschema import validate
from datetime import datetime

def end_session(metrics_input):
    """Deterministic session ending with validation"""
    
    # Load and validate current state
    with open('ai_state/coach_state.json') as f:
        state = json.load(f)
    
    # Validate input from AI
    schema = {
        "type": "object",
        "properties": {
            "pages": {"type": "integer", "minimum": 0},
            "retrieval_attempts": {"type": "integer", "minimum": 0},
            "successful_recalls": {"type": "integer", "minimum": 0},
            "cards_created": {"type": "integer", "minimum": 0, "maximum": 8}
        },
        "required": ["pages", "retrieval_attempts", "successful_recalls"]
    }
    
    try:
        validate(metrics_input, schema)
    except:
        return {"error": "Invalid metrics format", "expected": schema}
    
    # Calculate derived metrics deterministically
    retrieval_rate = (metrics_input['successful_recalls'] / 
                     metrics_input['retrieval_attempts'] 
                     if metrics_input['retrieval_attempts'] > 0 else 0)
    
    # Update state atomically
    state['metrics']['last_retrieval_rate'] = retrieval_rate
    state['metrics']['total_sessions'] += 1
    
    # Check governance gates
    if retrieval_rate < 0.8:
        state['governance']['calibration_gate'] = 'warning'
    
    # Write with backup
    backup_path = f"ai_state/backups/state_{datetime.now():%Y%m%d_%H%M%S}.json"
    shutil.copy('ai_state/coach_state.json', backup_path)
    
    with open('ai_state/coach_state.json.tmp', 'w') as f:
        json.dump(state, f, indent=2)
    os.rename('ai_state/coach_state.json.tmp', 'ai_state/coach_state.json')
    
    return {
        "status": "success",
        "retrieval_rate": f"{retrieval_rate:.1%}",
        "governance": state['governance'],
        "next_action": "Run /osl-review to check due items"
    }
```

#### Pattern 3: Structured Output Enforcement
```markdown
# Force AI to use specific output format
---
allowed-tools: Bash(python3:scripts/quiz_runner.py)
---

## Quiz Administration Protocol

You MUST use the quiz runner for ALL quiz operations:

```bash
# Initialize quiz
python3 scripts/quiz_runner.py --action start --topic "$TOPIC"

# Get next question (returns JSON)
python3 scripts/quiz_runner.py --action next

# Submit confidence (returns validation)
python3 scripts/quiz_runner.py --action confidence --rating $RATING

# Submit answer (returns feedback)
python3 scripts/quiz_runner.py --action answer --response "$ANSWER"
```

Parse the JSON output and present to user. NEVER:
- Show answers before confidence collection
- Skip feedback delivery
- Calculate scores yourself
```

### Validation Gates for Commands

Every OSL command must pass these validation gates:

#### Gate 1: Input Validation
- Can the AI reliably parse user intent?
- Are there ambiguous cases that need clarification?
- Is there a clear mapping to deterministic actions?

#### Gate 2: State Safety
- Are all state modifications atomic?
- Is there rollback capability?
- Are backups created before changes?

#### Gate 3: Calculation Accuracy
- Are all calculations delegated to scripts?
- Do scripts return structured, parseable output?
- Are edge cases handled (division by zero, etc.)?

#### Gate 4: Flow Integrity
- Is the workflow enforceable by state machine?
- Can the AI skip critical steps?
- Are there guards against out-of-order execution?

#### Gate 5: Error Recovery
- What happens when scripts fail?
- How does AI communicate errors to users?
- Is there always a manual fallback?

### Continuous Validation Protocol

```bash
# scripts/validate_ai_behavior.py
"""
Run after each session to detect AI misbehavior
"""

def validate_session_log(log_path):
    violations = []
    
    with open(log_path) as f:
        log = json.load(f)
    
    # Check for manual calculations
    if 'calculated_by_ai' in log:
        violations.append("AI performed manual calculation")
    
    # Check for direct state edits
    if log.get('state_edit_method') != 'script':
        violations.append("AI edited state directly")
    
    # Check for skipped steps
    expected_flow = ['start', 'active', 'ending', 'complete']
    if log.get('state_transitions') != expected_flow:
        violations.append(f"Invalid flow: {log.get('state_transitions')}")
    
    # Check governance enforcement
    if log.get('governance_overridden'):
        violations.append("AI overrode governance gate")
    
    return {
        'session': log_path,
        'violations': violations,
        'severity': 'critical' if violations else 'pass'
    }
```

### Migration Strategy for Existing Commands

Transform non-deterministic commands systematically:

**Before (Non-deterministic):**
```markdown
Calculate retrieval rate and update the state file
```

**After (Deterministic):**
```markdown
Run: `python3 scripts/update_metrics.py --retrieval $SUCCESS --attempts $TOTAL`
Display the JSON output to user
```

### Testing Framework

```bash
# scripts/test_determinism.sh
#!/bin/bash

# Test 1: State modification safety
echo "Testing state safety..."
cp ai_state/coach_state.json /tmp/before.json
/osl-session end <<< "5 pages, 8 retrieval, 7 success"
diff /tmp/before.json ai_state/backups/latest.json || echo "✓ Backup created"

# Test 2: Calculation accuracy
echo "Testing calculations..."
result=$(python3 scripts/calculate_metrics.py retrieval_rate 7 8)
expected="0.875"
[ "$result" == "$expected" ] && echo "✓ Calculation correct"

# Test 3: Flow enforcement
echo "Testing flow state..."
python3 scripts/quiz_runner.py --action answer --response "test" 2>&1 | \
  grep -q "Must collect confidence first" && echo "✓ Flow enforced"

# Test 4: Governance gates
echo "Testing governance..."
python3 scripts/check_governance.py --set card_debt 2.5
/osl-session start 2>&1 | grep -q "BLOCKED" && echo "✓ Gate enforced"
```

### Success Metrics

Track reliability improvements:

1. **Error Rate**: < 1% of sessions have AI violations
2. **Rollback Frequency**: < 0.1% of state updates need rollback
3. **User Corrections**: < 5% of commands need user intervention
4. **Flow Violations**: 0 instances of skipped required steps
5. **Calculation Errors**: 0 instances of manual math by AI

## OSL CLI Tool Specification

### Architecture
```
osl                         # Main CLI entry point
├── book/                   # Book management commands
│   ├── start              # Initialize new book
│   ├── list               # List active books
│   └── select             # Set current book
├── session/               # Session management
│   ├── start              # Begin reading session
│   ├── end                # End with metrics
│   └── status             # Current session info
├── questions/             # Curiosity question tracking [LEARNING]
│   ├── add                # Add curiosity question
│   ├── list               # Show current questions
│   ├── resolve            # Mark question as answered
│   └── pending            # Show unresolved questions
├── microloop/             # Micro-loop tracking [LEARNING]
│   ├── complete           # Record micro-loop completion
│   ├── recall             # Save free recall (verbatim)
│   └── explain            # Save Feynman explanation (verbatim)
├── flashcard/             # Flashcard management [LEARNING]
│   ├── create             # Learner creates card
│   ├── list               # Show session cards
│   └── check-limit        # Check against 8-card limit
├── misconception/         # Misconception tracking [LEARNING]
│   ├── add                # Learner identifies misconception
│   ├── list               # Show current misconceptions
│   └── resolve            # Mark as corrected
├── review/                # Retrieval practice [ADMIN]
│   ├── due                # Show due items
│   ├── quiz               # Run quiz session
│   └── calibrate          # Calibration test
├── synthesis/             # Integration commands [LEARNING]
│   ├── weekly             # Weekly synthesis
│   └── project            # Transfer projects
├── metrics/               # Calculations & queries [ADMIN]
│   ├── calculate          # Compute metrics
│   ├── track              # Record events
│   └── report             # Generate reports
├── state/                 # State management [ADMIN]
│   ├── query              # Read state values
│   ├── update             # Modify state
│   └── backup             # Create backup
├── context/               # AI context generation [ADMIN]
│   ├── get                # Retrieve context
│   └── summary            # Generate summaries
└── config/                # Configuration [ADMIN]
    ├── init               # Initial setup
    └── validate           # Check configuration
```

### CLI Implementation with Verbatim Preservation
```python
#!/usr/bin/env python3
# osl_cli.py - Main CLI tool with Learning/Admin boundaries
import argparse
import json
import sys
import hashlib
from pathlib import Path
from datetime import datetime
import logging

class CommandType:
    """Explicit boundary between learning and admin tasks"""
    LEARNING = "LEARNING"  # Requires human cognition
    ADMIN = "ADMIN"        # Can be automated

class OSLCli:
    """OSL Command Line Interface - Single source of truth for all operations"""
    
    def __init__(self):
        self.config_path = Path.home() / '.osl' / 'config.json'
        self.state_path = Path('ai_state/coach_state.json')
        self.session_path = Path('ai_state/current_session.json')
        self.setup_logging()
        
    def setup_logging(self):
        """Configure structured logging for AI parsing"""
        logging.basicConfig(
            format='%(levelname)s: %(message)s',
            level=logging.INFO
        )
        
    def preserve_verbatim(self, text, activity_type):
        """Preserve learner's exact input with hash verification"""
        return {
            'raw': text,
            'hash': hashlib.sha256(text.encode()).hexdigest(),
            'timestamp': datetime.now().isoformat(),
            'type': activity_type,
            'preserved': True
        }
        
    def error_with_suggestion(self, message, suggestion=None, code=1):
        """Provide clear error messages for AI self-correction"""
        output = {
            "status": "error",
            "message": message,
            "suggestion": suggestion,
            "exit_code": code
        }
        print(json.dumps(output, indent=2))
        sys.exit(code)
        
    def success_response(self, data):
        """Return structured success response"""
        output = {
            "status": "success",
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(output, indent=2))
        return 0

    # Command implementations
    def cmd_questions_add(self, args):
        """[LEARNING] Add curiosity question"""
        self.command_type = CommandType.LEARNING
        
        session = self.load_current_session()
        question = {
            'id': len(session.get('curiosity_questions', [])) + 1,
            'question': args.question,
            'created': datetime.now().isoformat(),
            'resolved': False,
            'answer': None,
            'page_found': None
        }
        
        if 'curiosity_questions' not in session:
            session['curiosity_questions'] = []
        session['curiosity_questions'].append(question)
        
        self.save_current_session(session)
        return self.success_response({
            'question_id': question['id'],
            'message': f"Question {question['id']} added"
        })
    
    def cmd_microloop_complete(self, args):
        """[LEARNING] Record micro-loop completion with real-time metrics"""
        self.command_type = CommandType.LEARNING
        
        session = self.load_current_session()
        
        # Preserve recall and explanation verbatim
        recall_preserved = self.preserve_verbatim(args.recall_text, 'free_recall')
        explain_preserved = self.preserve_verbatim(args.explain_text, 'feynman')
        
        micro_loop = {
            'pages': args.pages,
            'timestamp': datetime.now().isoformat(),
            'recall_quality': args.recall_quality,
            'recall_text_hash': recall_preserved['hash'],
            'feynman_text_hash': explain_preserved['hash'],
            'confidence': args.confidence,
            'gaps_identified': args.gaps.split(',') if args.gaps else []
        }
        
        if 'micro_loops' not in session:
            session['micro_loops'] = []
        session['micro_loops'].append(micro_loop)
        
        # Calculate real-time retrieval rate
        total = len(session['micro_loops'])
        successful = sum(1 for ml in session['micro_loops'] 
                        if ml['recall_quality'] in ['complete', 'good'])
        retrieval_rate = (successful / total) * 100 if total > 0 else 0
        
        session['retrieval_rate_realtime'] = retrieval_rate
        
        # Check governance gates in real-time
        governance_warnings = []
        if retrieval_rate < 80:
            governance_warnings.append("Retrieval below 80% - consider review")
        
        self.save_current_session(session)
        return self.success_response({
            'micro_loop_count': total,
            'retrieval_rate': f'{retrieval_rate:.1f}%',
            'warnings': governance_warnings
        })
    
    def cmd_misconception_add(self, args):
        """[LEARNING] Learner identifies misconception"""
        self.command_type = CommandType.LEARNING
        
        session = self.load_current_session()
        misconception = {
            'concept': args.concept,
            'wrong_understanding': args.wrong,
            'correct_understanding': args.correct,
            'identified_during': f"micro_loop_{len(session.get('micro_loops', []))}",
            'timestamp': datetime.now().isoformat()
        }
        
        if 'misconceptions' not in session:
            session['misconceptions'] = []
        session['misconceptions'].append(misconception)
        
        self.save_current_session(session)
        return self.success_response({
            'misconception_tracked': args.concept,
            'message': 'Misconception logged for review'
        })
    
    def cmd_flashcard_create(self, args):
        """[LEARNING] Learner creates flashcard (enforces limits)"""
        self.command_type = CommandType.LEARNING
        
        session = self.load_current_session()
        current_cards = len(session.get('flashcards_created', []))
        
        # Check governance limits
        state = self.load_state()
        max_cards = state['governance_thresholds']['max_new_cards']['default']
        if state['governance_status']['calibration_gate'] == 'failing':
            max_cards = state['governance_thresholds']['max_new_cards']['min']
        
        if current_cards >= max_cards:
            return self.error_with_suggestion(
                f"Card limit ({max_cards}) reached for this session",
                "Review existing cards or save for next session"
            )
        
        # Preserve card content verbatim
        card_preserved = self.preserve_verbatim(
            f"FRONT: {args.front}\nBACK: {args.back}",
            'flashcard'
        )
        
        card = {
            'id': f"card_{current_cards + 1:03d}",
            'learner_authored': True,
            'content_hash': card_preserved['hash'],
            'from_gap': args.gap if args.gap else None,
            'source': args.source,
            'timestamp': datetime.now().isoformat()
        }
        
        if 'flashcards_created' not in session:
            session['flashcards_created'] = []
        session['flashcards_created'].append(card)
        
        self.save_current_session(session)
        return self.success_response({
            'card_id': card['id'],
            'cards_created': current_cards + 1,
            'remaining': max_cards - (current_cards + 1)
        })
    
    def cmd_book_start(self, args):
        """[ADMIN] Initialize new book with all OSL structure"""
        self.command_type = CommandType.ADMIN
        
        if not args.book:
            self.error_with_suggestion(
                "No book title provided",
                "osl book start --book 'Book Title'"
            )
        
        # Sanitize book name
        safe_name = args.book.lower().replace(' ', '_')
        book_path = Path(f'obsidian/10_books/{safe_name}')
        
        # Create structure
        book_path.mkdir(parents=True, exist_ok=True)
        (book_path / 'notes' / 'permanent').mkdir(parents=True)
        (book_path / 'notes' / 'literature').mkdir(parents=True)
        
        # Update state atomically
        state = self.load_state()
        state['active_books'].append({
            'id': safe_name,
            'title': args.book,
            'author': args.author,
            'start_date': datetime.now().isoformat(),
            'current_page': 0,
            'total_pages': args.pages or 0
        })
        self.save_state(state)
        
        return self.success_response({
            'book_id': safe_name,
            'path': str(book_path),
            'message': f"Book '{args.book}' initialized"
        })
    
    def cmd_session_start(self, args):
        """Start session with governance checks"""
        state = self.load_state()
        
        # Check governance gates
        if state['governance']['card_debt_gate'] == 'failing':
            self.error_with_suggestion(
                "Card debt exceeds 2x limit",
                "osl review due --clear-debt"
            )
        
        # Create session
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        session_file = Path(f'ai_state/session_logs/{session_id}.json')
        
        session_data = {
            'id': session_id,
            'book': args.book or state['active_books'][0]['title'],
            'start_time': datetime.now().isoformat()
        }
        
        session_file.write_text(json.dumps(session_data, indent=2))
        Path('.osl_session_timer').write_text(str(datetime.now().timestamp()))
        
        warnings = []
        if state['governance']['calibration_gate'] == 'warning':
            warnings.append("Calibration <80%: max 4 new cards")
        
        return self.success_response({
            'session_id': session_id,
            'warnings': warnings
        })
    
    def cmd_metrics_calculate(self, args):
        """Perform calculations deterministically"""
        if args.type == 'retrieval':
            if args.total == 0:
                rate = 0.0
            else:
                rate = args.success / args.total
            
            return self.success_response({
                'retrieval_rate': rate,
                'formatted': f'{rate:.1%}',
                'success': args.success,
                'total': args.total
            })
        
        self.error_with_suggestion(
            f"Unknown metric type: {args.type}",
            "osl metrics calculate --type retrieval"
        )
    
    def load_state(self):
        """Load state with validation"""
        if not self.state_path.exists():
            return self.default_state()
        
        with open(self.state_path) as f:
            return json.load(f)
    
    def save_state(self, state):
        """Save state atomically with backup"""
        # Backup
        backup = self.state_path.with_suffix('.backup')
        if self.state_path.exists():
            backup.write_text(self.state_path.read_text())
        
        # Atomic write
        temp = self.state_path.with_suffix('.tmp')
        temp.write_text(json.dumps(state, indent=2))
        temp.rename(self.state_path)

def main():
    parser = argparse.ArgumentParser(prog='osl')
    subparsers = parser.add_subparsers(dest='command')
    
    # Book commands
    book = subparsers.add_parser('book')
    book_sub = book.add_subparsers(dest='subcommand')
    
    book_start = book_sub.add_parser('start')
    book_start.add_argument('--book', required=True)
    book_start.add_argument('--author')
    book_start.add_argument('--pages', type=int)
    
    # Session commands
    session = subparsers.add_parser('session')
    session_sub = session.add_subparsers(dest='subcommand')
    
    session_start = session_sub.add_parser('start')
    session_start.add_argument('--book')
    
    session_end = session_sub.add_parser('end')
    session_end.add_argument('--pages', type=int, required=True)
    session_end.add_argument('--retrieval', type=int, required=True)
    session_end.add_argument('--recalls', type=int, required=True)
    
    # Metrics commands
    metrics = subparsers.add_parser('metrics')
    metrics_sub = metrics.add_subparsers(dest='subcommand')
    
    calc = metrics_sub.add_parser('calculate')
    calc.add_argument('--type', required=True)
    calc.add_argument('--success', type=int)
    calc.add_argument('--total', type=int)
    
    # Parse and execute
    args = parser.parse_args()
    cli = OSLCli()
    
    # Route to appropriate command
    if args.command == 'book' and args.subcommand == 'start':
        return cli.cmd_book_start(args)
    elif args.command == 'session' and args.subcommand == 'start':
        return cli.cmd_session_start(args)
    elif args.command == 'metrics' and args.subcommand == 'calculate':
        return cli.cmd_metrics_calculate(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

### Example CLI Usage

```bash
# Curiosity Questions (LEARNING)
osl questions add --question "How does deep work relate to flow state?"
osl questions list --session current
osl questions resolve --id 1 --answer "Found on p48: different concepts" --page 48
osl questions pending

# Micro-Loop Tracking (LEARNING) - Real-time metrics
osl microloop complete \
  --pages "45-50" \
  --recall-quality "complete" \
  --confidence 4 \
  --gaps "4-hour limit" \
  --recall-text "$(cat recall.txt)" \
  --explain-text "$(cat feynman.txt)"

# Misconception Tracking (LEARNING)
osl misconception add \
  --concept "deep work vs flow" \
  --wrong "They are the same" \
  --correct "Deep work is practice, flow is experience"

# Flashcard Creation (LEARNING) - Learner authored
osl flashcard create \
  --front "What's the daily limit for deep work?" \
  --back "4 hours (up to 5 with training)" \
  --source "Deep Work p.47" \
  --gap "4-hour limit"

osl flashcard check-limit  # Shows remaining cards allowed

# Session Management (ADMIN)
osl session start --book "Deep Work"
osl session status  # Shows real-time retrieval rate
osl session end     # Automatic metrics from micro-loops

# Metrics (ADMIN) - All calculations delegated
osl metrics calculate --type retrieval --success 7 --total 8
osl metrics report --type progress --period week
```

### Installation
```bash
# Install globally
pip install -e .

# Or create standalone executable
pyinstaller --onefile osl_cli.py -n osl

# Add to PATH
echo 'export PATH="$HOME/.osl/bin:$PATH"' >> ~/.bashrc
```

## Example Deterministic Scripts

### Session Start Script
```python
#!/usr/bin/env python3
# scripts/session_start.py
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

def start_session(book_title=None):
    """Start a new OSL session with governance checks"""
    
    # Check governance gates first
    with open('ai_state/coach_state.json') as f:
        state = json.load(f)
    
    # Hard blocks
    if state['governance']['card_debt_gate'] == 'failing':
        return {
            "status": "blocked",
            "reason": "Card debt exceeds 2x limit",
            "action": "Run /osl-review to clear backlog",
            "exit_code": 1
        }
    
    # Warnings
    warnings = []
    if state['governance']['calibration_gate'] == 'failing':
        warnings.append("Calibration below 80% - limiting new cards to 4")
    
    # Create session
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_data = {
        "id": session_id,
        "book": book_title or state.get('active_books', [{}])[0].get('title'),
        "start_time": datetime.now().isoformat(),
        "warnings": warnings
    }
    
    # Write session file
    session_file = f"ai_state/session_logs/{session_id}.json"
    with open(session_file, 'w') as f:
        json.dump(session_data, f, indent=2)
    
    # Write timer file
    with open('.osl_session_timer', 'w') as f:
        f.write(str(datetime.now().timestamp()))
    
    return {
        "status": "success",
        "session_id": session_id,
        "book": session_data['book'],
        "warnings": warnings,
        "message": "Session started. Timer running."
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--book', help='Book title')
    args = parser.parse_args()
    
    result = start_session(args.book)
    print(json.dumps(result, indent=2))
    sys.exit(result.get('exit_code', 0))
```

### Metric Calculation Script
```bash
#!/bin/bash
# scripts/calculate_metrics.sh

case "$1" in
    retrieval_rate)
        # Calculate retrieval rate with precision
        if [ "$3" -eq 0 ]; then
            echo "0.0"
        else
            echo "scale=3; $2 / $3" | bc
        fi
        ;;
        
    calibration_score)
        # Complex calibration from confidence vs actual
        python3 -c "
import json
import sys

confidence_file = '$2'
actual_file = '$3'

with open(confidence_file) as f:
    confidence = json.load(f)['ratings']
with open(actual_file) as f:
    actual = json.load(f)['correct']

# Brier score calculation
score = sum((c/5 - a)**2 for c,a in zip(confidence, actual)) / len(confidence)
calibration = (1 - score) * 100

print(f'{calibration:.1f}')
"
        ;;
        
    card_debt_ratio)
        # Query current card debt
        python3 -c "
import json

with open('ai_state/coach_state.json') as f:
    state = json.load(f)

due = state['metrics'].get('cards_due', 0)
throughput = state['metrics'].get('daily_throughput', 1)

ratio = due / max(throughput, 1)
print(f'{ratio:.2f}')
"
        ;;
        
    *)
        echo "Unknown metric: $1" >&2
        exit 1
        ;;
esac
```

### Quiz Runner with State Machine
```python
#!/usr/bin/env python3
# scripts/quiz_runner.py
import json
import argparse
import sys
from pathlib import Path

class QuizStateMachine:
    """Enforces quiz flow: INIT -> CONFIDENCE -> ANSWER -> FEEDBACK"""
    
    def __init__(self):
        self.state_file = '.quiz_state.json'
        self.load_state()
    
    def load_state(self):
        if Path(self.state_file).exists():
            with open(self.state_file) as f:
                self.state = json.load(f)
        else:
            self.state = {"status": "INIT", "current_question": None}
    
    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)
    
    def start(self, topic):
        """Initialize quiz session"""
        if self.state['status'] != 'INIT':
            return {"error": f"Cannot start: already in {self.state['status']}"}
        
        # Load questions for topic
        quiz_file = f"quiz_bank/{topic}/quiz_001.json"
        with open(quiz_file) as f:
            questions = json.load(f)['questions']
        
        self.state = {
            "status": "READY",
            "topic": topic,
            "questions": questions,
            "current_index": 0,
            "responses": []
        }
        self.save_state()
        
        return {
            "status": "success",
            "message": f"Quiz started for {topic}",
            "total_questions": len(questions)
        }
    
    def next_question(self):
        """Get next question - must be in READY state"""
        if self.state['status'] != 'READY':
            return {"error": f"Cannot get question in state: {self.state['status']}"}
        
        if self.state['current_index'] >= len(self.state['questions']):
            return {"status": "complete", "message": "All questions answered"}
        
        question = self.state['questions'][self.state['current_index']]
        self.state['status'] = 'AWAITING_CONFIDENCE'
        self.state['current_question'] = question
        self.save_state()
        
        return {
            "status": "success",
            "question_number": self.state['current_index'] + 1,
            "question": question['text'],
            "next_action": "Submit confidence rating (1-5)"
        }
    
    def submit_confidence(self, rating):
        """Record confidence - must be before answer"""
        if self.state['status'] != 'AWAITING_CONFIDENCE':
            return {"error": "Must get question first"}
        
        if not 1 <= rating <= 5:
            return {"error": "Confidence must be 1-5"}
        
        self.state['current_confidence'] = rating
        self.state['status'] = 'AWAITING_ANSWER'
        self.save_state()
        
        return {
            "status": "success",
            "confidence_recorded": rating,
            "next_action": "Submit your answer"
        }
    
    def submit_answer(self, answer):
        """Check answer and provide feedback"""
        if self.state['status'] != 'AWAITING_ANSWER':
            return {"error": "Must submit confidence first"}
        
        question = self.state['current_question']
        correct = answer.lower() == question['answer'].lower()
        
        # Record response
        self.state['responses'].append({
            "question_id": self.state['current_index'],
            "confidence": self.state['current_confidence'],
            "answer": answer,
            "correct": correct
        })
        
        # Move to next question
        self.state['current_index'] += 1
        self.state['status'] = 'READY'
        self.save_state()
        
        return {
            "status": "success",
            "correct": correct,
            "feedback": question.get('feedback', 'No feedback available'),
            "citation": question.get('citation'),
            "next_action": "Get next question or end quiz"
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', required=True, 
                       choices=['start', 'next', 'confidence', 'answer'])
    parser.add_argument('--topic', help='Topic for quiz')
    parser.add_argument('--rating', type=int, help='Confidence rating')
    parser.add_argument('--response', help='Answer text')
    
    args = parser.parse_args()
    quiz = QuizStateMachine()
    
    if args.action == 'start':
        result = quiz.start(args.topic)
    elif args.action == 'next':
        result = quiz.next_question()
    elif args.action == 'confidence':
        result = quiz.submit_confidence(args.rating)
    elif args.action == 'answer':
        result = quiz.submit_answer(args.response)
    
    print(json.dumps(result, indent=2))
    sys.exit(1 if 'error' in result else 0)
```

## Critical Design Clarifications

### 1. Quiz Generation Philosophy (Testing Effect + Calibration)
Based on research evidence for testing effect and calibration:
- **Micro-loop questions**: 2-3 AI-generated AFTER learner's free recall (preserves effortful retrieval)
- **Weekly calibration**: 6-10 AI-generated items (3 recall, 3-4 application, 2-3 transfer)
- **Pre-reading probe**: ≤90s, 3 items, optional, simple prerequisites only
- **Source**: AI generates from material covered, not from "gaps" (learner identifies gaps)
- **Storage**: Generated quizzes saved for reuse and refinement
- **Evidence**: Testing effect (Roediger & Karpicke, 2006) + immediate feedback (Hattie & Timperley, 2007)

### 2. Flashcard Pipeline (Learner-Authored, AI-Assisted)
```json
// anki/cards/{session_id}.json
{
  "session_id": "20250129_deep_work",
  "book": "Deep Work",
  "cards": [
    {
      "id": "uuid-1234",
      "type": "cloze",
      "text": "The {{c1::micro-loop}} consists of Q→Read→Retrieve→Explain→Feedback",
      "source": {
        "title": "OSL V3 Core",
        "author": "OSL Team",
        "page": "6",
        "location": "Section 6"
      },
      "tags": ["book/osl_v3", "concept/micro_loop", "type/cloze"],
      "created": "2025-01-29T10:30:00Z",
      "from_miss": true,
      "learner_authored": true,
      "ai_refined": false,
      "context": "I failed to recall this during micro-loop 3"
    },
    {
      "id": "uuid-5678",
      "type": "application",
      "front": "You've just read 10 pages of a technical chapter. What should you do next?",
      "back": "Stop reading and enter the micro-loop: 1) Free recall for 1-2 min, 2) Write Feynman explanation, 3) Get Tutor feedback",
      "source": {
        "title": "OSL V3 Core",
        "page": "6"
      },
      "tags": ["book/osl_v3", "concept/micro_loop", "type/application"],
      "created": "2025-01-29T10:35:00Z",
      "from_miss": false
    }
  ]
}
```

**AnkiConnect Pipeline:**
```bash
# CLI commands for flashcard management
osl flashcard create --from-miss "concept" --session current
osl flashcard list --session current
osl flashcard sync --deck "OSL::BookTitle"  # Uses AnkiConnect
osl flashcard export --format apkg          # Fallback export
```

### 3. Permanent Note Creation Workflow
Following OSL Section 7 ("end of Each Session, 8-12 min"):
```bash
# After micro-loops complete
osl note create --type permanent --session current
# CLI provides template with structure:
# - Claim (own words)
# - Context (applies when/fails when)
# - Example or application
# - Citation (with page/location)
# - Links to related notes

# AI assistance available but not required
osl note suggest --from-retrieval "last-session"
```

### 4. Misconception Tracking Implementation
```json
// ai_state/misconceptions.json
{
  "misconceptions": [
    {
      "id": "misc-001",
      "concept": "spacing intervals",
      "initial_understanding": "Review daily for best retention",
      "corrected_understanding": "Increasing intervals (1d→3d→7d) optimize retention",
      "date_identified": "2025-01-29",
      "date_resolved": "2025-02-05",
      "source": "micro-loop-3",
      "resolution_method": "targeted_practice"
    }
  ]
}
```

### 5. Multi-Book Session Handling
- **Design Decision**: Single book per session (simplifies tracking)
- **Multiple books**: Use separate sessions with explicit book switching
```bash
osl session end --book "Deep Work"
osl session start --book "Atomic Habits"
```

### Flashcard Creation Philosophy (Generation Effect)
**Research-grounded approach:**
- **Learner authors cards** from their identified misses (generation effect)
- **AI assists only with**:
  - Formatting (cloze syntax)
  - Citation verification
  - Flagging ambiguity
  - Suggesting refinements (learner approves)
- **Never**: AI creates cards automatically from "gaps"
- **Always**: Learner decides what becomes a card

### 6. Subagent Context Generation
```bash
# Each subagent gets specific context via CLI
osl context tutor    # Returns: misconceptions, failed retrievals, session history
osl context extractor # Returns: current text, citation requirements
osl context coach    # Returns: metrics, gates, schedule, performance trends

# Subagents call these in their initialization:
# .claude/agents/osl-tutor.md:
# Context: !`osl context tutor --format json`
```

### 7. Hybrid Quiz Storage (Obsidian + Structured)
```
obsidian/quiz_bank/
├── deep_work/
│   ├── chapter_1/
│   │   ├── quiz_001.md        # Human-readable in Obsidian
│   │   ├── quiz_001.json      # Structured for automation
│   │   └── results.json       # Performance tracking
│   └── synthesis/
│       └── week_3_quiz.md
└── index.json                  # Master index for programmatic access
```

**Quiz Markdown Format (quiz_001.md):**
```markdown
---
type: quiz
book: Deep Work
chapter: 1
generated: 2025-01-29
from_misses: [retrieval_3, retrieval_7]
dataview: true
---

# Quiz: Deep Work Chapter 1

## Q1: Recall
**Question**: What are the two core abilities for thriving in the new economy?
**Answer**: 1) The ability to quickly master hard things, 2) The ability to produce at an elite level
**Source**: p. 29
**Type**: recall
**Confidence**: _____
**Actual**: _____

## Q2: Application
**Question**: How would you apply the "deep work hypothesis" to your current project?
**Answer**: [Open-ended - evaluate based on proper application of principles]
**Source**: p. 34
**Type**: application
```

### 8. Workflow Validation & Input Preservation

**See full details in:** [OSL Validation Framework](OSL_Validation_Framework.md)

Key validation mechanisms:
- **State Machine Enforcement**: No skipping steps, validates all transitions
- **Verbatim Preservation**: User inputs stored with SHA256 hashes
- **Claude Hooks**: Pre-write validation prevents AI modification
- **Session State Tracking**: Current state, completed steps, pending actions
- **Error Recovery**: Clear messages on what went wrong and how to fix

```python
# Every CLI command validates state first
validation = state_machine.validate_transition(current, target)
if not validation['valid']:
    return error_with_suggestion(validation['error'], validation['suggestion'])

# All user inputs preserved verbatim
preserver.preserve_input('recall', raw_user_text, 'RECALL_ACTIVE')
# Returns hash for verification
```

## Technical Decisions

### Core Architecture Decisions (COMPLETED)
1. ✅ **Framework**: Claude Code as central agentic system
2. ✅ **Commands**: Slash commands for all workflows
3. ✅ **AI Roles**: Subagents for each OSL role
4. ✅ **Storage**: JSON files for state persistence
5. ✅ **Sync**: Git for cross-device synchronization
6. ✅ **Notes**: Direct file manipulation + Obsidian URI
7. ✅ **Flashcards**: JSON format with AnkiConnect sync

### Implementation Decisions (COMPLETED)
1. ✅ **Anki Integration**: Option C (Both AnkiConnect API and .apkg export)
2. ✅ **Session Handling**: Single book per session
3. ✅ **Quiz Storage**: Hybrid markdown + JSON for Obsidian visibility

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