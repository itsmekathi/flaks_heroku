import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password= 'cat')
        self.assertTrue(u.password is not None)
    