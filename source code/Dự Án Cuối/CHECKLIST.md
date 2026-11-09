# BẢNG CHECKLIST TRIỂN KHAI HỆ THỐNG AI-NATIVE COMMERCE
### Chuẩn Đặc Tả ChatGPT & Dự Án Môn Học NET108 — FPT Polytechnic
*Mô hình phát triển: Waterfall SDLC 5 Giai Đoạn & Quy Trình Vibe Coding 10 Bước*

---

## 📌 QUY TẮC BẮT BUỘC KHI AI THỰC HIỆN CÁC TÁC VỤ
1. **Chia nhỏ chức năng lớn**: Tuyệt đối không làm gộp. Chia thành các bước vi mô: `UI/UX` ➔ `Frontend Component & State` ➔ `Backend API & Saga (C# .NET)` ➔ `Database & Seed` ➔ `Kiểm thử xác nhận`.
2. **Hỏi trước khi làm**: Nếu gặp bất kỳ điểm nào chưa rõ hoặc có nhiều phương án thiết kế, **phải dừng lại hỏi người dùng trước**, không được tự giả định rồi viết code.
3. **Kỷ luật Git & Đánh dấu Checklist**: Hoàn thành từng mục nào thì đánh dấu `[x]` vào mục đó, kiểm tra build không lỗi rồi mới chuyển sang mục tiếp theo.

---

## 📑 MỤC LỤC CÁC SECTION HỆ THỐNG

