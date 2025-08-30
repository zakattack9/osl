"""Governance checking and threshold management."""

import click
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import FloatPrompt, Confirm

from osl_cli.state.manager import StateManager
from osl_cli.governance.gates import GovernanceChecker


@click.command(name="governance")
@click.argument("action", type=click.Choice(["check", "tune"]))
@click.option("--gate", "-g", help="Specific gate to tune")
@click.pass_context
def governance(ctx: click.Context, action: str, gate: str) -> None:
    """Check governance gates and manage thresholds.
    
    Gates enforce learning quality:
    - Calibration: Retrieval accuracy (75-85%)
    - Card Debt: Review backlog (1.5×-2.5× daily throughput)
    - Transfer: Project completion per book
    - Interleaving: Mixed practice frequency
    """
    console: Console = ctx.obj['console']
    state_manager = StateManager()
    
    coach_state = state_manager.load_coach_state()
    checker = GovernanceChecker(coach_state)
    
    if action == "check":
        # Check all gates
        console.print(Panel("🔍 Governance Gate Check", style="bold blue"))
        
        gates_status = checker.check_all_gates()
        
        # Display results
        table = Table(title="Gate Status")
        table.add_column("Gate", style="cyan", width=15)
        table.add_column("Status", style="green", width=12)
        table.add_column("Current", style="yellow", width=15)
        table.add_column("Threshold", style="white", width=15)
        table.add_column("Action Required", style="red", width=30)
        
        for gate_name, status in gates_status.items():
            status_emoji = "✅" if status["passing"] else "❌"
            status_text = f"{status_emoji} {status['status']}"
            
            action_text = status.get("action", "None")
            if action_text and action_text != "None":
                action_style = "[red]" + action_text + "[/red]"
            else:
                action_style = "[green]None[/green]"
            
            table.add_row(
                gate_name.replace("_", " ").title(),
                status_text,
                status.get("current_value", "N/A"),
                status.get("threshold", "N/A"),
                action_style
            )
        
        console.print(table)
        
        # Overall status
        overall = coach_state.governance_status.overall_state
        
        if overall == "NORMAL":
            console.print(
                Panel(
                    "[green]✅ All systems operational![/green]\n"
                    "Continue with normal learning workflow.",
                    style="green"
                )
            )
        elif overall == "REMEDIATION":
            console.print(
                Panel(
                    "[yellow]⚠️ Remediation needed![/yellow]\n"
                    "Some gates need attention but learning can continue.\n"
                    "Address the issues shown above.",
                    style="yellow"
                )
            )
        elif overall == "BLOCKED":
            console.print(
                Panel(
                    "[red]🚫 Learning blocked![/red]\n"
                    "Critical gates are failing.\n"
                    "You must address these issues before creating new content.",
                    style="red"
                )
            )
        
        # Save updated state
        state_manager.save_coach_state(coach_state)
    
    elif action == "tune":
        # Tune thresholds
        if not gate:
            # Show tunable gates
            console.print(Panel("⚙️ Tunable Governance Thresholds", style="bold blue"))
            
            table = Table()
            table.add_column("Gate", style="cyan")
            table.add_column("Current", style="yellow")
            table.add_column("Range", style="white")
            table.add_column("Command", style="green")
            
            thresholds = coach_state.governance_thresholds
            
            table.add_row(
                "Calibration Gate",
                f"{thresholds.calibration_gate.current}%",
                f"{thresholds.calibration_gate.min}-{thresholds.calibration_gate.max}%",
                "osl governance tune --gate calibration"
            )
            table.add_row(
                "Card Debt Multiplier",
                f"{thresholds.card_debt_multiplier.current}×",
                f"{thresholds.card_debt_multiplier.min}×-{thresholds.card_debt_multiplier.max}×",
                "osl governance tune --gate card_debt"
            )
            table.add_row(
                "Max New Cards",
                str(int(thresholds.max_new_cards.current)),
                f"{int(thresholds.max_new_cards.min)}-{int(thresholds.max_new_cards.max)}",
                "osl governance tune --gate max_cards"
            )
            table.add_row(
                "Interleaving/Week",
                str(int(thresholds.interleaving_per_week.current)),
                f"{int(thresholds.interleaving_per_week.min)}-{int(thresholds.interleaving_per_week.max)}",
                "osl governance tune --gate interleaving"
            )
            
            console.print(table)
            console.print("\n[cyan]Use the commands above to tune specific thresholds.[/cyan]")
        
        else:
            # Tune specific gate
            thresholds = coach_state.governance_thresholds
            
            if gate == "calibration":
                threshold = thresholds.calibration_gate
                name = "Calibration Gate (Retrieval Accuracy %)"
            elif gate == "card_debt":
                threshold = thresholds.card_debt_multiplier
                name = "Card Debt Multiplier"
            elif gate == "max_cards":
                threshold = thresholds.max_new_cards
                name = "Max New Cards per Session"
            elif gate == "interleaving":
                threshold = thresholds.interleaving_per_week
                name = "Interleaving Sessions per Week"
            else:
                console.print(f"[red]Unknown gate: {gate}[/red]")
                return
            
            console.print(
                Panel(
                    f"⚙️ Tuning: {name}\n\n"
                    f"Current: {threshold.current}\n"
                    f"Range: {threshold.min} - {threshold.max}\n\n"
                    "[yellow]Note: Adjust based on your performance data.[/yellow]",
                    style="bold blue"
                )
            )
            
            # Get new value
            new_value = FloatPrompt.ask(
                f"New value ({threshold.min}-{threshold.max})",
            )
            
            # Validate range
            if new_value < threshold.min or new_value > threshold.max:
                console.print(f"[red]Value must be between {threshold.min} and {threshold.max}[/red]")
                return
            
            # Confirm change
            confirm = Confirm.ask(
                f"Change {name} from {threshold.current} to {new_value}?"
            )
            
            if confirm:
                threshold.current = new_value
                threshold.last_adjusted = datetime.now()
                state_manager.save_coach_state(coach_state)
                
                console.print(
                    Panel(
                        f"[green]✅ Threshold updated![/green]\n"
                        f"{name}: {new_value}",
                        style="green"
                    )
                )