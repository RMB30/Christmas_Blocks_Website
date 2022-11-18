from flask_app import app
from flask import flash
from flask_app.models.models_user import User
from flask_app.config.mysqlconnection import connectToMySQL
import re

db = 'christmas_blocks_db'

class Score:

    def __init__(self, data):
        self.id = data['id']
        self.high_score = data['high_score']
        self.date_achieved = data['date_achieved']
        self.user_id = data['user_id']
        self.owner = None

    @classmethod
    def create_score(cls, data):
        query = """
                INSERT INTO scores (high_score, date_achieved, user_id ) 
                VALUES (%(high_score)s, %(date_achieved)s, %(user_id)s )
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def all_scores(cls):
        query = 'SELECT * FROM scores'
        results = connectToMySQL(db).query_db(query)
        scores = []
        for score in results:
            scores.append(cls(score))
        return scores


    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM scores JOIN users on users.id = scores.user_id WHERE scores.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        score = cls(results[0])
        owner_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at'],
        }
        score.owner = User(owner_data)
        return score

    @classmethod
    def update_score(cls, form_data, score_id):
        query = f"UPDATE scores SET high_score = %(high_score)s, date_achieved = %(date_achieved)s WHERE id = {score_id} "
        return connectToMySQL(db).query_db(query, form_data)

        # Delete a Score
    @classmethod
    def delete(cls, data):
        query = """
                DELETE FROM scores WHERE id = %(id)s
                """
        return connectToMySQL(db).query_db(query, data)


        # Score Validator

    @staticmethod
    def score_validator(data):
        is_valid = True
        if len(data['high_score']) < 0:
            flash('High Score must be greater than the 0 seconds')
            is_valid = False
        if len(data['date_achieved']) < 1:
            flash('Date Achieved must be greater than 0')
            is_valid = False
        return is_valid
