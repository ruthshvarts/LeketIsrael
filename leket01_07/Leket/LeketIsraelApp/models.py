from django.db import models
from django.core.exceptions import ValidationError
import re
import datetime

def validate_password(value):
    """Validate the password against certain criteria"""
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', value):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r'\d', value):
        raise ValidationError('Password must contain at least one digit.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError('Password must contain at least one special character.')

class Users1(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50, validators=[validate_password])
    email = models.EmailField(max_length=254, unique=True)

    def clean(self):
        """Validate the model fields"""
        super(Users1, self).clean()
        # if Users.objects.filter(username=self.username).exists():
        #     raise ValidationError('Username already exists.')
        if Users1.objects.filter(email=self.email).exists():
            raise ValidationError('Email address already exists.')


class leket_DB(models.Model):
    type = models.CharField(("type"),max_length=100)
    area = models.CharField(("area"),max_length=100)
    location = models.CharField(("location"),max_length=100)
    amount_kg = models.FloatField(("amount_kg"))
    missionID = models.FloatField(("missionID"))
    farmerID = models.CharField(("farmerID"),max_length=100)
    date = models.DateField(("date"))

# class Users(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     email = models.EmailField(max_length=254, unique=True)
#     def clean(self):
#         if not validate_password(self.password):
#             raise ValidationError('Password does not meet the requirements.')


class leket_DB_new(models.Model):
    group = models.CharField("group", max_length=100, null=True)
    type = models.CharField(("type"), max_length=100)
    area = models.CharField(("area"),max_length=100)
    leket_location = models.CharField(("leket_location"), max_length=100)
    sum_amount_kg = models.FloatField(("sum_amount_kg"))
    missionID = models.CharField("missionID", max_length=100, null=True)
    date = models.DateField("date", default=datetime.date.today)
    napa_name = models.CharField(("napa_name"), max_length=100)
    aklim_area = models.CharField(("aklim_area"), max_length=100)
    TMY_station = models.CharField(("TMY_station"), max_length=100)
    station = models.CharField(("station"), max_length=100)
    ground_temp = models.CharField("ground_temp", max_length=100, null=True)
    shmita = models.IntegerField("shmita", default=0)
    chagim = models.IntegerField("chagim", default=0)


class leket_DB_24_06(models.Model):
    group = models.IntegerField("group", null=True)
    type = models.CharField(("type"), max_length=100)
    area = models.CharField(("area"),max_length=100)
    leket_location = models.CharField(("leket_location"), max_length=100)
    amount_kg = models.FloatField(("amount_kg"))
    missionID = models.CharField("missionID", max_length=100, null=True)
    farmerID = models.CharField("farmerID", max_length=100, null=True)
    date = models.DateField("date", default=datetime.date.today)
    napa_name = models.CharField(("napa_name"), max_length=100)
    aklim_area = models.CharField(("aklim_area"), max_length=100, null=True)
    TMY_station = models.CharField(("TMY_station"), max_length=100, null=True)
    station = models.CharField(("station"), max_length=100, null=True)
    max_temp = models.CharField("max_temp", max_length=100, null=True)
    min_temp = models.CharField("min_temp", max_length=100, null=True)
    ground_temp = models.CharField("ground_temp", max_length=100, null=True)
    shmita = models.IntegerField("shmita", default=0)
    chagim = models.IntegerField("chagim", default=0)
    # max_temp = models.CharField("max_temp", max_length=100, null=True)
    # min_temp = models.CharField("min_temp", max_length=100, null=True)
    # ground_temp = models.CharField("ground_temp", max_length=100, null=True)



