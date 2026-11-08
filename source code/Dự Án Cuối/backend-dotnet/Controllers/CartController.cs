using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using AiNativeCommerce.Api.Data;
using AiNativeCommerce.Api.DTOs;
using AiNativeCommerce.Api.Models;

namespace AiNativeCommerce.Api.Controllers;

[ApiController]
[Route("api/v1/cart")]
public class CartController : ControllerBase
{
    private readonly CommerceDbContext _context;

    public CartController(CommerceDbContext context)
    {
        _context = context;
    }

    private async Task<Cart> GetOrCreateUserCartAsync(int userId = 3)
    {
        var cart = await _context.Carts
            .Include(c => c.Items)
            .ThenInclude(i => i.Product)
            .ThenInclude(p => p.Category)
            .FirstOrDefaultAsync(c => c.UserId == userId);

        if (cart == null)
        {
            cart = new Cart { UserId = userId };
            _context.Carts.Add(cart);
            await _context.SaveChangesAsync();
        }

        return cart;
    }

    [HttpGet]
    public async Task<IActionResult> GetCart()
    {
        var cart = await GetOrCreateUserCartAsync();
        var subtotal = cart.Items.Sum(i => i.Quantity * i.UnitPriceMinor);

        return Ok(new
        {
            id = cart.Id,
            userId = cart.UserId,
            subtotalMinor = subtotal,
            items = cart.Items.Select(i => new
            {
                i.Id,
                i.ProductId,
                i.Quantity,
                i.UnitPriceMinor,
                product = new
                {
                    i.Product.Id,
                    i.Product.Name,
                    i.Product.Slug,
                    i.Product.PriceMinor,
                    i.Product.ImageUrl,
                    Category = new { i.Product.Category.Id, i.Product.Category.Name }
                }
            })
        });
    }

    [HttpPost("items")]
    public async Task<IActionResult> AddItem([FromBody] AddCartItemRequest req)
    {
        var cart = await GetOrCreateUserCartAsync();
        var product = await _context.Products.FindAsync(req.ProductId);

        if (product == null || product.Status != "ACTIVE")
        {
            return BadRequest(new { error = "PRODUCT_NOT_AVAILABLE", message = "Sản phẩm không tồn tại hoặc đã ngừng kinh doanh" });
        }

        var existingItem = cart.Items.FirstOrDefault(i => i.ProductId == req.ProductId);
        if (existingItem != null)
        {
            existingItem.Quantity += req.Quantity > 0 ? req.Quantity : 1;
        }
        else
        {
            var newItem = new CartItem
            {
                CartId = cart.Id,
                ProductId = req.ProductId,
                Quantity = req.Quantity > 0 ? req.Quantity : 1,
                UnitPriceMinor = product.PriceMinor
            };
            _context.CartItems.Add(newItem);
        }

        await _context.SaveChangesAsync();
        return await GetCart();
    }

    [HttpPut("items/{id}")]
    public async Task<IActionResult> UpdateItem(int id, [FromBody] UpdateCartItemRequest req)
    {
        var item = await _context.CartItems.FindAsync(id);
        if (item == null) return NotFound(new { error = "NOT_FOUND", message = "Không tìm thấy sản phẩm trong giỏ" });

        if (req.Quantity <= 0)
        {
            _context.CartItems.Remove(item);
        }
        else
        {
            item.Quantity = req.Quantity;
        }

        await _context.SaveChangesAsync();
        return await GetCart();
    }

    [HttpDelete("items/{id}")]
    public async Task<IActionResult> RemoveItem(int id)
    {
        var item = await _context.CartItems.FindAsync(id);
        if (item != null)
        {
            _context.CartItems.Remove(item);
            await _context.SaveChangesAsync();
        }

        var cart = await GetCart();
        return Ok(new { message = "Đã xóa sản phẩm khỏi giỏ", cart = (cart as OkObjectResult)?.Value });
    }

    [HttpPost("quote")]
    public async Task<IActionResult> CreateQuote()
    {
        var cart = await GetOrCreateUserCartAsync();
        if (!cart.Items.Any())
        {
            return BadRequest(new { error = "EMPTY_CART", message = "Giỏ hàng đang trống, không thể tạo báo giá" });
        }

        var subtotal = cart.Items.Sum(i => i.Quantity * i.UnitPriceMinor);
        var discount = subtotal >= 30000000 ? 500000L : 0L; // 500k AI coupon discount
        var shipping = subtotal >= 2000000 ? 0L : 30000L;
        var tax = (long)Math.Round((subtotal - discount) * 0.10);
        var total = subtotal - discount + shipping + tax;

        // Generate SHA-256 cryptographic quote fingerprint
        var rawString = $"{cart.Id}:{subtotal}:{discount}:{shipping}:{tax}:{total}:{DateTime.UtcNow:yyyyMMddHHmm}";
        using var sha256 = SHA256.Create();
        var hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(rawString));
        var fingerprint = "fp_sha256_" + Convert.ToHexString(hashBytes).ToLower();

        var itemsList = cart.Items.Select(i => new
        {
            productId = i.ProductId,
            name = i.Product.Name,
            quantity = i.Quantity,
            priceMinor = i.UnitPriceMinor,
            lineTotalMinor = i.Quantity * i.UnitPriceMinor
        }).ToList();

        var quote = new CommerceQuote
        {
            CartId = cart.Id,
            UserId = cart.UserId,
            SubtotalMinor = subtotal,
            DiscountMinor = discount,
            ShippingMinor = shipping,
            TaxMinor = tax,
            TotalMinor = total,
            Fingerprint = fingerprint,
            ExpiresAt = DateTime.UtcNow.AddMinutes(15),
            ItemsJson = JsonSerializer.Serialize(itemsList)
        };

        _context.CommerceQuotes.Add(quote);
        await _context.SaveChangesAsync();

        return Ok(new
        {
            quote = new
            {
                id = quote.Id,
                cartId = quote.CartId,
                subtotalMinor = quote.SubtotalMinor,
                discountMinor = quote.DiscountMinor,
                shippingMinor = quote.ShippingMinor,
                taxMinor = quote.TaxMinor,
                totalMinor = quote.TotalMinor,
                currency = quote.Currency,
                fingerprint = quote.Fingerprint,
                expiresAt = quote.ExpiresAt,
                items = itemsList
            },
            message = "Báo giá đóng băng (Quote Lock) 15 phút đã được khởi tạo thành công!"
        });
    }
}
