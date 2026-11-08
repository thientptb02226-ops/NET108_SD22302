# Quy trình Vibe Coding chuẩn (tóm tắt video cho AI)

## 0. Metadata

| Trường | Giá trị |
|---|---|
| Nguồn | TikTok `@aidailyvietnam`, video ID `7674461635787967762` |
| Định dạng | Video dọc 576x1024, dài khoảng 9 phút 52 giây |
| Ngôn ngữ | Tiếng Việt (phụ đề lớn dưới màn hình + slide minh hoạ) |
| Chủ đề | Cách dùng AI Agent (Claude Code, Codex, Cursor) để xây phần mềm bài bản, không chỉ "một prompt là xong" |
| Cấu trúc video | 3 phần (Act): định nghĩa & hiểu lầm, quy trình 10 bước, bản chất & kết luận |

**Lưu ý về độ tin cậy:** Bản tóm tắt này được dựng từ các khung hình lấy mẫu mỗi 10 giây (slide + phụ đề), **không có bản chép lời âm thanh**. Phần giọng nói có thể có chi tiết không xuất hiện trên slide. Các con số trong slide (99.8%, 10x, 5x, biểu đồ nợ kỹ thuật) trông như hình minh hoạ, không phải số liệu đo đạc.

---

## 1. Thông điệp cốt lõi

> Vibe Coding hiệu quả không phải là ném một prompt lớn cho AI rồi chờ. Con người làm chủ kiến trúc, phạm vi và kiểm soát chất lượng; AI là máy gia tốc.

Hai "lá chắn an toàn" video nhấn mạnh: **Specification (tài liệu context)** và **Git**.

---

## 2. Phần 1: Vibe Coding là gì, và hiểu lầm phổ biến

- **Định nghĩa:** xây phần mềm bằng ngôn ngữ tự nhiên. Con người nhập prompt, AI Agent (Claude Code, Codex, Cursor...) phân tích và thực thi, kết quả là ứng dụng hoàn thiện.
- **Hiểu lầm:** Vibe Coding *không phải* là bảo AI "làm cả dự án cho tôi chỉ với 1 câu lệnh". Giao toàn bộ trách nhiệm cho AI là tự gây tai hại cho dự án lớn.
- **Giới hạn của "one-prompt":**
  - Dự án nhỏ/thử nghiệm (ví dụ app To-Do list bằng HTML/CSS/JS, dưới khoảng 100 dòng): hoạt động tốt.
  - Dự án thực tế (hệ thống quản lý công việc có Auth, Database, API, UI): code nhanh mất kiểm soát, AI tự đoán cấu trúc, lỗi dây chuyền, khó bảo trì.
  - Kết luận: one-prompt không áp dụng được cho app lớn.

---

## 3. Phần 2: Quy trình 10 bước

Ví dụ xuyên suốt: **ứng dụng quản lý công việc cho sinh viên** (Student Task App).

### Bước 1. Xác định bài toán & phạm vi
- Trả lời 3 câu hỏi trước khi AI viết code: (1) Người dùng là ai? (2) Ứng dụng giải quyết vấn đề gì? (3) Chức năng chính là gì?
- Ví dụ: sinh viên CNTT, trễ deadline / quên lịch & quá tải bài tập, chức năng gồm tạo task, đặt deadline, phân loại, hoàn thành.
- Phạm vi mẫu: phân loại công việc, đánh dấu hoàn thành, nhận thông báo, quản lý deadline.
- **Tránh** prompt chung chung kiểu "Hãy tạo cho tôi một ứng dụng quản lý công việc".

### Bước 2. Phân tích & thiết kế hệ thống
- Chia 3 tầng: Frontend (giao diện), Backend (nghiệp vụ), Database (lưu trữ).
- Xác định phân quyền (ví dụ Quản trị viên, Quản lý nhóm) và luồng giao tiếp giữa các module.
- Chia module chức năng: Authentication, User Management, Task Management...
- Chọn tech stack trước khi code. Ví dụ trong video: React (frontend), Node.js (backend), PostgreSQL (database).
- Mục đích: **AI không phải tự đoán mò** về kiến trúc.

