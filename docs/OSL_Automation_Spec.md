# OSL Automation Specification
_Living document for OSL automation design and implementation_

---

## Table of Contents
1. [Core Philosophy](#core-philosophy)
2. [Script Specifications](#script-specifications)
3. [AI Role Implementation](#ai-role-implementation)
4. [Technical Architecture](#technical-architecture)
5. [Implementation Roadmap](#implementation-roadmap)
6. [Open Questions](#open-questions)

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

## Script Specifications

### 1. `osl` - Master Command Interface

#### Purpose
Single entry point for all OSL operations with context awareness.

#### User Interface
```bash
osl                    # Show dashboard and what's due today
osl start [book]       # Initialize new book
osl session [start|end]# Manage reading sessions  
osl review            # Check what needs review
osl sync              # Sync with Anki
osl coach [role]      # AI assistant interaction
osl stats [period]    # View metrics
osl help [command]    # Get help
```

#### Internal Logic
```python
def main():
    if no_args:
        show_dashboard()
        show_due_items()
        suggest_next_action()
    else:
        route_to_subcommand()
        
def show_dashboard():
    # Load coach_state.json
    # Calculate current metrics
    # Check governance gates
    # Display in formatted table
    
def suggest_next_action():
    # Based on time of day
    # Based on what's overdue
    # Based on current book progress
```

#### Implementation Notes
- Written in Python for complex logic
- Shell wrapper for PATH integration
- Config file for user preferences
- Colorized output for better UX

---

### 2. `osl start` - Book Initialization

#### Purpose
Eliminate friction when starting a new book/topic.

#### User Interface
```bash
osl start                        # Interactive mode
osl start "Deep Work"            # Quick mode with title
osl start "Deep Work" --author "Cal Newport" --pages 296
```

#### Workflow
1. Prompt for book metadata (title, author, pages, ISBN)
2. Create folder structure: `obsidian/10_books/BookName/`
3. Generate pre-filled templates:
   - `book.md` with metadata and sections
   - `YYYY-MM-DD_session.md` for today
   - Empty `notes/permanent/` folder
4. Update `coach_state.json` with new book
5. Calculate suggested reading schedule
6. Open Obsidian to book folder (optional)

#### Template Generation
```markdown
# book.md template
---
title: "{title}"
author: "{author}"
isbn: "{isbn}"
pages: {total_pages}
started: {today}
target_completion: {calculated_date}
status: active
---

## Learning Outcomes
1. [Fill: What specific skill/knowledge do you want?]
2. [Fill: How will you apply this?]
3. [Fill: What problem does this solve?]

## Curiosity Questions
[Pre-reading: What do you wonder about?]
1. 
2. 
3. 
4. 
5. 

## Reading Schedule
- Pages per day: {calculated_pace}
- Review days: Tuesday, Thursday
- Synthesis: Sunday
- Estimated completion: {date}
```

#### State Management
```json
// Addition to coach_state.json
{
  "active_books": [{
    "id": "deep_work_2024",
    "title": "Deep Work",
    "author": "Cal Newport",
    "start_date": "2024-01-15",
    "target_date": "2024-02-15",
    "current_page": 0,
    "total_pages": 296,
    "sessions": [],
    "avg_retrieval": null
  }]
}
```

---

### 3. `osl session` - Session Management

#### Purpose
Track learning sessions without manual bookkeeping.

#### User Interface
```bash
osl session start              # Begin session
osl session end                # End with metrics prompt
osl session pause              # Pause timer
osl session status             # Current session info
osl session abandon            # Cancel without saving
```

#### Session Start Flow
1. Detect current book (from pwd or prompt)
2. Check governance gates - warn if blocked
3. Show any overdue reviews
4. Create new session file from template
5. Start timer (background process)
6. Display: "Session started. Timer running..."

#### Session End Flow
1. Stop timer, calculate duration
2. Prompt for metrics:
   ```
   Pages read: ___
   Retrieval attempts: ___
   Successful recalls (%): ___
   Permanent notes created: ___
   Flashcards created (max 8): ___
   Key misconceptions identified: ___
   ```
3. Validate governance rules
4. Update coach_state.json
5. Calculate next review date
6. Git commit session file (optional)

#### Timer Implementation
```python
# Use subprocess for background timer
import subprocess
import pickle
import time

def start_timer():
    timer_file = '.osl_session_timer'
    start_time = time.time()
    with open(timer_file, 'wb') as f:
        pickle.dump({'start': start_time, 'paused': False}, f)
        
def end_timer():
    # Read timer file
    # Calculate duration
    # Delete timer file
    # Return formatted duration
```

---

### 4. `osl review` - Intelligent Scheduler

#### Purpose
Never wonder what to study next.

#### User Interface
```bash
osl review                    # What's due today
osl review week               # Week ahead view
osl review compliance         # Governance gate status
osl review prescribe          # Get remediation plan
```

#### Daily Review Logic
```python
def get_due_today():
    due_items = []
    
    # Check Anki reviews
    anki_due = get_anki_due_count()
    if anki_due > 0:
        due_items.append(f"📇 {anki_due} cards to review")
    
    # Check interleaving schedule
    if today in ['Tuesday', 'Thursday']:
        due_items.append("🔄 Interleaving session (20-30 min)")
    
    # Check weekly synthesis
    if today == 'Sunday':
        due_items.append("📝 Weekly synthesis essay")
        due_items.append("🧪 Calibration test")
    
    # Check monthly project
    if days_since_last_project() >= 30:
        due_items.append("🎯 Transfer project due")
    
    return due_items
```

#### Governance Gate Checking
```python
def check_governance():
    gates = {
        'calibration': check_calibration_gate(),  # <80% blocks new content
        'card_debt': check_card_debt(),           # >2x blocks new cards
        'transfer': check_transfer_proof()        # Monthly requirement
    }
    
    if any(gate['failing'] for gate in gates.values()):
        return generate_remediation_plan(gates)
```

#### Smart Scheduling
- Detects patterns (e.g., always miss Thursday)
- Adjusts recommendations based on performance
- Suggests lighter days after heavy sessions
- Balances load across the week

---

### 5. `osl sync` - Anki Integration

#### Purpose
Seamless flashcard management across devices.

#### User Interface
```bash
osl sync                     # Two-way sync
osl sync export              # Export only
osl sync import              # Import only
osl sync stats               # Show Anki statistics
```

#### AnkiConnect Integration
```python
import requests
import json

class AnkiConnector:
    def __init__(self):
        self.url = 'http://localhost:8765'
        
    def invoke(self, action, params={}):
        return requests.post(self.url, json={
            'action': action,
            'version': 6,
            'params': params
        }).json()
    
    def export_deck(self, deck_name):
        # Export to osl/anki/exports/
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = f'anki/exports/{deck_name}_{timestamp}.apkg'
        
        return self.invoke('exportPackage', {
            'deck': deck_name,
            'path': path,
            'includeSched': False
        })
    
    def get_stats(self, deck_name):
        return self.invoke('getDeckStats', {'decks': [deck_name]})
    
    def get_due_cards(self):
        return self.invoke('findCards', {'query': 'is:due'})
```

#### Sync Strategy
1. Check if Anki is running
2. Get current deck stats
3. Compare with last sync timestamp
4. Export current deck to timestamped file
5. Update sync_log.json
6. Calculate card debt ratio
7. Update coach_state.json with metrics
8. Optional: git commit the export

---

### 6. `osl coach` - AI Assistant Interface

#### Purpose
Structured AI interactions with proper context and role management.

#### User Interface
```bash
osl coach                    # Interactive mode
osl coach tutor              # Q&A for current reading
osl coach extract            # Create cited outline
osl coach validate           # Check session completeness
osl coach calibrate          # Generate weekly quiz
```

#### Context Management Strategy

##### Automatic Context Loading
```python
def load_context():
    context = {
        'current_book': get_active_book(),
        'recent_sessions': get_last_n_sessions(3),
        'performance_metrics': get_current_metrics(),
        'governance_status': check_governance(),
        'current_misconceptions': get_misconception_list()
    }
    return format_as_prompt(context)
```

##### Role Prompts

**Tutor Role:**
```python
TUTOR_PROMPT = """
You are an OSL Tutor. Your role:
1. Generate 2-3 questions per micro-loop (recall → application → transfer)
2. Provide brief corrective feedback with citations
3. Track missed concepts for flashcard creation
4. Validate understanding without giving away answers

Current context:
{context}

Session rules:
- Questions should progress in difficulty
- Always cite page/location for corrections
- Flag concepts that need flashcards
- End each interaction with: "Key gaps identified: [list]"
"""
```

**Extractor Role:**
```python
EXTRACTOR_PROMPT = """
You are an OSL Extractor. Your ONLY role:
1. Create bullet-point outlines from provided text
2. Include verbatim citations for EVERY point
3. Never paraphrase without quotes
4. Add dependency relationships between concepts

Format:
- Main point [Author, p.X]
  - Supporting detail [p.Y]
  - "Direct quote when important" [p.Z]

Dependencies:
- Concept A requires understanding of Concept B
"""
```

**Coach Role:**
```python
COACH_PROMPT = """
You are an OSL Coach managing learning cadence.

Current state:
{metrics}

Your responsibilities:
1. Monitor governance gates (calibration: {cal}%, debt: {debt}x)
2. Prescribe remediation when gates fail
3. Adjust scheduling based on performance
4. Maintain sustainable pace

When gates trigger:
- Calibration <80%: Prescribe concept review
- Debt >2x: Suspend new cards, focus on review
- Transfer missing: Schedule project time

Be encouraging but firm about maintaining standards.
"""
```

##### Conversation Management
```python
class CoachConversation:
    def __init__(self, role):
        self.role = role
        self.history = []
        self.session_file = f'ai_state/conversations/{date}_{role}.json'
        
    def add_exchange(self, user_msg, ai_response):
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_msg,
            'assistant': ai_response
        })
        self.save()
    
    def get_context_window(self, n=5):
        # Return last n exchanges for context
        return self.history[-n:] if len(self.history) > n else self.history
```

##### API Integration Options

**Option 1: Direct OpenAI/Anthropic API**
```python
import openai

def query_ai(prompt, role_context):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": role_context},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content
```

**Option 2: Local LLM (Ollama)**
```python
import requests

def query_local_llm(prompt, role_context):
    response = requests.post('http://localhost:11434/api/generate', 
        json={
            'model': 'llama2',
            'prompt': f"{role_context}\n\n{prompt}",
            'stream': False
        })
    return response.json()['response']
```

**Option 3: CLI Integration**
```bash
# User manually copies prompt
osl coach tutor --export-prompt
# Pastes to ChatGPT/Claude
# Copies response back
osl coach tutor --import-response
```

---

## Technical Architecture

### Directory Structure
```
osl/
├── bin/                    # Executable scripts
│   ├── osl                # Master command
│   ├── osl-start
│   ├── osl-session
│   ├── osl-review
│   ├── osl-sync
│   └── osl-coach
├── lib/                   # Shared libraries
│   ├── osl_core.py       # Core functions
│   ├── osl_state.py      # State management
│   ├── osl_anki.py       # Anki integration
│   └── osl_ai.py         # AI interfaces
├── config/
│   └── osl_config.yaml   # User configuration
└── var/                   # Runtime data
    ├── session_timer
    └── current_book
```

### State Management

#### Centralized State Store
```python
class OSLState:
    def __init__(self):
        self.state_file = 'ai_state/coach_state.json'
        self.lock_file = 'ai_state/.lock'
        
    def read(self):
        # Implement file locking for concurrent access
        with FileLock(self.lock_file):
            with open(self.state_file) as f:
                return json.load(f)
    
    def update(self, updates):
        with FileLock(self.lock_file):
            state = self.read()
            state.update(updates)
            state['last_updated'] = datetime.now().isoformat()
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
    
    def get_active_book(self):
        # Return currently active book based on recent sessions
        pass
```

### Error Handling

```python
class OSLError(Exception):
    """Base exception for OSL"""
    pass

class GovernanceGateError(OSLError):
    """Raised when governance gate blocks action"""
    def __init__(self, gate, value, threshold):
        self.message = f"Gate '{gate}' failed: {value} vs threshold {threshold}"

class AnkiConnectionError(OSLError):
    """Raised when Anki cannot be reached"""
    pass

def safe_command(func):
    """Decorator for graceful failure"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OSLError as e:
            print(f"❌ {e.message}")
            print("💡 Falling back to manual mode")
            show_manual_instructions()
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("📧 Report at: github.com/user/osl/issues")
    return wrapper
```

### Configuration Management

```yaml
# osl_config.yaml extended
automation:
  auto_commit: true          # Git commit after sessions
  notifications: true        # Desktop notifications
  anki_auto_sync: false     # Requires AnkiConnect
  
ui:
  color_output: true
  emoji_indicators: true
  progress_bars: true
  
ai:
  provider: "openai"        # openai|anthropic|local|manual
  api_key_env: "OPENAI_API_KEY"
  model: "gpt-4"
  temperature: 0.7
  
paths:
  obsidian_command: "open -a Obsidian"  # macOS
  # obsidian_command: "obsidian"        # Linux
  # obsidian_command: "start obsidian"  # Windows
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
**Goal:** Basic workflow automation

1. [ ] Create `osl` master command with dashboard
2. [ ] Implement `osl start` for book initialization
3. [ ] Implement `osl session` for session tracking
4. [ ] Create shared state management library
5. [ ] Add basic error handling

**Testing:**
- Start 2 different books
- Run 5 sessions with metrics
- Verify state persistence

### Phase 2: Intelligence (Week 3-4)
**Goal:** Smart scheduling and governance

1. [ ] Implement `osl review` with due items
2. [ ] Add governance gate checking
3. [ ] Create remediation prescriptions
4. [ ] Add progress visualization
5. [ ] Implement notification system

**Testing:**
- Trigger each governance gate
- Verify remediation plans
- Test across a full week cycle

### Phase 3: Integration (Week 5-6)
**Goal:** External tool integration

1. [ ] Implement `osl sync` with AnkiConnect
2. [ ] Add Anki stats integration
3. [ ] Create `osl coach` framework
4. [ ] Implement AI role prompts
5. [ ] Add conversation management

**Testing:**
- Full Anki round-trip
- Each AI role interaction
- Context window management

### Phase 4: Polish (Week 7-8)
**Goal:** Production ready

1. [ ] Add comprehensive help system
2. [ ] Create installation script
3. [ ] Add configuration wizard
4. [ ] Implement backup/restore
5. [ ] Create user documentation

**Testing:**
- Fresh install on new system
- Migration from manual setup
- Full month simulation

---

## Open Questions

### User Experience
1. Should commands be subcommands (`osl start`) or separate (`osl-start`)?
2. How much interactivity vs command-line flags?
3. Should there be a GUI/TUI option (using something like Rich/Textual)?
4. Notification preference: desktop, terminal, or both?

### AI Integration
1. Which AI provider to prioritize? (OpenAI, Anthropic, local, manual)
2. How to handle API keys securely?
3. Should conversations be stored indefinitely?
4. How to handle rate limits gracefully?
5. Fallback strategy when AI unavailable?

### Data Management
1. How often to auto-backup state?
2. Should we support multiple user profiles?
3. How to handle sync conflicts across devices?
4. Privacy: what data should never be synced/shared?

### Platform Support
1. Priority: macOS, Linux, or Windows?
2. Shell: bash, zsh, or Python-only?
3. Package distribution: pip, homebrew, or manual?
4. Mobile companion app feasibility?

### Integration Points
1. Obsidian plugin vs external scripts?
2. Direct Anki database access vs AnkiConnect?
3. Calendar integration for scheduling?
4. Export formats for learning portfolio?

### Governance Tuning
1. Should thresholds be adaptive based on user performance?
2. How to handle different difficulty levels of material?
3. Should there be a "vacation mode"?
4. How strict should the system be with beginners?

---

## Next Steps

1. **Review and refine** this specification
2. **Prioritize features** based on your workflow
3. **Choose technology decisions** (AI provider, platform priority)
4. **Create proof-of-concept** for highest-impact script
5. **Test with real learning sessions**
6. **Iterate based on experience**

---

## Notes Section
_Use this space to capture thoughts, decisions, and iterations as you develop the system._

### Decision Log
- 

### Ideas Parking Lot
- 

### Rejected Features (and why)
- 