import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://krillavilla:1234@localhost:5432/trivia_test"
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

    def test_get_categories(self):
        """Test getting categories."""
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        """Test getting questions."""
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])

    def test_404_requesting_beyond_valid_page(self):
        """Test requesting a page that doesn't exist."""
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    def test_delete_question(self):
        """Test deleting a question."""
        response = self.client().delete('/questions/5')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['deleted'], 5)

    def test_422_if_question_does_not_exist(self):
        """Test error if question to delete doesn't exist."""
        response = self.client().delete('/questions/1000')
        self.assertEqual(response.status_code, 422)

    def test_create_question(self):
        """Test creating a question."""
        new_question = {
            'question': 'What is the capital of France?',
            'answer': 'Paris',
            'category': 3,
            'difficulty': 2
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['created'])

    def test_search_questions(self):
        """Test searching questions."""
        search_term = {'searchTerm': 'title'}
        response = self.client().post('/questions/search', json=search_term)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])

    def test_get_questions_by_category(self):
        """Test getting questions by category."""
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])

    def test_404_get_questions_by_category(self):
        """Test getting questions by invalid category."""
        response = self.client().get('/categories/1000/questions')
        self.assertEqual(response.status_code, 404)

    def test_play_quiz(self):
        """Test playing quiz."""
        quiz = {'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': 1}}
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['question'])

    def test_404_play_quiz(self):
        """Test playing quiz with invalid category."""
        quiz = {'previous_questions': [], 'quiz_category': {'type': 'Invalid', 'id': 1000}}
        response = self.client().post('/quizzes', json=quiz)
        self.assertEqual(response.status_code, 404)

    def test_422_play_quiz(self):
        """Test playing quiz with invalid previous questions."""
        quiz = {'previous_questions': [1000], 'quiz_category': {'type': 'Science', 'id': 1}}
        response = self.client().post('/quizzes', json=quiz)
        self.assertEqual(response.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
