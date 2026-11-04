# Quy trình Vibe Coding chuẩn cho AI Agents

> **Nguồn**: `@aidailyvietnam` (TikTok ID: 7674461635787967762)  
> **Áp dụng cho**: Claude Code CLI, Antigravity, OpenAI Codex

---

## 1. Thông điệp cốt lõi
> *"Vibe Coding hiệu quả không phải là ném một prompt lớn cho AI rồi chờ. Con người làm chủ kiến trúc, phạm vi và kiểm soát chất lượng; AI là máy gia tốc."*

**Hai lá chắn an toàn bắt buộc**:
1. **Specification** (Tài liệu context & spec chi tiết).
2. **Git** (Kỷ luật commit từng atomic task, điểm tựa rollback an toàn).

---

## 2. Quy trình 10 bước phát triển

### Bước 1: Xác định bài toán & phạm vi
- Trả lời 3 câu hỏi trước khi code:
  1. Người dùng là ai?
  2. Ứng dụng giải quyết vấn đề gì?
  3. Chức năng chính là gì?
- Tránh prompt chung chung không có ranh giới rõ ràng.

### Bước 2: Phân tích & thiết kế hệ thống
- Chia 3 tầng rõ ràng: Frontend (giao diện), Backend (nghiệp vụ), Database (lưu trữ).
- Thiết lập phân quyền (RBAC/ABAC) và luồng giao tiếp giữa các module.
- Chốt tech stack trước khi bắt tay viết dòng code đầu tiên.

### Bước 3: Tạo tài liệu specs & context cho AI
- Xây dựng `CONTEXT.md`, `PROJECT_RULES.md`, `SCHEMA.sql`, OpenAPI spec.
- Càng nhiều context chuẩn xác thì AI sinh code càng ít lỗi.

### Bước 4: Triển khai tuần tự, từng task nhỏ (Atomic Tasks)
- Chia nhỏ pipeline: xong 1 chức năng nhỏ ➔ test OK ➔ mới sang chức năng kế tiếp.

### Bước 5: Bắt buộc AI đọc codebase trước khi sửa
- Đọc cấu trúc hiện tại ➔ tìm module liên quan ➔ chỉ ra vị trí tích hợp trước khi code.

### Bước 6: Lập kế hoạch trước khi code (Plan first)
- AI đưa ra kế hoạch từng bước; **chưa được sửa file nào** cho đến khi con người duyệt kế hoạch.

### Bước 7: Kiểm tra & test kỹ
- Chạy test suite, kiểm tra các edge case (lỗi xác thực, hết hạn, race condition).

### Bước 8: Debug có thiết kế
- Cung cấp đủ 3 thông tin: Kết quả mong muốn, Kết quả thực tế, Error message & stack trace.
- Tìm nguyên nhân gốc: *"Tại sao lỗi này lại xảy ra?"*, không copy-paste mù quáng.

### Bước 9: Review & refactor có phạm vi
- Refactor có giới hạn từng module, không refactor toàn bộ dự án tràn lan.

### Bước 10: Kỷ luật Git
- Commit ngay sau mỗi tính năng hoạt động ổn định.
- Giữ lịch sử commit nguyên tử làm điểm tựa rollback (`git reset`).

