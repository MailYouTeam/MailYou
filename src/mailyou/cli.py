from __future__ import annotations

import typer

from .config import Config
from .parser import parse_email_file
from .sender import send

app = typer.Typer(name="mailyou", help="Send an email from the CLI")


@app.command()
def main(
    target: str = typer.Option(
        ...,
        "-t", "--target",
        metavar="FILE",
        help="Path to the email file (.txt or .html)",
    ),
) -> None:
    try:
        config = Config.from_config()
    except (FileNotFoundError, EnvironmentError, ValueError) as exc:
        typer.echo(f"Configuration error: {exc}", err=True)
        raise typer.Exit(code=1)

    try:
        subject, body, content_type = parse_email_file(target)
    except (FileNotFoundError, ValueError) as exc:
        typer.echo(f"Error reading {target!r}: {exc}", err=True)
        raise typer.Exit(code=1)

    try:
        send(subject, body, content_type, config)
    except (FileNotFoundError, ValueError) as exc:
        typer.echo(f"Attachment error: {exc}", err=True)
        raise typer.Exit(code=1)
    except Exception as exc:
        typer.echo(f"Failed to send email: {exc}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
