import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
from typing import Optional

from .runner import run_tests_on_pdf, run_batch
from .tests.base import get_all_test_names

app = typer.Typer(
    name="pdf-tester",
    help="PDF validation and testing tool",
    add_completion=False,
)
console = Console()


@app.command()
def test(
    pdf_path: Path = typer.Argument(..., exists=True, help="Path to PDF file"),
    tests: Optional[str] = typer.Option(
        None, "--tests", "-t",
        help="Comma-separated tests to run (e.g. structure,metadata). Omit to run all."
    ),
    ):
    """Run tests on a single PDF file."""
    report = run_tests_on_pdf(pdf_path, tests)

    # Print results
    table = Table(title=f"PDF Test Results: {pdf_path.name}")
    table.add_column("Test", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Message")

    for result in report.results:
        status = "[bold green]PASS[/bold green]" if result.passed else "[bold red]FAIL[/bold red]"
        table.add_row(result.test_name, status, result.message)

    console.print(table)
    console.print(f"\nSummary: [bold]{report.summary()}[/bold]")

    if not report.all_passed:
        raise typer.Exit(code=1)


@app.command()
def batch(
    directory: Path = typer.Argument(..., exists=True, file_okay=False, help="Directory containing PDFs"),
    tests: Optional[str] = typer.Option(
        None, "--tests", "-t",
        help="Comma-separated tests to run. Omit to run all."
    ),
    output: str = typer.Option("console", "--output", "-o", help="Output format: console, json"),
):
    """Run tests on all PDFs in a directory."""
    reports = run_batch(directory, tests)

    if output == "json":
        import json
        data = [
            {
                "pdf": r.pdf_path,
                "all_passed": r.all_passed,
                "results": [r.__dict__ for r in r.results]
            }
            for r in reports
        ]
        typer.echo(json.dumps(data, indent=2))
    else:
        console.print(f"\n[bold]Batch completed:[/bold] {len(reports)} PDF(s) processed.")


@app.command()
def list():
    """List all available tests."""
    table = Table(title="Available PDF Tests")
    table.add_column("Test Name", style="cyan")
    table.add_column("Description")

    for name, desc, _ in TESTS:  # TESTS imported from base
        table.add_row(name, desc)
    
    console.print(table)


# Make TESTS available for list command
from .tests.base import TESTS


if __name__ == "__main__":
    app()