# server/app.py
from flask import Flask
from server.models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Add this block to create tables when the app runs directly
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
