from django.db import models
from django.utils import timezone
from account.models import Account


# Create your models here.
class GardenAdminNotice(models.Model):
    announces_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    announcement_date = models.DateField(default=timezone.now)
    announcement_text = models.CharField(max_length=300)
