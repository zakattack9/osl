"""Misconception tracking and resolution commands."""

import click
from datetime import datetime
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

from osl_cli.state.manager import StateManager


@click.group(name="misconception")
@click.pass_context
def misconception_group(ctx: click.Context) -> None:
    """Track and resolve learning misconceptions."""
    pass


@misconception_group.command(name="add")
@click.option("--description", "-d", help="Description of the misconception")
@click.option("--source", "-s", help="Where the error occurred (page/topic)")
@click.pass_context
def add_misconception(ctx: click.Context, description: Optional[str], source: Optional[str]) -> None:
    """Record a misconception identified during learning.
    
    Misconceptions are:
    - Errors in understanding discovered through retrieval
    - Incorrect assumptions revealed by AI questions
    - Gaps identified during self-explanation
    
    Recording helps target future review.
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    if not state_manager.has_active_session():
        console.print("[red]No active session![/red]")
        console.print("Start a session first: [cyan]osl session start[/cyan]")
        return
    
    session = state_manager.load_current_session()
    
    # Get description if not provided
    if not description:
        console.print("[cyan]Describe the misconception:[/cyan]")
        description = Prompt.ask("What did you misunderstand")
    
    # Get source if not provided
    if not source:
        source = Prompt.ask("Where did this occur (page/topic)", default=f"Page {session.micro_loops[-1].pages if session.micro_loops else 'unknown'}")
    
    # Create misconception ID
    misconception_id = f"misc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Create misconception data
    misconception = {
        "misconception_id": misconception_id,
        "identified_at": datetime.now().isoformat(),
        "during_loop": len(session.micro_loops),
        "description": description,
        "source": source,
        "resolved": False
    }
    
    # Add to session (we'll store in a list for now)
    if not hasattr(session, 'misconceptions_identified'):
        session.misconceptions_identified = []
    session.misconceptions_identified.append(misconception)
    
    # Update metrics
    coach_state = state_manager.load_coach_state()
    coach_state.performance_metrics.misconceptions_active += 1
    
    state_manager.save_current_session(session)
    state_manager.save_coach_state(coach_state)
    
    console.print(
        Panel(
            f"[yellow]⚠️ Misconception recorded[/yellow]\n\n"
            f"[cyan]ID:[/cyan] {misconception_id}\n"
            f"[cyan]Description:[/cyan] {description}\n"
            f"[cyan]Source:[/cyan] {source}\n\n"
            f"This will be targeted in future reviews",
            style="yellow"
        )
    )


@misconception_group.command(name="list")
@click.option("--all", "-a", is_flag=True, help="Show resolved misconceptions too")
@click.pass_context
def list_misconceptions(ctx: click.Context, all: bool) -> None:
    """List misconceptions from current session.
    
    Shows:
    - Active misconceptions that need resolution
    - Source and description
    - When they were identified
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    if not state_manager.has_active_session():
        console.print("[red]No active session![/red]")
        return
    
    session = state_manager.load_current_session()
    
    if not hasattr(session, 'misconceptions_identified') or not session.misconceptions_identified:
        console.print("[green]No misconceptions identified—great work![/green]")
        return
    
    # Filter misconceptions
    misconceptions = session.misconceptions_identified
    if not all:
        misconceptions = [m for m in misconceptions if not m.get('resolved', False)]
        if not misconceptions:
            console.print("[green]All misconceptions resolved![/green]")
            console.print("Use [cyan]--all[/cyan] to see resolved ones")
            return
    
    table = Table(title="⚠️ Misconceptions", show_header=True)
    table.add_column("ID", style="yellow", width=20)
    table.add_column("Description", style="white")
    table.add_column("Source", style="dim", width=15)
    table.add_column("Status", justify="center", width=10)
    table.add_column("Loop", justify="center", width=6)
    
    for m in misconceptions:
        status = "[green]✓[/green]" if m.get('resolved', False) else "[yellow]○[/yellow]"
        desc = m['description'][:50] + "..." if len(m['description']) > 50 else m['description']
        
        table.add_row(
            m['misconception_id'],
            desc,
            m['source'],
            status,
            str(m.get('during_loop', '—'))
        )
    
    console.print(table)


