using Core.DTOs;
using System;
using System.Collections.Generic;
using System.Text;

namespace Core.Interfaces.IServices
{
    public interface IFolderService
    {
        /// <summary>
        /// Đẩy danh sách tên file lên S3 để lấy URL upload file
        /// </summary>
        /// <param name="filesName">
        /// Danh sách tên file cần upload, có thể là tên file gốc và prefix của nó ví dụ "images/abc.jpg" hoặc "abc.jpg", nếu có prefix thì sẽ được giữ nguyên khi upload lên S3, nếu không có prefix thì sẽ được tự động thêm prefix "images/" vào trước tên file khi upload lên S3
        /// </param>
        /// <returns>
        /// Danh sách url được upload.
        /// Danh sách message sinh ra cho user hoặc dev.
        /// Mã lỗi theo dạng http
        /// Trạng thái thành công hay thất bại của việc lấy url upload file
        /// </returns>
        public Task<ServiceResult?> getURLsUploadFileAync(string[] filesName);
    }
}
