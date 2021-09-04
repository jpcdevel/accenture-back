from graphene_django import DjangoObjectType
from main.models import ExtendedUser, Portfolio, Security

class UserType(DjangoObjectType):
    class Meta:
        model = ExtendedUser
        fields = (
            "id", 
            "username", 
            "email", 
            "password", 
            "first_name", 
            "last_name",
        )
        
class PortfolioType(DjangoObjectType):
    class Meta:
        model = Portfolio
        fields = (
            "id",
            "cost",
            "risk_status",
            "limit",
            "predicted_income",
            "risk",
            "year_income",
            "securities",
            "recommended_securities",
            "date_created",
            "name",
            "year_change"
        )

class SecurityType(DjangoObjectType):
    class Meta:
        model = Security
        fields = (
            "id",
            "name",
            "volatility",
            "type",
            "price",
            "var",
            "tog",
            "pne",
            "type",
            "debt_load",
            "capm",
            "spoint"
        )