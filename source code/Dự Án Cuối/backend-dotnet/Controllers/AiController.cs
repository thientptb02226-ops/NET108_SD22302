using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;
using System.Text.RegularExpressions;
using AiNativeCommerce.Api.Data;
using AiNativeCommerce.Api.DTOs;
using AiNativeCommerce.Api.Models;

namespace AiNativeCommerce.Api.Controllers;

[ApiController]
[Route("api/v1/ai")]
public class AiController : ControllerBase
{
    private readonly CommerceDbContext _context;

    public AiController(CommerceDbContext context)
    {
        _context = context;
    }

    [HttpPost("nlp-search")]
    public async Task<IActionResult> NlpSearch([FromBody] NlpSearchRequest req)
    {
        if (string.IsNullOrWhiteSpace(req.Query))
        {
            return BadRequest(new { error = "INVALID_QUERY", message = "Vui lòng nhập câu hỏi hoặc yêu cầu tìm kiếm" });
        }

        var q = req.Query.ToLower();

        // 1. Detect Price Constraints
        long? maxPrice = null;
        if (q.Contains("dưới 35 triệu") || q.Contains("duoi 35tr") || q.Contains("< 35tr"))
        {
            maxPrice = 35000000;
        }
        else if (q.Contains("dưới 10 triệu") || q.Contains("duoi 10tr"))
        {
            maxPrice = 10000000;
        }
        else if (q.Contains("dưới 50 triệu"))
        {
            maxPrice = 50000000;
        }

        // 2. Fetch all active products
        var products = await _context.Products
            .Include(p => p.Category)
            .Where(p => p.Status == "ACTIVE")
            .ToListAsync();

        var tokens = Regex.Split(q, @"\W+").Where(t => t.Length > 1).ToList();

        var scored = products.Select(p =>
        {
            var score = 0;
            var corpus = $"{p.Name} {p.Description} {p.AiTagsJson} {p.Category.Name}".ToLower();

            foreach (var t in tokens)
            {
                if (corpus.Contains(t)) score += 3;
            }

            if (q.Contains("mỏng nhẹ") && corpus.Contains("mong-nhe")) score += 5;
            if (q.Contains("pin trâu") && corpus.Contains("pin-trau")) score += 5;
            if (q.Contains("tai nghe") && p.CategoryId == 2) score += 6;
            if (q.Contains("cà phê") && p.CategoryId == 4) score += 6;

            if (maxPrice.HasValue && p.PriceMinor > maxPrice.Value)
            {
                score -= 10;
            }

            return new
            {
                product = p,
                score
            };
        })
        .Where(x => x.score > 0)
        .OrderByDescending(x => x.score)
        .Take(6)
        .ToList();

        return Ok(new
        {
            query = req.Query,
            detectedIntent = new
            {
                maxPriceMinor = maxPrice,
                keywords = tokens,
                category = scored.Any() ? scored.First().product.Category.Name : "Tất cả"
            },
            matchCount = scored.Count,
            results = scored.Select(s => new
            {
                s.product.Id,
                s.product.Sku,
                s.product.Name,
                s.product.Slug,
                s.product.Description,
                s.product.PriceMinor,
                s.product.StockQty,
                s.product.CategoryId,
                Category = new { s.product.Category.Id, s.product.Category.Name },
                s.product.ImageUrl,
                Specs = !string.IsNullOrEmpty(s.product.SpecsJson) ? JsonSerializer.Deserialize<object>(s.product.SpecsJson) : null,
                AiTags = !string.IsNullOrEmpty(s.product.AiTagsJson) ? JsonSerializer.Deserialize<string[]>(s.product.AiTagsJson) : Array.Empty<string>(),
                matchScore = s.score,
                aiExplanation = $"Phù hợp với nhu cầu '{req.Query}' nhờ thông số tối ưu và nhãn AI tương đồng"
            })
        });
    }

