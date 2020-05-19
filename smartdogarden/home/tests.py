import unittest
from django.test import Client
from django.test import TestCase
import json

# Create your tests here.

from django.contrib.auth import get_user_model
# from django.contrib.auth import get_user_model
from django.contrib.auth import SESSION_KEY
from django.test import TestCase
import datetime

from account.models import Account
from gardens.buttons_functions import Arrive_DB, Leave_DB
from gardens.models import ArriveLeaveGarden, ReportOnHazard
from dogsitterService.models import ActivityTimeDogSitter, ServiceRequests, MeetingsActivity, Meetings, \
    RejectedActivity, ServiceRejected



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


    def test_integration_confirm_service_request(self):
        dog_owner = Account.objects.filter(username="test2").first()
        dog_sitter = Account.objects.filter(username="test5").first()
        dog_sitter_activity = ActivityTimeDogSitter.objects.create(
            username=dog_sitter.username,
            activity_date="2025-02-02",
            activity_start="09:30",
            activity_end="11:30",
            user_id=dog_sitter
        )
        dog_sitter_activity.save()
        service_request = ServiceRequests.objects.create(
            activity_id=dog_sitter_activity,
            requesting_user=dog_owner
        )
        service_request.save()
        meeting_activity = MeetingsActivity.objects.create(
            activity_date=service_request.activity_id.activity_date,
            activity_start=service_request.activity_id.activity_start,
            activity_end=service_request.activity_id.activity_end,
            dogsitter_id=dog_sitter
        )
        meeting_activity.save()
        meeting = Meetings.objects.create(
            dog_owner_id=dog_owner,
            meetings_activity_id=meeting_activity
        )
        meeting.save()
        dog_sitter_activity.delete()
        service_request.delete()
        meeting = Meetings.objects.filter(id=meeting.id).first()
        self.assertTrue(meeting)
        meeting.delete()
        meeting_activity.delete()

    def test_integration_view_my_service_request(self):
        dog_owner = Account.objects.filter(username="test2").first()
        dog_sitter = Account.objects.filter(username="test5").first()
        dog_sitter_activity = ActivityTimeDogSitter.objects.create(
            username=dog_sitter.username,
            activity_date="2025-02-02",
            activity_start="09:30",
            activity_end="11:30",
            user_id=dog_sitter
        )
        dog_sitter_activity.save()
        service_request = ServiceRequests.objects.create(
            activity_id=dog_sitter_activity,
            requesting_user=dog_owner
        )
        service_request.save()
        my_service_request = ServiceRequests.objects.filter(id=service_request.id).first()
        self.assertTrue(my_service_request)
        dog_sitter_activity.delete()
        service_request.delete()

    def test_integration_update_meeting_activity(self):
        dog_owner = Account.objects.filter(username="test2").first()
        dog_sitter = Account.objects.filter(username="test5").first()
        dogsitter_activity = ActivityTimeDogSitter.objects.create(
            username=dog_sitter.username,
            activity_date="2055-05-05",
            activity_start="14:00",
            activity_end="18:00",
            user_id=dog_sitter
        )
        dogsitter_activity.save()
        service_request = ServiceRequests.objects.create(
            activity_id=dogsitter_activity,
            requesting_user=dog_owner
        )
        service_request.save()
        meeting_activity_old = MeetingsActivity.objects.create(
            activity_date=dogsitter_activity.activity_date,
            activity_start=dogsitter_activity.activity_start,
            activity_end=dogsitter_activity.activity_end,
            dogsitter_id=dog_sitter
        )
        meeting_activity_old.save()
        dogsitter_activity.delete()
        meeting = Meetings.objects.create(
            dog_owner_id=dog_owner,
            meetings_activity_id=meeting_activity_old
        )
        meeting.save()
        service_request.delete()
        meeting_activity_old.activity_end = "17:20"
        meeting_activity_old.save()
        time1 = datetime.time(17, 20, 00)
        meeting_activity_after_update = MeetingsActivity.objects.filter(id=meeting_activity_old.id).first()
        self.assertEquals(meeting_activity_after_update.activity_end, time1)
        meeting_activity_after_update.delete()
        meeting.delete()




if __name__ == '__main__':
    unittest.main()
