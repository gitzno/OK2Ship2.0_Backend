using Amazon.S3;
using Amazon.S3.Model;
using Amazon.S3.Util;
using Core.Interfaces.IRepositories;

namespace S3_Repository
{
    public class StorageObjectRepository : IStorageRepository
    {
        private readonly IAmazonS3 _s3Client;

        public StorageObjectRepository(IAmazonS3 s3Client)
        {
            _s3Client = s3Client;
        }

        public async Task<PutBucketResponse> CreateBucket(string bucketName)
        {
            try
            {
                var response = await _s3Client.PutBucketAsync(bucketName);
                return response;
            }
            catch (Exception ex)
            {
                throw new Exception($"Lỗi khởi tạo bucket: {ex.Message}");
            }
        }


        public async Task DeleteObjectAsync(string keyName, string bucketName)
        {
            try
            {
                var deleteObject = new DeleteObjectRequest
                {
                    BucketName = bucketName,
                    Key = keyName
                };
                await _s3Client.DeleteObjectAsync(deleteObject);
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }

        public async Task<bool> EnsureBucketExistsAsync(string bucketName)
        {
            return await AmazonS3Util.DoesS3BucketExistV2Async(_s3Client, bucketName);
        }

        public async Task<List<S3Bucket>> ListBucketsAsync()
        {
            return (await _s3Client.ListBucketsAsync()).Buckets;
        }

        public async Task<List<string>> getURLsUploadFileAync(List<string> fileNames, string bucketName)
        {
            var urls = new List<string>();
            foreach (var fileName in fileNames)
            {
                var request = new GetPreSignedUrlRequest
                {
                    BucketName = bucketName,
                    Key = fileName,
                    Expires = DateTime.UtcNow.AddMinutes(10), // URL có hiệu lực trong 10 phút
                    Verb = HttpVerb.PUT // Sử dụng PUT để upload file
                };
                var url = _s3Client.GetPreSignedURL(request);
                urls.Add(url);
            }
            return urls;
        }

        public Task<string> UploadFileAsync(Stream fileStream, string fileName, string contentType, string bucketName)
        {
            throw new NotImplementedException();
        }


    }
}
