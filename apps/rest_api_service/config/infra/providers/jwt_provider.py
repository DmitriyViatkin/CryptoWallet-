from dishka import  Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.services.jwt_serv import JWTService

class JWTProviders(Provider):
    """ DI provider for promotion module. """

    # -------------------- REPOSITORIES --------------------

    # -------------------- SERVICES --------------------
    jwt_serv= provide(
       JWTService, scope= Scope.REQUEST) 