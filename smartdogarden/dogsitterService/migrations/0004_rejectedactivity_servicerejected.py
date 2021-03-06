# Generated by Django 3.0.4 on 2020-05-10 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dogsitterService', '0003_meetings_meetingsactivity'),
    ]

    operations = [
        migrations.CreateModel(
            name='RejectedActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_date', models.DateField()),
                ('activity_start', models.TimeField()),
                ('activity_end', models.TimeField()),
                ('dogsitter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRejected',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dog_owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('rejected_activity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogsitterService.RejectedActivity')),
            ],
        ),
    ]
