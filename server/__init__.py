import pytest
from server.app import app
from server.config import db
from server.models import Customer, Item, Review

def test_customer_serialization():
    with app.app_context():
        db.drop_all()
        db.create_all()