# Email Sender Skill

Purpose
- Send notification emails using SMTP. Designed to be spec-compliant and safe to test.

Configuration
- `SMTP_HOST` - SMTP server host (optional for dry-run/testing)
- `SMTP_PORT` - SMTP server port (default: 587)
- `SMTP_USER` - SMTP username
- `SMTP_PASS` - SMTP password

API
- `EmailSender.send(subject: str, body: str, to: List[str], dry_run: bool = True) -> dict`
  - Returns metadata: `{sent: bool, dry_run: bool, to: [...], subject: str}` or `{sent: False, error: str}` on failure.

Notes
- The skill defaults to `dry_run=True` to avoid accidental sends during development and testing.
