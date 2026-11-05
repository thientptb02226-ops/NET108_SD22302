# Docs Placement — Mọi file .md phải nằm đúng chỗ trong docs/

> **Level: MANDATORY**  
> **Rule**: Khi AI tạo bất kỳ file `.md` nào cho dự án (report, plan, spec, guide, note, analysis, design doc...) $\rightarrow$ **PHẢI** đặt trong thư mục `docs/` ở gốc dự án, vào đúng nhóm con tương ứng. **Cấm vứt file `.md`, file `.png`, script `.py` rải rác khắp nơi** (cạnh code, ở root, trong thư mục ngẫu nhiên).

---

## 1. Cấu trúc chuẩn — `docs/` ở gốc dự án

```
docs/
├── README.md               # index: liệt kê mọi doc + 1 dòng mô tả (luôn cập nhật)
├── 01-tong-quan/           # overview: mục tiêu, phạm vi, kiến trúc tổng, roadmap
├── 02-ky-thuat/            # technical: API, DB, tech decision, integration, ARCHITECTURE
├── 03-san-pham/            # product: PRD, spec, user story, feature, business case
├── 04-van-hanh/            # operations: deploy, runbook, incident, backup, monitoring
├── 05-mau/                 # mẫu / templates: doc mẫu, form, checklist tái sử dụng
├── 06-design/              # design: UI/UX, wireframe, design system, flow, diagram
└── 99-ghi-chu/             # notes: nháp, ghi chú nhanh, meeting, lặt vặt chưa phân loại
```

- Nhóm con dùng **prefix số (`01-`, `02-` ... `99-`)** để sort ổn định.
- `99-ghi-chu` luôn cuối. Đây là bộ nhóm mặc định — nếu dự án đã có `docs/` với nhóm khác thì theo nhóm hiện có, không tự đổi tên.

---

## 2. Quy tắc Thư mục gốc (Root Directory)
1. Thư mục gốc chỉ chứa các phân hệ module, `docs/`, `Các Bài Lab/` và **đúng 2 file cấu hình agent**:
   - `AGENTS.md`
   - `CLAUDE.md`
   *(Kèm các file gốc chuẩn: `README.md`, `package.json`, `docker-compose.yml`, `.gitignore`)*.
2. Tuyệt đối không sinh file script nháp, file kết xuất hình ảnh hay tài liệu tạm thời tại thư mục gốc. Mọi script sinh tự động phải lưu trữ trong `scripts/`.
