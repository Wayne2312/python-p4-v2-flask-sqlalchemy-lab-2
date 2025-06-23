from server.app import app
from server.models import db, Customer, Item, Review


import pytest

class TestReview:
    '''Review model in models.py'''

    @pytest.fixture(autouse=True, scope='function')
    def setup_and_teardown(self):
        with app.app_context():
            db.create_all()
            yield
            db.session.remove()
            db.drop_all()

    def test_can_be_instantiated(self):
        '''can be invoked to create a Python object.'''
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        '''can be instantiated with a comment attribute.'''
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self):
        '''can be added to a transaction and committed to review table with comment column.'''
        with app.app_context():
            assert 'comment' in Review.__table__.columns
            # Provide all required fields
            c = Customer(name="Test Customer")
            i = Item(name="Test Item", price=1.0)
            db.session.add_all([c, i])
            db.session.commit()
            r = Review(comment='great!', star_rating=5, customer_id=c.id, item_id=i.id)
            db.session.add(r)
            db.session.commit()

    def test_is_related_to_customer_and_item(self):
        '''has foreign keys and relationships'''
        with app.app_context():
            assert 'customer_id' in Review.__table__.columns
            assert 'item_id' in Review.__table__.columns

            c = Customer(name="Test Customer")
            i = Item(name="Test Item", price=1.0)
            db.session.add_all([c, i])
            db.session.commit()
            r = Review(comment='nice', star_rating=4, customer_id=c.id, item_id=i.id)
            db.session.add(r)
            db.session.commit()
            assert r.customer == c
            assert r.item == i
