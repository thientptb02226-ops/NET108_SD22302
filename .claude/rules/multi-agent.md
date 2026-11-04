# Rule: Multi-Agent Orchestration — Parallel Fan-Out

> **Source**: Code Web Không Khó — Agent Hub

## 1. Decision Rule
- **Việc nhỏ (1 component, 1 bug, 1 function)**: Sử dụng 1 agent duy nhất để tối ưu token và tránh overhead.
- **Việc lớn (Full feature từ backend sang frontend, refactor diện rộng, audit toàn hệ thống)**: Chia nhỏ và kích hoạt các agent chuyên biệt chạy song song (tối đa 5 agent cùng lúc).

## 2. Khi nào dùng nhiều Agent
1. **Phân tách Frontend và Backend**:
   - Agent 1 (`ui-ux-designer` / `software-engineer`) xây dựng giao diện React / Vite.
   - Agent 2 (`software-engineer` backend) xây dựng REST API / Prisma schema.
2. **Feature & Testing song hành**:
   - Dev agent viết code tính năng.
   - QA agent (`qa-test-engineer`) viết integration test và edge case suites.
3. **Audit & Review**:
   - Một agent độc lập quét bảo mật (`/security-review-pro`) trong khi dev agent tiếp tục phát triển.

## 3. Khi nào KHÔNG dùng nhiều Agent
- Fix bug nhỏ (1 dòng code hoặc 1 file).
- Chưa có hợp đồng API (Interface Contract) rõ ràng giữa 2 bên.
- Chỉnh sửa cùng 1 file (dễ gây conflict).

