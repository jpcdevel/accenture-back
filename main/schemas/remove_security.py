import graphene

from main.models import *
from main.schemas.types import *

class RemoveSecurity(graphene.Mutation):
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
        volume = VolumeSecurity.objects.filter(security=security, portfolio=portfolio)

        if volume.count() > 0:
            volume.all().last().delete()
        else:
            portfolio.securities.remove(security)

        # if portfolio.cost >= security.price:
        #     portfolio.cost = truncate(portfolio.cost - security.price, 1)
        portfolio.on_security_alter()
        portfolio.save()

        return RemoveSecurity(portfolio=portfolio)
