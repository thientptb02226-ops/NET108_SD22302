# -*- coding: utf-8 -*-
"""
Script to insert 14 detailed UML Use Case diagrams into Section 2.2 (SRS)
of Lab1_NET108_AI_Native_Commerce.docx.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

DOC_PATH = r"C:\Net108Khai\Các Bài Lab\Lab1_NET108_AI_Native_Commerce.docx"
IMG_DIR = r"C:\Net108Khai\docs\06-design\use-cases"

USE_CASES_INFO = [
    {
        "kw": "2.2.1. Use Case 1: Đăng ký tài khoản",
        "file": "usecase_detail_uc01_register.png",
        "title": "UC01: Đăng ký tài khoản (Register)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả các ca sử dụng thành phần bắt buộc <<include>> (nhập liệu, kiểm tra hợp lệ, xác thực OTP) và các luồng mở rộng <<extend>> (Google OAuth, xử lý lỗi trùng lặp) của chức năng Đăng ký tài khoản:"
    },
    {
        "kw": "2.2.2. Use Case 2: Đăng nhập hệ thống",
        "file": "usecase_detail_uc02_login.png",
        "title": "UC02: Đăng nhập hệ thống (Login)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả quy trình xác thực Bcrypt Hash, cấp phát JWT Token (Access & Refresh Token) và các ca sử dụng mở rộng (Google SSO, Ghi nhớ đăng nhập):"
    },
    {
        "kw": "2.2.3. Use Case 3: Quên mật khẩu",
        "file": "usecase_detail_uc03_forgot_pwd.png",
        "title": "UC03: Quên mật khẩu (Forgot Password)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả chu trình xác minh danh tính qua Email OTP và thiết lập lại mật khẩu an toàn:"
    },
    {
        "kw": "2.2.4. Use Case 4: Tìm kiếm bằng ngôn ngữ tự nhiên",
        "file": "usecase_detail_uc04_nlp_search.png",
        "title": "UC04: Tìm kiếm bằng ngôn ngữ tự nhiên (NLP Search)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả tiến trình trích xuất ý định (Intent Extraction), chuyển đổi Vector Embedding và truy vấn tương đồng ngữ nghĩa trong CSDL pgvector/ChromaDB:"
    },
    {
        "kw": "2.2.5. Use Case 5: Tương tác với AI Shopping Assistant",
        "file": "usecase_detail_uc05_ai_assistant.png",
        "title": "UC05: Tương tác với AI Shopping Assistant",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả tương tác hai chiều giữa Khách hàng và Tác tử AI (Gemini LLM & RAG), hỗ trợ gợi ý sản phẩm và thêm trực tiếp vào giỏ hàng:"
    },
    {
        "kw": "2.2.6. Use Case 6: Quản lý giỏ hàng thông minh",
        "file": "usecase_detail_uc06_smart_cart.png",
        "title": "UC06: Quản lý giỏ hàng thông minh (Smart Cart)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả các thao tác quản lý giỏ hàng, đồng bộ tồn kho tức thì và các tính năng mở rộng của AI (gợi ý combo cross-sell, lưu mua sau):"
    },
    {
        "kw": "2.2.7. Use Case 7: Đặt hàng và áp dụng khuyến mãi tự động",
        "file": "usecase_detail_uc07_checkout.png",
        "title": "UC07: Đặt hàng và áp dụng khuyến mãi tự động (Checkout)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả luồng kiểm tra tồn kho (Hold Stock), tối ưu mã giảm giá tự động và khởi tạo đơn hàng PENDING:"
    },
    {
        "kw": "2.2.8. Use Case 8: Thanh toán trực tuyến",
        "file": "usecase_detail_uc08_payment.png",
        "title": "UC08: Thanh toán trực tuyến (Online Payment)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả luồng tích hợp cổng thanh toán trực tuyến (VNPay / MoMo / VietQR), xác thực Webhook IPN và cập nhật trạng thái đơn hàng:"
    },
    {
        "kw": "2.2.9. Use Case 9: Tra cứu đơn hàng và theo dõi vận chuyển",
        "file": "usecase_detail_uc09_order_tracking.png",
        "title": "UC09: Tra cứu đơn hàng và theo dõi vận chuyển",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả quá trình đồng bộ vận đơn thời gian thực với đối tác giao nhận (GHN / GHTK) và gửi phản hồi đánh giá sau nhận hàng:"
    },
    {
        "kw": "2.2.10. Use Case 10: Quản lý danh mục & sản phẩm chuẩn hóa cho AI",
        "file": "usecase_detail_uc10_product_mgmt.png",
        "title": "UC10: Quản lý sản phẩm & Chuẩn hóa AI (Product Management)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả nghiệp vụ quản lý sản phẩm của Merchant/Admin, tự động sinh Vector Embeddings và Metadata phục vụ tìm kiếm ngữ nghĩa:"
    },
    {
        "kw": "2.2.11. Use Case 11: Quản lý đơn hàng và trạng thái đơn hàng",
        "file": "usecase_detail_uc11_order_mgmt.png",
        "title": "UC11: Quản lý và xử lý đơn hàng (Order Management)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả quy trình tiếp nhận, xác nhận, chuyển trạng thái đóng gói, đẩy vận đơn sang đơn vị vận chuyển và xử lý đổi trả:"
    },
    {
        "kw": "2.2.12. Use Case 12: Quản lý tài khoản và phân quyền RBAC",
        "file": "usecase_detail_uc12_rbac_mgmt.png",
        "title": "UC12: Quản lý tài khoản và phân quyền RBAC (Security)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả các chức năng quản trị cấp cao: gán vai trò người dùng, thiết lập ma trận quyền hạn và giám sát nhật ký kiểm toán (Audit Logs):"
    },
    {
        "kw": "2.2.13. Use Case 13: Báo cáo thống kê và phân tích hành vi AI",
        "file": "usecase_detail_uc13_analytics.png",
        "title": "UC13: Báo cáo thống kê & Phân tích hành vi AI (Analytics)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả các báo cáo doanh thu, tồn kho và các chỉ số đo lường hiệu quả chuyển đổi của AI Shopping Assistant:"
    },
    {
        "kw": "2.2.14. Use Case 14: Thực thi giao dịch qua giao thức tác tử AI",
        "file": "usecase_detail_uc14_ai_agent_tx.png",
        "title": "UC14: Thực thi giao dịch qua giao thức tác tử AI (Agentic Protocol)",
        "intro": "Sơ đồ Use Case chi tiết dưới đây mô tả quy trình thực thi giao dịch tự hành của External AI Agent qua Agentic Protocol, kiểm duyệt an toàn qua AI Guardrails và cơ chế Human-in-the-loop:"
    }
]

def main():
    print("Loading document:", DOC_PATH)
    doc = docx.Document(DOC_PATH)

    # 1. First, renumber existing figures 6 to 12 -> 20 to 26
    print("Renumbering existing subsequent figures (Hình 6..12 -> Hình 20..26)...")
    renumber_map = {
        "Hình 6. Sơ đồ mô hình quan hệ thực thể": "Hình 20. Sơ đồ mô hình quan hệ thực thể",
        "Hình 7. Sơ đồ triển khai hệ thống": "Hình 21. Sơ đồ triển khai hệ thống",
        "Hình 8. Sơ đồ tổ chức của ứng dụng": "Hình 22. Sơ đồ tổ chức của ứng dụng",
        "Hình 9. Sơ đồ phân tầng mô hình công nghệ": "Hình 23. Sơ đồ phân tầng mô hình công nghệ",
        "Hình 10. Thiết kế giao diện (UI Wireframe) các chức năng dùng chung": "Hình 24. Thiết kế giao diện (UI Wireframe) các chức năng dùng chung",
        "Hình 11. Thiết kế giao diện (UI Wireframe) phân hệ Khách hàng": "Hình 25. Thiết kế giao diện (UI Wireframe) phân hệ Khách hàng & Mua sắm AI",
        "Hình 12. Thiết kế giao diện (UI Wireframe) phân hệ Quản trị": "Hình 26. Thiết kế giao diện (UI Wireframe) phân hệ Quản trị & Nhà bán hàng",
    }

    for p in doc.paragraphs:
        t = p.text.strip()
        for old_prefix, new_prefix in renumber_map.items():
            if t.startswith(old_prefix):
                p.text = t.replace(old_prefix, new_prefix)
                # Re-apply italic styling and font
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(11)
                    r.font.italic = True
                    r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                print(f"  Renumbered: {old_prefix[:25]}... -> {new_prefix[:25]}...")
                break

    # 2. Insert the 14 Use Case diagrams into Section 2.2
    print("Inserting 14 detailed Use Case diagrams into Section 2.2...")
    for idx, uc_info in enumerate(USE_CASES_INFO):
        fig_num = 6 + idx
        kw = uc_info["kw"]
        img_file = os.path.join(IMG_DIR, uc_info["file"])

        # Find heading paragraph
        heading_p = None
        for p in doc.paragraphs:
            if kw in p.text:
                heading_p = p
                break

        if not heading_p:
            print(f"  WARNING: Could not find heading for {kw}!")
            continue

        # We will insert:
        # 1. intro_p
        # 2. img_p
        # 3. caption_p
        # right after heading_p
        
        # Create paragraphs
        intro_p = doc.add_paragraph()
        intro_p.paragraph_format.space_before = Pt(4)
        intro_p.paragraph_format.space_after = Pt(4)
        intro_p.paragraph_format.line_spacing = 1.15
        r_intro = intro_p.add_run(uc_info["intro"])
        r_intro.font.name = "Times New Roman"
        r_intro.font.size = Pt(11.5)
        r_intro.font.italic = True
        r_intro.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

        img_p = doc.add_paragraph()
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.paragraph_format.space_before = Pt(4)
        img_p.paragraph_format.space_after = Pt(2)
        r_img = img_p.add_run()
        r_img.add_picture(img_file, width=Inches(5.8))

        caption_p = doc.add_paragraph()
        caption_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption_p.paragraph_format.space_before = Pt(2)
        caption_p.paragraph_format.space_after = Pt(8)
        caption_text = f"Hình {fig_num}. Sơ đồ Use Case chi tiết {uc_info['title']}"
        r_cap = caption_p.add_run(caption_text)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(11)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

        # Move paragraphs in XML to immediately follow heading_p
        # heading_p -> intro_p -> img_p -> caption_p
        heading_p._p.addnext(intro_p._p)
        intro_p._p.addnext(img_p._p)
        img_p._p.addnext(caption_p._p)

        print(f"  Inserted Hình {fig_num} for {uc_info['title']}")

    print("Saving updated document to:", DOC_PATH)
    doc.save(DOC_PATH)
    print("=== FINISHED INSERTING ALL 14 USE CASE DIAGRAMS SUCCESSFULLY! ===")

if __name__ == "__main__":
    main()
