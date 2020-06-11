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
from gardens.models import ArriveLeaveGarden, ReportOnHazard, HazardReports
from dogsitterService.models import ActivityTimeDogSitter, ServiceRequests, MeetingsActivity, Meetings, \
    RejectedActivity, ServiceRejected
from .models import GardenAdminNotice

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

    def test_json_DB(self):
        json_data = open('smartdogarden/home/dog-gardens.json', encoding="utf8")
        data1 = json.load(json_data)  # deserialises it
        json_data.close()
        size = len(data1)
        self.assertEquals(size, 13)

    def test_arrive_to_garden(self):
        # json_data = open('home/dog-gardens.json', encoding="utf8")
        # data1 = json.load(json_data)  # deserialises it
        # json_data.close()
        user = Account.objects.filter(username='test2').first()
        arrive = ArriveLeaveGarden.objects.create(
            # garden_name=data1[0]['name'],
            garden_name="פארק קפלן",
            username="test2",
            user_id=user,
        )
        arrive.save()
        self.assertTrue(arrive)

    def test_view_user_in_garden(self):
        user = Account.objects.filter(username='test2').first()
        arrive = ArriveLeaveGarden.objects.create(
            # garden_name=data1[0]['name'],
            garden_name="פארק קפלן",
            username="test2",
            user_id=user,
        )
        arrive.save()
        arrive = ArriveLeaveGarden.objects.filter(username="test2").first()
        self.assertEqual(arrive.garden_name, "פארק קפלן")
        arrive.delete()

    def test_leave_the_garden(self):
        user = Account.objects.filter(username='test2').first()
        id = user.id
        leave = ArriveLeaveGarden.objects.filter(user_id=id).first()
        leave.delete()
        leave = ArriveLeaveGarden.objects.filter(user_id=id).first()
        self.assertFalse(leave)

    def test_update_meeting_activity(self):
        dog_owner = Account.objects.filter(username="test2").first()
        dog_sitter = Account.objects.filter(username="test5").first()
        meeting_activity_old = MeetingsActivity.objects.create(
            activity_date="2027-01-01",
            activity_start="10:00",
            activity_end="11:00",
            dogsitter_id=dog_sitter
        )
        meeting_activity_old.save()
        meeting = Meetings.objects.create(
            dog_owner_id=dog_owner,
            meetings_activity_id=meeting_activity_old
        )
        meeting.save()
        meeting_activity_update = MeetingsActivity.objects.filter(id=meeting_activity_old.id).first()
        meeting_activity_update.activity_end = "11:30"
        meeting_activity_update.save()
        meeting_activity_after_update = MeetingsActivity.objects.filter(id=meeting_activity_old.id).first()
        time1 = datetime.time(11, 30, 00)
        self.assertEquals(meeting_activity_after_update.activity_end, time1)
        meeting.delete()
        meeting_activity_after_update.delete()

    def test_add_dogsitter_activity_time(self):
        dog_sitter = Account.objects.filter(username="test5").first()
        dogsitter_activity = ActivityTimeDogSitter.objects.create(
            username=dog_sitter.username,
            activity_date="2028-01-01",
            activity_start="08:00",
            activity_end="09:00",
            user_id=dog_sitter
        )
        dogsitter_activity.save()
        self.assertTrue(dogsitter_activity)

    def test_add_service_request(self):
        dog_owner = Account.objects.filter(username="test2").first()
        dog_sitter = Account.objects.filter(username="test5").first()
        dogsitter_activity = ActivityTimeDogSitter.objects.filter(user_id=dog_sitter).first()
        service_request = ServiceRequests.objects.create(
            activity_id=dogsitter_activity,
            requesting_user=dog_owner
        )
        service_request.save()
        self.assertTrue(service_request)

    def test_integration_view_my_service_requests(self):
        dog_sitter = Account.objects.filter(username="test5").first()
        dog_owner = Account.objects.filter(username="test2").first()
        dogsitter_activity = ActivityTimeDogSitter.objects.create(
            username=dog_sitter.username,
            activity_date="2066-06-06",
            activity_start="06:00",
            activity_end="06:08",
            user_id=dog_sitter
        )
        dogsitter_activity.save()
        service_request = ServiceRequests.objects.create(
            activity_id=dogsitter_activity,
            requesting_user=dog_owner
        )
        service_request.save()
        all_service_requests = ServiceRequests.objects.all()
        my_service_requests = []
        for i in all_service_requests:
            if i.activity_id.user_id == dog_sitter:
                my_service_requests.append(i)
        self.assertTrue(my_service_requests)

    def test_confirm_service_request(self):
        dog_sitter = Account.objects.filter(username="test5").first()
        dog_owner = Account.objects.filter(username="test2").first()
        all_service_requests = ServiceRequests.objects.all()
        my_service_requests = []
        for i in all_service_requests:
            if i.activity_id.user_id == dog_sitter:
                my_service_requests.append(i)
        service_request = ServiceRequests.objects.filter(id=my_service_requests[0].id).first()
        activity_id = service_request.activity_id.id
        dogsitter_activity = ActivityTimeDogSitter.objects.filter(id=activity_id)
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
        self.assertTrue(meeting)
        meeting.delete()
        meeting_activity.delete()
        service_request.delete()
        dogsitter_activity.delete()

    def test_reject_service_request(self):
        dog_sitter = Account.objects.filter(username="test5").first()
        dog_owner = Account.objects.filter(username="test2").first()
        service_request = ServiceRequests.objects.filter(requesting_user=dog_owner).first()
        activity_id = service_request.activity_id.id
        service_activity = ActivityTimeDogSitter.objects.filter(id=activity_id).first()
        rejected_activity = RejectedActivity.objects.create(
            activity_date=service_activity.activity_date,
            activity_start=service_activity.activity_start,
            activity_end=service_activity.activity_end,
            dogsitter_id=dog_sitter
        )
        rejected_activity.save()
        service_request.delete()
        service_activity.delete()
        rejected_service = ServiceRejected.objects.create(
            dog_owner_id=dog_owner,
            rejected_activity_id=rejected_activity
        )
        rejected_service_id = rejected_service.id
        rejected_service = ServiceRejected.objects.filter(id=rejected_service_id).first()
        self.assertTrue(rejected_service)
        rejected_activity.delete()
        rejected_service.delete()

    def test_view_doggsitter(self):
        dog_sitters = Account.objects.filter(is_dog_sitter=True).first()
        self.assertTrue(dog_sitters)

    def test_report_on_hazard(self):
        dog_owner = Account.objects.filter(username="test2").first()
        new_hazard_report = ReportOnHazard.objects.create(
            reporter_user_name=dog_owner.username,
            garden_name="פארק קפלן",
            report_title="test",
            report_text="this is report test",
            reporter_id=dog_owner
        )
        new_hazard_report.save()
        self.assertTrue(new_hazard_report)

    def test_view_hazard(self):
        hazard = ReportOnHazard.objects.filter(report_title="test").first()
        self.assertEqual(hazard.garden_name, "פארק קפלן")
        hazard.delete()

    def test_view_my_meetings(self):
        dog_sitter = Account.objects.filter(username="test5").first()
        my_meetings_activity = MeetingsActivity.objects.filter(id=dog_sitter.id)
        self.assertEqual(len(my_meetings_activity), 0)

    def test_dogsitter_service_coordination(self):
        dog_owner = Account.objects.filter(username="test2").first()
        dog_sitter = Account.objects.filter(username="test5").first()
        dogsitter_activity = ActivityTimeDogSitter.objects.create(
            username=dog_sitter.username,
            activity_date="2026-01-01",
            activity_start="08:00",
            activity_end="09:00",
            user_id=dog_sitter
        )
        dogsitter_activity.save()
        service_request = ServiceRequests.objects.create(
            activity_id=dogsitter_activity,
            requesting_user=dog_owner
        )
        service_request.save()
        service_request_id = service_request.id
        service_request = ServiceRequests.objects.filter(id=service_request_id).first()
        self.assertTrue(service_request)
        dogsitter_activity.delete()
        service_request.delete()

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

    def test_integration_reject_service_request(self):
        dog_owner = Account.objects.filter(username="test2").first()
        dog_sitter = Account.objects.filter(username="test5").first()
        dog_sitter_activity = ActivityTimeDogSitter.objects.create(
            username=dog_sitter.username,
            activity_date="2077-07-07",
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
        rejected_activity = RejectedActivity.objects.create(
            activity_date=service_request.activity_id.activity_date,
            activity_start=service_request.activity_id.activity_start,
            activity_end=service_request.activity_id.activity_end,
            dogsitter_id=dog_sitter
        )
        rejected_activity.save()
        service_request.delete()
        dog_sitter_activity.delete()
        rejected_service = ServiceRejected.objects.create(
            dog_owner_id=dog_owner,
            rejected_activity_id=rejected_activity
        )
        rejected_service.save()
        rejected_service_id = rejected_service.id
        rejected_service = ServiceRejected.objects.filter(id=rejected_service_id).first()
        self.assertTrue(rejected_service)
        rejected_activity.delete()
        rejected_service.delete()

    def test_integration_leave_garden(self):
        user = Account.objects.filter(username="test5").first()
        json_data = open('smartdogarden/home/dog-gardens.json', encoding="utf8")
        data1 = json.load(json_data)  # deserialises it
        json_data.close()
        garden_name = data1[10]['name']
        arrive = ArriveLeaveGarden.objects.create(
            garden_name=garden_name,
            username="test2",
            user_id=user,
        )
        arrive.save()
        leave = ArriveLeaveGarden.objects.filter(garden_name=garden_name).first()
        leave.delete()
        leave = ArriveLeaveGarden.objects.filter(garden_name=garden_name).first()
        self.assertFalse(leave)

    # sprint 3

    def test_announcement_board(self):
        garden_admin = Account.objects.filter(username="test7").first()
        announcement_test = GardenAdminNotice.objects.create(
            announces_id=garden_admin,
            announcement_text="test_view_annou_boa.."
        )
        announcement_test.save()
        announcement_test_id = announcement_test.id
        announcement = GardenAdminNotice.objects.filter(id=announcement_test_id).first()
        self.assertEquals(announcement.announcement_text, "test_view_annou_boa..")
        announcement.delete()

    def test_hazard_update_status(self):
        dog_owner = Account.objects.filter(username="test2").first()
        hazard_report_old = HazardReports.objects.create(
            reporter_id=dog_owner,
            reporter_user_name=dog_owner.username,
            garden_name="פארק קפלן",
            report_title="test status update",
            report_text="this is a test foe status update.."
        )
        hazard_report_old.save()
        hazard_id = hazard_report_old.id
        update_hazard = HazardReports.objects.filter(id=hazard_id).first()
        update_hazard.report_status = "test status update successfully!"
        update_hazard.save()
        update_hazard = HazardReports.objects.filter(id=hazard_id).first()
        self.assertEquals(update_hazard.report_status, "test status update successfully!")
        update_hazard.delete()

    def test_add_new_announcement_to_board(self):
        all_announcements = GardenAdminNotice.objects.all()
        the_old_announcement_amount = len(all_announcements)
        garden_admin = Account.objects.filter(username="test7").first()
        announcement_test = GardenAdminNotice.objects.create(
            announces_id=garden_admin,
            announcement_text="test add new announcement"
        )
        announcement_test.save()
        all_announcements = GardenAdminNotice.objects.all()
        new_len = len(all_announcements)
        self.assertEquals(new_len, the_old_announcement_amount + 1)
        announcement_test.delete()

    def test_admin_view_hazards_report_to_confirm_or_reject(self):
        all_report_requests = ReportOnHazard.objects.all()
        the_old_report_request_amount = len(all_report_requests)
        dog_owner = Account.objects.filter(username="test2").first()
        new_user_hazard_report_for_confirm = ReportOnHazard.objects.create(
            reporter_user_name=dog_owner.username,
            garden_name="פארק קפלן",
            report_title="test new report for confirm",
            report_text="this is report  confirm reject test",
            reporter_id=dog_owner
        )
        new_user_hazard_report_for_confirm.save()
        all_report_requests = ReportOnHazard.objects.all()
        new_len = len(all_report_requests)
        self.assertEquals(new_len, the_old_report_request_amount + 1)
        new_user_hazard_report_for_confirm.delete()


    def test_view_confirm_hazard(self):
        dog_owner = Account.objects.filter(username="test2").first()
        hazard_report = HazardReports.objects.create(
            reporter_id=dog_owner,
            reporter_user_name=dog_owner.username,
            garden_name="פארק קפלן",
            report_title="test status update",
            report_text="this is a test foe status update.."
        )
        hazard_report.save()
        all_confirm_hazard = HazardReports.objects.all()
        self.assertTrue(all_confirm_hazard)
        hazard_report.delete()

    def test_delete_announcement_from_board(self):
        garden_admin = Account.objects.filter(username="test7").first()
        announcement_test = GardenAdminNotice.objects.create(
            announces_id=garden_admin,
            announcement_text="test delete an announcement"
        )
        announcement_test.save()
        announcement_test_id = announcement_test.id
        announcement_test.delete()
        announcement_test = GardenAdminNotice.objects.filter(id=announcement_test_id).first()
        self.assertFalse(announcement_test)


    def test_delete_dog_owner_user(self):
        dog_owner_to_delete = Account.objects.create(
            username="dog_owner_delete",
            email="dog_owner_delete@dogownerdelete.dogownerdelete",
            password='pbkdf2_sha256$180000$zZwGjD6j2MAe$PYA0uuF0t6ci/384ULDJLrQD2hoY/YfideKHYRZPm6A=',
            first_name="dog_owner_delete",
            last_name="dog_owner_delete",
            user_id="7536636",
            phone_number="9991174225",
            is_dog_owner="1"
        )
        dog_owner_to_delete.save()
        dog_owner_id = dog_owner_to_delete.id
        dog_owner_to_delete = Account.objects.filter(id=dog_owner_id).first()
        dog_owner_to_delete.delete()
        dog_owner_to_delete = Account.objects.filter(id=dog_owner_id).first()
        self.assertFalse(dog_owner_to_delete)

    def test_delete_dog_sitter_user(self):
        dog_sitter_to_delete = Account.objects.create(
            username="dog_sitter_delete",
            email="dog_sitter_delete@dogsitterdelete.dogsitterdelete",
            password='pbkdf2_sha256$180000$zZwGjD6j2MAe$PYA0uuF0t6ci/384ULDJLrQD2hoY/YfideKHYRZPm6A=',
            first_name="dog_sitter_delete",
            last_name="dog_sitter_delete",
            user_id="78745125",
            phone_number="8887547785",
            is_dog_sitter="1"
        )
        dog_sitter_to_delete.save()
        dog_sitter_id = dog_sitter_to_delete.id
        dog_sitter_to_delete = Account.objects.filter(id=dog_sitter_id).first()
        dog_sitter_to_delete.delete()
        dog_sitter_to_delete = Account.objects.filter(id=dog_sitter_id).first()
        self.assertFalse(dog_sitter_to_delete)

    def test_view_dogsitters_users(self):
        all_dogsitters_users = Account.objects.filter(is_dog_sitter=1)
        self.assertTrue(all_dogsitters_users)

    def test_view_dog_owner_users(self):
        all_dog_owner_users = Account.objects.filter(is_dog_owner=1)
        self.assertTrue(all_dog_owner_users)

    def test_delete_dogsitter_activity_time(self):
        dog_sitter = Account.objects.filter(username="test5").first()
        dog_sitter_activity = ActivityTimeDogSitter.objects.create(
            username=dog_sitter.username,
            activity_date="2011-11-11",
            activity_start="08:30",
            activity_end="11:30",
            user_id=dog_sitter
        )
        dog_sitter_activity.save()
        activity_id = dog_sitter_activity.id
        dog_sitter_activity.delete()
        dog_sitter_activity = ActivityTimeDogSitter.objects.filter(id=activity_id)
        self.assertFalse(dog_sitter_activity)

    # sprint3 integration tests

    def test_integration_register_login_logout_user(self):
        new_user = Account.objects.create(
            username="test_r_l_l",
            email="test_r_l_l@testrll.testrll",
            password='pbkdf2_sha256$180000$zZwGjD6j2MAe$PYA0uuF0t6ci/384ULDJLrQD2hoY/YfideKHYRZPm6A=',
            first_name="test_r_l_l",
            last_name="test_r_l_l",
            user_id="7856989",
            phone_number="8885222963",
            is_dog_owner="1"
        )
        new_user.save()
        new_user_id = new_user.id
        c = Client()
        login = c.post('/login/', {'username': 'test_r_l_l', 'password': 'l123123123'})
        logout = c.post('/logout/')
        new_user_for_delete = Account.objects.filter(id=new_user_id)
        self.assertTrue(logout)
        new_user_for_delete.delete()


    def test_integration_delete_user(self):
        new_user = Account.objects.create(
            username="test_delete",
            email="test_delete@testdelete.testdelete",
            password='pbkdf2_sha256$180000$zZwGjD6j2MAe$PYA0uuF0t6ci/384ULDJLrQD2hoY/YfideKHYRZPm6A=',
            first_name="test_delete",
            last_name="test_delete",
            user_id="1000100",
            phone_number="0509999999",
            is_dog_sitter="1"
        )
        new_user.save()
        c = Client()
        login = c.post('/login/', {'username': 'test_delete', 'password': 'l123123123'})
        logout = c.post('/logout/')
        all_dog_sitters = Account.objects.filter(is_dog_sitter=1)
        user_id = new_user.id
        the_user = all_dog_sitters.filter(id=user_id).first()
        the_user.delete()
        all_dog_sitters = Account.objects.filter(is_dog_sitter=1)
        the_user = all_dog_sitters.filter(id=user_id).first()
        self.assertFalse(the_user)

    def test_integration_reject_hazard_request(self):
        new_user = Account.objects.create(
            username="test_reject",
            email="test_reject@testreject.testreject",
            password='pbkdf2_sha256$180000$zZwGjD6j2MAe$PYA0uuF0t6ci/384ULDJLrQD2hoY/YfideKHYRZPm6A=',
            first_name="test_reject",
            last_name="test_reject",
            user_id="9517536",
            phone_number="9874681783",
            is_dog_owner="1"
        )
        new_user.save()
        c = Client()
        login = c.post('/login/', {'username': 'test_delete', 'password': 'l123123123'})
        logout = c.post('/logout/')
        new_user = Account.objects.filter(username="test_reject").first()
        new_user_hazard_report_for_reject = ReportOnHazard.objects.create(
            reporter_user_name=new_user.username,
            garden_name="פארק קפלן",
            report_title="test new report for reject",
            report_text="this is report reject test",
            reporter_id=new_user
        )
        new_user_hazard_report_for_reject.save()
        report_id = new_user_hazard_report_for_reject.id
        the_request_hazard_report = ReportOnHazard.objects.filter(id=report_id).first()
        the_request_hazard_report.delete()
        the_request_hazard_report = ReportOnHazard.objects.filter(id=report_id).first()
        new_user.delete()
        self.assertFalse(the_request_hazard_report)

    def test_integration_update_hazard_status(self):
        new_user = Account.objects.create(
            username="test_status",
            email="test_status@teststatus.teststatus",
            password='pbkdf2_sha256$180000$zZwGjD6j2MAe$PYA0uuF0t6ci/384ULDJLrQD2hoY/YfideKHYRZPm6A=',
            first_name="test_status",
            last_name="test_status",
            user_id="7546289",
            phone_number="4527430005",
            is_dog_owner="1"
        )
        new_user.save()
        c = Client()
        login = c.post('/login/', {'username': 'test_delete', 'password': 'l123123123'})
        logout = c.post('/logout/')
        new_user = Account.objects.filter(username="test_status").first()
        new_user_hazard_report_for_confirm = ReportOnHazard.objects.create(
            reporter_user_name=new_user.username,
            garden_name="פארק קפלן",
            report_title="test new report for integration status update",
            report_text="this is report integration status update test",
            reporter_id=new_user
        )
        new_user_hazard_report_for_confirm.save()
        request_id = new_user_hazard_report_for_confirm.id
        the_report_request = ReportOnHazard.objects.filter(id=request_id)
        hazard_report = HazardReports.objects.create(
            reporter_id=new_user_hazard_report_for_confirm.reporter_id,
            reporter_user_name=new_user_hazard_report_for_confirm.reporter_user_name,
            garden_name=new_user_hazard_report_for_confirm.garden_name,
            report_title=new_user_hazard_report_for_confirm.report_title,
            report_text=new_user_hazard_report_for_confirm.report_text
        )
        hazard_report.save()
        the_report_request.delete()
        hazard_id = hazard_report.id
        hazard_update_status = HazardReports.objects.filter(id=hazard_id).first()
        hazard_update_status.report_status = "test hazard status update successfully!"
        hazard_update_status.save()
        hazard_update_status = HazardReports.objects.filter(id=hazard_id).first()
        self.assertEquals(hazard_update_status.report_status, "test hazard status update successfully!")
        hazard_update_status.delete()
        new_user.delete()

    def test_integration_confirm_hazard_report(self):
        new_user_for_test = Account.objects.create(
            username="test_confrim_re",
            email="test_confrim_re@testconfrimre.testconfrimre",
            password='pbkdf2_sha256$180000$zZwGjD6j2MAe$PYA0uuF0t6ci/384ULDJLrQD2hoY/YfideKHYRZPm6A=',
            first_name="test_confrim_re",
            last_name="test_confrim_re",
            user_id="7462015",
            phone_number="1549621954",
            is_dog_owner="1"
        )
        new_user_for_test.save()
        c = Client()
        login = c.post('/login/', {'username': 'test_delete', 'password': 'l123123123'})
        logout = c.post('/logout/')
        new_user = Account.objects.filter(username="test_confrim_re").first()
        new_user_hazard_report_for_confirm = ReportOnHazard.objects.create(
            reporter_user_name=new_user.username,
            garden_name="פארק קפלן",
            report_title="test new report for reject",
            report_text="this is report reject test",
            reporter_id=new_user
        )
        new_user_hazard_report_for_confirm.save()
        report_id = new_user_hazard_report_for_confirm.id
        the_request_hazard_report = ReportOnHazard.objects.filter(id=report_id).first()
        the_hazard = HazardReports.objects.create(
            reporter_id=new_user_hazard_report_for_confirm.reporter_id,
            reporter_user_name=new_user_hazard_report_for_confirm.reporter_user_name,
            garden_name=new_user_hazard_report_for_confirm.garden_name,
            report_title=new_user_hazard_report_for_confirm.report_title,
            report_text=new_user_hazard_report_for_confirm.report_text
        )
        the_hazard.save()
        the_request_hazard_report.delete()
        the_hazard_id = the_hazard.id
        the_hazard = HazardReports.objects.filter(id=the_hazard_id).first()
        new_user.delete()
        self.assertTrue(the_hazard)
        the_hazard.delete()




if __name__ == '__main__':
    unittest.main()
