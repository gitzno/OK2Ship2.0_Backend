from datetime import datetime

import jwt

from src.domain.exceptions import TokenExpiredError, TokenInvalidError
from src.domain.user import User
from src.infrastructure.config import settings
from src.use_cases.ports.services.token_service import TokenServicePort
from typing import Dict, Any
from datetime import timezone, timedelta


class JWTService(TokenServicePort):
    def __init__(self):
        self.default_expires = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.secret_key = settings.JWT_SECRET_KEY
        self.al = settings.JWT_ALGORITHM

    def generate_access_token(self, data: Dict[str, Any], expires_delta_minutes: int = None) -> str:
        to_encode = data.copy()

        #Tính toán thời gian hết hạn của token
        mintues = expires_delta_minutes or self.default_expires
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=mintues)

        to_encode.update({"exp": expires_delta})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=[self.al])
        #Tiến hành ký và mã hóa chuỗi
        return encoded_jwt

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.al])
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.PyJWTError:
            raise TokenInvalidError()

