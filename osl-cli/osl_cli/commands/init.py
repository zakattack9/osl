"""Initialize OSL directory structure and configuration."""

import json
import click
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from osl_cli.state.schemas import (
    CoachState,
    GovernanceThresholds,
    GovernanceThreshold,
    GovernanceStatus,
)


@click.command(name="init")
@click.option(
    "--path",
    "-p",
    type=click.Path(),
    default=".",
    help="Path where OSL directory will be created",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force initialization even if directory exists",
)
@click.pass_context
def init_command(ctx: click.Context, path: str, force: bool) -> None:
    """Initialize OSL directory structure and configuration.
    
    Creates the following structure:
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
    """
    console: Console = ctx.obj['console']
    
    base_path = Path(path).resolve()
    osl_path = base_path / "osl"
    
    if osl_path.exists() and not force:
        console.print(
            "[red]OSL directory already exists![/red]\n"
            "Use --force to reinitialize (this will preserve existing data)."
        )
        return
    
    console.print(Panel("🎯 Initializing OSL System", style="bold blue"))
    
    # Create directory structure
    directories = [
        osl_path / "obsidian" / "10_books",
        osl_path / "obsidian" / "20_synthesis",
        osl_path / "obsidian" / "30_projects",
        osl_path / "anki",
        osl_path / "ai_state" / "session_logs",
        osl_path / "ai_state" / "memory",
        osl_path / "config",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        console.print(f"✅ Created: {directory.relative_to(base_path)}")
    
    # Create initial coach_state.json with default thresholds
    coach_state_path = osl_path / "ai_state" / "coach_state.json"
    
    if not coach_state_path.exists() or force:
        now = datetime.now()
        
        # Create default governance thresholds
        governance_thresholds = GovernanceThresholds(
            calibration_gate=GovernanceThreshold(
                min=75, current=80, max=85, last_adjusted=now
            ),
            card_debt_multiplier=GovernanceThreshold(
                min=1.5, current=2.0, max=2.5, last_adjusted=now
            ),
            max_new_cards=GovernanceThreshold(
                min=4, current=8, max=10, last_adjusted=now
            ),
            interleaving_per_week=GovernanceThreshold(
                min=1, current=2, max=3, last_adjusted=now
            ),
        )
        
        # Create default governance status
        governance_status = GovernanceStatus(
            calibration_gate="passing",
            card_debt_gate="passing",
            transfer_gate="passing",
            overall_state="NORMAL",
            remediation_active=False,
        )
        
        # Create initial coach state
        coach_state = CoachState(
            version="3.0",
            last_updated=now,
            governance_thresholds=governance_thresholds,
            governance_status=governance_status,
        )
        
        # Write coach state
        with open(coach_state_path, "w") as f:
            json.dump(coach_state.model_dump(mode="json"), f, indent=2, default=str)
        
        console.print(f"✅ Created: {coach_state_path.relative_to(base_path)}")
    
    # Create default config
    config_path = osl_path / "config" / "osl_config.yaml"
    
    if not config_path.exists() or force:
        config_content = """# OSL Configuration
version: "3.0"

# User preferences
user:
  daily_review_time: "07:00"
  timezone: "UTC"
  
# Learning preferences  
learning:
  default_session_duration: 60  # minutes
  micro_loop_size: 5  # pages
  
# AI configuration (optional)
ai:
  provider: null  # openai, anthropic, local
  model: null
  api_key: null  # Set via environment variable OSL_API_KEY
  
# Anki configuration
anki:
  deck_name: "OSL::Default"
  export_format: "apkg"
"""
        config_path.write_text(config_content)
        console.print(f"✅ Created: {config_path.relative_to(base_path)}")
    
    # Display structure tree
    tree = Tree("📚 OSL Directory Structure")
    obsidian = tree.add("📝 obsidian/")
    obsidian.add("📖 10_books/")
    obsidian.add("✍️ 20_synthesis/")
    obsidian.add("🚀 30_projects/")
    tree.add("🎴 anki/")
    ai_state = tree.add("🤖 ai_state/")
    ai_state.add("📊 coach_state.json")
    ai_state.add("📁 session_logs/")
    ai_state.add("🧠 memory/")
    config = tree.add("⚙️ config/")
    config.add("📄 osl_config.yaml")
    
    console.print("\n", tree)
    
    console.print(
        Panel(
            "[green]✨ OSL initialized successfully![/green]\n\n"
            "Next steps:\n"
            "1. Run [cyan]osl session start[/cyan] to begin learning\n"
            "2. Edit [cyan]osl/config/osl_config.yaml[/cyan] to customize settings\n"
            "3. Open [cyan]osl/obsidian[/cyan] in Obsidian for note-taking",
            title="Success",
            style="green",
        )
    )