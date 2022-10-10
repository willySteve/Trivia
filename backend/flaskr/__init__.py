import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def pagination(request, whole_objects):
    # get the page number to render..
    page = request.args.get("page", 1, type=int)
    begin = (page - 1) * QUESTIONS_PER_PAGE
    end = begin + QUESTIONS_PER_PAGE

    # format the objects to be rendered..
    formated = [obj.format() for obj in whole_objects]
    return formated[begin:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, origins=['*'])

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()
        format_categories = {}
        for c in categories:
            format_categories[c.id] = c.type

        if len(format_categories) == 0:
            # no category found..
            abort(404)

        return jsonify({
            'success': True,
            'categories': format_categories
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def retrieve_questions():
        questions = Question.query.order_by(Question.id).all()
        filtered_questions = pagination(request, questions)

        categories = Category.query.order_by(Category.id).all()
        format_categories = {}
        for c in categories:
            format_categories[c.id] = c.type

        if len(questions) == 0:
            # no questions found..
            abort(404)

        return jsonify({
            'success': True,
            'questions': filtered_questions,
            'total_questions': len(questions),
            'categories': format_categories,
            'current_category': None
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=["DELETE"])
    def delete_question(id):
        question = Question.query.filter(Question.id==id).one_or_none()
        if question is None:
            abort(404)

        question.delete()
        questions = Question.query.order_by(Question.id).all()
        format_questions = [q.format() for q in questions]

        return jsonify({
            'success': True,
            'deleted': id,
            'questions': format_questions,
            'total_questions': len(questions)
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def new_question():    
        try:
            data = request.get_json()
            quest = data.get('question')
            answer = data.get('answer')
            category = data.get('category')
            diff = data.get('difficulty')
            if diff is None or category is None or quest is None or answer is None:
                abort(422)

            new_question = Question(quest, answer, category, diff)
            new_question.insert()

            questions = Question.query.order_by(Question.id).all()
            format_questions = [q.format() for q in questions]

            return jsonify({
                'success': True,
                'questions': format_questions,
                'total_questions': len(questions),
                'created': new_question.id
            })
        except Exception as e:
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/search/questions', methods=['POST'])
    def search_questions():
        data = request.get_json()
        key = data.get('searchTerm', '')

        questions = Question.query.filter(Question.question.ilike(f'%{key}%')).all()
        if len(questions) == 0:
            abort(404)

        format_questions = [q.format() for q in questions]
        
        return jsonify({
            'success': True,
            'questions': format_questions,
            'total_questions': len(Question.query.all()),
            'current_category': None
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def questions_category(id):
        categorie = Category.query.filter(Category.id==id).one_or_none()
        if categorie is None:
            abort(404)

        questions = Question.query.filter(Question.category == categorie.id).all()

        filtered_questions = [q.format() for q in questions]

        return jsonify({
            'success': True,
            'questions': filtered_questions,
            'total_questions': len(filtered_questions),
            'current_category': id
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_next_question():
        data = request.get_json()
        previous_questions = data.get('previous_questions', [])
        category = data.get('quiz_category', None)
        if category is None:
            abort(422)

        current = None
        questions = Question.query.filter(Question.category == category['id']).all() \
            if category['id'] != 0 else \
            Question.query.order_by(Question.id).all()

        format_questions = [q.id for q in questions]

        while (current is None or current.id in previous_questions):
            if len(previous_questions) >= len(format_questions):
                # No longer have available questions for that session..
                print("Epuisé --") 
                abort(422)

            current = Question.query.filter(
                Question.id==random.choice(format_questions)).one_or_none()

        # From here, we get the next question to render on this category..
        return jsonify({
            'success': True,
            'question': current.format()
        })


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({'success': False, 'error': 404, 'message': 'couldn\'t find that resource'}),
            404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400
        )    

    @app.errorhandler(500)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 500, "message": "internal server error"}),
            500
        )

    return app

