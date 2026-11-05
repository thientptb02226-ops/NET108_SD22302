# 🎓 BÁO CÁO DỰ ÁN MÔN HỌC NET108 — LỚP SD22302
### TRƯỜNG CAO ĐẲNG FPT POLYTECHNIC — KHOA CÔNG NGHỆ THÔNG TIN

---

## 📋 THÔNG TIN ĐỀ TÀI & SINH VIÊN
* **Môn học**: Dự án mẫu (Mã môn: **NET108** / PRO1041)
* **Lớp**: **SD22302** (Chuyên ngành Lập trình / Phát triển phần mềm)
* **Đề tài**: **Hệ thống Quản lý Bán hàng Quán Đồ Uống (Poly Drink Management System)**
* **Sinh viên thực hiện**: **Trịnh Quốc Khải**
* **Mã số sinh viên (MSSV)**: **PS38237**
* **Giảng viên hướng dẫn**: Giảng viên Bộ môn CNTT — FPT Polytechnic

---

## 🌟 1. GIỚI THIỆU TỔNG QUAN HỆ THỐNG
Dự án được xây dựng theo chuẩn công nghiệp, ứng dụng phương pháp **Vibe Coding & Multi-Agent Collaboration** (kết hợp các AI Agent: Claude Code CLI, Google Antigravity, OpenAI Codex) để phân tích, thiết kế và phát triển:
- **Phân hệ Quán đồ uống (Poly Drink)**: Quản lý Menu (Loại đồ uống, Đồ uống), Bán hàng tại quầy (POS), Quản lý nhân viên, Phân quyền (Nhân viên, Quản lý), Hóa đơn, Thống kê doanh thu.
- **Nền tảng mở rộng AI-Native Commerce**: 
  - Trợ lý AI Shopping Assistant tư vấn theo nhu cầu thực tế.
  - Tìm kiếm ngữ nghĩa (Semantic & Hybrid Search).
  - Quy trình Checkout Saga an toàn, chống bán quá tồn kho (Over-selling) và Idempotency chống trùng giao dịch.

---

## 📂 2. CẤU TRÚC THƯ MỤC NỘP BÀI (DIRECTORY LAYOUT)

```
NET108_SD22302/
├── 📄 BaoCao_Lab1_NET108_Nhom5_QuanLyQuanCaPhe.docx  # File Word Báo cáo Lab 1 (Nhóm 5)
├── 🖼️ usecase_tongquat.png                           # Sơ đồ Use Case tổng quát Lab 1
│
├── 📚 docs/                                          # HỒ SƠ TÀI LIỆU KỸ THUẬT & HỌC THUẬT
│   ├── 01-tong-quan/
│   │   ├── BaoCao_Lab1_NET108_Nhom5_QuanLyQuanCaPhe.docx # Bản lưu báo cáo đề cương
│   │   ├── usecase_tongquat.png                         # Sơ đồ Use Case
│   │   ├── ai-native-commerce-blueprint.md              # Đặc tả tổng thể hệ thống
│   │   ├── vibe-coding-workflow.md                      # Quy trình Vibe Coding chuẩn 10 bước
│   │   └── karpathy-examples.md                         # Mẫu đối chiếu Karpathy Guidelines
│   ├── 02-ky-thuat/
│   │   ├── schema-transactional.sql                     # Thiết kế CSDL PostgreSQL DDL
│   │   ├── openapi.yaml                                 # Hợp đồng API chuẩn OpenAPI 3.1
│   │   └── test-cases-p0-p1.csv                         # Ma trận 30 kịch bản kiểm thử P0/P1
│   ├── 03-san-pham/
│   │   └── roadmap.md                                   # Lộ trình Sprint & Nhật ký Changelog
│   └── 04-van-hanh/
│       └── deployment-guide.md                          # Hướng dẫn triển khai & vận hành
│
├── 💻 Mã nguồn các Module:
│   ├── Trello-Clone-Frontend/     # Giao diện Web / Kanban Board
│   ├── Trello-Clone-Backend/      # REST API & WebSocket Server
│   ├── Trello-Clone-MCP/          # Server MCP kết nối AI Agent với dữ liệu
│   ├── Trello-Clone-AI-RAG/       # Dịch vụ RAG tìm kiếm ngữ nghĩa
│   ├── Chatbot-Frontend/          # Widget Trợ lý AI Assistant
│   ├── Trello-Clone-Desktop/      # Ứng dụng Desktop
│   └── Trello-Clone-Mobile/       # Ứng dụng Di động
│
├── 🤖 .agent/ & .claude/ & .cursor/ # Cấu hình Multi-Agent, Karpathy Skills & Rules
├── 📜 AGENTS.md                   # Thỏa ước điều phối đa tác nhân AI
├── 📜 CLAUDE.md                   # Hướng dẫn thực thi cho Claude Code (tích hợp Karpathy)
├── 🐳 docker-compose.yml          # Hạ tầng PostgreSQL, Redis, ChromaDB
├── 📦 package.json                # Root Monorepo Workspaces
└── 📜 README.md                   # Tài liệu hướng dẫn này
```

