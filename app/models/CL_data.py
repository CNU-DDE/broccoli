from django.db import models
from .base_data import BaseData

class CLData(BaseData, models.Model):
    """
    INHERITED:
    @PRIMARY    id          BIGINT      20
    @FOREIGN    owner       VARCHAR     72
    @FIELD      title       VARCHAR     128
    @FIELD      content     TEXT        65535
    @FIELD      last_update DATETIME    6
    """
    pass
