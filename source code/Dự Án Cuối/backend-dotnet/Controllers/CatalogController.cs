using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;
using AiNativeCommerce.Api.Data;
using AiNativeCommerce.Api.Models;

namespace AiNativeCommerce.Api.Controllers;

[ApiController]
[Route("api/v1/catalog")]
public class CatalogController : ControllerBase
{
    private readonly CommerceDbContext _context;

    public CatalogController(CommerceDbContext context)
    {
        _context = context;
    }

    [HttpGet("categories")]
    public async Task<IActionResult> GetCategories()
    {
        var categories = await _context.Categories.ToListAsync();
        return Ok(categories);
    }

    [HttpGet("products")]
    public async Task<IActionResult> GetProducts(
        [FromQuery] int? categoryId,
        [FromQuery] string? search,
        [FromQuery] int page = 1,
        [FromQuery] int limit = 12)
    {
        var query = _context.Products.Include(p => p.Category).AsQueryable();

        if (categoryId.HasValue)
        {
            query = query.Where(p => p.CategoryId == categoryId.Value);
        }

        if (!string.IsNullOrWhiteSpace(search))
        {
            var s = search.ToLower();
            query = query.Where(p => p.Name.ToLower().Contains(s) || (p.Description != null && p.Description.ToLower().Contains(s)));
        }

        var total = await query.CountAsync();
        var products = await query
            .OrderByDescending(p => p.Id)
            .Skip((page - 1) * limit)
            .Take(limit)
            .ToListAsync();

        var result = products.Select(p => new
        {
            p.Id,
            p.Sku,
            p.Name,
            p.Slug,
            p.Description,
            p.PriceMinor,
            p.StockQty,
            p.CategoryId,
            Category = new { p.Category.Id, p.Category.Name, p.Category.Slug },
            p.ImageUrl,
            p.Status,
            Specs = !string.IsNullOrEmpty(p.SpecsJson) ? JsonSerializer.Deserialize<object>(p.SpecsJson) : null,
            AiTags = !string.IsNullOrEmpty(p.AiTagsJson) ? JsonSerializer.Deserialize<string[]>(p.AiTagsJson) : Array.Empty<string>()
        });

        return Ok(new
        {
            products = result,
            pagination = new
            {
                page,
                limit,
                total,
                totalPages = (int)Math.Ceiling(total / (double)limit)
            }
        });
    }

    [HttpGet("products/{slug}")]
    public async Task<IActionResult> GetProductBySlug(string slug)
    {
        var p = await _context.Products
            .Include(x => x.Category)
            .FirstOrDefaultAsync(x => x.Slug == slug || x.Id.ToString() == slug);

        if (p == null) return NotFound(new { error = "NOT_FOUND", message = "Không tìm thấy sản phẩm" });

        return Ok(new
        {
            p.Id,
            p.Sku,
            p.Name,
            p.Slug,
            p.Description,
            p.PriceMinor,
            p.StockQty,
            p.CategoryId,
            Category = new { p.Category.Id, p.Category.Name, p.Category.Slug },
            p.ImageUrl,
            p.Status,
            Specs = !string.IsNullOrEmpty(p.SpecsJson) ? JsonSerializer.Deserialize<object>(p.SpecsJson) : null,
            AiTags = !string.IsNullOrEmpty(p.AiTagsJson) ? JsonSerializer.Deserialize<string[]>(p.AiTagsJson) : Array.Empty<string>()
        });
    }
}
