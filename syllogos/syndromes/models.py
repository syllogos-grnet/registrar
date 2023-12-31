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

    def __str__(self):
        return f'{self.registar_id}. {self.name} <{self.email}>'

    @staticmethod
    def get_by_email(email):
        return Registar.objects.get(email=email)

    @staticmethod
    def get_by_registar_id(registar_id):
        try:
            return Registar.objects.get(registar_id=registar_id)
        except Registar.DoesNotExist:
            return None


class NotificationLog(models.Model):
    registar = models.ForeignKey(
        Registar, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(max_length=1024, null=False)
    timestamp = models.DateTimeField(null=False, default=timezone.now)
    description = models.CharField(max_length=256, null=True, default="email")
