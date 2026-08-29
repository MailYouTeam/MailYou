from __future__ import annotations

import os

_SUPPORTED_EXTENSIONS: dict[str, str] = {
    ".txt": "plain",
    ".html": "html",
}


def parse_email_file(path: str) -> tuple[str, str, str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Email file not found: {path!r}")

    ext = os.path.splitext(path)[1].lower()
    content_type = _SUPPORTED_EXTENSIONS.get(ext)
    if content_type is None:
        supported = ", ".join(_SUPPORTED_EXTENSIONS)
        raise ValueError(
            f"Unsupported file extension {ext!r}. Supported: {supported}"
        )

    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    if not lines:
        raise ValueError("Email file is completely empty")

    subject = lines[0].strip()

    if len(lines) == 1:
        return subject, "", content_type

    if lines[1].strip() != "":
        raise ValueError(
            "Line 2 must be completely blank"
        )

    body = "\n".join(lines[2:])

    return subject, body, content_type
