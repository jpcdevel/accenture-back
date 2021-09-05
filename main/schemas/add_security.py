import graphene

from main.models import *
from main.schemas.types import *

class AddSecurity(graphene.Mutation):
    class Arguments:
        idp = graphene.ID(required=True) # id portfolio
        ids = graphene.ID(required=True) # id security

    portfolio = graphene.Field(PortfolioType)

    @classmethod
    def mutate(cls,
               root,
               info,
               idp,
               ids
               ):
        security = Security.objects.get(id=ids)
        portfolio = Portfolio.objects.get(id=idp)

        if security in portfolio.securities.all():
            volume = VolumeSecurity.objects.create(security=security, portfolio=portfolio)
            volume.save()
        else:
            portfolio.securities.add(security)

        # portfolio.cost = truncate(portfolio.cost + security.price, 1)
        portfolio.on_security_alter()
        portfolio.save()

        return AddSecurity(portfolio=portfolio)
