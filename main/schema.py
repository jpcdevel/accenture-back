import graphene

from main.models import Portfolio, Security, VolumeSecurity
from main.schemas.types import PortfolioType, SecurityType, VolumeType
from main.schemas.add_security import AddSecurity
from main.schemas.remove_security import RemoveSecurity
from main.schemas.create_portfolio import CreatePortfolio

class Query(graphene.ObjectType):
    get_all_portfolios = graphene.List(PortfolioType)
    get_portfolio_by_id = graphene.Field(PortfolioType, id=graphene.ID(required=True))
    get_all_securities = graphene.List(SecurityType)
    get_all_volumes = graphene.List(VolumeType, id=graphene.ID(required=True))

    def resolve_get_all_portfolios(root, info):
        return Portfolio.objects.all()

    def resolve_get_portfolio_by_id(root, info, id):
        return Portfolio.objects.get(id=id)

    def resolve_get_all_securities(root, info):
        return Security.objects.all()

    def resolve_get_all_volumes(root, info, id):
        return VolumeSecurity.objects.filter(portfolio__id=id)


class Mutation(graphene.ObjectType):
    add_security = AddSecurity.Field()
    remove_security = RemoveSecurity.Field()
    create_portfolio = CreatePortfolio.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
