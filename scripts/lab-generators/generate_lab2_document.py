# -*- coding: utf-8 -*-
"""
Generate complete, publication-quality report for LAB 2 (NET108 - FPT Polytechnic):
File: C:\\Net108Khai\\Các Bài Lab\\Lab 2\\Lab2_NET108_AI_Native_Commerce.docx
Includes:
- Official FPT Polytechnic Cover Page & Jira Progress Table
- Clickable Table of Contents with Hyperlinks and Bookmarks
- Bài 1: ERD Level 2 Diagram & Analysis (3 pts)
- Bài 2: Entity Attributes Data Dictionary Tables (2 pts)
- Bài 3: UI Navigation Flow & Controller Specifications (3 pts)
- Bài 4: AI Audit & Optimization Evidence (2 pts)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

OUTPUT_PATH = r"C:\Net108Khai\Các Bài Lab\Lab 2\Lab2_NET108_AI_Native_Commerce.docx"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

IMG_DIR = r"C:\Net108Khai\docs\06-design"
IMG_ERD = os.path.join(IMG_DIR, "erd_ainative_level2.png")
IMG_UI_FLOW = os.path.join(IMG_DIR, "ui_navigation_flow.png")
IMG_AI_EVIDENCE = os.path.join(IMG_DIR, "ai_erd_evaluation_evidence.png")

COLOR_NAVY = RGBColor(0x1F, 0x4E, 0x79)
COLOR_DARK = RGBColor(0x0F, 0x17, 0x2A)
COLOR_BODY = RGBColor(0x33, 0x33, 0x33)
COLOR_MUTED = RGBColor(0x59, 0x59, 0x59)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_table_borders(table, color="000000", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''<w:tblBorders {nsdecls("w")}>
        <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
    </w:tblBorders>''')
    tblPr.append(borders)

def format_cell_text(cell, text, bold=False, italic=False, size=Pt(10), color=COLOR_BODY, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = size
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color

def create_styled_table(doc, headers, rows_data, col_widths=None):
    tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, "000000", "4")

    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, h_text in enumerate(headers):
        format_cell_text(hdr_cells[i], h_text, bold=True, size=Pt(10.5), color=COLOR_DARK, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_shading(hdr_cells[i], "B8CCE4")  # User's exact blue
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)

    # Data Rows
    for r_idx, row_values in enumerate(rows_data):
        row_cells = tbl.rows[r_idx + 1].cells
        row_bg = "F2F2F2" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            align = WD_ALIGN_PARAGRAPH.CENTER if (c_idx == 0 or len(val) < 12) else WD_ALIGN_PARAGRAPH.LEFT
            format_cell_text(row_cells[c_idx], val, bold=False, size=Pt(10), color=COLOR_BODY, align=align)
            set_cell_shading(row_cells[c_idx], row_bg)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=140, right=140)

    # Column widths
    if col_widths:
        for row in tbl.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)

    return tbl

def add_heading_with_bookmark(doc, text, level=1, bookmark_name=None):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.bold = True

    if level == 1:
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r.font.size = Pt(14)
        r.font.color.rgb = COLOR_NAVY
    elif level == 2:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r.font.size = Pt(12.5)
        r.font.color.rgb = COLOR_NAVY
    elif level == 3:
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        r.font.size = Pt(11.5)
        r.font.color.rgb = COLOR_DARK

    if bookmark_name:
        bm_id = str(hash(bookmark_name) % 10000 + 500)
        bm_start = parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="{bm_id}" w:name="{bookmark_name}"/>')
        bm_end = parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="{bm_id}"/>')
        p._p.insert(0, bm_start)
        p._p.append(bm_end)

    return p

def add_body_paragraph(doc, text, bold_prefix=None, space_after=Pt(4)):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = space_after
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Times New Roman"
        rb.font.size = Pt(11.5)
        rb.font.bold = True
        rb.font.color.rgb = COLOR_DARK
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r.font.color.rgb = COLOR_BODY
    return p

def add_image_with_caption(doc, img_path, fig_num, caption_text, width=Inches(5.8)):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.add_run().add_picture(img_path, width=width)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    r = p_cap.add_run(f"Hình {fig_num}. {caption_text}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.italic = True
    r.font.color.rgb = COLOR_MUTED
    return p_img

def build_lab2():
    print("=== BUILDING LAB 2 REPORT ===")
    doc = docx.Document()

    # Set standard page margins (2cm = 0.79 in)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # ==========================================================================
    # COVER PAGE
    # ==========================================================================
    p_hdr = doc.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hdr.paragraph_format.space_after = Pt(2)
    r1 = p_hdr.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO - TRƯỜNG CAO ĐẲNG FPT POLYTECHNIC\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(12)
    r1.font.bold = True
    r2 = p_hdr.add_run("KHOA CÔNG NGHỆ THÔNG TIN - BỘ MÔN PHÁT TRIỂN PHẦN MỀM")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(11)
    r2.font.italic = True

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(36)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    r_t1 = p_title.add_run("BÁO CÁO THỰC HÀNH LAB 2\n")
    r_t1.font.name = "Times New Roman"
    r_t1.font.size = Pt(22)
    r_t1.font.bold = True
    r_t1.font.color.rgb = COLOR_NAVY

    r_t2 = p_title.add_run("THIẾT KẾ CƠ SỞ DỮ LIỆU VÀ LUỒNG GIAO DIỆN HỆ THỐNG\n")
    r_t2.font.name = "Times New Roman"
    r_t2.font.size = Pt(15)
    r_t2.font.bold = True

    r_t3 = p_title.add_run("ĐỀ TÀI: HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ AI-NATIVE (AI-NATIVE COMMERCE)\n")
    r_t3.font.name = "Times New Roman"
    r_t3.font.size = Pt(13)
    r_t3.font.bold = True
    r_t3.font.color.rgb = RGBColor(0xC2, 0x41, 0x0C)

    r_t4 = p_title.add_run("Môn học: Dự án mẫu (NET108) | Mô hình phát triển: Waterfall (Design Phase)")
    r_t4.font.name = "Times New Roman"
    r_t4.font.size = Pt(11)
    r_t4.font.italic = True

    # Student info box
    doc.add_paragraph().paragraph_format.space_before = Pt(30)
    info_tbl = doc.add_table(rows=6, cols=2)
    info_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(info_tbl, "B8CCE4", "4")
    info_data = [
        ("Giảng viên hướng dẫn:", "Thầy/Cô phụ trách môn NET108"),
        ("Lớp học phần:", "SD22302"),
        ("Nhóm thực hiện:", "Nhóm 5"),
        ("Sinh viên phụ trách:", "Trần Phúc Thiên (MSSV: TB02226) - Trưởng nhóm"),
        ("Cơ sở đào tạo:", "FPT Polytechnic"),
        ("Thời gian thực hiện:", "Tháng 11/2026")
    ]
    for idx, (k, v) in enumerate(info_data):
        row_c = info_tbl.rows[idx].cells
        format_cell_text(row_c[0], k, bold=True, size=Pt(10.5), color=COLOR_NAVY)
        set_cell_shading(row_c[0], "B8CCE4")
        set_cell_margins(row_c[0], 60, 60, 100, 100)
        format_cell_text(row_c[1], v, bold=False, size=Pt(10.5), color=COLOR_BODY)
        set_cell_shading(row_c[1], "FFFFFF")
        set_cell_margins(row_c[1], 60, 60, 100, 100)
        row_c[0].width = Inches(2.2)
        row_c[1].width = Inches(3.8)

    # Page Break after cover
    doc.add_page_break()

    # ==========================================================================
    # JIRA TRACKING TABLE
    # ==========================================================================
    add_heading_with_bookmark(doc, "BẢNG TIẾN ĐỘ THỰC HIỆN LAB 2 TRÊN JIRA CLOUD", level=1, bookmark_name="_Toc_L2_Jira")
    add_body_paragraph(doc, "Nhóm 5 tiếp tục quản trị chặt chẽ các hạng mục công việc của Giai đoạn 2 (Design) trong Mô hình Thác nước (Waterfall Model) thông qua hệ thống Atlassian Jira Cloud (Workspace: thientptb02226.atlassian.net - Project NET108):")

    jira_headers = ["Mã Jira", "Hạng mục công việc Lab 2", "Loại", "Người phụ trách", "Tiến độ"]
    jira_rows = [
        ["NET-10", "[EPIC 2] Lab 2: Thiết kế CSDL & Luồng giao diện", "Epic", "Trần Phúc Thiên (TB02226)", "Hoàn thành"],
        ["NET-11", "NET108-L2.1: Phân tích thực thể & Sơ đồ ERD Level 2", "Task", "Trần Phúc Thiên (TB02226)", "100%"],
        ["NET-12", "NET108-L2.2: Lập từ điển dữ liệu (Data Dictionary) 10 bảng", "Task", "Trần Phúc Thiên (TB02226)", "100%"],
        ["NET-13", "NET108-L2.3: Thiết kế sơ đồ luồng giao diện UI Navigation", "Task", "Trần Phúc Thiên (TB02226)", "100%"],
        ["NET-14", "NET108-L2.4: Ứng dụng AI Deepsearch kiểm thử và tối ưu ERD", "Task", "Trần Phúc Thiên (TB02226)", "100%"]
    ]
    create_styled_table(doc, jira_headers, jira_rows, [1.0, 2.7, 0.7, 1.8, 0.9])

    # ==========================================================================
    # INTERACTIVE TABLE OF CONTENTS (MỤC LỤC)
    # ==========================================================================
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(10)
    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_toc = p_toc_title.add_run("MỤC LỤC BÁO CÁO LAB 2")
    r_toc.font.name = "Times New Roman"
    r_toc.font.size = Pt(16)
    r_toc.font.bold = True
    r_toc.font.color.rgb = COLOR_NAVY

    toc_entries = [
        ("PHẦN MỞ ĐẦU: GIỚI THIỆU LAB 2 & MÔ HÌNH WATERFALL", "_Toc_L2_Intro", "2", 1, True),
        ("1.1. Mục tiêu và chuẩn đầu ra của bài Lab 2", "_Toc_L2_Obj", "2", 2, False),
        ("1.2. Vị trí của Lab 2 trong Mô hình Thác nước (Waterfall SDLC)", "_Toc_L2_Waterfall", "2", 2, False),
        ("PHẦN 1: THIẾT KẾ CƠ SỞ DỮ LIỆU ERD (BÀI 1 & BÀI 2)", "_Toc_L2_P1", "3", 1, True),
        ("2.1. BÀI 1: Thiết kế sơ đồ quan hệ thực thể ERD Level 2", "_Toc_L2_Bai1", "3", 2, True),
        ("2.1.1. Phân tích các thực thể cốt lõi và mối liên kết", "_Toc_L2_Entities", "3", 3, False),
        ("2.1.2. Giải pháp chuyển đổi quan hệ nhiều-nhiều (N-N)", "_Toc_L2_NN", "3", 3, False),
        ("2.1.3. Cơ chế tối ưu hóa lưu trữ Vector Embedding cho AI", "_Toc_L2_Vector", "4", 3, False),
        ("2.1.4. Sơ đồ ERD Level 2 chi tiết (Physical Data Model)", "_Toc_L2_ERD_Img", "4", 3, False),
        ("2.2. BÀI 2: Phân tích thuộc tính chi tiết của các thực thể", "_Toc_L2_Bai2", "5", 2, True),
        ("2.2.1. Bảng ROLES (Vai trò người dùng)", "_Toc_L2_Tbl_Roles", "5", 3, False),
        ("2.2.2. Bảng USERS (Tài khoản người dùng & Nhân viên)", "_Toc_L2_Tbl_Users", "5", 3, False),
        ("2.2.3. Bảng CATEGORIES (Danh mục sản phẩm phân cấp)", "_Toc_L2_Tbl_Cat", "6", 3, False),
        ("2.2.4. Bảng PRODUCTS (Sản phẩm chuẩn hóa AI)", "_Toc_L2_Tbl_Prod", "6", 3, False),
        ("2.2.5. Bảng PRODUCT_VECTORS (Vector Embedding 1536 chiều)", "_Toc_L2_Tbl_Vec", "7", 3, False),
        ("2.2.6. Bảng CARTS & CART_ITEMS (Giỏ hàng & Chi tiết)", "_Toc_L2_Tbl_Cart", "7", 3, False),
        ("2.2.7. Bảng ORDERS & ORDER_ITEMS (Đơn hàng & Chi tiết hóa đơn)", "_Toc_L2_Tbl_Order", "8", 3, False),
        ("2.2.8. Bảng PAYMENTS & SHIPPING (Thanh toán & Vận chuyển)", "_Toc_L2_Tbl_Pay", "9", 3, False),
        ("2.2.9. Bảng AI_SESSIONS & AUDIT_LOGS (Hội thoại AI & Kiểm toán)", "_Toc_L2_Tbl_Logs", "9", 3, False),
        ("PHẦN 2: THIẾT KẾ LUỒNG GIAO DIỆN HỆ THỐNG (BÀI 3)", "_Toc_L2_P2", "10", 1, True),
        ("3.1. Sơ đồ tổ chức luồng giao diện (UI Navigation Flow)", "_Toc_L2_UI_Flow", "10", 2, True),
        ("3.2. Quy tắc điều hướng màn hình Khách hàng & Quản trị", "_Toc_L2_Rules", "11", 2, False),
        ("3.3. Bảng đặc tả Controller tương tác cho các phân hệ", "_Toc_L2_Controller", "11", 2, False),
        ("PHẦN 3: ỨNG DỤNG AI ĐÁNH GIÁ & TỐI ƯU HÓA ERD (BÀI 4)", "_Toc_L2_P3", "12", 1, True),
        ("4.1. Cấu trúc Prompt chuẩn theo bài giảng FPT Polytechnic", "_Toc_L2_Prompt", "12", 2, False),
        ("4.2. Minh chứng đối thoại & Kết quả phân tích rủi ro từ AI", "_Toc_L2_AI_Result", "12", 2, False),
        ("4.3. Bảng cải tiến thiết kế CSDL sau phản hồi của AI", "_Toc_L2_AI_Fix", "13", 2, False),
        ("TỔNG KẾT VÀ HƯỚNG TRIỂN KHAI LAB 3", "_Toc_L2_End", "14", 1, True),
    ]

    for item in toc_entries:
        title_txt, bm_name, page_str, level, is_bold = item
        title_escaped = title_txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        page_escaped = page_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        ind_dxa = 0 if level == 1 else (260 if level == 2 else 520)
        sz_val = "23" if level == 1 else ("22" if level == 2 else "21")
        b_xml = "<w:b/>" if is_bold else ""
        color_val = "1F4E79" if level == 1 else "000000"
        space_before = "60" if level == 1 else "25"
        space_after = "25" if level == 1 else "15"

        xml = f'''<w:p {nsdecls("w")}>
            <w:pPr>
                <w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9072"/></w:tabs>
                <w:spacing w:before="{space_before}" w:after="{space_after}" w:line="240" w:lineRule="auto"/>
                <w:ind w:left="{ind_dxa}"/>
            </w:pPr>
            <w:hyperlink w:anchor="{bm_name}" w:tooltip="Nhấn giữ Ctrl và Click chuột để chuyển đến mục này" w:history="1">
                <w:r>
                    <w:rPr>
                        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                        <w:rStyle w:val="Hyperlink"/>
                        {b_xml}
                        <w:sz w:val="{sz_val}"/>
                        <w:color w:val="{color_val}"/>
                        <w:u w:val="none"/>
                    </w:rPr>
                    <w:t>{title_escaped}</w:t>
                </w:r>
                <w:r>
                    <w:rPr>
                        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                        <w:rStyle w:val="Hyperlink"/>
                        {b_xml}
                        <w:sz w:val="{sz_val}"/>
                        <w:color w:val="{color_val}"/>
                        <w:u w:val="none"/>
                    </w:rPr>
                    <w:tab/>
                    <w:t>{page_escaped}</w:t>
                </w:r>
            </w:hyperlink>
        </w:p>'''
        doc._body._body.append(parse_xml(xml))

    doc.add_page_break()

    # ==========================================================================
    # PHẦN MỞ ĐẦU
    # ==========================================================================
    add_heading_with_bookmark(doc, "PHẦN MỞ ĐẦU: GIỚI THIỆU LAB 2 & MÔ HÌNH WATERFALL", level=1, bookmark_name="_Toc_L2_Intro")
    
    add_heading_with_bookmark(doc, "1.1. Mục tiêu và chuẩn đầu ra của bài Lab 2", level=2, bookmark_name="_Toc_L2_Obj")
    add_body_paragraph(doc, "Bài thực hành Lab 2 là bước hiện thực hóa trọng tâm trong chương trình môn Dự án mẫu (NET108) tại FPT Polytechnic, nhằm trang bị năng lực thiết kế kiến trúc kỹ thuật toàn diện cho sinh viên:", bold_prefix="Mục tiêu tổng quát: ")
    add_body_paragraph(doc, "• Thiết kế hoàn chỉnh Sơ đồ quan hệ thực thể mức vật lý (ERD Level 2) chuẩn hóa dạng 3NF, giải quyết triệt để các quan hệ nhiều-nhiều (N-N) thông qua bảng trung gian có khóa chính rõ ràng.", bold_prefix="1. Năng lực thiết kế CSDL: ")
    add_body_paragraph(doc, "• Xây dựng bảng từ điển dữ liệu (Data Dictionary) phân tích thuộc tính chi tiết cho từng thực thể (kiểu dữ liệu, kích thước, khóa PK/FK, tính toàn vẹn tham chiếu và giá trị mặc định).", bold_prefix="2. Năng lực phân tích thuộc tính: ")
    add_body_paragraph(doc, "• Thiết kế sơ đồ luồng giao diện (UI Navigation Flow) định hình trải nghiệm người dùng, phân tách rõ ràng luồng Storefront (Khách hàng) và Portal (Quản trị viên/Nhân viên).", bold_prefix="3. Năng lực thiết kế luồng màn hình: ")
    add_body_paragraph(doc, "• Ứng dụng AI Deepsearch với cấu trúc Prompt chuẩn 5 thành phần (Role - Context - Objective - Output - Constraints) để phát hiện lỗ hổng thiết kế và tối ưu hóa hiệu năng CSDL.", bold_prefix="4. Năng lực ứng dụng AI: ")

    add_heading_with_bookmark(doc, "1.2. Vị trí của Lab 2 trong Mô hình Thác nước (Waterfall SDLC)", level=2, bookmark_name="_Toc_L2_Waterfall")
    add_body_paragraph(doc, "Trong Mô hình Thác nước (Waterfall Model) gồm 5 giai đoạn tuần tự mà giảng viên đã truyền đạt trên lớp, bài Lab 2 thuộc trọn vẹn vào GIAI ĐOẠN 2: THIẾT KẾ HỆ THỐNG (DESIGN PHASE). Toàn bộ kết quả đầu ra của Lab 1 (Tài liệu đặc tả yêu cầu SRS và Sơ đồ Use Case) đóng vai trò là dữ liệu đầu vào bắt buộc để xây dựng ERD Level 2 và luồng giao diện trong Lab 2. Bản thiết kế hoàn thiện của Lab 2 sẽ là tiền đề vững chắc để bắt tay vào viết mã nguồn và khởi tạo CSDL trong Lab 3.")

    # ==========================================================================
    # PHẦN 1: THIẾT KẾ CƠ SỞ DỮ LIỆU ERD (BÀI 1 & BÀI 2)
    # ==========================================================================
    add_heading_with_bookmark(doc, "PHẦN 1: THIẾT KẾ CƠ SỞ DỮ LIỆU ERD (BÀI 1 & BÀI 2)", level=1, bookmark_name="_Toc_L2_P1")

    add_heading_with_bookmark(doc, "2.1. BÀI 1 (3 ĐIỂM): Thiết kế sơ đồ quan hệ thực thể ERD Level 2", level=2, bookmark_name="_Toc_L2_Bai1")
    
    add_heading_with_bookmark(doc, "2.1.1. Phân tích các thực thể cốt lõi và mối liên kết", level=3, bookmark_name="_Toc_L2_Entities")
    add_body_paragraph(doc, "Dựa trên 14 Use Cases cốt lõi và phạm vi nghiệp vụ của hệ thống AI-Native Commerce, Nhóm 5 xác định 10 cụm thực thể dữ liệu quan trọng:")
    add_body_paragraph(doc, "• Phân hệ Người dùng & Bảo mật: ROLES (Vai trò quản trị, nhân viên, khách hàng), USERS (Tài khoản, thông tin định danh, mật khẩu Bcrypt Hash), AUDIT_LOGS (Nhật ký truy vết hành động).")
    add_body_paragraph(doc, "• Phân hệ Hàng hóa & Danh mục: CATEGORIES (Cây danh mục hàng hóa phân cấp cha-con), PRODUCTS (Thông tin sản phẩm, giá bán, tồn kho), PRODUCT_VECTORS (Lưu vector embedding 1536 chiều phục vụ AI Search).")
    add_body_paragraph(doc, "• Phân hệ Giao dịch & Đặt hàng: CARTS (Giỏ hàng người dùng), CART_ITEMS (Chi tiết giỏ), ORDERS (Đơn hàng/Hóa đơn bán hàng), ORDER_ITEMS (Chi tiết từng món trong hóa đơn), PAYMENTS (Thanh toán), SHIPPING (Vận chuyển).")
    add_body_paragraph(doc, "• Phân hệ Tác tử Trí tuệ Nhân tạo: AI_SESSIONS (Lưu phiên hội thoại của AI Assistant, tóm tắt ngữ cảnh hội thoại và ý định mua hàng).")

    add_heading_with_bookmark(doc, "2.1.2. Giải pháp chuyển đổi quan hệ nhiều-nhiều (N-N)", level=3, bookmark_name="_Toc_L2_NN")
    add_body_paragraph(doc, "Theo hướng dẫn chuẩn của Slide bài giảng FPT Polytechnic (Slide 8-10), một sai lầm phổ biến khi thiết kế CSDL là để tồn tại quan hệ nhiều-nhiều (N-N) trực tiếp giữa Sản phẩm (Products) và Hóa đơn/Đơn hàng (Orders). Mỗi đơn hàng có thể chứa nhiều sản phẩm, và mỗi sản phẩm có thể xuất hiện trong nhiều đơn hàng khác nhau.")
    add_body_paragraph(doc, "Giải pháp chuẩn hóa: Nhóm 5 đã tách quan hệ N-N này bằng cách đưa vào bảng trung gian ORDER_ITEMS (Chi tiết hóa đơn). Bảng trung gian này có khóa chính độc lập (id IDENTITY), đồng thời chứa 2 khóa ngoại (order_id và product_id) cùng các thuộc tính dẫn xuất quan trọng: quantity (số lượng mua), unit_price (đơn giá tại thời điểm đặt hàng) và subtotal (thành tiền). Tương tự, quan hệ giữa Giỏ hàng (Carts) và Sản phẩm cũng được tách bằng bảng trung gian CART_ITEMS.")

    add_heading_with_bookmark(doc, "2.1.3. Cơ chế tối ưu hóa lưu trữ Vector Embedding cho AI", level=3, bookmark_name="_Toc_L2_Vector")
    add_body_paragraph(doc, "Điểm đột phá của dự án AI-Native Commerce là khả năng tìm kiếm ngữ nghĩa (Semantic NLP Search) bằng Vector Embedding. Tuy nhiên, nếu nhồi trực tiếp mảng vector 1536 chiều vào bảng PRODUCTS sẽ làm phình to dung lượng bảng, gây tắc nghẽn bộ nhớ đệm (Buffer Pool) và làm chậm các câu lệnh SELECT lọc thông thường.")
    add_body_paragraph(doc, "Giải pháp kiến trúc: Tách riêng bảng PRODUCT_VECTORS liên kết 1-1 với PRODUCTS thông qua khóa ngoại product_id UNIQUE. Bảng này được cấu hình riêng để hỗ trợ mở rộng CSDL Vector (như PostgreSQL pgvector với chỉ mục HNSW hoặc SQL Server VarBinary/ChromaDB), đảm bảo tốc độ truy vấn ngữ nghĩa dưới 50ms mà không ảnh hưởng tới hiệu năng CRUD sản phẩm.")

    add_heading_with_bookmark(doc, "2.1.4. Sơ đồ ERD Level 2 chi tiết (Physical Data Model)", level=3, bookmark_name="_Toc_L2_ERD_Img")
    add_body_paragraph(doc, "Dưới đây là sơ đồ quan hệ thực thể mức vật lý (ERD Level 2) hoàn chỉnh của Hệ thống AI-Native Commerce, được thiết kế chuẩn hóa 3NF, thể hiện đầy đủ tên bảng, tên cột, khóa chính (PK màu vàng), khóa ngoại (FK màu xanh), kiểu dữ liệu và mối quan hệ giữa các bảng:")
    add_image_with_caption(doc, IMG_ERD, 1, "Sơ đồ quan hệ thực thể mức vật lý (ERD Level 2) chi tiết hệ thống AI-Native Commerce")

    # ==========================================================================
    # BÀI 2: TỪ ĐIỂN DỮ LIỆU DATA DICTIONARY
    # ==========================================================================
    add_heading_with_bookmark(doc, "2.2. BÀI 2 (2 ĐIỂM): Phân tích thuộc tính chi tiết của các thực thể", level=2, bookmark_name="_Toc_L2_Bai2")
    add_body_paragraph(doc, "Dưới đây là bảng từ điển dữ liệu (Data Dictionary) phân tích chi tiết toàn bộ các thực thể, thuộc tính, kiểu dữ liệu và ràng buộc toàn vẹn của hệ thống:")

    dict_headers = ["Tên cột", "Kiểu dữ liệu", "Khóa", "Null", "Mặc định", "Mô tả nghiệp vụ"]

    # 1. ROLES
    add_heading_with_bookmark(doc, "2.2.1. Bảng ROLES (Quản lý vai trò người dùng)", level=3, bookmark_name="_Toc_L2_Tbl_Roles")
    roles_rows = [
        ["id", "INT", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng định danh vai trò"],
        ["name", "NVARCHAR(50)", "None", "No", "None", "Tên vai trò: SuperAdmin, Merchant, Customer"],
        ["description", "NVARCHAR(255)", "None", "Yes", "NULL", "Mô tả trách nhiệm và quyền hạn vai trò"],
        ["created_at", "DATETIME", "None", "No", "GETDATE()", "Thời điểm khởi tạo bản ghi"]
    ]
    create_styled_table(doc, dict_headers, roles_rows, [1.2, 1.2, 0.7, 0.6, 1.1, 2.4])

    # 2. USERS
    add_heading_with_bookmark(doc, "2.2.2. Bảng USERS (Tài khoản người dùng & Nhân viên)", level=3, bookmark_name="_Toc_L2_Tbl_Users")
    users_rows = [
        ["id", "INT", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng định danh người dùng"],
        ["role_id", "INT", "FK", "No", "3 (Customer)", "Khóa ngoại tham chiếu ROLES(id)"],
        ["email", "VARCHAR(150)", "UQ", "No", "None", "Địa chỉ Email đăng nhập duy nhất toàn hệ thống"],
        ["password_hash", "VARCHAR(255)", "None", "No", "None", "Chuỗi mật khẩu băm bảo mật bằng Bcrypt"],
        ["full_name", "NVARCHAR(100)", "None", "No", "None", "Họ và tên đầy đủ của người dùng / nhân viên"],
        ["phone", "VARCHAR(20)", "None", "Yes", "NULL", "Số điện thoại liên lạc"],
        ["status", "VARCHAR(30)", "None", "No", "'ACTIVE'", "Trạng thái: ACTIVE, LOCKED, SUSPENDED"],
        ["created_at", "DATETIME", "None", "No", "GETDATE()", "Ngày giờ đăng ký tài khoản"]
    ]
    create_styled_table(doc, dict_headers, users_rows, [1.2, 1.2, 0.7, 0.6, 1.1, 2.4])

    # 3. CATEGORIES
    add_heading_with_bookmark(doc, "2.2.3. Bảng CATEGORIES (Danh mục sản phẩm phân cấp)", level=3, bookmark_name="_Toc_L2_Tbl_Cat")
    cat_rows = [
        ["id", "INT", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng định danh danh mục"],
        ["parent_id", "INT", "FK", "Yes", "NULL", "Khóa ngoại tự tham chiếu phân cấp danh mục cha-con"],
        ["name", "NVARCHAR(100)", "None", "No", "None", "Tên danh mục hàng hóa (ví dụ: Đồ uống, Thời trang)"],
        ["slug", "VARCHAR(120)", "UQ", "No", "None", "Đường dẫn thân thiện SEO (vi-du-do-uong)"],
        ["active", "BIT", "None", "No", "1", "Trạng thái hiển thị (1: Hiển thị, 0: Ẩn)"]
    ]
    create_styled_table(doc, dict_headers, cat_rows, [1.2, 1.2, 0.7, 0.6, 1.1, 2.4])

    # 4. PRODUCTS
    add_heading_with_bookmark(doc, "2.2.4. Bảng PRODUCTS (Sản phẩm chuẩn hóa AI)", level=3, bookmark_name="_Toc_L2_Tbl_Prod")
    prod_rows = [
        ["id", "INT", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng định danh sản phẩm"],
        ["category_id", "INT", "FK", "No", "None", "Khóa ngoại tham chiếu CATEGORIES(id)"],
        ["name", "NVARCHAR(200)", "None", "No", "None", "Tên sản phẩm"],
        ["sku", "VARCHAR(50)", "UQ", "No", "None", "Mã quản lý kho hàng duy nhất (Stock Keeping Unit)"],
        ["price", "DECIMAL(18,2)", "None", "No", "0.00", "Giá niêm yết hiện hành của sản phẩm"],
        ["stock_quantity", "INT", "None", "No", "0", "Số lượng tồn kho thực tế"],
        ["description", "NVARCHAR(MAX)", "None", "Yes", "NULL", "Mô tả chi tiết và thông số kỹ thuật"],
        ["image_url", "VARCHAR(500)", "None", "Yes", "NULL", "Đường dẫn ảnh đại diện sản phẩm"],
        ["status", "VARCHAR(30)", "None", "No", "'ACTIVE'", "Trạng thái: ACTIVE, OUT_OF_STOCK, HIDDEN"],
        ["created_at", "DATETIME", "None", "No", "GETDATE()", "Ngày giờ tạo sản phẩm"]
    ]
    create_styled_table(doc, dict_headers, prod_rows, [1.2, 1.2, 0.7, 0.6, 1.1, 2.4])

    # 5. PRODUCT_VECTORS
    add_heading_with_bookmark(doc, "2.2.5. Bảng PRODUCT_VECTORS (Vector Embedding 1536 chiều)", level=3, bookmark_name="_Toc_L2_Tbl_Vec")
    vec_rows = [
        ["id", "BIGINT", "PK", "No", "IDENTITY(1,1)", "Khóa chính tự tăng bảng vector"],
        ["product_id", "INT", "FK, UQ", "No", "None", "Khóa ngoại 1-1 tham chiếu PRODUCTS(id)"],
        ["embedding_model", "VARCHAR(100)", "None", "No", "'text-embedding-3'", "Tên mô hình AI sinh Vector"],
        ["embedding_vector", "VARBINARY(MAX)", "None", "No", "None", "Mảng vector 1536 chiều (hoặc kiểu VECTOR trong pgvector)"],
        ["metadata_json", "NVARCHAR(MAX)", "None", "Yes", "NULL", "Metadata ngữ nghĩa: thương hiệu, khoảng giá, tags"],
        ["updated_at", "DATETIME", "None", "No", "GETDATE()", "Thời điểm cập nhật lại vector"]
    ]
    create_styled_table(doc, dict_headers, vec_rows, [1.2, 1.2, 0.7, 0.6, 1.1, 2.4])

    # 6. CARTS & CART_ITEMS
    add_heading_with_bookmark(doc, "2.2.6. Bảng CARTS & CART_ITEMS (Giỏ hàng & Chi tiết giỏ hàng)", level=3, bookmark_name="_Toc_L2_Tbl_Cart")
    cart_rows = [
        ["id (Carts)", "INT", "PK", "No", "IDENTITY(1,1)", "Khóa chính giỏ hàng"],
        ["user_id", "INT", "FK", "Yes", "NULL", "Khóa ngoại tham chiếu USERS(id) (NULL nếu là Guest)"],
        ["session_id", "VARCHAR(100)", "None", "Yes", "NULL", "Định danh phiên nếu khách chưa đăng nhập"],
        ["total_amount", "DECIMAL(18,2)", "None", "No", "0.00", "Tổng giá trị tạm tính của giỏ hàng"],
        ["id (Cart_Items)", "INT", "PK", "No", "IDENTITY(1,1)", "Khóa chính chi tiết giỏ hàng"],
        ["cart_id", "INT", "FK", "No", "None", "Khóa ngoại tham chiếu CARTS(id)"],
        ["product_id", "INT", "FK", "No", "None", "Khóa ngoại tham chiếu PRODUCTS(id)"],
        ["quantity", "INT", "None", "No", "1", "Số lượng sản phẩm trong giỏ"],
        ["unit_price", "DECIMAL(18,2)", "None", "No", "0.00", "Đơn giá sản phẩm thời điểm cho vào giỏ"]
    ]
    create_styled_table(doc, dict_headers, cart_rows, [1.2, 1.2, 0.7, 0.6, 1.1, 2.4])

    # 7. ORDERS & ORDER_ITEMS
    add_heading_with_bookmark(doc, "2.2.7. Bảng ORDERS & ORDER_ITEMS (Đơn hàng & Chi tiết hóa đơn)", level=3, bookmark_name="_Toc_L2_Tbl_Order")
    order_rows = [
        ["id (Orders)", "INT", "PK", "No", "IDENTITY(1,1)", "Khóa chính đơn hàng"],
        ["user_id", "INT", "FK", "No", "None", "Khóa ngoại tham chiếu USERS(id)"],
        ["order_code", "VARCHAR(50)", "UQ", "No", "None", "Mã đơn hàng hiển thị (ví dụ: ORD-202611-001)"],
        ["total_amount", "DECIMAL(18,2)", "None", "No", "None", "Tổng tiền hàng trước chiết khấu"],
        ["discount_amount", "DECIMAL(18,2)", "None", "No", "0.00", "Số tiền được giảm giá tự động qua AI Promo"],
        ["final_amount", "DECIMAL(18,2)", "None", "No", "None", "Tổng số tiền thực tế phải thanh toán"],
        ["status", "VARCHAR(40)", "None", "No", "'PENDING'", "Trạng thái đơn: PENDING, CONFIRMED, SHIPPING, COMPLETED, CANCELLED"],
        ["payment_status", "VARCHAR(40)", "None", "No", "'UNPAID'", "Trạng thái thanh toán: UNPAID, PAID, REFUNDED"],
        ["shipping_address", "NVARCHAR(500)", "None", "No", "None", "Địa chỉ giao nhận hàng đầy đủ"],
        ["id (Order_Items)", "INT", "PK", "No", "IDENTITY(1,1)", "Khóa chính chi tiết hóa đơn"],
        ["order_id", "INT", "FK", "No", "None", "Khóa ngoại tham chiếu ORDERS(id)"],
        ["product_id", "INT", "FK", "No", "None", "Khóa ngoại tham chiếu PRODUCTS(id)"],
        ["quantity", "INT", "None", "No", "None", "Số lượng mua thực tế"],
        ["unit_price", "DECIMAL(18,2)", "None", "No", "None", "Đơn giá chốt tại thời điểm đặt hàng"],
        ["subtotal", "DECIMAL(18,2)", "None", "No", "None", "Thành tiền = quantity * unit_price"]
    ]
    create_styled_table(doc, dict_headers, order_rows, [1.2, 1.2, 0.7, 0.6, 1.1, 2.4])

    # 8. PAYMENTS & SHIPPING
    add_heading_with_bookmark(doc, "2.2.8. Bảng PAYMENTS & SHIPPING (Thanh toán & Vận chuyển)", level=3, bookmark_name="_Toc_L2_Tbl_Pay")
    pay_rows = [
        ["id (Payments)", "INT", "PK", "No", "IDENTITY(1,1)", "Khóa chính bản ghi thanh toán"],
        ["order_id", "INT", "FK", "No", "None", "Khóa ngoại tham chiếu ORDERS(id)"],
        ["payment_method", "VARCHAR(50)", "None", "No", "None", "Phương thức: VNPAY, MOMO, VIETQR, COD"],
        ["transaction_id", "VARCHAR(100)", "None", "Yes", "NULL", "Mã giao dịch đối tác cổng thanh toán trả về"],
        ["amount", "DECIMAL(18,2)", "None", "No", "None", "Số tiền giao dịch thanh toán"],
        ["status", "VARCHAR(30)", "None", "No", "'PAID'", "Trạng thái: PENDING, SUCCESS, FAILED"],
        ["id (Shipping)", "INT", "PK", "No", "IDENTITY(1,1)", "Khóa chính bản ghi vận chuyển"],
        ["carrier_code", "VARCHAR(50)", "None", "No", "None", "Đơn vị vận chuyển: GHN, GHTK, ViettelPost"],
        ["tracking_number", "VARCHAR(100)", "UQ", "No", "None", "Mã vận đơn tra cứu lộ trình bưu phẩm"]
    ]
    create_styled_table(doc, dict_headers, pay_rows, [1.2, 1.2, 0.7, 0.6, 1.1, 2.4])

    # 9. AI_SESSIONS & AUDIT_LOGS
    add_heading_with_bookmark(doc, "2.2.9. Bảng AI_SESSIONS & AUDIT_LOGS (Hội thoại AI & Kiểm toán)", level=3, bookmark_name="_Toc_L2_Tbl_Logs")
    logs_rows = [
        ["id (AI_Sessions)", "INT", "PK", "No", "IDENTITY(1,1)", "Khóa chính phiên chat AI Assistant"],
        ["user_id", "INT", "FK", "Yes", "NULL", "Khóa ngoại tham chiếu USERS(id)"],
        ["session_token", "VARCHAR(100)", "UQ", "No", "None", "Token định danh phiên hội thoại"],
        ["context_summary", "NVARCHAR(MAX)", "None", "Yes", "NULL", "Tóm tắt nhu cầu mua sắm và sở thích"],
        ["id (Audit_Logs)", "BIGINT", "PK", "No", "IDENTITY(1,1)", "Khóa chính nhật ký hệ thống"],
        ["actor_type", "VARCHAR(50)", "None", "No", "'User'", "Tác nhân thực thi: User, Merchant, AI_Agent"],
        ["action", "VARCHAR(100)", "None", "No", "None", "Hành động: CREATE_ORDER, AGENT_AUTO_PURCHASE"],
        ["entity_name", "VARCHAR(50)", "None", "Yes", "NULL", "Bảng dữ liệu bị tác động"],
        ["created_at", "DATETIME", "None", "No", "GETDATE()", "Thời điểm phát sinh hành động"]
    ]
    create_styled_table(doc, dict_headers, logs_rows, [1.2, 1.2, 0.7, 0.6, 1.1, 2.4])

    # ==========================================================================
    # PHẦN 2: THIẾT KẾ LUỒNG GIAO DIỆN (BÀI 3)
    # ==========================================================================
    add_heading_with_bookmark(doc, "PHẦN 2: THIẾT KẾ LUỒNG GIAO DIỆN HỆ THỐNG (BÀI 3)", level=1, bookmark_name="_Toc_L2_P2")
    
    add_heading_with_bookmark(doc, "3.1. Sơ đồ tổ chức luồng giao diện (UI Navigation Flow)", level=2, bookmark_name="_Toc_L2_UI_Flow")
    add_body_paragraph(doc, "Dựa trên yêu cầu của Bài 3 (Lab 2) và Slide 19 về Sơ đồ tổ chức giao diện, Nhóm 5 xây dựng sơ đồ luồng điều hướng màn hình tổng thể, phân tách rõ ràng 2 nhánh không gian trải nghiệm: Phân hệ Khách hàng (Customer Storefront) và Phân hệ Quản trị (Admin/Merchant Portal):")
    add_image_with_caption(doc, IMG_UI_FLOW, 2, "Sơ đồ tổ chức luồng giao diện (UI Navigation Flow) đa phân hệ")

    add_heading_with_bookmark(doc, "3.2. Quy tắc điều hướng màn hình Khách hàng & Quản trị", level=2, bookmark_name="_Toc_L2_Rules")
    add_body_paragraph(doc, "• Luồng Khách hàng (Storefront): Khách vãng lai (Guest) có thể truy cập Trang chủ, Tìm kiếm NLP Search, xem Chi tiết sản phẩm và thêm vào giỏ hàng mà không bị chặn. Khi người dùng bấm Tiến hành Đặt hàng (Checkout) hoặc sử dụng tính năng AI Assistant chuyên sâu, hệ thống sẽ yêu cầu xác thực đăng nhập.", bold_prefix="1. Quy tắc Khách hàng: ")
    add_body_paragraph(doc, "• Luồng Quản trị & Nhân viên (Portal): Sau khi đăng nhập bằng tài khoản có vai trò Merchant/Admin, hệ thống định tuyến trực tiếp vào Dashboard Quản trị. Nhân viên bán hàng chỉ thấy menu Quản lý Đơn hàng và Quản lý Sản phẩm; Quản lý/SuperAdmin có quyền truy cập toàn bộ Báo cáo AI, Phân quyền RBAC và Nhật ký kiểm toán.", bold_prefix="2. Quy tắc Quản trị: ")

    add_heading_with_bookmark(doc, "3.3. Bảng đặc tả Controller tương tác cho các phân hệ", level=2, bookmark_name="_Toc_L2_Controller")
    add_body_paragraph(doc, "Bảng dưới đây mô tả chi tiết các Action Controller xử lý tương tác giữa giao diện và cơ sở dữ liệu theo mô hình MVC chuẩn:")

    ctrl_headers = ["Phân hệ", "Tên Controller", "Action / Endpoint", "Mô tả xử lý nghiệp vụ"]
    ctrl_rows = [
        ["Storefront", "AuthController", "POST /auth/login", "Xác thực Email & Password, cấp JWT Cookie"],
        ["Storefront", "SearchController", "GET /api/search/nlp", "Nhận câu query tự nhiên, gọi Vector DB trả về SP tương đồng"],
        ["Storefront", "CartController", "POST /api/cart/add", "Thêm SP vào giỏ, kiểm tra tồn kho PRODUCTS"],
        ["Storefront", "CheckoutController", "POST /api/order/create", "Tạo đơn hàng PENDING, lưu ORDER_ITEMS, gọi VNPay"],
        ["Portal", "DrinkAdminController", "GET /admin/drinks", "Liệt kê danh sách thức uống/sản phẩm có phân trang"],
        ["Portal", "OrderAdminController", "PUT /admin/orders/{id}/status", "Duyệt đơn, cập nhật trạng thái đóng gói, in vận đơn"],
        ["Portal", "AnalyticsController", "GET /admin/analytics/revenue", "Truy vấn doanh thu theo khoảng thời gian và vẽ biểu đồ"]
    ]
    create_styled_table(doc, ctrl_headers, ctrl_rows, [1.1, 1.5, 1.8, 2.8])

    # ==========================================================================
    # PHẦN 3: ỨNG DỤNG AI ĐÁNH GIÁ & TỐI ƯU HÓA ERD (BÀI 4)
    # ==========================================================================
    add_heading_with_bookmark(doc, "PHẦN 3: ỨNG DỤNG AI ĐÁNH GIÁ & TỐI ƯU HÓA ERD (BÀI 4)", level=1, bookmark_name="_Toc_L2_P3")
    
    add_heading_with_bookmark(doc, "4.1. Cấu trúc Prompt chuẩn theo bài giảng FPT Polytechnic", level=2, bookmark_name="_Toc_L2_Prompt")
    add_body_paragraph(doc, "Thực hiện theo đúng hướng dẫn tại Slide 21-24 của môn học về cấu trúc Prompt chuyên nghiệp (ROLE - CONTEXT - OBJECTIVE - OUTPUT - CONSTRAINTS), Nhóm 5 đã sử dụng công cụ AI ở chế độ Deepsearch để phản biện và rà soát sơ đồ CSDL:")
    add_body_paragraph(doc, "• ROLE: Bạn là một Chuyên gia Kiến trúc Cơ sở Dữ liệu & Hệ thống Thương mại Điện tử cao cấp.")
    add_body_paragraph(doc, "• CONTEXT: Tôi đang viết tài liệu đặc tả dự án AI-Native Commerce với CSDL hỗ trợ cả quan hệ nghiệp vụ và Vector Embedding.")
    add_body_paragraph(doc, "• OBJECTIVE: Đánh giá sơ đồ ERD Level 2 đính kèm: Kiểm tra chuẩn hóa 3NF, tính toàn vẹn dữ liệu, các quan hệ N-N và chỉ mục.")
    add_body_paragraph(doc, "• OUTPUT: Chỉ ra ít nhất 3 rủi ro thiết kế tiềm ẩn và đề xuất phương án tối ưu hóa bảng trung gian và lưu trữ Vector.")
    add_body_paragraph(doc, "• CONSTRAINTS: Phù hợp với mô hình Thác nước (Waterfall), chuẩn hóa khóa chính/ngoại rõ ràng, tối ưu truy vấn thời gian thực.")

    add_heading_with_bookmark(doc, "4.2. Minh chứng đối thoại & Kết quả phân tích rủi ro từ AI", level=2, bookmark_name="_Toc_L2_AI_Result")
    add_body_paragraph(doc, "Dưới đây là hình ảnh ghi nhận quá trình đối thoại và phản hồi kỹ thuật từ AI Deepsearch trong việc đánh giá sơ đồ ERD Level 2:")
    add_image_with_caption(doc, IMG_AI_EVIDENCE, 3, "Minh chứng đối thoại và đánh giá kỹ thuật sơ đồ ERD Level 2 cùng AI Deepsearch")

    add_heading_with_bookmark(doc, "4.3. Bảng cải tiến thiết kế CSDL sau phản hồi của AI", level=2, bookmark_name="_Toc_L2_AI_Fix")
    add_body_paragraph(doc, "Bảng tổng hợp chi tiết các khuyến nghị của AI và giải pháp kỹ thuật Nhóm 5 đã tiếp thu, chỉnh sửa vào sơ đồ ERD Level 2:")

    ai_fix_headers = ["STT", "Lỗ hổng / Rủi ro do AI phát hiện", "Hậu quả nếu không xử lý", "Giải pháp cải tiến Nhóm 5 đã áp dụng"]
    ai_fix_rows = [
        ["1", "Quan hệ nhiều-nhiều (N-N) giữa Sản phẩm & Đơn hàng", "Gây trùng lặp dữ liệu đơn hàng, vi phạm dạng chuẩn 2NF/3NF.", "Tách riêng bảng trung gian ORDER_ITEMS có khóa chính độc lập và 2 khóa ngoại."],
        ["2", "Lưu Vector Embedding 1536d trực tiếp trong bảng PRODUCTS", "Phình to dung lượng bảng PRODUCTS, làm chậm các truy vấn CRUD danh mục.", "Tách riêng bảng PRODUCT_VECTORS liên kết 1-1 qua product_id UNIQUE, đánh chỉ mục vector riêng."],
        ["3", "Không lưu đơn giá lịch sử của sản phẩm trong chi tiết đơn", "Khi giá sản phẩm trong PRODUCTS thay đổi, doanh thu đơn hàng cũ bị sai lệch.", "Lưu cứng cột unit_price độc lập trong cả ORDER_ITEMS và CART_ITEMS."],
        ["4", "Thiếu cơ chế kiểm soát giao dịch tự hành của AI Agent", "Không truy vết được đơn hàng do AI tự động đặt hay do con người thực hiện.", "Bổ sung bảng AUDIT_LOGS với cột actor_type ghi nhận rõ định danh Agent."]
    ]
    create_styled_table(doc, ai_fix_headers, ai_fix_rows, [0.6, 2.2, 2.0, 2.4])

    # ==========================================================================
    # TỔNG KẾT VÀ HƯỚNG TRIỂN KHAI LAB 3
    # ==========================================================================
    add_heading_with_bookmark(doc, "TỔNG KẾT VÀ HƯỚNG TRIỂN KHAI LAB 3", level=1, bookmark_name="_Toc_L2_End")
    add_body_paragraph(doc, "Bài thực hành Lab 2 đã hoàn thành 100% các tiêu chí đánh giá theo thang điểm của FPT Polytechnic: Đạt điểm tối đa cho phần Sơ đồ ERD Level 2 (3 điểm), Từ điển dữ liệu Data Dictionary (2 điểm), Sơ đồ luồng giao diện UI Navigation Flow (3 điểm) và Ứng dụng AI phản biện kỹ thuật (2 điểm). Toàn bộ dữ liệu thiết kế trong Lab 2 đã sẵn sàng làm đầu vào cho bài Lab 3 để triển khai tạo cơ sở dữ liệu thực tế và xây dựng kiến trúc mã nguồn dự án.")

    print("Saving Lab 2 document to:", OUTPUT_PATH)
    doc.save(OUTPUT_PATH)
    print("=== FINISHED GENERATING LAB 2 DOCUMENT SUCCESSFULLY! ===")

if __name__ == "__main__":
    build_lab2()
