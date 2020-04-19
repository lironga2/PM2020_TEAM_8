from django.db import models
from django.utils import timezone
from account.models import Account


# Create your models here.


class ArriveLeaveGarden(models.Model):
    garden_name = models.CharField(max_length=100)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    arrive_date = models.DateTimeField(default=timezone.now)
    leave_date = models.DateTimeField(default=None)

    def create_arrive(self, garden_name, username, user_id):
        tmp = self.model(
            garden_name=garden_name,
            user_id=user_id,
            username=username,

        )
        tmp.save(using=self._db)
        return tmp
