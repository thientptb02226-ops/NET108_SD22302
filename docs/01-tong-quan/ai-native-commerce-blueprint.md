# ĐẶC TẢ TỔNG THỂ HỆ THỐNG AI-NATIVE COMMERCE
**Phiên bản 1.0 & Bản mở rộng 2.0 | System Blueprint – Business & Technical Specification**

---

## PHẦN I — TỔNG QUAN HỆ THỐNG & KIẾN TRÚC LOGIC

### I. Tổng quan hệ thống
#### 1. AI-Native Commerce là gì?
AI-Native Commerce là hệ thống thương mại điện tử được thiết kế với AI là thành phần cốt lõi, tham gia trực tiếp vào việc hiểu nhu cầu, tìm kiếm sản phẩm, tư vấn, bán hàng, chăm sóc khách hàng và hỗ trợ vận hành.

Khác với thương mại điện tử truyền thống chỉ tích hợp thêm chatbot AI, hệ thống AI-Native sử dụng AI để điều phối các quy trình thương mại, nhưng vẫn phải tuân theo các quy tắc nghiệp vụ, quyền truy cập và cơ chế phê duyệt.

| Tiêu chí | E-Commerce truyền thống | AI-Native Commerce |
| :--- | :--- | :--- |
| **Tìm sản phẩm** | Từ khóa, bộ lọc | Hội thoại, hình ảnh, ngữ nghĩa |
| **Tư vấn** | Nhân viên hoặc FAQ | AI Sales Agent |
| **Đề xuất** | Dựa trên quy tắc | Theo nhu cầu và ngữ cảnh |
| **Đặt hàng** | Khách tự thao tác | AI hỗ trợ thực hiện |
| **Chăm sóc** | Ticket, chatbot | AI Service Agent |
| **Marketing** | Tạo chiến dịch thủ công | AI đề xuất và tối ưu |
| **Vận hành** | Nhân sự theo dõi | AI phát hiện, đề xuất xử lý |
| **Ra quyết định** | Con người | AI trong phạm vi được cấp quyền |

#### 2. Mục tiêu nghiệp vụ
- Tăng tỷ lệ chuyển đổi từ người truy cập thành người mua.
- Cá nhân hóa quá trình mua sắm.
- Giảm thời gian tìm kiếm và đặt hàng.
- Tự động hóa các công việc bán hàng và hậu mãi có thể kiểm soát.
- Tối ưu doanh thu, chi phí và hiệu suất vận hành.
- Cho phép các AI Agent thực hiện giao dịch an toàn thông qua API và các giao thức thương mại.

#### 3. Phạm vi triển khai
Mô hình tham chiếu B2C bán hàng hóa vật lý, đa kênh, nhiều nhà bán hàng, có khả năng mở rộng sang B2B, sản phẩm số và marketplace.
- **Customer Application**: Web, Mobile, Chat.
- **Merchant Portal**: Quản lý nhà bán hàng.
- **Admin Portal**: Quản trị toàn hệ thống.
- **AI Agent Platform**: Nền tảng điều phối và thực thi AI.
- **Commerce Core**: Nền tảng giao dịch thương mại.
- **Data & Intelligence Platform**: Dữ liệu và phân tích.
- **Integration Platform**: Tích hợp thanh toán, vận chuyển, ERP, CRM và các nền tảng AI bên ngoài.

#### 4. Các nguyên tắc thiết kế
| Mã | Nguyên tắc | Yêu cầu |
| :--- | :--- | :--- |
| **P01** | AI-first | AI tham gia trực tiếp vào hành trình thương mại |
| **P02** | API-first | Mỗi chức năng nghiệp vụ có API rõ ràng |
| **P03** | Agent-ready | Các chức năng phù hợp có thể được AI Agent gọi |
| **P04** | Human-in-the-loop | Giao dịch nhạy cảm có bước xác nhận |
| **P05** | Event-driven | Các thay đổi quan trọng phát sinh sự kiện |
| **P06** | Data-centric | Quyết định dựa trên dữ liệu có kiểm chứng |
| **P07** | Secure-by-design | Kiểm soát truy cập từ kiến trúc |
| **P08** | Observable | Có nhật ký, truy vết và đo lường |
| **P09** | Modular | Có thể thay thế hoặc mở rộng từng phần |
| **P10** | Resilient | AI lỗi không làm hỏng giao dịch cốt lõi |

---

