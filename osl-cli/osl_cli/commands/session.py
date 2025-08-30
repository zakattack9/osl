"""Session management commands."""

import json
import click
from pathlib import Path
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

from osl_cli.state.schemas import SessionState, CoachState, BookState
from osl_cli.governance.gates import GovernanceChecker
from osl_cli.state.manager import StateManager


@click.group(name="session")
@click.pass_context
def session_group(ctx: click.Context) -> None:
    """Manage learning sessions."""
    pass


@session_group.command(name="start")
@click.option("--book", "-b", help="Book ID or title to study")
@click.option("--type", "-t", 
              type=click.Choice(["standard", "interleaving", "review", "calibration"]),
              default="standard",
              help="Session type")
@click.pass_context
def start_session(ctx: click.Context, book: Optional[str], type: str) -> None:
    """Begin a new learning session with governance checks.
    
    Performs the following:
    1. Checks all governance gates
    2. Loads or creates book context
    3. Initializes session state
    4. Prompts for curiosity questions
    """
    console: Console = ctx.obj['console']
    
    # Initialize state manager
    state_manager = StateManager()
    
    # Check if session already active
    if state_manager.has_active_session():
        console.print("[yellow]⚠️ Session already active![/yellow]")
        console.print("Run [cyan]osl session end[/cyan] to close current session first.")
        return
    
    # Load coach state
    coach_state = state_manager.load_coach_state()
    
    # Run governance checks
    console.print(Panel("🔍 Running Governance Checks", style="bold blue"))
    
    checker = GovernanceChecker(coach_state)
    gates_status = checker.check_all_gates()
    
    # Display governance status
    table = Table(title="Governance Gate Status")
    table.add_column("Gate", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Value", style="yellow")
    table.add_column("Threshold", style="white")
    
    for gate_name, status in gates_status.items():
        status_emoji = "✅" if status["passing"] else "❌"
        table.add_row(
            gate_name,
            f"{status_emoji} {status['status']}",
            str(status.get("current_value", "N/A")),
            str(status.get("threshold", "N/A"))
        )
    
    console.print(table)
    
    # Check for blocking conditions
    if coach_state.governance_status.overall_state == "BLOCKED":
        console.print(
            Panel(
                "[red]❌ Cannot start session - governance gates failing![/red]\n"
                "Address the failing gates before continuing.",
                style="red"
            )
        )
        return
    
    # Handle book selection
    if not book and not coach_state.active_books:
        # No active books, need to add one
        console.print("\n[yellow]No active books found.[/yellow]")
        add_new = Confirm.ask("Would you like to add a new book?")
        
        if add_new:
            book_title = Prompt.ask("Book title")
            book_author = Prompt.ask("Author")
            total_pages = int(Prompt.ask("Total pages"))
            
            new_book = BookState(
                id=book_title.lower().replace(" ", "_") + "_" + datetime.now().strftime("%Y"),
                title=book_title,
                author=book_author,
                start_date=datetime.now(),
                current_page=0,
                total_pages=total_pages,
            )
            
            coach_state.active_books.append(new_book)
            state_manager.save_coach_state(coach_state)
            book = new_book.id
        else:
            console.print("[red]Cannot start session without a book.[/red]")
            return
    
    elif not book:
        # Select from active books
        if len(coach_state.active_books) == 1:
            book = coach_state.active_books[0].id
        else:
            console.print("\n[cyan]Active Books:[/cyan]")
            for i, b in enumerate(coach_state.active_books, 1):
                console.print(f"{i}. {b.title} by {b.author} (p.{b.current_page}/{b.total_pages})")
            
            choice = Prompt.ask("Select book number", choices=[str(i) for i in range(1, len(coach_state.active_books) + 1)])
            book = coach_state.active_books[int(choice) - 1].id
    
    # Find selected book
    selected_book = next((b for b in coach_state.active_books if b.id == book), None)
    
    if not selected_book:
        console.print(f"[red]Book '{book}' not found![/red]")
        return
    
    # Create session state
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    session = SessionState(
        session_id=session_id,
        book_id=selected_book.id,
        book_title=selected_book.title,
        start_time=datetime.now(),
        last_activity=datetime.now(),
        session_type=type,
        governance_gates_checked=True,
        gates_status={k: v["status"] for k, v in gates_status.items()},
    )
    
    # Save session state
    state_manager.save_current_session(session)
    
    # Display session start info
    console.print(
        Panel(
            f"[green]✨ Session Started![/green]\n\n"
            f"📖 Book: {selected_book.title}\n"
            f"👤 Author: {selected_book.author}\n"
            f"📄 Current Page: {selected_book.current_page}\n"
            f"🎯 Session Type: {type}\n"
            f"🆔 Session ID: {session_id}\n\n"
            f"[cyan]Next: Generate 5 curiosity questions about what you'll read[/cyan]",
            title="Session Active",
            style="green"
        )
    )
    
    # Prompt for curiosity questions
    console.print("\n[bold]Generate 5 curiosity questions:[/bold]")
    console.print("[dim]What do you want to learn from this reading?[/dim]\n")
    
    for i in range(1, 6):
        question = Prompt.ask(f"Question {i}")
        # Note: In full implementation, these would be saved to session state


@session_group.command(name="end")
@click.pass_context
def end_session(ctx: click.Context) -> None:
    """Close current session and update state.
    
    Performs the following:
    1. Saves session metrics
    2. Updates coach state
    3. Archives session log
    4. Checks governance gates
    """
    console: Console = ctx.obj['console']
    
    state_manager = StateManager()
    
    # Check for active session
    if not state_manager.has_active_session():
        console.print("[yellow]No active session to end.[/yellow]")
        return
    
    # Load current session
    session = state_manager.load_current_session()
    coach_state = state_manager.load_coach_state()
    
    # Calculate session metrics
    end_time = datetime.now()
    duration = (end_time - session.start_time).total_seconds() / 60
    
    # Update session
    session.last_activity = end_time
    session.duration_minutes = int(duration)
    session.state = "SESSION_END"
    
    # Display session summary
    console.print(Panel("📊 Session Summary", style="bold blue"))
    
    table = Table()
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="yellow")
    
    table.add_row("Duration", f"{session.duration_minutes} minutes")
    table.add_row("Micro-loops Completed", str(len(session.micro_loops)))
    table.add_row("Flashcards Created", f"{session.flashcards_created}/{session.max_flashcards}")
    table.add_row("Curiosity Questions", f"{len(session.curiosity_questions)}")
    
    if session.retrieval_scores:
        avg_score = sum(session.retrieval_scores) / len(session.retrieval_scores)
        table.add_row("Avg Retrieval Score", f"{avg_score:.1f}%")
    
    console.print(table)
    
    # Update book progress
    book = next((b for b in coach_state.active_books if b.id == session.book_id), None)
    if book:
        book.sessions_completed += 1
        book.total_hours += duration / 60
        book.last_session = end_time
        
        if session.retrieval_scores:
            # Update rolling average
            new_avg = sum(session.retrieval_scores) / len(session.retrieval_scores)
            if book.avg_retrieval_score == 0:
                book.avg_retrieval_score = new_avg
            else:
                # Weighted average favoring recent sessions
                book.avg_retrieval_score = (book.avg_retrieval_score * 0.7) + (new_avg * 0.3)
    
    # Update coach state metrics
    coach_state.performance_metrics.cards_completed_today += session.flashcards_created
    coach_state.last_updated = end_time
    
    # Archive session
    state_manager.archive_session(session)
    
    # Save updated coach state
    state_manager.save_coach_state(coach_state)
    
    # Clear current session
    state_manager.clear_current_session()
    
    # Final governance check
    checker = GovernanceChecker(coach_state)
    gates_status = checker.check_all_gates()
    
    if any(not status["passing"] for status in gates_status.values()):
        console.print(
            Panel(
                "[yellow]⚠️ Some governance gates need attention![/yellow]\n"
                "Run [cyan]osl governance check[/cyan] for details.",
                style="yellow"
            )
        )
    
    console.print(
        Panel(
            "[green]✅ Session ended successfully![/green]\n\n"
            f"Session archived: {session.session_id}\n"
            f"Total learning time today: {coach_state.performance_metrics.cards_completed_today} cards",
            style="green"
        )
    )