- [SECTION 1: Thiết Kế Giao Diện & Bố Cục Trực Quan (UI/UX Section Architecture)](#section-1-thiết-kế-giao-diện--bố-cục-trực-quan-uiux)
- [SECTION 2: Phân Hệ Xác Thực & Phân Quyền Người Dùng (Auth & RBAC — M01)](#section-2-phân-hệ-xác-thực--phân-quyền-người-dùng-auth--rbac--m01)
- [SECTION 3: Phân Hệ Danh Mục & Sản Phẩm AI-Native (Catalog & AI Attributes — M05)](#section-3-phân-hệ-danh-mục--sản-phẩm-ai-native-catalog--ai-attributes--m05)
- [SECTION 4: Phân Hệ Giỏ Hàng & Khóa Báo Giá 15 Phút (Cart & 15-Min Quote Lock — M06)](#section-4-phân-hệ-giỏ-hàng--khóa-báo-giá-15-phút-cart--15-min-quote-lock--m06)
- [SECTION 5: Phân Hệ Thanh Toán & Đơn Hàng Saga (Checkout Saga & Idempotency — M07, M08, M09)](#section-5-phân-hệ-thanh-toán--đơn-hàng-saga-checkout-saga--idempotency--m07-m08-m09)
- [SECTION 6: Phân Hệ Trí Tuệ Nhân Tạo & Duyệt Hành Động (AI-Native Engine & HITL Level 2 — M04, M13)](#section-6-phân-hệ-trí-tuệ-nhân-tạo--duyệt-hành-động-ai-native-engine--hitl-level-2--m04-m13)
- [SECTION 7: Phân Hệ Bảng Điều Khiển Quản Trị (Admin & Merchant Portal — M01, M08)](#section-7-phân-hệ-bảng-điều-khiển-quản-trị-admin--merchant-portal--m01-m08)
- [SECTION 8: Đóng Gói Triển Khai & Bộ Kiểm Thử QA P0/P1 (DevOps & QA Validation)](#section-8-đóng-gói-triển-khai--bộ-kiểm-thử-qa-p0p1-devops--qa-validation)

---

## SECTION 1: THIẾT KẾ GIAO DIỆN & BỐ CỤC TRỰC QUAN (UI/UX)
> **Mục tiêu**: Đảm bảo giao diện cân đối, thẳng hàng 100%, chia section rõ ràng, dễ quản lý và chuẩn responsive.

- [x] **1.1. Header & Thanh Điều Hướng (Navbar Section)**
  - [x] Logo thương hiệu AI-Native Commerce + Nhãn môn học FPT NET108
  - [x] Thanh tìm kiếm AI NLP trung tâm có gợi ý câu lệnh nhanh (`laptop mỏng nhẹ < 35tr`, `tai nghe chống ồn`, `bàn phím cơ`)
  - [x] Dropdown chuyển đổi vai trò Demo (`CUSTOMER` / `MERCHANT` / `ADMIN`)
  - [x] Nút kích hoạt Bảng điều khiển Quản trị (khi ở role Admin)
  - [x] Nút mở nhanh Trợ lý AI nổi với hiệu ứng ánh sáng tím (Pulsing gradient)
  - [x] Nút mở Giỏ hàng có huy hiệu hiển thị số lượng sản phẩm thời gian thực

- [x] **1.2. Khung Giới Thiệu Kiến Trúc (Hero Banner Section)**
  - [x] Tiêu đề nhận diện thương hiệu AI-First Commerce chuẩn Enterprise
  - [x] Thẻ tóm tắt 4 trụ cột kỹ thuật: Khóa Báo Giá 15 Phút, Idempotency Saga, NLP Vector Search, HITL Action Router
  - [x] Nút kêu gọi hành động (CTA): Trò chuyện với Trợ lý AI & Xem demo tìm kiếm NLP

- [x] **1.3. Phân Đoạn Danh Mục & Bộ Lọc (Category Filter Section)**
  - [x] Tiêu đề phân đoạn rõ ràng kèm tổng số sản phẩm hiện có
  - [x] Hàng tab danh mục dạng pill (`Tất cả`, `Laptop`, `Phụ kiện & Âm thanh`, `Điện thoại`, `Đời sống`)
  - [x] Banner thông báo kết quả tìm kiếm ngữ nghĩa AI khi người dùng truy vấn tự nhiên

- [x] **1.4. Lưới Sản Phẩm Đồng Bộ (Product Grid & Cards Section)**
  - [x] Cố định chiều cao khung ảnh chuẩn 224px (`h-56`) với `object-cover` để triệt tiêu tình trạng co giãn lệch
  - [x] Khóa chiều cao hàng nhãn AI Tags (`h-6`)
  - [x] Khóa chiều cao tên sản phẩm đúng 2 dòng (`h-12`)
  - [x] Khóa chiều cao mô tả sản phẩm đúng 2 dòng (`h-10`)
  - [x] Cố định giá tiền và nút **"Chọn mua"** thẳng tắp trên cùng một đường chân trời ở đáy thẻ
  - [x] Huy hiệu trạng thái tồn kho (`Còn X món` / `Hết hàng`) và điểm khớp AI (`Phù hợp X%`)

- [x] **1.5. Cửa Sổ Chi Tiết Sản Phẩm (Product Details Modal)**
  - [x] Bố cục 2 cột: Ảnh phóng to bên trái, Thông số chi tiết bên phải
  - [x] Bảng thông số kỹ thuật phần cứng cốt lõi (CPU, RAM, Ổ cứng, Màn hình, Pin...)
  - [x] Nhãn cam kết chất lượng (Chính hãng 100%, Đổi trả 7 ngày, Giao 2h)
  - [x] Nút phím tắt: *"Hỏi Trợ lý AI về sản phẩm này"*
  - [x] Bộ chọn số lượng (+/-) và nút Thêm vào giỏ hàng an toàn

- [x] **1.6. Ngăn Trượt Giỏ Hàng (Smart Cart Drawer)**
  - [x] Danh sách các mặt hàng trong giỏ, hỗ trợ tăng giảm số lượng hoặc xóa từng món
  - [x] Bảng tính giá tự động: Tạm tính, Chiết khấu AI voucher, Phí vận chuyển, Thuế VAT 10%
  - [x] Thẻ Khóa Báo Giá Đóng Băng với đồng hồ đếm ngược thời gian thực 15 phút (`15:00` ➔ `00:00`)
  - [x] Nút tiến hành Đặt hàng An toàn (chỉ mở khi đã có báo giá hợp lệ)

- [x] **1.7. Cửa Sổ Thanh Toán (Checkout Modal)**
  - [x] Nhập thông tin nhận hàng: Họ tên, Số điện thoại, Địa chỉ giao hàng
  - [x] Chọn phương thức thanh toán: Quét mã VietQR chuyển khoản hoặc COD tiền mặt
  - [x] Khung hiển thị mã VietQR động tự động điền số tiền theo báo giá và nội dung đơn
  - [x] Nút xác nhận thanh toán bảo vệ bởi Idempotency Saga

- [x] **1.8. Cửa Sổ Thông Báo Đơn Hàng Thành Công (Order Success Modal)**
  - [x] Biểu tượng thành công và mã đơn hàng định danh duy nhất (VD: `ORD-202611-1234`)
  - [x] Trực quan hóa tiến trình vòng đời State Machine (Đã xác nhận ➔ Đang xử lý ➔ Đang giao ➔ Hoàn tất)
  - [x] Dự kiến thời gian nhận hàng và tổng tiền đã đóng băng

- [x] **1.9. Widget Trợ Lý AI Chatbot Nổi (AI Assistant Floating Widget)**
  - [x] Nút tròn nổi góc phải với biểu tượng Robot và hiệu ứng phát sáng
  - [x] Cửa sổ chat 420px có thanh tiêu đề gắn nhãn `HITL L2`
  - [x] Luồng tin nhắn đa lượt (Khách hàng hỏi, AI phân tích, Thẻ đề xuất sản phẩm mini)
  - [x] Thẻ phê duyệt thao tác HITL với 2 nút: **[Xác nhận duyệt]** và **[Từ chối]**
  - [x] Các chip gợi ý câu hỏi nhanh (Laptop mỏng nhẹ, Tai nghe chống ồn, Chính sách đổi trả)

- [x] **1.10. Bảng Điều Khiển Quản Trị (Admin Dashboard Modal)**
  - [x] Thẻ thống kê 4 chỉ số KPI: Tổng doanh thu, Tổng đơn hàng, Khách hàng, Tỷ lệ duyệt AI
  - [x] Bảng theo dõi vòng đời đơn hàng State Machine
  - [x] Dropdown cho phép Admin chuyển đổi trạng thái đơn hàng trực tiếp

---

## SECTION 2: PHÂN HỆ XÁC THỰC & PHÂN QUYỀN NGƯỜI DÙNG (AUTH & RBAC — M01)
- [x] **2.1. CSDL Quan Hệ & Thực Thể**
  - [x] Bảng `Roles` (`ADMIN`, `MERCHANT`, `CUSTOMER`)
  - [x] Bảng `Users` (Email unique, PasswordHash, FullName, Phone, RoleId)
- [x] **2.2. Backend C# ASP.NET Core API**
  - [x] `POST /api/v1/auth/register`: Đăng ký tài khoản khách hàng mới, mã hóa mật khẩu bằng BCrypt
  - [x] `POST /api/v1/auth/login`: Kiểm tra thông tin, sinh chuỗi JWT Bearer token có Claim Role
  - [x] `GET /api/v1/auth/me`: Lấy thông tin tài khoản đang đăng nhập
- [x] **2.3. Frontend State & Token**
  - [x] Lưu trữ JWT token an toàn trong `localStorage`
  - [x] Hàm `setAuthToken` tự động đính kèm `Authorization: Bearer <token>` vào mọi yêu cầu
  - [x] Chức năng chuyển đổi nhanh vai trò Demo trên giao diện
- [ ] **2.4. Kiểm Thử QA**
  - [x] Đăng nhập sai mật khẩu trả về HTTP 401 Unauthorized
  - [x] Email trùng trả về HTTP 400 Email already exists
  - [ ] Kiểm thử QA-SEC-001 (Kiểm soát truy cập chéo giữa các vai trò)

---

## SECTION 3: PHÂN HỆ DANH MỤC & SẢN PHẨM AI-NATIVE (CATALOG & AI ATTRIBUTES — M05)
- [x] **3.1. CSDL Quan Hệ & Thuộc Tính AI**
  - [x] Bảng `Categories` (Id, Name, Slug, Icon, Description)
  - [x] Bảng `Products` (Sku, Name, Slug, PriceMinor, StockQty, SpecsJson, AiTagsJson, Status)
- [x] **3.2. Backend C# ASP.NET Core API**
  - [x] `GET /api/v1/catalog/categories`: Lấy toàn bộ danh mục sản phẩm
  - [x] `GET /api/v1/catalog/products`: Phân trang (`page`, `limit`), lọc theo `categoryId`, tìm kiếm từ khóa
  - [x] `GET /api/v1/catalog/products/{slug}`: Chi tiết sản phẩm kèm thông số JSON
- [x] **3.3. Dữ Liệu Khởi Tạo (Seed Data)**
  - [x] Nạp 4 danh mục cốt lõi (Laptop, Phụ kiện âm thanh, Điện thoại, Đời sống)
  - [x] Nạp 7 sản phẩm có đầy đủ ảnh, thông số kỹ thuật và nhãn AI Tags (đặc biệt có laptop HP 15s giá 9.99M cho phân khúc sinh viên)
- [ ] **3.4. Kiểm Thử QA**
  - [x] Giá trị tiền tệ tính bằng đơn vị Minor (VND) tránh sai số số thực
  - [ ] Kiểm thử QA-TAX-001 / QA-TAX-002 (Tính toàn vẹn phân bổ thuế và làm tròn)

---

## SECTION 4: PHÂN HỆ GIỎ HÀNG & KHÓA BÁO GIÁ 15 PHÚT (CART & 15-MIN QUOTE LOCK — M06)
> *Chức năng lớn — Phân rã thành các bước vi mô:*

- [x] **4.1. CSDL Quản Lý Giỏ Hàng & Báo Giá Đóng Băng**
  - [x] Bảng `Carts` và `CartItems` lưu giỏ hàng của từng tài khoản
  - [x] Bảng `CommerceQuotes` lưu báo giá đóng băng: `SubtotalMinor`, `DiscountMinor`, `ShippingMinor`, `TaxMinor`, `TotalMinor`, `Fingerprint`, `ExpiresAt`
- [x] **4.2. Backend API Quản Lý Giỏ Hàng**
  - [x] `GET /api/v1/cart`: Lấy giỏ hàng kèm danh sách sản phẩm
  - [x] `POST /api/v1/cart/items`: Thêm sản phẩm vào giỏ (nếu đã có thì cộng dồn số lượng)
  - [x] `PUT /api/v1/cart/items/{id}`: Cập nhật số lượng sản phẩm
  - [x] `DELETE /api/v1/cart/items/{id}`: Xóa món khỏi giỏ
- [x] **4.3. Thuật Toán Khóa Báo Giá 15 Phút (Quote Lock Saga Step 1)**
  - [x] `POST /api/v1/cart/quote`: Kiểm tra giỏ hàng có sản phẩm không
  - [x] Tính toán thuế VAT 10%, phí ship (miễn phí nếu đơn >= 2 triệu), áp dụng chiết khấu voucher
  - [x] Băm mật mã SHA-256 tạo `fingerprint` từ cấu trúc giỏ hàng và mốc thời gian
  - [x] Đặt thời hạn hết hạn chính xác 15 phút (`ExpiresAt = UtcNow + 15m`)
- [x] **4.4. Frontend Quản Lý Thời Gian Báo Giá**
  - [x] Khi bấm *"Tạo Báo Giá Đóng Băng"*, nhận Quote và bật đồng hồ đếm ngược
  - [x] Đếm ngược từng giây (`15:00` ➔ `00:00`)
  - [x] Tự động hủy báo giá khi hết giờ hoặc khi người dùng thay đổi số lượng món trong giỏ
- [ ] **4.5. Kiểm Thử QA Chuyên Sâu**
  - [ ] QA-CHK-001: Quote hợp lệ đầy đủ fingerprint và expires_at
  - [ ] QA-CHK-002: Từ chối thanh toán nếu Quote đã quá 15 phút (`409 QUOTE_EXPIRED`)
  - [ ] QA-CHK-004: Từ chối thanh toán nếu giỏ hàng bị sửa đổi sau khi đã báo giá (`409 QUOTE_STALE`)

---

## SECTION 5: PHÂN HỆ THANH TOÁN & ĐƠN HÀNG SAGA (CHECKOUT SAGA & IDEMPOTENCY — M07, M08, M09)
> *Chức năng lớn — Phân rã thành các bước vi mô:*

- [x] **5.1. CSDL Quản Lý Giao Dịch & Tránh Trùng Lặp**
  - [x] Bảng `CommerceIdempotency` (RequestKey unique, RequestHash, HttpStatus, ResponseJson, Status)
  - [x] Bảng `Orders` và `OrderItems`
  - [x] Khóa ngoại liên kết người dùng và sản phẩm
- [x] **5.2. Cơ Chế Chống Trùng Lặp Giao Dịch (Idempotency Middleware)**
  - [x] Đọc tiêu đề `Idempotency-Key` từ HTTP Request
  - [x] Nếu RequestKey đã tồn tại và đã `COMMITTED`: trả về ngay kết quả lưu trong DB kèm header `X-Idempotent-Replay: true`, không bao giờ trừ tiền hoặc tạo đơn lần 2
- [x] **5.3. Quy Trình Saga Checkout An Toàn**
  - [x] Bước 1: Xác thực Quote ID còn thời hạn (chưa quá 15 phút)
  - [x] Bước 2: Giữ và trừ tồn kho thực tế (`StockQty = StockQty - Quantity`)
  - [x] Bước 3: Tạo đơn hàng với mã định danh ngẫu nhiên (VD: `ORD-202611-xxxx`)
  - [x] Bước 4: Chuyển dữ liệu các món từ Quote sang `OrderItems`
  - [x] Bước 5: Làm sạch giỏ hàng của người dùng
  - [x] Bước 6: Lưu kết quả vào bảng `CommerceIdempotency`
- [x] **5.4. Phương Thức Thanh Toán VietQR & COD**
  - [x] Tự động sinh link ảnh VietQR chuẩn Napas theo định dạng: `https://img.vietqr.io/image/...`
  - [x] Đơn VietQR chuyển sang trạng thái thanh toán `PAID` / `CONFIRMED`
  - [x] Đơn COD ở trạng thái `PENDING_PAYMENT`
- [x] **5.5. Quản Lý Vòng Đời Đơn Hàng (State Machine)**
  - [x] Các trạng thái chuẩn: `PENDING_PAYMENT` ➔ `CONFIRMED` ➔ `PROCESSING` ➔ `SHIPPED` ➔ `DELIVERED` ➔ `COMPLETED`
  - [x] Hủy đơn hàng (`/cancel`): Tự động cộng hoàn trả lại tồn kho sản phẩm
- [ ] **5.6. Kiểm Thử QA Chuyên Sâu**
  - [ ] QA-ORD-001: Gửi 2 request thanh toán cùng Idempotency Key ➔ chỉ tạo 1 đơn hàng duy nhất
  - [ ] QA-ORD-002: Cùng Idempotency Key nhưng đổi payload ➔ báo lỗi 409 Conflict
  - [ ] QA-INV-001: Hai khách hàng cùng mua sản phẩm cuối cùng ➔ không bao giờ bị âm tồn kho

---

## SECTION 6: PHÂN HỆ TRÍ TUỆ NHÂN TẠO & DUYỆT HÀNH ĐỘNG (AI ENGINE & HITL LEVEL 2 — M04, M13)
> *Chức năng lớn — Phân rã thành các bước vi mô:*

- [x] **6.1. Tìm Kiếm Ngữ Nghĩa Ngôn Ngữ Tự Nhiên (NLP Semantic Search)**
  - [x] Thuật toán bóc tách ngân sách bằng Regex: Nhận diện *"tôi có 10 triệu"*, *"dưới 35tr"*, *"ngân sách 10 triệu"*
  - [x] Thuật toán bóc tách thuộc tính AI: `mỏng nhẹ`, `pin trâu`, `sinh viên`, `chống ồn`, `lập trình`
  - [x] Chấm điểm độ phù hợp (Match score) và đưa ra lời giải thích AI trực quan
- [x] **6.2. Trợ Lý Mua Sắm Đa Tác Tử (Conversational Shopping Agent)**
  - [x] Duy trì ngữ cảnh hội thoại đa lượt
  - [x] Tác tử Tra cứu tiến độ đơn hàng (Order Tracking Agent)
  - [x] Tác tử Giải đáp chính sách bảo hành & đổi trả 7 ngày (Return Policy Agent)
- [x] **6.3. Cơ Chế Con Người Phê Duyệt Hành Động (Human-in-the-Loop - HITL Level 2)**
  - [x] Khi AI muốn thêm hàng vào giỏ, AI không tự ý ghi DB mà phát sinh một đề xuất hành động (`AiActionApproval`) ở trạng thái `PENDING`
  - [x] Giao diện hiển thị thẻ phê duyệt màu tím với nội dung chi tiết thao tác
  - [x] Người dùng bấm **[Xác nhận duyệt]** ➔ gọi API `/assistant/approve` để thực thi ghi giỏ hàng
  - [x] Người dùng bấm **[Từ chối]** ➔ hủy thao tác an toàn
- [x] **6.4. AI Microservice Bổ Trợ (Python FastAPI Cổng 8000)**
  - [x] Microservice Python độc lập với Swagger UI tại `http://localhost:8000/docs`
  - [x] Cấu hình sẵn sàng kết nối Gemini API qua biến môi trường `GEMINI_API_KEY`
- [ ] **6.5. Kiểm Thử QA Chuyên Sâu**
  - [ ] QA-AI-002: AI Agent tuyệt đối không tự ý thanh toán nếu chưa có yêu cầu từ khách
  - [ ] QA-SEC-003: Xác thực tính toàn vẹn của mã băm phê duyệt (Action Hash)
  - [ ] QA-RET-001 / QA-RET-002: Kiểm tra chính sách đổi trả trong vòng 7 ngày

---

## SECTION 7: PHÂN HỆ BẢNG ĐIỀU KHIỂN QUẢN TRỊ (ADMIN & MERCHANT PORTAL — M01, M08)
- [x] **7.1. Backend API Thống Kê Doanh Thu**
  - [x] `GET /api/v1/admin/dashboard`: Tính tổng doanh thu, số lượng đơn, khách hàng kích hoạt, tỷ lệ duyệt AI
  - [x] `PUT /api/v1/admin/orders/{id}/status`: Cập nhật trạng thái vòng đời đơn hàng
- [x] **7.2. Giao Diện Bảng Điều Khiển Admin**
  - [x] Thẻ chỉ số KPI doanh thu có tỷ lệ tăng trưởng
  - [x] Bảng đơn hàng thời gian thực kèm dropdown cập nhật trạng thái
  - [x] Nút làm mới dữ liệu nhanh
- [ ] **7.3. Kiểm Thử QA**
  - [x] Chuyển trạng thái đơn sang `COMPLETED` tự động cập nhật trạng thái thanh toán sang `PAID`

---

## SECTION 8: ĐÓNG GÓI TRIỂN KHAI & BỘ KIỂM THỬ QA P0/P1
- [x] **8.1. File Khởi Động 1-Click Chuẩn Môn NET108**
  - [x] File `start-all.bat` khởi chạy tự động: Backend C# (`dotnet run`) + Frontend + AI Service + tự mở trình duyệt
  - [x] File `run.ps1` hỗ trợ khởi động nhanh trong môi trường PowerShell
- [x] **8.2. Tài Liệu Hướng Dẫn Chi Tiết**
  - [x] File `README.md` hướng dẫn giảng viên và sinh viên chạy thử nghiệm
  - [x] Bảng tài khoản Demo phân quyền có sẵn mật khẩu
- [x] **8.3. Cơ Sở Dữ Liệu Sẵn Sàng 100%**
  - [x] CSDL SQLite `dev.db` tự động tạo và nạp dữ liệu khi gõ `dotnet run` (không cần cài thêm DB server phức tạp)
  - [x] CSDL PostgreSQL `database/schema_postgresql.sql` và `seed_data.sql` chuẩn 3NF
- [ ] **8.4. Bộ Kịch Bản Tự Động Hóa Kiểm Thử (Automated Test Suite)**
  - [ ] Viết bộ Unit/Integration tests cho Checkout Saga & Idempotency theo file `ai_native_commerce_qa_p0p1.csv`

---

## 📌 LỊCH TRÌNH VÀ BƯỚC TIẾP THEO CẦN XÁC NHẬN VỚI NGƯỜI DÙNG:
1. Bạn có muốn điều chỉnh hoặc bổ sung thêm Section/chức năng nào trong bảng Checklist trên không?
2. Trong các chức năng lớn ở trên (Section 4: Khóa báo giá, Section 5: Checkout Saga, Section 6: AI HITL), bạn muốn chúng ta tập trung tinh chỉnh sâu hoặc viết kịch bản kiểm thử tự động (Automated Test) cho phân hệ nào trước?
