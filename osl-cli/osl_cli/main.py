#!/usr/bin/env python3
"""OSL CLI - Main entry point."""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from osl_cli.commands.init import init_command
from osl_cli.commands.session import session_group
from osl_cli.commands.microloop import microloop
from osl_cli.commands.flashcard import flashcard
from osl_cli.commands.quiz import quiz
from osl_cli.commands.governance import governance
from osl_cli.commands.state import state

console = Console()


@click.group()
@click.version_option(version="3.4.0", prog_name="osl")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Optimized System for Learning - Command Line Interface.
    
    OSL enforces research-backed learning practices through:
    - Retrieval practice (active recall, not passive reading)
    - Spaced repetition (review at increasing intervals)
    - Interleaving (mix topics to strengthen discrimination)
    - Self-explanation (rephrase in your own words)
    - Immediate feedback (correct errors quickly)
    - Calibration (test predictions against performance)
    - Transfer (apply knowledge through projects)
    - Curiosity-driven questioning (learner-generated questions)
    """
    ctx.ensure_object(dict)
    ctx.obj['console'] = console


cli.add_command(init_command)
cli.add_command(session_group)
cli.add_command(microloop)
cli.add_command(flashcard)
cli.add_command(quiz)
cli.add_command(governance)
cli.add_command(state)


if __name__ == "__main__":
    cli()