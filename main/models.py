from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class ExtendedUser(AbstractUser):
    email = models.EmailField(blank=False, unique=True, max_length=255, verbose_name='User Email')

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

# Портфель
class Portfolio(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    cost = models.FloatField(blank=True, default=0.0) # Цена всего портфеля
    year_change = models.IntegerField(default=0, blank=True)

    # При анкетировании:
    risk_status = models.CharField(max_length=20, default='medium', blank=True) # Риск статус портфеля (low, medium, high)
    limit = models.IntegerField(blank=True, default=0) # Лимит предполагаемых потерь

    predicted_income = models.IntegerField(blank=True, default=0)
    risk = models.IntegerField(blank=True, default=0)
    year_income = models.IntegerField(blank=True, default=0)
    securities = models.ManyToManyField('Security', related_name='portfolio_securities', blank=True)
    recommended_securities = models.ManyToManyField('Security', related_name='portfolio_recommended_securities', blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return str(self.risk_status) + str(self.id)

# Ценная бумага
class Security(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    volatility = models.IntegerField(default=0, blank=True)
    type = models.CharField(max_length=40, blank=True) # Тип ценной бумаги
    price = models.FloatField(default=0.0, blank=True)
    var = models.IntegerField(default=0, blank=True)
    tog = models.IntegerField(default=0, blank=True) # temp of growth
    pne = models.FloatField(default=0.0, blank=True) # P/E
    debt_load = models.FloatField(default=0.0, blank=True)
    capm = models.FloatField(default=0.0, blank=True)
    spoint = models.IntegerField(default=0, blank=True) # Скорринг бал
