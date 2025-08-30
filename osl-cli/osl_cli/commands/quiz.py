"""Quiz generation command - weekly calibration only."""

import click
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from osl_cli.state.manager import StateManager


@click.command(name="quiz")
@click.argument("action", type=click.Choice(["generate", "schedule"]))
@click.pass_context
def quiz(ctx: click.Context, action: str) -> None:
    """Generate calibration quiz (weekly only).
    
    Weekly calibration quiz:
    - 6-10 AI-generated items
    - Tests understanding and retention
    - Provides prediction vs actual performance data
    
    Structure:
    - 3 recall items (facts/definitions)
    - 3-4 application items (scenarios)
    - 2-3 transfer items (new contexts)
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    
    if action == "generate":
        # Check if it's time for weekly quiz
        next_calibration = coach_state.review_schedule.next_calibration
        
        if next_calibration and datetime.now() < next_calibration:
            days_until = (next_calibration - datetime.now()).days
            console.print(
                Panel(
                    f"[yellow]⏰ Not time for calibration quiz yet![/yellow]\n\n"
                    f"Next calibration: {next_calibration.strftime('%Y-%m-%d')}\n"
                    f"Days remaining: {days_until}\n\n"
                    "[cyan]Calibration quizzes are weekly to measure retention.[/cyan]",
                    style="yellow"
                )
            )
            return
        
        console.print(
            Panel(
                "📝 Weekly Calibration Quiz\n\n"
                "[bold]Purpose:[/bold] Measure actual vs predicted performance\n\n"
                "[cyan]In full implementation, AI would generate:[/cyan]\n"
                "• 3 recall questions (facts from the week)\n"
                "• 3-4 application questions (use concepts)\n"
                "• 2-3 transfer questions (new contexts)\n\n"
                "You would:\n"
                "1. Predict your score\n"
                "2. Take the quiz\n"
                "3. Compare actual vs predicted\n"
                "4. Identify calibration gaps",
                style="bold blue"
            )
        )
        
        # Simulate quiz blueprint
        table = Table(title="Quiz Blueprint")
        table.add_column("Type", style="cyan")
        table.add_column("Count", style="yellow")
        table.add_column("Example", style="white")
        
        table.add_row(
            "Recall",
            "3",
            "What is the 4-hour limit for?"
        )
        table.add_row(
            "Application", 
            "4",
            "How would you apply deep work to coding?"
        )
        table.add_row(
            "Transfer",
            "3",
            "How might deep work principles apply to painting?"
        )
        
        console.print(table)
        
        # Update next calibration date
        coach_state.review_schedule.next_calibration = datetime.now() + timedelta(days=7)
        state_manager.save_coach_state(coach_state)
        
        console.print(
            "\n[green]Quiz framework ready![/green]\n"
            "[dim](In full implementation, AI would generate actual questions)[/dim]"
        )
    
    elif action == "schedule":
        # Show quiz schedule
        schedule = coach_state.review_schedule
        
        console.print(Panel("📅 Quiz Schedule", style="bold blue"))
        
        table = Table()
        table.add_column("Activity", style="cyan")
        table.add_column("Next Date", style="yellow")
        table.add_column("Frequency", style="white")
        
        if schedule.next_calibration:
            table.add_row(
                "Calibration Quiz",
                schedule.next_calibration.strftime("%Y-%m-%d"),
                "Weekly"
            )
        
        if schedule.next_synthesis:
            table.add_row(
                "Synthesis Essay",
                schedule.next_synthesis.strftime("%Y-%m-%d") if schedule.next_synthesis else "Not scheduled",
                "Weekly"
            )
        
        if schedule.next_interleaving:
            table.add_row(
                "Interleaving Session",
                schedule.next_interleaving.strftime("%Y-%m-%d") if schedule.next_interleaving else "Not scheduled",
                "2-3x/week"
            )
        
        console.print(table)