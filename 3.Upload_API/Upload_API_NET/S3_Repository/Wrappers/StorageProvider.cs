using Amazon.S3;
using Core.Interfaces;
using Core.Interfaces.IRepositories;

namespace S3_Repository.Wrappers
{
    public class StorageProvider : IStorageProvider
    {
        public IStorageRepository HotStorage { get; }
        public IStorageRepository ColdStorage { get; }

        public StorageProvider(IAmazonS3 hotClient, IAmazonS3 coldClient)
        {
            HotStorage = new StorageObjectRepository(hotClient);
            ColdStorage = new StorageObjectRepository(coldClient);
        }
    }
}
