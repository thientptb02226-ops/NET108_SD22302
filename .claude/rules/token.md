# Rule: Token Discipline

> **Source**: Code Web Không Khó — Agent Hub

## 1. Output Rules (Text to User)
- Trả lời ngắn gọn, trực diện vào vấn đề, không vòng vo chào hỏi dài dòng.
- Không lặp lại nguyên văn file artifact hoặc code đã có.
- Trình bày dạng bullet points, bảng biểu hoặc liên kết file rõ ràng.

## 2. Tool Call Rules
- Đọc file đúng phạm vi (dùng `StartLine` / `EndLine` khi file lớn).
- Không search vô định, dùng query chính xác.
- Commit nguyên tử, kiểm tra syntax trước khi hoàn tất lượt.
