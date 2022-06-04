from django.db import models
from django.conf import settings
from .base_data import BaseData
from .position_data import PositionData

class ResumeData(BaseData, models.Model):
    """
    INHERITED:
    @PRIMARY    id          BIGINT      20 
    @FOREIGN    owner       VARCHAR     72 
    @FIELD      title       VARCHAR     128 
    @FIELD      content     TEXT        65535 
    @FIELD      last_update DATETIME    6
    """                                

    # Resume verifier
    verifier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verifier",
        blank=True,
        null=True,
        default=None,
    )

    # Submitted position
    position = models.ForeignKey(
        PositionData,
        on_delete=models.CASCADE,
        related_name="position",
        blank=True,
        null=True,
        default=None,
    )
