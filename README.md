<div align="center">
<img src="./assets/learny.png" alt="Learny" width="200">
</div>

# Optimized System for Learning (OSL V3)

A research-backed, AI-assisted learning system for comprehension, retention, and transfer.

## Quick Start Guide

### 1. Open Obsidian Vault

1. Open Obsidian
2. Select "Open folder as vault"
3. Navigate to `osl/obsidian/`
4. Start with a new book in `10_books/`

### 2. Configure Anki

1. Install [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on (code: 2055492159)
2. Create a new deck named "OSL::Current"
3. Import settings from `anki/deck_config.json`
4. Enable FSRS scheduler in preferences

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

### Starting a New Book/Topic

1. Create folder: `obsidian/10_books/BookTitle/`
2. Copy session template from `obsidian/90_templates/`
3. Set 3 learning outcomes
4. Write 5 curiosity questions

### Daily Reading Session (~45 min)

1. **Micro-loops** (per 5-10 pages):
   - Pick 1-3 guiding questions
   - Read focused chunk
   - Free recall (1-2 min)
   - Write Feynman explanation
   - Get AI feedback

2. **Capture** (after reading):
   - Create 2-5 permanent notes
   - Add ≤8 high-yield flashcards
   - Update session log

3. **Review** (10-15 min):
   - Complete Anki reviews
   - Export deck after session

### Weekly Tasks

- **Synthesis** (Sun, 60-90 min): Essay + concept map
- **Interleaving** (Tue/Thu, 20-30 min): Mix topics
- **Calibration** (Sun): Test + predictions

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
