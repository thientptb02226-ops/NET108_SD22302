# 🎓 BÁO CÁO DỰ ÁN MÔN HỌC .NET 1 (NET108) — LỚP SD22302

### TRƯỜNG CAO ĐẲNG FPT POLYTECHNIC ĐỒNG NAI — CÔNG NGHỆ THÔNG TIN (KHÓA K20)

---

## 📋 THÔNG TIN ĐỀ TÀI & NHÓM SINH VIÊN THỰC HIỆN

- **Môn học**: Dự án .NET 1 (Mã môn: **NET108**)
- **Lớp**: **SD22302** (Chuyên ngành Phát triển Phần mềm)
- **Đề tài**: **Xây dựng Hệ thống Thương mại Điện tử AI-Native (AI-Native Commerce)**
- **Giảng viên hướng dẫn**: **ThS. Phan Hoàng Khải**
- **Nhóm thực hiện**: **Nhóm 5**
    1. **Trần Phúc Thiên** (Nhóm trưởng — MSSV: **TB02226**)
    2. **Trần Phạm Hoàng Minh** (Thành viên — MSSV: **TB02231**)
    3. **Cho Hoàng Hiếu Trung** (Thành viên — MSSV: **TB02324**)
    4. **Nguyễn Hoàng Quốc Anh** (Thành viên — MSSV: **TB02232**)
    5. **Nguyễn Châu Văn Phát** (Thành viên — MSSV: **TB02274**)
