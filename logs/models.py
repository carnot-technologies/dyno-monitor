from django.db import models
from django.conf import settings
from django.utils.timezone import now
from dynos.models import App
from dynos.models import Dyno


# Create your models here.
class ErrorLog(models.Model):

    app_fk = models.ForeignKey(App, blank=False, null=False, on_delete=models.CASCADE)
    dyno_fk = models.ForeignKey(Dyno, blank=False, null=False, on_delete=models.CASCADE)
    category = models.CharField(blank=False, null=False, max_length=5)
    source = models.CharField(blank=True, null=True, max_length=64)
    time_stamp = models.DateTimeField(default=now, blank=True, null=True)

    class Meta:
        verbose_name = ('Error Log')
        verbose_name_plural = ('Error Logs')
        indexes = [
            models.Index(fields=['-time_stamp']),
        ]

    # Override unicode to return something meaningful
    def __str__(self):
        return str(self.dyno_fk) + settings.SEPERATOR + str(self.category)
