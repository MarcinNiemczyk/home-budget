from flask import Flask, redirect, render_template, request, session, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Name database
DB_NAME = "database.db"

# Configure database
app.config['SECRET_KEY'] = 'supersecretkeythatnobodycansee'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
db = SQLAlchemy(app)

# Set up database tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create database
db.create_all()
db.session.commit()

@app.route('/')
def index():
    """Display overview of user's monthly expenses"""

    # Ensure user is logged in
    if not 'user_id' in session:
        # Redirect not logged user to login form
        return redirect('/login')

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
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Ensure username length is between 3 and 20 characters
        if len(username) <= 3:
            flash("Username is too short", category='error')
            return render_template('register.html')
        if len(username) >= 20:
            flash("Username is too long", category='error')
            return render_template('register.html')

        # Ensure entered passwords are matching
        if password1 != password2:
            flash("Passwords don't match", category='error')
            return render_template('register.html')

        # Ensure password is between 6 and 50 characters
        if len(password1) <= 6:
            flash("Password must be at least 6 characters", category='error')
            return render_template('register.html')
        if len(password1) >= 50:
            flash("Password is too long", category='error')
            return render_template('register.html')

        # Query database for username
        found_user = User.query.filter_by(username=username).first()

        # Ensure username is available
        if found_user:
            flash("Username already exists", category='error')
            return render_template('register.html')

        # Generate password hash
        password = generate_password_hash(password1, method='sha256')

        # Create user model
        user = User(username=username, password=password)

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
def settings():
    """Show settings menu"""

    # Ensure user is logged in
    if not 'user_id' in session:
        # Redirect not logged user to login form
        return redirect('/login')

    return render_template('settings.html')

