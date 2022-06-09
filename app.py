from flask import Flask, redirect, render_template, request, session, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

DB_NAME = "database.db"

# TODO: Change it to env variable
app.config['SECRET_KEY'] = 'supersecretkeythatnobodycansee'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

db.create_all()
db.session.commit()

@app.route('/')
def index():
    if not 'user_id' in session:
        return redirect('/login')
    return render_template('layout.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("User not found", category='error')
            return render_template('login.html')
        if not check_password_hash(user.password, password):
            flash("Wrong password", category='error')
            return render_template('login.html')
        
        session['user_id'] = user.id
        flash(f"Successfully logged in!", category='success')
        return redirect('/')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect('/')

    if request.method == 'POST':

        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(username) < 3:
            flash("Username is too short", category='error')
            return render_template('register.html')
        if len(username) >= 20:
            flash("Username is too long", category='error')
            return render_template('register.html')
        if password1 != password2:
            flash("Passwords don't match", category='error')
            return render_template('register.html')
        if len(password1) < 6:
            flash("Password must be at least 6 characters", category='error')
            return render_template('register.html')
        if len(password1) >= 50:
            flash("Password is too long", category='error')
            return render_template('register.html')

        found_user = User.query.filter_by(username=username).first()
        if found_user:
            flash("Username already exists", category='error')
            return render_template('register.html')

        password = generate_password_hash(password1, method='sha256')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        flash("Successfully registered!", category='success')
        return redirect('/')

    return render_template('register.html')


@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.clear()
        flash("Successfully logged out", category='success')
    return redirect('/')
