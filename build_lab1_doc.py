# -*- coding: utf-8 -*-
"""
Script to build full Lab 1 Report Word Document (.docx) for course NET108 (Dự án .NET 1)
Class: SD22302 - Group: Nhóm 5
Topic: Hệ thống Quản lý Quán Cà phê (QuanLyQuanCaPhe)
Instructor: ThS. Phan Hoàng Khải
Strictly covers Lab 1 requirements.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_lab1_docx():
    doc = docx.Document()

    # Standard A4 margins
    for sec in doc.sections:
        sec.page_width = Inches(8.27)
        sec.page_height = Inches(11.69)
        sec.top_margin = Inches(0.79)
        sec.bottom_margin = Inches(0.79)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(0.79)

    def apply_standard_header_footer(section):
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False

        # Header: FPT POLYTECHNIC | SAMPLE PROJECT
        hdr = section.header
        for p in hdr.paragraphs:
            p.text = ""
        tbl = hdr.add_table(rows=1, cols=2, width=Inches(6.48))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_left = tbl.cell(0, 0)
        c_right = tbl.cell(0, 1)
        c_left.width = Inches(3.24)
        c_right.width = Inches(3.24)

        p_l = c_left.paragraphs[0]
        p_l.paragraph_format.space_after = Pt(2)
        p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_l = p_l.add_run("FPT POLYTECHNIC")
        r_l.font.name = "Times New Roman"
        r_l.font.bold = True
        r_l.font.size = Pt(11)
        r_l.font.color.rgb = RGBColor(242, 107, 33)  # FPT Orange

        p_r = c_right.paragraphs[0]
        p_r.paragraph_format.space_after = Pt(2)
        p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_r = p_r.add_run("SAMPLE PROJECT")
        r_r.font.name = "Times New Roman"
        r_r.font.bold = True
        r_r.font.size = Pt(11)
        r_r.font.color.rgb = RGBColor(110, 110, 110)  # Grey

        for c in (c_left, c_right):
            tcPr = c._tc.get_or_add_tcPr()
            borders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="none"/><w:right w:val="none"/><w:bottom w:val="single" w:sz="8" w:space="4" w:color="A0A0A0"/></w:tcBorders>'
            )
            tcPr.append(borders)

        # Footer: Trang [PAGE]
        ftr = section.footer
        p_f = ftr.paragraphs[0] if ftr.paragraphs else ftr.add_paragraph()
        p_f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_f = p_f.add_run("Trang ")
        r_f.font.name = "Times New Roman"
        r_f.font.size = Pt(10)
        fldSimple = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
        p_f._p.append(fldSimple)

    def style_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 78, 121)
        return p

    def style_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(46, 117, 182)
        return p

    def style_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.italic = True
        r.font.color.rgb = RGBColor(0, 32, 96)
        return p

    def add_p(text, bold_prefix="", italic=False, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(12)
            r_pre.font.bold = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.italic = italic
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(12)
            r_pre.font.bold = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        return p

    def create_styled_table(rows_data, col_widths, headers=None):
        total_rows = len(rows_data) + (1 if headers else 0)
        cols = len(col_widths)
        t = doc.add_table(rows=total_rows, cols=cols)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False

        curr_row = 0
        if headers:
            hdr_row = t.rows[0]
            for c_idx, title in enumerate(headers):
                cell = hdr_row.cells[c_idx]
                cell.width = col_widths[c_idx]
                cell.text = title
                shd = parse_xml(r'<w:shd {} w:fill="1F4E79"/>'.format(nsdecls("w")))
                cell._tc.get_or_add_tcPr().append(shd)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.bold = True
                    run.font.size = Pt(11)
                    run.font.color.rgb = RGBColor(255, 255, 255)
            curr_row = 1

        for r_idx, row_values in enumerate(rows_data):
            row = t.rows[curr_row + r_idx]
            bg_color = "F2F5F9" if (r_idx % 2 == 1) else "FFFFFF"
            for c_idx, val in enumerate(row_values):
                cell = row.cells[c_idx]
                cell.width = col_widths[c_idx]
                cell.text = str(val)
                shd = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls("w"), bg_color))
                cell._tc.get_or_add_tcPr().append(shd)
                tcBorders = parse_xml(
                    r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/><w:left w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/><w:right w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/></w:tcBorders>'.format(
                        nsdecls("w")
                    )
                )
                cell._tc.get_or_add_tcPr().append(tcBorders)
                p = cell.paragraphs[0]
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(11)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        return t

    def add_srs_table(uc_id, uc_name, desc, actor, trigger, pre, post, main_flow, alt_flow, exc_flow):
        data = [
            ["Use Case ID", uc_id],
            ["Use Case", uc_name],
            ["Short Description", desc],
            ["Actors", actor],
            ["Trigger", trigger],
            ["Pre-conditions", pre],
            ["Post-conditions", post],
            ["Main Flow", main_flow],
            ["Alternative Flow", alt_flow],
            ["Exception Flow", exc_flow],
        ]
        t = doc.add_table(rows=10, cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        for r_idx, row in enumerate(data):
            r = t.rows[r_idx]
            cell_lbl = r.cells[0]
            cell_val = r.cells[1]
            cell_lbl.width = Inches(1.8)
            cell_val.width = Inches(4.7)

            cell_lbl.text = row[0]
            cell_val.text = row[1]

            shd_lbl = parse_xml(r'<w:shd {} w:fill="E8EEF5"/>'.format(nsdecls("w")))
            cell_lbl._tc.get_or_add_tcPr().append(shd_lbl)

            cell_lbl._tc.get_or_add_tcPr().append(
                parse_xml(
                    r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/></w:tcBorders>'.format(
                        nsdecls("w")
                    )
                )
            )
            cell_val._tc.get_or_add_tcPr().append(
                parse_xml(
                    r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/></w:tcBorders>'.format(
                        nsdecls("w")
                    )
                )
            )

            p0 = cell_lbl.paragraphs[0]
            if p0.runs:
                p0.runs[0].font.name = "Times New Roman"
                p0.runs[0].font.bold = True
                p0.runs[0].font.size = Pt(11)

            p1 = cell_val.paragraphs[0]
            if p1.runs:
                p1.runs[0].font.name = "Times New Roman"
                p1.runs[0].font.size = Pt(11)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==================== TRANG BÌA (SECTION 0) ====================
    sec_cover = doc.sections[0]
    sec_cover.header.is_linked_to_previous = False
    sec_cover.footer.is_linked_to_previous = False

    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_top.add_run("TRƯỜNG CAO ĐẲNG FPT POLYTECHNIC ĐỒNG NAI\nBỘ MÔN CÔNG NGHỆ THÔNG TIN\n")
    r1.font.name = "Times New Roman"
    r1.font.bold = True
    r1.font.size = Pt(13)
    r1.font.color.rgb = RGBColor(242, 107, 33)

    r_star = p_top.add_run("---***---\n")
    r_star.font.bold = True
    r_star.font.color.rgb = RGBColor(120, 120, 120)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(20)

    r2 = p_title.add_run("BÁO CÁO LAB 1\n")
    r2.font.name = "Times New Roman"
    r2.font.bold = True
    r2.font.size = Pt(22)
    r2.font.color.rgb = RGBColor(31, 78, 121)

    r3 = p_title.add_run("HỌC PHẦN: DỰ ÁN .NET 1 (NET108) - LỚP: SD22302\nĐỀ TÀI: HỆ THỐNG QUẢN LÝ QUÁN CÀ PHÊ\n(QUANLYQUANCAPHE)\n")
    r3.font.name = "Times New Roman"
    r3.font.bold = True
    r3.font.size = Pt(13.5)
    r3.font.color.rgb = RGBColor(60, 60, 60)

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_info.paragraph_format.space_before = Pt(40)
    p_info.paragraph_format.line_spacing = 1.3

    r_gv = p_info.add_run("Giảng viên hướng dẫn:\n")
    r_gv.font.bold = True
    r_gv.font.size = Pt(12)
    r_gv_name = p_info.add_run("ThS. Phan Hoàng Khải\n\n")
    r_gv_name.font.bold = True
    r_gv_name.font.size = Pt(13)
    r_gv_name.font.color.rgb = RGBColor(31, 78, 121)

    r_grp = p_info.add_run("Nhóm sinh viên thực hiện:\n")
    r_grp.font.bold = True
    r_grp.font.size = Pt(12)
    r_grp_name = p_info.add_run("NHÓM 5\n\n")
    r_grp_name.font.bold = True
    r_grp_name.font.size = Pt(13)
    r_grp_name.font.color.rgb = RGBColor(242, 107, 33)

    r_mem = p_info.add_run(
        "1. Trần Phúc Thiên (Nhóm trưởng - MSSV: PS38237)\n"
        "2. Trần Phạm Hoàng Minh (Thành viên - MSSV: PS38301)\n"
        "3. Cho Hoàng Hiếu Trung (Thành viên - MSSV: PS38412)\n"
        "4. Nguyễn Hoàng Quốc Anh (Thành viên - MSSV: PS38255)\n"
        "5. Nguyễn Châu Văn Phát (Thành viên - MSSV: PS38390)\n"
    )
    r_mem.font.size = Pt(12)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(45)
    r_loc = p_loc.add_run("ĐỒNG NAI, NĂM 2026")
    r_loc.font.bold = True
    r_loc.font.size = Pt(12)
    r_loc.font.color.rgb = RGBColor(100, 100, 100)

    # ==================== SECTION 1: PHÂN CÔNG NHIỆM VỤ ====================
    sec_plan = doc.add_section()
    apply_standard_header_footer(sec_plan)

    style_heading_1("THÔNG TIN DỰ ÁN VÀ PHÂN CÔNG NHIỆM VỤ NHÓM 5")
    add_p("Thông tin tổng quát học phần và đề tài:")
    info_table_data = [
        ["Học phần:", "NET108 - Dự án .NET 1 (FPT Polytechnic)"],
        ["Lớp học phần:", "SD22302"],
        ["Giảng viên giảng dạy:", "ThS. Phan Hoàng Khải"],
        ["Tên dự án / Đề tài:", "Hệ thống Quản lý Quán Cà phê (QuanLyQuanCaPhe)"],
        ["Nhóm thực hiện:", "Nhóm 5"],
        ["Thời gian thực hiện:", "Học kỳ Fall 2026 / Tháng 11 năm 2026"],
        ["Phạm vi báo cáo:", "Lab 1: Giới thiệu dự án, khảo sát AI, mô hình hóa Use Case và đặc tả SRS"],
    ]
    create_styled_table(info_table_data, [Inches(2.0), Inches(4.5)])

    add_p("Bảng phân công chi tiết nhiệm vụ và đánh giá mức độ đóng góp bài Lab 1:")
    task_table_headers = ["STT", "Họ và tên", "MSSV", "Nhiệm vụ phân công cụ thể trong Lab 1", "Tỷ lệ đóng góp"]
    task_table_data = [
        [
            "1",
            "Trần Phúc Thiên\n(Nhóm trưởng)",
            "PS38237",
            "Chủ trì khảo sát tài liệu bằng AI; Thiết lập cấu trúc hồ sơ Lab 1; Xây dựng sơ đồ Use Case tổng quát; Đặc tả SRS các ca sử dụng Bán hàng (UC05, UC06, UC07) và Đăng nhập (UC01); Rà soát tổng hợp tài liệu.",
            "100%",
        ],
        [
            "2",
            "Trần Phạm Hoàng Minh",
            "PS38301",
            "Nghiên cứu tra cứu mẫu tài liệu trên Perplexity AI; Phân tích yêu cầu khách hàng và hiện trạng quán cà phê; Đặc tả SRS Use Case Quản lý loại đồ uống (UC09) và Quản lý đồ uống (UC10).",
            "100%",
        ],
        [
            "3",
            "Cho Hoàng Hiếu Trung",
            "PS38412",
            "Phân tích luồng nghiệp vụ liên kết các chức năng; Phân loại nhóm người dùng (Actors); Đặc tả SRS Use Case Quản lý nhân viên (UC11) và Báo cáo thống kê (UC13).",
            "100%",
        ],
        [
            "4",
            "Nguyễn Hoàng Quốc Anh",
            "PS38255",
            "Nghiên cứu Gemini Deepsearch & quy tắc vẽ sơ đồ UML; Xây dựng ma trận chức năng hệ thống; Đặc tả SRS Use Case Xem hóa đơn cá nhân (UC08) và Quản lý hóa đơn (UC12).",
            "100%",
        ],
        [
            "5",
            "Nguyễn Châu Văn Phát",
            "PS38390",
            "Khảo sát quy trình xác thực và bảo mật; Nghiên cứu luồng xử lý ngoại lệ; Đặc tả SRS Use Case Quên mật khẩu (UC02), Đổi mật khẩu (UC03) và Sửa thông tin cá nhân (UC04).",
            "100%",
        ],
    ]
    create_styled_table(task_table_data, [Inches(0.5), Inches(1.5), Inches(0.9), Inches(2.8), Inches(0.8)], task_table_headers)

    # ==================== SECTION 2: MỤC LỤC ====================
    doc.add_page_break()
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_toc = p_toc.add_run("MỤC LỤC")
    r_toc.font.name = "Times New Roman"
    r_toc.font.bold = True
    r_toc.font.size = Pt(16)
    r_toc.font.color.rgb = RGBColor(31, 78, 121)

    toc_data = [
        ["THÔNG TIN DỰ ÁN VÀ PHÂN CÔNG NHIỆM VỤ NHÓM 5", "..................................................................................................", "2"],
        ["PHẦN I: GIỚI THIỆU DỰ ÁN", "..................................................................................................", "3"],
        ["  1. BÀI 1: ỨNG DỤNG AI TRONG TÌM KIẾM THÔNG TIN (2.0 ĐIỂM)", "..................................................................................................", "3"],
        ["    1.1. Mục tiêu và phương pháp nghiên cứu ứng dụng AI", "..................................................................................................", "3"],
        ["    1.2. Nhật ký Prompting chi tiết (Perplexity AI, ChatGPT, Gemini)", "..................................................................................................", "3"],
        ["    1.3. Đánh giá, đối sánh và chọn lọc giải pháp từ AI", "..................................................................................................", "5"],
        ["  2. BÀI 2: THỰC HIỆN TÀI LIỆU GIỚI THIỆU DỰ ÁN (4.0 ĐIỂM)", "..................................................................................................", "6"],
        ["    2.1. Giới thiệu tổng quan dự án Quản lý Quán Cà phê", "..................................................................................................", "6"],
        ["    2.2. Phân tích hiện trạng vận hành và nhu cầu khách hàng", "..................................................................................................", "6"],
        ["    2.3. Phân tích thành phần người dùng (Actors)", "..................................................................................................", "7"],
        ["    2.4. Danh sách chức năng theo nhóm người dùng", "..................................................................................................", "7"],
        ["    2.5. Phân tích luồng hoạt động tổng thể và sự liên kết", "..................................................................................................", "8"],
        ["PHẦN II: PHÂN TÍCH VÀ VẼ SƠ ĐỒ", "..................................................................................................", "10"],
        ["  2. PHÂN TÍCH YÊU CẦU", "..................................................................................................", "10"],
        ["    2.1. Sơ đồ Use Cases", "..................................................................................................", "10"],
        ["      2.1.1. Các quy tắc vẽ sơ đồ Use Case UML chuẩn", "..................................................................................................", "10"],
        ["      2.1.2. Sơ đồ Use Case tổng quát hệ thống (Theo đề bài Lab 1)", "..................................................................................................", "11"],
        ["      2.1.3. Phân rã chức năng và phân loại nhóm chức năng", "..................................................................................................", "13"],
        ["      2.1.4. Các sơ đồ Use Case phân rã chi tiết theo phân hệ", "..................................................................................................", "14"],
        ["    2.2. Đặc tả yêu cầu hệ thống (SRS - 13 Use Cases)", "..................................................................................................", "16"],
        ["      2.2.1. Use Case 1: Đăng nhập (UC01)", "..................................................................................................", "16"],
        ["      2.2.2. Use Case 2: Quên mật khẩu (UC02)", "..................................................................................................", "17"],
        ["      2.2.3. Use Case 3: Đổi mật khẩu (UC03)", "..................................................................................................", "18"],
        ["      2.2.4. Use Case 4: Sửa thông tin cá nhân (UC04)", "..................................................................................................", "19"],
        ["      2.2.5. Use Case 5: Tạo phiếu bán hàng (UC05)", "..................................................................................................", "20"],
        ["      2.2.6. Use Case 6: Sửa phiếu bán hàng (UC06)", "..................................................................................................", "21"],
        ["      2.2.7. Use Case 7: Xem phiếu bán hàng (UC07)", "..................................................................................................", "22"],
        ["      2.2.8. Use Case 8: Xem danh sách hóa đơn cá nhân (UC08)", "..................................................................................................", "23"],
        ["      2.2.9. Use Case 9: Quản lý loại đồ uống (UC09)", "..................................................................................................", "24"],
        ["      2.2.10. Use Case 10: Quản lý đồ uống (UC10)", "..................................................................................................", "25"],
        ["      2.2.11. Use Case 11: Quản lý nhân viên (UC11)", "..................................................................................................", "26"],
        ["      2.2.12. Use Case 12: Quản lý hóa đơn (UC12)", "..................................................................................................", "27"],
        ["      2.2.13. Use Case 13: Báo cáo thống kê (UC13)", "..................................................................................................", "28"],
    ]
    t_toc = doc.add_table(rows=len(toc_data), cols=3)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_toc.autofit = False
    for r_idx, row in enumerate(toc_data):
        r = t_toc.rows[r_idx]
        r.cells[0].width = Inches(4.3)
        r.cells[1].width = Inches(1.8)
        r.cells[2].width = Inches(0.4)
        for c_idx, val in enumerate(row):
            c = r.cells[c_idx]
            c.text = val
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            if c_idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if row[0].startswith("PHẦN") or row[0].startswith("THÔNG TIN"):
                p.runs[0].font.bold = True
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(11)

    # ==================== PHẦN I ====================
    doc.add_page_break()
    style_heading_1("PHẦN I: GIỚI THIỆU DỰ ÁN")

    # ---------- BÀI 1 ----------
    style_heading_2("1. BÀI 1 (2 ĐIỂM): ỨNG DỤNG AI TRONG TÌM KIẾM THÔNG TIN")

    style_heading_3("1.1. Mục tiêu và phương pháp nghiên cứu ứng dụng AI")
    add_p(
        "Trong khuôn khổ môn học Dự án .NET 1 (NET108) tại FPT Polytechnic, việc áp dụng trí tuệ nhân tạo (Generative AI) vào giai đoạn khảo sát, lấy yêu cầu và đặc tả hệ thống đóng vai trò quan trọng giúp sinh viên nâng cao năng suất, chuẩn hóa thuật ngữ chuyên ngành và hoàn thiện tài liệu theo tiêu chuẩn quốc tế (IEEE 830) kết hợp khung biểu mẫu của nhà trường."
    )
    add_p("Nhóm 5 đã định hướng và triển khai khảo sát qua 3 công cụ AI chủ đạo:")
    add_bullet(
        "https://www.perplexity.ai/ (Perplexity Search Engine): Tìm kiếm có dẫn nguồn thời gian thực các mẫu tài liệu SRS (Software Requirements Specification), mẫu bảng phân tích Use Case 10 trường theo chuẩn thực tiễn và các quy định quản lý hóa đơn/bán hàng trong ngành F&B tại Việt Nam.",
        "Perplexity AI: ",
    )
    add_bullet(
        "OpenAI ChatGPT (Model GPT-4o / Deepsearch): Nghiên cứu sâu về phân tích quy trình nghiệp vụ quán cà phê, luồng bán hàng POS, xử lý ca làm việc, kiểm toán tiền mặt và phát hiện các luồng ngoại lệ (Exception Flows) tiềm ẩn.",
        "ChatGPT Deepsearch: ",
    )
    add_bullet(
        "Google Gemini (Gemini 1.5 Pro / Deep Thinking): Thiết kế ma trận phân quyền người dùng (Role-Based Access Control), mô hình hóa quan hệ Actors với Use Cases và chuẩn hóa ngôn ngữ đặc tả C# .NET và SQL Server.",
        "Google Gemini: ",
    )

    style_heading_3("1.2. Bảng nhật ký Prompting và kết quả tra cứu chi tiết")
    add_p(
        "Dưới đây là nhật ký câu lệnh (Prompt Log) được Nhóm 5 thực hiện trong quá trình khảo sát tài liệu đặc tả hệ thống cho dự án Quản lý Quán Cà phê:"
    )

    prompt_headers = ["STT", "Công cụ AI & Chế độ", "Nội dung Prompt (Câu lệnh chi tiết)", "Kết quả trích xuất & Tiếp thu", "Đánh giá chất lượng"]
    prompt_rows = [
        [
            "1",
            "Perplexity AI\n(Pro Search)",
            'Prompt:\n"Hãy tìm kiếm mẫu tài liệu đặc tả yêu cầu phần mềm (SRS) chuẩn của FPT Polytechnic cho môn Dự án Mẫu / Dự án .NET 1. Cụ thể cấu trúc bảng đặc tả Use Case gồm những trường dữ liệu nào? Đưa ra ví dụ cho chức năng Tạo phiếu bán hàng."',
            "Kết quả trích xuất:\n- Cung cấp mẫu cấu trúc bảng SRS 10 hàng tiêu chuẩn: Use Case ID, Use Case, Short Description, Actors, Trigger, Pre-conditions, Post-conditions, Main Flow, Alternative Flow, ExceptionFlow.\n- Gợi ý bảng mẫu chuẩn cho nghiệp vụ F&B (POS).",
            "Độ tin cậy: 9.5/10.\nNguồn dẫn chuẩn xác từ tài nguyên giáo trình và tài liệu đồ án FPT Edu.",
        ],
        [
            "2",
            "ChatGPT\n(Chế độ Deepsearch)",
            'Prompt:\n"Đóng vai trò là Chuyên gia Phân tích Nghiệp vụ (BA) trong ngành F&B. Hãy phân tích chi tiết quy trình bán hàng và quản lý bàn tại một quán cà phê vừa và nhỏ: từ lúc khách vào gọi món, nhân viên tạo phiếu, chuyển pha chế, cập nhật món, cho đến khi thanh toán in hóa đơn và bàn giao ca. Hãy chỉ rõ các điểm nóng có thể xảy ra sai sót hoặc thất thoát."',
            "Kết quả trích xuất:\n- Phân rã luồng bán hàng thành 4 giai đoạn chính: Đặt món (Order) -> Pha chế (Barista) -> Phục vụ & Sửa phiếu -> Thanh toán & Đóng ca.\n- Chỉ ra các nguy cơ: Nhân viên tự ý hủy đơn bỏ tiền túi, nhầm lẫn bàn khi khách đổi chỗ, sai lệch số liệu ca.",
            "Độ tin cậy: 9.0/10.\nPhân tích nghiệp vụ sâu sắc, giúp Nhóm 5 thiết kế Use Case Quản lý hóa đơn và Kiểm kê cá nhân rất chặt chẽ.",
        ],
        [
            "3",
            "Google Gemini\n(1.5 Pro Deep Thinking)",
            'Prompt:\n"Tôi đang làm đề tài Quản lý Quán Cà phê bằng C# .NET WinForms và SQL Server. Sơ đồ Use Case tổng quát gồm 2 Actors: Nhân viên và Quản lý với 13 Use Cases: Tạo phiếu bán hàng, Sửa phiếu bán hàng, Xem phiếu bán hàng, Xem danh sách hóa đơn cá nhân, Quản lý loại đồ uống, Quản lý đồ uống, Quản lý nhân viên, Quản lý hóa đơn, Sửa thông tin cá nhân, Đăng nhập, Quên mật khẩu, Đổi mật khẩu, Báo cáo thống kê. Hãy xây dựng ma trận phân quyền CRUD và quan hệ tương tác giữa 2 Actors này."',
            "Kết quả trích xuất:\n- Phân định rõ ràng ma trận phân quyền (RBAC):\n+ Dùng chung: Đăng nhập, Đổi mật khẩu, Quên mật khẩu, Sửa thông tin cá nhân.\n+ Nhân viên: Bán hàng, xem và sửa phiếu của ca, xem hóa đơn cá nhân.\n+ Quản lý: Quản lý danh mục loại, món, tài khoản nhân viên, xem toàn bộ hóa đơn quán, xem báo cáo doanh thu.",
            "Độ tin cậy: 9.5/10.\nCực kỳ logic, khớp hoàn toàn với sơ đồ Use Case đề bài giao cho Nhóm 5.",
        ],
        [
            "4",
            "ChatGPT & Gemini\n(Cross-Verification)",
            'Prompt:\n"Hãy viết chi tiết kịch bản luồng xử lý ngoại lệ (Exception Flows) cho Use Case Quên mật khẩu và Hủy hóa đơn bán hàng trong phần mềm quản lý quán cà phê để đảm bảo an toàn bảo mật và kiểm toán tài chính."',
            "Kết quả trích xuất:\n- Quên mật khẩu: Kiểm tra email khớp tài khoản -> Sinh OTP 6 số hết hạn sau 5 phút -> Khóa tạm thời nếu nhập sai OTP 3 lần.\n- Hủy hóa đơn: Bắt buộc chỉ Quản lý mới có quyền hủy; yêu cầu nhập lý do hủy tối thiểu 10 ký tự; lưu vết Audit Log gồm ngày giờ, ID người hủy.",
            "Độ tin cậy: 9.0/10.\nĐược đưa trực tiếp vào bảng SRS của UC02 và UC12.",
        ],
    ]
    create_styled_table(prompt_rows, [Inches(0.4), Inches(1.3), Inches(2.2), Inches(2.1), Inches(1.0)], prompt_headers)

    style_heading_3("1.3. Đánh giá, đối sánh và chọn lọc giải pháp từ kết quả AI")
    add_p(
        "Sau khi thu thập kết quả từ các phiên làm việc với AI, Nhóm 5 đã tiến hành tổng hợp, chắt lọc và điều chỉnh để phù hợp tuyệt đối với yêu cầu thực tế của đề tài môn NET108:"
    )
    add_bullet(
        "Tiếp thu cấu trúc SRS FPT chuẩn: Kế thừa trọn vẹn biểu mẫu bảng đặc tả SRS 10 hàng từ Perplexity AI, bao gồm các thành phần: Mã ca sử dụng, Tên ca, Mô tả ngắn, Tác nhân, Sự kiện kích hoạt, Tiền điều kiện, Hậu điều kiện, Luồng chính, Luồng rẽ nhánh và Luồng ngoại lệ.",
        "Về hình thức đặc tả: ",
    )
    add_bullet(
        "Giới hạn đúng phạm vi 13 Use Cases: Loại bỏ các chức năng dư thừa mà AI tự suy đoán (như đặt bàn trực tuyến qua app, tích điểm thẻ thành viên phức tạp) để tập trung cao độ vào 13 Use Cases cốt lõi được giảng viên chỉ định trong đề bài Lab 1.",
        "Về phạm vi nghiệp vụ: ",
    )
    add_bullet(
        "Tối ưu cho kiến trúc C# .NET: Định hình các ngoại lệ xử lý gắn liền với Windows Forms và SQL Server (như lỗi mất kết nối máy chủ, trùng khóa chính Primary Key, vi phạm khóa ngoại Foreign Key khi xóa danh mục đang có sản phẩm kinh doanh).",
        "Về giải pháp kỹ thuật: ",
    )

    # ---------- BÀI 2 ----------
    style_heading_2("2. BÀI 2 (4 ĐIỂM): THỰC HIỆN TÀI LIỆU GIỚI THIỆU DỰ ÁN")

    style_heading_3("2.1. Giới thiệu tổng quan dự án Quản lý Quán Cà phê")
    add_p(
        'Dự án "Hệ thống Quản lý Quán Cà phê" (QuanLyQuanCaPhe) là ứng dụng máy tính dành cho các cơ sở kinh doanh dịch vụ đồ uống và giải khát. Phần mềm được xây dựng trên nền tảng Microsoft .NET Framework / .NET Core với ngôn ngữ C# và hệ quản trị cơ sở dữ liệu Microsoft SQL Server.'
    )
    add_p(
        "Mục tiêu cốt lõi của dự án là số hóa toàn diện quy trình vận hành tại quầy thu ngân và khu vực quản lý cửa hàng, thay thế phương pháp ghi chép order thủ công bằng giấy truyền thống, loại bỏ tối đa sai sót trong việc tính tiền, phục vụ đồ uống nhanh chóng và quản lý dòng tiền minh bạch, chính xác theo thời gian thực."
    )

    style_heading_3("2.2. Phân tích hiện trạng vận hành và nhu cầu khách hàng")
    add_p("A. Hiện trạng vận hành thủ công tại các quán cà phê vừa và nhỏ:", bold_prefix="")
    add_bullet(
        "Nhân viên ghi phiếu order bằng giấy tay, dễ bị nhầm lẫn khi quán đông khách, chữ viết mờ nhạt hoặc thất lạc phiếu order khi chuyển vào quầy bar pha chế.",
        "Sai sót khi gọi món: ",
    )
    add_bullet(
        "Thu ngân tự tính tiền thủ công hoặc dùng máy tính bỏ túi cơ bản, dễ gây nhầm lẫn khi áp dụng giá theo size (S, M, L), phụ thu hoặc tính toán số tiền thối lại cho khách hàng.",
        "Rủi ro tính tiền: ",
    )
    add_bullet(
        "Chủ quán khó kiểm soát được chính xác số lượng ly bán ra và số tiền mặt thực tế thu được trong từng ca làm việc, dễ phát sinh thất thoát và gian lận.",
        "Khó khăn trong đối soát: ",
    )
    add_bullet(
        "Việc thống kê doanh thu cuối ngày/cuối tháng phải cộng dồn từng hóa đơn giấy rất tốn thời gian, không có biểu đồ so sánh các loại đồ uống bán chạy để lên kế hoạch nhập nguyên vật liệu.",
        "Thiếu báo cáo trực quan: ",
    )

    add_p("B. Nhu cầu cấp thiết của khách hàng (Chủ cơ sở kinh doanh & Nhân viên):", bold_prefix="")
    add_bullet(
        "Giao diện trực quan, dễ thao tác trên màn hình cảm ứng hoặc chuột máy tính, hỗ trợ tạo phiếu bán hàng theo bàn, chọn món nhanh theo hình ảnh và danh mục.",
        "Tối ưu tốc độ phục vụ: ",
    )
    add_bullet(
        "Hỗ trợ chỉnh sửa phiếu bán hàng linh hoạt (thêm món, bớt món, đổi bàn cho khách) trước khi xuất hóa đơn thanh toán.",
        "Linh hoạt xử lý order: ",
    )
    add_bullet(
        "Phân quyền rõ ràng giữa Nhân viên thu ngân và Quản lý cửa hàng để đảm bảo tính an toàn dữ liệu và chống gian lận.",
        "Bảo mật và phân quyền: ",
    )
    add_bullet(
        "Hệ thống báo cáo tự động, chính xác về doanh thu, số hóa đơn, sản lượng bán ra theo ngày/tháng và hỗ trợ kết xuất dữ liệu báo cáo ra file Excel.",
        "Tự động hóa báo cáo: ",
    )

    style_heading_3("2.3. Phân tích thành phần người dùng (Actors) trong hệ thống")
    add_p("Hệ thống Quản lý Quán Cà phê xác định rõ 2 nhóm tác nhân (Actors) trực tiếp vận hành hệ thống:")

    actors_headers = ["Tác nhân (Actor)", "Phân loại vai trò", "Mô tả trách nhiệm & Phạm vi quyền hạn"]
    actors_data = [
        [
            "Nhân viên\n(Staff / Cashier)",
            "Người dùng vận hành tác nghiệp trực tiếp tại quầy",
            "- Thực hiện đăng nhập, đổi mật khẩu và cập nhật thông tin cá nhân của mình.\n"
            "- Tạo mới phiếu bán hàng (order món theo bàn hoặc mang về).\n"
            "- Chỉnh sửa phiếu bán hàng đang phục vụ (thêm món, đổi món, đổi bàn).\n"
            "- Xem chi tiết phiếu bán hàng đang mở.\n"
            "- Tra cứu danh sách các hóa đơn do chính mình lập trong ca để kiểm kê bàn giao tiền.",
        ],
        [
            "Quản lý\n(Store Manager / Admin)",
            "Người dùng quản trị, điều hành và giám sát toàn quán",
            "- Sở hữu toàn bộ quyền hạn của người dùng hệ thống (đăng nhập, thông tin cá nhân).\n"
            "- Quản lý danh mục loại đồ uống (thêm, sửa, xóa loại đồ uống).\n"
            "- Quản lý danh mục món đồ uống (thêm, cập nhật giá, size, hình ảnh, ngưng bán).\n"
            "- Quản lý hồ sơ nhân viên (thêm nhân viên, cấp tài khoản, phân quyền, khóa tài khoản).\n"
            "- Giám sát và quản lý toàn bộ hóa đơn của cửa hàng, thực hiện hủy hóa đơn sai sót có kiểm toán.\n"
            "- Xem báo cáo thống kê doanh thu, số lượng bán và xuất dữ liệu báo cáo ra file Excel.",
        ],
    ]
    create_styled_table(actors_data, [Inches(1.8), Inches(1.8), Inches(3.2)], actors_headers)

    style_heading_3("2.4. Danh sách chức năng theo nhóm người dùng")
    add_p("Hệ thống gồm tổng cộng 13 ca sử dụng cốt lõi, được phân bổ chặt chẽ theo ma trận chức năng sau:")

    func_headers = ["Nhóm phân hệ", "Mã UC", "Tên chức năng / Use Case", "Nhân viên", "Quản lý", "Ghi chú phân quyền"]
    func_data = [
        ["Phân hệ Dùng chung", "UC01", "Đăng nhập", "x", "x", "Xác thực danh tính và phân quyền giao diện"],
        ["Phân hệ Dùng chung", "UC02", "Quên mật khẩu", "x", "x", "Xác thực OTP qua email để cấp lại mật khẩu"],
        ["Phân hệ Dùng chung", "UC03", "Đổi mật khẩu", "x", "x", "Chủ động đổi mật khẩu định kỳ"],
        ["Phân hệ Dùng chung", "UC04", "Sửa thông tin cá nhân", "x", "x", "Cập nhật họ tên, SĐT, email cá nhân"],
        ["Phân hệ Bán hàng", "UC05", "Tạo phiếu bán hàng", "x", "-", "Order món, chọn bàn, tính tiền tạm"],
        ["Phân hệ Bán hàng", "UC06", "Sửa phiếu bán hàng", "x", "-", "Thêm món, bớt món, chuyển bàn"],
        ["Phân hệ Bán hàng", "UC07", "Xem phiếu bán hàng", "x", "-", "Tra cứu chi tiết phiếu đang phục vụ"],
        ["Phân hệ Bán hàng", "UC08", "Xem danh sách hóa đơn cá nhân", "x", "-", "Xem hóa đơn do mình lập trong ca làm việc"],
        ["Phân hệ Quản trị", "UC09", "Quản lý loại đồ uống", "-", "x", "Thêm/sửa/xóa danh mục nhóm đồ uống"],
        ["Phân hệ Quản trị", "UC10", "Quản lý đồ uống", "-", "x", "Cập nhật menu món, giá bán, size, ảnh món"],
        ["Phân hệ Quản trị", "UC11", "Quản lý nhân viên", "-", "x", "Quản lý hồ sơ, tài khoản và phân quyền"],
        ["Phân hệ Quản trị", "UC12", "Quản lý hóa đơn", "-", "x", "Xem toàn bộ hóa đơn quán, hủy đơn sai"],
        ["Phân hệ Quản trị", "UC13", "Báo cáo thống kê", "-", "x", "Thống kê doanh thu theo ngày/tháng, xuất Excel"],
    ]
    create_styled_table(func_data, [Inches(1.5), Inches(0.8), Inches(2.2), Inches(0.7), Inches(0.7), Inches(1.8)], func_headers)

    style_heading_3("2.5. Phân tích luồng hoạt động tổng thể và sự liên kết giữa các chức năng")
    add_p(
        "Các chức năng trong hệ thống Quản lý Quán Cà phê không hoạt động biệt lập mà liên kết chặt chẽ với nhau tạo thành một chuỗi quy trình khép kín, đảm bảo tính nhất quán dữ liệu:"
    )
    add_bullet(
        "Người dùng (Nhân viên hoặc Quản lý) nhập tài khoản tại màn hình Đăng nhập (UC01). Hệ thống xác thực và điều hướng giao diện phù hợp. Nếu quên mật khẩu, người dùng sử dụng Quên mật khẩu (UC02) để nhận mã OTP khôi phục. Sau khi vào hệ thống, người dùng có thể Đổi mật khẩu (UC03) hoặc Sửa thông tin cá nhân (UC04).",
        "1. Luồng Xác thực & Tài khoản: ",
    )
    add_bullet(
        "Tại quầy thu ngân, Nhân viên chọn bàn trống trên sơ đồ và bấm Tạo phiếu bán hàng (UC05). Nhân viên chọn các món đồ uống từ menu (dữ liệu được lấy từ UC10). Khi khách yêu cầu gọi thêm món hoặc chuyển bàn, nhân viên sử dụng Sửa phiếu bán hàng (UC06). Để kiểm tra lại các món đã gọi cho khách, nhân viên sử dụng Xem phiếu bán hàng (UC07). Khi khách thanh toán, hệ thống chốt phiếu thành Hóa đơn chính thức.",
        "2. Luồng Nghiệp vụ Bán hàng & Phục vụ: ",
    )
    add_bullet(
        "Cuối ca trực, Nhân viên truy cập Xem danh sách hóa đơn cá nhân (UC08) để tổng kết số lượng hóa đơn mình đã lập và tổng tiền thu được trong ca, đối chiếu với số tiền mặt trong két để bàn giao cho ca tiếp theo.",
        "3. Luồng Kiểm kê & Bàn giao ca: ",
    )
    add_bullet(
        "Quản lý thiết lập danh mục Loại đồ uống (UC09), sau đó thêm mới hoặc cập nhật các Món đồ uống (UC10) gồm đơn giá, size và hình ảnh. Mọi thay đổi ở danh mục này lập tức cập nhật đồng bộ lên màn hình Tạo phiếu bán hàng của Nhân viên.",
        "4. Luồng Cấu hình Thực đơn (Menu): ",
    )
    add_bullet(
        "Quản lý theo dõi việc vận hành thông qua Quản lý hóa đơn (UC12) để xem mọi giao dịch trong ngày và xử lý các trường hợp hủy hóa đơn có sai sót. Đồng thời, Quản lý truy cập Báo cáo thống kê (UC13) để xem biểu đồ doanh thu theo mốc thời gian, top đồ uống bán chạy nhất và xuất báo cáo ra file Excel để báo cáo tài chính.",
        "5. Luồng Kiểm soát & Báo cáo quản trị: ",
    )

    # ==================== PHẦN II ====================
    doc.add_page_break()
    style_heading_1("PHẦN II: PHÂN TÍCH VÀ VẼ SƠ ĐỒ")

    # ---------- BÀI 3 ----------
    style_heading_2("2. PHÂN TÍCH YÊU CẦU (BÀI 3 - 4 ĐIỂM: VẼ MÔ HÌNH HỆ THỐNG VÀ XÁC ĐỊNH THỰC THỂ)")

    style_heading_2("2.1. Sơ đồ Use Cases")

    style_heading_3("2.1.1. Các quy tắc vẽ sơ đồ Use Case UML chuẩn")
    add_p(
        "Sơ đồ ca sử dụng (Use Case Diagram) là một trong những sơ đồ hành vi cơ bản của ngôn ngữ mô hình hóa thống nhất UML (Unified Modeling Language). Để đảm bảo tính chuẩn xác và khoa học, Nhóm 5 tuân thủ nghiêm ngặt các quy tắc vẽ UML quốc tế:"
    )
    add_bullet(
        "Được ký hiệu bằng hình người (Stick Man), đại diện cho vai trò của người hoặc hệ thống bên ngoài tương tác với phần mềm. Tên Actor phải là danh từ, đặt ngay dưới hình vẽ (ví dụ: Nhân viên, Quản lý).",
        "Tác nhân (Actor): ",
    )
    add_bullet(
        "Được ký hiệu bằng hình Elip (Oval) chứa tên chức năng bên trong. Tên Use Case bắt buộc phải bắt đầu bằng một Động từ đi kèm bổ ngữ rõ nghĩa (ví dụ: Tạo phiếu bán hàng, Đăng nhập, Báo cáo thống kê).",
        "Ca sử dụng (Use Case): ",
    )
    add_bullet(
        "Khung hình chữ nhật bao quanh toàn bộ các Use Case của hệ thống, trên góc có ghi tên hệ thống phần mềm (QuanLyQuanCaPhe). Các Actors luôn nằm bên ngoài ranh giới hệ thống.",
        "Ranh giới hệ thống (System Boundary): ",
    )
    add_bullet(
        "Đường thẳng liền nét (Solid Line) nối giữa Actor và Use Case mà Actor đó trực tiếp tham gia tương tác kích hoạt hoặc thụ hưởng kết quả.",
        "Quan hệ kết hợp (Association): ",
    )
    add_bullet(
        "Quan hệ Include (Bao hàm - <<include>> với mũi tên nét đứt) thể hiện Use Case bắt buộc phải thực thi Use Case con. Quan hệ Extend (Mở rộng - <<extend>>) thể hiện hành vi rẽ nhánh có điều kiện.",
        "Quan hệ phụ thuộc (Include / Extend): ",
    )

    style_heading_3("2.1.2. Sơ đồ Use Case tổng quát hệ thống (Theo đúng đề bài Lab 1)")
    add_p(
        "Dưới đây là sơ đồ Use Case tổng quát của Hệ thống Quản lý Quán Cà phê, tuân thủ chính xác theo bố cục đề bài Lab 1 gồm 2 Actors và 13 Use Cases:"
    )

    # Check and insert images
    img_debai = r"C:\Net108Khai\usecase_debai_lab1.jpeg"
    if os.path.exists(img_debai):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.paragraph_format.space_before = Pt(6)
        p_img1.paragraph_format.space_after = Pt(2)
        doc.add_picture(img_debai, width=Inches(6.0))
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap1.paragraph_format.space_after = Pt(8)
        r_cap1 = p_cap1.add_run("Hình 2.1: Sơ đồ Use Case phân bổ 13 Use Cases theo nguyên bản đề bài Lab 1")
        r_cap1.font.name = "Times New Roman"
        r_cap1.font.italic = True
        r_cap1.font.size = Pt(10.5)

    add_p(
        "Để làm rõ luồng tương tác thực tế giữa các tác nhân và từng Use Case, Nhóm 5 đã xây dựng sơ đồ Use Case tổng quát hoàn chỉnh bổ sung đầy đủ các đường liên kết (Association lines) giữa Nhân viên, Quản lý và 13 ca sử dụng:"
    )

    img_full = r"C:\Net108Khai\usecase_tongquat.png"
    if os.path.exists(img_full):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(6)
        p_img2.paragraph_format.space_after = Pt(2)
        doc.add_picture(img_full, width=Inches(6.3))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.paragraph_format.space_after = Pt(10)
        r_cap2 = p_cap2.add_run("Hình 2.2: Sơ đồ Use Case tổng quát hoàn chỉnh thể hiện tương tác của Nhân viên và Quản lý")
        r_cap2.font.name = "Times New Roman"
        r_cap2.font.italic = True
        r_cap2.font.size = Pt(10.5)

    style_heading_3("2.1.3. Phân rã chức năng và phân loại nhóm chức năng theo loại người dùng")
    add_p("Bảng phân loại chi tiết 13 ca sử dụng theo phân hệ và tác nhân chịu trách nhiệm:")

    decomp_headers = ["STT", "Mã UC", "Tên chức năng", "Phân hệ nghiệp vụ", "Tác nhân chính", "Mục tiêu nghiệp vụ cốt lõi"]
    decomp_rows = [
        ["1", "UC01", "Đăng nhập", "Phân hệ Dùng chung", "Nhân viên, Quản lý", "Xác thực danh tính đăng nhập bằng tài khoản và mật khẩu."],
        ["2", "UC02", "Quên mật khẩu", "Phân hệ Dùng chung", "Nhân viên, Quản lý", "Khôi phục quyền truy cập qua mã OTP gửi về Email."],
        ["3", "UC03", "Đổi mật khẩu", "Phân hệ Dùng chung", "Nhân viên, Quản lý", "Tăng cường bảo mật bằng cách thay đổi mật khẩu định kỳ."],
        ["4", "UC04", "Sửa thông tin cá nhân", "Phân hệ Dùng chung", "Nhân viên, Quản lý", "Cập nhật hồ sơ cá nhân (Họ tên, SĐT, Email, Ảnh đại diện)."],
        ["5", "UC05", "Tạo phiếu bán hàng", "Phân hệ Bán hàng", "Nhân viên", "Lập order món cho khách theo bàn/mang về, tạm tính tiền."],
        ["6", "UC06", "Sửa phiếu bán hàng", "Phân hệ Bán hàng", "Nhân viên", "Thêm bớt món, đổi món hoặc đổi bàn trước khi thanh toán."],
        ["7", "UC07", "Xem phiếu bán hàng", "Phân hệ Bán hàng", "Nhân viên", "Tra cứu chi tiết các order đang phục vụ để kiểm tra món."],
        ["8", "UC08", "Xem danh sách hóa đơn cá nhân", "Phân hệ Bán hàng", "Nhân viên", "Xem lại các hóa đơn do chính mình lập trong ca để bàn giao ca."],
        ["9", "UC09", "Quản lý loại đồ uống", "Phân hệ Quản trị", "Quản lý", "Thiết lập danh mục phân loại đồ uống (Cà phê, Trà, Nước ép)."],
        ["10", "UC10", "Quản lý đồ uống", "Phân hệ Quản trị", "Quản lý", "Quản lý danh sách món, đơn giá bán, size và hình ảnh."],
        ["11", "UC11", "Quản lý nhân viên", "Phân hệ Quản trị", "Quản lý", "Quản lý hồ sơ nhân viên, phân quyền và khóa tài khoản."],
        ["12", "UC12", "Quản lý hóa đơn", "Phân hệ Quản trị", "Quản lý", "Tra cứu toàn bộ hóa đơn của quán, xử lý hủy đơn sai sót."],
        ["13", "UC13", "Báo cáo thống kê", "Phân hệ Quản trị", "Quản lý", "Thống kê doanh thu theo thời gian, top đồ uống, xuất Excel."],
    ]
    create_styled_table(decomp_rows, [Inches(0.4), Inches(0.7), Inches(1.8), Inches(1.5), Inches(1.3), Inches(2.3)], decomp_headers)

    style_heading_3("2.1.4. Các sơ đồ Use Case phân rã chi tiết theo phân hệ")
    add_p(
        "Nhằm làm rõ ranh giới xử lý và mối liên hệ giữa tác nhân với từng nhóm chức năng cụ thể, hệ thống được phân rã thành 3 sơ đồ Use Case chi tiết sau:"
    )

    # Sub-diagram 1: Common
    add_p("A. Sơ đồ Use Case Phân hệ Dùng chung (Common Module):", bold_prefix="")
    add_p(
        "Bao gồm 4 chức năng nền tảng phục vụ cho cả Nhân viên và Quản lý: Đăng nhập, Quên mật khẩu, Đổi mật khẩu và Sửa thông tin cá nhân."
    )
    img_sub_chung = r"C:\Net108Khai\usecase_sub_chung.png"
    if os.path.exists(img_sub_chung):
        p_sub1 = doc.add_paragraph()
        p_sub1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img_sub_chung, width=Inches(5.5))
        p_csub1 = doc.add_paragraph()
        p_csub1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_csub1.paragraph_format.space_after = Pt(8)
        r_csub1 = p_csub1.add_run("Hình 2.3: Sơ đồ Use Case Phân hệ Dùng chung")
        r_csub1.font.italic = True
        r_csub1.font.size = Pt(10.5)

    # Sub-diagram 2: Staff
    add_p("B. Sơ đồ Use Case Phân hệ Bán hàng & Phục vụ (POS Module):", bold_prefix="")
    add_p(
        "Bao gồm 4 chức năng cốt lõi do Nhân viên thu ngân/phục vụ trực tiếp vận hành: Tạo phiếu bán hàng, Sửa phiếu bán hàng, Xem phiếu bán hàng và Xem danh sách hóa đơn cá nhân."
    )
    img_sub_banhang = r"C:\Net108Khai\usecase_sub_banhang.png"
    if os.path.exists(img_sub_banhang):
        p_sub2 = doc.add_paragraph()
        p_sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img_sub_banhang, width=Inches(5.5))
        p_csub2 = doc.add_paragraph()
        p_csub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_csub2.paragraph_format.space_after = Pt(8)
        r_csub2 = p_csub2.add_run("Hình 2.4: Sơ đồ Use Case Phân hệ Bán hàng & Phục vụ")
        r_csub2.font.italic = True
        r_csub2.font.size = Pt(10.5)

    # Sub-diagram 3: Manager
    add_p("C. Sơ đồ Use Case Phân hệ Quản trị cửa hàng (Administration Module):", bold_prefix="")
    add_p(
        "Bao gồm 5 chức năng quản lý cấp cao dành riêng cho Quản lý cửa hàng: Quản lý loại đồ uống, Quản lý đồ uống, Quản lý nhân viên, Quản lý hóa đơn và Báo cáo thống kê."
    )
    img_sub_quanly = r"C:\Net108Khai\usecase_sub_quanly.png"
    if os.path.exists(img_sub_quanly):
        p_sub3 = doc.add_paragraph()
        p_sub3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img_sub_quanly, width=Inches(5.5))
        p_csub3 = doc.add_paragraph()
        p_csub3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_csub3.paragraph_format.space_after = Pt(8)
        r_csub3 = p_csub3.add_run("Hình 2.5: Sơ đồ Use Case Phân hệ Quản trị cửa hàng")
        r_csub3.font.italic = True
        r_csub3.font.size = Pt(10.5)

    # ==================== ĐẶC TẢ SRS CHI TIẾT (13 USE CASES) ====================
    doc.add_page_break()
    style_heading_2("2.2. Đặc tả yêu cầu hệ thống (SRS)")
    add_p(
        "Phần này trình bày đặc tả chi tiết toàn bộ 13 Use Cases của hệ thống Quản lý Quán Cà phê theo đúng biểu mẫu chuẩn 10 trường của Trường Cao đẳng FPT Polytechnic (gồm Use Case ID, Use Case, Short Description, Actors, Trigger, Pre-conditions, Post-conditions, Main Flow, Alternative Flow và ExceptionFlow):"
    )

    # UC01: Đăng nhập
    style_heading_3("2.2.1. Use case 1: Đăng nhập (UC01)")
    add_srs_table(
        "UC01",
        "Đăng nhập hệ thống",
        "Xác thực danh tính người dùng khi truy cập phần mềm bằng Tên đăng nhập và Mật khẩu; phân quyền giao diện (Nhân viên hoặc Quản lý) và khởi tạo phiên làm việc (Session).",
        "Nhân viên (Staff), Quản lý (Manager)",
        "Người dùng mở phần mềm Quản lý Quán Cà phê hoặc chọn Đăng xuất để đăng nhập lại.",
        "Hệ thống đã kết nối thành công với CSDL SQL Server; tài khoản người dùng đã được cấp và ở trạng thái kích hoạt (IsActive = true).",
        "Thành công: Đăng nhập thành công, điều hướng vào màn hình chính tương ứng vai trò (Main Form).\nThất bại: Đăng nhập thất bại, hệ thống báo lỗi cụ thể và giữ nguyên tại màn hình Login.",
        "(1) Người dùng mở phần mềm, hệ thống hiển thị màn hình Đăng nhập.\n"
        "(2) Người dùng nhập Tên đăng nhập và Mật khẩu.\n"
        '(3) Người dùng bấm nút "Đăng nhập" (hoặc nhấn phím Enter).\n'
        "(4) Hệ thống mã hóa mật khẩu đầu vào (băm SHA-256) và so khớp với CSDL.\n"
        "(5) Hệ thống kiểm tra vai trò (Role: Nhân viên hay Quản lý).\n"
        "(6) Hệ thống lưu phiên làm việc, mở giao diện chính tương ứng với quyền hạn.",
        '(2a) Người dùng tích chọn "Nhớ mật khẩu": Hệ thống lưu thông tin đăng nhập đã mã hóa cho lần sau.',
        '(4.1) Tên đăng nhập hoặc mật khẩu không chính xác: Hệ thống báo lỗi "Tên đăng nhập hoặc mật khẩu không chính xác!".\n'
        '(5.1) Tài khoản bị khóa (IsActive = false): Hệ thống cảnh báo "Tài khoản của bạn đã bị vô hiệu hóa. Vui lòng liên hệ Quản lý!".\n'
        "(4.2) Quá 5 lần nhập sai liên tiếp: Hệ thống tạm khóa đăng nhập trong vòng 5 phút để bảo vệ tài khoản.",
    )

    # UC02: Quên mật khẩu
    style_heading_3("2.2.2. Use case 2: Quên mật khẩu (UC02)")
    add_srs_table(
        "UC02",
        "Quên mật khẩu",
        "Hỗ trợ người dùng tự lấy lại quyền truy cập khi quên mật khẩu qua việc xác thực Email/Tên đăng nhập, gửi mã OTP 6 số để thiết lập mật khẩu mới an toàn.",
        "Nhân viên (Staff), Quản lý (Manager)",
        'Người dùng bấm vào liên kết "Quên mật khẩu?" tại màn hình Đăng nhập.',
        "Tài khoản đã đăng ký Email hợp lệ trong hệ thống; máy tính có kết nối Internet để gửi email xác thực qua SMTP.",
        "Thành công: Mật khẩu mới được cập nhật vào CSDL, người dùng đăng nhập lại bình thường.\nThất bại: Không đổi được mật khẩu, hệ thống báo lỗi tương ứng.",
        '(1) Tại màn hình Đăng nhập, người dùng bấm "Quên mật khẩu?".\n'
        "(2) Hệ thống mở form Khôi phục mật khẩu.\n"
        '(3) Người dùng nhập Tên đăng nhập và Email đã đăng ký, bấm nút "Gửi mã OTP".\n'
        "(4) Hệ thống kiểm tra tính khớp nối giữa Tên đăng nhập và Email trong CSDL.\n"
        "(5) Hệ thống sinh mã OTP ngẫu nhiên 6 chữ số (hiệu lực 5 phút) và gửi tới Email người dùng.\n"
        "(6) Người dùng nhận mã OTP qua Email, nhập mã OTP, Mật khẩu mới và Nhập lại mật khẩu mới.\n"
        '(7) Người dùng bấm "Xác nhận đổi mật khẩu".\n'
        "(8) Hệ thống kiểm tra OTP, mã hóa mật khẩu mới và lưu vào CSDL, thông báo thành công.",
        '(3a) Người dùng bấm "Quay lại": Hệ thống hủy phiên khôi phục và trở về màn hình Đăng nhập.',
        '(4.1) Tên đăng nhập hoặc Email không tồn tại / không khớp: Hệ thống báo lỗi "Thông tin tài khoản hoặc Email không chính xác!".\n'
        '(8.1) Mã OTP nhập vào sai hoặc đã hết hạn (quá 5 phút): Hệ thống báo lỗi "Mã xác thực không hợp lệ hoặc đã hết hạn!".\n'
        '(8.2) Mật khẩu xác nhận không trùng khớp: Hệ thống báo lỗi "Mật khẩu xác nhận không khớp!".',
    )

    # UC03: Đổi mật khẩu
    style_heading_3("2.2.3. Use case 3: Đổi mật khẩu (UC03)")
    add_srs_table(
        "UC03",
        "Đổi mật khẩu",
        "Cho phép người dùng đang đăng nhập tự chủ động thay đổi mật khẩu định kỳ nhằm nâng cao tính bảo mật, yêu cầu nhập chính xác mật khẩu hiện tại.",
        "Nhân viên (Staff), Quản lý (Manager)",
        'Người dùng chọn mục "Đổi mật khẩu" trên menu Tiện ích / Tài khoản.',
        "Người dùng đã đăng nhập thành công vào hệ thống.",
        "Thành công: Mật khẩu mới được mã hóa và lưu vào CSDL, hệ thống yêu cầu đăng nhập lại.\nThất bại: Mật khẩu cũ không đổi, hệ thống hiển thị thông báo lỗi.",
        '(1) Người dùng chọn chức năng "Đổi mật khẩu" từ menu tài khoản.\n'
        "(2) Hệ thống hiển thị form Đổi mật khẩu gồm: Mật khẩu hiện tại, Mật khẩu mới, Xác nhận mật khẩu mới.\n"
        '(3) Người dùng nhập đầy đủ thông tin vào 3 ô và bấm nút "Cập nhật".\n'
        "(4) Hệ thống kiểm tra mật khẩu hiện tại có khớp với CSDL hay không.\n"
        "(5) Hệ thống kiểm tra mật khẩu mới: độ dài tối thiểu 6 ký tự, khác mật khẩu cũ.\n"
        "(6) Hệ thống kiểm tra tính trùng khớp giữa Mật khẩu mới và Xác nhận mật khẩu mới.\n"
        "(7) Hệ thống mã hóa (băm SHA-256) mật khẩu mới và cập nhật vào CSDL.\n"
        '(8) Hệ thống thông báo "Đổi mật khẩu thành công! Vui lòng đăng nhập lại" và tự động đăng xuất.',
        '(3a) Người dùng bấm "Hủy bỏ": Hệ thống đóng form và giữ nguyên phiên làm việc hiện tại.',
        '(4.1) Nhập sai mật khẩu hiện tại: Hệ thống báo lỗi "Mật khẩu hiện tại không chính xác!".\n'
        '(5.1) Mật khẩu mới trùng với mật khẩu cũ: Hệ thống báo lỗi "Mật khẩu mới không được trùng mật khẩu cũ!".\n'
        '(5.2) Mật khẩu mới dưới 6 ký tự: Hệ thống báo lỗi "Mật khẩu mới phải có tối thiểu 6 ký tự!".',
    )

    # UC04: Sửa thông tin cá nhân
    style_heading_3("2.2.4. Use case 4: Sửa thông tin cá nhân (UC04)")
    add_srs_table(
        "UC04",
        "Sửa thông tin cá nhân",
        "Cho phép người dùng đang đăng nhập tự cập nhật thông tin hồ sơ của chính mình như Họ và tên, Số điện thoại liên hệ, Email cá nhân và Ảnh đại diện (Avatar).",
        "Nhân viên (Staff), Quản lý (Manager)",
        'Người dùng nhấp vào ảnh đại diện hoặc tên tài khoản và chọn "Thông tin cá nhân".',
        "Người dùng đã đăng nhập thành công vào hệ thống.",
        "Thành công: Thông tin cá nhân được cập nhật vào CSDL và phản ánh ngay lên giao diện phần mềm.\nThất bại: Giữ nguyên thông tin cũ, hiển thị cảnh báo lỗi dữ liệu.",
        '(1) Người dùng chọn chức năng "Thông tin cá nhân".\n'
        "(2) Hệ thống hiển thị form Thông tin cá nhân với dữ liệu hiện tại của tài khoản.\n"
        '(3) Người dùng chỉnh sửa các trường: Họ và tên, Số điện thoại, Email, tải ảnh mới từ máy tính.\n'
        '(4) Người dùng bấm nút "Lưu thay đổi".\n'
        "(5) Hệ thống kiểm tra hợp lệ dữ liệu (Email đúng định dạng, Số điện thoại đúng 10 chữ số).\n"
        "(6) Hệ thống lưu dữ liệu mới vào bảng Nhân viên trong CSDL.\n"
        '(7) Hệ thống thông báo "Cập nhật thông tin thành công!" và làm mới tên hiển thị trên thanh trạng thái.',
        '(3a) Người dùng bấm "Hủy": Hệ thống đóng form mà không lưu các chỉnh sửa.',
        '(5.1) Số điện thoại không hợp lệ (chứa chữ cái hoặc không đủ 10 số): Hệ thống báo lỗi "Số điện thoại không hợp lệ!".\n'
        '(5.2) Email sai định dạng quy chuẩn RFC: Hệ thống báo lỗi "Email không đúng định dạng!".',
    )

    # UC05: Tạo phiếu bán hàng
    style_heading_3("2.2.5. Use case 5: Tạo phiếu bán hàng (UC05)")
    add_srs_table(
        "UC05",
        "Tạo phiếu bán hàng",
        "Cho phép Nhân viên thu ngân tạo mới một phiếu bán hàng/order gồm chọn số bàn hoặc mang về, chọn các món đồ uống, điều chỉnh số lượng, ghi chú (đường, đá, topping), tính tiền tạm tính và gửi đơn cho pha chế.",
        "Nhân viên (Staff / Thu ngân)",
        'Khách hàng gọi đồ uống hoặc Nhân viên bấm chọn bàn trống trên sơ đồ và nhấn "Tạo phiếu mới".',
        "Nhân viên đã đăng nhập hệ thống; danh mục đồ uống đã được cấu hình trong CSDL.",
        "Thành công: Phiếu bán hàng được tạo với trạng thái Đang phục vụ, mã hóa đơn tạm được sinh ra, bàn chuyển sang trạng thái Có khách (màu đỏ/cam).\nThất bại: Hệ thống báo lỗi, không tạo được phiếu.",
        '(1) Nhân viên mở giao diện Bán hàng POS và bấm nút "Tạo phiếu bán hàng mới".\n'
        "(2) Hệ thống hiển thị danh mục loại đồ uống và danh sách các món đồ uống kèm hình ảnh, đơn giá.\n"
        "(3) Nhân viên chọn hình thức phục vụ: Tại quán (chọn số bàn) hoặc Mang về (Take away).\n"
        "(4) Nhân viên chọn các món đồ uống khách order, tăng/giảm số lượng và thêm ghi chú đặc biệt.\n"
        "(5) Hệ thống tự động tính thành tiền từng món và tổng tiền tạm tính của phiếu.\n"
        '(6) Nhân viên kiểm tra lại thông tin và bấm nút "Xác nhận tạo phiếu".\n'
        "(7) Hệ thống lưu phiếu vào CSDL và cập nhật trạng thái bàn trên sơ đồ.",
        "(4a) Khách hàng đổi ý muốn xóa món trước khi bấm xác nhận: Nhân viên bấm nút Xóa món trên danh sách order.\n"
        "(5a) Áp dụng giảm giá/khuyến mãi: Nhân viên chọn voucher giảm giá, hệ thống tự động tính lại tổng tiền.",
        '(4.1) Món đồ uống đã hết nguyên liệu/tạm ngưng kinh doanh: Hệ thống báo lỗi "Món đồ uống này hiện đã hết hàng!".\n'
        '(3.1) Bàn được chọn đã có khách khác ngồi: Hệ thống cảnh báo "Bàn này đang có khách, vui lòng chọn bàn khác!".',
    )

    # UC06: Sửa phiếu bán hàng
    style_heading_3("2.2.6. Use case 6: Sửa phiếu bán hàng (UC06)")
    add_srs_table(
        "UC06",
        "Sửa phiếu bán hàng",
        "Cho phép Nhân viên chỉnh sửa phiếu bán hàng đang trong trạng thái phục vụ (chưa thanh toán): thêm món mới, cập nhật số lượng, đổi món, chuyển bàn hoặc áp dụng ưu đãi.",
        "Nhân viên (Staff / Thu ngân)",
        "Khách hàng gọi thêm món, đổi món hoặc yêu cầu chuyển sang vị trí bàn khác.",
        'Phiếu bán hàng đã tồn tại và chưa hoàn tất thanh toán (trạng thái "Đang phục vụ").',
        "Thành công: Thông tin phiếu bán hàng được cập nhật vào CSDL, tổng tiền được tính lại chính xác.\nThất bại: Giữ nguyên trạng thái phiếu cũ, hiển thị thông báo lỗi.",
        "(1) Nhân viên truy cập danh sách phiếu đang mở hoặc bấm vào bàn đang có khách trên sơ đồ.\n"
        "(2) Hệ thống hiển thị chi tiết phiếu bán hàng hiện tại của bàn đó.\n"
        "(3) Nhân viên thực hiện thao tác sửa: chọn thêm món mới, tăng/giảm số lượng hoặc chọn chuyển bàn.\n"
        "(4) Hệ thống tự động cập nhật lại tổng tiền tạm tính của hóa đơn.\n"
        '(5) Nhân viên bấm nút "Lưu thay đổi".\n'
        "(6) Hệ thống ghi nhận các thay đổi vào CSDL và cập nhật lại giao diện bán hàng.",
        '(3a) Khách yêu cầu chuyển bàn: Nhân viên chọn "Chuyển bàn", chọn bàn trống mới, hệ thống cập nhật bàn đích và giải phóng bàn cũ.\n'
        '(3b) Khách yêu cầu gộp bàn: Nhân viên chọn chức năng "Gộp bàn", hệ thống dồn các món vào một phiếu duy nhất.',
        '(1.1) Phiếu bán hàng đã được thanh toán hoặc đã bị hủy: Hệ thống khóa chức năng sửa và thông báo "Phiếu đã đóng, không thể sửa!".\n'
        '(3.1) Bàn chuyển đến đã có khách: Hệ thống cảnh báo "Bàn đích đang có khách, không thể chuyển bàn!".',
    )

    # UC07: Xem phiếu bán hàng
    style_heading_3("2.2.7. Use case 7: Xem phiếu bán hàng (UC07)")
    add_srs_table(
        "UC07",
        "Xem phiếu bán hàng",
        "Cho phép Nhân viên tra cứu, xem chi tiết thông tin và trạng thái của các phiếu bán hàng (đang chờ, đang phục vụ) để đối chiếu món hoặc in tạm tính cho khách hàng.",
        "Nhân viên (Staff / Thu ngân)",
        "Nhân viên cần kiểm tra món của bàn hoặc khách hàng yêu cầu xem trước hóa đơn tạm tính.",
        "Nhân viên đã đăng nhập thành công vào hệ thống.",
        "Thành công: Hiển thị đầy đủ chi tiết phiếu bán hàng gồm danh sách món, số lượng, đơn giá, thành tiền, giờ vào và mã nhân viên phục vụ.\nThất bại: Báo lỗi không tìm thấy phiếu.",
        '(1) Nhân viên chọn chức năng "Xem phiếu bán hàng" từ menu hoặc nhấp đúp vào bàn đang hoạt động.\n'
        "(2) Hệ thống hiển thị danh sách các phiếu bán hàng hiện hành.\n"
        "(3) Nhân viên chọn phiếu bán hàng cần xem.\n"
        "(4) Hệ thống hiển thị chi tiết phiếu: mã phiếu, tên bàn, nhân viên tạo, giờ tạo, danh sách món và tạm tính.\n"
        '(5) Nhân viên xem thông tin, có thể bấm "In tạm tính" cho khách kiểm tra trước khi tính tiền.',
        "(2a) Nhân viên sử dụng ô tìm kiếm nhanh theo mã phiếu hoặc số bàn để lọc phiếu mong muốn.",
        '(3.1) Phiếu bán hàng vừa bị hủy bởi thu ngân khác hoặc quản lý: Hệ thống thông báo "Phiếu không còn tồn tại trên hệ thống!".',
    )

    # UC08: Xem danh sách hóa đơn cá nhân
    style_heading_3("2.2.8. Use case 8: Xem danh sách hóa đơn cá nhân (UC08)")
    add_srs_table(
        "UC08",
        "Xem danh sách hóa đơn cá nhân",
        "Cho phép Nhân viên tra cứu danh sách toàn bộ các hóa đơn bán hàng do chính tài khoản của mình đã thực hiện lập và thu tiền trong ca làm việc, phục vụ việc kiểm kê tiền mặt và bàn giao ca.",
        "Nhân viên (Staff / Thu ngân)",
        "Nhân viên chuẩn bị hết ca làm việc hoặc cần đối soát các đơn hàng do mình phụ trách.",
        "Nhân viên đã đăng nhập tài khoản vào hệ thống.",
        "Thành công: Danh sách hóa đơn do nhân viên lập trong ngày/ca hiển thị kèm tổng số tiền mặt và chuyển khoản đã thu.\nThất bại: Thông báo lỗi tải dữ liệu.",
        '(1) Nhân viên chọn menu "Hóa đơn cá nhân" trên thanh điều hướng.\n'
        "(2) Hệ thống tự động lọc các hóa đơn có mã nhân viên trùng với tài khoản đang đăng nhập trong ngày hiện tại.\n"
        "(3) Màn hình hiển thị danh sách hóa đơn: Mã hóa đơn, Giờ lập, Số bàn, Tổng tiền, Hình thức thanh toán.\n"
        "(4) Phía dưới danh sách hiển thị tổng hợp: Tổng số hóa đơn, Tổng doanh số thu trong ca.\n"
        "(5) Nhân viên có thể bấm chọn từng hóa đơn để xem lại chi tiết các món đã bán.",
        "(2a) Nhân viên chọn lọc theo ngày làm việc trước đó để kiểm tra lại lịch sử ca cũ.",
        '(2.1) Trong ca chưa phát sinh hóa đơn thanh toán nào: Hệ thống hiển thị thông báo "Chưa có hóa đơn nào được lập trong ca làm việc hiện tại".',
    )

    # UC09: Quản lý loại đồ uống
    style_heading_3("2.2.9. Use case 9: Quản lý loại đồ uống (UC09)")
    add_srs_table(
        "UC09",
        "Quản lý loại đồ uống",
        "Cho phép Quản lý cửa hàng quản lý danh mục phân loại đồ uống (Cà phê, Trà trái cây, Đá xay, Nước ép), gồm xem danh sách, thêm loại mới, sửa tên/mô tả loại và xóa loại đồ uống không còn kinh doanh.",
        "Quản lý (Store Manager / Admin)",
        'Quản lý chọn mục "Quản lý loại đồ uống" trên thanh menu Quản trị.',
        "Đã đăng nhập vào hệ thống với vai trò Quản lý.",
        "Thành công: Danh mục loại đồ uống trong CSDL được cập nhật, đồng bộ ngay lập tức sang giao diện bán hàng của Nhân viên.\nThất bại: Báo lỗi, dữ liệu được hoàn nguyên (rollback).",
        '(1) Quản lý bấm chọn mục "Quản lý loại đồ uống".\n'
        "(2) Hệ thống tải và hiển thị danh sách tất cả các loại đồ uống hiện có.\n"
        '(3) Thêm mới: Quản lý nhấn "Thêm loại", nhập Mã loại, Tên loại đồ uống, Ghi chú rồi bấm "Lưu".\n'
        '(4) Cập nhật: Quản lý chọn một loại trên bảng, sửa tên/thông tin trên các ô nhập liệu và bấm "Cập nhật".\n'
        '(5) Xóa: Quản lý chọn một loại và bấm "Xóa", hệ thống hiển thị hộp thoại xác nhận.\n'
        "(6) Sau khi xác nhận, hệ thống kiểm tra ràng buộc và lưu vào CSDL, làm mới danh sách hiển thị.",
        "(2a) Quản lý nhập từ khóa vào ô tìm kiếm để lọc nhanh loại đồ uống theo tên.",
        '(3.1) Tên loại đồ uống bị để trống hoặc trùng với loại đã tồn tại: Hệ thống báo lỗi "Tên loại đồ uống đã tồn tại hoặc không hợp lệ!".\n'
        '(5.1) Loại đồ uống đang chứa các món đồ uống đang hoạt động: Hệ thống ngăn chặn xóa và thông báo "Không thể xóa loại đồ uống này vì vẫn còn các món đồ uống trực thuộc!".',
    )

    # UC10: Quản lý đồ uống
    style_heading_3("2.2.10. Use case 10: Quản lý đồ uống (UC10)")
    add_srs_table(
        "UC10",
        "Quản lý đồ uống",
        "Cho phép Quản lý quản lý toàn diện menu món đồ uống: thêm món mới, cập nhật giá bán, cập nhật size (S/M/L), đổi loại đồ uống, tải ảnh đại diện món và đổi trạng thái kinh doanh (Đang bán / Tạm ngưng).",
        "Quản lý (Store Manager / Admin)",
        'Quản lý chọn mục "Quản lý đồ uống" trên menu Quản trị.',
        "Đã đăng nhập hệ thống với quyền Quản lý.",
        "Thành công: Thông tin món đồ uống được cập nhật trong CSDL và phản ánh ngay lập tức trên menu bán hàng của Nhân viên.\nThất bại: Hệ thống báo lỗi, không lưu thay đổi.",
        '(1) Quản lý chọn chức năng "Quản lý đồ uống".\n'
        "(2) Hệ thống hiển thị bảng danh sách đồ uống (Mã món, Tên món, Loại đồ uống, Giá bán, Size, Trạng thái, Hình ảnh).\n"
        '(3) Thêm món: Quản lý nhấn "Thêm mới", nhập Tên món, chọn Loại đồ uống, nhập Giá bán, tải ảnh đại diện và nhấn "Lưu".\n'
        '(4) Sửa món: Quản lý chọn món cần chỉnh sửa trên bảng, điều chỉnh thông tin (sửa giá, sửa tên, đổi ảnh) và bấm "Cập nhật".\n'
        '(5) Đổi trạng thái: Quản lý chuyển trạng thái món sang "Tạm ngưng" khi hết nguyên liệu.\n'
        '(6) Xóa món: Quản lý nhấn "Xóa", hệ thống hiển thị xác nhận và kiểm tra ràng buộc hóa đơn cũ.\n'
        "(7) Hệ thống cập nhật CSDL và hiển thị thông báo thành công.",
        "(2a) Quản lý lọc đồ uống theo từng Loại danh mục hoặc tìm kiếm nhanh theo tên món.",
        '(3.1) Đơn giá nhập vào là số âm hoặc không phải số: Hệ thống báo lỗi "Đơn giá phải là số nguyên dương lớn hơn 0!".\n'
        "(6.1) Món đồ uống đã từng phát sinh trong hóa đơn bán hàng trước đây: Hệ thống chuyển sang cơ chế xóa mềm (Soft Delete - đổi trạng thái Ngừng bán) để đảm bảo toàn vẹn dữ liệu kế toán.",
    )

    # UC11: Quản lý nhân viên
    style_heading_3("2.2.11. Use case 11: Quản lý nhân viên (UC11)")
    add_srs_table(
        "UC11",
        "Quản lý nhân viên",
        "Cho phép Quản lý cửa hàng quản lý hồ sơ nhân viên: thêm nhân viên mới, phân công vai trò (Nhân viên / Quản lý), cập nhật thông tin liên hệ, đặt lại mật khẩu hoặc khóa tài khoản khi nhân viên nghỉ việc.",
        "Quản lý (Store Manager / Admin)",
        'Quản lý chọn mục "Quản lý nhân viên" trên giao diện quản trị.',
        "Đã đăng nhập với tài khoản Quản lý cấp cao.",
        "Thành công: Hồ sơ nhân viên và tài khoản đăng nhập được cập nhật trong CSDL.\nThất bại: Báo lỗi và giữ nguyên trạng thái cũ.",
        '(1) Quản lý chọn chức năng "Quản lý nhân viên".\n'
        "(2) Hệ thống hiển thị danh sách toàn bộ nhân viên cửa hàng kèm trạng thái tài khoản (Đang làm việc / Đã khóa).\n"
        '(3) Thêm nhân viên: Quản lý nhấn "Thêm mới", điền Họ tên, Tên đăng nhập, Mật khẩu khởi tạo, Số điện thoại, Email, Chức vụ và bấm "Lưu".\n'
        '(4) Sửa nhân viên: Quản lý chọn nhân viên trong danh sách, cập nhật thông tin liên lạc, lương cơ bản hoặc đổi vai trò rồi bấm "Cập nhật".\n'
        '(5) Khóa tài khoản: Khi nhân viên nghỉ việc, Quản lý chuyển trạng thái thành "Đã nghỉ việc / Khóa tài khoản".\n'
        "(6) Hệ thống ghi nhận vào CSDL và gửi thông báo xác nhận thành công.",
        '(3a) Đặt lại mật khẩu (Reset Password): Quản lý bấm "Reset Mật khẩu" cho nhân viên quên mật khẩu, hệ thống sinh mật khẩu mặc định (ví dụ: 123456) và yêu cầu đổi ở lần đăng nhập sau.',
        '(3.1) Tên đăng nhập hoặc Email đã tồn tại trong hệ thống: Hệ thống báo lỗi "Tên đăng nhập hoặc Email này đã có người sử dụng!".\n'
        '(5.1) Quản lý tự thao tác khóa tài khoản của chính mình: Hệ thống ngăn chặn với cảnh báo "Bạn không thể tự khóa tài khoản quản trị đang đăng nhập!".',
    )

    # UC12: Quản lý hóa đơn
    style_heading_3("2.2.12. Use case 12: Quản lý hóa đơn (UC12)")
    add_srs_table(
        "UC12",
        "Quản lý hóa đơn",
        "Cung cấp cho Quản lý công cụ tra cứu, kiểm soát toàn bộ các hóa đơn bán hàng đã phát sinh trong quán, lọc hóa đơn theo ngày/tháng/nhân viên, xem chi tiết từng đơn và xử lý hủy hóa đơn sai sót có lưu nhật ký kiểm toán.",
        "Quản lý (Store Manager / Admin)",
        'Quản lý truy cập chức năng "Quản lý hóa đơn" từ menu Quản trị.',
        "Đã đăng nhập hệ thống với quyền Quản lý.",
        "Thành công: Danh sách hóa đơn được truy vấn và hiển thị chính xác theo tiêu chí lọc; thao tác hủy đơn có nhật ký ghi nhận.\nThất bại: Báo lỗi truy vấn hoặc không tìm thấy hóa đơn.",
        '(1) Quản lý chọn menu "Quản lý hóa đơn".\n'
        "(2) Hệ thống tải danh sách các hóa đơn phát sinh trong ngày mặc định.\n"
        "(3) Quản lý thiết lập bộ lọc tra cứu: Chọn khoảng thời gian (Từ ngày - Đến ngày), lọc theo nhân viên thu ngân, hoặc tìm chính xác theo Mã hóa đơn.\n"
        "(4) Quản lý bấm vào một hóa đơn để xem chi tiết danh sách đồ uống, số lượng, giá bán, thời gian in, phương thức thanh toán và nhân viên phụ trách.\n"
        '(5) Quản lý có thể chọn in lại hóa đơn (In bản sao) hoặc xuất hóa đơn ra file PDF/Excel.',
        '(4a) Hủy hóa đơn sai sót: Quản lý bấm "Hủy hóa đơn", nhập bắt buộc lý do hủy (ví dụ: Khách hủy đơn đột xuất, tính nhầm món), hệ thống chuyển trạng thái sang "Đã hủy" và hoàn lại số liệu doanh thu.',
        '(4.1) Hủy hóa đơn mà không nhập lý do: Hệ thống cảnh báo "Bắt buộc phải nhập lý do hủy hóa đơn phục vụ kiểm toán!".',
    )

    # UC13: Báo cáo thống kê
    style_heading_3("2.2.13. Use case 13: Báo cáo thống kê (UC13)")
    add_srs_table(
        "UC13",
        "Báo cáo thống kê",
        "Cung cấp cho Quản lý các báo cáo tổng hợp và phân tích hoạt động kinh doanh của quán cà phê: tổng doanh thu theo ngày/tháng/năm, số lượng ly đồ uống tiêu thụ, top các món bán chạy nhất và hiệu suất bán hàng của từng nhân viên, hỗ trợ xuất báo cáo ra Excel.",
        "Quản lý (Store Manager / Admin)",
        'Quản lý chọn mục "Báo cáo thống kê" trên thanh công cụ Quản trị.',
        "Đã đăng nhập vào hệ thống với vai trò Quản lý.",
        "Thành công: Hiển thị đầy đủ số liệu thống kê, bảng chi tiết và biểu đồ trực quan; có thể xuất báo cáo ra file Excel.\nThất bại: Báo lỗi truy vấn hoặc không có dữ liệu giao dịch trong khoảng thời gian được chọn.",
        '(1) Quản lý truy cập màn hình "Báo cáo thống kê".\n'
        "(2) Hệ thống hiển thị mặc định tổng quan kinh doanh của ngày hôm nay (Doanh thu hôm nay, Số hóa đơn, Số ly đồ uống bán ra).\n"
        "(3) Quản lý lựa chọn loại báo cáo và khoảng thời gian:\n"
        "    + Thống kê theo ngày cụ thể hoặc theo khoảng ngày (Từ ngày... Đến ngày...).\n"
        "    + Thống kê theo tháng / năm.\n"
        "    + Thống kê theo danh mục món / đồ uống bán chạy nhất (Top 5 / Top 10).\n"
        "    + Thống kê doanh thu theo nhân viên trong từng ca.\n"
        '(4) Quản lý bấm nút "Xem báo cáo" (hoặc "Thống kê").\n'
        "(5) Hệ thống tổng hợp dữ liệu từ bảng Hóa đơn và Chi tiết hóa đơn trong CSDL, tính toán số liệu và kết xuất dữ liệu trực quan (Bảng số liệu, Biểu đồ cột/tròn).\n"
        '(6) Quản lý có thể chọn nút "Xuất file Excel" để lưu trữ báo cáo phục vụ kế toán cửa hàng.',
        '(6a) Quản lý chọn "In báo cáo": Hệ thống xuất bản in khổ A4 chuẩn biểu mẫu báo cáo tài chính của quán.',
        '(5.1) Khoảng thời gian lọc không phát sinh bất kỳ hóa đơn nào: Hệ thống hiển thị thông báo "Không có dữ liệu giao dịch trong khoảng thời gian đã chọn" với doanh thu hiển thị là 0 VNĐ.\n'
        '(3.1) Ngày bắt đầu lớn hơn ngày kết thúc: Hệ thống cảnh báo "Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc!".',
    )

    # Save output to C:\Net108Khai\Các Bài Lab\Lab1_NET108_QuanLyQuanCaPhe.docx
    output_dir = r"C:\Net108Khai\Các Bài Lab"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "Lab1_NET108_QuanLyQuanCaPhe.docx")
    doc.save(output_file)
    print(f"Document saved successfully at: {output_file}")
    return output_file

if __name__ == "__main__":
    generate_lab1_docx()
