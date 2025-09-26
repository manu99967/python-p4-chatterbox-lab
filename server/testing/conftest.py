import pytest
from server.app import create_app
from models import db

@pytest.fixture(scope='module')
def test_app():
    """Create a Flask app context for testing with a temporary in-memory DB."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
