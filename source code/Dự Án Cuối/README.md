# AI-Native Commerce — Nền Tảng Thương Mại Điện Tử Trí Tuệ Nhân Tạo
### Dự Án Tốt Nghiệp / Cuối Khóa — Môn NET108 (Cơ Sở Dữ Liệu & Phát Triển Ứng Dụng)
**Trường Cao đẳng FPT Polytechnic**  
*Sinh viên thực hiện: Nguyễn Văn Khải*  
*Mô hình phát triển: Waterfall SDLC (5 Giai đoạn) & Vibe Coding Workflow*

---

## 1. Giới thiệu tổng quan hệ thống

**AI-Native Commerce** là sản phẩm thương mại điện tử thế hệ mới được thiết kế theo tư duy *AI-First*, kết hợp giữa nền tảng Web Hiện đại (React + Vite + TailwindCSS), Backend Doanh nghiệp (Node.js + Express + TypeScript + Prisma), và AI Microservice (FastAPI + LangChain + Gemini NLP).

### Các điểm đột phá kiến trúc:
1. **Khóa Báo Giá Đóng Băng 15 Phút (Quote Lock Fingerprint)**:
   - Toàn bộ giá tiền, chiết khấu AI voucher, thuế VAT 10% và phí vận chuyển được chốt chặn thành chữ ký số SHA-256 có thời hạn 15 phút.
   - Giữ chỗ tồn kho (`Stock Reservation`), đảm bảo khách hàng không bị đổi giá hoặc mất hàng giữa chừng.
2. **Cơ chế Chống Trùng Lặp Giao Dịch (Idempotency Saga)**:
   - Mỗi lệnh gửi thanh toán đi kèm tiêu đề `Idempotency-Key`.
   - Đảm bảo 100% không bao giờ bị trừ tiền hai lần hoặc tạo đơn hàng trùng khi mạng chập chờn.
3. **Trợ lý Mua sắm Trí tuệ Nhân tạo (Conversational Shopping Assistant)**:
   - Hỗ trợ trò chuyện hai chiều, tự động phân tích ý định (Intent Recognition), tra cứu đơn hàng, giải thích chính sách đổi trả 7 ngày.
   - **HITL (Human-in-the-Loop) Level 2**: AI đề xuất thêm vào giỏ hàng hoặc áp mã giảm giá, hiển thị thẻ phê duyệt để người dùng xác nhận trực tiếp trước khi ghi vào cơ sở dữ liệu.
4. **Tìm kiếm Ngữ nghĩa Tự nhiên (NLP Vector Search)**:
   - Tìm kiếm theo nhu cầu thay vì từ khóa cứng: *"laptop mỏng nhẹ dưới 35 triệu"*, *"tai nghe chống ồn làm việc"*, *"cà phê đặc sản đà lạt"*.

---

## 2. Cấu trúc thư mục mã nguồn (`source code/Dự Án Cuối/`)

```
Dự Án Cuối/
├── backend-dotnet/             # Core REST API C# ASP.NET Core Web API (Chuẩn NET108)
│   ├── Controllers/            # AuthController, CatalogController, CartController,
│   │                           # CheckoutController (Idempotency Saga), OrdersController, AiController, AdminController
│   ├── Data/                   # CommerceDbContext & DbInitializer (Tự động tạo dev.db & nạp dữ liệu mẫu)
│   ├── Models/                 # User, Product, Category, Cart, CommerceQuote, Order, AiActionApproval
│   ├── DTOs/                   # Data Transfer Objects chuẩn OpenAPI của ChatGPT
│   ├── Program.cs              # Entry point cấu hình JWT, CORS, EF Core Sqlite trên Cổng 5000
│   └── AiNativeCommerce.Api.csproj # Chạy trực tiếp bằng lệnh: dotnet run
├── backend/                    # Core REST API Node.js + TypeScript (Phiên bản Node.js song song)
├── database/                   # Thiết kế CSDL quan hệ 3NF (PostgreSQL DDL & Seed SQL)
├── ai-service/                 # Microservice AI Python FastAPI (Cổng 8000)
├── frontend/                   # Ứng dụng Web Storefront & Admin Portal (React 18 + Vite + TailwindCSS)
├── start-all.bat               # File khởi động 1-click toàn bộ hệ thống
└── README.md                   # Tài liệu hướng dẫn này
```

---

## 3. Hướng dẫn khởi chạy ứng dụng (Quick Start)

### Cách 1: Khởi động 1-Click bằng file Batch (Khuyên dùng)
Nhấp đúp chuột vào file:
```
source code\Dự Án Cuối\start-all.bat
```
Script sẽ tự động khởi động đồng thời:
- **Backend API**: `http://localhost:5000`
- **AI Microservice**: `http://localhost:8000`
- **Frontend Web App**: `http://localhost:3000`

