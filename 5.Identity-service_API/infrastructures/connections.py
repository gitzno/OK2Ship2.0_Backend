
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from redis.asyncio import Redis
from core.config import settings

print("🔄 Đang khởi tạo các kết nối hạ tầng...")

# 1. KHỞI TẠO KẾT NỐI DATABASE (SQL SERVER)
db_engine = create_async_engine(
    settings.DATA_TABLE_URL,
    echo=False,           # Tắt log SQL để terminal đỡ rối (bật True khi debug)
    pool_pre_ping=True,   # Tự động kiểm tra kết nối "sống/chết" trước khi query
    pool_size=10,         # Số lượng kết nối duy trì sẵn
    max_overflow=20       # Số lượng kết nối tối đa khi quá tải
)

async_session_maker = async_sessionmaker(
    bind=db_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 2. KHỞI TẠO KẾT NỐI CACHE (REDIS)
redis_client = settings.REDIS_URL


print("✅ Khởi tạo kết nối hoàn tất!")