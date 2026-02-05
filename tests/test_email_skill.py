import pytest
from skills.skill_email_sender.logic import EmailSender


def test_email_sender_dry_run_returns_metadata():
    sender = EmailSender(smtp_host=None)  # force dry-run behavior
    res = sender.send(
        subject="Test",
        body="This is a test.",
        to=["user@example.com"],
        dry_run=True,
    )
    assert isinstance(res, dict)
    assert res.get("dry_run") is True
    assert res.get("sent") is False
    assert res.get("to") == ["user@example.com"]


def test_email_sender_validation_of_recipients():
    sender = EmailSender()
    with pytest.raises(TypeError):
        sender.send("s", "b", to="not-a-list")
