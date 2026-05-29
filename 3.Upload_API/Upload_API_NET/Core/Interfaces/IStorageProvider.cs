using Core.Interfaces.IRepositories;
using System;
using System.Collections.Generic;
using System.Text;

namespace Core.Interfaces
{
    public interface IStorageProvider
    {
        IStorageRepository HotStorage { get; }
        IStorageRepository ColdStorage { get; } 
    }
}
