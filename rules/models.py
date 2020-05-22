from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from dynos.models import Dyno


ACTION_CHOICES = (
    ('No Action', 'No Action'),
    ('Restart Dyno', 'Restart Dyno'),
    ('Restart App', 'Restart App'),
)

LOG_SOURCE_CHOICES = (
    ('heroku', 'heroku'),
    ('app', 'app')
)


# Create your models here.
class HError(models.Model):

    HXX_ERROR_CHOICES = (
        ('H10', 'H10'),
        ('H12', 'H12'),
        ('H14', 'H14'),
        ('H80', 'H80'),
        ('H99', 'H99'),
    )

    # PK
    # TODO: HErrors are only applicable for web dynos. Enforce further check
    dyno_fk = models.ForeignKey(Dyno, blank=False, null=False, on_delete=models.CASCADE)
    category = models.CharField(max_length=5, choices=HXX_ERROR_CHOICES, default='H10')
    least_count = models.IntegerField(blank=False, null=False, default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    time_window = models.IntegerField(blank=False, null=False, default=300, validators=[MinValueValidator(60), MaxValueValidator(3600)])
    email_alert = models.BooleanField(blank=False, null=False, default=False)
    log = models.BooleanField(blank=False, null=False, default=False)
    action = models.CharField(max_length=15, choices=ACTION_CHOICES, default='No Action')
    log_source = models.CharField(max_length=40, choices=LOG_SOURCE_CHOICES, default='heroku')
    log_dyno = models.CharField(max_length=40, blank=False, null=False, default='router')

    class Meta:
        unique_together = ['dyno_fk', 'category']
        verbose_name = ('Hxx Error')
        verbose_name_plural = ('Hxx Errors')

    def export_dict(self):
        res = self.__dict__.copy()
        res.pop('_state', None)
        res['app'] = self.dyno_fk.app_fk.name
        res['dyno'] = self.dyno_fk.name
        res['search_key'] = 'code=' + self.category
        return res

    # Override unicode to return something meaningful
    def __str__(self):
        return str(self.dyno_fk) + settings.SEPERATOR + str(self.category)


class RError(models.Model):

    RXX_ERROR_CHOICES = (
        ('R14', 'R14'),
        ('R15', 'R15'),
        ('R99', 'R99'),
    )

    # PK
    dyno_fk = models.ForeignKey(Dyno, blank=False, null=False, on_delete=models.CASCADE)
    category = models.CharField(max_length=5, choices=RXX_ERROR_CHOICES, default='R14')
    least_count = models.IntegerField(blank=False, null=False, default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    time_window = models.IntegerField(blank=False, null=False, default=300, validators=[MinValueValidator(60), MaxValueValidator(3600)])
    email_alert = models.BooleanField(blank=False, null=False, default=False)
    log = models.BooleanField(blank=False, null=False, default=False)
    action = models.CharField(max_length=15, choices=ACTION_CHOICES, default='No Action')
    log_source = models.CharField(max_length=40, choices=LOG_SOURCE_CHOICES, default='heroku')
    log_dyno = models.CharField(max_length=40, blank=False, null=False, default='router')

    class Meta:
        unique_together = ['dyno_fk', 'category']
        verbose_name = ('Rxx Error')
        verbose_name_plural = ('Rxx Errors')

    def export_dict(self):
        res = self.__dict__.copy()
        res.pop('_state', None)
        res['app'] = self.dyno_fk.app_fk.name
        res['dyno'] = self.dyno_fk.name
        res['search_key'] = 'Error ' + self.category
        return res

    # Override unicode to return something meaningful
    def __str__(self):
        return str(self.dyno_fk) + settings.SEPERATOR + str(self.category)
