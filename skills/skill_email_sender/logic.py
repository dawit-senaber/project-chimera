import os
import smtplib
from email.message import EmailMessage
from typing import List, Optional


class EmailSender:
    """A small, spec-compliant email sender skill.

    Configuration through environment variables:
    - SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS

    The `send` method supports `dry_run=True` (default) so tests
    can validate behavior without sending real emails.
    """

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = True,
    ):
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST")
        self.smtp_port = int(smtp_port or os.getenv("SMTP_PORT", 587))
        self.user = user or os.getenv("SMTP_USER")
        self.password = password or os.getenv("SMTP_PASS")
        self.use_tls = use_tls

    def send(self, subject: str, body: str, to: List[str], dry_run: bool = True) -> dict:
        """Send an email or simulate sending when `dry_run=True`.

        Returns a dict with `sent` boolean and metadata for auditing.
        """
        if not isinstance(to, (list, tuple)):
            raise TypeError("`to` must be a list of recipient email addresses")

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.user or "no-reply@example.com"
        msg["To"] = ", ".join(to)
        msg.set_content(body)

        if dry_run or not self.smtp_host:
            return {"sent": False, "dry_run": True, "to": to, "subject": subject}

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as smtp:
                if self.use_tls:
                    smtp.starttls()
                if self.user and self.password:
                    smtp.login(self.user, self.password)
                smtp.send_message(msg)
            return {"sent": True, "dry_run": False, "to": to, "subject": subject}
        except Exception as e:
            return {"sent": False, "error": str(e)}
