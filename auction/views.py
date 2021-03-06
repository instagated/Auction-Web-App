from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required
from .models import Item, Bid, Watchlist

mainbp = Blueprint('main', __name__)

# route to allow users to search using search bar
@mainbp.route('/search')
def search():
    #get the search string from request
    if request.args['search']:
        ite = "%" + request.args['search'] + '%'
        #use filter and like function to search for matching destinations
        items = Item.query.filter(Item.record_name.like(ite)).all()
        #render index.html with few destinations
        return render_template('index.html', items=items)
    else:
        return redirect(url_for('main.index'))

# route to allow users to search by category using dropdown menu
@mainbp.route('/cat')
def cat():
    #get the search string from request
    if request.args['cat']:
        ite = "%" + request.args['cat'] + '%'
        #use filter and like function to search for matching destinations
        items = Item.query.filter(Item.genre.like(ite)).all()
        #render index.html with few destinations
        return render_template('index.html', items=items)
    else:
        return redirect(url_for('main.index'))

@mainbp.route('/')
def index():
    items = Item.query.all()
    bids = Bid.query.all()
    return render_template('index.html', items=items, bids=bids)

@mainbp.route('/watchlist')
@login_required #decorator between the route and view function 
def watchlist():
    items = Item.query.all()
    watchlists = Watchlist.query.all()
    return render_template('watchlist.html', items=items, watchlists=watchlists)

@mainbp.route('/user')
def user():
    return render_template('user.html')
