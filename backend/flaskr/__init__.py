import os
import sys
sys.path.append('../')
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
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources = {r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]

    return jsonify({
      'success' : True,
      'categories' : formatted_categories,
      'total_categories': len(formatted_categories)
    })



  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    questions = Question.query.all()
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in questions]

    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]

    return jsonify({
      'success' : True,
      'questions' : formatted_questions[start:end],
      'total_questions' : len(formatted_questions),
      'categories': formatted_categories
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods= ['DELETE'])
  def delete_question(question_id):
    try:
     question = Question.query.filter(Question.id == question_id).one_or_none()

     if question is None:
       abort(404)

     question.delete()

     return jsonify({
      'success' : True,
      'deleted' : question_id
    })
    except:
      abort(404)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    question = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)

    try:
      question_item = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      question_item.insert()
      return jsonify({
      'success' : True,
      'created' : question_item.id
    })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search')
  def get_question_by_search_question():
    body = request.get_json()
    search = body.get('search', None)
    try:
      selection = Question.query.filter(Question.question.ilike('%{}%'.format(search)))
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      formatted_questions = [question.format() for question in selection]
      return jsonify({
      'success' : True,
      'questions' : formatted_questions[start:end],
      'total_questions' : len(formatted_questions),
    })
    except:
      abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category>/questions')
  def get_questions_by_category(category):
    try:
      selection = Question.query.filter(Question.category.ilike('{}'.format(category)))
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      formatted_questions = [question.format() for question in selection]
      return jsonify({
      'success' : True,
      'questions' : formatted_questions[start:end],
      'total_questions' : len(formatted_questions),
    })
    except:
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quizzes():
     body = request.get_json()

     previous_questions = body.get('previous_questions', None)
     quiz_category = body.get('quiz_category', None)
     print(quiz_category) 
     try:
       question = Question.query.filter(Question.category == quiz_category,Question.id.notin_(previous_questions)).first()
       if question is None:
         abort(404)

       return jsonify({
      'success' : True,
      'question' : question.format()
       })
     except:
      abort(404)
     


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "method not allowed"
        }), 405
  
  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422
  return app

if __name__ == '__main__':
    create_app().run(debug=True)
    