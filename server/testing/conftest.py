# server/testing/conftest.py

import pytest
from server.app import app, db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
