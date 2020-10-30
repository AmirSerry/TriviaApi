import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

    def test_categories_method_not_found(self):
         res = self.client().post('/categories')

         self.assertEqual(res.status_code, 405)

    def test_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_questions_method_not_found(self):
         res = self.client().patch('/questions')

         self.assertEqual(res.status_code, 405)     

    def test_delete_question(self):
      question = Question(question="created to be deleted", answer="created to be deleted", category="created to be deleted", difficulty=1)
      question.insert()
      id = question.id

      res = self.client().delete('/questions/' + str(id))
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['deleted'],id)

    def test_delete_error(self):
      question = Question(question="created to be deleted", answer="created to be deleted", category="created to be deleted", difficulty=1)
      question.insert()
      id = question.id  
      res = self.client().delete('/questions/' + str(id))

      res = self.client().delete('/questions/' + str(id))
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 404)
     
    def test_add_question(self):
        new_question = {
             "question": "new question",
             "answer": "new answer",
             "category": "comic",
             "difficulty": 1
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['created'])
         

    def test_422_add_question(self):
        new_question = {
             "question": "new question",
             "answer": "new answer",
             "category": "comic",
             "difficulty": 11111111111111111111111111111111
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
           
    def test_search_question(self):
        search = {
                "search": ""   
                 }
        res = self.client().get('/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])


    def test__search_questions_method_not_found(self):
         res = self.client().post('/questions/search')

         self.assertEqual(res.status_code, 405)   

    def test_get_question_by_category(self):
        question = Question.query.first()
        res = self.client().get('/categories/'+question.category+'/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])


    def test_get_question_by_category_404(self):
        res = self.client().get('/categories/not/found/questions')

        self.assertEqual(res.status_code, 404)

    def test_quizzes(self):
        question = Question.query.first()
        input = {
          "previous_questions": [question.id],
          "quiz_category": question.category
            }
        res = self.client().post('/quizzes', json= input)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])



    def test_quizzes_not_found(self):
        question = Question.query.first()
        input = {
          "previous_questions": [question.id],
          "quiz_category": question.category + "not found"
            }
        res = self.client().post('/quizzes', json= input)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
       



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()