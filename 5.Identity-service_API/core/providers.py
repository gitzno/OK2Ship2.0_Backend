from core.interfaces.cache_interface import ICacheService
from domain.interfaces.repositories.i_unit_of_work import IUnitOfWork

from infrastructures.cache.redis_service import RedisService
from core.UnitOfWork import UnitOfWork

from infrastructures.connections import async_session_maker, redis_client

def get_uow() -> IUnitOfWork:
    """Cung cấp Unit of Work (Database)"""
    return UnitOfWork(async_session_maker)

def get_cache() -> ICacheService:
    """Cung cấp Cache Service (Redis)"""
    return RedisService(redis_client)