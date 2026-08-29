from __future__ import annotations

import smtplib
from email.message import EmailMessage

from .attachment import attach_files, parse_attachments
from .config import Config


def send(subject: str, body: str, content_type: str, config: Config) -> None:
    attachment_paths = parse_attachments(config.mail_attachments)

    msg = EmailMessage()
    msg["From"] = config.mail_from
    msg["To"] = ", ".join(config.mail_to)
    msg["Subject"] = subject

    if config.mail_cc:
        msg["Cc"] = ", ".join(config.mail_cc)

    if config.mail_reply_to:
        msg["Reply-To"] = ", ".join(config.mail_reply_to)

    msg.set_content(body, subtype=content_type)

    if attachment_paths:
        attach_files(msg, attachment_paths)

    all_recipients = config.mail_to + config.mail_cc + config.mail_bcc

    print(f"Connecting to {config.smtp_server}:{config.smtp_port}...")
    with smtplib.SMTP(config.smtp_server, config.smtp_port) as smtp:
        smtp.starttls()
        print("TLS enabled")

        smtp.login(config.smtp_user, config.smtp_pass)
        print("Authenticated")

        smtp.sendmail(config.mail_from, all_recipients, msg.as_string())

    _print_summary(config, attachment_paths)


def _print_summary(config: Config, attachment_paths: list[str]) -> None:
    parts = [f"To: {', '.join(config.mail_to)}"]
    if config.mail_cc:
        parts.append(f"CC: {', '.join(config.mail_cc)}")
    if config.mail_bcc:
        parts.append(f"BCC: {', '.join(config.mail_bcc)}")
    if config.mail_reply_to:
        parts.append(f"Reply-To: {', '.join(config.mail_reply_to)}")
    if attachment_paths:
        parts.append(f"Attachments: {len(attachment_paths)}")
    print(f"Email sent successfully! ({' | '.join(parts)})")
