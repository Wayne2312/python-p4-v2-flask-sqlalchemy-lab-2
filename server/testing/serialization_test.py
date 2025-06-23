import pytest
from server.app import app
from server.models import db, Customer, Item, Review

@pytest.fixture(autouse=True)
def setup_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield

class TestCustomer:
    def test_customer_is_serializable(self):
        '''customer is serializable'''
        with app.app_context():
            c = Customer(name="Test Customer")
            db.session.add(c)
            db.session.commit()

            assert c.to_dict() == {
                'id': c.id,
                'name': "Test Customer",
                'reviews': []
            }

class TestItem:
    def test_item_is_serializable(self):
        '''item is serializable'''
        with app.app_context():
            i = Item(name="Test Item", price=1.0)
            db.session.add(i)
            db.session.commit()

            assert i.to_dict() == {
                'id': i.id,
                'name': "Test Item",
                'price': 1.0,
                'reviews': []
            }

class TestReview:
    def test_review_is_serializable(self):
        '''review is serializable'''
        with app.app_context():
            c = Customer(name="Bob")
            i = Item(name="Laptop", price=1500.00)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment="Great laptop!", star_rating=5, customer_id=c.id, item_id=i.id)
            db.session.add(r)
            db.session.commit()

            assert r.to_dict() == {
                'id': r.id,
                'comment': "Great laptop!",
                'star_rating': 5,
                'customer_id': c.id,
                'item_id': i.id,
                'customer': {'id': c.id, 'name': 'Bob'},
                'item': {'id': i.id, 'name': 'Laptop', 'price': 1500.00}
            }
