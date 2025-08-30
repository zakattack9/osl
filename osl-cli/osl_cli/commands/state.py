"""State display command."""

import json
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.json import JSON

from osl_cli.state.manager import StateManager


@click.command(name="state")
@click.argument("target", type=click.Choice(["show", "coach", "session", "path"]))
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def state(ctx: click.Context, target: str, as_json: bool) -> None:
    """Display current learning state.
    
    Targets:
    - show: Overview of all state
    - coach: Coach state details
    - session: Current session details
    - path: Show state file paths
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    if target == "path":
        # Show file paths
        console.print(Panel("📁 OSL State File Paths", style="bold blue"))
        
        tree = Tree("🗂️ State Files")
        tree.add(f"Coach State: {state_manager.coach_state_path}")
        tree.add(f"Current Session: {state_manager.current_session_path}")
        tree.add(f"Session Logs: {state_manager.session_logs_path}/")
        
        console.print(tree)
        return
    
    if target == "show":
        # Overview of all state
        console.print(Panel("📊 OSL State Overview", style="bold blue"))
        
        # Coach state summary
        try:
            coach_state = state_manager.load_coach_state()
            
            table = Table(title="Coach State Summary")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="yellow")
            
            table.add_row("Version", coach_state.version)
            table.add_row("Last Updated", coach_state.last_updated.strftime("%Y-%m-%d %H:%M"))
            table.add_row("Active Books", str(len(coach_state.active_books)))
            table.add_row("Overall Status", coach_state.governance_status.overall_state)
            table.add_row("Total Flashcards", str(coach_state.performance_metrics.total_flashcards))
            table.add_row("Total Notes", str(coach_state.performance_metrics.total_permanent_notes))
            table.add_row("7-Day Retrieval", f"{coach_state.performance_metrics.avg_retrieval_7d:.1f}%")
            
            console.print(table)
        except FileNotFoundError:
            console.print("[red]No coach state found. Run 'osl init' first.[/red]")
        
        # Session state summary
        console.print()
        if state_manager.has_active_session():
            session = state_manager.load_current_session()
            
            table = Table(title="Active Session")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="yellow")
            
            table.add_row("Session ID", session.session_id)
            table.add_row("Book", session.book_title)
            table.add_row("Duration", f"{session.duration_minutes} min")
            table.add_row("State", session.state)
            table.add_row("Micro-loops", str(len(session.micro_loops)))
            table.add_row("Flashcards", f"{session.flashcards_created}/{session.max_flashcards}")
            
            console.print(table)
        else:
            console.print("[yellow]No active session[/yellow]")
    
    elif target == "coach":
        # Detailed coach state
        try:
            coach_state = state_manager.load_coach_state()
            
            if as_json:
                console.print(JSON(json.dumps(coach_state.model_dump(mode="json"), default=str)))
            else:
                console.print(Panel("🤖 Coach State Details", style="bold blue"))
                
                # Active books
                if coach_state.active_books:
                    books_table = Table(title="Active Books")
                    books_table.add_column("Title", style="cyan")
                    books_table.add_column("Author", style="white")
                    books_table.add_column("Progress", style="yellow")
                    books_table.add_column("Sessions", style="green")
                    books_table.add_column("Avg Score", style="magenta")
                    
                    for book in coach_state.active_books:
                        progress = f"{book.current_page}/{book.total_pages}"
                        progress_pct = (book.current_page / book.total_pages * 100) if book.total_pages > 0 else 0
                        books_table.add_row(
                            book.title,
                            book.author,
                            f"{progress} ({progress_pct:.0f}%)",
                            str(book.sessions_completed),
                            f"{book.avg_retrieval_score:.0f}%"
                        )
                    
                    console.print(books_table)
                
                # Governance thresholds
                console.print()
                thresh_table = Table(title="Governance Thresholds")
                thresh_table.add_column("Threshold", style="cyan")
                thresh_table.add_column("Current", style="yellow")
                thresh_table.add_column("Range", style="white")
                
                t = coach_state.governance_thresholds
                thresh_table.add_row("Calibration", f"{t.calibration_gate.current}%", 
                                   f"{t.calibration_gate.min}-{t.calibration_gate.max}%")
                thresh_table.add_row("Card Debt", f"{t.card_debt_multiplier.current}×",
                                   f"{t.card_debt_multiplier.min}×-{t.card_debt_multiplier.max}×")
                thresh_table.add_row("Max Cards", str(int(t.max_new_cards.current)),
                                   f"{int(t.max_new_cards.min)}-{int(t.max_new_cards.max)}")
                thresh_table.add_row("Interleaving", str(int(t.interleaving_per_week.current)),
                                   f"{int(t.interleaving_per_week.min)}-{int(t.interleaving_per_week.max)}")
                
                console.print(thresh_table)
                
                # Performance metrics
                console.print()
                perf_table = Table(title="Performance Metrics")
                perf_table.add_column("Metric", style="cyan")
                perf_table.add_column("Value", style="yellow")
                
                m = coach_state.performance_metrics
                perf_table.add_row("7-Day Avg Retrieval", f"{m.avg_retrieval_7d:.1f}%")
                perf_table.add_row("7-Day Prediction Accuracy", f"{m.avg_prediction_accuracy_7d:.1f}%")
                perf_table.add_row("Card Debt Ratio", f"{m.current_card_debt_ratio:.1f}")
                perf_table.add_row("Cards Due", str(m.cards_due))
                perf_table.add_row("Cards Today", f"{m.cards_completed_today}/{m.daily_review_throughput}")
                perf_table.add_row("Total Flashcards", str(m.total_flashcards))
                perf_table.add_row("Total Notes", str(m.total_permanent_notes))
                perf_table.add_row("Active Misconceptions", str(m.misconceptions_active))
                
                console.print(perf_table)
                
        except FileNotFoundError:
            console.print("[red]No coach state found. Run 'osl init' first.[/red]")
    
    elif target == "session":
        # Detailed session state
        if not state_manager.has_active_session():
            console.print("[yellow]No active session[/yellow]")
            return
        
        session = state_manager.load_current_session()
        
        if as_json:
            console.print(JSON(json.dumps(session.model_dump(mode="json"), default=str)))
        else:
            console.print(Panel("📖 Current Session Details", style="bold blue"))
            
            # Basic info
            info_table = Table(title="Session Info")
            info_table.add_column("Field", style="cyan")
            info_table.add_column("Value", style="yellow")
            
            info_table.add_row("Session ID", session.session_id)
            info_table.add_row("Book", f"{session.book_title} ({session.book_id})")
            info_table.add_row("Type", session.session_type)
            info_table.add_row("State", session.state)
            info_table.add_row("Started", session.start_time.strftime("%H:%M:%S"))
            info_table.add_row("Duration", f"{session.duration_minutes} minutes")
            info_table.add_row("Flashcards", f"{session.flashcards_created}/{session.max_flashcards}")
            
            console.print(info_table)
            
            # Micro-loops
            if session.micro_loops:
                console.print()
                loops_table = Table(title="Micro-loops")
                loops_table.add_column("ID", style="cyan")
                loops_table.add_column("Pages", style="white")
                loops_table.add_column("Score", style="yellow")
                loops_table.add_column("Cards", style="green")
                loops_table.add_column("Status", style="magenta")
                
                for loop in session.micro_loops:
                    status = "Complete" if loop.end_time else "In Progress"
                    score = f"{loop.retrieval_score:.0f}%" if loop.retrieval_score else "N/A"
                    loops_table.add_row(
                        str(loop.loop_id),
                        loop.pages,
                        score,
                        str(len(loop.flashcards_created)),
                        status
                    )
                
                console.print(loops_table)
            
            # Curiosity questions
            if session.curiosity_questions:
                console.print()
                questions_table = Table(title="Curiosity Questions")
                questions_table.add_column("#", style="cyan", width=3)
                questions_table.add_column("Question", style="white")
                questions_table.add_column("Status", style="yellow")
                
                for q in session.curiosity_questions:
                    status = "✅ Resolved" if q.resolved else "❓ Open"
                    questions_table.add_row(str(q.id), q.question, status)
                
                console.print(questions_table)