### II. Kiến trúc tổng thể 7 lớp logic
- **L1. Experience Layer**: Web • Mobile • Conversational UI • Voice • Merchant Portal • Admin
- **L2. AI Orchestration Layer**: Intent Router • Planner • Agent Registry • Context • Memory • Guardrails
- **L3. AI Agent Layer**: Shopping • Sales • Order • Support • Marketing • Inventory • Risk Agents
- **L4. Commerce Services Layer**: Catalog • Pricing • Inventory • Cart • Checkout • Order • Payment • Fulfillment • Returns
- **L5. Data & Intelligence Layer**: Transactional DB • Search Index • Vector DB • Event Streaming • Warehouse • Feature Store
- **L6. Integration Layer**: Payment Gateway • Logistics • ERP • CRM • Marketplace • ACP • UCP
- **L7. Security, Governance & Observability**: IAM • Policy Engine • Audit • Monitoring • AI Evaluation • Compliance (xuyên suốt L1–L6)

> **Nguyên tắc cốt lõi**: AI Agent không trực tiếp chỉnh sửa database đơn hàng, số dư hoặc tồn kho. AI phải gọi các nghiệp vụ được cấp quyền thông qua Tool Gateway và Commerce Services.

---

### III. Danh mục 16 Module Hệ Thống
1. **M01 — Identity & Customer**: Tài khoản, khách hàng, phân quyền, Customer 360, consent, quản lý phiên.
2. **M02 — Product & Catalog**: Sản phẩm, danh mục, thuộc tính, SKU, media, AI enrichment.
3. **M03 — AI Discovery**: Tìm kiếm ngữ nghĩa, tìm bằng ngôn ngữ tự nhiên, tìm bằng ảnh, so sánh sản phẩm.
4. **M04 — AI Shopping Assistant**: Hiểu ý định, duy trì ngữ cảnh, tư vấn giỏ hàng, hướng dẫn checkout.
5. **M05 — Pricing & Promotion**: Giá gốc, quy tắc giá, giá động, voucher, khuyến mãi, phê duyệt giá.
6. **M06 — Cart & Checkout**: Giỏ hàng, kiểm tra tính hợp lệ, tính báo giá checkout quote, xác nhận đơn.
7. **M07 — Order Management**: Quản lý vòng đời đơn hàng, tra cứu, hủy đơn, tách đơn, timeline.
8. **M08 — Payment & Settlement**: Khởi tạo payment intent, xử lý thanh toán, hoàn tiền, đối soát, kiểm soát rủi ro.
9. **M09 — Inventory & Fulfillment**: Quản lý tồn kho, giữ hàng (reservation), phân bổ kho, vận đơn.
10. **M10 — Customer Service**: AI FAQ, ticket, khiếu nại, phân tích cảm xúc, chuyển giao nhân viên.
11. **M11 — Merchant Management**: Đăng ký, xác minh nhà bán hàng, cấu hình shop, phí sàn, quyết toán.
12. **M12 — AI Marketing & Growth**: Phân khúc khách hàng, tạo chiến dịch, gợi ý cá nhân hóa, dự đoán churn.
13. **M13 — AI Agent Platform**: Quản lý agent, điều phối tác vụ, danh mục tool, bộ nhớ, guardrails, evaluation.
14. **M14 — Data & Analytics**: Thu thập sự kiện, pipeline dữ liệu, phân tích doanh thu, dự báo.
15. **M15 — Integration & Protocol**: API Gateway, Webhooks, cổng thanh toán ngoài, ACP/UCP Adapters.
16. **M16 — Administration & Governance**: Cấu hình hệ thống, RBAC/ABAC, quản lý chính sách, audit logs.

---

### IV. Hệ Thống 12 AI Agent Chuyên Biệt
| Agent | Trách nhiệm | Quyền công cụ | Mức tự chủ |
| :--- | :--- | :--- | :--- |
| **Shopping Agent** | Tìm và so sánh sản phẩm theo nhu cầu | Search, Catalog | L0 - L2 |
| **Sales Agent** | Tư vấn, gợi ý, thêm sửa giỏ hàng | Catalog, Cart, Pricing | L2 |
| **Checkout Agent** | Hướng dẫn chốt đơn, chuẩn bị thanh toán | Checkout, Shipping | L3 (Cần xác nhận) |
| **Order Agent** | Tra cứu trạng thái đơn, hỗ trợ đổi trả | Order, Fulfillment | L2 - L3 |
| **Support Agent** | Giải đáp thắc mắc, phân loại ticket | Knowledge, Ticket | L1 - L2 |
| **Return Agent** | Kiểm tra điều kiện hoàn trả theo chính sách | Order, Return, Policy | L2 - L3 |
| **Marketing Agent**| Đề xuất chiến dịch, phân khúc khách | Analytics, Campaign | L1 (Đề xuất) |
| **Inventory Agent**| Dự báo nhu cầu nhập hàng, cảnh báo tồn kho| Inventory, Forecast | L1 - L2 |
| **Pricing Agent**  | Đề xuất điều chỉnh giá tối ưu | Pricing, Analytics | L1 (Cần duyệt) |
| **Fraud Agent**    | Sàng lọc dấu hiệu gian lận thanh toán | Risk, Payment | L2 - L4 |
| **Merchant Agent** | Trợ lý hỗ trợ nhà bán hàng vận hành | Catalog, Merchant, Sales| L2 |
| **Analytics Agent**| Trích xuất báo cáo, phân tích KPI | Data, Reporting | L0 - L1 |

