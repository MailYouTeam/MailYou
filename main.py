import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

MAIL_FROM = os.getenv("MAIL_FROM", SMTP_USER)
MAIL_TO = os.getenv("MAIL_TO")
MAIL_CC = os.getenv("MAIL_CC", "")
MAIL_BCC = os.getenv("MAIL_BCC", "")
MAIL_REPLY_TO = os.getenv("MAIL_REPLY_TO", "")

EMAIL_FILE = "email.txt"


def parse_addresses(value: str) -> list[str]:
    return [addr.strip() for addr in value.split(",") if addr.strip()]


def parse_email_file(path: str) -> tuple[str, str]:
    if not os.path.exists(path):
        raise ValueError(
            "Email file not found"
        )

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    if len(lines) == 0:
        raise ValueError(
            "File is completely empty"
        )

    subject = lines[0].strip()

    if len(lines) == 1:
        return subject, ""

    if lines[1].strip() != "":
        raise ValueError(
            "Line 2 must be completely blank"
        )

    body = "\n".join(lines[2:]).strip()

    return subject, body


def main():
    if not all([SMTP_SERVER, SMTP_USER, SMTP_PASS, MAIL_TO]):
        raise RuntimeError("Missing SMTP configuration in .env")

    try:
        subject, body = parse_email_file(EMAIL_FILE)
    except ValueError as e:
        print(f"Error reading '{EMAIL_FILE}':\n{e}")
        return

    to_addrs = parse_addresses(MAIL_TO)
    cc_addrs = parse_addresses(MAIL_CC)
    bcc_addrs = parse_addresses(MAIL_BCC)
    reply_to_addrs = parse_addresses(MAIL_REPLY_TO)

    msg = EmailMessage()
    msg["From"] = MAIL_FROM
    msg["To"] = ", ".join(to_addrs)
    msg["Subject"] = subject

    if cc_addrs:
        msg["Cc"] = ", ".join(cc_addrs)

    if reply_to_addrs:
        msg["Reply-To"] = ", ".join(reply_to_addrs)


    msg.set_content(body)

    all_recipients = to_addrs + cc_addrs + bcc_addrs

    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        print("TLS enabled")

        smtp.login(SMTP_USER, SMTP_PASS)
        print("Authenticated")

        smtp.sendmail(MAIL_FROM, all_recipients, msg.as_string())

        summary = f"To: {', '.join(to_addrs)}"
        if cc_addrs:
            summary += f" | CC: {', '.join(cc_addrs)}"
        if bcc_addrs:
            summary += f" | BCC: {', '.join(bcc_addrs)}"
        if reply_to_addrs:
            summary += f" | Reply-To: {', '.join(reply_to_addrs)}"
        print(f"Email sent successfully! ({summary})")


if __name__ == "__main__":
    main()
