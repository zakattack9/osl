# OSL CLI - Optimized System for Learning

Command-line interface for the OSL learning system, enforcing research-backed learning practices.

## Installation

```bash
# From the osl-cli directory
pip install -e .

# Or for development with test dependencies
pip install -e ".[dev]"
```

## Quick Start

```bash
# Initialize OSL directory structure
osl init

# Start a learning session
osl session start

# Complete a micro-loop
osl microloop start --pages "45-50"
# ... read the pages ...
osl microloop complete

# Create flashcards from your gaps
osl flashcard create

# End session
osl session end

# Check governance gates
osl governance check

# View current state
osl state show
```

## Core Commands

### `osl init`
Initialize OSL directory structure and configuration files.

### `osl session start/end`
Manage learning sessions with governance gate checks.

### `osl microloop start/complete`
Track micro-loop cycles (read → recall → explain → feedback).

### `osl flashcard create`
Create learner-authored flashcards (generation effect protection).

### `osl quiz generate`
Generate weekly calibration quiz (AI-assisted).

### `osl governance check/tune`
Check governance gates and tune thresholds.

### `osl state show`
Display current learning state and metrics.

## Key Principles

1. **Generation Effect**: YOU must author all flashcards
2. **Testing Effect**: AI questions only AFTER free recall
3. **Governance Gates**: Adaptive thresholds enforce quality
4. **Verbatim Storage**: Your exact words are preserved

## Governance Gates

- **Calibration Gate**: 75-85% retrieval accuracy
- **Card Debt Gate**: 1.5×-2.5× daily throughput
- **Transfer Gate**: Project per completed book
- **Interleaving**: 30-50% of sessions

## Directory Structure

```
osl/
├── obsidian/           # Notes vault
│   ├── 10_books/       # Per-book workspaces  
│   ├── 20_synthesis/   # Weekly essays
│   └── 30_projects/    # Transfer artifacts
├── anki/               # Flashcard exports
├── ai_state/           # State management
│   ├── coach_state.json
│   ├── session_logs/
│   └── memory/
└── config/             # User configuration
    └── osl_config.yaml
```

## Development

```bash
# Run tests
python -m pytest tests/

# Format code
black osl_cli/

# Lint code
ruff osl_cli/

# Type check
mypy osl_cli/
```

## Documentation

See `/docs/` directory for complete OSL documentation:
- `README.md` - Implementation guide
- `V3_Core.md` - Core methodology
- `OSL_AI_Boundaries.md` - AI interaction rules
- `OSL_Flashcard_Philosophy.md` - Generation effect protection