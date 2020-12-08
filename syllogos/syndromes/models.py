from django.db import models
from django.utils import timezone

# Create your models here.

BIG_BANG = timezone.datetime.strptime('20150101EET', '%Y%m%d%Z')


class Registar(models.Model):
    registar_id = models.IntegerField(primary_key=True)
    subscription_date = models.DateField(null=False, default=BIG_BANG)
    name = models.CharField(max_length=1024, null=False)
    email = models.EmailField(unique=True)
    dept = models.FloatField(default=0.0)

    @staticmethod
    def get_by_email(email):
        return Registar.objects.get(email=email).last()

    @staticmethod
    def get_by_registar_id(registar_id):
        try:
            return Registar.objects.get(registar_id=registar_id)
        except Registar.DoesNotExist:
            return None
