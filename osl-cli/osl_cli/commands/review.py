"""Spaced repetition and review scheduling commands."""

import click
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm

from osl_cli.state.schemas import ReviewSchedule, CoachState
from osl_cli.state.manager import StateManager


@click.group(name="review")
@click.pass_context
def review_group(ctx: click.Context) -> None:
    """Manage spaced repetition reviews."""
    pass


@review_group.command(name="due")
@click.option("--deck", "-d", help="Specific deck to check")
@click.pass_context
def check_due(ctx: click.Context, deck: Optional[str]) -> None:
    """Check cards due for review.
    
    Shows:
    - Total cards due today
    - Card debt ratio
    - Recommended review time
    - Overdue cards needing attention
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    metrics = coach_state.performance_metrics
    
    # Calculate card debt
    card_debt_ratio = metrics.cards_due / metrics.daily_review_throughput if metrics.daily_review_throughput > 0 else 0
    debt_status = "🟢 Healthy" if card_debt_ratio <= coach_state.governance_thresholds.card_debt_multiplier.current else "🔴 High"
    
    # Estimate review time (assuming 10 seconds per card average)
    estimated_minutes = (metrics.cards_due * 10) / 60
    
    console.print(
        Panel(
            f"[bold cyan]📚 Review Status[/bold cyan]\n\n"
            f"[cyan]Cards Due:[/cyan] {metrics.cards_due}\n"
            f"[cyan]Completed Today:[/cyan] {metrics.cards_completed_today}\n"
            f"[cyan]Daily Throughput:[/cyan] {metrics.daily_review_throughput}\n\n"
            f"[bold]Card Debt[/bold]\n"
            f"├─ Ratio: {card_debt_ratio:.1f}x\n"
            f"├─ Threshold: {coach_state.governance_thresholds.card_debt_multiplier.current}x\n"
            f"└─ Status: {debt_status}\n\n"
            f"[cyan]Estimated Time:[/cyan] {estimated_minutes:.0f} minutes\n"
            f"[cyan]Review Time:[/cyan] {coach_state.review_schedule.daily_review_time}",
            style="cyan"
        )
    )
    
    if metrics.cards_due > 0:
        console.print("\n[cyan]Start review with:[/cyan] [bold]osl review start[/bold]")
    else:
        console.print("\n[green]✓ No cards due—all caught up![/green]")


@review_group.command(name="start")
@click.option("--limit", "-l", type=int, help="Maximum cards to review")
@click.option("--type", "-t", 
              type=click.Choice(["standard", "interleaving", "calibration"]),
              default="standard",
              help="Review type")
@click.pass_context
def start_review(ctx: click.Context, limit: Optional[int], type: str) -> None:
    """Start a spaced repetition review session.
    
    Enforces:
    - Card debt limits
    - Quality over quantity
    - Interleaving when scheduled
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    metrics = coach_state.performance_metrics
    
    if metrics.cards_due == 0:
        console.print("[green]No cards due for review![/green]")
        return
    
    # Check card debt gate
    card_debt_ratio = metrics.cards_due / metrics.daily_review_throughput if metrics.daily_review_throughput > 0 else 0
    if card_debt_ratio > coach_state.governance_thresholds.card_debt_multiplier.max:
        console.print(
            Panel(
                f"[red]⚠️ Card Debt Gate Triggered![/red]\n\n"
                f"Current debt: {card_debt_ratio:.1f}x\n"
                f"Maximum allowed: {coach_state.governance_thresholds.card_debt_multiplier.max}x\n\n"
                f"[yellow]Recommendations:[/yellow]\n"
                f"• Focus on quality over quantity\n"
                f"• Suspend new cards temporarily\n"
                f"• Consider adjusting daily throughput",
                style="red"
            )
        )
        if not Confirm.ask("Continue anyway?"):
            return
    
    # Set review limit
    if not limit:
        suggested = min(metrics.cards_due, metrics.daily_review_throughput)
        limit = IntPrompt.ask(
            f"How many cards to review? (due: {metrics.cards_due})",
            default=suggested
        )
    
    console.print(
        Panel(
            f"[green]🎯 Starting Review Session[/green]\n\n"
            f"[cyan]Type:[/cyan] {type.title()}\n"
            f"[cyan]Cards:[/cyan] {limit}\n"
            f"[cyan]Estimated Time:[/cyan] {(limit * 10) / 60:.0f} minutes\n\n"
            f"[dim]In full implementation, this would:[/dim]\n"
            f"[dim]• Connect to Anki via AnkiConnect[/dim]\n"
            f"[dim]• Track performance metrics[/dim]\n"
            f"[dim]• Update retrieval scores[/dim]",
            style="green"
        )
    )
    
    # Update metrics (simplified simulation)
    metrics.cards_completed_today += limit
    metrics.cards_due = max(0, metrics.cards_due - limit)
    
    # Add to 7-day average (simplified)
    metrics.avg_retrieval_7d = (metrics.avg_retrieval_7d * 6 + 80) / 7  # Simulated 80% score
    
    state_manager.save_coach_state(coach_state)
    
    console.print(f"\n[green]✓ Completed {limit} cards![/green]")
    console.print(f"[cyan]Remaining due:[/cyan] {metrics.cards_due}")


