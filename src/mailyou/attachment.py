from __future__ import annotations

import mimetypes
import os
from email.message import EmailMessage


def parse_attachments(paths: list[str]) -> list[str]:
    for path in paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Attachment not found: {path!r}")
        if not os.path.isfile(path):
            raise ValueError(f"Attachment path is not a file: {path!r}")
    return paths


def attach_files(msg: EmailMessage, paths: list[str]) -> None:
    for path in paths:
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type is None:
            mime_type = "application/octet-stream"
        maintype, subtype = mime_type.split("/", 1)
        filename = os.path.basename(path)
        with open(path, "rb") as fh:
            msg.add_attachment(
                fh.read(),
                maintype=maintype,
                subtype=subtype,
                filename=filename,
            )
        print(f"Attached: {filename} ({mime_type})")
