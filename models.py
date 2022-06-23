from sqlalchemy import true
from app import db, ma
from datetime import date


# Set up database tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(150))
    transactions = db.relationship('Transactions')

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(10))
    amount = db.Column(db.Integer)
    category = db.Column(db.String(20))
    date = db.Column(db.Date, default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Set up database schemas used for json
class TransactionsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transactions
        include_relationships = True
        load_instance = True