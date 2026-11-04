# Rule: Architecture Sync

> **Source**: Code Web Không Khó — Agent Hub

## 1. Nguyên tắc cốt lõi
- **Chốt kiến trúc trước khi code**: Nếu dự án chưa có hoặc thay đổi kiến trúc tổng thể, phải cập nhật tài liệu kiến trúc tại `docs/02-ky-thuat/architecture.md` trước.
- **Cập nhật ngay khi kiến trúc đổi**: Mỗi khi code thêm service, module, bảng DB mới, endpoint API mới hoặc biến môi trường, Agent PHẢI cập nhật `docs/02-ky-thuat/architecture.md` (kèm Mermaid diagram) ngay trong phiên làm việc.

## 2. Trigger tự động
- **Trigger 1**: Code vừa đổi kiến trúc (thêm route, thêm controller, thêm table) -> Cập nhật docs ngay.
- **Trigger 2**: User chốt quyết định kỹ thuật mới -> Ghi nhận vào docs trước khi bắt tay viết code.
- **Trigger 3**: Phát hiện tài liệu lệch với mã nguồn thực tế -> Đồng bộ hóa ngay lập tức.