---

### Cách 2: Khởi động từng phần thủ công

#### Bước 1: Khởi động Backend C# ASP.NET Core API (Chuẩn NET108)
```powershell
cd "source code/Dự Án Cuối/backend-dotnet"
dotnet run
```
*API hoạt động tại: `http://localhost:5000` | Kiểm tra sức khỏe: `http://localhost:5000/health`*
*(Hoặc bạn có thể dùng Backend Node.js tại `backend/` bằng lệnh `npm run dev`)*

#### Bước 2: Khởi động AI Microservice (Tùy chọn)
```bash
cd "source code/Dự Án Cuối/ai-service"
pip install -r requirements.txt
python main.py
```
*AI Service hoạt động tại: `http://localhost:8000`*

#### Bước 3: Khởi động Frontend Web App
```bash
cd "source code/Dự Án Cuối/frontend"
npm install
npm run dev
```
*Giao diện mở tại: `http://localhost:3000`*

---

## 4. Tài khoản Demo kiểm thử phân quyền (RBAC)

Hệ thống đã được tích hợp sẵn 3 vai trò (có thể chuyển đổi trực tiếp trên menu góc phải giao diện):

| Vai trò | Email đăng nhập | Mật khẩu | Quyền hạn chính |
| :--- | :--- | :--- | :--- |
| **Quản trị viên (ADMIN)** | `admin@ainative.vn` | `Admin@123` | Toàn quyền Bảng điều khiển KPI, cập nhật State Machine đơn hàng, xem Audit Logs |
| **Nhà bán hàng (MERCHANT)** | `merchant@ainative.vn` | `Admin@123` | Quản lý kho, xử lý đơn hàng, xem doanh thu sản phẩm |
| **Khách hàng (CUSTOMER)** | `customer@gmail.com` | `Admin@123` | Mua sắm, trò chuyện với Trợ lý AI, đóng băng báo giá 15 phút, đặt hàng VietQR/COD |

---

## 5. Danh sách API Endpoints chính

### Nhóm Xác thực & Người dùng (`/api/v1/auth`)
- `POST /register`: Đăng ký tài khoản khách hàng mới.
- `POST /login`: Đăng nhập cấp mã Bearer JWT token.
- `GET /me`: Lấy thông tin tài khoản hiện tại kèm quyền hạn RBAC.

### Nhóm Danh mục & Sản phẩm (`/api/v1/catalog`)
- `GET /categories`: Lấy danh mục sản phẩm (Laptop, Phụ kiện âm thanh, Đời sống...).
- `GET /products`: Truy vấn sản phẩm có phân trang, bộ lọc danh mục và từ khóa.
- `GET /products/:slug`: Chi tiết sản phẩm, bảng thông số specs và AI Tags.

### Nhóm Giỏ hàng & Báo giá 15 Phút (`/api/v1/cart`)
- `GET /`: Lấy giỏ hàng đang hoạt động.
- `POST /items`: Thêm sản phẩm vào giỏ hàng.
- `PUT /items/:id`: Cập nhật số lượng.
- `DELETE /items/:id`: Xóa sản phẩm khỏi giỏ.
- `POST /quote`: **Tạo Báo Giá Đóng Băng (15-Minute Quote)** sinh mã băm SHA-256 fingerprint.

### Nhóm Thanh toán & Đơn hàng (`/api/v1/checkout` & `/api/v1/orders`)
- `POST /checkout`: Thực thi **Saga Checkout** với tiêu đề `Idempotency-Key`, kiểm tra tính toàn vẹn của Quote, giữ tồn kho và tạo đơn hàng.
- `GET /orders`: Lịch sử đơn hàng của người dùng.
- `GET /orders/:id`: Chi tiết hành trình đơn hàng theo State Machine.
- `POST /orders/:id/cancel`: Hủy đơn hàng và tự động giải phóng tồn kho (`RELEASED`).

### Nhóm Trợ lý AI & Tìm kiếm Tự nhiên (`/api/v1/ai`)
- `POST /nlp-search`: Tìm kiếm ngữ nghĩa theo ý định ngôn ngữ tự nhiên.
- `POST /assistant/chat`: Trò chuyện hai chiều với Trợ lý mua sắm AI.
- `POST /assistant/approve`: Gửi quyết định phê duyệt (Duyệt / Từ chối) cho hành động HITL đề xuất.

### Nhóm Quản trị (`/api/v1/admin`)
- `GET /dashboard`: Thống kê KPI tổng doanh thu, số đơn hàng, khách hàng và tỷ lệ duyệt AI.
- `PUT /orders/:id/status`: Chuyển trạng thái đơn hàng (CONFIRMED -> PROCESSING -> SHIPPED -> COMPLETED).
