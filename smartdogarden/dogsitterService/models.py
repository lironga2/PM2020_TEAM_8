from django.db import models
from account.models import Account


# Create your models here.

class ActivityTimeDogSitter(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    activity_date = models.DateField()
    activity_start = models.TimeField()
    activity_end = models.TimeField()