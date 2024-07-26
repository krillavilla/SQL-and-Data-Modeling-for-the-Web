import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

# Ensure models.py is correctly referenced
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        # Set the default database path with the correct password
        database_path = 'postgresql://krillavilla:1234@localhost:5432/trivia_test'
    else:
        # Use the test configuration database path
        database_path = test_config.get('DATABASE_URL',
                                        'postgresql://krillavilla:1234@localhost:5432/trivia_test')

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''

    CORS(app, resource={r" /*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def app_after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    @TODO: Create an endpoint to handle GET requests for all available categories.
    '''

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        categories_dict = {category.id: category.type for category in categories}
        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    '''
    @TODO: Create an endpoint to handle GET requests for questions, including pagination (every 10 questions).
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions[start:end]]
        categories = Category.query.all()
        categories_dict = {category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'categories': categories_dict,
            'current_category': None
        })

    '''
    @TODO: Create an endpoint to DELETE question using a question ID.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

    '''
    @TODO: Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(question=new_question, answer=new_answer, category=new_category,
                                difficulty=new_difficulty)
            question.insert()
            return jsonify({
                'success': True,
                'created': question.id,
            })
        except:
            abort(422)

    '''
    @TODO: Create a POST endpoint to get questions based on a search term.
    '''

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': None
        })

    '''
    @TODO: Create a GET endpoint to get questions based on category.
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': category_id
        })

    '''
    @TODO: Create a POST endpoint to get questions to play the quiz.
    '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        if quiz_category is None or quiz_category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(Question.category == quiz_category['id']).all()

        formatted_questions = [question.format() for question in questions]
        remaining_questions = [question for question in formatted_questions if question['id'] not in previous_questions]

        if len(remaining_questions) == 0:
            return jsonify({
                'success': True,
                'question': None
            })

        question = random.choice(remaining_questions)

        return jsonify({
            'success': True,
            'question': question
        })

    '''
    @TODO: Create error handlers for all expected errors including 404 and 422.
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    return app
