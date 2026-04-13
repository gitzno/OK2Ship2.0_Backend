FROM mcr.microsoft.com/mssql/server:2025-latest

# Chuyển sang root để có quyền sửa file
USER root

WORKDIR /usr/src/app

# Copy toàn bộ thư mục hiện tại vào container
COPY . /usr/src/app

# Sửa lỗi CRLF của Windows và cấp quyền chạy cho script (CHỈ CẦN 1 LẦN)
RUN sed -i 's/\r$//' /usr/src/app/entrypoint.sh && \
    chmod +x /usr/src/app/entrypoint.sh

# QUAN TRỌNG: Trả lại quyền cho user mssql (Best Practice về bảo mật của Microsoft)
USER mssql

# Chạy script khởi động
CMD ["/bin/bash", "./entrypoint.sh"]