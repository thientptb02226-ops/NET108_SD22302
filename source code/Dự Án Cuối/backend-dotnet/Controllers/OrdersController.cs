using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using AiNativeCommerce.Api.Data;
using AiNativeCommerce.Api.Models;

namespace AiNativeCommerce.Api.Controllers;

[ApiController]
[Route("api/v1/orders")]
public class OrdersController : ControllerBase
{
    private readonly CommerceDbContext _context;

    public OrdersController(CommerceDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<IActionResult> GetOrders()
    {
        var orders = await _context.Orders
            .Include(o => o.Items)
            .ThenInclude(i => i.Product)
            .OrderByDescending(o => o.Id)
            .ToListAsync();

        return Ok(orders.Select(o => new
        {
            o.Id,
            o.OrderNumber,
            o.Status,
            o.TotalMinor,
            o.Currency,
            o.ShippingAddress,
            o.ShippingPhone,
            o.RecipientName,
            o.PaymentMethod,
            o.PaymentStatus,
            o.CreatedAt,
            items = o.Items.Select(i => new
            {
                i.Id,
                i.ProductId,
                i.Quantity,
                i.UnitPriceMinor,
                i.SubtotalMinor,
                product = new
                {
                    i.Product.Id,
                    i.Product.Name,
                    i.Product.ImageUrl
                }
            })
        }));
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetOrderById(int id)
    {
        var o = await _context.Orders
            .Include(x => x.Items)
            .ThenInclude(i => i.Product)
            .FirstOrDefaultAsync(x => x.Id == id);

        if (o == null) return NotFound(new { error = "NOT_FOUND", message = "Không tìm thấy đơn hàng" });

        return Ok(new
        {
            o.Id,
            o.OrderNumber,
            o.Status,
            o.TotalMinor,
            o.Currency,
            o.ShippingAddress,
            o.ShippingPhone,
            o.RecipientName,
            o.PaymentMethod,
            o.PaymentStatus,
            o.CreatedAt,
            items = o.Items.Select(i => new
            {
                i.Id,
                i.ProductId,
                i.Quantity,
                i.UnitPriceMinor,
                i.SubtotalMinor,
                product = new
                {
                    i.Product.Id,
                    i.Product.Name,
                    i.Product.ImageUrl
                }
            })
        });
    }

    [HttpPost("{id}/cancel")]
    public async Task<IActionResult> CancelOrder(int id)
    {
        var o = await _context.Orders
            .Include(x => x.Items)
            .FirstOrDefaultAsync(x => x.Id == id);

        if (o == null) return NotFound(new { error = "NOT_FOUND", message = "Không tìm thấy đơn hàng" });

        if (o.Status is "SHIPPED" or "COMPLETED")
        {
            return BadRequest(new { error = "CANNOT_CANCEL", message = "Đơn hàng đã được giao hoặc hoàn thành, không thể hủy" });
        }

        o.Status = "CANCELLED";

        // Restore stock
        foreach (var item in o.Items)
        {
            var p = await _context.Products.FindAsync(item.ProductId);
            if (p != null) p.StockQty += item.Quantity;
        }

        await _context.SaveChangesAsync();
        return Ok(new { message = "Đã hủy đơn hàng thành công và hoàn trả tồn kho", order = o });
    }
}
