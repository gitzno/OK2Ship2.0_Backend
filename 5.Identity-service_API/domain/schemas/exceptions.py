from fastapi import status


class DomainException(Exception):
    def __init__(self, error_code: str, status_code: int = 400):
        self.user_msg = ERROR_MESSAGES[error_code]["user_message"]
        self.dev_msg = ERROR_MESSAGES[error_code]["dev_message"]
        self.error_code = error_code
        self.status_code = ERROR_MESSAGES[error_code]["status_code"]
        super().__init__(self.user_msg)



ERROR_MESSAGES = {
    "ACCOUNT_BANNED": {
        "dev_message": "This account was banned by admin.",
        "user_message": "Tài khoản của bạn đã bị cấm!",
        "status_code": status.HTTP_403_FORBIDDEN # 403: Biết user là ai, nhưng cấm cửa không cho vào.
    },

    "ACCOUNT_DELETED": {
        "dev_message": "This account was soft-deleted.",
        "user_message": "Tài khoản của bạn không tồn tại hoặc đã bị xóa!",
        "status_code": status.HTTP_404_NOT_FOUND # 404: Không tìm thấy tài nguyên.
    },

    "ACCOUNT_NOT_FOUND": {
        "dev_message": "This account was not found in the database.",
        "user_message": "Tài khoản hoặc mật khẩu không chính xác!",
        "status_code": status.HTTP_404_NOT_FOUND # 404: Không tìm thấy.
    },

    "PASSWORD_INCORRECT": {
        "dev_message": "Password hash mismatch.",
        "user_message": "Tài khoản hoặc mật khẩu không chính xác!",
        "status_code": status.HTTP_401_UNAUTHORIZED # 401: Sai thông tin xác thực.
    },

    "TOKEN_EXPIRED": {
        "dev_message": "This JWT session has expired.",
        "user_message": "Phiên đăng nhập hết hạn, xin hãy đăng nhập lại!",
        "status_code": status.HTTP_401_UNAUTHORIZED # 401: Lỗi liên quan đến xác thực danh tính.
    },

    "TOKEN_INVALID": {
        "dev_message": "This JWT token is malformed or invalid.",
        "user_message": "Phiên đăng nhập không hợp lệ, xin hãy đăng nhập lại!",
        "status_code": status.HTTP_401_UNAUTHORIZED # 401: Lỗi liên quan đến xác thực danh tính.
    },

    "USER_DUPLICATE": {
        "dev_message": "This account already exists in the database.",
        "user_message": "Tài khoản này đã tồn tại trên hệ thống!",
        "status_code": status.HTTP_409_CONFLICT # 409: Xung đột dữ liệu (Tạo mới nhưng bị trùng).
    },

    "ACCOUNT_VALIDATION": {
        "dev_message": "Request payload failed regex validation.",
        "user_message": "Tài khoản hoặc mật khẩu không đúng định dạng cho phép.",
        "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY # 422: Dữ liệu gửi lên đúng kiểu (string), nhưng sai định dạng (regex).
    },

    "OK": {
        "dev_message": "Get data successful.",
        "user_message": "Lấy dữ liệu thành công",
        "status_code": status.HTTP_200_OK
    },

    "OK_CREATE": {
        "dev_message": "Create data successful.",
        "user_message": "Tạo dữ liệu thành công",
        "status_code": status.HTTP_201_CREATED
    },

    "OK_ACCEPTED": {
        "dev_message": "Process is accepted",
        "user_message": "Quá trình đã bắt đầu",
            "status_code": status.HTTP_202_ACCEPTED
    },

    "OK_NOCONTENT": {
        "dev_message": "Get data successful.",
        "user_message": "Lấy dữ liệu thành công",
        "status_code": status.HTTP_204_NO_CONTENT
    },

}

class AccountBannerError(DomainException):
    def __init__(self, custom_message: str ):
        super().__init__(error_code="ACCOUNT_BANNED")

class AccountDeletedError(DomainException):
    def __init__(self, custom_message: str ):
        super().__init__(error_code="ACCOUNT_DELETED")


class AccountNotFoundError(DomainException):
    def __init__(self, custom_message: str ):
        super().__init__(error_code="ACCOUNT_NOT_FOUND")

class PasswordIncorrectError(DomainException):
    def __init__(self, custom_message: str ):
        super().__init__(error_code="PASSWORD_INCORRECT")

class TokenExpiredError(DomainException):
    def __init__(self, custom_message: str ):
        super().__init__(error_code="TOKEN_EXPIRED")

class TokenInvalidError(DomainException):
    def __init__(self, custom_message: str ):
        super().__init__(error_code="TOKEN_INVALID")

class DuplicateAccountError(DomainException):
    def __init__(self, custom_message: str ):
        super().__init__(error_code="USER_DUPLICATE")