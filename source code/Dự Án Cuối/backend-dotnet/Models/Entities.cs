using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace AiNativeCommerce.Api.Models;

public class Role
{
    [Key]
    public int Id { get; set; }
    [Required]
    [MaxLength(50)]
    public string Name { get; set; } = string.Empty; // ADMIN, MERCHANT, CUSTOMER
    public string? Description { get; set; }
}

public class User
{
    [Key]
    public int Id { get; set; }
    [Required]
    [MaxLength(100)]
    public string Email { get; set; } = string.Empty;
    [Required]
    public string PasswordHash { get; set; } = string.Empty;
    [Required]
    [MaxLength(100)]
    public string FullName { get; set; } = string.Empty;
    [MaxLength(20)]
    public string? Phone { get; set; }
    public int RoleId { get; set; }
    [ForeignKey("RoleId")]
    public Role Role { get; set; } = null!;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}

public class Category
{
    [Key]
    public int Id { get; set; }
    [Required]
    [MaxLength(100)]
    public string Name { get; set; } = string.Empty;
    [Required]
    [MaxLength(100)]
    public string Slug { get; set; } = string.Empty;
    public string? Icon { get; set; }
    public string? Description { get; set; }
    public ICollection<Product> Products { get; set; } = new List<Product>();
}

public class Product
{
    [Key]
    public int Id { get; set; }
    [Required]
    [MaxLength(50)]
    public string Sku { get; set; } = string.Empty;
    [Required]
    [MaxLength(255)]
    public string Name { get; set; } = string.Empty;
    [Required]
    [MaxLength(255)]
    public string Slug { get; set; } = string.Empty;
    public string? Description { get; set; }
    public long PriceMinor { get; set; } // VND minor
    public int StockQty { get; set; }
    public int CategoryId { get; set; }
    [ForeignKey("CategoryId")]
    public Category Category { get; set; } = null!;
    public string? ImageUrl { get; set; }
    public string? SpecsJson { get; set; }
    public string? AiTagsJson { get; set; }
    [MaxLength(20)]
    public string Status { get; set; } = "ACTIVE";
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}

public class Cart
{
    [Key]
    public int Id { get; set; }
    public int UserId { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    public ICollection<CartItem> Items { get; set; } = new List<CartItem>();
}

public class CartItem
{
    [Key]
    public int Id { get; set; }
    public int CartId { get; set; }
    [ForeignKey("CartId")]
    public Cart Cart { get; set; } = null!;
    public int ProductId { get; set; }
    [ForeignKey("ProductId")]
    public Product Product { get; set; } = null!;
    public int Quantity { get; set; } = 1;
    public long UnitPriceMinor { get; set; }
}

public class CommerceQuote
{
    [Key]
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public int CartId { get; set; }
    public int UserId { get; set; }
    public long SubtotalMinor { get; set; }
    public long DiscountMinor { get; set; } = 0;
    public long ShippingMinor { get; set; } = 0;
    public long TaxMinor { get; set; } = 0;
    public long TotalMinor { get; set; }
    public string Currency { get; set; } = "VND";
    [Required]
    [MaxLength(128)]
    public string Fingerprint { get; set; } = string.Empty;
    public DateTime ExpiresAt { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public string ItemsJson { get; set; } = "[]";
}

public class CommerceIdempotency
{
    [Key]
    public string Id { get; set; } = Guid.NewGuid().ToString();
    [Required]
    [MaxLength(160)]
    public string RequestKey { get; set; } = string.Empty;
    [Required]
    [MaxLength(64)]
    public string RequestHash { get; set; } = string.Empty;
    [Required]
    [MaxLength(96)]
    public string Operation { get; set; } = string.Empty;
    public int HttpStatus { get; set; }
    public string? ResponseJson { get; set; }
    [MaxLength(20)]
    public string Status { get; set; } = "COMMITTED"; // PROCESSING, COMMITTED, FAILED
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime ExpiresAt { get; set; }
}

public class Order
{
    [Key]
    public int Id { get; set; }
    [Required]
    [MaxLength(60)]
    public string OrderNumber { get; set; } = string.Empty;
    public int UserId { get; set; }
    [ForeignKey("UserId")]
    public User User { get; set; } = null!;
    [MaxLength(30)]
    public string Status { get; set; } = "PENDING_PAYMENT";
    public long TotalMinor { get; set; }
    public string Currency { get; set; } = "VND";
    public string ShippingAddress { get; set; } = string.Empty;
    public string ShippingPhone { get; set; } = string.Empty;
    public string RecipientName { get; set; } = string.Empty;
    public string PaymentMethod { get; set; } = "VIETQR";
    public string PaymentStatus { get; set; } = "PENDING";
    public string? QuoteFingerprint { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public ICollection<OrderItem> Items { get; set; } = new List<OrderItem>();
}

public class OrderItem
{
    [Key]
    public int Id { get; set; }
    public int OrderId { get; set; }
    [ForeignKey("OrderId")]
    public Order Order { get; set; } = null!;
    public int ProductId { get; set; }
    [ForeignKey("ProductId")]
    public Product Product { get; set; } = null!;
    public int Quantity { get; set; }
    public long UnitPriceMinor { get; set; }
    public long SubtotalMinor { get; set; }
}

public class AiActionApproval
{
    [Key]
    public int Id { get; set; }
    public int UserId { get; set; }
    [Required]
    [MaxLength(50)]
    public string ActionType { get; set; } = string.Empty; // ADD_TO_CART, APPLY_VOUCHER
    public string Description { get; set; } = string.Empty;
    public string PayloadJson { get; set; } = "{}";
    [MaxLength(20)]
    public string Status { get; set; } = "PENDING"; // PENDING, APPROVED, REJECTED
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
