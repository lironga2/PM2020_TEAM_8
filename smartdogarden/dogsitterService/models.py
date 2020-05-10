from django.db import models
from account.models import Account


# Create your models here.

class ActivityTimeDogSitter(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    activity_date = models.DateField()
    activity_start = models.TimeField()
    activity_end = models.TimeField()


class ServiceRequests(models.Model):
    activity_id = models.ForeignKey(ActivityTimeDogSitter, on_delete=models.CASCADE)
    requesting_user = models.ForeignKey(Account, on_delete=models.CASCADE)


class MeetingsActivity(models.Model):
    dogsitter_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    activity_date = models.DateField()
    activity_start = models.TimeField()
    activity_end = models.TimeField()


class Meetings(models.Model):
    dog_owner_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    meetings_activity_id = models.ForeignKey(MeetingsActivity, on_delete=models.CASCADE)
