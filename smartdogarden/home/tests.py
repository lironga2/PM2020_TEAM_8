import unittest
from django.test import Client
from django.test import TestCase
import json

# Create your tests here.

from django.contrib.auth import get_user_model
# from django.contrib.auth import get_user_model
from django.contrib.auth import SESSION_KEY
from django.test import TestCase

from account.models import Account
from gardens.buttons_functions import Arrive_DB, Leave_DB
from gardens.models import ArriveLeaveGarden


class MyTestCase(unittest.TestCase):
    # def LogInTest(TestCase):
    c = Client()

    def test_insert_to_DB(self):

        self.credentials = {
            'user_id': '555',
            'email': 'super@super.super',
            'username': 'super',
            'password': 'l123123123'}
        with self.assertRaisesRegex(Exception, "user"):
            get_user_model().objects.create_user(**self.credentials)
        # get_user_model().objects.save(using=self._db)

    def test_register_with_exist_dogOwner_user(self):
        self.credentials = {
            'user_id': '123',
            'email': 'test2@test2.test2',
            'username': 'test2',
            'password': 'l123123123'}
        with self.assertRaisesRegex(Exception, "user"):
            get_user_model().objects.create_user(**self.credentials)
        # get_user_model().objects.save(using=self._db)

    def test_register_with_exist_dogSitter_user(self):
        self.credentials = {
            'user_id': '1111',
            'email': 'test1@test1.test1',
            'username': 'test1',
            'password': 'l123123123'}
        with self.assertRaisesRegex(Exception, "user"):
            get_user_model().objects.create_user(**self.credentials)
        # get_user_model().objects.save(using=self._db)

    def test_login(self):
        c = Client()
        login = c.post('/login/', {'username': 'super', 'password': 'l123123123'})
        self.assertTrue(login)

    def test_logout(self):
        c = Client()
        logout = c.post('/logout/')
        self.assertTrue(logout)

    #def test_json_DB(self):
        #json_data = open('data_from_b7_open_data/dog-gardens.json, encoding="utf8")
        #data1 = json.load(json_data)  # deserialises it
        #json_data.close()
        #size = len(data1)
        #self.assertEquals(size, 13)

    def test_arrive_to_garden(self):
        #json_data = open('data_from_b7_open_data/dog-gardens.json', encoding="utf8")
        #data1 = json.load(json_data)  # deserialises it
        #json_data.close()
        user = Account.objects.filter(username='test2').first()
        arrive = ArriveLeaveGarden.objects.create(
            #garden_name=data1[0]['name'],
            garden_name="פארק קפלן",
            username="test2",
            user_id=user,
        )
        arrive.save()
        self.assertTrue(arrive)

    def test_leave_the_garden(self):
        user = Account.objects.filter(username='test2').first()
        id = user.id
        leave = ArriveLeaveGarden.objects.filter(user_id=id).first()
        leave.delete()
        leave = ArriveLeaveGarden.objects.filter(user_id=id).first()
        self.assertFalse(leave)


if __name__ == '__main__':
    unittest.main()