    [HttpPost("assistant/chat")]
    public async Task<IActionResult> AssistantChat([FromBody] ChatRequest req)
    {
        var msg = req.Message.Trim().ToLower();
        var sessionId = req.SessionId ?? $"session-{Guid.NewGuid():N}";

        // 1. Order Tracking
        if (msg.Contains("đơn hàng") || msg.Contains("mã đơn") || msg.Contains("tra cứu"))
        {
            return Ok(new
            {
                sessionId,
                reply = "Chào bạn! Tôi có thể hỗ trợ bạn theo dõi đơn hàng ngay lập tức. Đơn hàng gần nhất của bạn (ORD-DEMO-001) đang ở trạng thái 'ĐÃ XÁC NHẬN & ĐANG XỬ LÝ'. Bạn có thể xem lộ trình giao hàng trực tiếp trong phần Đơn hàng.",
                intent = "ORDER_TRACKING",
                suggestedActions = new[] { "Xem chi tiết đơn ORD-DEMO-001", "Chính sách đổi trả trong 7 ngày" }
            });
        }

        // 2. Return Policy
        if (msg.Contains("đổi trả") || msg.Contains("hoàn tiền") || msg.Contains("bảo hành"))
        {
            return Ok(new
            {
                sessionId,
                reply = "Chính sách đổi trả của AI-Native Commerce áp dụng trong 7 ngày kể từ ngày giao hàng. Sản phẩm cần còn nguyên tem và phụ kiện. AI Return Agent sẽ tự động phê duyệt và phát hành mã vận đơn thu hồi nếu đạt điều kiện.",
                intent = "RETURN_POLICY",
                suggestedActions = new[] { "Yêu cầu hoàn trả đơn gần nhất", "Tư vấn sản phẩm khác" }
            });
        }

        // 3. Cart Action Proposal (HITL Level 2)
        if (msg.Contains("thêm") || msg.Contains("mua") || msg.Contains("lấy con") || msg.Contains("chọn"))
        {
            var p = await _context.Products.FirstOrDefaultAsync(x => x.Id == 1) ?? await _context.Products.FirstAsync();

            var approval = new AiActionApproval
            {
                UserId = 3,
                ActionType = "ADD_TO_CART",
                Description = $"Thêm {p.Name} (Số lượng: 1) vào giỏ hàng cá nhân",
                PayloadJson = JsonSerializer.Serialize(new { productId = p.Id, quantity = 1, priceMinor = p.PriceMinor }),
                Status = "PENDING"
            };
            _context.AiActionApprovals.Add(approval);
            await _context.SaveChangesAsync();

            return Ok(new
            {
                sessionId,
                reply = $"Tôi đã tìm thấy sản phẩm **{p.Name}** với giá ưu đãi **{p.PriceMinor:N0} đ**. Bạn có muốn tôi hỗ trợ thêm sản phẩm này vào giỏ hàng không?",
                intent = "CART_ACTION",
                proposedAction = new
                {
                    actionType = "ADD_TO_CART",
                    actionId = approval.Id,
                    description = approval.Description,
                    payload = new { productId = p.Id, quantity = 1 },
                    requiresConfirmation = true
                },
                suggestedActions = new[] { "Đồng ý thêm vào giỏ", "Xem thông số kỹ thuật", "Tìm sản phẩm khác" }
            });
        }

        // 4. Recommendation Fallback
        var recs = await _context.Products.Take(2).ToListAsync();
        return Ok(new
        {
            sessionId,
            reply = "Chào bạn! Tôi là Trợ lý Mua sắm Trí tuệ Nhân tạo (AI-Native Commerce). Tôi có thể hỗ trợ bạn tìm laptop, tai nghe, đồ công nghệ theo nhu cầu ngôn ngữ tự nhiên, đóng băng báo giá 15 phút hoặc tra cứu hành trình đơn hàng.",
            intent = "GENERAL_ASSISTANT",
            suggestedProducts = recs.Select(r => new
            {
                r.Id,
                r.Name,
                r.PriceMinor,
                r.ImageUrl
            }),
            suggestedActions = new[] { "Laptop mỏng nhẹ dưới 35 triệu", "Tai nghe chống ồn cao cấp", "Chính sách đổi trả 7 ngày" }
        });
    }

    [HttpPost("assistant/approve")]
    public async Task<IActionResult> ApproveAction([FromBody] ApproveActionRequest req)
    {
        var approval = await _context.AiActionApprovals.FindAsync(req.ActionId);
        if (approval == null)
        {
            return NotFound(new { error = "NOT_FOUND", message = "Không tìm thấy yêu cầu phê duyệt" });
        }

        approval.Status = req.Approved ? "APPROVED" : "REJECTED";

        if (req.Approved && approval.ActionType == "ADD_TO_CART")
        {
            var payload = JsonSerializer.Deserialize<JsonElement>(approval.PayloadJson);
            var productId = payload.GetProperty("productId").GetInt32();
            var quantity = payload.GetProperty("quantity").GetInt32();

            var cart = await _context.Carts
                .Include(c => c.Items)
                .FirstOrDefaultAsync(c => c.UserId == approval.UserId);

            if (cart != null)
            {
                var existing = cart.Items.FirstOrDefault(i => i.ProductId == productId);
                if (existing != null) existing.Quantity += quantity;
                else cart.Items.Add(new CartItem { ProductId = productId, Quantity = quantity, UnitPriceMinor = 32990000 });
            }
        }

        await _context.SaveChangesAsync();
        return Ok(new
        {
            message = req.Approved ? "Đã phê duyệt và thực hiện hành động thành công!" : "Đã từ chối hành động an toàn.",
            status = approval.Status
        });
    }
}
