using Microsoft.EntityFrameworkCore;
using AiNativeCommerce.Api.Models;

namespace AiNativeCommerce.Api.Data;

public class CommerceDbContext : DbContext
{
    public CommerceDbContext(DbContextOptions<CommerceDbContext> options) : base(options)
    {
    }

    public DbSet<Role> Roles => Set<Role>();
    public DbSet<User> Users => Set<User>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Cart> Carts => Set<Cart>();
    public DbSet<CartItem> CartItems => Set<CartItem>();
    public DbSet<CommerceQuote> CommerceQuotes => Set<CommerceQuote>();
    public DbSet<CommerceIdempotency> CommerceIdempotencies => Set<CommerceIdempotency>();
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();
    public DbSet<AiActionApproval> AiActionApprovals => Set<AiActionApproval>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<User>()
            .HasIndex(u => u.Email)
            .IsUnique();

        modelBuilder.Entity<CommerceIdempotency>()
            .HasIndex(i => i.RequestKey)
            .IsUnique();
    }
}
