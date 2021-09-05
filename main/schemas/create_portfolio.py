import graphene

from main.models import *
from main.schemas.types import *

class CreatePortfolio(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        limit = graphene.Int(required=True)
        risk = graphene.String(required=True)

    portfolio = graphene.Field(PortfolioType)

    @classmethod
    def mutate(cls,
               root,
               info,
               name,
               limit,
               risk
               ):
        portfolio = Portfolio.objects.create(name=name, limit=limit, risk_status=risk)
        return CreatePortfolio(portfolio=portfolio)
