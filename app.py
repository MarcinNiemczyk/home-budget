from multiprocessing.sharedctypes import Value
from flask import Flask, redirect, render_template, request, session, flash, get_flashed_messages, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import func, extract
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import TRANSACTION_TYPES, YEARS, login_required, CATEGORIES, MONTHS
from datetime import date, datetime
import json


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure database
DB_NAME = "database.db"
app.config['SECRET_KEY'] = 'supersecretkeythatnobodycansee'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import User, Transactions,TransactionsSchema

# Create database
db.create_all()
db.session.commit()


@app.route('/')
@login_required
def index():
    """Display overview of user's monthly expenses"""

    return render_template('layout.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""

    # Prevent logged user from accessing page 
    if 'user_id' in session:
        return redirect('/')

    if request.method == 'POST':
        # Get user data from submitted form
        username = request.form.get('username')
        password = request.form.get('password')

        # Query database for username
        user = User.query.filter_by(username=username).first()

        # Ensure username exists
        if not user:
            flash("User not found", category='error')
            return render_template('login.html')
        
        # Ensure password is correct
        if not check_password_hash(user.password, password):
            flash("Wrong password", category='error')
            return render_template('login.html')
        
        # Remember which user has logged in
        session['user_id'] = user.id
        flash("Successfully logged in!", category='success')

        # Redirect user to home page
        return redirect('/')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Sign user up"""

    # Prevent logged user from accessing page 
    if 'user_id' in session:
        return redirect('/')

    if request.method == 'POST':
        # Get user data from submitted form
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Ensure username length is between 3 and 20 characters
        if len(username) < 3:
            flash("Username is too short", category='error')
            return render_template('register.html')
        if len(username) > 20:
            flash("Username is too long", category='error')
            return render_template('register.html')

        # Ensure entered passwords are matching
        if password != confirm_password:
            flash("Passwords are different", category='error')
            return render_template('register.html')

        # Ensure password is between 6 and 50 characters
        if len(password) < 6:
            flash("Password must be at least 6 characters", category='error')
            return render_template('register.html')
        if len(password) > 50:
            flash("Password is too long", category='error')
            return render_template('register.html')

        # Query database for username
        found_user = User.query.filter_by(username=username).first()

        # Ensure username is available
        if found_user:
            flash("Username already exists", category='error')
            return render_template('register.html')

        # Generate password hash
        hash = generate_password_hash(password, method='sha256')

        # Create user model
        user = User(username=username, password=hash)

        # Add user to database
        db.session.add(user)
        db.session.commit()
        
        # Log registered user in
        session['user_id'] = user.id
        flash("Successfully registered!", category='success')

        # Redirect user to home page
        return redirect('/')

    return render_template('register.html')


@app.route('/logout')
def logout():
    """Log user out"""

    # Ensure user is logged in
    if 'user_id' in session:
        session.clear()
        flash("Successfully logged out", category='success')

    # Redirect user to home page  
    return redirect('/')


@app.route('/settings')
@login_required
def settings():
    """Show settings menu"""

    return render_template('settings.html')


@app.route('/settings/change-password', methods=['GET', 'POST'])
@login_required
def password():
    """Change user password"""

    if request.method == 'POST':
        # Get data from submitted form
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirmed_password = request.form.get('confirmed_password')

        # Query database for logged user
        user = User.query.filter_by(id=session['user_id']).first()

        # Ensure passwords are correct
        if not check_password_hash(user.password, old_password):
            flash("Wrong password", category='error')
            return render_template('password.html')
        if new_password != confirmed_password:
            flash("Passwords are different", category='error')
            return render_template('password.html')
        if len(new_password) < 6:
            flash("Password is too short", category='error')
            return render_template('password.html')
        if len(new_password) > 50:
            flash("Password is too long", category='error')
            return render_template('password.html')
        if check_password_hash(user.password, new_password):
            flash("New password must be different", category='error')
            return render_template('password.html')
   
        # Update password in database
        user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()

        # Redirect user back to settings
        flash("Password has been changed", category='success')
        return redirect('/settings')

    return render_template('change-password.html')


@app.route('/settings/remove-account', methods=['GET', 'POST'])
@login_required
def remove():
    """Remove user account"""

    if request.method == 'POST':
        # Get data from submitted form
        password = request.form.get('password')

        # Query database for logged user
        user = User.query.filter_by(id=session['user_id']).first()

        # Ensure password is correct
        if not check_password_hash(user.password, password):
            flash("Invalid password", category='error')
            return render_template('remove.html')
        
        # Remove user from database
        User.query.filter_by(id=user.id).delete()
        db.session.commit()

        # Forget session id and redirect user to login form
        session.clear()
        flash("Account has been removed", category='success')
        return redirect('/login')

    return render_template('remove-account.html')


@app.route('/settings/currency')
@login_required
def currency():
    """Change displaying currency on page"""

    flash("This feature is currently unavailable", category='error')
    return redirect('/')

@app.route('/transactions', defaults={'year': datetime.today().year, 'month': datetime.today().month, 'transaction_type': 'all'})
@app.route('/transactions/<int:year>/<int:month>/<transaction_type>', methods=['GET', 'POST'])
@login_required
def transactions(year, month, transaction_type):
    """Show usertransactions and allow him to modify data."""

    # Prevent user to access wrong page
    if month < 1 or month > 12:
        flash('Invalid month', category='error')
        return redirect('/transactions')
    if year < min(YEARS) or year > max(YEARS):
        flash('Invalid year', category='error')
        return redirect('/transactions')
    if transaction_type not in TRANSACTION_TYPES:
        flash('Invalid transaction type', category='error')
        return redirect('/transactions')

    # Get search input
    search_text = request.args.get('q')

    # Get logged user transactions data
    transactions = Transactions.query.filter_by(user_id=session['user_id'])

    # Query for applied month
    transactions = transactions.filter(extract('month', Transactions.date)==month)

    # Query for applied year
    transactions = transactions.filter(extract('year', Transactions.date)==year)

    # Handle transaction type
    if not transaction_type == 'all':
        transactions = transactions.filter_by(type=transaction_type)

    # Handle search functionality
    if search_text:
        transactions = transactions.filter(Transactions.name.like((f'%{search_text}%')))

    # Apply selected filters
    transactions = transactions.all()

    # Ensure text is inside input and handle request
    if search_text is not None:
        transactions_schema = TransactionsSchema()
        output = transactions_schema.dump(transactions, many=True)
        return jsonify(output)

    print(transactions)
    return render_template('transactions.html', transactions=transactions, months=MONTHS, years=YEARS, 
           transaction_types=TRANSACTION_TYPES, selected_month=month, selected_year=year, selected_type=transaction_type)


@app.route('/transactions/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    """Add or modify transactions"""

    if request.method == 'POST':
        # Validate date input
        date_input = request.form.get('date')
        if len(date_input) != 10:
            flash('Incorrect date', category='error')
            return redirect('/transactions/add')
        try:
            year = int(date_input[0:4])
            month = int(date_input[5:7])
            day = int(date_input[8:10])
        except (TypeError, ValueError):
            flash('Incorrect date', category='error')
            return redirect('/transactions/add')
        if year < min(YEARS) or year > max(YEARS):
            flash('Incorrect date', category='error')
            return redirect('/transactions/add')
        date_output = date(year, month, day)

        # Validate type input
        transaction_type = request.form.get('transaction_type')
        if transaction_type != 'outcome' and transaction_type != 'income':
            flash('Incorrect transaction type', category='error')
            return redirect('/transactions/add')

        # Validate name input
        name = request.form.get('name')
        if len(name) < 2:
            flash('Name is too short', category='error')
            return redirect('/transactions/add')
        if len(name) > 99:
            flash('Name is too long', category='error')
            return redirect('/transactions/add')

        # Validate amount input
        amount = request.form.get('amount')
        try:
            amount = float(amount)
            amount = round(amount)
        except (TypeError, ValueError):
            flash('Incorrect amount', category='error')
            return redirect('/transactions/add')
        if amount <= 0 or amount > 9999999:
            flash('Incorrect amount', category='error')
            return redirect('/transactions/add')

        # Validate transaction category input
        category = request.form.get('category')
        if transaction_type == 'outcome' and category not in CATEGORIES['outcomes']:
            flash('Incorrect category', category='error')
            return redirect('/transactions/add')
        if transaction_type == 'income' and category not in CATEGORIES['incomes']:
            flash('Incorrect category', category='error')
            return redirect('/transactions/add')

        # Create new transaction and add it to database
        new_transaction = Transactions(name=name, type=transaction_type, amount=amount, category=category, date=date_output, user_id = session['user_id'])
        db.session.add(new_transaction)
        db.session.commit()
        flash('Transaction added!', category='success')

    today = date.today()

    return render_template('add-transaction.html', outcomes=CATEGORIES['outcomes'], incomes=CATEGORIES['incomes'], today=today)


@app.route('/remove-transaction', methods=['POST'])
@login_required
def remove_transaction():
    """Removes selected transaction"""
    transaction = json.loads(request.data)
    transactionId = transaction['transactionId']
    transaction = Transactions.query.get(transactionId)
    if transaction:
        if transaction.user_id == session['user_id']:
            db.session.delete(transaction)
            db.session.commit()

    return jsonify({})
