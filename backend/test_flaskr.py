import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_USER, DB_HOST, DB_PASSWORD,\
    DB_TEST_NAME, DB_DIALECT, DB_PORT


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"

        self.database_path = "{}://{}:{}@{}:{}/{}".format(
            DB_DIALECT, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_TEST_NAME
        )
        setup_db(self.app, self.database_path)

        # New question for the test..
        self.new_question = {
            "question": "Who's the first ever to walk on the moon ?",
            "answer": "Neil Armstrong",
            "category": 1,
            "difficulty": 3
        }
        self.dummy = {"question": None,
            "answer": None, "category": None}

        self.quiz = {"previous_questions": [2],
            "quiz_category": {'id': 5, 'type': 'Entertainment'}}

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
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']))

    def test_get_categories_fail(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertNotEqual(res.status_code, 404)
        self.assertNotEqual(res.status_code, 400)
        self.assertNotEqual(res.status_code, 500)
        self.assertNotEqual(res.status_code, 422)
        self.assertNotEqual(data['success'], False)

    def test_get_questions_and_categories(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertIs(data['success'], True)
        self.assertGreaterEqual(data['total_questions'], 0, "Questions list empty.")
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])

    def test_get_questions_empty(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertIsNot(data['success'], False)
        self.assertNotEqual(res.status_code, 404)

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertIs(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(data['created'], 0)

    def test_add_question_not_processable(self):
        res = self.client().post('/questions', json=self.dummy)
        data = json.loads(res.data)
        self.assertIs(data['success'], False)
        self.assertEqual(res.status_code, 422)

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        self.assertIs(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    def test_delete_question_fail(self):
        res = self.client().delete('/questions/3000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertIs(data['success'], False)

    def test_search_question(self):
        res = self.client().post('/search/questions', json={"searchTerm": "moon"})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(data['total_questions'], 0)

    def test_search_question_not_found(self):
        res = self.client().post('/search/questions', json={"searchTerm": "afcon"})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    def test_questions_for_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)
        self.assertIs(data['success'], True)
        self.assertGreaterEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], 3)
        self.assertEqual(res.status_code, 200)

    def test_questions_for_category_not_found(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        self.assertIs(data['success'], False)
        self.assertEqual(res.status_code, 404)

    def test_quiz(self):
        res = self.client().post('/quizzes', json=self.quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIs(data['success'], True)
        self.assertTrue(data['question'])

    def test_quiz_category_not_found(self):
        res = self.client().post('/quizzes', json={'previous_questions': []})
        data = json.loads(res.data)
        self.assertIs(data['success'], False)
        self.assertEqual(res.status_code, 422)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()