---

## PHẦN II — ĐẶC TẢ TRIỂN KHAI CHI TIẾT (FSD / DATA / API / QA)

### V. State Machine & Saga Giao Dịch
1. **Vòng đời Đơn hàng**:
   `PENDING_PAYMENT` ➔ `CONFIRMED` ➔ `PROCESSING` ➔ `SHIPPED` ➔ `DELIVERED` ➔ `COMPLETED`
   *(Nhánh lỗi: CANCELLED, DELIVERY_FAILED, RETURN_REQUESTED, RETURNED)*
2. **Saga Checkout An Toàn**:
   1. Khóa Quote (giá, phí vận chuyển, thuế, mã voucher) thành `quote_hash` có thời hạn (15 phút).
   2. Giữ tồn kho (`Stock Reservation`).
   3. Tạo đơn hàng trạng thái `PENDING_PAYMENT`.
   4. Khởi tạo `PaymentIntent`.
   5. Chờ xác thực thanh toán qua Webhook server-to-server (có chữ ký số).
   6. Commit đơn hàng và trừ tồn kho thực tế (`Consumed`).
   7. Ghi sự kiện vào Outbox Table (`Transactional Outbox Pattern`).

---

## PHẦN III — SCHEMA CƠ SỞ DỮ LIỆU POSTGRESQL (PHYSICAL BASELINE)

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1. Bảng Quotes (Báo giá đóng băng)
CREATE TABLE IF NOT EXISTS commerce_quotes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  customer_id uuid NOT NULL,
  cart_id uuid NOT NULL,
  quote_version integer NOT NULL DEFAULT 1,
  currency char(3) NOT NULL DEFAULT 'VND',
  subtotal_minor bigint NOT NULL CHECK(subtotal_minor >= 0),
  discount_minor bigint NOT NULL DEFAULT 0 CHECK(discount_minor >= 0),
  shipping_minor bigint NOT NULL DEFAULT 0 CHECK(shipping_minor >= 0),
  tax_minor bigint NOT NULL DEFAULT 0 CHECK(tax_minor >= 0),
  total_minor bigint NOT NULL CHECK(total_minor >= 0),
  fingerprint varchar(128) NOT NULL,
  expires_at timestamptz NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, id, quote_version),
  CHECK (total_minor = subtotal_minor - discount_minor + shipping_minor + tax_minor)
);

-- 2. Bảng Idempotency (Chống trùng lặp lệnh ghi)
CREATE TABLE IF NOT EXISTS commerce_idempotency (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  actor_id uuid NOT NULL,
  operation varchar(96) NOT NULL,
  request_key varchar(160) NOT NULL,
  request_hash char(64) NOT NULL,
  http_status integer,
  response_json jsonb,
  status varchar(20) NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  expires_at timestamptz NOT NULL,
  UNIQUE(tenant_id, actor_id, operation, request_key)
);

-- 3. Bảng Giữ Tồn Kho (Stock Reservations)
CREATE TABLE IF NOT EXISTS commerce_inventory_reservations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  quote_id uuid NOT NULL REFERENCES commerce_quotes(id),
  sku_id uuid NOT NULL,
  warehouse_id uuid NOT NULL,
  qty integer NOT NULL CHECK(qty > 0),
  status varchar(20) NOT NULL CHECK(status IN('ACTIVE','CONSUMED','RELEASED','EXPIRED')),
  expires_at timestamptz NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- 4. Bảng Outbox (Transactional Outbox cho Event-Driven)
CREATE TABLE IF NOT EXISTS commerce_outbox (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  aggregate_type varchar(64) NOT NULL,
  aggregate_id uuid NOT NULL,
  event_type varchar(120) NOT NULL,
  schema_version integer NOT NULL,
  payload jsonb NOT NULL,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  dispatched_at timestamptz,
  attempts integer NOT NULL DEFAULT 0
);

-- 5. Bảng Phê Duyệt Hành Động AI (Approval Gate)
CREATE TABLE IF NOT EXISTS ai_action_approvals (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  actor_id uuid NOT NULL,
  agent_run_id uuid NOT NULL,
  tool_name varchar(100) NOT NULL,
  action_hash char(64) NOT NULL,
  payload_json jsonb NOT NULL,
  status varchar(20) NOT NULL CHECK(status IN ('PENDING','APPROVED','REJECTED','EXPIRED','CONSUMED')),
  expires_at timestamptz NOT NULL,
  decided_by uuid,
  decided_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);
```

