import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    def question_pagination(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page -1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response


    @app.route('/categories')
    def retrive_categories():
        categories = Category.query.all()

        data = {item.id: item.type for item in categories}

        return jsonify({
            'categories': data
        })

    @app.route('/questions')
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = question_pagination(request, selection)

        category_objects = Category.query.order_by(Category.id).all()
        categories = {item.id: item.type for item in category_objects}
        current_categories = [question['category'] for question in current_questions]

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'current_category': current_categories,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': categories
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.filter_by(id=question_id).first()

        if not question:
            return abort(404)
        try:
            question_id = question.id
            question.delete()

            return jsonify({
                "success": True,
                "id": question_id
            })
        except:
            abort(500)

    @app.route('/questions', methods=['POST'])
    def add_question():
        try:
            request_data = request.get_json()
            new_question = Question(**request_data)
            new_question.insert()

            return jsonify({
                "success": True
            })
        except:
            abort(500)


    @app.route('/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search = body.get('searchTerm', None)
        try:
            if search:
                questions =  Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
                current_category = [question.category for question in questions]

                return jsonify({
                    "questions": [question.format() for question in questions.all()],
                    "total_questions": len(questions.all()),
                    "current_category": current_category
                })
            else:
                    abort(404)
        except:
            abort(404)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        try:

            questions = Question.query.order_by(Question.id).filter_by(category=category_id)
            current_category = [question.category for question in questions]

            return jsonify({
                "questions": [question.format() for question in questions.all()],
                "total_questions": len(questions.all()),
                "current_category": current_category
            })

        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        try:
            if quiz_category:
                if quiz_category['id'] == 0:
                    selections = Question.query.all()
                else:
                    selections = Question.query.filter_by(category=quiz_category['id']).all()

            options =  [question.format() for question in selections if question.id not in previous_questions]
            if len(options) == 0:
                return jsonify({
                    'question': False
                })
            result = random.choice(options)
            return jsonify({
                'question': result
            })
        except:
            abort(500)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        })
    return app

    