from django.db import models


class ScriptsActivity(models.Model):
    id = models.BigAutoField(primary_key=True)
    database_reset_is_active = models.BooleanField(blank=False, null=False, default=False)