import pytest
from models import db, Message

def test_message_creation(test_app):
    """Check that a message is created correctly."""
    msg = Message(body="Hello", username="Tester")
    db.session.add(msg)
    db.session.commit()

    # Use Session.get() instead of legacy Query.get()
    retrieved = db.session.get(Message, msg.id)
    assert retrieved is not None
    assert retrieved.body == "Hello"
    assert retrieved.username == "Tester"

def test_message_columns(test_app):
    """Check that Message has required columns."""
    msg = Message(body="Check columns", username="Tester")
    db.session.add(msg)
    db.session.commit()

    retrieved = db.session.get(Message, msg.id)
    assert hasattr(retrieved, "id")
    assert hasattr(retrieved, "body")
    assert hasattr(retrieved, "username")
    assert hasattr(retrieved, "created_at")

def test_message_deletion(test_app):
    """Check that a message can be deleted."""
    msg = Message(body="Delete me", username="Tester")
    db.session.add(msg)
    db.session.commit()

    db.session.delete(msg)
    db.session.commit()

    assert db.session.get(Message, msg.id) is None



