from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def get_scorring_result(number):
    if number < 33:
        return 1
    elif 33 < number < 66:
        return 2
    elif number > 66:
        return 3


class ExtendedUser(AbstractUser):
    email = models.EmailField(blank=False, unique=True, max_length=255, verbose_name='User Email')

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

# Модель для покупки нескольких акций одного вида
class VolumeSecurity(models.Model):
    security = models.ForeignKey('Security', on_delete=models.DO_NOTHING, null=True, blank=True)
    portfolio = models.ForeignKey('Portfolio', on_delete=models.DO_NOTHING, null=True, blank=True)

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
    capm = models.FloatField(default=0.0, blank=True)
    volatility = models.FloatField(default=0.0, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for sec in Security.objects.all():
            if sec.spoint < 33 and self.risk_status == "low":
                self.recommended_securities.add(sec)
            elif 33 < sec.spoint < 66 and self.risk_status == "medium":
                self.recommended_securities.add(sec)
            elif sec.spoint > 66 and self.risk_status == "high":
                self.recommended_securities.add(sec)
        super().save()


    def on_security_alter(self):
        sum = 0
        predicted_income = 0
        risk = 0
        capm = 0
        volatility = 0

        for sec in self.securities.all():
            sum += sec.price
            predicted_income += sec.capm
            risk += sec.spoint
            capm += sec.capm
            volatility += sec.volatility

        for sec in VolumeSecurity.objects.filter(portfolio__id=self.id):
            sum += sec.security.price
            predicted_income += sec.security.capm
            risk += sec.security.spoint
            capm += sec.security.capm
            volatility += sec.security.volatility

        self.cost = truncate(sum, 1)
        if predicted_income != 0:
            self.predicted_income = truncate(predicted_income / (self.securities.all().count() + VolumeSecurity.objects.filter(portfolio__id=self.id).count()), 1)
        else:
            self.predicted_income = 0

        if risk != 0:
            self.risk = truncate(risk / (self.securities.all().count() + VolumeSecurity.objects.filter(portfolio__id=self.id).all().count()), 1)
        else:
            self.risk = 0

        if capm != 0:
            self.capm = truncate(capm / (self.securities.all().count() + VolumeSecurity.objects.filter(portfolio__id=self.id).all().count()), 1)
        else:
            self.capm = 0

        if volatility != 0:
            self.volatility = truncate(volatility / (self.securities.all().count() + VolumeSecurity.objects.filter(portfolio__id=self.id).all().count()), 1)
        else:
            self.volatility = 0
        super().save()

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        sp = 0

        # volatility
        if self.volatility < 19:
            sp += 6
        elif 19 < self.volatility < 42:
            sp += 12
        elif self.volatility > 42:
            sp += 20

        # var
        if 5 < self.var < 15:
            sp += 4
        elif 15 < self.var < 25:
            sp += 12
        elif 25 < self.var:
            sp += 18

        # tog
        if 50 < self.tog < 100:
            sp += 3
        elif 100 < self.tog < 150:
            sp += 6
        elif 150 < self.tog < 200:
            sp += 12
        elif self.tog > 200:
            sp += 18

        # type
        if self.type == 'curr':
            sp += 2
        elif self.type == 'obl':
            sp += 4
        elif self.type == 'gobl' or self.type == 'fut':
            sp += 6
        elif self.type == 'fcom':
            sp += 8
        elif self.type == 'scom':
            sp += 16
        elif self.type == 'lcom':
            sp += 18

        # P/E
        if (
            self.type == 'fcom'
            or self.type == 'scom'
            or self.type == 'lcom'
        ):
            if self.pne < 4:
                sp += 5
            elif 4 < self.pne < 7.5:
                sp += 10
            elif 7.5 < self.pne < 12:
                sp += 14
            elif self.pne > 12:
                sp += 16

            # debt load
            if 0.5 < self.debt_load < 0.7:
                sp += 4
            elif 0.7 < self.debt_load < 1:
                sp += 8
            elif self.debt_load > 1:
                sp += 12

        self.spoint = sp
        super().save()



