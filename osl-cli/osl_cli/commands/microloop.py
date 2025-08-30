"""Micro-loop tracking command."""

import hashlib
import click
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt

from osl_cli.state.schemas import MicroLoop, RecallData, FeynmanExplanation
from osl_cli.state.manager import StateManager


@click.command(name="microloop")
@click.argument("action", type=click.Choice(["complete", "start"]))
@click.option("--pages", "-p", help="Page range (e.g., '45-50')")
@click.pass_context
def microloop(ctx: click.Context, action: str, pages: str) -> None:
    """Track micro-loop completion.
    
    A micro-loop consists of:
    1. Reading chunk (5-10 pages)
    2. Free recall (1-2 minutes)
    3. Feynman explanation
    4. AI feedback (2-3 questions max)
    5. Flashcard creation
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    if not state_manager.has_active_session():
        console.print("[red]No active session![/red]")
        console.print("Run [cyan]osl session start[/cyan] first.")
        return
    
    session = state_manager.load_current_session()
    
    if action == "start":
        # Start new micro-loop
        if not pages:
            pages = Prompt.ask("Page range (e.g., '45-50')")
        
        loop_id = len(session.micro_loops) + 1
        
        new_loop = MicroLoop(
            loop_id=loop_id,
            pages=pages,
            chunk_type="standard",
            start_time=datetime.now(),
        )
        
        session.micro_loops.append(new_loop)
        session.state = "READING"
        state_manager.save_current_session(session)
        
        console.print(
            Panel(
                f"[green]📖 Micro-loop {loop_id} started![/green]\n\n"
                f"Pages: {pages}\n\n"
                "[cyan]Steps:[/cyan]\n"
                "1. Read the pages carefully\n"
                "2. Close the book\n" 
                "3. Run [cyan]osl microloop complete[/cyan] when done reading",
                style="green"
            )
        )
    
    elif action == "complete":
        # Complete current micro-loop
        if not session.micro_loops:
            console.print("[red]No micro-loop in progress![/red]")
            return
        
        current_loop = session.micro_loops[-1]
        
        if current_loop.end_time:
            console.print("[yellow]Current micro-loop already completed![/yellow]")
            return
        
        console.print(Panel("🧠 Free Recall Phase", style="bold blue"))
        console.print(
            "[cyan]Close your book and spend 1-2 minutes recalling what you just read.[/cyan]\n"
            "Write down key points below (press Enter twice when done):\n"
        )
        
        # Collect recall points
        key_points = []
        while True:
            point = Prompt.ask(f"Point {len(key_points) + 1}", default="")
            if not point:
                if key_points:
                    break
                console.print("[yellow]Add at least one key point[/yellow]")
            else:
                key_points.append(point)
        
        # Get verbatim recall
        console.print("\n[cyan]Now write a paragraph summarizing what you remember:[/cyan]")
        verbatim_recall = Prompt.ask("Your recall")
        
        # Calculate hash for verbatim storage
        recall_hash = hashlib.sha256(verbatim_recall.encode()).hexdigest()
        
        # Get confidence score
        confidence = IntPrompt.ask(
            "Rate your recall confidence (1-10)",
            choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        )
        
        # Create recall data
        recall_data = RecallData(
            duration_seconds=90,  # Would track actual time in full implementation
            key_points=key_points,
            confidence_score=int(confidence),
            verbatim_recall=verbatim_recall,
            recall_hash=recall_hash,
        )
        
        console.print(Panel("📝 Feynman Explanation Phase", style="bold blue"))
        console.print(
            "[cyan]Explain what you learned as if teaching a smart 12-year-old.[/cyan]\n"
        )
        
        explanation = Prompt.ask("Your explanation")
        
        # Ask for analogies and examples
        console.print("\n[cyan]List any analogies you used:[/cyan]")
        analogies = []
        while True:
            analogy = Prompt.ask("Analogy", default="")
            if not analogy:
                break
            analogies.append(analogy)
        
        console.print("\n[cyan]List any examples you created:[/cyan]")
        examples = []
        while True:
            example = Prompt.ask("Example", default="")
            if not example:
                break
            examples.append(example)
        
        # Create Feynman data
        explanation_hash = hashlib.sha256(explanation.encode()).hexdigest()
        
        feynman_data = FeynmanExplanation(
            explanation_text=explanation,
            explanation_hash=explanation_hash,
            analogies_used=analogies,
            examples_created=examples,
            duration_seconds=120,  # Would track actual time
        )
        
        # Calculate retrieval score (simplified)
        # In full implementation, would compare against source material
        retrieval_score = min(100, confidence * 10 + len(key_points) * 5)
        
        # Update micro-loop
        current_loop.end_time = datetime.now()
        current_loop.recall_data = recall_data
        current_loop.feynman_explanation = feynman_data
        current_loop.retrieval_score = retrieval_score
        
        # Update session
        session.retrieval_scores.append(retrieval_score)
        session.total_recall_time += 90
        session.total_explanation_time += 120
        session.state = "FEEDBACK"
        
        state_manager.save_current_session(session)
        
        console.print(
            Panel(
                f"[green]✅ Micro-loop {current_loop.loop_id} completed![/green]\n\n"
                f"📊 Retrieval Score: {retrieval_score}%\n"
                f"🧠 Key Points Recalled: {len(key_points)}\n"
                f"💡 Analogies Used: {len(analogies)}\n"
                f"📝 Examples Created: {len(examples)}\n\n"
                "[cyan]Next:[/cyan] AI tutor will ask 2-3 questions about the material\n"
                "(In full implementation, AI would interact here)\n\n"
                "Then run [cyan]osl flashcard create[/cyan] to create cards from gaps",
                style="green"
            )
        )