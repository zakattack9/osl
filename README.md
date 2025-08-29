# Optimized System for Learning (OSL V3)

A research-backed, AI-assisted learning system for comprehension, retention, and transfer.

## Quick Start

### 1. Setup Folder Structure

```bash
# Clone this repository
git clone <your-repo-url> osl
cd osl

# Create directory structure
mkdir -p obsidian/{00_inbox,10_books,20_synthesis,30_projects_transfer,90_templates}
mkdir -p anki/{exports,media}
mkdir -p ai_state/{session_logs,memory,archive}
mkdir -p scripts config/templates

# Move docs to proper location
mkdir -p docs
mv "V3 Core.md" docs/V3_Core.md
mv "V3 Implementation Guide.md" docs/V3_Implementation_Guide.md
```

### 2. Configure Obsidian

1. Open Obsidian
2. Select "Open folder as vault"
3. Navigate to `osl/obsidian/`
4. Obsidian will create `.obsidian/` folder automatically

### 3. Configure Anki

1. Install [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on (code: 2055492159)
2. Export existing decks to `osl/anki/exports/`
3. Import decks from this location when needed

## Folder Structure

```
osl/
├── docs/                    # Core documentation
├── obsidian/               # Your Obsidian vault
├── anki/                   # Anki deck exports
├── ai_state/               # AI coaching state
├── scripts/                # Automation examples
└── config/                 # Configuration files
```

## Core Documents

- **[V3 Core](docs/V3_Core.md)** - The complete OSL system principles and workflow
- **[V3 Implementation Guide](docs/V3_Implementation_Guide.md)** - Detailed setup, templates, and tools

## Key Features

- **Micro-loops**: Active recall cycles (Question → Read → Retrieve → Explain → Feedback)
- **Spaced repetition**: Anki integration with ≤8 new cards per session
- **AI coaching**: Structured state management for continuity
- **Git-controlled**: Version control for all learning materials
- **Portable**: Single folder contains entire learning system

## Daily Workflow

1. **Reading Session** (~45 min)
   - Set learning intent
   - Run micro-loops on 5-10 pages
   - Create permanent notes
   - Add ≤8 flashcards

2. **Spaced Reviews** (10-15 min)
   - Review Anki cards
   - Export deck to `anki/exports/` after session

3. **Weekly Synthesis** (60-90 min)
   - Calibration test
   - Write synthesis essay
   - Update concept maps

## Git Backup

```bash
# Daily backup
git add -A
git commit -m "OSL backup $(date +%Y-%m-%d)"
git push origin main  # If using remote
```

## Configuration

Edit `osl_config.yaml` to customize:
- Governance thresholds (calibration gate, card debt)
- File paths
- Anki settings

## Support

See the [Implementation Guide](docs/V3_Implementation_Guide.md) for:
- Detailed setup instructions (Section N)
- Obsidian templates (Section A)
- Anki configuration (Section B)
- AI role prompts (Section C)
- Troubleshooting (Section L)