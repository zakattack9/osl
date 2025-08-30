"""Curiosity question tracking commands."""

import click
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt

from osl_cli.state.schemas import CuriosityQuestion, SessionState
from osl_cli.state.manager import StateManager


@click.group(name="questions")
@click.pass_context
def questions_group(ctx: click.Context) -> None:
    """Manage curiosity questions."""
    pass


@questions_group.command(name="add")
@click.option("--question", "-q", help="Your curiosity question")
@click.pass_context
def add_question(ctx: click.Context, question: Optional[str]) -> None:
    """Add a curiosity question.
    
    Curiosity questions:
    - Drive focused reading
    - Guide attention during sessions
    - Should be genuine questions you want answered
    - Maximum 5 per session
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    if not state_manager.has_active_session():
        console.print("[red]No active session![/red]")
        console.print("Start a session first: [cyan]osl session start[/cyan]")
        return
    
    session = state_manager.load_current_session()
    
    # Check question limit
    if len(session.curiosity_questions) >= 5:
        console.print("[yellow]⚠️ Maximum 5 curiosity questions per session[/yellow]")
        console.print("Focus on your existing questions:")
        for q in session.curiosity_questions:
            status = "✓" if q.resolved else "○"
            console.print(f"  {status} {q.question}")
        return
    
    # Get question if not provided
    if not question:
        console.print("[cyan]What are you curious about?[/cyan]")
        question = Prompt.ask("Question")
    
    # Create question
    new_question = CuriosityQuestion(
        id=len(session.curiosity_questions) + 1,
        question=question,
        created=datetime.now()
    )
    
    session.curiosity_questions.append(new_question)
    state_manager.save_current_session(session)
    
    console.print(
        Panel(
            f"[green]❓ Question added![/green]\n\n"
            f"[cyan]Question {new_question.id}:[/cyan] {question}\n\n"
            f"You have {len(session.curiosity_questions)}/5 questions for this session",
            style="green"
        )
    )


@questions_group.command(name="list")
@click.option("--all", "-a", is_flag=True, help="Show resolved questions too")
@click.pass_context
def list_questions(ctx: click.Context, all: bool) -> None:
    """List curiosity questions for current session.
    
    Shows:
    - Active (unresolved) questions by default
    - All questions with --all flag
    - Resolution status and page found
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    if not state_manager.has_active_session():
        console.print("[red]No active session![/red]")
        return
    
    session = state_manager.load_current_session()
    
    if not session.curiosity_questions:
        console.print("[yellow]No curiosity questions yet![/yellow]")
        console.print("Add questions with: [cyan]osl questions add[/cyan]")
        return
    
    # Filter questions
    questions = session.curiosity_questions
    if not all:
        questions = [q for q in questions if not q.resolved]
        if not questions:
            console.print("[yellow]All questions resolved![/yellow]")
            console.print("Use [cyan]--all[/cyan] to see resolved questions")
            return
    
    table = Table(title="❓ Curiosity Questions", show_header=True)
    table.add_column("ID", style="cyan", width=4)
    table.add_column("Question", style="white")
    table.add_column("Status", justify="center", width=10)
    table.add_column("Page", justify="center", width=8)
    table.add_column("Created", style="dim", width=12)
    
    for q in questions:
        status = "[green]✓ Resolved[/green]" if q.resolved else "[yellow]○ Active[/yellow]"
        page = str(q.page_found) if q.page_found else "—"
        created = q.created.strftime("%H:%M")
        
        table.add_row(
            str(q.id),
            q.question[:60] + "..." if len(q.question) > 60 else q.question,
            status,
            page,
            created
        )
    
    console.print(table)


@questions_group.command(name="resolve")
@click.argument("question_id", type=int)
@click.option("--page", "-p", type=int, help="Page where answer was found")
@click.option("--answer", "-a", help="Brief answer summary")
@click.pass_context
def resolve_question(ctx: click.Context, question_id: int, page: Optional[int], answer: Optional[str]) -> None:
    """Mark a curiosity question as resolved.
    
    Records:
    - Page where answer was found
    - Brief answer summary
    - Resolution timestamp
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    if not state_manager.has_active_session():
        console.print("[red]No active session![/red]")
        return
    
    session = state_manager.load_current_session()
    
    # Find question
    question = None
    for q in session.curiosity_questions:
        if q.id == question_id:
            question = q
            break
    
    if not question:
        console.print(f"[red]Question {question_id} not found![/red]")
        return
    
    if question.resolved:
        console.print(f"[yellow]Question {question_id} already resolved![/yellow]")
        return
    
    # Get page if not provided
    if page is None:
        page = IntPrompt.ask("On what page did you find the answer?")
    
    # Get answer summary if not provided
    if not answer:
        console.print("[cyan]Briefly summarize the answer:[/cyan]")
        answer = Prompt.ask("Answer")
    
    # Update question
    question.resolved = True
    question.page_found = page
    question.answer = answer
    question.resolved_at = datetime.now()
    
    state_manager.save_current_session(session)
    
    console.print(
        Panel(
            f"[green]✓ Question resolved![/green]\n\n"
            f"[cyan]Question:[/cyan] {question.question}\n"
            f"[cyan]Answer:[/cyan] {answer}\n"
            f"[cyan]Found on page:[/cyan] {page}",
            style="green"
        )
    )
    
    # Show remaining questions
    unresolved = [q for q in session.curiosity_questions if not q.resolved]
    if unresolved:
        console.print(f"\n[cyan]Remaining questions ({len(unresolved)}):[/cyan]")
        for q in unresolved:
            console.print(f"  {q.id}. {q.question}")


@questions_group.command(name="review")
@click.pass_context
def review_questions(ctx: click.Context) -> None:
    """Review all questions and their resolution status.
    
    Provides:
    - Summary of resolved vs unresolved
    - Questions that drove learning
    - Patterns in your curiosity
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    if not state_manager.has_active_session():
        console.print("[red]No active session![/red]")
        return
    
    session = state_manager.load_current_session()
    
    if not session.curiosity_questions:
        console.print("[yellow]No curiosity questions in this session![/yellow]")
        return
    
    resolved = [q for q in session.curiosity_questions if q.resolved]
    unresolved = [q for q in session.curiosity_questions if not q.resolved]
    
    console.print(
        Panel(
            f"[bold cyan]📊 Question Review[/bold cyan]\n\n"
            f"[cyan]Total Questions:[/cyan] {len(session.curiosity_questions)}\n"
            f"[green]Resolved:[/green] {len(resolved)}\n"
            f"[yellow]Unresolved:[/yellow] {len(unresolved)}\n",
            style="cyan"
        )
    )
    
    if resolved:
        console.print("\n[bold green]✓ Resolved Questions:[/bold green]")
        for q in resolved:
            console.print(f"\n  [cyan]Q{q.id}:[/cyan] {q.question}")
            console.print(f"  [dim]Answer:[/dim] {q.answer}")
            console.print(f"  [dim]Page:[/dim] {q.page_found}")
    
    if unresolved:
        console.print("\n[bold yellow]○ Unresolved Questions:[/bold yellow]")
        for q in unresolved:
            console.print(f"\n  [cyan]Q{q.id}:[/cyan] {q.question}")
            console.print(f"  [dim]Consider researching this further[/dim]")