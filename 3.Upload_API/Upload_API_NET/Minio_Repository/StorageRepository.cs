using Amazon.S3;
using Core.Interfaces.IRepositories;
using System;
using System.Collections.Generic;
using System.Text;

namespace Minio_Repository
{
    public class StorageRepository : IStorageRepository
    {
        private readonly IAmazonS3 _s3Client;


        public StorageRepository(string endPoint, string accessKey, string secretKey)
        {
            var s3Config = new AmazonS3Config
            {
                ServiceURL = endPoint, // http://localhost:9000
                ForcePathStyle = true,
            };

            _s3Client = new AmazonS3Client(accessKey, secretKey, s3Config);
        }

        public Task DeleteFileAsync(string fileName, string bucketName)
        {
            throw new NotImplementedException();
        }

        public Task<bool> EnsureBucketExistsAsync(string bucketName)
        {
            throw new NotImplementedException();
        }

        public Task<IEnumerable<string>> ListBucketsAsync()
        {
            throw new NotImplementedException();
        }

        public Task SetLifecyclePolicyAsync(string bucketName, int days)
        {
            throw new NotImplementedException();
        }

        public Task<string> UploadFileAsync(Stream fileStream, string fileName, string contentType, string bucketName)
        {
            throw new NotImplementedException();
        }
    }
}
