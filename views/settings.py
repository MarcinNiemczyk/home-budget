from flask import Blueprint, flash, request, render_template, redirect, session, url_for 
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import login_required, User
from .. import db


settings = Blueprint('settings', __name__)

@settings.route('/settings')
@login_required
def settings_page():
    """Show settings menu"""

    return render_template('settings/settings.html')


@settings.route('/settings/change-password', methods=['GET', 'POST'])
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
            return redirect(url_for('settings.password'))
        if new_password != confirmed_password:
            flash("Passwords are different", category='error')
            return redirect(url_for('settings.password'))
        if len(new_password) < 6:
            flash("Password is too short", category='error')
            return redirect(url_for('settings.password'))
        if len(new_password) > 50:
            flash("Password is too long", category='error')
            return redirect(url_for('settings.password'))
        if check_password_hash(user.password, new_password):
            flash("New password must be different", category='error')
            return redirect(url_for('settings.password'))
   
        # Update password in database
        user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()

        # Redirect user back to settings
        flash("Password has been changed", category='success')
        return redirect(url_for('settings.settings_page'))

    return render_template('settings/change-password.html')


@settings.route('/settings/remove-account', methods=['GET', 'POST'])
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
            return redirect(url_for('settings.remove'))
        
        # Remove user from database
        User.query.filter_by(id=user.id).delete()
        db.session.commit()

        # Forget session id and redirect user to login form
        session.clear()
        flash("Account has been removed", category='success')
        return redirect(url_for('auth.login'))

    return render_template('settings/remove-account.html')


@settings.route('/settings/currency')
@login_required
def currency():
    """Change displaying currency on page"""

    flash("This feature is currently unavailable", category='error')
    return redirect(url_for('home.index'))