from myproject import app,db,admin
from flask import render_template, redirect, request, url_for, flash,abort, session
from flask_login import login_user,login_required,logout_user
from myproject.models import User,Product,CartItem
from myproject.forms import LoginForm, RegistrationForm, Quantity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView



class MyModlView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaaccessible_callback(self,name, **kwargs):
        return redirect(url_for(login))


admin.add_view(ModelView(Product, db.session))




@app.route('/')
def home():
    form = Quantity()
    data = db.session.execute("Select * from products;")
    itemData =[]

    for r in data:
        itemData.append(r)
    return render_template('home.html',itemData=itemData,form1=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user is not None:
            #Log in the user
            if user.check_password(form.password.data):
                login_user(user)

                # If a user was trying to visit a page that requires a login
                # flask saves that URL as 'next'.
                next = request.args.get('next')

                # So let's now check if that next exists, otherwise we'll go to
                # the welcome page.
                if next == None or not next[0]=='/':
                    next = url_for('home')

                return redirect(next)

            else:
                flash("Wrong Password")
        else:
            flash("Your details not found in DataBase Please SignUp")
    return render_template('Login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if form.check_email(form.email):
            msg = form.check_email(form.email)
            flash(msg)
        else:
            fullname = form.fullname.data
            email = form.email.data
            phone_no = form.phone_no.data
            pwd = form.pwd.data
            country = form.country.data
            user = User(fullname,email,pwd,phone_no,country)

            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering! Now you can login!')
            return redirect(url_for('login'))
        return redirect(url_for('login'))
    return render_template('SignUp.html', form=form)

def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array

	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		print(first_array,'------------item array')
		print(second_array,'-----------session["cart"]')
		res= {**second_array,**first_array}
		return res
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False

@app.route('/add/<pid>', methods=['GET', 'POST'])
@login_required
def add_to_cart(pid):
    itemArray={}
    if request.method == 'POST':
        qunt = int(request.form['quantity'])

        if qunt:
            row = Product.query.filter_by(id=pid).first_or_404()
            p_key=str(row.id)
            itemArray = { p_key : { 'id' : row.id, 'image' : row.image, 'title' : row.title, 'quantity' : qunt, 'price' : row.price,  'total_price': qunt * row.price}}
            print(itemArray)
            all_total_price = 0
            all_total_quantity = 0
            session.modified = True

            try:
                if 'cart_item' in session:
                    if p_key in session['cart_item']:
                        for key, value in session['cart_item'].items():
                            if p_key == key:
                                session['cart_item'][key]['quantity'] = qunt
                                session['cart_item'][key]['total_price'] = qunt * row.price
                    else:
                        print(session['cart_item'],'-----------session cart item')
                        session['cart_item'] = array_merge(itemArray,session['cart_item'])

                    for key, value in session['cart_item'].items():
                        individual_quantity = session['cart_item'][key]['quantity']

                        individual_price = session['cart_item'][key]['total_price']

                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                else:

                    session['cart_item'] = itemArray
                    all_total_quantity = all_total_quantity + qunt
                    all_total_price = all_total_price + qunt * row.price

                session['all_total_quantity'] = all_total_quantity
                session['all_total_price'] = all_total_price

                return redirect(url_for('.home'))
            except :
                pass
        else:
            return 'Error while adding item to cart'
    return redirect(url_for('.home'))

@app.route('/gotocart', methods=['GET', 'POST'])

def gotocart():

    return render_template('cart.html')

@app.route('/empty')
def empty_cart():
	try:
		session['cart_item']={}
		session['all_total_price'] = 0
		session['all_total_quantity'] = 0
		return redirect(url_for('.gotocart'))
	except Exception as e:
		print(e)


@app.route('/delete/<pid>')
def delete_product(pid):

    try:
        pid=str(pid)
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
        for item in session['cart_item'].items():
            if item[0] == pid:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break
        if all_total_quantity == 0:
            session['cart_item']={}
            session['all_total_price'] = 0
            session['all_total_quantity'] = 0
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
        return redirect(url_for('.gotocart'))
    except Exception as e:
        print(e)



@app.route('/checkout',methods=['GET', 'POST'])
def checkout():
    try:
        session['cart_item']={}
        session['all_total_price'] = 0
        session['all_total_quantity'] = 0
        return render_template('checkout.html')

    except Exception as e:
        print(e)
    return redirect(url_for('.home'))

if __name__ == '__main__':
    app.run(debug=True)
