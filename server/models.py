from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    star_rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship("Customer", back_populates="reviews")
    item = db.relationship("Item", back_populates="reviews")

    serialize_rules = ('-customer.reviews', '-item.reviews')

    @validates('star_rating')
    def validate_star_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Star rating must be between 1 and 5")
        return rating


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    reviews = db.relationship("Review", back_populates="customer", cascade="all, delete-orphan")
    items = association_proxy("reviews", "item")

    serialize_rules = ('-reviews.customer',)


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    reviews = db.relationship("Review", back_populates="item", cascade="all, delete-orphan")
    customers = association_proxy("reviews", "customer")

    serialize_rules = ('-reviews.item',)
