"""Weekly synthesis and integration commands."""

import click
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm

from osl_cli.state.schemas import CoachState
from osl_cli.state.manager import StateManager


@click.group(name="synthesis")
@click.pass_context
def synthesis_group(ctx: click.Context) -> None:
    """Weekly knowledge integration activities."""
    pass


@synthesis_group.command(name="essay")
@click.option("--topic", "-t", help="Essay topic or theme")
@click.option("--books", "-b", multiple=True, help="Books to synthesize from")
@click.pass_context
def write_essay(ctx: click.Context, topic: Optional[str], books: tuple) -> None:
    """Start weekly synthesis essay.
    
    Synthesis essays:
    - Integrate concepts across multiple sources
    - Identify patterns and connections
    - Deepen understanding through writing
    - 60-90 minutes recommended
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    
    # Check if synthesis is due
    if coach_state.review_schedule.next_synthesis:
        days_until = (coach_state.review_schedule.next_synthesis - datetime.now()).days
        if days_until > 0:
            console.print(f"[yellow]Next synthesis scheduled in {days_until} days (Sunday)[/yellow]")
            if not Confirm.ask("Start early?"):
                return
    
    # Get topic if not provided
    if not topic:
        console.print("[cyan]What theme or question will you explore?[/cyan]")
        topic = Prompt.ask("Essay topic")
    
    # Get books if not provided
    if not books:
        console.print("\n[cyan]Which books/sources will you synthesize?[/cyan]")
        if coach_state.active_books:
            console.print("[dim]Active books:[/dim]")
            for book in coach_state.active_books:
                console.print(f"  • {book.title}")
        
        book_list = []
        for i in range(3):
            book = Prompt.ask(f"Book {i+1}", default="")
            if book:
                book_list.append(book)
            elif i < 1:
                console.print("[yellow]Include at least one source[/yellow]")
        books = tuple(book_list)
    
    # Create synthesis workspace
    synthesis_dir = Path("obsidian/20_synthesis")
    synthesis_dir.mkdir(parents=True, exist_ok=True)
    
    essay_file = synthesis_dir / f"{datetime.now().strftime('%Y%m%d')}_{topic.replace(' ', '_')[:30]}.md"
    
    console.print(
        Panel(
            f"[bold cyan]📝 Weekly Synthesis Essay[/bold cyan]\n\n"
            f"[cyan]Topic:[/cyan] {topic}\n"
            f"[cyan]Sources:[/cyan]\n" + "\n".join(f"  • {b}" for b in books) + "\n\n"
            f"[bold]Structure:[/bold]\n"
            f"1. Central claim or question\n"
            f"2. Evidence from multiple sources\n"
            f"3. Connections and patterns\n"
            f"4. Personal insights\n"
            f"5. Open questions\n\n"
            f"[cyan]File:[/cyan] {essay_file}\n"
            f"[cyan]Time:[/cyan] 60-90 minutes recommended",
            style="cyan"
        )
    )
    
    # Create essay template
    template = f"""# {topic}
_Weekly Synthesis: {datetime.now().strftime('%Y-%m-%d')}_

## Central Question
What am I trying to understand?

## Key Concepts
### From {books[0] if books else 'Book 1'}
- 

### From {books[1] if len(books) > 1 else 'Book 2'}
- 

## Connections
How do these ideas relate?

## Personal Insights
What new understanding emerged?

## Open Questions
What remains unclear?

