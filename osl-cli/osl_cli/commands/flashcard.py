"""Flashcard creation command - learner authored only."""

import hashlib
import uuid
import click
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from osl_cli.state.schemas import FlashcardCreated
from osl_cli.state.manager import StateManager


@click.command(name="flashcard")
@click.argument("action", type=click.Choice(["create", "list"]))
@click.pass_context
def flashcard(ctx: click.Context, action: str) -> None:
    """Validate and store learner-authored flashcards.
    
    CRITICAL: Flashcards must be authored by the learner.
    AI can only assist with formatting, never generate content.
    
    Generation Effect: Self-created materials are remembered 
    50% better than provided materials.
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    if not state_manager.has_active_session():
        console.print("[red]No active session![/red]")
        console.print("Run [cyan]osl session start[/cyan] first.")
        return
    
    session = state_manager.load_current_session()
    
    if action == "create":
        # Check flashcard limit
        if session.flashcards_created >= session.max_flashcards:
            console.print(
                Panel(
                    f"[yellow]⚠️ Flashcard limit reached![/yellow]\n\n"
                    f"You've created {session.flashcards_created}/{session.max_flashcards} cards this session.\n"
                    "This limit ensures quality over quantity.\n\n"
                    "[cyan]Remaining gaps become tomorrow's priority.[/cyan]",
                    style="yellow"
                )
            )
            return
        
        console.print(
            Panel(
                "🎴 Create Flashcard from YOUR Identified Gap\n\n"
                "[bold]Remember:[/bold] YOU decide what becomes a card\n"
                "based on what YOU missed during recall.\n\n"
                "AI will ONLY help with formatting.",
                style="bold blue"
            )
        )
        
        # Step 1: Identify the gap
        console.print("[cyan]What gap did you identify during recall?[/cyan]")
        gap = Prompt.ask("Gap identified")
        
        # Step 2: Decide importance
        important = Confirm.ask("Is this gap important enough to become a flashcard?")
        
        if not important:
            console.print("[yellow]Skipping this gap.[/yellow]")
            return
        
        # Step 3: Learner writes the question
        console.print("\n[cyan]Write YOUR question for this card:[/cyan]")
        console.print("[dim](In your own words, targeting your confusion)[/dim]")
        front = Prompt.ask("Front (question)")
        
        # Step 4: Learner writes the answer
        console.print("\n[cyan]Write YOUR answer:[/cyan]")
        console.print("[dim](In your own words, as you understand it)[/dim]")
        back = Prompt.ask("Back (answer)")
        
        # Step 5: Add source
        page = Prompt.ask("Source page number", default="0")
        
        # Generate hashes for verbatim storage
        card_id = str(uuid.uuid4())[:8]
        content_combined = f"{front}|{back}"
        verbatim_hash = hashlib.sha256(content_combined.encode()).hexdigest()
        
        # Create flashcard
        new_card = FlashcardCreated(
            card_id=card_id,
            front=front,
            back=back,
            source_page=int(page) if page.isdigit() else 0,
            created_from_gap=gap,
            learner_authored=True,
            verbatim_hash=verbatim_hash,
            ai_assisted_formatting=False,
        )
        
        # Add to current micro-loop if exists
        if session.micro_loops:
            current_loop = session.micro_loops[-1]
            current_loop.flashcards_created.append(new_card)
        
        # Update session
        session.flashcards_created += 1
        state_manager.save_current_session(session)
        
        console.print(
            Panel(
                f"[green]✅ Flashcard created![/green]\n\n"
                f"[bold]Front:[/bold] {front}\n"
                f"[bold]Back:[/bold] {back}\n"
                f"[bold]Gap:[/bold] {gap}\n"
                f"[bold]ID:[/bold] {card_id}\n\n"
                f"Cards created: {session.flashcards_created}/{session.max_flashcards}\n\n"
                "[dim]Hash: {verbatim_hash[:16]}...[/dim]",
                style="green"
            )
        )
        
        # Offer to create another
        if session.flashcards_created < session.max_flashcards:
            create_another = Confirm.ask("Create another card?")
            if create_another:
                ctx.invoke(flashcard, action="create")
    
    elif action == "list":
        # List flashcards from current session
        cards_count = 0
        
        console.print(Panel("📚 Session Flashcards", style="bold blue"))
        
        for loop in session.micro_loops:
            for card in loop.flashcards_created:
                cards_count += 1
                console.print(
                    f"\n[cyan]Card {cards_count}:[/cyan]\n"
                    f"  [bold]Q:[/bold] {card.front}\n"
                    f"  [bold]A:[/bold] {card.back}\n"
                    f"  [dim]Gap: {card.created_from_gap}[/dim]\n"
                    f"  [dim]Page: {card.source_page}[/dim]"
                )
        
        if cards_count == 0:
            console.print("[yellow]No flashcards created yet this session.[/yellow]")
        else:
            console.print(
                f"\n[green]Total: {cards_count}/{session.max_flashcards} cards[/green]"
            )