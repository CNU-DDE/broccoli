from django.db import models
from django.conf import settings

class BaseData(models.Model):

    # Content owner foreign key
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    # Content title
    title = models.CharField(max_length=128)

    # Content
    content = models.TextField(max_length=65535)

    # Last update timestamp
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
