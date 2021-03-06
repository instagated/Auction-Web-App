from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .models import Item, Bid, Watchlist
from .forms import ItemForm, BidForm
from flask_wtf import FlaskForm
from . import db
from flask_login import login_required, current_user
from .forms import LoginForm,RegisterForm
from sqlalchemy import desc
from .models import User

#Create a blueprint
bp = Blueprint('item', __name__)

#Create a page that will show the details of the item listed by the seller
@bp.route('/<id>') 
def show(id): 
    item = Item.query.filter_by(id=id).first() 
    items = Item.query.all()
    watchlists = Watchlist.query.all()
    bids = Bid.query.all()
    bForm = BidForm()    
    return render_template('details.html', item=item, items=items, bids=bids, watchlists=watchlists, form=bForm)



#Allows seller to list an item for sale
@bp.route('/create', methods = ['GET', 'POST'])
@login_required #decorator between the route and view function 
def create():
    print('Method type: ', request.method)
    form = ItemForm()
    if form.validate_on_submit():
        # if the form was successfully submitted, access form data
        item = Item(user_id=current_user.get_id(), record_name=form.record_name.data, artist=form.artist.data, cover=form.album_cover.data, genre=form.genre.data, year=form.year.data, description=form.description.data, time=form.list_time.data, starting_bid=form.starting_bid.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('item.show', id=item.id))
    return render_template('create.html', form=form)

#Allows user to make a bid on an open item
@bp.route('/<id>', methods = ['GET', 'POST'])
@login_required
def bid(id):
    form = BidForm()
    #get the item object associated to the page and the bid
    item_obj = Item.query.filter_by(id=id).first()
    watch_lists = Watchlist.query.filter_by(user_id=current_user.get_id(), item_id=id).scalar()

    if(not form.validate_on_submit()):
        # Closes the item and selects the highest bidder as the winner
        if request.method == 'POST' and 'form2' in request.form:
            item_obj.time = "Closed"
            db.session.commit()
        elif (request.method == 'POST' and 'form3' in request.form) and not current_user.is_authenticated:
            return redirect(url_for('auth.login'))            
        elif (request.method == 'POST' and 'form3' in request.form) and current_user.is_authenticated:
            if(watch_lists != None):
                flash('This item has already been added to your watchlist!', 'danger')  
                return redirect(url_for('item.show', id=id))
            
            elif(watch_lists == None):                     
                watch = Watchlist(user_id=current_user.get_id(), item_id=id)
                db.session.add(watch)
                db.session.commit()
                flash('The item has been added to your watchlist', 'success')   
                return redirect(url_for('main.watchlist'))                        
        else:
            flash('Error: Your bid must be an integer value (i.e. 20)', 'danger')      
        return redirect(url_for('item.show', id=id))

    if form.validate_on_submit():
        # Newly entered bid
        bid_val = form.bid_amount.data

        # Initial starting price
        start_bid = item_obj.starting_bid

        # Checks if there are any bids already made on the item
        rows = Bid.query.filter(Bid.item_id == id).count() 

        current_user_id = int(current_user.get_id())
        list_user_id = item_obj.user_id
 
        # If no bids made
        if(rows == 0):  
            # Checks bid entered by user against starting price of item       
            if(bid_val <= start_bid):
                flash('Your bid needs to be higher than the STARTING bid!', 'warning')
                return redirect(url_for('item.show', id=id))
        # Checks if user placing a bid is not the user who listed the item
        elif(current_user_id == list_user_id):
            flash('You cannot bid on your own item!', 'danger')
            return redirect(url_for('item.show', id=id))
        else:
            # Gets current item based on item ID
            results = Item.query.filter_by(id=id).first()
            # Checks bid entered by user against highest bid price 
            if(bid_val <= results.current_bid):
                flash('Your bid needs to be higher than the CURRENT bid!', 'warning')
                return redirect(url_for('item.show', id=id))

        # Stores new highest bid into Item class
        new_bid = Item.query.filter_by(id=id).first()
        new_bid.current_bid = form.bid_amount.data
        db.session.commit()



        #read the bid from the form
        bid = Bid(user_id=current_user.get_id(), bid_amount=form.bid_amount.data, item=item_obj)
        db.session.add(bid)
        db.session.commit()   
    flash('Your bid was successfully placed', 'success')      
    return redirect(url_for('item.show', id=id))