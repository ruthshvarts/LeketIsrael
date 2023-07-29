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


class leket_DB(models.Model): # TODO: change the name
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
