
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.models_user import User
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

# Register User

@app.route('/register_user', methods=['POST'])
def register_user():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password'],
    }
    valid = User.user_validator(data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data['pw_hash'] = pw_hash
        user = User.create(data)
        session['user_id'] = user
        return redirect('/dashboard')
    return redirect('/')

    # Login

@app.route('/login_user', methods=['POST'])
def login_user():
    user = User.get_my_email(request.form)
    if not user:
        flash('Invalid email or password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

        # Logout

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')