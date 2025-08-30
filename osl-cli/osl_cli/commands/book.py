"""Book management commands."""

import click
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt

from osl_cli.state.schemas import BookState, CoachState
from osl_cli.state.manager import StateManager


@click.group(name="book")
@click.pass_context
def book_group(ctx: click.Context) -> None:
    """Manage books in your learning system."""
    pass


@book_group.command(name="add")
@click.option("--title", "-t", help="Book title")
@click.option("--author", "-a", help="Book author")
@click.option("--pages", "-p", type=int, help="Total pages")
@click.pass_context
def add_book(ctx: click.Context, title: Optional[str], author: Optional[str], pages: Optional[int]) -> None:
    """Add a new book to study.
    
    Creates a book entry with:
    - Title and author
    - Total page count
    - Unique ID for tracking
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    # Prompt for missing information
    if not title:
        title = Prompt.ask("Book title")
    if not author:
        author = Prompt.ask("Author")
    if not pages:
        pages = IntPrompt.ask("Total pages")
    
    # Generate book ID (simplified version)
    book_id = f"book_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Create book state
    new_book = BookState(
        id=book_id,
        title=title,
        author=author,
        start_date=datetime.now(),
        current_page=0,
        total_pages=pages
    )
    
    # Load coach state and add book
    coach_state = state_manager.load_coach_state()
    coach_state.active_books.append(new_book)
    state_manager.save_coach_state(coach_state)
    
    console.print(
        Panel(
            f"[green]📚 Book added successfully![/green]\n\n"
            f"[cyan]Title:[/cyan] {title}\n"
            f"[cyan]Author:[/cyan] {author}\n"
            f"[cyan]Pages:[/cyan] {pages}\n"
            f"[cyan]ID:[/cyan] {book_id}\n\n"
            f"Start a session with: [cyan]osl session start --book {book_id}[/cyan]",
            style="green"
        )
    )


@book_group.command(name="list")
@click.pass_context
def list_books(ctx: click.Context) -> None:
    """List all books in your learning system.
    
    Shows:
    - Active books with progress
    - Sessions completed
    - Average retrieval scores
    - Last session date
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    
    if not coach_state.active_books:
        console.print("[yellow]No books added yet![/yellow]")
        console.print("Add a book with: [cyan]osl book add[/cyan]")
        return
    
    table = Table(title="📚 Active Books", show_header=True)
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Author", style="dim")
    table.add_column("Progress", justify="center")
    table.add_column("Sessions", justify="center")
    table.add_column("Avg Retrieval", justify="center")
    table.add_column("Last Session", style="dim")
    
    for book in coach_state.active_books:
        progress_pct = (book.current_page / book.total_pages * 100) if book.total_pages > 0 else 0
        progress_str = f"{book.current_page}/{book.total_pages} ({progress_pct:.0f}%)"
        
        avg_retrieval = f"{book.avg_retrieval_score:.0f}%" if book.avg_retrieval_score > 0 else "—"
        last_session = book.last_session.strftime("%Y-%m-%d") if book.last_session else "Never"
        
        table.add_row(
            book.id,
            book.title[:30] + "..." if len(book.title) > 30 else book.title,
            book.author[:20] + "..." if len(book.author) > 20 else book.author,
            progress_str,
            str(book.sessions_completed),
            avg_retrieval,
            last_session
        )
    
    console.print(table)


@book_group.command(name="update")
@click.argument("book_id")
@click.option("--page", "-p", type=int, help="Update current page")
@click.option("--complete", is_flag=True, help="Mark book as complete")
@click.pass_context
def update_book(ctx: click.Context, book_id: str, page: Optional[int], complete: bool) -> None:
    """Update book progress.
    
    Updates:
    - Current page number
    - Completion status
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    
    # Find the book
    book = None
    for b in coach_state.active_books:
        if b.id == book_id or b.title.lower().startswith(book_id.lower()):
            book = b
            break
    
    if not book:
        console.print(f"[red]Book '{book_id}' not found![/red]")
        return
    
    if complete:
        book.current_page = book.total_pages
        console.print(f"[green]✅ Book '{book.title}' marked as complete![/green]")
    elif page is not None:
        if page > book.total_pages:
            console.print(f"[yellow]Page {page} exceeds total pages ({book.total_pages})[/yellow]")
            return
        book.current_page = page
        console.print(f"[green]Updated '{book.title}' to page {page}[/green]")
    else:
        console.print("[yellow]No update specified. Use --page or --complete[/yellow]")
        return
    
    state_manager.save_coach_state(coach_state)


@book_group.command(name="stats")
@click.argument("book_id")
@click.pass_context
def book_stats(ctx: click.Context, book_id: str) -> None:
    """Show detailed statistics for a book.
    
    Displays:
    - Reading progress
    - Time invested
    - Performance metrics
    - Session history summary
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    
    # Find the book
    book = None
    for b in coach_state.active_books:
        if b.id == book_id or b.title.lower().startswith(book_id.lower()):
            book = b
            break
    
    if not book:
        console.print(f"[red]Book '{book_id}' not found![/red]")
        return
    
    progress_pct = (book.current_page / book.total_pages * 100) if book.total_pages > 0 else 0
    days_active = (datetime.now() - book.start_date).days
    
    console.print(
        Panel(
            f"[bold cyan]📊 Book Statistics[/bold cyan]\n\n"
            f"[cyan]Title:[/cyan] {book.title}\n"
            f"[cyan]Author:[/cyan] {book.author}\n"
            f"[cyan]ID:[/cyan] {book.id}\n\n"
            f"[bold]Progress[/bold]\n"
            f"├─ Pages: {book.current_page}/{book.total_pages} ({progress_pct:.1f}%)\n"
            f"├─ Sessions: {book.sessions_completed}\n"
            f"├─ Days Active: {days_active}\n"
            f"└─ Total Hours: {book.total_hours:.1f}\n\n"
            f"[bold]Performance[/bold]\n"
            f"├─ Avg Retrieval: {book.avg_retrieval_score:.1f}%\n"
            f"└─ Last Session: {book.last_session.strftime('%Y-%m-%d %H:%M') if book.last_session else 'Never'}",
            style="cyan"
        )
    )