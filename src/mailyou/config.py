from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from platformdirs import user_config_dir

_CONFIG_DIR = Path(user_config_dir("mailyou"))
_CONFIG_FILE = _CONFIG_DIR / "config.toml"


def _read_toml_smtp() -> dict:
    if not _CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Config file not found: {_CONFIG_FILE}"
        )
    with open(_CONFIG_FILE, "rb") as fh:
        data = tomllib.load(fh)
    return data.get("smtp", {})


def _load_addresses(key: str) -> list[str]:
    raw = os.getenv(key, "")
    return [addr.strip() for addr in raw.split(",") if addr.strip()]


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
    def from_config(cls, dotenv_path: str | None = None) -> "Config":
        smtp = _read_toml_smtp()

        smtp_server = smtp.get("server", "")
        smtp_user = smtp.get("user", "")

        raw_port = smtp.get("port", 587)
        try:
            smtp_port = int(raw_port)
        except (TypeError, ValueError):
            raise ValueError(f"[smtp] port must be an integer, got: {raw_port!r}")

        missing_toml = [
            name
            for name, val in [("server", smtp_server), ("user", smtp_user)]
            if not val
        ]
        if missing_toml:
            raise ValueError(
                f"Missing required [smtp] key(s) in {_CONFIG_FILE}: "
                f"{', '.join(missing_toml)}"
            )

        load_dotenv(dotenv_path)

        smtp_pass = os.getenv("SMTP_PASS", "")
        mail_to = _load_addresses("MAIL_TO")

        missing_env = (
            ["SMTP_PASS"] if not smtp_pass else []
        ) + ([] if mail_to else ["MAIL_TO"])

        if missing_env:
            raise EnvironmentError(
                f"Missing required .env variable(s): {', '.join(missing_env)}"
            )

        raw_attachments = os.getenv("MAIL_ATTACHMENTS", "")
        attachment_paths = [p.strip() for p in raw_attachments.split(",") if p.strip()]

        return cls(
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_pass=smtp_pass,
            mail_from=os.getenv("MAIL_FROM", smtp_user),
            mail_to=mail_to,
            mail_cc=_load_addresses("MAIL_CC"),
            mail_bcc=_load_addresses("MAIL_BCC"),
            mail_reply_to=_load_addresses("MAIL_REPLY_TO"),
            mail_attachments=attachment_paths,
        )
