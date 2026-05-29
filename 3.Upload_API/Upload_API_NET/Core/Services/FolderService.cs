using Core.DTOs;
using Core.Interfaces;
using Core.Interfaces.IRepositories;
using Core.Interfaces.IServices;
using System;
using System.Collections.Generic;
using System.Net;
using System.Text;

namespace Core.Services
{
    public class FolderService : IFolderService
    {

        IStorageRepository _storage;
        public FolderService(IStorageProvider storage)
        {
            _storage = storage.HotStorage;
        }


        public async Task<ServiceResult?> getURLsUploadFileAync(string[] filesName)
        {
            List<string> urls = new List<string>();
            string msgDev = "", msgUser = "";
            HttpStatusCode statusCode = HttpStatusCode.OK;
            try
            {
                urls = await _storage.getURLsUploadFileAync(filesName.ToList(), "ok2ship-images");
            }
            catch (Exception ex)
            {
                msgDev = $"Lỗi Repository khi khởi tạo URL Upload: {ex.Message}";
                
            }

            ServiceResult result = new ServiceResult()
            {
                Success = true,
                Data = urls.ToArray(),
                StatusCode = statusCode,
                DevMsg = new List<string>() { msgDev },
                UserMsg = new List<string>() { msgUser },
            };

            return result;
        }





    }
}
