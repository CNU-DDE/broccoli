from django.db import models
from django.conf import settings

class BaseData(models.Model):

    # Cover letter owner foreigh key
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    # Cover letter content
    content = models.TextField(max_length=65535)

    # Timestamp of the updating
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
