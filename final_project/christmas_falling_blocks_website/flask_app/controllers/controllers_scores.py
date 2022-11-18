

from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.models_user import User
from flask_app.models.models_score import Score

from flask_app.config.mysqlconnection import connectToMySQL

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    user = User.get_one(user_data)
    all = Score.all_scores()
    return render_template('dashboard.html', user = user, all = all)

    # Add a score page

@app.route('/add_score')
def add_score():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_score.html')

    # Create a Score

@app.route('/create_score', methods=['POST'])
def create_score():
    data = {
        'high_score': request.form['high_score'],
        'date_achieved': request.form['date_achieved'],
        'user_id': session['user_id'],
    }
    valid = Score.score_validator(data)
    if valid:
        Score.create_score(data)
        return redirect('/dashboard')
    return redirect('/add_score')

    # Edit Score Page
@app.route('/edit_score/<int:score_id>')
def edit_score(score_id):
    data = {
        'id' : score_id
    }
    score = Score.get_one(data)
    return render_template('edit_score.html', score = score)

    # Update Score
@app.route('/update_score/<int:score_id>', methods=['POST'])
def update_score(score_id):
    data = {
        'high_score': request.form['high_score'],
        'date_achieved': request.form['date_achieved'],
        'user_id': session['user_id'],
    }
    valid = Score.score_validator(data)
    if valid:
        Score.update_score(request.form, score_id)
        return redirect('/dashboard')
    return redirect('/dashboard')

    # Show Score
@app.route('/one_score')
def show_score():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('one_score.html')

    # Show Owner
@app.route('/show_owner/<int:score_id>')
def show_owner(score_id):
    data = {
        'id' : score_id
    }
    score = Score.get_one(data)
    return render_template('show_owner.html', score = score)

    # Delete a Score
@app.route('/delete/<int:score_id>')
def delete(score_id):
    data = {
        'id' : score_id
    }
    Score.delete(data)
    return redirect('/dashboard')


