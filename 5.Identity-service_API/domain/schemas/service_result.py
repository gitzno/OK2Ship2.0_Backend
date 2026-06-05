from typing import Generic, TypeVar, Optional, Any

T = TypeVar('T')
class ServiceResult(Generic[T]):
    def __init__(
        self, 
        success: bool, 
        data: Optional[T] = None, 
        user_msg: Optional[str] = None, 
        dev_msg: Optional[str] = None,
        error_code: Optional[str] = None
    ):
        self.success = success       # Trạng thái True/False
        self.data = data             # Đối tượng trả về (User, Token, List...)
        self.user_msg = user_msg     # Thông báo thân thiện cho người dùng hiển thị lên UI
        self.dev_msg = dev_msg       # Thông báo chi tiết lỗi cho Developer/Log hệ thống
        self.error_code = error_code # Mã lỗi nội bộ hệ thống (Ví dụ: USER_LOCKED, PASS_INVALID)

    # Factory method: Tạo nhanh một result thành công
    @classmethod
    def ok(cls, data: T, user_msg: str = "Suggestfully", dev_msg: str = "Thành công") -> "ServiceResult[T]":
        return cls(success=True, data=data, user_msg=user_msg)

    # Factory method: Tạo nhanh một result thất bại
    @classmethod
    def fail(
        cls, 
        user_msg: str, 
        dev_msg: str, 
    ) -> "ServiceResult[None]":
        return cls(success=False, data=None, user_msg=user_msg, dev_msg=dev_msg)