from src.domain.exceptions import AccountDeletedError, AccountNotFoundError, PasswordIncorrectError
from src.domain.user import User
from src.use_cases.ports.repositories import user_repository
from src.use_cases.ports.services import token_service, PasswordHasherService

class UserUseCase:
    def __init__(self, userRepo: user_repository, tokenService: token_service, passwordHahser: PasswordHasherService ):
        self.userRepo = userRepo
        self.tokenService = tokenService
        self.PasswordHashed = passwordHahser

    def login(self, account: str, password: str) -> str:
        user = self.userRepo.get_user_by_username(account)

        #Kiểm tra tài khoản có tồn tại hay không
        if not user:
            raise Exception("Account not found")

        #Kiểm tra trạng thái tài khoản
        if not user.is_login():
           raise AccountNotFoundError()

        #So sánh mật khẩu
        if not self.PasswordHashed.verify_password(password, user.password):
            raise PasswordIncorrectError()

        #Khởi tạo thông tin
        token_payload = {
            "sub":  user.userID,
            "username": user.username,
        }

        #Khởi tạo token
        token = self.tokenService.generate_token(token_payload)

        return token
