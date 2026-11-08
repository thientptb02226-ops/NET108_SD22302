using AiNativeCommerce.Api.Models;
using System.Text.Json;

namespace AiNativeCommerce.Api.Data;

public static class DbInitializer
{
    public static void Initialize(CommerceDbContext context)
    {
        context.Database.EnsureCreated();

        if (context.Roles.Any())
        {
            return; // DB already seeded
        }

        // 1. Seed Roles
        var adminRole = new Role { Name = "ADMIN", Description = "Quản trị viên toàn hệ thống" };
        var merchantRole = new Role { Name = "MERCHANT", Description = "Nhà bán hàng vận hành gian hàng" };
        var customerRole = new Role { Name = "CUSTOMER", Description = "Khách hàng mua sắm" };
        context.Roles.AddRange(adminRole, merchantRole, customerRole);
        context.SaveChanges();

        // 2. Seed Users (Password: Admin@123)
        var passwordHash = BCrypt.Net.BCrypt.HashPassword("Admin@123");
        var adminUser = new User
        {
            Email = "admin@ainative.vn",
            FullName = "Hệ thống Quản Trị Viên (Admin)",
            PasswordHash = passwordHash,
            RoleId = adminRole.Id,
            Phone = "0901234567"
        };
        var merchantUser = new User
        {
            Email = "merchant@ainative.vn",
            FullName = "Đại lý Ủy Quyền Chính Hãng (Merchant)",
            PasswordHash = passwordHash,
            RoleId = merchantRole.Id,
            Phone = "0912345678"
        };
        var customerUser = new User
        {
            Email = "customer@gmail.com",
            FullName = "Nguyễn Văn Khải (Customer)",
            PasswordHash = passwordHash,
            RoleId = customerRole.Id,
            Phone = "0987654321"
        };
        context.Users.AddRange(adminUser, merchantUser, customerUser);
        context.SaveChanges();

        // 3. Seed Categories
        var catLaptop = new Category { Name = "Laptop & Máy tính", Slug = "laptops", Icon = "laptop", Description = "Máy tính xách tay văn phòng, đồ họa, gaming" };
        var catAudio = new Category { Name = "Phụ kiện & Âm thanh", Slug = "accessories-audio", Icon = "headphones", Description = "Tai nghe, bàn phím cơ, chuột công thái học" };
        var catMobile = new Category { Name = "Điện thoại & Tablet", Slug = "phones-tablets", Icon = "smartphone", Description = "Smartphone thế hệ mới và máy tính bảng" };
        var catLife = new Category { Name = "Đời sống & Tiện ích", Slug = "lifestyle", Icon = "coffee", Description = "Cà phê đặc sản, bình giữ nhiệt, đồ gia dụng" };
        context.Categories.AddRange(catLaptop, catAudio, catMobile, catLife);
        context.SaveChanges();

        // 4. Seed Products
        var p1 = new Product
        {
            Sku = "LAP-DELL-XPS13",
            Name = "Laptop Dell XPS 13 Plus 9320 (Core i7 / 16GB / 512GB SSD)",
            Slug = "laptop-dell-xps-13-plus-9320",
            Description = "Laptop doanh nhân siêu mỏng nhẹ, màn hình OLED 3.5K sắc nét, pin 12 tiếng, thiết kế nhôm nguyên khối sang trọng.",
            PriceMinor = 32990000,
            StockQty = 15,
            CategoryId = catLaptop.Id,
            ImageUrl = "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=600&auto=format&fit=crop&q=80",
            AiTagsJson = JsonSerializer.Serialize(new[] { "mong-nhe", "van-phong", "do-hoa", "pin-trau", "cao-cap" }),
            SpecsJson = JsonSerializer.Serialize(new { cpu = "Intel Core i7-1360P", ram = "16GB LPDDR5", storage = "512GB NVMe SSD", display = "13.4 inch 3.5K OLED" }),
            Status = "ACTIVE"
        };
        var p2 = new Product
        {
            Sku = "LAP-MAC-M3-15",
            Name = "MacBook Air M3 15-inch (8-Core GPU / 16GB / 512GB)",
            Slug = "macbook-air-m3-15-inch",
            Description = "Trải nghiệm đỉnh cao với chip Apple M3, pin dùng đến 18 giờ liên tục, màn hình Liquid Retina tuyệt đẹp và thiết kế không quạt êm ái.",
            PriceMinor = 37990000,
            StockQty = 8,
            CategoryId = catLaptop.Id,
            ImageUrl = "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=80",
            AiTagsJson = JsonSerializer.Serialize(new[] { "mong-nhe", "pin-trau", "hoc-tap", "van-phong", "apple" }),
            SpecsJson = JsonSerializer.Serialize(new { chip = "Apple M3 8-Core", ram = "16GB Unified", storage = "512GB SSD", display = "15.3 inch Liquid Retina" }),
            Status = "ACTIVE"
        };
        var p3 = new Product
        {
            Sku = "AUD-SONY-XM5",
            Name = "Tai nghe Sony WH-1000XM5 Chống Ồn Chủ Động Cao Cấp",
            Slug = "tai-nghe-sony-wh-1000xm5",
            Description = "Công nghệ chống ồn chủ động đỉnh cao số 1 thế giới, chất lượng âm thanh Hi-Res không dây, micro AI đàm thoại pha lê.",
            PriceMinor = 7990000,
            StockQty = 25,
            CategoryId = catAudio.Id,
            ImageUrl = "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
            AiTagsJson = JsonSerializer.Serialize(new[] { "chong-on", "pin-trau", "am-thanh-hifi", "du-lich" }),
            SpecsJson = JsonSerializer.Serialize(new { battery = "30 giờ (bật ANC)", driver = "30mm Carbon", noiseCancelling = "Dual Processor V1 + QN1" }),
            Status = "ACTIVE"
        };
        var p4 = new Product
        {
            Sku = "ACC-KEYCHRON-Q1",
            Name = "Bàn phím cơ không dây Keychron Q1 Pro QMK/VIA Hot-swap",
            Slug = "ban-phim-co-keychron-q1-pro",
            Description = "Vỏ nhôm CNC cao cấp, kết nối Bluetooth 5.1 & dây Type-C, núm xoay đa năng tùy biến qua QMK/VIA.",
            PriceMinor = 4290000,
            StockQty = 20,
            CategoryId = catAudio.Id,
            ImageUrl = "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80",
            AiTagsJson = JsonSerializer.Serialize(new[] { "ban-phim-co", "lap-trinh", "gaming", "custom" }),
            SpecsJson = JsonSerializer.Serialize(new { layout = "75%", body = "Nhôm CNC Anodized", switchType = "Keychron K Pro Brown" }),
            Status = "ACTIVE"
        };
        var p5 = new Product
        {
            Sku = "ACC-LOGI-MX3S",
            Name = "Chuột không dây Logitech MX Master 3S Ergonomic",
            Slug = "chuot-khong-day-logitech-mx-master-3s",
            Description = "Cảm biến 8.000 DPI di chuyển trên mọi bề mặt kể cả mặt kính. Con lăn điện từ MagSpeed cuộn 1.000 dòng/giây.",
            PriceMinor = 2490000,
            StockQty = 40,
            CategoryId = catAudio.Id,
            ImageUrl = "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=600&auto=format&fit=crop&q=80",
            AiTagsJson = JsonSerializer.Serialize(new[] { "van-phong", "ergonomic", "pin-trau", "lap-trinh" }),
            SpecsJson = JsonSerializer.Serialize(new { dpi = "8000 DPI", battery = "70 ngày", connection = "Logi Bolt / Bluetooth" }),
            Status = "ACTIVE"
        };
        var p6 = new Product
        {
            Sku = "LIF-COFFEE-ARABICA",
            Name = "Cà phê Arabica Cầu Đất Thượng Hạng (Rang Mộc 500g)",
            Slug = "ca-phe-arabica-cau-dat-thuong-hang",
            Description = "100% hạt cà phê Arabica Cầu Đất Đà Lạt tuyển chọn thủ công, thu hái chín cây ở độ cao 1.600m. Hương vị thanh tao hậu ngọt.",
            PriceMinor = 280000,
            StockQty = 100,
            CategoryId = catLife.Id,
            ImageUrl = "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=600&auto=format&fit=crop&q=80",
            AiTagsJson = JsonSerializer.Serialize(new[] { "cafe", "tinh-tao", "huong-hoa-qua", "thu-cong" }),
            SpecsJson = JsonSerializer.Serialize(new { origin = "Cầu Đất, Đà Lạt", roast = "Medium Light", weight = "500g" }),
            Status = "ACTIVE"
        };
        context.Products.AddRange(p1, p2, p3, p4, p5, p6);
        context.SaveChanges();

        // 5. Seed Demo Cart
        var cart = new Cart { UserId = customerUser.Id };
        context.Carts.Add(cart);
        context.SaveChanges();

        context.CartItems.Add(new CartItem
        {
            CartId = cart.Id,
            ProductId = p1.Id,
            Quantity = 1,
            UnitPriceMinor = p1.PriceMinor
        });

        // 6. Seed Demo Order
        var order = new Order
        {
            OrderNumber = "ORD-DEMO-001",
            UserId = customerUser.Id,
            Status = "CONFIRMED",
            TotalMinor = 32990000,
            ShippingAddress = "Tòa nhà FPT Polytechnic, Phố Trịnh Văn Bô, Nam Từ Liêm, Hà Nội",
            ShippingPhone = "0987654321",
            RecipientName = "Nguyễn Văn Khải",
            PaymentMethod = "VIETQR",
            PaymentStatus = "PAID",
            QuoteFingerprint = "fp_sha256_demo_001"
        };
        context.Orders.Add(order);
        context.SaveChanges();

        context.OrderItems.Add(new OrderItem
        {
            OrderId = order.Id,
            ProductId = p1.Id,
            Quantity = 1,
            UnitPriceMinor = p1.PriceMinor,
            SubtotalMinor = p1.PriceMinor
        });
        context.SaveChanges();
    }
}
