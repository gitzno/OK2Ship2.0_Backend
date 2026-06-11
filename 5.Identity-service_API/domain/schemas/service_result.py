from typing import Generic, TypeVar, Optional, Any

from domain.schemas.exceptions import ERROR_MESSAGES

T = TypeVar('T')
class ServiceResult(Generic[T]):
    def __init__(
        self, 
        success: bool, 
        data: Optional[T] = None, 
        user_msg: Optional[str] = None, 
        dev_msg: Optional[str] = None,
        http_request: Optional[str] = None
    ):
        self.success = success       # Trạng thái True/False
        self.data = data             # Đối tượng trả về (User, Token, List...)
        self.user_msg = user_msg     # Thông báo thân thiện cho người dùng hiển thị lên UI
        self.dev_msg = dev_msg       # Thông báo chi tiết lỗi cho Developer/Log hệ thống
        self.http_request = http_request # Mã lỗi nội bộ hệ thống (Ví dụ: USER_LOCKED, PASS_INVALID)

    def __init__(
            self,
            success: bool,
            data: Optional[T] = None,
            exception_message_code: str = None
    ):
        self.success = success  # Trạng thái True/False
        self.data = data  # Đối tượng trả về (User, Token, List...)
        self.user_msg =  ERROR_MESSAGES[exception_message_code]["user_message"]  # Thông báo thân thiện cho người dùng hiển thị lên UI
        self.dev_msg =  ERROR_MESSAGES[exception_message_code]["dev_message"]  # Thông báo chi tiết lỗi cho Developer/Log hệ thống
        self.http_request = ERROR_MESSAGES[exception_message_code]["status_code"]  # Mã lỗi nội bộ hệ thống (Ví dụ: USER_LOCKED, PASS_INVALID)

    def to_dict(self) -> dict[str, Any]:
        """Chuyển đổi ServiceResult thành dictionary để trả về API"""
        processed_data = self.data
        if hasattr(self.data, 'model_dump'):
            processed_data = self.data.model_dump()
        elif hasattr(self.data, 'dict'):  # Hỗ trợ Pydantic v1
            processed_data = self.data.dict()

        return {
            'success': self.success,
            'data': processed_data,
            'user_msg': self.user_msg,
            'dev_msg': self.dev_msg,
            'http_request': self.http_request
        }