# -*- coding: utf-8 -*-
"""
Script to update Lab 1 NET108 AI-Native Commerce report:
1. Replace 4 existing Use Case diagram images with the new 28-UC diagrams
2. Populate 2.1.5 with the full 28 categorized functions
3. Insert Conceptual ERD diagram into Section 2.3.1
4. Append Chapter 3: THIẾT KẾ HỆ THỐNG with 3.1 & 3.2, all diagrams, and 3 Controller tables formatted to user standard
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DOC_PATH = r"C:\Net108Khai\Các Bài Lab\Lab1_NET108_AI_Native_Commerce.docx"
DESIGN_DIR = r"C:\Net108Khai\docs\06-design"
UC_DIR = os.path.join(DESIGN_DIR, "use-cases")

def set_cell_properties(cell, fill_hex="FFFFFF", bold=False, align="left", font_size=10, text="", width_dxa=None):
    tcPr = cell._tc.get_or_add_tcPr()
    # Width
    if width_dxa:
        w_xml = f'<w:tcW {nsdecls("w")} w:w="{width_dxa}" w:type="dxa"/>'
        tcPr.append(parse_xml(w_xml))
    # Borders
    b_xml = f'''<w:tcBorders {nsdecls("w")}>
        <w:top w:val="single" w:color="000000" w:sz="4" w:space="0"/>
        <w:left w:val="single" w:color="000000" w:sz="4" w:space="0"/>
        <w:bottom w:val="single" w:color="000000" w:sz="4" w:space="0"/>
        <w:right w:val="single" w:color="000000" w:sz="4" w:space="0"/>
    </w:tcBorders>'''
    tcPr.append(parse_xml(b_xml))
    # Shading
    s_xml = f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{fill_hex}"/>'
    tcPr.append(parse_xml(s_xml))
    # Padding
    m_xml = f'''<w:tcMar {nsdecls("w")}>
        <w:top w:w="80" w:type="dxa"/>
        <w:left w:w="120" w:type="dxa"/>
        <w:bottom w:w="80" w:type="dxa"/>
        <w:right w:w="120" w:type="dxa"/>
    </w:tcMar>'''
    tcPr.append(parse_xml(m_xml))

    # Text formatting
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)

def create_styled_table(doc, headers, rows_data, col_widths, table_num, table_caption):
    # Caption paragraph
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(8)
    p_cap.paragraph_format.space_after = Pt(4)
    run_cap = p_cap.add_run(f"Bảng {table_num}. {table_caption}")
    run_cap.font.name = "Times New Roman"
    run_cap.font.size = Pt(11)
    run_cap.font.bold = True
    run_cap.font.color.rgb = RGBColor(31, 78, 121)

    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    tblPr.append(parse_xml(f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>'))

    # Header Row
    hdr_row = table.rows[0]
    hdr_row._tr.get_or_add_trPr().append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    hdr_row._tr.get_or_add_trPr().append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    for col_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[col_idx]
        w_dxa = col_widths[col_idx]
        set_cell_properties(cell, fill_hex="B8CCE4", bold=True, align="center", font_size=10.5, text=h_text, width_dxa=w_dxa)

    # Data Rows
    for r_idx, row_vals in enumerate(rows_data):
        row = table.rows[r_idx + 1]
        row._tr.get_or_add_trPr().append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        fill_hex = "FFFFFF" if r_idx % 2 == 0 else "F7FAFD"
        for col_idx, val in enumerate(row_vals):
            cell = row.cells[col_idx]
            w_dxa = col_widths[col_idx]
            # align center for col 0, 2; left for others
            al = "center" if col_idx in [0, 2] else "left"
            set_cell_properties(cell, fill_hex=fill_hex, bold=False, align=al, font_size=10, text=val, width_dxa=w_dxa)

    # Empty spacing paragraph after table
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(2)
    p_after.paragraph_format.space_after = Pt(6)

def add_styled_heading(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    pPr = p._p.get_or_add_pPr()

    # Style ID & Outline Level
    if level == 1:
        # Chapter title
        pPr.append(parse_xml(f'<w:pStyle {nsdecls("w")} w:val="3"/>'))
        pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="1"/>'))
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(31, 78, 121)
    elif level == 2:
        # Section (3.1, 3.2)
        pPr.append(parse_xml(f'<w:pStyle {nsdecls("w")} w:val="4"/>'))
        pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="2"/>'))
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(31, 78, 121)
    elif level == 3:
        # Sub-section (3.1.1, 3.2.1)
        pPr.append(parse_xml(f'<w:pStyle {nsdecls("w")} w:val="5"/>'))
        pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="3"/>'))
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_body_paragraph(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_image_with_caption(doc, img_path, caption_text, width_inches=6.0):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(8)
    run_cap = p_cap.add_run(caption_text)
    run_cap.font.name = "Times New Roman"
    run_cap.font.size = Pt(10.5)
    run_cap.font.italic = True
    run_cap.font.color.rgb = RGBColor(50, 60, 75)

def main():
    print("Loading document:", DOC_PATH)
    doc = docx.Document(DOC_PATH)

    # 1. Replace 4 existing Use Case images with 28-UC diagrams
    print("Replacing 4 existing Use Case diagram image blobs...")
    img_map = {
        "rId10": os.path.join(UC_DIR, "usecase_ainative_tongquat.png"),
        "rId11": os.path.join(UC_DIR, "usecase_ainative_customer.png"),
        "rId12": os.path.join(UC_DIR, "usecase_ainative_admin.png"),
        "rId13": os.path.join(UC_DIR, "usecase_ainative_agent.png"),
    }
    for rId, path in img_map.items():
        if rId in doc.part.related_parts:
            part = doc.part.related_parts[rId]
            with open(path, "rb") as f:
                part._blob = f.read()
            print(f"Updated {rId} ({part.partname}) from {path}")

    # 2. Update 2.1.5 Actor Function lists in paragraphs 113, 115, 117, 119
    print("Populating 2.1.5 categorized Use Case lists...")
    p113 = doc.paragraphs[113]
    p113.text = (
        "• UC01: Đăng ký tài khoản mới (xác thực email kích hoạt & OTP).\n"
        "• UC02: Đăng nhập hệ thống & cấp phát JWT Session an toàn.\n"
        "• UC03: Quên mật khẩu / khôi phục tài khoản qua OTP email bảo mật.\n"
        "• UC04: Tìm kiếm sản phẩm bằng ngôn ngữ tự nhiên (NLP Semantic Hybrid Search).\n"
        "• UC05: Xem thông tin chi tiết & so sánh thông số kỹ thuật sản phẩm thông minh."
    )
    p113.paragraph_format.line_spacing = 1.15
    for r in p113.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    p115 = doc.paragraphs[115]
    p115.text = (
        "• UC06: Quản lý thông tin hồ sơ cá nhân & danh bạ sổ địa chỉ nhận hàng.\n"
        "• UC07: Mua sắm hội thoại với Trợ lý AI (AI Shopping Assistant & Intent Router).\n"
        "• UC08: Quản lý danh sách sản phẩm yêu thích (Wishlist cá nhân hóa).\n"
        "• UC09: Quản lý giỏ hàng thông minh (Smart Cart với cơ chế giữ tồn kho 15 phút).\n"
        "• UC10: Đặt hàng và tự động áp dụng mã giảm giá / Voucher tối ưu (Checkout Saga).\n"
        "• UC11: Thanh toán trực tuyến an toàn qua Cổng thanh toán điện tử VNPay / MoMo.\n"
        "• UC12: Tra cứu lịch sử đơn hàng và theo dõi hành trình vận chuyển thời gian thực.\n"
        "• UC13: Đánh giá, nhận xét sản phẩm và xem tóm tắt cảm xúc người dùng bằng AI.\n"
        "• UC14: Gửi yêu cầu đổi trả hàng & hoàn tiền thông minh tự động (AI Returns)."
    )
    p115.paragraph_format.line_spacing = 1.15
    for r in p115.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    p117 = doc.paragraphs[117]
    p117.text = (
        "• UC15: Quản lý danh mục & sản phẩm chuẩn hóa cho AI (tự động sinh Vector Embeddings).\n"
        "• UC16: Quản lý kho hàng & kiểm soát ngưỡng cảnh báo hết hàng tồn kho tự động.\n"
        "• UC17: Quản lý danh sách đơn hàng & điều phối trạng thái vận chuyển qua hãng ship.\n"
        "• UC18: Quản lý chương trình khuyến mãi, Voucher giảm giá & chiến dịch Flash Sale.\n"
        "• UC19: Quản lý tài khoản người dùng, phân quyền truy cập RBAC và bảo mật phiên.\n"
        "• UC20: Cấu hình Prompt hệ thống, hàng rào an toàn Guardrails và tiêu chuẩn kiểm duyệt AI.\n"
        "• UC21: Báo cáo thống kê doanh thu, lưu lượng và phân tích hành vi mua sắm AI.\n"
        "• UC22: Quản lý tỷ lệ hoa hồng, bảng kê thanh toán và đối soát doanh thu nhà bán."
    )
    p117.paragraph_format.line_spacing = 1.15
    for r in p117.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    p119 = doc.paragraphs[119]
    p119.text = (
        "• UC23: Tự động phân tích sở thích và gợi ý sản phẩm cá nhân hóa (Personalized Ranking).\n"
        "• UC24: Điều phối tác tử tự hành phân tán giải quyết tác vụ (Multi-Agent Orchestration).\n"
        "• UC25: Truy xuất tri thức & bộ nhớ ngữ cảnh hội thoại RAG (Vector Semantic Retrieval).\n"
        "• UC26: Thực thi giao dịch tự động qua giao thức thương mại tác tử (Agentic Commerce Protocol - ACP).\n"
        "• UC27: Giám sát hàng rào an toàn Guardrails, kiểm soát hạn mức giao dịch và kích hoạt 2FA OTP.\n"
        "• UC28: Ghi nhật ký kiểm toán hành vi AI (Audit Log) và giám sát chi phí tiêu thụ Token LLM."
    )
    p119.paragraph_format.line_spacing = 1.15
    for r in p119.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    # 3. Insert Conceptual ERD image after Section 2.3.1 (before TÀI LIỆU THAM KHẢO)
    # Find paragraph of 2.3.1
    print("Inserting Conceptual ERD diagram into section 2.3.1...")
    # We will insert Chapter 3 right before TÀI LIỆU THAM KHẢO
    # Let's find index of TÀI LIỆU THAM KHẢO
    ref_idx = None
    for i, p in enumerate(doc.paragraphs):
        if "TÀI LIỆU THAM KHẢO" in p.text:
            ref_idx = i
            break
    print("Found TÀI LIỆU THAM KHẢO at paragraph index:", ref_idx)

    # First add Conceptual ERD image before Chapter 3
    # We can add ERD image right after paragraph 158
    p158 = doc.paragraphs[158]
    # We can insert using add_image_with_caption at the end, but let's see how paragraphs are structured
    # Instead of messy insertion before ref_idx, we can save reference paragraphs, remove them, add our content, and re-add reference paragraphs!
    ref_paras_data = []
    for i in range(ref_idx, len(doc.paragraphs)):
        ref_paras_data.append((doc.paragraphs[i].text, doc.paragraphs[i].style.name))

    # Truncate doc paragraphs from ref_idx onwards
    for i in range(len(doc.paragraphs) - 1, ref_idx - 1, -1):
        p_elem = doc.paragraphs[i]._p
        p_elem.getparent().remove(p_elem)

    # Now we are at the end of section 2.3.1!
    # Add Conceptual ERD diagram
    add_image_with_caption(
        doc,
        os.path.join(DESIGN_DIR, "erd_ainative_conceptual.png"),
        "Hình 6. Sơ đồ mô hình quan hệ thực thể mức khái niệm (Conceptual ERD)",
        width_inches=6.2
    )

    # ==========================================================================
    # 4. CHƯƠNG 3: THIẾT KẾ HỆ THỐNG
    # ==========================================================================
    print("Appending CHƯƠNG 3: THIẾT KẾ HỆ THỐNG...")
    add_styled_heading(doc, "CHƯƠNG 3: THIẾT KẾ HỆ THỐNG", level=1)

    # --- 3.1 Thiết kế tổng thể ---
    add_styled_heading(doc, "3.1. Thiết kế tổng thể", level=2)
    add_body_paragraph(
        doc,
        "Thiết kế tổng thể hệ thống AI-Native Commerce tập trung vào tính mô đun hóa cao, khả năng mở rộng linh hoạt "
        "(Scalability), và sự phân tách độc lập giữa tầng giao diện trải nghiệm, tầng xử lý nghiệp vụ giao dịch và tầng trí tuệ nhân tạo (AI Engine). "
        "Mô hình kiến trúc tổng thể đáp ứng đầy đủ các tiêu chuẩn vận hành doanh nghiệp với độ sẵn sàng cao (High Availability), an toàn dữ liệu tuyệt đối và "
        "khả năng tích hợp đa kênh thông suốt."
    )

    # 3.1.1 Deploy Diagram
    add_styled_heading(doc, "3.1.1. Sơ đồ triển khai (Deploy Diagram)", level=3)
    add_body_paragraph(
        doc,
        "Hệ thống áp dụng kiến trúc triển khai container hóa hoàn chỉnh trên nền tảng Docker Compose Production Host. "
        "Mô hình triển khai bao gồm 5 tầng vật lý và dịch vụ tách biệt: (1) Tầng thiết bị đầu cuối Client Tier (Web Next.js, Desktop Electron, AI Widget); "
        "(2) Tầng cổng biên Edge & Reverse Proxy Nginx đảm nhiệm cân bằng tải, chấm dứt SSL/TLS và giới hạn tốc độ Rate Limiting; "
        "(3) Tầng dịch vụ lõi Core API (.NET 8 / Express) xử lý giao dịch Saga và xác thực JWT; "
        "(4) Tầng AI & Agent Microservice (FastAPI, Python) tích hợp các mô hình ngôn ngữ lớn (LLM) và Vector Embeddings; và "
        "(5) Tầng lưu trữ phân tán bao gồm PostgreSQL 16 (quan hệ ACID), Redis 7 (Cache/Session/Queue), ChromaDB (Vector Store) và MinIO (S3 Object Storage). "
        "Ngoài ra, hệ thống tích hợp các cổng thanh toán ngoài (VNPay Sandbox) và giao diện API đám mây bảo mật."
    )
    add_image_with_caption(
        doc,
        os.path.join(DESIGN_DIR, "deploy_diagram.png"),
        "Hình 7. Sơ đồ triển khai hệ thống (Deployment Diagram)",
        width_inches=6.2
    )

    # 3.1.2 Appmap
    add_styled_heading(doc, "3.1.2. Sơ đồ tổ chức của ứng dụng (Appmap)", level=3)
    add_body_paragraph(
        doc,
        "Sơ đồ tổ chức ứng dụng (Appmap / Sitemap Navigation Flow) phản ánh cấu trúc phân cấp điều hướng màn hình và luồng thao tác của người dùng. "
        "Từ Cổng chính (Homepage Portal), hệ thống rẽ nhánh thành 4 phân hệ chính: (1) Phân hệ Dùng chung (Đăng nhập, Đăng ký, Tìm kiếm NLP); "
        "(2) Phân hệ Khách hàng & Mua sắm (AI Shopping Assistant, Giỏ hàng thông minh, Checkout Saga, Tra cứu đơn); "
        "(3) Phân hệ Nhà bán hàng (Merchant Hub quản lý sản phẩm, tồn kho, đơn hàng, đối soát); và "
        "(4) Phân hệ Quản trị viên (Admin Portal giám sát KPI, phân quyền RBAC và cấu hình hàng rào an toàn AI Guardrails)."
    )
    add_image_with_caption(
        doc,
        os.path.join(DESIGN_DIR, "appmap_diagram.png"),
        "Hình 8. Sơ đồ tổ chức của ứng dụng (Appmap / Sitemap Navigation Flow)",
        width_inches=6.2
    )

    # 3.1.3 Tech Stack
    add_styled_heading(doc, "3.1.3. Mô hình công nghệ", level=3)
    add_body_paragraph(
        doc,
        "Hệ sinh thái công nghệ của đề tài được cấu trúc thành 5 tầng phân tầng chuẩn mực công nghiệp: "
        "(1) Tầng trải nghiệm người dùng (Experience Layer) sử dụng Next.js 14, React 19, TailwindCSS, Zustand và Lucide Icons; "
        "(2) Tầng cổng truyền thông và bảo mật (API Gateway & Security Layer) với Nginx, JWT, CORS Policy và Model Context Protocol (MCP); "
        "(3) Tầng dịch vụ lõi (Application Core Layer) vận hành trên ASP.NET Core 8 / Express, Checkout Saga Coordinator, Idempotency Engine và VNPay SDK; "
        "(4) Tầng trí tuệ nhân tạo (AI & Intelligence Layer) với Python FastAPI, Google Gemini 1.5 Pro, LangChain Hybrid Search và Agentic Commerce Protocol (ACP); "
        "và (5) Tầng lưu trữ & hạ tầng (Persistence & Infrastructure Layer) với PostgreSQL 16, Redis In-Memory, ChromaDB Vector DB và Docker Compose."
    )
    add_image_with_caption(
        doc,
        os.path.join(DESIGN_DIR, "tech_stack_diagram.png"),
        "Hình 9. Sơ đồ phân tầng mô hình công nghệ (Tech Stack Architecture)",
        width_inches=6.2
    )

    # --- 3.2 Thiết kế UI và Controller ---
    add_styled_heading(doc, "3.2. Thiết kế UI (giao diện) và Controller (tương tác)", level=2)
    add_body_paragraph(
        doc,
        "Thiết kế giao diện người dùng (UI Wireframe) và bộ điều khiển tương tác (Controller) xác định chi tiết cách thức người dùng tương tác với hệ thống, "
        "các endpoint API được kích hoạt, các lớp Controller tiếp nhận xử lý và luồng dữ liệu phản hồi tương ứng. "
        "Mỗi phân hệ được trang bị ma trận đặc tả Controller kết hợp bản vẽ Mockup giao diện trực quan."
    )

    # 3.2.1 Shared UI & Controller
    add_styled_heading(doc, "3.2.1. Thiết kế các chức năng dùng chung", level=3)
    add_body_paragraph(
        doc,
        "Các chức năng dùng chung phục vụ cho cả khách vãng lai (Guest) và người dùng đã xác thực (Customer/Merchant/Admin). "
        "Bao gồm quy trình xác thực người dùng (Đăng ký, Đăng nhập JWT, Quên mật khẩu OTP) và cổng Tìm kiếm sản phẩm thông minh bằng ngôn ngữ tự nhiên (NLP Search)."
    )

    # Table 24: Shared Controllers
    headers_t24 = ["Mã CTL", "Tên chức năng", "Phương thức & Endpoint", "Controller xử lý", "Luồng dữ liệu & Phản hồi"]
    widths_t24 = [1000, 1600, 2100, 1800, 2400]
    rows_t24 = [
        ["CTL-01", "Đăng ký tài khoản", "POST /api/v1/auth/register", "AuthController.Register()", "Kiểm tra email trùng lặp, mã hóa mật khẩu với BCrypt, sinh verification token, gửi email kích hoạt, trả về mã HTTP 201 Created."],
        ["CTL-02", "Đăng nhập hệ thống", "POST /api/v1/auth/login", "AuthController.Login()", "Xác thực email/password, kiểm tra khóa tài khoản, tạo cặp Access Token (JWT 15p) và Refresh Token (7 ngày), trả về HTTP 200 OK kèm vai trò RBAC."],
        ["CTL-03", "Quên / Reset mật khẩu", "POST /api/v1/auth/forgot-password", "AuthController.ForgotPassword()", "Sinh mã OTP ngẫu nhiên 6 chữ số, lưu vào Redis với TTL 5 phút, gửi email chứa liên kết khôi phục, trả về HTTP 200 OK."],
        ["CTL-04", "Tìm kiếm NLP / Hybrid", "POST /api/v1/search/hybrid", "SearchController.HybridSearch()", "Vector hóa câu hỏi người dùng qua AI Embedding, truy vấn đồng thời Vector DB (ChromaDB) và Text DB (Postgres), rerank kết quả, trả về HTTP 200 danh sách SP."]
    ]
    create_styled_table(doc, headers_t24, rows_t24, widths_t24, 24, "Bảng thiết kế Controller và Luồng tương tác các chức năng dùng chung")

    add_image_with_caption(
        doc,
        os.path.join(DESIGN_DIR, "ui_wireframe_shared.png"),
        "Hình 10. Thiết kế giao diện (UI Wireframe) các chức năng dùng chung",
        width_inches=6.2
    )

    # 3.2.2 Customer UI & Controller
    add_styled_heading(doc, "3.2.2. Thiết kế các chức năng dành cho khách hàng và bán hàng", level=3)
    add_body_paragraph(
        doc,
        "Phân hệ khách hàng và quy trình bán hàng tập trung vào trải nghiệm mua sắm hội thoại với Trợ lý AI (Conversational Commerce), "
        "quản lý giỏ hàng thông minh có cơ chế giữ hàng tự động (Stock Reservation), quy trình Checkout Saga an toàn chống bán quá tồn kho và cổng thanh toán VNPay."
    )

    # Table 25: Customer Controllers
    headers_t25 = ["Mã CTL", "Tên chức năng", "Phương thức & Endpoint", "Controller xử lý", "Luồng dữ liệu & Phản hồi"]
    widths_t25 = [1000, 1600, 2100, 1800, 2400]
    rows_t25 = [
        ["CTL-05", "Tương tác AI Assistant", "POST /api/v1/assistant/chat", "AssistantController.SendMessage()", "Nhận diện Intent, truy xuất ngữ cảnh lịch sử từ Redis, kích hoạt Gemini 1.5 Pro, đề xuất sản phẩm kèm lý do gợi ý và voucher độc quyền."],
        ["CTL-06", "Quản lý Smart Cart", "POST /api/v1/cart/items", "CartController.AddItem()", "Kiểm tra tồn kho thời gian thực, tạm khóa số lượng trong 15 phút, tính toán lại tổng tiền và khuyến mãi, trả về Cart DTO cập nhật."],
        ["CTL-07", "Khởi tạo Checkout Saga", "POST /api/v1/checkout/saga", "CheckoutController.StartSaga()", "Kiểm tra Idempotency Key, kích hoạt điều phối Saga: Khóa tồn kho -> Tạo bản ghi Order Pending -> Áp dụng mã Voucher, trả về CheckoutQuote."],
        ["CTL-08", "Thanh toán VNPay", "POST /api/v1/payment/vnpay-url", "PaymentController.CreateVNPayUrl()", "Ký số checksum HMAC-SHA512 với bí mật merchant, sinh URL chuyển hướng khách hàng sang cổng thanh toán trực tuyến VNPay."],
        ["CTL-09", "Tra cứu đơn hàng", "GET /api/v1/orders/{orderId}", "OrderController.GetOrderDetail()", "Xác thực quyền sở hữu Customer, đọc trạng thái đơn hàng và nhật ký Saga từ DB, trả về lộ trình vận chuyển và mã vận đơn shipper."]
    ]
    create_styled_table(doc, headers_t25, rows_t25, widths_t25, 25, "Bảng thiết kế Controller và Luồng tương tác phân hệ Khách hàng & Bán hàng")

    add_image_with_caption(
        doc,
        os.path.join(DESIGN_DIR, "ui_wireframe_customer.png"),
        "Hình 11. Thiết kế giao diện (UI Wireframe) phân hệ Khách hàng & Mua sắm AI",
        width_inches=6.2
    )

    # 3.2.3 Admin UI & Controller
    add_styled_heading(doc, "3.2.3. Thiết kế các chức năng dành cho nhân viên quản lý", level=3)
    add_body_paragraph(
        doc,
        "Phân hệ quản trị dành cho Merchant và Quản trị viên sàn (Admin) cung cấp bộ công cụ điều hành toàn diện: "
        "Dashboard chỉ số KPI thời gian thực, quản lý vòng đời sản phẩm chuẩn hóa AI (tự động sinh Vector Embedding), "
        "quản lý đơn hàng Checkout Saga và đặc biệt là hệ thống kiểm soát hàng rào an toàn AI (Guardrails Policy & Token Budget)."
    )

    # Table 26: Admin Controllers
    headers_t26 = ["Mã CTL", "Tên chức năng", "Phương thức & Endpoint", "Controller xử lý", "Luồng dữ liệu & Phản hồi"]
    widths_t26 = [1000, 1600, 2100, 1800, 2400]
    rows_t26 = [
        ["CTL-10", "Dashboard KPI Tổng quan", "GET /api/v1/admin/analytics/kpi", "AdminAnalyticsController.GetKPIs()", "Tổng hợp doanh thu thuần, tỷ lệ chuyển đổi chốt đơn của AI, số lượng đơn Saga thành công và ngân sách token LLM tiêu thụ."],
        ["CTL-11", "Quản lý Sản phẩm & SKU", "POST /api/v1/merchant/products", "MerchantProductController.CreateProduct()", "Xác thực quyền Merchant, lưu trữ DB Postgres, phát sinh sự kiện ProductCreated sinh Vector Embeddings nạp vào ChromaDB."],
        ["CTL-12", "Quản lý Kho & Tồn kho", "PUT /api/v1/merchant/inventory", "InventoryController.UpdateStock()", "Cập nhật số lượng khả dụng, điều chỉnh hạn mức an toàn, kích hoạt cảnh báo hết hàng tự động gửi thông báo qua email/SMS."],
        ["CTL-13", "Cấu hình AI Guardrails", "PUT /api/v1/admin/ai/guardrails", "AIGovernanceController.UpdatePolicies()", "Cập nhật hạn mức giao dịch tự động tối đa của Agent, bật/tắt chính sách 2FA OTP, cấu hình prompt injection filters và whitelist tools."],
        ["CTL-14", "Đối soát hoa hồng Merchant", "GET /api/v1/admin/settlements", "SettlementController.GetSummary()", "Tính toán doanh số thực thu, khấu trừ phí hoa hồng sàn (Commission), lập bảng kê thanh toán kỳ và xuất hóa đơn điện tử VAT."]
    ]
    create_styled_table(doc, headers_t26, rows_t26, widths_t26, 26, "Bảng thiết kế Controller và Luồng tương tác phân hệ Quản trị & Nhà bán")

    add_image_with_caption(
        doc,
        os.path.join(DESIGN_DIR, "ui_wireframe_admin.png"),
        "Hình 12. Thiết kế giao diện (UI Wireframe) phân hệ Quản trị & Nhà bán hàng",
        width_inches=6.2
    )

    # Re-append TÀI LIỆU THAM KHẢO
    print("Re-appending TÀI LIỆU THAM KHẢO...")
    for t_text, s_name in ref_paras_data:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.15
        if "TÀI LIỆU THAM KHẢO" in t_text:
            p_ref.paragraph_format.space_before = Pt(14)
            p_ref.paragraph_format.space_after = Pt(6)
            run = p_ref.add_run(t_text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(31, 78, 121)
        else:
            run = p_ref.add_run(t_text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0, 0, 0)

    print("Saving document to:", DOC_PATH)
    doc.save(DOC_PATH)
    print("=== SUCESSFULLY UPDATED LAB 1 DOCUMENT! ===")

if __name__ == "__main__":
    main()

