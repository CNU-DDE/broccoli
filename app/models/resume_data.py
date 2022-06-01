from django.db import models
from .base_data import BaseData

class ResumeData(BaseData, models.Model):

    accessible_to = models.CharField(
        max_length = 72,
        default = "*",
        blank = True,
    )