### Bước 3. Tạo tài liệu specs & context cho AI
- Viết các file như `CONTEXT.md`, `PROJECT_RULES.md`, `SCHEMA...` gồm: tổng quan dự án, kiến trúc & công nghệ, quy định cho AI Agent (phạm vi làm gì, cấm gì).
- Coding convention ví dụ: API theo RESTful + JSON response + HTTP status; TypeScript strict, camelCase, kiến trúc module/layer.
- Coi đây là "bộ tài liệu onboarding" như cho developer mới, nhưng dành cho AI.
- Nguyên tắc: **context càng chi tiết thì AI sinh code càng đúng.**

### Bước 4. Triển khai tuần tự, từng task nhỏ
- Chia pipeline task: Đăng ký, rồi Đăng nhập, rồi Tạo công việc...
- Quy tắc vàng: xong một chức năng và test OK thì mới sang chức năng kế.
- Lợi ích: dễ khoanh vùng lỗi. Nếu one-prompt cho dự án lớn, lỗi rất khó truy ra nguyên nhân.

### Bước 5. Bắt buộc AI đọc codebase trước khi sửa
- Không ra lệnh kiểu "Hãy thêm Notification vào project ngay!".
- Cách đúng: (1) đọc cấu trúc project hiện tại, (2) tìm module liên quan (ví dụ Notification), (3) phân tích luồng Task và chỉ ra vị trí tích hợp phù hợp (ví dụ qua event hook sau khi tạo task).

### Bước 6. Lập kế hoạch trước khi code (Plan first)
- Yêu cầu AI đưa ra kế hoạch triển khai, **chưa được sửa file nào**. Ví dụ kế hoạch thêm RBAC: (1) bảng Roles/UserRoles trong DB, (2) middleware kiểm tra quyền, (3) API guard cho endpoint, (4) cập nhật UI theo role.
- **Con người review kế hoạch**; chỉ khi duyệt mới cho AI triển khai.
- Triển khai theo từng bước trong kế hoạch. AI hoạt động như co-pilot có kỷ luật, không phải autocomplete.

### Bước 7. Kiểm tra & test kỹ
- Chạy test suite, kiểm tra các edge case (ví dụ: sai password trả 401, thiếu password trả 400, truy cập chưa cấp quyền trả 403).
- AI tạo test case, nhưng **con người vẫn phải hiểu kết quả** và đánh giá chất lượng.

### Bước 8. Debug có thiết kế
- Khi báo lỗi, cung cấp đủ context. Slide nêu "4 thông tin debug chuẩn"; các mục thấy rõ: kết quả mong muốn, kết quả thực tế, error message & stack trace.
- Hỏi nguyên nhân gốc: **nên hỏi** "Tại sao lỗi này lại xảy ra?", **không nên hỏi** "Sửa lỗi như thế nào?".
- **Tránh copy-paste mù quáng** (vòng lặp copy lỗi, dán cho AI, chấp nhận code) vì dễ sinh code rác, mất kiểm soát. Phải hiểu nguyên nhân trước khi chấp nhận bản sửa.

### Bước 9. Review & refactor có phạm vi
- Sau khi chạy được: kiểm tra phân layer, an ninh (bảo mật), code trùng lặp, logic đặt sai layer.
- Refactor có giới hạn rõ (ví dụ chỉ module Auth và tách helper), **không** ra lệnh "refactor toàn bộ project cho tốt hơn".

### Bước 10. Kỷ luật Git
- Commit ngay sau mỗi tính năng hoạt động ổn định (ví dụ hoàn thành Authentication thì commit).
- Mỗi commit là điểm tựa an toàn để quay lại (ví dụ `git reset --hard HEAD~1` khi AI làm hỏng).
- Dùng Git để kiểm soát tốc độ thay đổi do AI sinh ra.

