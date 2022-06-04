from django.db import models
from .base_data import BaseData

class PositionData(BaseData, models.Model):
    """
    INHERITED:
    @PRIMARY    id          BIGINT      20 
    @FOREIGN    owner       VARCHAR     72 
    @FIELD      title       VARCHAR     128 
    @FIELD      content     TEXT        65535 
    @FIELD      last_update DATETIME    6
    """                                

    employment_period = models.CharField(max_length = 255)

    working_time = models.CharField(max_length = 255)

    payment_interval_type = models.CharField(max_length=64)

    payment_per_interval = models.CharField(max_length=64)

    hiring_number = models.IntegerField()
