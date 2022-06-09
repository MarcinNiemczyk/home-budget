from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

DB_NAME = "database.db"
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
    return render_template('layout.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user:
            # TODO: flash message
            print("user not found")
            return render_template('login.html')
        if not check_password_hash(user.password, password):
            # TODO: flash message
            print("wrong password")
            return render_template('login.html')
        
        print("successfully logged in")
        return redirect('/')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(username) < 3:
            # TODO: flash message
            print("username too short")
            return render_template('register.html')
        if len(username) >= 20:
            print("username too long")
            return render_template('register.html')
        if password1 != password2:
            # TODO: flash message
            print("passwords don't match")
            return render_template('register.html')
        if len(password1) < 6:
            # TODO: flash message
            print("password must be at least 6 characters")
            return render_template('register.html')
        if len(password1) >= 50:
            print("password is too long")
            return render_template('register.html')

        found_user = User.query.filter_by(username=username).first()
        if found_user:
             # TODO: flash message
             print("username already exists")
             return render_template('register.html')

        password = generate_password_hash(password1, method='sha256')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        # TODO: flash message
        return redirect('/')

    return render_template('register.html')