### Vòng lặp phát triển
Sau mỗi vòng: chọn task tiếp theo, nạp context cho AI, lập kế hoạch triển khai, yêu cầu phân tích, rồi lặp lại.

---

## 4. Tóm tắt 4 giai đoạn (slide tổng kết)

| Giai đoạn | Nội dung |
|---|---|
| 1. Chuẩn bị & Thiết kế | Hiểu bài toán, phân tích requirement, xác định scope, thiết kế kiến trúc, tạo tài liệu context |
| 2. Lập kế hoạch & Thực thi | Chia project thành task nhỏ (atomic), cho AI đọc code trước khi thay đổi, lập & duyệt kế hoạch |
| 3. Kiểm thử & Chất lượng | Triển khai từng bước, chạy & test, test edge case, debug theo nguyên nhân gốc, review code & bảo mật, refactor có phạm vi |
| 4. Tổng hợp & Lặp lại | Refactor có phạm vi, commit bản ổn định, lặp vòng phát triển mới |

---

## 5. Phần 3: Bản chất của Vibe Coding

- **AI code rất nhanh nhưng cần kiểm soát chặt.** AI có thể viết code nhanh hơn con người rất nhiều, nhưng con người phải giữ quyền định hướng và quyết định thay đổi.
- **Thiếu nền tảng ban đầu thì hậu quả lớn:** không có requirement rõ ràng, AI tự đưa ra quyết định thay vì làm theo chỉ dẫn.
- **Nợ kỹ thuật tăng vọt** khi thiếu specification và bỏ qua review code (slide minh hoạ bằng biểu đồ cột tăng dần, mang tính minh hoạ).
- **Lá chắn an toàn: Spec & Git.** Specification định hình phạm vi để AI hiểu và không làm sai; Git cho phép khôi phục an toàn, kiểm soát tốc độ thay đổi, tiết kiệm thời gian debug.
- **Bản chất quy trình tốt:** *không phải* chỉ đưa prompt và nhận code mù quáng, để AI tự đoán kiến trúc, mất kiểm soát khi sửa. *Mà là* hiểu rõ bài toán & thiết kế giải pháp, chia nhỏ công việc thành atomic tasks, kiểm soát chất lượng & quản lý lịch sử code.
- **AI là đồng đội tăng tốc, developer giữ vai trò kiểm soát:** AI hỗ trợ phân tích (đọc codebase), triển khai (sinh code theo kế hoạch), kiểm thử (chạy test, soát edge case), tăng tốc (rút ngắn thời gian phát triển). Developer là "thuyền trưởng": định hướng chiến lược, kiểm soát chất lượng, giữ cho toàn bộ dự án đi đúng hướng.

---

## 6. Kết luận của video

Bốn kỹ năng cốt lõi để tổ chức quy trình phát triển phần mềm với AI:

1. **Thiết kế hệ thống:** xác định scope & kiến trúc.
2. **Atomic tasks:** chia nhỏ task và tạo context.
3. **Test & review code:** kiểm tra kỹ và xử lý edge case.
4. **Kỷ luật Git:** commit và điểm tựa rollback.

> **Con người làm chủ kiến trúc, AI là máy gia tốc.** Quy trình chuẩn là kỹ năng số 1 của kỷ nguyên AI.

---

## 7. Gợi ý cho AI khi dùng nội dung này

- Nếu người dùng muốn "làm cả app bằng một prompt", hãy giải thích giới hạn (mục 2) và đề xuất bắt đầu từ Bước 1-3.
- Khi hỗ trợ code cho dự án có sẵn: đọc codebase và đề xuất kế hoạch trước, **chưa sửa file** cho đến khi người dùng duyệt (Bước 5-6).
- Khi gặp lỗi: yêu cầu đủ context (kết quả mong muốn, kết quả thực tế, error + stack trace) và giải thích nguyên nhân gốc trước khi sửa (Bước 8).
- Khuyến khích commit sau mỗi tính năng ổn định và refactor theo phạm vi nhỏ (Bước 9-10).
