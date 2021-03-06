# Generated by Django 3.0.4 on 2020-04-05 15:35

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=60, verbose_name='email')),
                ('user_id', models.IntegerField(editable=False, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=150)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone_number', phone_field.models.PhoneField(blank=True, max_length=31)),
                ('city', models.CharField(max_length=30)),
                ('street', models.CharField(max_length=30)),
                ('app_number', models.IntegerField(null=True)),
                ('zip', models.IntegerField(null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_dog_owner', models.BooleanField(default=False)),
                ('is_dog_sitter', models.BooleanField(default=False)),
                ('is_dog_garden_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
