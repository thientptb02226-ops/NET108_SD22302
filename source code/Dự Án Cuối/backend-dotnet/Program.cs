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

// 8. Health Check
app.MapGet("/health", () => Results.Ok(new
{
    status = "healthy",
    service = "AI-Native Commerce ASP.NET Core Web API (C# .NET 10/8)",
    timestamp = DateTime.UtcNow,
    architecture = "Enterprise Saga with 15-Min Quote Lock & Idempotency"
}));

app.MapControllers();

Console.WriteLine("=======================================================");
Console.WriteLine("🚀 AI-Native Commerce C# ASP.NET Core Web API is running!");
Console.WriteLine("📡 URL: http://localhost:5000");
Console.WriteLine("🏥 Health Check: http://localhost:5000/health");
Console.WriteLine("=======================================================");

app.Run();