@misconception_group.command(name="resolve")
@click.argument("misconception_id")
@click.option("--correction", "-c", help="How you corrected the misconception")
@click.option("--flashcard", "-f", is_flag=True, help="Create flashcard for this")
@click.pass_context
def resolve_misconception(ctx: click.Context, misconception_id: str, correction: Optional[str], flashcard: bool) -> None:
    """Mark a misconception as resolved.
    
    Records:
    - How you corrected your understanding
    - Whether a flashcard was created
    - Resolution timestamp
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    if not state_manager.has_active_session():
        console.print("[red]No active session![/red]")
        return
    
    session = state_manager.load_current_session()
    
    if not hasattr(session, 'misconceptions_identified'):
        console.print("[yellow]No misconceptions recorded![/yellow]")
        return
    
    # Find misconception
    misconception = None
    for m in session.misconceptions_identified:
        if m['misconception_id'] == misconception_id:
            misconception = m
            break
    
    if not misconception:
        console.print(f"[red]Misconception '{misconception_id}' not found![/red]")
        return
    
    if misconception.get('resolved', False):
        console.print(f"[yellow]Misconception already resolved![/yellow]")
        return
    
    # Get correction if not provided
    if not correction:
        console.print(f"\n[cyan]Original misconception:[/cyan] {misconception['description']}")
        console.print("\n[cyan]How did you correct this understanding?[/cyan]")
        correction = Prompt.ask("Correction")
    
    # Update misconception
    misconception['resolved'] = True
    misconception['resolved_at'] = datetime.now().isoformat()
    misconception['correction'] = correction
    misconception['flashcard_created'] = flashcard
    
    # Update metrics
    coach_state = state_manager.load_coach_state()
    coach_state.performance_metrics.misconceptions_active -= 1
    coach_state.performance_metrics.misconceptions_resolved += 1
    
    state_manager.save_current_session(session)
    state_manager.save_coach_state(coach_state)
    
    console.print(
        Panel(
            f"[green]✓ Misconception resolved![/green]\n\n"
            f"[cyan]Original:[/cyan] {misconception['description']}\n"
            f"[cyan]Correction:[/cyan] {correction}\n"
            f"[cyan]Flashcard:[/cyan] {'Yes' if flashcard else 'No'}",
            style="green"
        )
    )
    
    if flashcard:
        console.print("\n[cyan]Remember to create a flashcard with:[/cyan]")
        console.print("[bold]osl flashcard create[/bold]")


@misconception_group.command(name="review")
@click.pass_context
def review_misconceptions(ctx: click.Context) -> None:
    """Review all misconceptions for pattern recognition.
    
    Helps identify:
    - Recurring error patterns
    - Topics needing more attention
    - Progress in understanding
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    
    console.print(
        Panel(
            f"[bold cyan]📊 Misconception Overview[/bold cyan]\n\n"
            f"[yellow]Active:[/yellow] {coach_state.performance_metrics.misconceptions_active}\n"
            f"[green]Resolved:[/green] {coach_state.performance_metrics.misconceptions_resolved}\n"
            f"[cyan]Total:[/cyan] {coach_state.performance_metrics.misconceptions_active + coach_state.performance_metrics.misconceptions_resolved}",
            style="cyan"
        )
    )
    
    if not state_manager.has_active_session():
        console.print("\n[dim]Start a session to track misconceptions[/dim]")
        return
    
    session = state_manager.load_current_session()
    
    if not hasattr(session, 'misconceptions_identified') or not session.misconceptions_identified:
        console.print("\n[green]No misconceptions in current session—excellent![/green]")
        return
    
    # Group by status
    active = [m for m in session.misconceptions_identified if not m.get('resolved', False)]
    resolved = [m for m in session.misconceptions_identified if m.get('resolved', False)]
    
    if active:
        console.print("\n[bold yellow]⚠️ Active Misconceptions:[/bold yellow]")
        for m in active:
            console.print(f"\n  [yellow]{m['misconception_id']}[/yellow]")
            console.print(f"  {m['description']}")
            console.print(f"  [dim]Source: {m['source']}[/dim]")
    
    if resolved:
        console.print("\n[bold green]✓ Resolved Misconceptions:[/bold green]")
        for m in resolved:
            console.print(f"\n  [green]{m['misconception_id']}[/green]")
            console.print(f"  [s]{m['description']}[/s]")
            console.print(f"  [cyan]→ {m.get('correction', 'Corrected')}[/cyan]")
            if m.get('flashcard_created'):
                console.print(f"  [dim]📇 Flashcard created[/dim]")