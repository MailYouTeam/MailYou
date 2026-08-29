from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


def _load_addresses(key: str) -> list[str]:
    raw = os.getenv(key, "")
    return [addr.strip() for addr in raw.split(",") if addr.strip()]


def _load_port() -> int:
    raw = os.getenv("SMTP_PORT", "587")
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"SMTP_PORT must be an integer, got: {raw!r}")


@dataclass(frozen=True)
class Config:
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_pass: str
    mail_from: str
    mail_to: list[str]
    mail_cc: list[str] = field(default_factory=list)
    mail_bcc: list[str] = field(default_factory=list)
    mail_reply_to: list[str] = field(default_factory=list)
    mail_attachments: list[str] = field(default_factory=list)

    @classmethod
    def from_env(cls, dotenv_path: str | None = None) -> "Config":
        load_dotenv(dotenv_path)

        smtp_server = os.getenv("SMTP_SERVER", "")
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_pass = os.getenv("SMTP_PASS", "")
        mail_to = _load_addresses("MAIL_TO")

        missing = [
            name
            for name, val in [
                ("SMTP_SERVER", smtp_server),
                ("SMTP_USER", smtp_user),
                ("SMTP_PASS", smtp_pass),
            ]
            if not val
        ] + ([] if mail_to else ["MAIL_TO"])

        if missing:
            raise EnvironmentError(
                f"Missing required .env variable(s): {', '.join(missing)}"
            )

        raw_attachments = os.getenv("MAIL_ATTACHMENTS", "")
        attachment_paths = [p.strip() for p in raw_attachments.split(",") if p.strip()]

        return cls(
            smtp_server=smtp_server,
            smtp_port=_load_port(),
            smtp_user=smtp_user,
            smtp_pass=smtp_pass,
            mail_from=os.getenv("MAIL_FROM", smtp_user),
            mail_to=mail_to,
            mail_cc=_load_addresses("MAIL_CC"),
            mail_bcc=_load_addresses("MAIL_BCC"),
            mail_reply_to=_load_addresses("MAIL_REPLY_TO"),
            mail_attachments=attachment_paths,
        )
