using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;
using AiNativeCommerce.Api.Data;
using AiNativeCommerce.Api.DTOs;
using AiNativeCommerce.Api.Models;

namespace AiNativeCommerce.Api.Controllers;

[ApiController]
[Route("api/v1/checkout")]
public class CheckoutController : ControllerBase
{
    private readonly CommerceDbContext _context;

    public CheckoutController(CommerceDbContext context)
    {
        _context = context;
    }

    [HttpPost]
    public async Task<IActionResult> ProcessCheckout([FromBody] CheckoutRequest req)
    {
        // 1. Check Idempotency Key
        var idempotencyKey = Request.Headers["Idempotency-Key"].ToString();
        if (string.IsNullOrEmpty(idempotencyKey))
        {
            idempotencyKey = $"idem-auto-{Guid.NewGuid():N}";
        }

        var existingIdempotency = await _context.CommerceIdempotencies
            .FirstOrDefaultAsync(i => i.RequestKey == idempotencyKey);

        if (existingIdempotency != null && existingIdempotency.Status == "COMMITTED")
        {
            Response.Headers.Append("X-Idempotent-Replay", "true");
            var cached = JsonSerializer.Deserialize<object>(existingIdempotency.ResponseJson ?? "{}");
            return StatusCode(existingIdempotency.HttpStatus, cached);
        }

        // 2. Validate Quote
        var quote = await _context.CommerceQuotes.FindAsync(req.QuoteId);
        if (quote == null)
        {
            return BadRequest(new { error = "INVALID_QUOTE", message = "Báo giá không tồn tại hoặc không hợp lệ" });
        }

        if (quote.ExpiresAt < DateTime.UtcNow)
        {
            return BadRequest(new { error = "QUOTE_EXPIRED", message = "Báo giá 15 phút đã hết hạn. Vui lòng tạo báo giá mới." });
        }

        // 3. Create Order
        var orderNumber = $"ORD-{DateTime.UtcNow:yyyyMM}-{Random.Shared.Next(1000, 9999)}";
        var isVietQr = req.PaymentMethod.ToUpper() == "VIETQR";

        var order = new Order
        {
            OrderNumber = orderNumber,
            UserId = quote.UserId,
            Status = isVietQr ? "CONFIRMED" : "PENDING_PAYMENT",
            TotalMinor = quote.TotalMinor,
            Currency = quote.Currency,
            ShippingAddress = req.ShippingAddress,
            ShippingPhone = req.ShippingPhone,
            RecipientName = req.RecipientName,
            PaymentMethod = req.PaymentMethod.ToUpper(),
            PaymentStatus = isVietQr ? "PAID" : "PENDING",
            QuoteFingerprint = quote.Fingerprint
        };

        _context.Orders.Add(order);
        await _context.SaveChangesAsync();

        // 4. Attach Order Items from Quote
        var quoteItems = JsonSerializer.Deserialize<List<JsonElement>>(quote.ItemsJson) ?? new();
        foreach (var item in quoteItems)
        {
            var pId = item.GetProperty("productId").GetInt32();
            var qty = item.GetProperty("quantity").GetInt32();
            var price = item.GetProperty("priceMinor").GetInt64();

            _context.OrderItems.Add(new OrderItem
            {
                OrderId = order.Id,
                ProductId = pId,
                Quantity = qty,
                UnitPriceMinor = price,
                SubtotalMinor = qty * price
            });

            // Decrement Stock
            var product = await _context.Products.FindAsync(pId);
            if (product != null)
            {
                product.StockQty = Math.Max(0, product.StockQty - qty);
            }
        }

        // 5. Clear User Cart
        var cart = await _context.Carts
            .Include(c => c.Items)
            .FirstOrDefaultAsync(c => c.Id == quote.CartId);

        if (cart != null)
        {
            _context.CartItems.RemoveRange(cart.Items);
        }

        // 6. Record Idempotency Commit
        var responsePayload = new
        {
            order = new
            {
                id = order.Id,
                orderNumber = order.OrderNumber,
                status = order.Status,
                totalMinor = order.TotalMinor,
                currency = order.Currency,
                shippingAddress = order.ShippingAddress,
                shippingPhone = order.ShippingPhone,
                recipientName = order.RecipientName,
                paymentMethod = order.PaymentMethod,
                paymentStatus = order.PaymentStatus,
                createdAt = order.CreatedAt
            },
            payment = new
            {
                paymentMethod = order.PaymentMethod,
                paymentStatus = order.PaymentStatus,
                qrCodeUrl = isVietQr
                    ? $"https://img.vietqr.io/image/970422-0987654321-compact2.png?amount={order.TotalMinor}&addInfo=AINATIVE_{order.OrderNumber}&accountName=AI%20NATIVE%20COMMERCE"
                    : null
            },
            message = "Saga Checkout hoàn tất thành công! Đơn hàng đã được xác nhận an toàn."
        };

        var idemRecord = new CommerceIdempotency
        {
            RequestKey = idempotencyKey,
            RequestHash = Convert.ToHexString(System.Security.Cryptography.SHA256.HashData(System.Text.Encoding.UTF8.GetBytes(req.QuoteId))),
            Operation = "CHECKOUT_SAGA",
            HttpStatus = 201,
            ResponseJson = JsonSerializer.Serialize(responsePayload),
            Status = "COMMITTED",
            ExpiresAt = DateTime.UtcNow.AddDays(7)
        };

        _context.CommerceIdempotencies.Add(idemRecord);
        await _context.SaveChangesAsync();

        return Created($"/api/v1/orders/{order.Id}", responsePayload);
    }
}
