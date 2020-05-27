from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.Text)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    phone_no = db.Column(db.Integer)
    country = db.Column(db.String(64))

    def __init__(self, fullname, email,  password_hash, phone_no, country):
        self.fullname = fullname
        self.email = email
        self.password_hash = generate_password_hash(password_hash)
        self.phone_no = phone_no
        self.country = country

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)



class Product(db.Model):

    __tablename__ = 'products'

    id=db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String(64))
    title=db.Column(db.String(64))
    description=db.Column(db.String(128))
    price=db.Column('price', db.Integer)
    cartitems = db.relationship('CartItem', backref='Cart.id', lazy='dynamic')


    def __init__(self, image, title,description, price):
        self.image = image
        self.title = title
        self.description = description
        self.price = price

class CartItem(db.Model):

    __tablename__='Cart'
    id = db.Column(db.Integer,primary_key=True)
    # adding the foreign key
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
