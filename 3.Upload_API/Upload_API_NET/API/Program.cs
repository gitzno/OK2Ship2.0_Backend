using Amazon.S3;
using Core.Interfaces;
using Core.Interfaces.IRepositories;
using Core.Interfaces.IServices;
using Core.Services;
using S3_Repository;
using S3_Repository.Wrappers;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();

// register swagger for API documentation   
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Đăng ký DI (Dependency Injection)


// cấu hình cho object storage service
var hotStorageSettings = builder.Configuration.GetSection("MinIO_HOT");
var coldStorageSettings = builder.Configuration.GetSection("MinIO_COLD");

// 2. Cấu hình Client cho VÍ NÓNG (Hot Storage - SSD)
var hotS3Config = new AmazonS3Config
{
    ServiceURL = hotStorageSettings["Endpoint"],
    ForcePathStyle = true
};
var coldS3Config = new AmazonS3Config
{
    ServiceURL = coldStorageSettings["Endpoint"],
    ForcePathStyle = true
};

builder.Services.AddKeyedSingleton<IAmazonS3>("HotStorage", (sp, key) =>
    new AmazonS3Client(hotStorageSettings["AccessKey"], hotStorageSettings["SecretKey"], hotS3Config));

builder.Services.AddKeyedSingleton<IAmazonS3>("ColdStorage", (sp, key) =>
    new AmazonS3Client(coldStorageSettings["AccessKey"], coldStorageSettings["SecretKey"], coldS3Config));


builder.Services.AddScoped<IStorageProvider>(sp =>
{
    var hotClient = sp.GetRequiredKeyedService<IAmazonS3>("HotStorage");
    var coldClient = sp.GetRequiredKeyedService<IAmazonS3>("ColdStorage");

    // Khởi tạo Provider - lớp này sẽ tự tạo ra 2 Repository riêng biệt bên trong
    return new StorageProvider(hotClient, coldClient);
});


////----end of DI configuration



// Set full cors for all connection
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

// Đăng ký dịch vụ FolderService để xử lý logic liên quan đến folder và file

builder.Services.AddScoped<IFolderService, FolderService>();


var app = builder.Build();

// Configure the HTTP request pipeline.
// 2. Kích hoạt giao diện Swagger UI (Thường chỉ nên bật ở môi trường Development)
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "OK2Ship API v1");
        // Giúp Swagger UI mở lên ngay ở trang chủ (localhost:port) thay vì phải gõ /swagger
        c.RoutePrefix = string.Empty;
    });
}

//allow
app.UseCors("AllowAll");

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

// Đoạn code test kết nối

app.Run();