## Action Items
How will I apply this?
"""
    
    essay_file.write_text(template)
    console.print(f"\n[green]✓ Essay template created at:[/green] {essay_file}")
    
    # Update schedule
    coach_state.review_schedule.next_synthesis = datetime.now() + timedelta(days=7)
    state_manager.save_coach_state(coach_state)


@synthesis_group.command(name="map")
@click.option("--concepts", "-c", multiple=True, help="Core concepts to map")
@click.option("--time-limit", "-t", type=int, default=5, help="Time limit in minutes")
@click.pass_context
def concept_map(ctx: click.Context, concepts: tuple, time_limit: int) -> None:
    """Create a concept map (5-minute constraint).
    
    Concept maps:
    - Visualize relationships between ideas
    - Identify hierarchies and dependencies
    - Reveal gaps in understanding
    - Time-boxed to prevent over-engineering
    """
    console: Console = ctx.obj['console']
    
    # Get concepts if not provided
    if not concepts:
        console.print("[cyan]List 3-5 core concepts to map:[/cyan]")
        concept_list = []
        for i in range(5):
            concept = Prompt.ask(f"Concept {i+1}", default="")
            if concept:
                concept_list.append(concept)
            elif i < 3:
                console.print("[yellow]Add at least 3 concepts[/yellow]")
        concepts = tuple(concept_list)
    
    if len(concepts) < 3:
        console.print("[red]Need at least 3 concepts for a meaningful map![/red]")
        return
    
    console.print(
        Panel(
            f"[bold cyan]🗺️ Concept Map Creation[/bold cyan]\n\n"
            f"[cyan]Concepts:[/cyan]\n" + "\n".join(f"  • {c}" for c in concepts) + "\n\n"
            f"[cyan]Time Limit:[/cyan] {time_limit} minutes\n\n"
            f"[bold]Instructions:[/bold]\n"
            f"1. Place central concept in middle\n"
            f"2. Add related concepts around it\n"
            f"3. Draw connections with labels\n"
            f"4. Use arrows for directionality\n"
            f"5. Stop at {time_limit} minutes!\n\n"
            f"[yellow]Timer starts now![/yellow]",
            style="cyan"
        )
    )
    
    # In full implementation, would integrate with drawing tool
    console.print(f"\n[dim]Create your map in Obsidian Canvas or on paper[/dim]")
    console.print(f"[dim]Save to: obsidian/20_synthesis/maps/[/dim]")


@synthesis_group.command(name="project")
@click.option("--book", "-b", help="Book to create project for")
@click.option("--type", "-t", 
              type=click.Choice(["code", "writing", "presentation", "tutorial", "other"]),
              help="Project type")
@click.pass_context
def transfer_project(ctx: click.Context, book: Optional[str], type: Optional[str]) -> None:
    """Create a transfer project to apply learning.
    
    Transfer projects:
    - Apply concepts to real-world problems
    - Create tangible artifacts
    - Test understanding through creation
    - One per completed book required
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    
    # Check if project is due
    if coach_state.review_schedule.next_project_due:
        days_until = (coach_state.review_schedule.next_project_due - datetime.now()).days
        if days_until < 0:
            console.print(
                Panel(
                    f"[red]⚠️ Transfer Project Overdue![/red]\n\n"
                    f"Days overdue: {abs(days_until)}\n\n"
                    f"Transfer gate requires one project per book",
                    style="red"
                )
            )
    
    # Get book if not provided
    if not book:
        if coach_state.active_books:
            console.print("[cyan]Which book is this project for?[/cyan]")
            for i, b in enumerate(coach_state.active_books):
                progress = (b.current_page / b.total_pages * 100) if b.total_pages > 0 else 0
                console.print(f"  {i+1}. {b.title} ({progress:.0f}% complete)")
            
            choice = IntPrompt.ask("Select book", choices=[str(i+1) for i in range(len(coach_state.active_books))])
            book = coach_state.active_books[choice - 1].title
        else:
            book = Prompt.ask("Book title")
    
    # Get project type if not provided
    if not type:
        console.print("\n[cyan]What type of project?[/cyan]")
        console.print("  1. Code (script, app, tool)")
        console.print("  2. Writing (article, guide, documentation)")
        console.print("  3. Presentation (slides, video, workshop)")
        console.print("  4. Tutorial (teach others)")
        console.print("  5. Other")
        
        choice = IntPrompt.ask("Select type", choices=["1", "2", "3", "4", "5"])
        type = ["code", "writing", "presentation", "tutorial", "other"][choice - 1]
    
    # Get project description
    console.print(f"\n[cyan]Describe your {type} project:[/cyan]")
    description = Prompt.ask("Project description")
    
    # Create project workspace
    project_dir = Path("obsidian/30_projects")
    project_dir.mkdir(parents=True, exist_ok=True)
    
    project_file = project_dir / f"{datetime.now().strftime('%Y%m%d')}_{book.replace(' ', '_')[:20]}_project.md"
    
    console.print(
        Panel(
            f"[bold green]🚀 Transfer Project[/bold green]\n\n"
            f"[cyan]Book:[/cyan] {book}\n"
            f"[cyan]Type:[/cyan] {type.title()}\n"
            f"[cyan]Description:[/cyan] {description}\n\n"
            f"[bold]Success Criteria:[/bold]\n"
            f"• Applies 3+ concepts from the book\n"
            f"• Creates working artifact\n"
            f"• Could teach someone else\n"
            f"• Identifies gaps in understanding\n\n"
            f"[cyan]File:[/cyan] {project_file}",
            style="green"
        )
    )
    
    # Create project template
    template = f"""# Transfer Project: {book}
_Created: {datetime.now().strftime('%Y-%m-%d')}_

## Project Type
{type.title()}

## Description
{description}

## Concepts to Apply
1. 
2. 
3. 

## Success Criteria
- [ ] Working artifact created
- [ ] 3+ concepts applied
- [ ] Could teach to someone else
- [ ] Gaps identified and documented

## Implementation Plan
1. 
2. 
3. 

## Progress Log
### {datetime.now().strftime('%Y-%m-%d')}
- Started project planning

## Lessons Learned


## Gaps Discovered

"""
    
    project_file.write_text(template)
    console.print(f"\n[green]✓ Project template created at:[/green] {project_file}")
    
    # Update metrics
    coach_state.performance_metrics.last_transfer_project = datetime.now()
    coach_state.review_schedule.next_project_due = datetime.now() + timedelta(days=30)
    
    state_manager.save_coach_state(coach_state)


