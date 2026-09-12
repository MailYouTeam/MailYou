from __future__ import annotations

import typer

from .config import Config
from .parser import parse_email_file
from .sender import send

app = typer.Typer(name="mailyou", help="Send an email from the CLI")


@app.command()
def main(
    target: str = typer.Argument(
        ...,
        metavar="FILE",
        help="Path to the email file (e.g. email.txt or email.html)",
    ),
    mail_from: str | None = typer.Option(
        None,
        "--from",
        metavar="SENDER",
        help="Sender name and email address (e.g. John Doe <john@example.com>)",
    ),
    mail_to: list[str] = typer.Option(
        ...,
        "--to",
        metavar="RECIPIENT",
        help="Recipient address (e.g. jane@example.com)",
    ),
    mail_cc: list[str] = typer.Option(
        [],
        "--cc",
        metavar="RECIPIENT",
        help="Cc address (e.g. alice@example.com, bob@example.com)",
    ),
    mail_bcc: list[str] = typer.Option(
        [],
        "--bcc",
        metavar="RECIPIENT",
        help="Bcc address (e.g. mike@example.com)",
    ),
    mail_reply_to: list[str] = typer.Option(
        [],
        "--reply-to",
        metavar="SENDER",
        help="Reply-To address (e.g. sarah@example.com)",
    ),
    mail_attachments: list[str] = typer.Option(
        [],
        "--attach",
        metavar="FILE",
        help="Path to an attachment (e.g. /path/to/file.pdf, /path/to/image.png)",
    ),
) -> None:
    smtp_pass = typer.prompt("SMTP password", hide_input=True)

    try:
        config = Config.from_config(
            smtp_pass=smtp_pass,
            mail_to=mail_to,
            mail_from_override=mail_from,
            mail_cc=mail_cc,
            mail_bcc=mail_bcc,
            mail_reply_to=mail_reply_to,
            mail_attachments=mail_attachments,
        )
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
