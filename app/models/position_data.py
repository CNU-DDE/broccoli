from django.db import models
from .base_data import BaseData

class PositionData(BaseData, models.Model):

    employment_period = models.CharField(
        max_length = 255,
    )

    working_time = models.CharField(
        max_length = 255,
    )

    payment_interval_type = models.SmallIntegerField()

    payment_per_internal = models.IntegerField()

    hiring_number = models.IntegerField()
