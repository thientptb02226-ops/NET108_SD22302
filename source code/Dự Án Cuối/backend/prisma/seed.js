"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const client_1 = require("@prisma/client");
const bcryptjs_1 = __importDefault(require("bcryptjs"));
const prisma = new client_1.PrismaClient();
async function main() {
    console.log('🌱 Starting database seeding for AI-Native Commerce...');
    // 1. Roles
    const adminRole = await prisma.role.upsert({
        where: { name: 'SuperAdmin' },
        update: {},
        create: {
            name: 'SuperAdmin',
            description: 'Quản trị viên toàn hệ thống, cấu hình chính sách AI & bảo mật'
        }
    });
    const merchantRole = await prisma.role.upsert({
        where: { name: 'Merchant' },
        update: {},
        create: {
            name: 'Merchant',
            description: 'Nhà bán hàng & nhân viên quản lý kho, sản phẩm và đơn hàng'
        }
    });
    const customerRole = await prisma.role.upsert({
        where: { name: 'Customer' },
        update: {},
        create: {
            name: 'Customer',
            description: 'Khách hàng mua sắm, tương tác AI Shopping Assistant'
        }
    });
    console.log('✅ Roles created');
    // 2. Users
    const salt = await bcryptjs_1.default.genSalt(10);
    const hashedPassword = await bcryptjs_1.default.hash('Admin@123', salt);
    const admin = await prisma.user.upsert({
        where: { email: 'admin@ainative.vn' },
        update: {},
        create: {
            email: 'admin@ainative.vn',
            fullName: 'Nguyễn Quản Trị',
            passwordHash: hashedPassword,
            roleId: adminRole.id,
            phone: '0901234567',
            status: 'ACTIVE'
        }
    });
    const merchant = await prisma.user.upsert({
        where: { email: 'merchant@ainative.vn' },
        update: {},
        create: {
            email: 'merchant@ainative.vn',
            fullName: 'Trần Phúc Thiên (Merchant)',
            passwordHash: hashedPassword,
            roleId: merchantRole.id,
            phone: '0912345678',
            status: 'ACTIVE'
        }
    });
    const customer = await prisma.user.upsert({
        where: { email: 'customer@gmail.com' },
        update: {},
        create: {
            email: 'customer@gmail.com',
            fullName: 'Lê Khách Hàng',
            passwordHash: hashedPassword,
            roleId: customerRole.id,
            phone: '0988776655',
            status: 'ACTIVE'
        }
    });
    console.log('✅ Users created (admin@ainative.vn, merchant@ainative.vn, customer@gmail.com / Pass: Admin@123)');
    // 3. Categories
    const catLaptop = await prisma.category.upsert({
        where: { slug: 'dien-tu-laptop' },
        update: {},
        create: {
            name: 'Thiết Bị Điện Tử & Laptop',
            slug: 'dien-tu-laptop',
            icon: 'Laptop',
            active: true
        }
    });
    const catPhone = await prisma.category.upsert({
        where: { slug: 'dien-thoai-phu-kien' },
        update: {},
        create: {
            name: 'Điện Thoại & Phụ Kiện',
            slug: 'dien-thoai-phu-kien',
            icon: 'Smartphone',
            active: true
        }
    });
    const catFashion = await prisma.category.upsert({
        where: { slug: 'thoi-trang-setup' },
        update: {},
        create: {
            name: 'Phụ Kiện Setup & Công Nghệ',
            slug: 'thoi-trang-setup',
            icon: 'Keyboard',
            active: true
        }
    });
    const catCoffee = await prisma.category.upsert({
        where: { slug: 'do-uong-cafe' },
        update: {},
        create: {
            name: 'Đồ Uống & Cà Phê Cao Cấp',
            slug: 'do-uong-cafe',
            icon: 'Coffee',
            active: true
        }
    });
    console.log('✅ Categories created');
    // 4. Products
    const productsData = [
        {
            categoryId: catLaptop.id,
            name: 'MacBook Air M3 15 inch (16GB RAM / 512GB SSD)',
            sku: 'MBA-M3-15-512',
            priceMinor: 32990000,
            originalPriceMinor: 35990000,
            stockQuantity: 25,
            description: 'Chiếc laptop siêu mỏng nhẹ hoàn hảo cho sinh viên và dân văn phòng, tích hợp chip Apple M3 Neural Engine hỗ trợ xử lý tác vụ AI cục bộ cực nhanh, thời lượng pin lên đến 18 giờ.',
            specs: JSON.stringify({ chip: 'Apple M3 8-core', ram: '16GB Unified', storage: '512GB SSD', display: '15.3 inch Liquid Retina', weight: '1.51 kg' }),
            imageUrl: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800',
            aiTags: JSON.stringify(['mong-nhe', 'pin-trau', 'apple', 'm3', 'hoc-tap', 'van-phong'])
        },
        {
            categoryId: catLaptop.id,
            name: 'Laptop Gaming ASUS ROG Zephyrus G16 (RTX 4070 / AI Boost)',
            sku: 'ROG-G16-4070',
            priceMinor: 48990000,
            originalPriceMinor: 52990000,
            stockQuantity: 15,
            description: 'Laptop gaming cao cấp màn hình OLED 240Hz, trang bị vi xử lý Intel Core Ultra 9 tích hợp NPU AI chuyên dụng kết hợp card đồ họa RTX 4070.',
            specs: JSON.stringify({ cpu: 'Intel Core Ultra 9', gpu: 'NVIDIA RTX 4070 8GB', ram: '32GB LPDDR5X', storage: '1TB PCIe 4.0', screen: '16 inch 2.5K OLED 240Hz' }),
            imageUrl: 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800',
            aiTags: JSON.stringify(['gaming', 'do-hoa', 'ai-npu', 'oled', 'hieu-nang-cao'])
        },
        {
            categoryId: catPhone.id,
            name: 'iPhone 16 Pro Max 256GB - Titan Tự Nhiên (Apple Intelligence)',
            sku: 'IP16PM-256-TI',
            priceMinor: 34490000,
            originalPriceMinor: 36990000,
            stockQuantity: 40,
            description: 'Siêu phẩm smartphone mới nhất của Apple với khung viền Titan Grade 5 siêu bền nhẹ, trang bị nút Camera Control cảm ứng lực và bộ tính năng Apple Intelligence tự hành.',
            specs: JSON.stringify({ screen: '6.9 inch Super Retina XDR ProMotion 120Hz', chip: 'Apple A18 Pro 3nm', camera: '48MP Fusion + 48MP Ultra Wide + 12MP 5x Telephoto', battery: '4685 mAh' }),
            imageUrl: 'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=800',
            aiTags: JSON.stringify(['apple', 'iphone-16', 'camera-khung', 'titan', 'cao-cap'])
        },
        {
            categoryId: catPhone.id,
            name: 'Tai Nghe Chống Ồn Sony WH-1000XM5 (Adaptive AI Sound)',
            sku: 'SONY-WH1000XM5',
            priceMinor: 6990000,
            originalPriceMinor: 8490000,
            stockQuantity: 50,
            description: 'Tai nghe chụp tai chống ồn chủ động số 1 thế giới với bộ xử lý chống ồn tích hợp V1 và HD QN1, tự động tối ưu hóa âm thanh theo môi trường xung quanh bằng AI.',
            specs: JSON.stringify({ battery: '30 giờ liên tục', noise_cancelling: 'Dual Noise Sensor AI', bluetooth: '5.2 LDAC Hi-Res Audio', weight: '250g' }),
            imageUrl: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800',
            aiTags: JSON.stringify(['tai-nghe', 'chong-on', 'sony', 'am-thanh-hay', 'lam-viec'])
        },
        {
            categoryId: catFashion.id,
            name: 'Bàn Phím Cơ Không Dây Custom NuPhy Air75 V2 (Low-Profile)',
            sku: 'NUPHY-AIR75-V2',
            priceMinor: 2890000,
            originalPriceMinor: 3290000,
            stockQuantity: 30,
            description: 'Bàn phím cơ siêu mỏng 75% gõ cực êm, hỗ trợ 3 chế độ kết nối (Bluetooth 5.1, 2.4GHz Receiver, Type-C) tương thích tuyệt đối cho cả macOS và Windows.',
            specs: JSON.stringify({ layout: '75% 84 phím', switch: 'Cowberry Linear Pre-lubed', keycaps: 'PBT Dye-sub', battery: '4000 mAh' }),
            imageUrl: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800',
            aiTags: JSON.stringify(['ban-phim-co', 'low-profile', 'nuphy', 'setup-dep', 'lap-trinh'])
        },
        {
            categoryId: catCoffee.id,
            name: 'Cà Phê Arabica Cầu Đất Thượng Hạng (Hương Vị AI Tuyển Chọn)',
            sku: 'CAFE-ARABICA-500G',
            priceMinor: 185000,
            originalPriceMinor: 220000,
            stockQuantity: 100,
            description: 'Hạt cà phê Arabica 100% trồng tại vùng Cầu Đất - Đà Lạt ở độ cao 1650m, được rang mộc tỉ mỉ với công thức tối ưu hóa nhiệt độ bằng AI cho hương vị trái cây thơm dịu.',
            specs: JSON.stringify({ origin: 'Cầu Đất, Đà Lạt', roast_level: 'Medium Roast', flavor_notes: 'Caramel, Chocolate, Cam Bergamot', weight: '500g hạt nguyên chất' }),
            imageUrl: 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800',
            aiTags: JSON.stringify(['cafe', 'ca-phe-moc', 'arabica', 'cau-dat', 'do-uong'])
        }
    ];
    for (const p of productsData) {
        const product = await prisma.product.upsert({
            where: { sku: p.sku },
            update: {},
            create: p
        });
        // Mock embedding vector for product (16 dimension demo array)
        const mockVector = Array.from({ length: 16 }, () => Number((Math.random() * 2 - 1).toFixed(4)));
        await prisma.productVector.upsert({
            where: { productId: product.id },
            update: {},
            create: {
                productId: product.id,
                embeddingModel: 'text-embedding-3-small',
                embeddingVector: JSON.stringify(mockVector),
                metadataJson: JSON.stringify({ category: p.categoryId, name: p.name })
            }
        });
    }
    console.log('✅ Products & Vector Embeddings created');
    // 5. Initial Demo Cart for customer
    const demoCart = await prisma.cart.create({
        data: {
            userId: customer.id,
            totalMinor: 32990000,
            items: {
                create: [
                    {
                        productId: 1, // MacBook Air M3
                        quantity: 1,
                        unitPriceMinor: 32990000
                    }
                ]
            }
        }
    });
    // 6. Initial Demo Order
    await prisma.order.create({
        data: {
            userId: customer.id,
            orderCode: 'ORD-202611-001',
            totalMinor: 32990000,
            discountMinor: 1000000, // 1 triệu AI coupon
            shippingMinor: 50000,
            finalAmountMinor: 32040000,
            status: 'CONFIRMED',
            paymentStatus: 'PAID',
            shippingName: 'Lê Khách Hàng',
            shippingPhone: '0988776655',
            shippingAddress: 'Tòa nhà FPT Polytechnic, Đường Trịnh Văn Bô, Nam Từ Liêm, Hà Nội',
            items: {
                create: [
                    {
                        productId: 1,
                        quantity: 1,
                        unitPriceMinor: 32990000,
                        subtotalMinor: 32990000
                    }
                ]
            },
            payments: {
                create: {
                    paymentMethod: 'VNPAY',
                    transactionId: 'VNPAY-TRANS-987654',
                    amountMinor: 32040000,
                    status: 'PAID'
                }
            },
            shippingRecord: {
                create: {
                    carrierCode: 'GHN',
                    trackingNumber: 'GHN-VN-8839201',
                    shippingStatus: 'IN_TRANSIT',
                    estimatedDelivery: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000)
                }
            }
        }
    });
    console.log('✅ Demo Order & Payment & Shipping created');
    console.log('🎉 Seeding completed successfully!');
}
main()
    .catch((e) => {
    console.error('❌ Error during seeding:', e);
    process.exit(1);
})
    .finally(async () => {
    await prisma.$disconnect();
});