@synthesis_group.command(name="review")
@click.pass_context
def review_synthesis(ctx: click.Context) -> None:
    """Review synthesis activities and patterns.
    
    Shows:
    - Recent essays and themes
    - Concept maps created
    - Transfer projects completed
    - Emerging patterns
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    
    # Check synthesis directory
    synthesis_dir = Path("obsidian/20_synthesis")
    essays = list(synthesis_dir.glob("*.md")) if synthesis_dir.exists() else []
    
    project_dir = Path("obsidian/30_projects")
    projects = list(project_dir.glob("*.md")) if project_dir.exists() else []
    
    console.print(
        Panel(
            f"[bold cyan]📊 Synthesis Review[/bold cyan]\n\n"
            f"[cyan]Weekly Essays:[/cyan] {len(essays)}\n"
            f"[cyan]Transfer Projects:[/cyan] {len(projects)}\n"
            f"[cyan]Last Project:[/cyan] {coach_state.performance_metrics.last_transfer_project.strftime('%Y-%m-%d') if coach_state.performance_metrics.last_transfer_project else 'Never'}\n\n"
            f"[bold]Upcoming:[/bold]\n"
            f"• Next synthesis: {coach_state.review_schedule.next_synthesis.strftime('%Y-%m-%d') if coach_state.review_schedule.next_synthesis else 'Not scheduled'}\n"
            f"• Project due: {coach_state.review_schedule.next_project_due.strftime('%Y-%m-%d') if coach_state.review_schedule.next_project_due else 'Not scheduled'}",
            style="cyan"
        )
    )
    
    if essays:
        console.print("\n[bold]Recent Essays:[/bold]")
        for essay in sorted(essays)[-5:]:
            console.print(f"  • {essay.name}")
    
    if projects:
        console.print("\n[bold]Transfer Projects:[/bold]")
        for project in sorted(projects)[-3:]:
            console.print(f"  • {project.name}")