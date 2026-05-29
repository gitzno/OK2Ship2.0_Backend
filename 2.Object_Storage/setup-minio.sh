#!/bin/sh

# --- 1. HÀM KIỂM TRA KẾT NỐI (POLLING) ---
wait_for_minio() {
  echo "Checking connection to MinIO nodes using mc..."
  
  # Chờ Ví Nóng (SSD)
  # Thử đặt alias cho đến khi không còn lỗi kết nối
  until mc alias set hot http://minio-hot:9000 ${MINIO_ROOT_USER_HOT} ${MINIO_ROOT_PASSWORD_HOT} > /dev/null 2>&1; do
    echo "Waiting for Hot Storage (SSD) to be ready..."
    sleep 3
  done

  # Chờ Ví Lạnh (HDD)
  until mc alias set cold http://minio-cold:9000 ${MINIO_ROOT_USER_COLD} ${MINIO_ROOT_PASSWORD_COLD} > /dev/null 2>&1; do
    echo "Waiting for Cold Storage (HDD) to be ready..."
    sleep 3
  done
}

# --- 2. THỰC THI ---
wait_for_minio

echo "--- All MinIO nodes are UP and Authenticated. Starting configuration... ---"

# Các lệnh mb (tạo bucket)
mc mb --ignore-existing hot/${BUCKET_NAME_IMAGES}
mc mb --ignore-existing hot/${BUCKET_NAME_REPORTS}
mc mb --ignore-existing cold/${BUCKET_NAME_IMAGES}-nas
mc mb --ignore-existing cold/${BUCKET_NAME_REPORTS}-nas

# Khởi tạo Tier (Nối ống)
mc ilm tier add s3 hot IMAGES_HDD_TIER --endpoint http://minio-cold:9000 --access-key ${MINIO_ROOT_USER_COLD} --secret-key ${MINIO_ROOT_PASSWORD_COLD} --bucket ${BUCKET_NAME_IMAGES}-nas
mc ilm tier add s3 hot REPORTS_HDD_TIER --endpoint http://minio-cold:9000 --access-key ${MINIO_ROOT_USER_COLD} --secret-key ${MINIO_ROOT_PASSWORD_COLD} --bucket ${BUCKET_NAME_REPORTS}-nas

# Áp dụng Policy
mc ilm add --transition-days 120 --transition-tier IMAGES_HDD_TIER --expiry-days 730 hot/${BUCKET_NAME_IMAGES}
mc ilm add --transition-days 120 --transition-tier REPORTS_HDD_TIER --expiry-days 730 hot/${BUCKET_NAME_REPORTS}

echo "--- MINIO TIERING INFRASTRUCTURE SETUP COMPLETED ---"