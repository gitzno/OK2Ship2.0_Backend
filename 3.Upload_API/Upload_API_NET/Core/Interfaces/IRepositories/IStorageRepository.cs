using Amazon.S3.Model;
using System;
using System.Collections.Generic;
using System.Text;

namespace Core.Interfaces.IRepositories
{
    public interface IStorageRepository
    {
        /// <summary>
        /// Kiểm tra sự tồn tại của bucket
        /// </summary>
        /// <param name="bucketName">Bucket's name</param>
        /// <returns>True nếu bucket tồn tại , false nếu không tồn tại</returns>
        public Task<bool> EnsureBucketExistsAsync(string bucketName);


        /// <summary>
        /// Create bucket with s3 client, if bucket already exists, it will return the existing bucket
        /// </summary>
        /// <param name="bucketName">bucket's name</param>
        /// <returns></returns>
        public Task<PutBucketResponse> CreateBucket(string bucketName);

        /// <summary>
        /// Get list pre-signed URL for upload file to S3 bucket, each URL will be valid for 10 minutes
        /// </summary>
        /// <param name="fileNames">List of file names to be uploaded</param>
        /// <param name="bucketName">Name of the S3 bucket</param>
        /// <returns>List of pre-signed URLs for uploading files</returns>
        Task<List<string>> getURLsUploadFileAync(List<string> fileNames, string bucketName);



        /// <summary>
        /// Not implement
        /// </summary>
        /// <param name="fileStream"></param>
        /// <param name="fileName"></param>
        /// <param name="contentType"></param>
        /// <param name="bucketName"></param>
        /// <returns></returns>
        public Task<string> UploadFileAsync(Stream fileStream, string fileName, string contentType, string bucketName);

        /// <summary>
        /// List bucket
        /// </summary>
        /// <returns></returns>
        public Task<List<S3Bucket>> ListBucketsAsync();


        /// <summary>
        /// Xóa object trong bucket, nếu object không tồn tại sẽ trả về lỗi
        /// </summary>
        /// <param name="kayName"> key object</param>
        /// <param name="bucketName">name bucket</param>
        /// <returns></returns>
        public Task DeleteObjectAsync(string kayName, string bucketName);
    }
}
