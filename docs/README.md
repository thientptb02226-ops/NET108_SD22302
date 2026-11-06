# Documentation Index — AI-Native Commerce & Trello Clone Architecture

> **Mục đích**: Bảng chỉ mục tập trung (Index Map) cho toàn bộ tài liệu dự án theo đúng chuẩn cấu trúc Vibe Coding. Mọi tài liệu mới phát sinh phải được đặt đúng thư mục con tương ứng và cập nhật vào bảng chỉ mục này.

---

## Cấu trúc thư mục tài liệu (`docs/`)

```
docs/
├── README.md               # [THIS FILE] Bảng chỉ mục tổng hợp mọi tài liệu dự án
├── 01-tong-quan/           # Overview: Mục tiêu, phạm vi đề tài, kiến trúc tổng quát, quy trình
├── 02-ky-thuat/            # Technical: API spec, Database schema, MCP architecture, Checklist
├── 03-san-pham/            # Product: PRD, Spec chi tiết, User stories, Roadmap
├── 04-van-hanh/            # Operations: Hướng dẫn triển khai, Docker, Runbook, CI/CD
├── 05-mau/                 # Templates: Biểu mẫu báo cáo, checklist tái sử dụng
├── 06-design/              # Design & Diagrams: Sơ đồ Use Case, ERD, Flowchart, UI Wireframes
└── 99-ghi-chu/             # Notes: Biên bản họp nhóm, ghi chú nháp, ý tưởng lặt vặt
```

---

## Danh mục tài liệu chi tiết

### 📁 `01-tong-quan/` (Tổng quan & Định hướng dự án)
- [`ai-native-commerce-blueprint.md`](01-tong-quan/ai-native-commerce-blueprint.md): Bản thiết kế kiến trúc toàn diện của Hệ thống Thương mại Điện tử AI-Native.
- [`vibe-coding-workflow.md`](01-tong-quan/vibe-coding-workflow.md): Quy trình chuẩn Vibe Coding, quản lý ngữ cảnh và phối hợp đa tác tử AI.
- [`multi-agent-workflow.md`](01-tong-quan/multi-agent-workflow.md): Giao thức phối hợp giữa Antigravity, Claude Code và OpenAI Codex.
- [`karpathy-examples.md`](01-tong-quan/karpathy-examples.md): Các ví dụ thực tế áp dụng nguyên tắc Andrej Karpathy (Think first, Minimal code, Surgical changes).

### 📁 `02-ky-thuat/` (Kiến trúc kỹ thuật & Kỹ nghệ hệ thống)
- [`mcp-reference-architecture.md`](02-ky-thuat/mcp-reference-architecture.md): Kiến trúc tham chiếu Model Context Protocol (MCP) kết nối Trello Clone & AI.
- [`api-spec.md`](02-ky-thuat/api-spec.md): Đặc tả chi tiết các RESTful API và WebSocket Endpoints.
- [`architecture.md`](02-ky-thuat/architecture.md): Sơ đồ kiến trúc tầng (Layered Architecture) và luồng dữ liệu.
- [`openapi.yaml`](02-ky-thuat/openapi.yaml): Chuẩn OpenAPI 3.0 cho toàn bộ API Core.
- [`schema-transactional.sql`](02-ky-thuat/schema-transactional.sql): Kịch bản cơ sở dữ liệu quan hệ và các bảng giao dịch tài chính.
- [`test-cases-p0-p1.csv`](02-ky-thuat/test-cases-p0-p1.csv): Ma trận 25 kịch bản kiểm thử trọng yếu mức P0/P1.
- `references/`: Bộ tiêu chuẩn kỹ thuật (Accessibility, Observability, Orchestration, Performance, Security, Testing, DoD).

### 📁 `03-san-pham/` (Yêu cầu nghiệp vụ & Sản phẩm)
- [`roadmap.md`](03-san-pham/roadmap.md): Kế hoạch và tiến độ bàn giao sản phẩm qua 4 Sprint tương ứng với 4 bài Lab môn NET108.

### 📁 `04-van-hanh/` (Triển khai & Vận hành)
- [`deployment-guide.md`](04-van-hanh/deployment-guide.md): Hướng dẫn triển khai Docker Compose, cấu hình môi trường (.env) và CI/CD.

### 📁 `05-mau/` (Biểu mẫu & Mẫu báo cáo)
- Lưu trữ các biểu mẫu báo cáo Word, Excel checklist chuẩn của trường Cao đẳng FPT Polytechnic.

### 📁 `06-design/` (Thiết kế & Sơ đồ mô hình hóa)
- `use-cases/`:
  - [`usecase_ainative_tongquat.png`](06-design/use-cases/usecase_ainative_tongquat.png): Sơ đồ Use Case tổng quát hệ thống AI-Native Commerce (Hình 2 - 28 UCs).
  - [`usecase_ainative_customer.png`](06-design/use-cases/usecase_ainative_customer.png): Sơ đồ Use Case phân hệ Khách hàng (Hình 3 - 14 UCs).
  - [`usecase_ainative_admin.png`](06-design/use-cases/usecase_ainative_admin.png): Sơ đồ Use Case phân hệ Quản trị & Nhà bán (Hình 4 - 10 UCs).
  - [`usecase_ainative_agent.png`](06-design/use-cases/usecase_ainative_agent.png): Sơ đồ Use Case phân hệ Tác tử AI Platform (Hình 5 - 8 UCs).
- Kiến trúc tổng thể & Sơ đồ hệ thống:
  - [`erd_ainative_conceptual.png`](06-design/erd_ainative_conceptual.png): Sơ đồ mô hình quan hệ thực thể mức khái niệm Conceptual ERD (Hình 6).
  - [`deploy_diagram.png`](06-design/deploy_diagram.png): Sơ đồ triển khai hệ thống phân tầng Docker Compose (Hình 7).
  - [`appmap_diagram.png`](06-design/appmap_diagram.png): Sơ đồ tổ chức của ứng dụng & luồng điều hướng Appmap (Hình 8).
  - [`tech_stack_diagram.png`](06-design/tech_stack_diagram.png): Sơ đồ phân tầng mô hình kiến trúc công nghệ Tech Stack (Hình 9).
  - [`ui_wireframe_shared.png`](06-design/ui_wireframe_shared.png): Thiết kế giao diện UI chức năng dùng chung (Hình 10).
  - [`ui_wireframe_customer.png`](06-design/ui_wireframe_customer.png): Thiết kế giao diện UI phân hệ Khách hàng & Mua sắm AI (Hình 11).
  - [`ui_wireframe_admin.png`](06-design/ui_wireframe_admin.png): Thiết kế giao diện UI phân hệ Quản trị & Nhà bán hàng (Hình 12).

### 📁 `99-ghi-chu/` (Ghi chú & Nháp)
- Lưu trữ các ghi chú họp nhóm, phân công việc phát sinh và nhật ký lỗi.

