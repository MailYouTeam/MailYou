from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

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
    def from_config(
        cls,
        smtp_pass: str,
        mail_to: list[str],
        mail_from_override: str | None = None,
        mail_cc: list[str] | None = None,
        mail_bcc: list[str] | None = None,
        mail_reply_to: list[str] | None = None,
        mail_attachments: list[str] | None = None,
    ) -> "Config":
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

        toml_mail_from = smtp.get("mail_from", smtp_user)
        mail_from = mail_from_override if mail_from_override else toml_mail_from

        return cls(
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_pass=smtp_pass,
            mail_from=mail_from,
            mail_to=mail_to,
            mail_cc=mail_cc or [],
            mail_bcc=mail_bcc or [],
            mail_reply_to=mail_reply_to or [],
            mail_attachments=mail_attachments or [],
        )
