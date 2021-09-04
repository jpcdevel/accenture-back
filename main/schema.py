import graphene

from main.models import Portfolio, Security
from main.schemas.types import PortfolioType, SecurityType

class Query(graphene.ObjectType):
    get_all_portfolios = graphene.List(PortfolioType)

    get_portfolio_by_id = graphene.Field(PortfolioType, id=graphene.ID(required=True))

    def resolve_get_all_portfolios(root, info):
        return Portfolio.objects.all()

    def resolve_get_portfolio_by_id(root, info, id):
        return Portfolio.objects.get(id=id)


class Mutation(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
