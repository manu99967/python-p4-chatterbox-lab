import pytest
from server.app import create_app, db
from server.models import Message

@pytest.fixture
def test_app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # in-memory DB for tests
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def init_message(test_app):
    """Create a temporary message for testing and clean up after."""
    message = Message(body="Hello 👋", username="Liza")
    db.session.add(message)
    db.session.commit()
    yield message
    db.session.delete(message)
    db.session.commit()

def test_message_creation(init_message):
    """Check that a message is created correctly."""
    assert init_message.id is not None
    assert init_message.body == "Hello 👋"
    assert init_message.username == "Liza"


