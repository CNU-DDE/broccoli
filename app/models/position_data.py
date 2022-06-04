from django.db import models
from .base_data import BaseData

class PositionData(BaseData, models.Model):

    employment_period = models.CharField(max_length = 255)

    working_time = models.CharField(max_length = 255)

    payment_interval_type = models.CharField(max_length=64)

    payment_per_interval = models.CharField(max_length=64)

    hiring_number = models.IntegerField()
