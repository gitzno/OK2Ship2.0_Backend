from linecache import cache

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from core.UnitOfWork import UnitOfWork
from core.config import settings
from core.interfaces.cache_interface import ICacheService
from core.providers import get_cache, get_uow
from domain.interfaces.repositories.i_unit_of_work import IUnitOfWork
from domain.schemas.exceptions import TokenExpiredError, TokenInvalidError, AccountNotFoundError, AccountNotVerify, \
    AccountBannerError, AccountDeletedError
from infrastructures.cache.redis_service import RedisService

# HTTPBearer giúp Swagger UI hiện cái ổ khóa màu xanh
security = HTTPBearer()


async def verify_global_token(credentials: HTTPAuthorizationCredentials = Depends(security),
    cache: ICacheService = Depends(get_cache),
    uow: IUnitOfWork = Depends(get_uow)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get('sub')
        token_stamp = payload.get('security_stamp')
        if user_id is None or token_stamp is None:
            raise TokenExpiredError()

        cache_key = f"user_{user_id}"

        try:
            current_stamp = await cache.get(cache_key)
        except Exception:
            current_stamp = None

        # nếu stamp không có trong cache thì lấy từ db ra

        if current_stamp is None:
            async with uow:
                user = await uow.users.get_by_id(user_id)

                if not user:
                    raise AccountNotFoundError()
                if user.UserStatus == 2:
                    raise AccountNotVerify()
                if user.UserStatus == 3:
                    raise AccountBannerError()
                if user.UserStatus == 4:
                    raise AccountDeletedError()

                current_stamp = str(user.SecurityStamp)
                print(current_stamp)
                # Nạp lại vào cache
                if current_stamp:
                    await cache.set(cache_key, current_stamp, 1500)

        # kiểm tra stamp
        if token_stamp != current_stamp:
            raise TokenExpiredError()
        return payload

    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        raise TokenInvalidError()