- **Hệ thống Quản lý Tiến độ (Jira Cloud)**: [thientptb02226.atlassian.net](https://thientptb02226.atlassian.net) (Dự án: **NET108**)

---

## 🌟 1. GIỚI THIỆU TỔNG QUAN HỆ THỐNG

Dự án được xây dựng theo chuẩn công nghiệp, ứng dụng phương pháp **Vibe Coding & Multi-Agent Collaboration** (phối hợp giữa các AI Agent: Google Antigravity, Claude Code CLI, OpenAI Codex) để phân tích, thiết kế và phát triển nền tảng **AI-Native Commerce**:

- **Trợ lý Mua sắm AI (Shopping Assistant & Intent Router)**: Tư vấn theo nhu cầu hội thoại thực tế của khách hàng, thấu hiểu ngữ cảnh và gợi ý sản phẩm cá nhân hóa.
- **Tìm kiếm Ngữ nghĩa (Semantic & Hybrid Search)**: Tích hợp RAG (Retrieval-Augmented Generation) kết hợp Vector Search và Full-text Search.
- **Giao thức Thương mại Tác tử (Agentic Commerce Protocol - ACP)**: Chuẩn hóa quy trình giao dịch tự động của các AI Agent với cơ chế Guardrails (giới hạn hạn mức, OTP xác thực 2 lớp, chống gian lận).
- **Giao dịch An toàn (Checkout Saga & Idempotency)**: Chống bán quá tồn kho (Over-selling), đảm bảo tính toàn vẹn dữ liệu giao dịch tài chính.
- **Quản trị Toàn diện (Admin & Merchant Hub)**: Phân quyền vai trò RBAC (Khách vãng lai, Khách hàng, Nhà bán/Quản trị viên, Tác tử AI Platform).

---

## 📂 2. CẤU TRÚC THƯ MỤC DỰ ÁN (CHUẨN VIBE CODING)

Dự án tuân thủ nghiêm ngặt nguyên tắc **Vibe Coding Workspace Protocol** — Thư mục gốc chỉ chứa các phân hệ module, tài liệu chuẩn hóa và đúng 2 file cấu hình AI Agent cốt lõi:

```
NET108_SD22302/
├── 📁 Các Bài Lab/                                 # HỒ SƠ BÁO CÁO LAB CHUẨN FPT POLYTECHNIC
│   └── 📄 Lab1_NET108_AI_Native_Commerce.docx      # Báo cáo Lab 1 chính thức (14 SRS, Sơ đồ Use Case)
│
├── 📁 docs/                                        # HỒ SƠ TÀI LIỆU KỸ THUẬT & HỌC THUẬT
│   ├── 📄 README.md                                # Bảng chỉ mục tổng hợp mọi tài liệu (Docs Index Map)
│   ├── 📁 01-tong-quan/                            # Tổng quan, Blueprint kiến trúc, Vibe Coding, Karpathy
│   │   ├── ai-native-commerce-blueprint.md         # Bản thiết kế kiến trúc toàn diện AI-Native Commerce
│   │   ├── vibe-coding-workflow.md                 # Quy trình Vibe Coding chuẩn 10 bước
│   │   ├── multi-agent-workflow.md                 # Giao thức phối hợp Antigravity, Claude Code, Codex
│   │   └── karpathy-examples.md                    # Đối chiếu 4 nguyên tắc kỹ thuật chuẩn Andrej Karpathy
│   ├── 📁 02-ky-thuat/                             # Đặc tả kỹ thuật, CSDL, API, MCP, Test Cases
│   │   ├── mcp-reference-architecture.md           # Kiến trúc tham chiếu Model Context Protocol (MCP)
│   │   ├── api-spec.md                             # Đặc tả chi tiết RESTful API & WebSocket
│   │   ├── architecture.md                         # Sơ đồ kiến trúc phân tầng hệ thống
│   │   ├── openapi.yaml                            # Hợp đồng API chuẩn OpenAPI 3.0
│   │   ├── schema-transactional.sql                # Thiết kế CSDL quan hệ PostgreSQL DDL
│   │   ├── test-cases-p0-p1.csv                    # Ma trận 25 kịch bản kiểm thử trọng yếu P0/P1
│   │   └── references/                             # Bộ tiêu chuẩn kỹ thuật (Accessibility, Performance, Security)
│   ├── 📁 03-san-pham/                             # Lộ trình sản phẩm & Sprint
│   │   └── roadmap.md                              # Kế hoạch phát triển qua 4 Sprint (Lab 1 -> Lab 4)
│   ├── 📁 04-van-hanh/                             # Hướng dẫn triển khai & vận hành
│   │   └── deployment-guide.md                     # Hướng dẫn Docker Compose, .env, CI/CD
│   ├── 📁 05-mau/                                  # Biểu mẫu báo cáo FPT Polytechnic tái sử dụng
│   ├── 📁 06-design/                               # Thiết kế & Sơ đồ mô hình hóa UML
│   │   └── use-cases/                              # Thư mục chứa toàn bộ hình ảnh sơ đồ Use Case
│   │       ├── usecase_ainative_tongquat.png       # Sơ đồ Use Case tổng quát AI-Native Commerce (Hình 2)
│   │       ├── usecase_ainative_customer.png       # Sơ đồ Use Case phân hệ Khách hàng (Hình 3)
│   │       ├── usecase_ainative_admin.png          # Sơ đồ Use Case phân hệ Quản trị & Nhà bán (Hình 4)
│   │       └── usecase_ainative_agent.png          # Sơ đồ Use Case phân hệ Tác tử AI Platform (Hình 5)
│   └── 📁 99-ghi-chu/                              # Biên bản họp nhóm & ghi chú kỹ thuật
│
├── 📁 scripts/                                     # TẬP LỆNH TỰ ĐỘNG HÓA & SINH DỮ LIỆU
│   └── 📁 lab-generators/                          # Các script sinh tài liệu Word & sơ đồ UML tự động
│
├── 💻 Mã nguồn các Phân hệ Module:
│   ├── 📁 Trello-Clone-Backend/                    # REST API Core (.NET / Node.js Express)
│   ├── 📁 Trello-Clone-Frontend/                   # Giao diện Web Client (React 19 / Next.js)
│   ├── 📁 Trello-Clone-MCP/                        # Model Context Protocol Server tích hợp AI Agent
│   ├── 📁 Trello-Clone-AI-RAG/                     # Dịch vụ RAG & Semantic Search (FastAPI / Vector DB)
│   ├── 📁 Chatbot-Frontend/                        # Widget Trợ lý AI Shopping Assistant
│   ├── 📁 Trello-Clone-Desktop/                    # Ứng dụng Desktop (Electron / Tauri)
│   ├── 📁 Trello-Clone-Mobile/                     # Ứng dụng Di động (React Native / Expo)
│   └── 📁 Trello-Clone-Infra/                      # Hạ tầng Docker, Kubernetes, CI/CD
│
├── 🤖 .agent/ & .claude/ & .codex/                 # Cấu hình Multi-Agent, Rules (docs-placement.md) & Skills
├── 📜 AGENTS.md                                    # Thỏa ước điều phối đa tác tử AI (Master Coordination)
├── 📜 CLAUDE.md                                    # Hướng dẫn thực thi cho Claude Code CLI
├── 🐳 docker-compose.yml                           # Hạ tầng PostgreSQL, Redis, MinIO
├── 📦 package.json                                 # Monorepo Workspace Root
└── 📜 README.md                                    # Tài liệu tổng quan dự án này
```

---

## 📑 3. LIÊN KẾT NHANH TÀI LIỆU QUAN TRỌNG CHO GIẢNG VIÊN

| STT | Tài liệu                        | Định dạng | Vị trí lưu trữ                                                                                                     | Tóm tắt nội dung                                                                                                      |
| :-: | :------------------------------ | :-------: | :----------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
|  1  | **Báo Cáo Lab 1 Chính Thức**    |  `.docx`  | [`Các Bài Lab/Lab1_NET108_AI_Native_Commerce.docx`](Các%20Bài%20Lab/Lab1_NET108_AI_Native_Commerce.docx)           | Báo cáo hoàn chỉnh: Khảo sát AI, Giới thiệu đề tài, 4 sơ đồ Use Case (28 UCs), 14 bảng SRS, Thực thể ERD, Chương 3 Thiết kế hệ thống (Deploy, Appmap, Tech Stack, UI/Controller). |
|  2  | **Chỉ Mục Toàn Bộ Docs**        |   `.md`   | [`docs/README.md`](docs/README.md)                                                                                 | Bảng mục lục tổng hợp toàn bộ tài liệu kỹ thuật, kiến trúc và vận hành.                                               |
|  3  | **Sơ Đồ Use Case Tổng Quát**    |  `.png`   | [`docs/06-design/use-cases/usecase_ainative_tongquat.png`](docs/06-design/use-cases/usecase_ainative_tongquat.png) | Sơ đồ Use Case tổng thể toàn hệ thống AI-Native Commerce (Hình 2 - 28 UCs).                                          |
|  4  | **Sơ Đồ Triển Khai Hệ Thống**   |  `.png`   | [`docs/06-design/deploy_diagram.png`](docs/06-design/deploy_diagram.png)                                           | Sơ đồ triển khai hệ thống phân tầng Docker Compose, Gateway, API Core, AI Engine (Hình 7).                            |
|  5  | **Sơ Đồ Tổ Chức Ứng Dụng**      |  `.png`   | [`docs/06-design/appmap_diagram.png`](docs/06-design/appmap_diagram.png)                                           | Sơ đồ cấu trúc điều hướng toàn bộ màn hình của ứng dụng Appmap / Sitemap (Hình 8).                                   |
|  6  | **Mô Hình Công Nghệ Tech Stack**|  `.png`   | [`docs/06-design/tech_stack_diagram.png`](docs/06-design/tech_stack_diagram.png)                                   | Sơ đồ phân tầng 5 lớp công nghệ hiện đại hợp nhất AI và E-Commerce (Hình 9).                                          |
|  7  | **Kiến Trúc MCP Reference**     |   `.md`   | [`docs/02-ky-thuat/mcp-reference-architecture.md`](docs/02-ky-thuat/mcp-reference-architecture.md)                 | Kiến trúc giao thức Model Context Protocol tích hợp AI Agent với dữ liệu.                                             |
|  8  | **Đặc Tả Hệ Thống (Blueprint)** |   `.md`   | [`docs/01-tong-quan/ai-native-commerce-blueprint.md`](docs/01-tong-quan/ai-native-commerce-blueprint.md)           | Kiến trúc 7 lớp, 16 Module, 12 Agent, quy trình nghiệp vụ mua sắm thông minh.                                         |
|  9  | **Thiết Kế CSDL DDL**           |  `.sql`   | [`docs/02-ky-thuat/schema-transactional.sql`](docs/02-ky-thuat/schema-transactional.sql)                           | DDL PostgreSQL: Quotes, Idempotency, Reservations, Outbox Pattern.                                                    |
| 10  | **Hợp Đồng OpenAPI 3.0**        |  `.yaml`  | [`docs/02-ky-thuat/openapi.yaml`](docs/02-ky-thuat/openapi.yaml)                                                   | Đặc tả toàn bộ API RESTful endpoints chuẩn OpenAPI 3.0.                                                               |
| 11  | **Ma Trận Kiểm Thử P0/P1**      |  `.csv`   | [`docs/02-ky-thuat/test-cases-p0-p1.csv`](docs/02-ky-thuat/test-cases-p0-p1.csv)                                   | 25 kịch bản kiểm thử trọng yếu (Precondition, Steps, Expected Results).                                               |
| 12  | **Bản Đồ Tri Thức Graphify**    |  `.html`  | [`graphify-out/graph.html`](graphify-out/graph.html)                                                               | Bản đồ trực quan 319 nodes & 413 edges AST toàn bộ mã nguồn và tài liệu.                                              |

---

## 🚀 4. HƯỚNG DẪN CÀI ĐẶT & CHẠY THỬ NGHIỆM (QUICKSTART)

### Bước 1: Khởi động cơ sở dữ liệu qua Docker

```bash
docker compose up -d
```

_Khởi động PostgreSQL trên port `5432`, Redis trên port `6379`, MinIO trên port `9000`._

### Bước 2: Khởi chạy Backend API

```bash
cd Trello-Clone-Backend
npm install
npm run dev
```

_API hoạt động tại `http://localhost:5000` (Healthcheck: `/health`)._

### Bước 3: Khởi chạy Giao diện Web Frontend

```bash
cd ../Trello-Clone-Frontend
npm install
npm run dev
```

_Truy cập giao diện tại `http://localhost:3000`._

### Bước 4: Khởi chạy AI-RAG Service (Python)

```bash
cd ../Trello-Clone-AI-RAG
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

_Dịch vụ RAG & Semantic Search hoạt động tại `http://localhost:8000`._

---

## 🏆 5. CAM KẾT CHẤT LƯỢNG & ĐẠO ĐỨC HỌC THUẬT

- Mọi tài liệu và mã nguồn được xây dựng tuân thủ nghiêm ngặt **Karpathy Guidelines** (Simplicity First, Surgical Changes, Goal-Driven).
- Lịch sử Git thể hiện minh bạch, chi tiết quá trình hoàn thành từng hạng mục theo các Epic/Task trên Jira Cloud.
- Bảo mật thông tin: Tuyệt đối không commit file cấu hình nhạy cảm (`.env`), không để lộ API Token hay Private Key.
