from server.app import app
from server.models import db, Customer, Item, Review


class TestAssociationProxy:
    '''Customer in models.py'''

    def test_has_association_proxy(self):
        '''has association proxy to items'''
        with app.app_context():
            c = Customer(name="Test Customer")
            i = Item(name="Test Item", price=1.0)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', star_rating=5, customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            assert hasattr(c, 'items')
            assert i in c.items
