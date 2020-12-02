from django.db import models
from django.utils import timezone

# Create your models here.

BIG_BANG = timezone.datetime.strptime('20150101EET', '%Y%m%d%Z')


class Registar(models.Model):
    registar_id = models.IntegerField(primary_key=True)
    subscription_date = models.DateField(null=False, default=BIG_BANG)
    name = models.CharField(max_length=1024, null=False)
    email = models.EmailField()
    dept = models.FloatField(default=0.0)
