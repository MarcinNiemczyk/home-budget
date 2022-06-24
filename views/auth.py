from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import User
from .. import db


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Sign user up"""

    # Prevent logged user from accessing page 
    if 'user_id' in session:
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        # Get user data from submitted form
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Ensure username length is between 3 and 20 characters
        if len(username) < 3:
            flash("Username is too short", category='error')
            return redirect(url_for('auth.register'))
        if len(username) > 20:
            flash("Username is too long", category='error')
            return redirect(url_for('auth.register'))

        # Ensure entered passwords are matching
        if password != confirm_password:
            flash("Passwords are different", category='error')
            return redirect(url_for('auth.register'))

        # Ensure password is between 6 and 50 characters
        if len(password) < 6:
            flash("Password must be at least 6 characters", category='error')
            return redirect(url_for('auth.register'))
        if len(password) > 50:
            flash("Password is too long", category='error')
            return redirect(url_for('auth.register'))

        # Query database for username
        found_user = User.query.filter_by(username=username).first()

        # Ensure username is available
        if found_user:
            flash("Username already exists", category='error')
            return redirect(url_for('auth.register'))

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
        return redirect(url_for('home.index'))

    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""

    # Prevent logged user from accessing page 
    if 'user_id' in session:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        # Get user data from submitted form
        username = request.form.get('username')
        password = request.form.get('password')

        # Query database for username
        user = User.query.filter_by(username=username).first()

        # Ensure username exists
        if not user:
            flash("User not found", category='error')
            return redirect(url_for('auth.login'))
        
        # Ensure password is correct
        if not check_password_hash(user.password, password):
            flash("Wrong password", category='error')
            return redirect(url_for('auth.login'))
        
        # Remember which user has logged in
        session['user_id'] = user.id
        flash("Successfully logged in!", category='success')

        # Redirect user to home page
        return redirect(url_for('home.index'))

    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    """Log user out"""

    # Ensure user is logged in
    if 'user_id' in session:
        session.clear()
        flash("Successfully logged out", category='success')

    # Redirect user to home page  
    return redirect(url_for('home.index'))
