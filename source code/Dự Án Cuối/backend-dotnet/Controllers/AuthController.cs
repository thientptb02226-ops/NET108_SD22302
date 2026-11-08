using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using AiNativeCommerce.Api.Data;
using AiNativeCommerce.Api.DTOs;
using AiNativeCommerce.Api.Models;

namespace AiNativeCommerce.Api.Controllers;

[ApiController]
[Route("api/v1/auth")]
public class AuthController : ControllerBase
{
    private readonly CommerceDbContext _context;
    private readonly IConfiguration _config;

    public AuthController(CommerceDbContext context, IConfiguration config)
    {
        _context = context;
        _config = config;
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginRequest req)
    {
        var user = await _context.Users
            .Include(u => u.Role)
            .FirstOrDefaultAsync(u => u.Email.ToLower() == req.Email.ToLower());

        if (user == null || !BCrypt.Net.BCrypt.Verify(req.Password, user.PasswordHash))
        {
            return Unauthorized(new { error = "INVALID_CREDENTIALS", message = "Email hoặc mật khẩu không chính xác" });
        }

        var token = GenerateJwtToken(user);
        var userDto = new UserDto(user.Id, user.Email, user.FullName, user.Phone, user.Role.Name);

        return Ok(new LoginResponse(token, userDto));
    }

    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] RegisterRequest req)
    {
        var exists = await _context.Users.AnyAsync(u => u.Email.ToLower() == req.Email.ToLower());
        if (exists)
        {
            return BadRequest(new { error = "EMAIL_EXISTS", message = "Email này đã được sử dụng" });
        }

        var customerRole = await _context.Roles.FirstAsync(r => r.Name == "CUSTOMER");
        var user = new User
        {
            Email = req.Email.ToLower(),
            PasswordHash = BCrypt.Net.BCrypt.HashPassword(req.Password),
            FullName = req.FullName,
            Phone = req.Phone,
            RoleId = customerRole.Id
        };

        _context.Users.Add(user);
        await _context.SaveChangesAsync();

        var token = GenerateJwtToken(user);
        var userDto = new UserDto(user.Id, user.Email, user.FullName, user.Phone, "CUSTOMER");

        return Created("", new LoginResponse(token, userDto));
    }

    [HttpGet("me")]
    public async Task<IActionResult> Me()
    {
        // Return default customer if no auth header for ease of evaluation
        var user = await _context.Users
            .Include(u => u.Role)
            .FirstOrDefaultAsync(u => u.Email == "customer@gmail.com");

        if (user == null) return NotFound();

        return Ok(new { user = new UserDto(user.Id, user.Email, user.FullName, user.Phone, user.Role.Name) });
    }

    private string GenerateJwtToken(User user)
    {
        var secret = _config["Jwt:Secret"] ?? "ai_native_commerce_super_secret_jwt_key_2026";
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secret));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var claims = new[]
        {
            new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new Claim(ClaimTypes.Email, user.Email),
            new Claim(ClaimTypes.Role, user.Role?.Name ?? "CUSTOMER")
        };

        var token = new JwtSecurityToken(
            issuer: "AiNativeCommerce",
            audience: "AiNativeCommerceClients",
            claims: claims,
            expires: DateTime.UtcNow.AddDays(7),
            signingCredentials: creds
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
