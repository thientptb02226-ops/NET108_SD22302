-- ==============================================================================
-- AI-NATIVE COMMERCE - INITIAL SEED DATA
-- ==============================================================================

-- 1. Roles
INSERT INTO roles (id, name, description) VALUES
(1, 'SuperAdmin', 'Quản trị viên toàn hệ thống, cấu hình chính sách AI & bảo mật'),
(2, 'Merchant', 'Nhà bán hàng & nhân viên quản lý kho, sản phẩm và đơn hàng'),
(3, 'Customer', 'Khách hàng mua sắm, tương tác AI Shopping Assistant')
ON CONFLICT (id) DO NOTHING;

-- 2. Users (Password: Admin@123 / Customer@123 hashed with Bcrypt)
-- Hash for 'Admin@123': $2a$10$wT0o3q6/Q5LlhQvSgJjFhOCz36F1rXg6iMwqh8Y4O.K6b4F9LzH6e
INSERT INTO users (id, role_id, email, password_hash, full_name, phone, status) VALUES
(1, 1, 'admin@ainative.vn', '$2a$10$wT0o3q6/Q5LlhQvSgJjFhOCz36F1rXg6iMwqh8Y4O.K6b4F9LzH6e', 'Nguyễn Quản Trị', '0901234567', 'ACTIVE'),
(2, 2, 'merchant@ainative.vn', '$2a$10$wT0o3q6/Q5LlhQvSgJjFhOCz36F1rXg6iMwqh8Y4O.K6b4F9LzH6e', 'Trần Phúc Thiên (Merchant)', '0912345678', 'ACTIVE'),
(3, 3, 'customer@gmail.com', '$2a$10$wT0o3q6/Q5LlhQvSgJjFhOCz36F1rXg6iMwqh8Y4O.K6b4F9LzH6e', 'Lê Khách Hàng', '0988776655', 'ACTIVE')
ON CONFLICT (id) DO NOTHING;

-- 3. Categories
INSERT INTO categories (id, parent_id, name, slug, icon, active) VALUES
(1, NULL, 'Thiết Bị Điện Tử & Laptop', 'dien-tu-laptop', 'Laptop', true),
(2, NULL, 'Điện Thoại & Phụ Kiện', 'dien-thoai-phu-kien', 'Smartphone', true),
(3, NULL, 'Thời Trang & Đời Sống', 'thoi-trang-doi-song', 'Shirt', true),
(4, NULL, 'Đồ Uống & Cafe Cao Cấp', 'do-uong-cafe', 'Coffee', true)
ON CONFLICT (id) DO NOTHING;

-- 4. Products with AI Tags and Detailed Specs
INSERT INTO products (id, category_id, name, sku, price_minor, original_price_minor, stock_quantity, description, specs, image_url, ai_tags, status) VALUES
(1, 1, 'MacBook Air M3 15 inch (16GB RAM / 512GB SSD)', 'MBA-M3-15-512', 32990000, 35990000, 25, 
'Chiếc laptop siêu mỏng nhẹ hoàn hảo cho sinh viên và dân văn phòng, tích hợp chip Apple M3 Neural Engine hỗ trợ xử lý tác vụ AI cục bộ cực nhanh, thời lượng pin lên đến 18 giờ.',
'{"chip": "Apple M3 8-core", "ram": "16GB Unified", "storage": "512GB SSD", "display": "15.3 inch Liquid Retina", "weight": "1.51 kg"}'::jsonb,
'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800',
'["mong-nhe", "pin-trau", "apple", "m3", "hoc-tap", "van-phong"]'::jsonb, 'ACTIVE'),

