from __future__ import annotations

import argparse
import sys

from .config import Config
from .parser import parse_email_file
from .sender import send


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mailyou",
        description="Send an email from the CLI",
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        metavar="FILE",
        help="Path to the email file (.txt or .html)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        config = Config.from_env()
    except (EnvironmentError, ValueError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1

    try:
        subject, body, content_type = parse_email_file(args.target)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error reading {args.target!r}: {exc}", file=sys.stderr)
        return 1

    try:
        send(subject, body, content_type, config)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Attachment error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Failed to send email: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