@review_group.command(name="schedule")
@click.option("--show-all", "-a", is_flag=True, help="Show all scheduled activities")
@click.pass_context
def show_schedule(ctx: click.Context, show_all: bool) -> None:
    """Show review schedule and upcoming activities.
    
    Displays:
    - Daily review time
    - Weekly synthesis schedule
    - Interleaving sessions
    - Calibration quizzes
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    schedule = coach_state.review_schedule
    
    table = Table(title="📅 Review Schedule", show_header=True)
    table.add_column("Activity", style="cyan")
    table.add_column("Next Due", style="white")
    table.add_column("Frequency", style="dim")
    table.add_column("Status", justify="center")
    
    # Daily reviews
    table.add_row(
        "Daily Review",
        schedule.daily_review_time,
        "Every day",
        "🟢 Active"
    )
    
    # Weekly activities
    if schedule.next_synthesis:
        days_until = (schedule.next_synthesis - datetime.now()).days
        status = "🟡 Soon" if days_until <= 2 else "🟢 Scheduled"
        table.add_row(
            "Weekly Synthesis",
            schedule.next_synthesis.strftime("%Y-%m-%d"),
            "Every Sunday",
            status
        )
    
    if schedule.next_calibration:
        days_until = (schedule.next_calibration - datetime.now()).days
        status = "🟡 Soon" if days_until <= 2 else "🟢 Scheduled"
        table.add_row(
            "Calibration Quiz",
            schedule.next_calibration.strftime("%Y-%m-%d"),
            "Weekly",
            status
        )
    
    if schedule.next_interleaving:
        table.add_row(
            "Interleaving Session",
            schedule.next_interleaving.strftime("%Y-%m-%d %H:%M"),
            "2-3x per week",
            "🟢 Scheduled"
        )
    
    if schedule.next_project_due:
        days_until = (schedule.next_project_due - datetime.now()).days
        status = "🔴 Overdue" if days_until < 0 else "🟡 Due Soon" if days_until <= 7 else "🟢 Scheduled"
        table.add_row(
            "Transfer Project",
            schedule.next_project_due.strftime("%Y-%m-%d"),
            "Per book",
            status
        )
    
    console.print(table)
    
    # Show recommendations
    now = datetime.now()
    recommendations = []
    
    if schedule.next_synthesis and (schedule.next_synthesis - now).days <= 0:
        recommendations.append("• Complete weekly synthesis essay")
    
    if schedule.next_calibration and (schedule.next_calibration - now).days <= 0:
        recommendations.append("• Take calibration quiz")
    
    metrics = coach_state.performance_metrics
    if metrics.interleaving_sessions_week < 1:
        recommendations.append("• Schedule an interleaving session")
    
    if recommendations:
        console.print("\n[bold yellow]📋 Recommendations:[/bold yellow]")
        for rec in recommendations:
            console.print(rec)


@review_group.command(name="interleave")
@click.option("--topics", "-t", multiple=True, help="Topics to interleave")
@click.pass_context
def start_interleaving(ctx: click.Context, topics: tuple) -> None:
    """Start an interleaving session.
    
    Interleaving:
    - Mixes topics from different books/domains
    - Improves discrimination between concepts
    - Enhances transfer and flexibility
    - 1-3 sessions per week recommended
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    
    # Check if interleaving is due
    if coach_state.review_schedule.next_interleaving:
        days_until = (coach_state.review_schedule.next_interleaving - datetime.now()).days
        if days_until > 0:
            console.print(f"[yellow]Next interleaving scheduled in {days_until} days[/yellow]")
            if not Confirm.ask("Start early?"):
                return
    
    # Get topics if not provided
    if not topics:
        console.print("[cyan]Select 2-3 topics to interleave:[/cyan]")
        topic_list = []
        for i in range(3):
            topic = Prompt.ask(f"Topic {i+1}", default="")
            if topic:
                topic_list.append(topic)
            elif i < 2:
                console.print("[yellow]Need at least 2 topics for interleaving[/yellow]")
        topics = tuple(topic_list)
    
    if len(topics) < 2:
        console.print("[red]Interleaving requires at least 2 topics![/red]")
        return
    
    console.print(
        Panel(
            f"[green]🔀 Starting Interleaving Session[/green]\n\n"
            f"[cyan]Topics:[/cyan]\n" + "\n".join(f"  • {t}" for t in topics) + "\n\n"
            f"[bold]Benefits:[/bold]\n"
            f"• Improves discrimination between concepts\n"
            f"• Reduces interference\n"
            f"• Enhances transfer\n\n"
            f"[dim]Alternate between topics every 10-15 minutes[/dim]",
            style="green"
        )
    )
    
    # Update metrics
    coach_state.performance_metrics.interleaving_sessions_week += 1
    
    # Schedule next interleaving (3-4 days out)
    coach_state.review_schedule.next_interleaving = datetime.now() + timedelta(days=3)
    
    state_manager.save_coach_state(coach_state)