(2, 1, 'Laptop Gaming ASUS ROG Zephyrus G16 (RTX 4070 / AI Boost)', 'ROG-G16-4070', 48990000, 52990000, 15,
'Laptop gaming cao cấp màn hình OLED 240Hz, trang bị vi xử lý Intel Core Ultra 9 tích hợp NPU AI chuyên dụng kết hợp card đồ họa RTX 4070.',
'{"cpu": "Intel Core Ultra 9", "gpu": "NVIDIA RTX 4070 8GB", "ram": "32GB LPDDR5X", "storage": "1TB PCIe 4.0", "screen": "16 inch 2.5K OLED 240Hz"}'::jsonb,
'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800',
'["gaming", "do-hoa", "ai-npu", "oled", "hieu-nang-cao"]'::jsonb, 'ACTIVE'),

(3, 2, 'iPhone 16 Pro Max 256GB - Titan Tự Nhiên (Apple Intelligence)', 'IP16PM-256-TI', 34490000, 36990000, 40,
'Siêu phẩm smartphone mới nhất của Apple với khung viền Titan Grade 5 siêu bền nhẹ, trang bị nút Camera Control cảm ứng lực và bộ tính năng Apple Intelligence tự hành.',
'{"screen": "6.9 inch Super Retina XDR ProMotion 120Hz", "chip": "Apple A18 Pro 3nm", "camera": "48MP Fusion + 48MP Ultra Wide + 12MP 5x Telephoto", "battery": "4685 mAh"}'::jsonb,
'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=800',
'["apple", "iphone-16", "camera-khung", "titan", "cao-cap"]'::jsonb, 'ACTIVE'),

(4, 2, 'Tai Nghe Chống Ồn Sony WH-1000XM5 (Adaptive AI Sound)', 'SONY-WH1000XM5', 6990000, 8490000, 50,
'Tai nghe chụp tai chống ồn chủ động số 1 thế giới với bộ xử lý chống ồn tích hợp V1 và HD QN1, tự động tối ưu hóa âm thanh theo môi trường xung quanh bằng AI.',
'{"battery": "30 giờ liên tục", "noise_cancelling": "Dual Noise Sensor AI", "bluetooth": "5.2 LDAC Hi-Res Audio", "weight": "250g"}'::jsonb,
'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800',
'["tai-nghe", "chong-on", "sony", "am-thanh-hay", "lam-viec"]'::jsonb, 'ACTIVE'),

(5, 3, 'Bàn Phím Cơ Không Dây Custom NuPhy Air75 V2 (Low-Profile)', 'NUPHY-AIR75-V2', 2890000, 3290000, 30,
'Bàn phím cơ siêu mỏng 75% gõ cực êm, hỗ trợ 3 chế độ kết nối (Bluetooth 5.1, 2.4GHz Receiver, Type-C) tương thích tuyệt đối cho cả macOS và Windows.',
'{"layout": "75% 84 phím", "switch": "Cowberry Linear Pre-lubed", "keycaps": "PBT Dye-sub", "battery": "4000 mAh"}'::jsonb,
'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800',
'["ban-phim-co", "low-profile", "nuphy", "setup-dep", "lap-trinh"]'::jsonb, 'ACTIVE'),

(6, 4, 'Cà Phê Arabica Cầu Đất Thượng Hạng (Hương Vị AI Tuyển Chọn)', 'CAFE-ARABICA-500G', 185000, 220000, 100,
'Hạt cà phê Arabica 100% trồng tại vùng Cầu Đất - Đà Lạt ở độ cao 1650m, được rang mộc tỉ mỉ với công thức tối ưu hóa nhiệt độ bằng AI cho hương vị trái cây thơm dịu.',
'{"origin": "Cầu Đất, Đà Lạt", "roast_level": "Medium Roast", "flavor_notes": "Caramel, Chocolate, Cam Bergamot", "weight": "500g hạt nguyên chất"}'::jsonb,
'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800',
'["cafe", "ca-phe-moc", "arabica", "cau-dat", "do-uong"]'::jsonb, 'ACTIVE')
ON CONFLICT (id) DO NOTHING;

-- Reset Sequences
SELECT setval('roles_id_seq', (SELECT MAX(id) FROM roles));
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories));
SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));
