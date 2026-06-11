
from domain.schemas.exceptions import DomainException
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback

def app_global_exception_middleware(app: FastAPI):

    

    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        # Tự động chuyển đổi Lỗi Nghiệp Vụ thành JSON chuẩn BaseApiResponse
        return JSONResponse(
            status_code = exc.status_code,
            content={
                "success": False,
                "user_msg": exc.user_msg,
                "dev_msg": exc.dev_msg,
                "error_code": exc.error_code
            }
        )

    # 1. Bắt các lỗi HTTP (do bạn chủ động raise HTTPException)
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # Nếu dev đã truyền dict vào detail (như bài trước ta làm)
        if isinstance(exc.detail, dict) and "success" in exc.detail:
            content = exc.detail
        else:
            content = {
                "success": False,
                "user_msg": str(exc.detail),
                "error_code": f"HTTP_{exc.status_code}"
            }

        return JSONResponse(status_code=exc.status_code, content=content)

    # 2. Bắt lỗi Validation của Pydantic (Gửi sai form, thiếu field)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "user_msg": "Dữ liệu đầu vào không hợp lệ.",
                "dev_msg": exc.errors(),  # Pydantic trả về mảng lỗi rất chi tiết
                "error_code": "VALIDATION_ERROR"
            }
        )

    # 3. Bắt TẤT CẢ các Exception còn lại (Lỗi sập Server 500)
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # In lỗi đỏ lòm ra Terminal để dev dễ debug
        traceback.print_exc()

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "user_msg": "Đã xảy ra lỗi hệ thống, vui lòng thử lại sau.",
                "dev_msg": repr(exc),  # Giấu cái này đi nếu đưa lên Production
                "error_code": "INTERNAL_SERVER_ERROR"
            }
        )