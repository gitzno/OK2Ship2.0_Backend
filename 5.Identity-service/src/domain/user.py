from dataclasses import dataclass
from uuid import UUID

from src.domain.exceptions import AccountBannerError, AccountDeletedError


@dataclass
class User:
    userID: UUID
    Username: str
    password: str
    Employee_ID: str = ""
    UserStatus: int = 0

    def is_login(self) -> bool:
        """0 No status,1 Active, 2 Pending, 3 Suspended, 4 Deleted"""
        match self.UserStatus:
            case 1:
                return True
            case 2:
                raise Exception("Account need validate")
            case 3:
                raise AccountBannerError()
            case 4:
                raise AccountDeletedError()

        return False;


