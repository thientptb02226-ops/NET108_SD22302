using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.Text;
using System.Text.Json;
using AiNativeCommerce.Api.Data;

var builder = WebApplication.CreateBuilder(args);

// 1. Port Configuration (Port 5000)
builder.WebHost.UseUrls("http://localhost:5000");

// 2. Add DbContext with SQLite
builder.Services.AddDbContext<CommerceDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection") ?? "Data Source=dev.db"));

// 3. Add CORS for Frontend
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod()
              .WithExposedHeaders("Idempotency-Key", "X-Idempotent-Replay");
    });
});

// 4. Add JWT Authentication
var jwtSecret = builder.Configuration["Jwt:Secret"] ?? "ai_native_commerce_super_secret_jwt_key_2026";
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = "AiNativeCommerce",
            ValidAudience = "AiNativeCommerceClients",
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtSecret))
        };
    });

builder.Services.AddAuthorization();

// 5. Add Controllers with camelCase JSON formatting
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
        options.JsonSerializerOptions.DictionaryKeyPolicy = JsonNamingPolicy.CamelCase;
    });

builder.Services.AddEndpointsApiExplorer();

var app = builder.Build();

// 6. Seed Database on Startup
using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<CommerceDbContext>();
    DbInitializer.Initialize(context);
}

// 7. Middlewares
app.UseCors("AllowAll");

app.UseAuthentication();
app.UseAuthorization();

// 8. Health Check & Root Landing Page
app.MapGet("/health", () => Results.Ok(new
{
    status = "healthy",
    service = "AI-Native Commerce ASP.NET Core Web API (C# .NET 10/8)",
    timestamp = DateTime.UtcNow,
    architecture = "Enterprise Saga with 15-Min Quote Lock & Idempotency"
}));

app.MapGet("/", () => Results.Content(@"
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'/>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'/>
    <title>AI-Native Commerce API — C# ASP.NET Core</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; background: #090d16; color: #f8fafc; padding: 40px 16px; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 85vh; }
        .card { max-width: 620px; width: 100%; background: #131c31; padding: 36px; border-radius: 24px; border: 1px solid #1e293b; box-shadow: 0 20px 40px rgba(0,0,0,0.6); text-align: center; }
        h1 { color: #818cf8; margin: 12px 0 6px 0; font-size: 26px; font-weight: 800; }
        p { color: #94a3b8; font-size: 14px; line-height: 1.6; margin: 8px 0; }
        .badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 9999px; font-size: 12px; font-weight: 700; }
        .badge::before { content: ''; width: 8px; height: 8px; border-radius: 50%; background: #34d399; display: inline-block; }
        .btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 14px 28px; background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; border-radius: 14px; text-decoration: none; font-weight: 700; font-size: 15px; margin: 20px 0 10px 0; box-shadow: 0 10px 20px rgba(79, 70, 229, 0.3); transition: transform 0.2s; }
        .btn:hover { transform: translateY(-2px); }
        .endpoints { text-align: left; background: #0b1120; padding: 16px 20px; border-radius: 16px; border: 1px solid #1e293b; margin-top: 24px; font-size: 12px; }
        .endpoints h4 { margin: 0 0 10px 0; color: #e2e8f0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; }
        .endpoints ul { list-style: none; padding: 0; margin: 0; }
        .endpoints li { padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center; }
        .endpoints li:last-child { border-bottom: none; }
        .method { font-weight: 800; font-size: 10px; padding: 2px 6px; border-radius: 4px; background: #1e1b4b; color: #818cf8; margin-right: 6px; }
        .method.post { background: #064e3b; color: #34d399; }
        .path { font-family: ui-monospace, monospace; color: #38bdf8; font-weight: 600; }
        .desc { color: #64748b; font-size: 11px; }
    </style>
</head>
<body>
    <div class='card'>
        <div class='badge'>C# ASP.NET Core API Đang Hoạt Động (Cổng 5000)</div>
        <h1>AI-Native Commerce API</h1>
        <p>Bạn vừa truy cập thành công vào máy chủ <strong>Backend REST API</strong> của đề tài <strong>NET108 - Dự án .NET 1 (FPT Polytechnic)</strong>.</p>
        <p style='color: #cbd5e1;'>Để xem <strong>Giao diện Web Mua sắm (React Kanban & AI Assistant)</strong>, hãy mở Cổng 3000:</p>
        <a class='btn' href='http://localhost:3000' target='_blank'>
            👉 Mở Giao diện Web Mua sắm (localhost:3000)
        </a>
        <div class='endpoints'>
            <h4>Danh sách API Endpoints kiểm thử:</h4>
            <ul>
                <li><span><span class='method'>GET</span><span class='path'>/health</span></span><span class='desc'>Kiểm tra máy chủ</span></li>
                <li><span><span class='method'>GET</span><span class='path'>/api/v1/catalog/products</span></span><span class='desc'>Danh mục sản phẩm 3NF</span></li>
                <li><span><span class='method post'>POST</span><span class='path'>/api/v1/cart/quote</span></span><span class='desc'>Khóa Báo Giá 15 Phút</span></li>
                <li><span><span class='method post'>POST</span><span class='path'>/api/v1/checkout</span></span><span class='desc'>Saga Idempotency</span></li>
                <li><span><span class='method post'>POST</span><span class='path'>/api/v1/ai/nlp-search</span></span><span class='desc'>Tìm kiếm AI</span></li>
            </ul>
        </div>
    </div>
</body>
</html>", "text/html"));

app.MapControllers();

Console.WriteLine("=======================================================");
Console.WriteLine("🚀 AI-Native Commerce C# ASP.NET Core Web API is running!");
Console.WriteLine("📡 URL: http://localhost:5000");
Console.WriteLine("🏥 Health Check: http://localhost:5000/health");
Console.WriteLine("=======================================================");

app.Run();
