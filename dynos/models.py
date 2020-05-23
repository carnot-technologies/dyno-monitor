from django.db import models
from django.conf import settings


# Create your models here.
class App(models.Model):

    # PK
    name = models.CharField(unique=True, primary_key=True, max_length=64)
    url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = ('App')
        verbose_name_plural = ('Apps')

    # Override unicode to return something meaningful
    def __str__(self):
        return str(self.name)


class Dyno(models.Model):

    # FK
    app_fk = models.ForeignKey(App, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=40)
    cnt = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        unique_together = ['app_fk', 'name']
        verbose_name = ('Dyno')
        verbose_name_plural = ('Dynos')

    # Override unicode to return something meaningful
    def __str__(self):
        return str(self.app_fk.name) + settings.SEPERATOR + str(self.name)
