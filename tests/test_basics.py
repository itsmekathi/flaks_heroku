import unittest
import pytest
from flask import current_app
from app import create_app, db

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_app_exists(self):
        self.assertTrue(current_app is not None)

    def test_main_page(self):
        c = self.app.test_client()
        response = c.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    def test_about_page(self):
        c = self.app.test_client()
        response = c.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])