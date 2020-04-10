import unittest
from django.test import Client
from django.test import TestCase

# Create your tests here.

from django.contrib.auth import get_user_model
# from django.contrib.auth import get_user_model
from django.contrib.auth import SESSION_KEY
from django.test import TestCase


class MyTestCase(unittest.TestCase):
    # def LogInTest(TestCase):
    c = Client()

    def test_insert_to_DB(self):

        self.credentials = {
            'user_id': '555',
            'email': 'super@super.super',
            'username': 'super',
            'password': 'l123123123'}
        with self.assertRaisesRegex(Exception, "Duplicate entry"):
            get_user_model().objects.create_user(**self.credentials)
        # get_user_model().objects.save(using=self._db)

    def test_login(self):
        c = Client()
        login = c.post('/login/', {'username': 'super', 'password': 'l123123123'})
        self.assertTrue(login)


if __name__ == '__main__':
    unittest.main()
