from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo


#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])

    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    contact_number=IntegerField("Contact Number", validators=[InputRequired()])
    address=StringField("Address", validators=[InputRequired()])

    #submit button
    submit = SubmitField("Register")

#Lets user list a record for sale
class ItemForm(FlaskForm):
    record_name = StringField('Record Name', validators=[InputRequired()])

    artist=StringField("Artist", validators=[InputRequired('Enter the title of the record')])

    album_cover=StringField('Album Cover (Paste URL)', validators=[InputRequired()])

    genre=SelectField(u'Genre', choices=[('Pop', 'Pop'), ('Indie', 'Indie'), ('Jazz', 'Jazz'), ('Country', 'Country'), ('Rock', 'Rock'), ('Hip-hop', 'Hip-hop'), ('R & B', 'R & B'), ('Rap', 'Rap'), ('Electronic', 'Electronic'), ('Folk', 'Folk'), ('Classical', 'Classical'), ('Film Score', 'Film score')])

    year=IntegerField("Year", validators=[InputRequired('Enter the year the record was released')])
    
    description=TextAreaField("Album Description", validators=[InputRequired('Enter any interesting facts about the album')])
    
    list_time=SelectField(u'Item List Time', choices=[('1 Day', '1 day'), ('2 Days', '2 days'), ('3 Days', '3 days'), ('4 Days', '4 days'), ('5 Days', '5 days'), ('6 Days', '6 days'), ('7 Days', '7 days'), ('14 Days', '14 days')])
    
    starting_bid=IntegerField("Starting Bid ($)", validators=[InputRequired('Enter the starting bid price for this record')])
    
    submit = SubmitField("Create")

#Lets user place a bid if item is open
class BidForm(FlaskForm):
    bid_amount=IntegerField("Enter your price:", validators=[InputRequired('Enter the year the record was released')])
    submit = SubmitField("Submit Bid")