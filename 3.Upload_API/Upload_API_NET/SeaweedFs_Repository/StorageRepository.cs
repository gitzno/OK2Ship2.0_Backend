using Amazon.S3;
using Amazon.S3.Model;
using Core.Interfaces.IRepositories;
using System;
using System.Collections.Generic;
using System.Text;

namespace SeaweedFs_Repository
{
    public class StorageRepository : IStorageRepository
    {
        private readonly IAmazonS3 _s3Client;

        public StorageRepository(string accesskey, string secretkey, string endpoint)
        {

            var s3Config = new AmazonS3Config
            {
                ServiceURL = endpoint,
                ForcePathStyle = true, // Bắt buộc true với MinIO/SeaweedFS
                UseHttp = true         // True nếu chạy localhost không có HTTPS
            };

            _s3Client = new AmazonS3Client(
                accesskey,
                secretkey,
                s3Config
            );
        }
        public async Task EnsureBucketExistsAsync(string bucketName)
        {
            try
            {
                var bucketExists = await Amazon.S3.Util.AmazonS3Util.DoesS3BucketExistV2Async(_s3Client, bucketName);
                if (!bucketExists)
                {
                    var putBucketRequest = new PutBucketRequest
                    {
                        BucketName = bucketName,
                        UseClientRegion = true
                    };
                    await _s3Client.PutBucketAsync(putBucketRequest);
                    Console.WriteLine($"[Storage] Created bucket: {bucketName}");
                }
            }
            catch (Exception ex)
            {
                // Nếu lỗi ở đây, bạn sẽ thấy ngay trong console khi app start
                Console.WriteLine($"[Storage Error] Could not ensure bucket {bucketName}: {ex.Message}");
                throw;
            }
        }
        public async Task<IEnumerable<string>> ListBucketsAsync()
        {
            // Lệnh này giờ đây sẽ trả về danh sách các folder nằm ở root của SeaweedFS
            var response = await _s3Client.ListBucketsAsync();
            return response.Buckets.Select(b => b.BucketName).ToList();
        }

        public async Task<string> UploadFileAsync(string fileName, Stream fileStream, string contentType, string bucketName , string ttl = "730d")
        {
            // Khởi tạo request
            var putRequest = new PutObjectRequest
            {
                BucketName = bucketName,
                Key = fileName,
                InputStream = fileStream,
                ContentType = contentType,
                DisablePayloadSigning = true // Tối ưu tốc độ cho file lớn
            };

            // Gắn TTL (Thời gian sống 2 năm) vào Metadata
            putRequest.Metadata.Add("Ttl", ttl);

            // Upload thẳng lên SeaweedFS
            await _s3Client.PutObjectAsync(putRequest);

            return fileName;
        }

   
    }
}