---

## 📑 3. LIÊN KẾT NHANH TÀI LIỆU QUAN TRỌNG CHO GIẢNG VIÊN

| Tài liệu | Định dạng | Mô tả nội dung |
| :--- | :---: | :--- |
| [**Báo Cáo Lab 1 Word (Nhóm 5)**](docs/01-tong-quan/BaoCao_Lab1_NET108_Nhom5_QuanLyQuanCaPhe.docx) | `.docx` | Báo cáo chi tiết theo biểu mẫu FPT Poly (Use Case, 2 Actor, 13 Chức năng). |
| [**Sơ Đồ Use Case Tổng Quát**](docs/01-tong-quan/usecase_tongquat.png) | `.png` | Sơ đồ 13 Use Cases & 2 Actor (Nhân viên, Quản lý). |
| [**Đặc Tả Hệ Thống**](docs/01-tong-quan/ai-native-commerce-blueprint.md) | `.md` | Kiến trúc 7 lớp, 16 Module, 12 Agent, Quy trình nghiệp vụ. |
| [**Thiết Kế CSDL DDL**](docs/02-ky-thuat/schema-transactional.sql) | `.sql` | Schema PostgreSQL: Quotes, Idempotency, Reservations, Outbox. |
| [**Hợp Đồng OpenAPI 3.1**](docs/02-ky-thuat/openapi.yaml) | `.yaml` | Đặc tả chi tiết các REST Endpoint theo chuẩn OpenAPI. |
| [**Ma Trận Kiểm Thử P0/P1**](docs/02-ky-thuat/test-cases-p0-p1.csv) | `.csv` | 30 kịch bản test case (Precondition, Steps, Expected). |
| [**Quy Trình Vibe Coding**](docs/01-tong-quan/vibe-coding-workflow.md) | `.md` | Quy trình phát triển phần mềm chuẩn mực cùng AI. |
| [**Karpathy Guidelines & Examples**](docs/01-tong-quan/karpathy-examples.md) | `.md` | 4 nguyên tắc kỹ thuật chuẩn Andrej Karpathy (Think, Simplicity, Surgical, Goals). |
| [**Bản Đồ Kiến Trúc Graphify**](graphify-out/graph.html) | `.html` | Bản đồ mạng tri thức trực quan 280 nodes & 330 edges AST của hệ thống. |
| [**Bộ 24 Agent Skills (Addy Osmani)**](skills/) | `24 skills` | Bộ quy trình công nghiệp 24 kỹ năng SDLC (Spec, Plan, Build, Test, Review, Ship). |

---

## 🚀 4. HƯỚNG DẪN CÀI ĐẶT & CHẠY THỬ NGHIỆM (QUICKSTART)

### Bước 1: Khởi động cơ sở dữ liệu qua Docker
```bash
docker compose up -d
```
*Khởi động PostgreSQL trên port `5432` và Redis trên port `6379`.*

### Bước 2: Khởi chạy Backend API
```bash
cd Trello-Clone-Backend
npm install
npm run dev
```
*API hoạt động tại `http://localhost:5000` (Healthcheck: `/health`).*

### Bước 3: Khởi chạy Giao diện Frontend
```bash
cd ../Trello-Clone-Frontend
npm install
npm run dev
```
*Truy cập giao diện tại `http://localhost:3000`.*

---

## 🏆 5. CAM KẾT CHẤT LƯỢNG & ĐẠO ĐỨC HỌC THUẬT
- Mọi tài liệu và mã nguồn được tổ chức tuần tự theo chuẩn **Karpathy Guidelines** (Simplicity First, Surgical Changes, Goal-Driven).
- Lịch sử Git thể hiện rõ ràng các bước thực hiện từng phần.
- Bảo mật thông tin: Không commit file cấu hình nhạy cảm (`.env`), không lộ token.
