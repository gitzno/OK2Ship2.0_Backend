from uuid import UUID

from pydantic import BaseModel

from domain.schemas.exceptions import AccountBannerError, AccountDeletedError


class LoginRequest(BaseModel):
    account: str
    password: str

class LoginResponse(BaseModel):

    UserID: UUID
    Token: str
    Username: str
    EmployeeID: str
    PasswordHash: str
    UserStatus: str

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