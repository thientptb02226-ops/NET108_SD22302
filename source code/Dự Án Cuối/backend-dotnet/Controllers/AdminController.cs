using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using AiNativeCommerce.Api.Data;
using AiNativeCommerce.Api.DTOs;

namespace AiNativeCommerce.Api.Controllers;

[ApiController]
[Route("api/v1/admin")]
public class AdminController : ControllerBase
{
    private readonly CommerceDbContext _context;

    public AdminController(CommerceDbContext context)
    {
        _context = context;
    }

    [HttpGet("dashboard")]
    public async Task<IActionResult> GetDashboard()
    {
        var totalOrders = await _context.Orders.CountAsync();
        var totalRevenue = await _context.Orders
            .Where(o => o.PaymentStatus == "PAID" || o.Status != "CANCELLED")
            .SumAsync(o => o.TotalMinor);

        var totalCustomers = await _context.Users
            .Where(u => u.Role.Name == "CUSTOMER")
            .CountAsync();

        var totalProducts = await _context.Products.CountAsync();

        var recentOrders = await _context.Orders
            .OrderByDescending(o => o.Id)
            .Take(5)
            .ToListAsync();

        return Ok(new
        {
            totalRevenueMinor = totalRevenue,
            totalOrders,
            totalCustomers,
            totalProducts,
            recentOrders = recentOrders.Select(o => new
            {
                o.Id,
                o.OrderNumber,
                o.RecipientName,
                o.TotalMinor,
                o.Status,
                o.PaymentStatus,
                o.PaymentMethod,
                o.CreatedAt
            }),
            revenueByDay = new[]
            {
                new { day = "T2", revenue = 12000000L },
                new { day = "T3", revenue = 15400000L },
                new { day = "T4", revenue = 8500000L },
                new { day = "T5", revenue = 21000000L },
                new { day = "T6", revenue = 32990000L },
                new { day = "T7", revenue = totalRevenue }
            }
        });
    }

    [HttpPut("orders/{id}/status")]
    public async Task<IActionResult> UpdateOrderStatus(int id, [FromBody] UpdateOrderStatusRequest req)
    {
        var order = await _context.Orders.FindAsync(id);
        if (order == null)
        {
            return NotFound(new { error = "NOT_FOUND", message = "Không tìm thấy đơn hàng" });
        }

        order.Status = req.Status.ToUpper();
        if (order.Status is "CONFIRMED" or "COMPLETED")
        {
            order.PaymentStatus = "PAID";
        }

        await _context.SaveChangesAsync();
        return Ok(new { message = $"Đã cập nhật trạng thái đơn sang {order.Status}", order });
    }
}