@review_group.command(name="calibrate")
@click.option("--questions", "-q", type=int, default=10, help="Number of questions")
@click.pass_context
def calibration_quiz(ctx: click.Context, questions: int) -> None:
    """Generate and take a calibration quiz.
    
    Calibration:
    - Tests prediction accuracy
    - Identifies overconfidence/underconfidence
    - Adjusts review priorities
    - Weekly recommended
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    
    console.print(
        Panel(
            f"[bold cyan]🎯 Calibration Quiz[/bold cyan]\n\n"
            f"[cyan]Questions:[/cyan] {questions}\n"
            f"[cyan]Current Accuracy:[/cyan] {coach_state.performance_metrics.avg_prediction_accuracy_7d:.0f}%\n\n"
            f"[bold]Process:[/bold]\n"
            f"1. Predict confidence (0-100%)\n"
            f"2. Answer the question\n"
            f"3. Compare prediction to actual\n"
            f"4. Adjust future predictions\n\n"
            f"[dim]In full implementation:[/dim]\n"
            f"[dim]• AI generates questions from your notes[/dim]\n"
            f"[dim]• Tracks calibration curves[/dim]\n"
            f"[dim]• Adjusts review priorities[/dim]",
            style="cyan"
        )
    )
    
    # Simulate quiz (in full implementation, would generate from notes)
    console.print("\n[cyan]Taking calibration quiz...[/cyan]")
    
    # Update metrics (simulated)
    new_accuracy = 78  # Simulated result
    coach_state.performance_metrics.avg_prediction_accuracy_7d = (
        coach_state.performance_metrics.avg_prediction_accuracy_7d * 6 + new_accuracy
    ) / 7
    
    # Check calibration gate
    if new_accuracy < coach_state.governance_thresholds.calibration_gate.min:
        console.print(
            Panel(
                f"[yellow]⚠️ Below Calibration Threshold[/yellow]\n\n"
                f"Score: {new_accuracy}%\n"
                f"Minimum: {coach_state.governance_thresholds.calibration_gate.min}%\n\n"
                f"[cyan]Recommendations:[/cyan]\n"
                f"• Review misconceptions\n"
                f"• Focus on fundamentals\n"
                f"• Reduce new card rate",
                style="yellow"
            )
        )
    else:
        console.print(f"\n[green]✓ Calibration complete: {new_accuracy}%[/green]")
    
    # Schedule next calibration
    coach_state.review_schedule.next_calibration = datetime.now() + timedelta(days=7)
    
    state_manager.save_coach_state(coach_state)