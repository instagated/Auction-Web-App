from . import db
from datetime import datetime
from flask_login import UserMixin, LoginManager


# DB for User class, contains all relevant attributes
class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    contact_no = db.Column(db.Integer, index=True, nullable=False)
    addr = db.Column(db.String(100), index=True, nullable=False)

    bids = db.relationship('Bid', backref='user')
    watchlists = db.relationship('Watchlist', backref='user')

# DB for Item class, contains all relevant attributes

class Item(db.Model):
    __tablename__='items' 
    id = db.Column(db.Integer, primary_key=True)    
    user_id = db.Column(db.Integer, index=True, nullable=False)
    record_name = db.Column(db.String(100), index=True, nullable=False)
    artist = db.Column(db.String(100), index=True, nullable=False)
    cover = db.Column(db.String(300), index=True, nullable=False)
    genre = db.Column(db.String(100), index=True, nullable=False)
    year = db.Column(db.Integer, index=True, nullable=False)
    description = db.Column(db.String(400), index=True, nullable=True)
    time = db.Column(db.String(100), index=True, nullable=False)
    starting_bid=db.Column(db.Integer, index=True, nullable=False)
    current_bid=db.Column(db.Integer, index=True)

    bids = db.relationship('Bid', backref='item')
    watchlists = db.relationship('Watchlist', backref='item')

    def __repr__(self): #string print method
        return "<Record Name: {}>".format(self.record_name)

# DB for Bid class, contains all relevant attributes

class Bid(db.Model):
    __tablename__='bids' 
    id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Integer, index=True, nullable=False)
    bid_time = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    def __repr__(self):
        return "<Bid: {}>".format(self.amount)

class Watchlist(db.Model):
    __tablename__='watchlists'
    id = db.Column(db.Integer, primary_key=True)    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
