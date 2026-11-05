# -*- coding: utf-8 -*-
"""
Script to build full, professional Lab 1 Report Word Document (.docx)
Topic: HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ AI-NATIVE (AI-NATIVE COMMERCE)
Course: DỰ ÁN .NET 1 (NET108) - Class: SD22302
School: TRƯỜNG CAO ĐẲNG FPT POLYTECHNIC ĐỒNG NAI
Instructor: ThS. Phan Hoàng Khải

Fixes:
1. Only ONE single cover page (no duplicate).
2. ONLY page 1 (cover page) has border frame. Page 2 onwards has NO borders.
3. Full Heading hierarchy (Heading 1, 2, 3, 4) with outlineLevel so that Word/WPS Navigation Pane displays the exact tree as in user screenshot.
4. Correct MSSVs and Jira tracking for NET108.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_lab1_document():
    doc = docx.Document()

    # Standard A4 Margins: Top 2.0cm, Bottom 2.0cm, Left 3.0cm (1.18in), Right 2.0cm
    for sec in doc.sections:
        sec.page_width = Inches(8.27)
        sec.page_height = Inches(11.69)
        sec.top_margin = Inches(0.79)
        sec.bottom_margin = Inches(0.79)
        sec.left_margin = Inches(1.18)
        sec.right_margin = Inches(0.79)

    # Helper: Set border on cover page ONLY
    def apply_cover_border(section):
        sectPr = section._sectPr
        for child in list(sectPr):
            if child.tag.endswith("pgBorders"):
                sectPr.remove(child)
        pg_borders = parse_xml(
            f'<w:pgBorders {nsdecls("w")} w:display="firstPage" w:offsetFrom="page">'
            f'  <w:top w:val="thinThickSmallGap" w:sz="24" w:space="24" w:color="1F4E79"/>'
            f'  <w:left w:val="thinThickSmallGap" w:sz="24" w:space="24" w:color="1F4E79"/>'
            f'  <w:bottom w:val="thickThinSmallGap" w:sz="24" w:space="24" w:color="1F4E79"/>'
            f'  <w:right w:val="thickThinSmallGap" w:sz="24" w:space="24" w:color="1F4E79"/>'
            f'</w:pgBorders>'
        )
        sectPr.append(pg_borders)

    # Helper: Ensure NO borders on subsequent sections
    def remove_borders(section):
        sectPr = section._sectPr
        for child in list(sectPr):
            if child.tag.endswith("pgBorders"):
                sectPr.remove(child)
        no_borders = parse_xml(
            f'<w:pgBorders {nsdecls("w")} w:display="allPages">'
            f'  <w:top w:val="none"/>'
            f'  <w:left w:val="none"/>'
            f'  <w:bottom w:val="none"/>'
            f'  <w:right w:val="none"/>'
            f'</w:pgBorders>'
        )
        sectPr.append(no_borders)

    # Helper: Set header and footer
    def setup_header_footer(section, header_title=None, is_linked=False):
        section.header.is_linked_to_previous = is_linked
        section.footer.is_linked_to_previous = is_linked

        if header_title:
            hdr = section.header
            for p in hdr.paragraphs:
                p.text = ""
            p_hdr = hdr.paragraphs[0]
            p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p_hdr.paragraph_format.space_after = Pt(4)
            r = p_hdr.add_run(header_title)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.color.rgb = RGBColor(100, 100, 100)

            # Bottom line under header
            pPr = p_hdr._p.get_or_add_pPr()
            pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="3" w:color="A0A0A0"/></w:pBdr>')
            pPr.append(pBdr)

        # Footer: Trang [PAGE]
        ftr = section.footer
        p_ftr = ftr.paragraphs[0] if ftr.paragraphs else ftr.add_paragraph()
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_ftr.text = ""
        r_f = p_ftr.add_run("Trang ")
        r_f.font.name = "Times New Roman"
        r_f.font.size = Pt(10)
        r_f.font.color.rgb = RGBColor(110, 110, 110)
        fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
        p_ftr._p.append(fld)

    # Heading helpers that guarantee appearance in Word & WPS Navigation Pane
    def add_h1(text):
        p = doc.add_heading(text, level=1)
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        pPr = p._p.get_or_add_pPr()
        for child in list(pPr):
            if child.tag.endswith("outlineLvl"):
                pPr.remove(child)
        pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="0"/>'))
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(14)
            r.font.bold = True
            r.font.color.rgb = RGBColor(31, 78, 121)
        return p

    def add_h2(text):
        p = doc.add_heading(text, level=2)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        pPr = p._p.get_or_add_pPr()
        for child in list(pPr):
            if child.tag.endswith("outlineLvl"):
                pPr.remove(child)
        pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="1"/>'))
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(13)
            r.font.bold = True
            r.font.color.rgb = RGBColor(46, 117, 182)
        return p

    def add_h3(text):
        p = doc.add_heading(text, level=3)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        pPr = p._p.get_or_add_pPr()
        for child in list(pPr):
            if child.tag.endswith("outlineLvl"):
                pPr.remove(child)
        pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="2"/>'))
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 32, 96)
        return p

    def add_h4(text):
        p = doc.add_heading(text, level=4)
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        pPr = p._p.get_or_add_pPr()
        for child in list(pPr):
            if child.tag.endswith("outlineLvl"):
                pPr.remove(child)
        pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="3"/>'))
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(11.5)
            r.font.bold = True
            r.font.italic = True
            r.font.color.rgb = RGBColor(46, 117, 182)
        return p

    def p_body(text, bold_prefix="", italic=False, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.25
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
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

    def p_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.2
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(12)
            r_pre.font.bold = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        return p

    def create_table(rows_data, col_widths, headers=None):
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
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
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
                    r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="C0C0C0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="C0C0C0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="C0C0C0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="C0C0C0"/></w:tcBorders>'.format(
                        nsdecls("w")
                    )
                )
                cell._tc.get_or_add_tcPr().append(tcBorders)
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
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
            ["ExceptionFlow", exc_flow],
        ]
        t = doc.add_table(rows=10, cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        col_w_lbl = Inches(1.8)
        col_w_val = Inches(4.5)

        for r_idx, row in enumerate(data):
            r = t.rows[r_idx]
            cell_lbl = r.cells[0]
            cell_val = r.cells[1]
            cell_lbl.width = col_w_lbl
            cell_val.width = col_w_val

            cell_lbl.text = row[0]
            cell_val.text = row[1]

            shd_lbl = parse_xml(r'<w:shd {} w:fill="EBF1F5"/>'.format(nsdecls("w")))
            cell_lbl._tc.get_or_add_tcPr().append(shd_lbl)

            borders = parse_xml(
                r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/></w:tcBorders>'.format(
                    nsdecls("w")
                )
            )
            cell_lbl._tc.get_or_add_tcPr().append(borders)
            cell_val._tc.get_or_add_tcPr().append(parse_xml(
                r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/></w:tcBorders>'.format(
                    nsdecls("w")
                )
            ))

            p0 = cell_lbl.paragraphs[0]
            p0.paragraph_format.space_before = Pt(2)
            p0.paragraph_format.space_after = Pt(2)
            if p0.runs:
                p0.runs[0].font.name = "Times New Roman"
                p0.runs[0].font.bold = True
                p0.runs[0].font.size = Pt(11)

            p1 = cell_val.paragraphs[0]
            p1.paragraph_format.space_before = Pt(2)
            p1.paragraph_format.space_after = Pt(2)
            p1.paragraph_format.line_spacing = 1.15
            if p1.runs:
                p1.runs[0].font.name = "Times New Roman"
                p1.runs[0].font.size = Pt(11)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==================== SECTION 0: TRANG BÌA CHÍNH (CHỈ 1 TRANG DUY NHẤT CÓ KHUNG VIỀN) ====================
    sec_cover = doc.sections[0]
    apply_cover_border(sec_cover)
    sec_cover.header.is_linked_to_previous = False
    sec_cover.footer.is_linked_to_previous = False

    p_c1 = doc.add_paragraph()
    p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c1.paragraph_format.space_before = Pt(20)
    r = p_c1.add_run("TRƯỜNG CAO ĐẲNG FPT POLYTECHNIC ĐỒNG NAI\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(242, 107, 33) # FPT Orange

    r = p_c1.add_run("KHOA CÔNG NGHỆ THÔNG TIN\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(31, 78, 121)

    r_star = p_c1.add_run("---***---\n")
    r_star.font.bold = True
    r_star.font.color.rgb = RGBColor(120, 120, 120)

    p_c2 = doc.add_paragraph()
    p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c2.paragraph_format.space_before = Pt(40)
    p_c2.paragraph_format.space_after = Pt(15)

    r = p_c2.add_run("BÁO CÁO LAB 1\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(24)
    r.font.bold = True
    r.font.color.rgb = RGBColor(31, 78, 121)

    r = p_c2.add_run("DỰ ÁN MÔN HỌC .NET 1 (NET108) - LỚP: SD22302\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(60, 60, 60)

    r = p_c2.add_run("ĐỀ TÀI:\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.italic = True

    r = p_c2.add_run("XÂY DỰNG HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ\nAI-NATIVE (AI-NATIVE COMMERCE)\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = RGBColor(242, 107, 33)

    p_c3 = doc.add_paragraph()
    p_c3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c3.paragraph_format.space_before = Pt(35)
    p_c3.paragraph_format.line_spacing = 1.3

    r = p_c3.add_run("GIẢNG VIÊN HƯỚNG DẪN:\n")
    r.font.bold = True
    r.font.size = Pt(12)
    r = p_c3.add_run("ThS. Phan Hoàng Khải\n\n")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(31, 78, 121)

    r = p_c3.add_run("NHÓM SINH VIÊN THỰC HIỆN: NHÓM 5\n")
    r.font.bold = True
    r.font.size = Pt(12)

    members_text = (
        "1. Trần Phúc Thiên (Nhóm trưởng - MSSV: TB02226)\n"
        "2. Trần Phạm Hoàng Minh (Thành viên - MSSV: TB02231)\n"
        "3. Cho Hoàng Hiếu Trung (Thành viên - MSSV: TB02324)\n"
        "4. Nguyễn Hoàng Quốc Anh (Thành viên - MSSV: TB02232)\n"
        "5. Nguyễn Châu Văn Phát (Thành viên - MSSV: TB02274)\n"
    )
    r = p_c3.add_run(members_text)
    r.font.size = Pt(12)

    p_c4 = doc.add_paragraph()
    p_c4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c4.paragraph_format.space_before = Pt(45)
    r = p_c4.add_run("ĐỒNG NAI, NĂM 2026")
    r.font.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(100, 100, 100)

    # ==================== SECTION 1: NỘI DUNG TỪ TRANG 2 TRỞ ĐI (HOÀN TOÀN KHÔNG CÓ KHUNG VIỀN) ====================
    sec_body = doc.add_section()
    remove_borders(sec_body)
    setup_header_footer(sec_body, "BÁO CÁO LAB 1 - NET108 | NHÓM 5")

    # Trang Nhận xét & Đánh giá
    p_nx = doc.add_paragraph()
    p_nx.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_nx = p_nx.add_run("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN\n")
    r_nx.font.name = "Times New Roman"
    r_nx.font.size = Pt(14)
    r_nx.font.bold = True
    r_nx.font.color.rgb = RGBColor(31, 78, 121)

    p_body("Họ và tên giảng viên: ThS. Phan Hoàng Khải")
    p_body("Bộ môn: Công nghệ thông tin - Trường Cao đẳng FPT Polytechnic Đồng Nai")
    p_body("1. Đánh giá về tiến độ và thái độ thực hiện của nhóm:")
    for _ in range(3):
        doc.add_paragraph("....................................................................................................................................................................")
    p_body("2. Đánh giá chất lượng báo cáo Lab 1 (Khảo sát AI, Giới thiệu & Phân tích Use Case SRS):")
    for _ in range(4):
        doc.add_paragraph("....................................................................................................................................................................")
    p_body("3. Điểm đánh giá:")
    doc.add_paragraph("Điểm số: .................... / 10               Điểm chữ: ..............................................................")
    doc.add_paragraph("\n                                                                                            Đồng Nai, ngày ..... tháng ..... năm 2026")
    doc.add_paragraph("                                                                                                               Giảng viên hướng dẫn\n\n\n")
    doc.add_paragraph("                                                                                                              ThS. Phan Hoàng Khải")

    doc.add_page_break()
    p_kh = doc.add_paragraph()
    p_kh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_kh = p_kh.add_run("KẾ HOẠCH THỰC HIỆN VÀ THEO DÕI JIRA CLOUD\n")
    r_kh.font.name = "Times New Roman"
    r_kh.font.size = Pt(14)
    r_kh.font.bold = True
    r_kh.font.color.rgb = RGBColor(31, 78, 121)

    p_body(
        "Nhóm 5 áp dụng quy trình Agile / Scrum trong khuôn khổ môn NET108, toàn bộ kế hoạch triển khai đề tài AI-Native Commerce được cấu trúc thành các Epic và Task, theo dõi trực tiếp trên hệ thống Atlassian Jira Cloud (Workspace: thientptb02226.atlassian.net - Project: NET108):"
    )

    jira_headers = ["Mã Jira", "Hạng mục triển khai đồ án NET108", "Loại", "Người phụ trách (MSSV)", "Tiến độ"]
    jira_data = [
        ["NET-2", "[EPIC 1] Lab 1: Khảo sát AI, Giới thiệu Dự án & Đặc tả SRS", "Epic", "Trần Phúc Thiên (TB02226)", "Hoàn thành"],
        ["NET-3", "NET108-L1.1: Khảo sát AI (Perplexity, ChatGPT, Gemini) & Prompt log", "Task", "Trần Phúc Thiên (TB02226)", "100%"],
        ["NET-4", "NET108-L1.2: Phân tích hiện trạng, tính cấp thiết và đề xuất hệ thống", "Task", "Cho Hoàng Hiếu Trung (TB02324)", "100%"],
        ["NET-5", "NET108-L1.3: Xác định Actors (Customer, Merchant, Agent) & Phân quyền", "Task", "Nguyễn Hoàng Quốc Anh (TB02232)", "100%"],
        ["NET-6", "NET108-L1.4: Xây dựng sơ đồ Use Case tổng quát & Sơ đồ phân rã module", "Task", "Trần Phạm Hoàng Minh (TB02231)", "100%"],
        ["NET-7", "NET108-L1.5: Viết tài liệu đặc tả yêu cầu hệ thống (SRS chi tiết 14 UCs)", "Task", "Toàn bộ Nhóm 5", "100%"],
        ["NET-8", "[EPIC 2] Lab 2: Thiết kế Kiến trúc & Cơ sở Dữ liệu Hệ thống", "Epic", "Trần Phạm Hoàng Minh (TB02231)", "Sắp tới"],
        ["NET-9", "NET108-L2.1: Thiết kế kiến trúc tổng thể 7 lớp (Experience đến Infra)", "Task", "Trần Phạm Hoàng Minh (TB02231)", "Chưa bắt đầu"],
        ["NET-10", "NET108-L2.2: Thiết kế sơ đồ ERD và Data DDL (SQL Server)", "Task", "Cho Hoàng Hiếu Trung (TB02324)", "Chưa bắt đầu"],
        ["NET-11", "NET108-L2.3: Thiết kế Schema Agentic Commerce Protocol (ACP)", "Task", "Nguyễn Châu Văn Phát (TB02274)", "Chưa bắt đầu"],
        ["NET-12", "[EPIC 3] Lab 3: Thiết kế Giao diện (UI/UX) & Phát triển API Core", "Epic", "Cho Hoàng Hiếu Trung (TB02324)", "Sắp tới"],
        ["NET-13", "NET108-L3.1: Thiết kế UI Web, Mobile và Conversational Widget", "Task", "Nguyễn Hoàng Quốc Anh (TB02232)", "Chưa bắt đầu"],
        ["NET-14", "NET108-L3.2: Phát triển Backend API Core (.NET / C#) và JWT / RBAC", "Task", "Trần Phúc Thiên (TB02226)", "Chưa bắt đầu"],
        ["NET-15", "NET108-L3.3: Hiện thực hóa Module Cart, Checkout & Payment Gateway", "Task", "Nguyễn Châu Văn Phát (TB02274)", "Chưa bắt đầu"],
        ["NET-16", "[EPIC 4] Lab 4: Tích hợp AI Agent Platform, RAG & Triển khai", "Epic", "Nguyễn Hoàng Quốc Anh (TB02232)", "Sắp tới"],
        ["NET-17", "NET108-L4.1: Tích hợp AI Shopping Assistant & Intent Router", "Task", "Trần Phúc Thiên (TB02226)", "Chưa bắt đầu"],
        ["NET-18", "NET108-L4.2: Xây dựng Agentic Search & RAG Vector Database", "Task", "Trần Phạm Hoàng Minh (TB02231)", "Chưa bắt đầu"],
        ["NET-19", "NET108-L4.3: Kiểm thử toàn diện, Docker hóa và đóng gói đồ án", "Task", "Toàn bộ Nhóm 5", "Chưa bắt đầu"],
    ]
    create_table(jira_data, [Inches(0.8), Inches(2.8), Inches(0.6), Inches(1.5), Inches(0.8)], jira_headers)

    # ==================== HEADING 1: MỤC LỤC ====================
    doc.add_page_break()
    add_h1("MỤC LỤC")

    toc_rows = [
        ["NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", "..................................................................................................", "2"],
        ["KẾ HOẠCH THỰC HIỆN VÀ THEO DÕI JIRA CLOUD", "..................................................................................................", "3"],
        ["DANH MỤC BẢNG", "..................................................................................................", "4"],
        ["DANH MỤC HÌNH", "..................................................................................................", "5"],
        ["PHẦN MỞ ĐẦU", "..................................................................................................", "6"],
        ["  1.1. Tính cấp thiết của đề tài", "..................................................................................................", "6"],
        ["  1.2. Mục tiêu của đề tài", "..................................................................................................", "6"],
        ["  1.3. Đối tượng và phạm vi nghiên cứu", "..................................................................................................", "7"],
        ["  1.4. Phương pháp nghiên cứu", "..................................................................................................", "7"],
        ["PHẦN NỘI DUNG", "..................................................................................................", "8"],
        ["CHƯƠNG 1: CƠ SỞ LÝ THUYẾT VÀ ỨNG DỤNG AI (BÀI 1 & BÀI 2)", "..................................................................................................", "8"],
        ["  1.1. Giới thiệu về Technical Stack", "..................................................................................................", "8"],
        ["    1.1.1. Technical Stack là gì?", "..................................................................................................", "8"],
        ["    1.1.2. Một số Stack thông dụng", "..................................................................................................", "8"],
        ["  1.2. Giới thiệu về AI-Native Commerce Stack", "..................................................................................................", "9"],
        ["    1.2.1. Định nghĩa AI-Native Commerce Stack", "..................................................................................................", "9"],
        ["    1.2.2. Cách thức hoạt động của AI-Native Commerce", "..................................................................................................", "9"],
        ["    1.2.3. Vai trò của AI Agent Platform", "..................................................................................................", "10"],
        ["  1.3. Ứng dụng AI trong tìm kiếm thông tin (Bài 1 - 2.0 Điểm)", "..................................................................................................", "10"],
        ["    1.3.1. Khảo sát mẫu tài liệu đặc tả SRS bằng Perplexity AI", "..................................................................................................", "10"],
        ["    1.3.2. Nghiên cứu nghiệp vụ AI Commerce bằng ChatGPT Deepsearch", "..................................................................................................", "11"],
        ["    1.3.3. Nghiên cứu hệ thống Multi-Agent bằng Google Gemini", "..................................................................................................", "11"],
        ["    1.3.4. Nhật ký Prompting chi tiết", "..................................................................................................", "12"],
        ["    1.3.5. Đánh giá, đối sánh và chọn lọc giải pháp từ kết quả AI", "..................................................................................................", "13"],
        ["  1.4. Giới thiệu tổng quan dự án AI-Native Commerce (Bài 2 - 4.0 Điểm)", "..................................................................................................", "14"],
        ["    1.4.1. Khái niệm và bối cảnh hình thành hệ thống", "..................................................................................................", "14"],
        ["    1.4.2. Phân tích hiện trạng thị trường và nhu cầu khách hàng", "..................................................................................................", "14"],
        ["    1.4.3. Các thành phần người dùng (Actors) trong hệ thống", "..................................................................................................", "15"],
        ["    1.4.4. Danh mục các module chức năng hệ thống", "..................................................................................................", "16"],
        ["    1.4.5. Phân tích luồng hoạt động tổng thể và sự liên kết", "..................................................................................................", "17"],
        ["CHƯƠNG 2: KHẢO SÁT VÀ PHÂN TÍCH YÊU CẦU (BÀI 3 - 4.0 ĐIỂM)", "..................................................................................................", "19"],
        ["  2.1. Khảo sát hiện trạng và quy tắc vẽ Use Case (Bài 3)", "..................................................................................................", "19"],
        ["    2.1.1. Khảo sát các giải pháp E-Commerce hiện nay", "..................................................................................................", "19"],
        ["    2.1.2. Các quy tắc vẽ sơ đồ Use Case UML chuẩn", "..................................................................................................", "19"],
        ["  2.2. Sơ đồ Use Case tổng quát hệ thống AI-Native Commerce", "..................................................................................................", "20"],
        ["  2.3. Sơ đồ Use Case phân rã theo phân hệ", "..................................................................................................", "22"],
        ["    2.3.1. Phân hệ Khách hàng (Guest & Customer)", "..................................................................................................", "22"],
        ["    2.3.2. Phân hệ Quản trị & Nhà bán hàng (Merchant & Admin)", "..................................................................................................", "23"],
        ["    2.3.3. Phân hệ Nền tảng Tác tử AI (AI Agent Platform)", "..................................................................................................", "24"],
        ["  2.4. Phân loại danh sách chức năng theo từng Actor", "..................................................................................................", "25"],
        ["    2.4.1. Chức năng của Guest", "..................................................................................................", "25"],
        ["    2.4.2. Chức năng của User / Customer", "..................................................................................................", "25"],
        ["    2.4.3. Chức năng của Admin / Merchant", "..................................................................................................", "26"],
        ["    2.4.4. Chức năng của AI Agent Platform", "..................................................................................................", "26"],
        ["  2.5. Đặc tả chi tiết các Use Cases cốt lõi (14 bảng SRS chuẩn FPT)", "..................................................................................................", "27"],
        ["TÀI LIỆU THAM KHẢO", "..................................................................................................", "41"],
    ]
    t_toc = doc.add_table(rows=len(toc_rows), cols=3)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_toc.autofit = False
    for r_idx, row in enumerate(toc_rows):
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
            if row[0].startswith("PHẦN") or row[0].startswith("CHƯƠNG") or row[0].startswith("MỤC"):
                p.runs[0].font.bold = True
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(11)

    # ==================== HEADING 1: DANH MỤC BẢNG ====================
    doc.add_page_break()
    add_h1("DANH MỤC BẢNG")
    p_body("Bảng 1. Kế hoạch thực hiện đề tài và theo dõi trên Jira Cloud\t.....................................................................\t3")
    p_body("Bảng 2. Bảng nhật ký Prompting khảo sát AI (Perplexity, ChatGPT, Gemini)\t..................................................\t12")
    p_body("Bảng 3. Bảng phân tích thành phần tác nhân (Actors) trong hệ thống\t.......................................................\t15")
    p_body("Bảng 4. Bảng danh mục 16 module nền tảng hệ thống AI-Native Commerce\t...................................................\t16")
    p_body("Bảng 5. Chức năng của Khách vãng lai (Guest)\t................................................................................\t25")
    p_body("Bảng 6. Chức năng của Khách hàng (User / Customer)\t..........................................................................\t25")
    p_body("Bảng 7. Chức năng của Quản trị viên & Nhà bán hàng (Admin / Merchant)\t....................................................\t26")
    p_body("Bảng 8. Chức năng của Nền tảng Tác tử AI (AI Agent Platform)\t..............................................................\t26")
    p_body("Bảng 9. <Guest> UC01 - Đăng ký tài khoản người dùng\t........................................................................\t27")
    p_body("Bảng 10. <User> UC02 - Đăng nhập hệ thống\t..................................................................................\t28")
    p_body("Bảng 11. <User> UC03 - Quên mật khẩu\t......................................................................................\t29")
    p_body("Bảng 12. <User> UC04 - Tìm kiếm sản phẩm bằng ngôn ngữ tự nhiên\t...........................................................\t30")
    p_body("Bảng 13. <User> UC05 - Mua sắm tương tác với Trợ lý AI\t.....................................................................\t31")
    p_body("Bảng 14. <User> UC06 - Quản lý giỏ hàng thông minh\t..........................................................................\t32")
    p_body("Bảng 15. <User> UC07 - Đặt hàng và áp dụng khuyến mãi tự động\t..............................................................\t33")
    p_body("Bảng 16. <User> UC08 - Thanh toán trực tuyến qua VNPay\t.....................................................................\t34")
    p_body("Bảng 17. <User> UC09 - Tra cứu đơn hàng và theo dõi vận chuyển\t.............................................................\t35")
    p_body("Bảng 18. <Admin> UC10 - Quản lý danh mục & sản phẩm chuẩn hóa cho AI\t........................................................\t36")
    p_body("Bảng 19. <Admin> UC11 - Quản lý đơn hàng và trạng thái đơn hàng\t............................................................\t37")
    p_body("Bảng 20. <Admin> UC12 - Quản lý tài khoản và phân quyền RBAC\t................................................................\t38")
    p_body("Bảng 21. <Admin> UC13 - Báo cáo thống kê và phân tích hành vi AI\t............................................................\t39")
    p_body("Bảng 22. <AI Agent> UC14 - Thực thi giao dịch qua giao thức tác tử ACP\t.....................................................\t40")

    # ==================== HEADING 1: DANH MỤC HÌNH ====================
    doc.add_page_break()
    add_h1("DANH MỤC HÌNH")
    p_body("Hình 1. Định nghĩa mô hình kiến trúc AI-Native Commerce so với E-Commerce truyền thống\t....................................\t9")
    p_body("Hình 2. Sơ đồ Use Case tổng quát Hệ thống Thương mại Điện tử AI-Native\t.......................................................\t21")
    p_body("Hình 3. Sơ đồ Use Case Phân hệ Khách hàng (Guest & Customer)\t................................................................\t22")
    p_body("Hình 4. Sơ đồ Use Case Phân hệ Quản trị & Nhà bán hàng (Merchant & Admin)\t..................................................\t23")
    p_body("Hình 5. Sơ đồ Use Case Phân hệ Nền tảng Tác tử AI (AI Agent Platform)\t......................................................\t24")

    # ==================== HEADING 1: PHẦN MỞ ĐẦU ====================
    doc.add_page_break()
    add_h1("PHẦN MỞ ĐẦU")

    add_h2("1.1. Tính cấp thiết của đề tài")
    p_body(
        "Thương mại điện tử (E-Commerce) đã trải qua nhiều giai đoạn phát triển, từ các website bán hàng tĩnh (Web 1.0) đến các sàn giao dịch tương tác quy mô lớn (Web 2.0). Tuy nhiên, hầu hết các nền tảng thương mại điện tử hiện nay vẫn đang vận hành dựa trên cơ chế tìm kiếm từ khóa cứng nhắc (Keyword Search), duyệt danh mục phân tầng và giao diện tĩnh thụ động. Khi người tiêu dùng đối mặt với hàng triệu sản phẩm, việc tìm kiếm một món hàng phù hợp với nhu cầu ngữ cảnh cụ thể (ví dụ: 'Tìm một chiếc laptop mỏng nhẹ dưới 20 triệu cho sinh viên công nghệ, pin bền và lập trình mượt mà') trở nên vô cùng tốn thời gian và mệt mỏi."
    )
    p_body(
        "Sự bùng nổ của Trí tuệ Nhân tạo Tạo sinh (Generative AI), Mô hình Ngôn ngữ Lớn (LLM) và Kiến trúc Tác tử Tự hành (Autonomous AI Agents) đã mở ra một kỷ nguyên hoàn toàn mới: AI-Native Commerce. Đây không đơn thuần là việc gắn thêm một chatbot hỗ trợ ở góc màn hình, mà là tái cấu trúc toàn diện kiến trúc thương mại lấy AI làm trung tâm, nơi AI Agent tham gia trực tiếp vào việc thấu hiểu nhu cầu, tư vấn ngữ cảnh, so sánh giá cả, đề xuất ưu đãi tự động và thực thi giao dịch an toàn thông qua giao thức Agentic Commerce Protocol (ACP)."
    )
    p_body(
        "Nhận thức được xu thế tất yếu đó, Nhóm 5 lựa chọn đề tài 'Xây dựng Hệ thống Thương mại Điện tử AI-Native (AI-Native Commerce)' cho học phần Dự án .NET 1 (NET108) nhằm nghiên cứu, mô hình hóa và hiện thực hóa một giải pháp thương mại điện tử thông minh, an toàn và có tính ứng dụng cao."
    )

    add_h2("1.2. Mục tiêu của đề tài")
    p_bullet("Xây dựng nền tảng thương mại điện tử thế hệ mới lấy AI làm hạt nhân điều phối giao dịch và tương tác khách hàng.", "Mục tiêu tổng quát: ")
    p_bullet("Nghiên cứu ứng dụng các công cụ AI hiện đại (Perplexity AI, ChatGPT Deepsearch, Google Gemini) trong khảo sát và đặc tả SRS.", "Mục tiêu khảo sát: ")
    p_bullet("Phát triển tính năng tìm kiếm bằng ngôn ngữ tự nhiên (Natural Language Discovery) và Trợ lý mua sắm AI (Shopping Assistant).", "Mục tiêu nghiệp vụ: ")
    p_bullet("Mô hình hóa toàn diện hệ thống bằng UML chuẩn quốc tế: Sơ đồ Use Case tổng quát, sơ đồ phân rã phân hệ và 14 bảng đặc tả SRS 10 hàng chuẩn FPT Polytechnic.", "Mục tiêu phân tích: ")
    p_bullet("Thiết lập giao thức giao dịch thương mại tác tử (Agentic Commerce Protocol - ACP) chuẩn hóa cho các AI Agent thực thi giao dịch.", "Mục tiêu kiến trúc: ")

    add_h2("1.3. Đối tượng và phạm vi nghiên cứu")
    p_body(
        "Đối tượng nghiên cứu: Kiến trúc hệ thống thương mại điện tử tích hợp AI; các quy trình nghiệp vụ mua sắm hội thoại (Conversational Commerce); mô hình phân quyền vai trò (RBAC); và các giao thức kết nối Agentic Commerce.",
        bold_prefix="Đối tượng nghiên cứu: "
    )
    p_body(
        "Phạm vi báo cáo Lab 1: Tập trung nghiên cứu khảo sát bằng AI (Bài 1), xây dựng tài liệu giới thiệu dự án (Bài 2), mô hình hóa sơ đồ Use Case và viết tài liệu đặc tả yêu cầu phần mềm SRS chi tiết cho 14 ca sử dụng cốt lõi (Bài 3). Các nội dung về thiết kế CSDL chi tiết, API Backend và kiểm thử sẽ được triển khai trong các bài Lab tiếp theo.",
        bold_prefix="Phạm vi bài Lab 1: "
    )

    add_h2("1.4. Phương pháp nghiên cứu")
    p_bullet("Sử dụng các công cụ Generative AI hàng đầu ở chế độ Deepsearch để nghiên cứu các bài toán kỹ thuật và nghiệp vụ phức tạp.", "Phương pháp nghiên cứu AI: ")
    p_bullet("Sử dụng ngôn ngữ mô hình hóa UML để trực quan hóa cấu trúc, hành vi và phân quyền người dùng trong hệ thống.", "Phương pháp mô hình hóa: ")
    p_bullet("Áp dụng khung làm việc Agile / Scrum, quản lý toàn bộ các hạng mục triển khai qua Jira Cloud (thientptb02226.atlassian.net) với Project NET108.", "Phương pháp quản lý dự án: ")

    # ==================== HEADING 1: PHẦN NỘI DUNG ====================
    doc.add_page_break()
    add_h1("PHẦN NỘI DUNG")

    # ---------- CHƯƠNG 1 ----------
    add_h2("CHƯƠNG 1: CƠ SỞ LÝ THUYẾT VÀ ỨNG DỤNG AI")

    add_h3("1.1. Giới thiệu về Technical Stack")
    add_h4("1.1.1. Technical Stack là gì?")
    p_body(
        "Technical Stack (Ngăn xếp công nghệ) là một tập hợp các công nghệ phần mềm, thư viện, ngôn ngữ lập trình, hệ quản trị cơ sở dữ liệu và cơ sở hạ tầng phối hợp chặt chẽ với nhau để xây dựng và vận hành một ứng dụng hoàn chỉnh. Một Technical Stack điển hình bao gồm tầng giao diện người dùng (Frontend), tầng xử lý nghiệp vụ (Backend), tầng lưu trữ dữ liệu (Database) và tầng hạ tầng triển khai (DevOps/Cloud)."
    )

    add_h4("1.1.2. Một số Stack thông dụng")
    p_body(
        "Trong ngành công nghiệp phần mềm hiện nay, một số Technical Stack phổ biến bao gồm:\n"
        "- MERN Stack: MongoDB, ExpressJS, ReactJS, NodeJS (phổ biến cho các ứng dụng web JavaScript).\n"
        "- LAMP Stack: Linux, Apache, MySQL, PHP (ngăn xếp mã nguồn mở truyền thống).\n"
        "- .NET Enterprise Stack: C#, ASP.NET Core, Microsoft SQL Server, Entity Framework Core (tiêu chuẩn vàng cho các hệ thống doanh nghiệp, thương mại điện tử quy mô lớn đòi hỏi tính ổn định, bảo mật cao và hiệu năng xử lý giao dịch vượt trội)."
    )

    add_h3("1.2. Giới thiệu về AI-Native Commerce Stack")
    add_h4("1.2.1. Định nghĩa AI-Native Commerce Stack")
    p_body(
        "AI-Native Commerce Stack là sự kết hợp đột phá giữa nền tảng ứng dụng doanh nghiệp chuẩn Microsoft .NET 8 / C# với hệ sinh thái Trí tuệ Nhân tạo Tạo sinh (Generative AI) và Cơ sở dữ liệu Vector (Vector Database). Trong ngăn xếp này, AI không phải là một module phụ trợ bên ngoài mà được tích hợp ngay tại tầng điều phối lõi (AI Orchestration Layer)."
    )

    add_h4("1.2.2. Cách thức hoạt động của AI-Native Commerce")
    p_body(
        "Hệ thống vận hành theo cơ chế vòng lặp tương tác đa tác tử (Multi-Agent Loop):\n"
        "(1) Người dùng đưa ra yêu cầu bằng ngôn ngữ tự nhiên qua giao diện Web/Mobile/Chat.\n"
        "(2) Bộ định tuyến ý định (Intent Router) phân tích ngữ cảnh và chuyển tiếp cho Tác tử chuyên trách (Shopping Agent, Search Agent, Support Agent).\n"
        "(3) AI Agent gọi các Tool API an toàn để truy vấn cơ sở dữ liệu sản phẩm, kiểm tra tồn kho và áp dụng voucher khuyến mãi.\n"
        "(4) Giao thức Agentic Commerce Protocol (ACP) giám sát và xác thực lệnh mua sắm trước khi gửi đến Cổng thanh toán trực tuyến."
    )

    add_h4("1.2.3. Vai trò của AI Agent Platform")
    p_body(
        "AI Agent Platform đóng vai trò là 'bộ não điều hành' của hệ thống, giúp xóa bỏ rào cản duyệt web truyền thống, mang lại trải nghiệm mua sắm siêu cá nhân hóa (Hyper-personalized Shopping), tối ưu hóa tỷ lệ chuyển đổi cho nhà bán hàng và giảm thiểu 80% thời gian xử lý khiếu nại khách hàng."
    )

    add_h3("1.3. Ứng dụng AI trong tìm kiếm thông tin (Bài 1 - 2.0 Điểm)")
    add_h4("1.3.1. Khảo sát mẫu tài liệu đặc tả SRS bằng Perplexity AI")
    p_body(
        "Nhóm 5 đã sử dụng Perplexity AI (https://www.perplexity.ai/) với chế độ Pro Search để tìm kiếm các tài liệu đặc tả yêu cầu phần mềm chuẩn quốc tế (IEEE 830) và mẫu tài liệu của FPT Polytechnic. Kết quả thu được giúp nhóm chuẩn hóa bảng phân tích Use Case 10 trường dữ liệu bắt buộc: Use Case ID, Use Case, Short Description, Actors, Trigger, Pre-conditions, Post-conditions, Main Flow, Alternative Flow và ExceptionFlow."
    )

    add_h4("1.3.2. Nghiên cứu nghiệp vụ AI Commerce bằng ChatGPT Deepsearch")
    p_body(
        "Bằng việc kích hoạt chế độ Deepsearch trên ChatGPT, nhóm đã phân tích sâu các bài toán thực tiễn trong thương mại điện tử AI-Native: cơ chế hội thoại thông minh, nhận diện ý định mua hàng (Intent Recognition), quản lý giỏ hàng thông minh (Smart Cart) và các điểm rủi ro giao dịch khi để AI Agent thực hiện lệnh thay cho người dùng."
    )

    add_h4("1.3.3. Nghiên cứu hệ thống Multi-Agent bằng Google Gemini")
    p_body(
        "Nhóm sử dụng Google Gemini 1.5 Pro ở chế độ suy luận chuyên sâu (Deep Thinking) để mô hình hóa kiến trúc điều phối đa tác tử (Multi-Agent System). Gemini cung cấp góc nhìn toàn diện về luồng dữ liệu giữa Shopping Agent, Order Agent và Customer Service Agent, đảm bảo tính phân quyền chặt chẽ theo mô hình RBAC."
    )

    add_h4("1.3.4. Nhật ký Prompting chi tiết")
    p_body("Dưới đây là nhật ký câu lệnh (AI Prompting Log) được thực hiện trong quá trình nghiên cứu bài Lab 1:")

    prompt_headers = ["STT", "Công cụ AI", "Nội dung câu lệnh Prompt", "Kết quả trích xuất & Tiếp thu", "Đánh giá chất lượng"]
    prompt_rows = [
        [
            "1",
            "Perplexity AI\n(Pro Search)",
            'Prompt: "Tìm mẫu tài liệu đặc tả yêu cầu phần mềm (SRS) chuẩn FPT Polytechnic môn Dự án Mẫu / Dự án .NET. Cấu trúc bảng Use Case chi tiết gồm những thành phần nào? Cho ví dụ về chức năng E-commerce."',
            "Cung cấp khung mẫu 10 trường chuẩn: ID, Tên, Mô tả, Actor, Trigger, Tiền điều kiện, Hậu điều kiện, Luồng chính, Luồng phụ, Ngoại lệ. Cấu trúc này được áp dụng nguyên mẫu vào toàn bộ 14 SRS của Lab 1.",
            "Độ tin cậy: 9.5/10.\nNguồn dẫn xác thực từ tài liệu giảng dạy FPT Edu.",
        ],
        [
            "2",
            "ChatGPT\n(Deepsearch)",
            'Prompt: "Đóng vai trò là Lead System Architect, hãy phân tích nghiệp vụ của hệ thống AI-Native Commerce: sự khác biệt với E-commerce truyền thống, các tác nhân (Actors), các module chức năng cốt lõi và kịch bản mua sắm hội thoại."',
            "Làm rõ 4 nhóm Actors (Guest, Customer, Admin/Merchant, AI Agent Platform) và 16 module nền tảng. Phân tích chi tiết luồng Mua sắm hội thoại (Conversational Shopping).",
            "Độ tin cậy: 9.0/10.\nPhân tích nghiệp vụ xuất sắc, định hình toàn bộ phạm vi đề tài.",
        ],
        [
            "3",
            "Google Gemini\n(1.5 Pro)",
            'Prompt: "Thiết kế ma trận phân quyền (RBAC) và các kịch bản ngoại lệ (Exception Flows) bảo mật cho giao thức Agentic Commerce Protocol (ACP) khi AI Agent tự động đặt hàng và thanh toán."',
            "Đề xuất cơ chế Guardrails: Giới hạn ngân sách tối đa của Agent, xác thực 2 lớp qua OTP khi số tiền vượt ngưỡng, cơ chế Rollback giao dịch khi API cổng thanh toán bị gián đoạn.",
            "Độ tin cậy: 9.5/10.\nĐưa trực tiếp vào kịch bản ngoại lệ của các ca sử dụng UC07, UC08 và UC14.",
        ],
    ]
    create_table(prompt_rows, [Inches(0.4), Inches(1.3), Inches(2.2), Inches(2.0), Inches(1.1)], prompt_headers)

    add_h4("1.3.5. Đánh giá, đối sánh và chọn lọc giải pháp từ kết quả AI")
    p_bullet("Tiếp thu và giữ nguyên cấu trúc bảng đặc tả SRS 10 cột theo chuẩn của trường.", "Chuẩn hóa định dạng: ")
    p_bullet("Không đưa các công nghệ không kiểm soát được vào phạm vi, tập trung giải quyết bài toán cốt lõi trên nền tảng .NET Core và SQL Server.", "Chắt lọc thực tiễn: ")
    p_bullet("Bổ sung đầy đủ các kịch bản ngoại lệ xử lý lỗi mạng, hết hàng trong kho, sai lệch giá khuyến mãi và kiểm toán giao dịch của Agent.", "Tối ưu an toàn hệ thống: ")

    add_h3("1.4. Giới thiệu tổng quan hệ thống AI-Native Commerce (Bài 2 - 4.0 Điểm)")
    add_h4("1.4.1. Khái niệm và bối cảnh hình thành hệ thống")
    p_body(
        'Hệ thống "AI-Native Commerce" là nền tảng thương mại điện tử thế hệ mới được thiết kế với Trí tuệ Nhân tạo là thành phần cốt lõi, tham gia trực tiếp vào toàn bộ hành trình mua sắm của khách hàng và quy trình vận hành của nhà bán hàng. Khác với các hệ thống truyền thống chỉ tích hợp chatbot làm công cụ hỏi đáp ngoại vi, AI-Native Commerce tích hợp sâu các tác tử tự hành (AI Agents) có khả năng đọc hiểu ngữ cảnh, tra cứu kho hàng thời gian thực, tư vấn cá nhân hóa và tự động tạo đơn hàng thông qua giao thức chuẩn.'
    )

    add_h4("1.4.2. Phân tích hiện trạng thị trường và nhu cầu khách hàng")
    p_body("A. Hiện trạng và hạn chế của E-commerce truyền thống:", bold_prefix="")
    p_bullet("Khách hàng phải duyệt qua hàng trăm trang sản phẩm với các bộ lọc cứng nhắc, dễ bỏ cuộc khi không tìm được sản phẩm ưng ý.", "Tìm kiếm kém hiệu quả: ")
    p_bullet("Hệ thống đề xuất dựa trên lịch sử xem cũ một cách máy móc, không hiểu được nhu cầu tức thời và ngữ cảnh sử dụng thực tế của khách.", "Thiếu tính cá nhân hóa sâu: ")
    p_bullet("Đội ngũ chăm sóc khách hàng bị quá tải vào các dịp khuyến mãi lớn, thời gian phản hồi chậm trễ dẫn đến sụt giảm tỷ lệ chốt đơn.", "Tắc nghẽn hỗ trợ: ")

    p_body("B. Nhu cầu cấp thiết của khách hàng và doanh nghiệp:", bold_prefix="")
    p_bullet("Khách hàng mong muốn được trò chuyện tự nhiên như với một chuyên gia tư vấn bán hàng tại cửa hàng truyền thống.", "Trải nghiệm mua sắm mượt mà: ")
    p_bullet("Doanh nghiệp cần hệ thống tự động hóa từ khâu tiếp thị, chốt đơn cho đến hậu mãi, giảm thiểu chi phí nhân sự.", "Tối ưu hóa chi phí vận hành: ")
    p_bullet("Chuẩn bị sẵn sàng kết nối với các hệ sinh thái AI Agent bên ngoài để không bị bỏ lại phía sau trong làn sóng Agentic AI.", "Đón đầu tương lai: ")

    add_h4("1.4.3. Các thành phần người dùng (Actors) trong hệ thống")
    p_body("Hệ thống AI-Native Commerce xác định rõ 4 nhóm tác nhân (Actors) chính:")

    actors_headers = ["Tác nhân (Actor)", "Phân loại vai trò", "Mô tả trách nhiệm & Quyền hạn"]
    actors_data = [
        [
            "Khách vãng lai\n(Guest)",
            "Người dùng chưa có tài khoản",
            "- Xem danh sách sản phẩm, chương trình khuyến mãi.\n"
            "- Tìm kiếm sản phẩm bằng từ khóa hoặc ngôn ngữ tự nhiên.\n"
            "- Nhận tư vấn tự động từ AI Assistant ở mức giới hạn.\n"
            "- Thực hiện đăng ký tài khoản để trở thành User.",
        ],
        [
            "Khách hàng\n(Customer / User)",
            "Người dùng mua sắm đã có tài khoản",
            "- Quản lý tài khoản cá nhân, địa chỉ giao hàng, phương thức thanh toán.\n"
            "- Mua sắm thông minh với Trợ lý AI (Shopping Assistant).\n"
            "- Quản lý giỏ hàng, áp dụng voucher, đặt hàng và thanh toán trực tuyến.\n"
            "- Theo dõi đơn hàng, đánh giá sản phẩm và khiếu nại đổi trả.",
        ],
        [
            "Quản trị / Nhà bán\n(Admin / Merchant)",
            "Người dùng điều hành và quản lý cửa hàng",
            "- Quản lý danh mục sản phẩm, biến thể, giá bán và tồn kho chuẩn hóa cho AI.\n"
            "- Quản lý đơn hàng, cập nhật trạng thái vận chuyển và thanh toán.\n"
            "- Quản lý tài khoản người dùng, phân quyền RBAC và chính sách khuyến mãi.\n"
            "- Giám sát báo cáo doanh thu, kiểm toán giao dịch của AI Agents.",
        ],
        [
            "Nền tảng Tác tử AI\n(AI Agent Platform)",
            "Tác nhân hệ thống tự hành (System Actor)",
            "- Tác tử tìm kiếm (Discovery Agent): Xử lý ngôn ngữ tự nhiên, tìm kiếm ngữ nghĩa.\n"
            "- Tác tử mua sắm (Shopping Agent): Đề xuất sản phẩm, quản lý giỏ hàng.\n"
            "- Tác tử giao thức (Commerce Protocol Agent): Thực thi lệnh mua qua ACP.",
        ],
    ]
    create_table(actors_data, [Inches(1.5), Inches(1.8), Inches(3.5)], actors_headers)

    add_h4("1.4.4. Danh mục các module chức năng hệ thống")
    p_body("Hệ thống gồm 16 module nền tảng được tổ chức thành 4 phân hệ chính:")
    module_headers = ["Phân hệ", "Mã Module", "Tên Module chức năng", "Mục tiêu & Phạm vi nghiệp vụ"]
    module_data = [
        ["Khách hàng & Giao tiếp", "M01", "Identity & Customer Management", "Đăng ký, đăng nhập, phân quyền, quản lý hồ sơ cá nhân và bảo mật."],
        ["Khách hàng & Giao tiếp", "M02", "Product & Catalog Management", "Cung cấp dữ liệu danh mục, sản phẩm chuẩn hóa cho UI và AI."],
        ["Khách hàng & Giao tiếp", "M03", "AI Product Discovery", "Tìm kiếm ngữ nghĩa bằng ngôn ngữ tự nhiên, gợi ý theo ngữ cảnh."],
        ["Khách hàng & Giao tiếp", "M04", "AI Shopping Assistant", "Trợ lý ảo đồng hành tư vấn mua sắm, so sánh món hàng."],
        ["Giao dịch Thương mại", "M05", "Pricing & Promotion", "Quản lý bảng giá, áp dụng voucher và khuyến mãi tự động."],
        ["Giao dịch Thương mại", "M06", "Cart & Checkout", "Giỏ hàng thông minh, quy trình thanh toán nhanh chóng."],
        ["Giao dịch Thương mại", "M07", "Order Management", "Theo dõi trạng thái đơn hàng, xử lý đổi trả hàng."],
        ["Giao dịch Thương mại", "M08", "Payment & Settlement", "Tích hợp cổng thanh toán trực tuyến (VNPay, Thẻ, Ví điện tử)."],
        ["Vận hành & Hậu cần", "M09", "Inventory & Fulfillment", "Kiểm soát số lượng tồn kho, đồng bộ đơn vị vận chuyển."],
        ["Vận hành & Hậu cần", "M10", "Customer Service & Returns", "Hỗ trợ khách hàng 24/7 và giải quyết khiếu nại."],
        ["Vận hành & Hậu cần", "M11", "Merchant Management", "Cổng thông tin cho nhà bán hàng theo dõi gian hàng."],
        ["Nền tảng AI & Dữ liệu", "M12", "AI Marketing & Growth", "Tiếp thị tự động hóa và phân nhóm khách hàng mục tiêu."],
        ["Nền tảng AI & Dữ liệu", "M13", "AI Agent Platform", "Nền tảng điều phối, Intent Router, Agent Registry và Guardrails."],
        ["Nền tảng AI & Dữ liệu", "M14", "Data & Analytics", "Báo cáo thống kê doanh thu, phân tích hành vi khách hàng."],
        ["Nền tảng AI & Dữ liệu", "M15", "Agentic Commerce Protocol (ACP)", "Giao thức chuẩn kết nối AI Agent với hệ thống thương mại."],
        ["Nền tảng AI & Dữ liệu", "M16", "Administration & Governance", "Quản trị hệ thống, nhật ký kiểm toán và an toàn thông tin."],
    ]
    create_table(module_data, [Inches(1.5), Inches(0.8), Inches(2.3), Inches(2.2)], module_headers)

    add_h4("1.4.5. Phân tích luồng hoạt động tổng thể và sự liên kết")
    p_body(
        "Các chức năng trong hệ thống AI-Native Commerce vận hành theo chuỗi liên kết khép kín, phân chia thành 4 luồng nghiệp vụ cốt lõi:"
    )
    p_bullet(
        "Người dùng nhập nhu cầu bằng câu tự nhiên (ví dụ: 'Tôi muốn mua áo khoác ấm cho bé 5 tuổi đi Đà Lạt'). AI Discovery Agent (M03) phân tích ý định, chuyển đổi thành truy vấn Vector Search trên Catalog (M02). Shopping Assistant (M04) hiển thị 3 lựa chọn kèm lý do đề xuất. Người dùng duyệt và yêu cầu thêm vào Smart Cart (M06).",
        "1. Luồng Khám phá & Đặt hàng Hội thoại: "
    )
    p_bullet(
        "Tại bước Checkout, Promotion Engine (M05) tự động quét và áp dụng mã giảm giá tối ưu nhất cho khách hàng. Hệ thống tạo đơn hàng (M07), kết nối cổng VNPay (M08) để xác thực thanh toán. Khi thanh toán thành công, tồn kho (M09) tự động được trừ và thông báo cho nhà bán hàng (M11).",
        "2. Luồng Xử lý Giao dịch & Thanh toán: "
    )
    p_bullet(
        "Khách hàng hỏi AI Chatbot: 'Đơn hàng của tôi đang ở đâu?'. Customer Support Agent (M10) gọi Tool API sang Order Management (M07) lấy tọa độ vận chuyển và phản hồi tự nhiên cho khách.",
        "3. Luồng Theo dõi & Hỗ trợ Khách hàng: "
    )
    p_bullet(
        "Admin thiết lập danh mục sản phẩm chuẩn hóa (thuộc tính, embedding vector), giám sát doanh thu và theo dõi các giao dịch tự hành do AI Agent thực hiện qua ACP (M15) nhằm bảo đảm an toàn dòng tiền.",
        "4. Luồng Quản trị & Giám sát Hệ thống: "
    )

    # ---------- CHƯƠNG 2 ----------
    add_h2("CHƯƠNG 2: KHẢO SÁT VÀ PHÂN TÍCH YÊU CẦU")

    add_h3("2.1. Khảo sát hiện trạng và quy tắc vẽ Use Case (Bài 3)")
    add_h4("2.1.1. Khảo sát các giải pháp E-Commerce hiện nay")
    p_body(
        "Khảo sát các nền tảng thương mại điện tử hàng đầu tại Việt Nam và quốc tế (Shopee, Lazada, Amazon, Shopify) cho thấy: Hầu hết các hệ thống này vẫn đang dùng thanh tìm kiếm từ khóa kết hợp bộ lọc danh mục và bộ lọc giá. Nhược điểm lớn nhất là không thể giải quyết được các câu hỏi ngữ cảnh phức tạp của người dùng. AI-Native Commerce giải quyết triệt để vấn đề này bằng việc đưa mô hình tìm kiếm ngữ nghĩa (Semantic Vector Search) và Trợ lý hội thoại vào làm phương thức tương tác chủ đạo."
    )

    add_h4("2.1.2. Các quy tắc vẽ sơ đồ Use Case UML chuẩn")
    p_body(
        "Để đảm bảo tính khoa học, chuẩn xác và dễ hiểu cho tài liệu kỹ thuật, Nhóm 5 tuân thủ các quy chuẩn UML 2.5:"
    )
    p_bullet("Ký hiệu hình người, đại diện cho vai trò người dùng hoặc hệ thống bên ngoài tương tác với phần mềm (Guest, Customer, Admin, AI Agent).", "Actor: ")
    p_bullet("Ký hiệu hình Elip chứa động từ + bổ ngữ rõ nghĩa (ví dụ: Tìm kiếm bằng ngôn ngữ tự nhiên, Quản lý giỏ hàng).", "Use Case: ")
    p_bullet("Hình chữ nhật bao quanh toàn bộ các ca sử dụng để định rõ phạm vi hệ thống.", "System Boundary: ")
    p_bullet("Đường nối liền nét thể hiện tương tác trực tiếp giữa Actor và Use Case.", "Association: ")

    add_h3("2.2. Sơ đồ Use Case tổng quát hệ thống AI-Native Commerce")
    p_body(
        "Dưới đây là sơ đồ Use Case tổng quát của Hệ thống Thương mại Điện tử AI-Native, thể hiện sự tương tác của 4 nhóm Actors với các phân hệ chức năng:"
    )

    img_tongquat = r"C:\Net108Khai\usecase_ainative_tongquat.png"
    if os.path.exists(img_tongquat):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img_tongquat, width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r = p_cap.add_run("Hình 2. Sơ đồ Use Case tổng quát Hệ thống AI-Native Commerce")
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.italic = True

    add_h3("2.3. Sơ đồ Use Case phân rã theo phân hệ")
    p_body("Hệ thống được phân rã thành 3 sơ đồ Use Case chuyên biệt tương ứng với từng nhóm nghiệp vụ:")

    add_h4("2.3.1. Phân hệ Khách hàng (Guest & Customer)")
    p_body(
        "Bao gồm các chức năng: Đăng ký/Đăng nhập, Tìm kiếm bằng ngôn ngữ tự nhiên, Tư vấn mua sắm với AI Shopping Assistant, Quản lý giỏ hàng thông minh, Đặt hàng & thanh toán, Tra cứu lịch sử đơn hàng."
    )
    img_cust = r"C:\Net108Khai\usecase_ainative_customer.png"
    if os.path.exists(img_cust):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img_cust, width=Inches(5.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r = p_cap.add_run("Hình 3. Sơ đồ Use Case Phân hệ Khách hàng (Guest & Customer)")
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.italic = True

    add_h4("2.3.2. Phân hệ Quản trị & Nhà bán hàng (Merchant & Admin)")
    p_body(
        "Bao gồm các chức năng quản trị: Quản lý danh mục & sản phẩm chuẩn hóa cho AI, Quản lý đơn hàng, Quản lý tài khoản & phân quyền RBAC, Quản lý khuyến mãi, Báo cáo thống kê & phân tích hành vi AI."
    )
    img_adm = r"C:\Net108Khai\usecase_ainative_admin.png"
    if os.path.exists(img_adm):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img_adm, width=Inches(5.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r = p_cap.add_run("Hình 4. Sơ đồ Use Case Phân hệ Quản trị & Nhà bán hàng")
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.italic = True

    add_h4("2.3.3. Phân hệ Nền tảng Tác tử AI (AI Agent Platform)")
    p_body(
        "Bao gồm các chức năng tự hành: Định tuyến ý định (Intent Router), Tìm kiếm ngữ nghĩa (Semantic Search), Thực thi giao thức thương mại tác tử (ACP), Hỗ trợ khách hàng tự động 24/7."
    )
    img_ag = r"C:\Net108Khai\usecase_ainative_agent.png"
    if os.path.exists(img_ag):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(img_ag, width=Inches(5.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r = p_cap.add_run("Hình 5. Sơ đồ Use Case Phân hệ Nền tảng Tác tử AI")
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.italic = True

    add_h3("2.4. Phân loại danh sách chức năng theo từng Actor")
    add_h4("2.4.1. Chức năng của Guest")
    g_headers = ["STT", "Tên chức năng", "Mô tả nghiệp vụ"]
    g_data = [
        ["1", "Xem danh sách sản phẩm", "Xem sản phẩm nổi bật, sản phẩm theo danh mục và khuyến mãi trên trang chủ."],
        ["2", "Tìm kiếm bằng ngôn ngữ tự nhiên", "Nhập mô tả nhu cầu để AI tìm kiếm và đề xuất sản phẩm phù hợp."],
        ["3", "Tương tác với AI Assistant cơ bản", "Hỏi đáp thông tin sản phẩm, chính sách bảo hành ở mức giới hạn."],
        ["4", "Đăng ký tài khoản", "Nhập thông tin cá nhân (Email, Mật khẩu, Họ tên) để đăng ký tài khoản khách hàng."],
    ]
    create_table(g_data, [Inches(0.6), Inches(2.2), Inches(4.0)], g_headers)

    add_h4("2.4.2. Chức năng của User / Customer")
    u_headers = ["STT", "Tên chức năng", "Mô tả nghiệp vụ"]
    u_data = [
        ["1", "Đăng nhập / Đăng xuất", "Đăng nhập bằng Email/Password hoặc Google OAuth, khởi tạo phiên làm việc bảo mật."],
        ["2", "Quản lý thông tin cá nhân & Địa chỉ", "Cập nhật hồ sơ, số điện thoại, danh sách địa chỉ nhận hàng."],
        ["3", "Mua sắm hội thoại với AI Shopping Assistant", "Trò chuyện ngữ cảnh, yêu cầu AI so sánh sản phẩm, lọc theo ngân sách."],
        ["4", "Quản lý giỏ hàng thông minh", "Thêm/sửa/xóa sản phẩm, chọn biến thể (size, màu), kiểm tra tồn kho tự động."],
        ["5", "Đặt hàng & Áp dụng voucher tự động", "Tự động chọn voucher giảm giá tối ưu, chọn đơn vị vận chuyển."],
        ["6", "Thanh toán trực tuyến", "Thanh toán an toàn qua cổng VNPay, thẻ tín dụng hoặc chọn hình thức COD."],
        ["7", "Theo dõi đơn hàng & Khiếu nại đổi trả", "Xem trạng thái giao hàng thời gian thực, gửi yêu cầu đổi trả có hỗ trợ của AI."],
    ]
    create_table(u_data, [Inches(0.6), Inches(2.4), Inches(3.8)], u_headers)

    add_h4("2.4.3. Chức năng của Admin / Merchant")
    a_headers = ["STT", "Tên chức năng", "Mô tả nghiệp vụ"]
    a_data = [
        ["1", "Quản lý sản phẩm & Chuẩn hóa cho AI", "Thêm, sửa, xóa sản phẩm, tạo thuộc tính chi tiết và nhúng vector phục vụ AI Search."],
        ["2", "Quản lý danh mục & Thương hiệu", "Tổ chức cây danh mục đa cấp, quản lý thông tin thương hiệu đối tác."],
        ["3", "Quản lý đơn hàng & Vận chuyển", "Tiếp nhận đơn, cập nhật trạng thái đóng gói, bàn giao vận chuyển, xử lý hoàn tiền."],
        ["4", "Quản lý tài khoản & Phân quyền RBAC", "Quản lý hồ sơ người dùng, phân vai trò (Admin, Merchant, Staff) và khóa tài khoản."],
        ["5", "Quản lý khuyến mãi & Mã giảm giá", "Tạo chương trình ưu đãi, flash sale, voucher theo hạng khách hàng."],
        ["6", "Báo cáo thống kê & Phân tích hành vi AI", "Báo cáo doanh thu theo mốc thời gian, tỷ lệ chuyển đổi từ AI Agent, xuất file Excel."],
    ]
    create_table(a_data, [Inches(0.6), Inches(2.4), Inches(3.8)], a_headers)

    add_h4("2.4.4. Chức năng của AI Agent Platform")
    ag_headers = ["STT", "Tên chức năng", "Mô tả nghiệp vụ"]
    ag_data = [
        ["1", "Định tuyến ý định (Intent Router)", "Phân tích ngữ cảnh câu nói của người dùng và chuyển tiếp đến Agent xử lý phù hợp."],
        ["2", "Tìm kiếm ngữ nghĩa (Semantic Search)", "Tạo embedding vector và truy vấn cơ sở dữ liệu vector theo khoảng cách Cosine."],
        ["3", "Thực thi giao thức thương mại (ACP)", "Cung cấp API và Tool Use chuẩn hóa cho phép Agent bên ngoài truy vấn và đặt hàng."],
        ["4", "Hỗ trợ khách hàng tự động 24/7", "Tự động trả lời thắc mắc về đơn hàng, vận chuyển, đổi trả sản phẩm."],
    ]
    create_table(ag_data, [Inches(0.6), Inches(2.4), Inches(3.8)], ag_headers)

    add_h3("2.5. Đặc tả chi tiết các Use Cases cốt lõi (14 bảng SRS chuẩn FPT)")
    p_body(
        "Dưới đây là đặc tả chi tiết toàn bộ 14 Use Cases cốt lõi của Hệ thống Thương mại Điện tử AI-Native theo đúng biểu mẫu bảng 10 trường của Trường Cao đẳng FPT Polytechnic:"
    )

    # 1. UC01
    add_h4("2.5.1. Use Case 1: Đăng ký tài khoản (UC01)")
    add_srs_table(
        "UC01",
        "Đăng ký tài khoản người dùng",
        "Cho phép khách vãng lai (Guest) tạo tài khoản mới trong hệ thống để thực hiện mua sắm, lưu giỏ hàng và sử dụng đầy đủ các tính năng của AI Assistant.",
        "Khách vãng lai (Guest)",
        'Guest nhấp vào nút "Đăng ký" trên thanh điều hướng hoặc từ lời mời của AI Assistant.',
        "Guest chưa đăng nhập và sở hữu một địa chỉ Email hợp lệ chưa từng đăng ký trong hệ thống.",
        "Thành công: Tài khoản được khởi tạo trong CSDL, gửi email kích hoạt, tự động chuyển sang trạng thái đã đăng nhập.\nThất bại: Báo lỗi và giữ nguyên form đăng ký kèm thông báo.",
        "(1) Guest nhấp vào nút \"Đăng ký\" trên màn hình trang chủ.\n"
        "(2) Hệ thống hiển thị form Đăng ký gồm: Họ và tên, Email, Mật khẩu, Nhập lại mật khẩu, Số điện thoại.\n"
        "(3) Guest điền đầy đủ các thông tin và nhấn nút \"Tạo tài khoản\".\n"
        "(4) Hệ thống kiểm tra hợp lệ dữ liệu (định dạng email, độ phức tạp mật khẩu >= 8 ký tự).\n"
        "(5) Hệ thống kiểm tra Email trong CSDL để đảm bảo không bị trùng lặp.\n"
        "(6) Hệ thống mã hóa mật khẩu (băm BCrypt / SHA-256), tạo bản ghi User mới với vai trò Customer.\n"
        "(7) Hệ thống tự động tạo Giỏ hàng rỗng (Cart) và hồ sơ sở thích ban đầu cho User.\n"
        "(8) Hệ thống thông báo \"Đăng ký tài khoản thành công!\" và điều hướng vào trang chủ.",
        "(3a) Guest chọn \"Đăng ký nhanh bằng Google\": Hệ thống gọi giao thức OAuth 2.0 để lấy thông tin xác thực.",
        "(4.1) Mật khẩu và xác nhận mật khẩu không khớp: Hệ thống báo lỗi \"Mật khẩu xác nhận không trùng khớp!\".\n"
        "(5.1) Email đã tồn tại: Hệ thống cảnh báo \"Email này đã được sử dụng. Vui lòng đăng nhập hoặc sử dụng email khác!\".\n"
        "(4.2) Mật khẩu yếu (< 8 ký tự hoặc thiếu chữ/số): Báo lỗi yêu cầu đặt mật khẩu mạnh hơn."
    )

    # 2. UC02
    add_h4("2.5.2. Use Case 2: Đăng nhập hệ thống (UC02)")
    add_srs_table(
        "UC02",
        "Đăng nhập hệ thống",
        "Xác thực danh tính người dùng bằng Email và Mật khẩu, phân quyền giao diện (Customer, Merchant, Admin) và khởi tạo phiên làm việc bảo mật (JWT Session).",
        "Guest, Customer, Admin / Merchant",
        'Người dùng bấm chọn nút "Đăng nhập" trên thanh tiêu đề ứng dụng.',
        "Người dùng đã có tài khoản và tài khoản ở trạng thái kích hoạt (IsActive = true).",
        "Thành công: Người dùng đăng nhập thành công, hệ thống sinh mã Access Token (JWT), tải thông tin giỏ hàng và lịch sử hội thoại AI.\nThất bại: Báo lỗi và ở lại form đăng nhập.",
        "(1) Người dùng mở form Đăng nhập từ thanh điều hướng.\n"
        "(2) Người dùng nhập Email và Mật khẩu, sau đó bấm nút \"Đăng nhập\".\n"
        "(3) Hệ thống truy vấn CSDL theo Email và kiểm tra trạng thái tài khoản.\n"
        "(4) Hệ thống so khớp mật khẩu đã băm.\n"
        "(5) Hệ thống tạo JSON Web Token (JWT) chứa UserID và Role.\n"
        "(6) Hệ thống lưu phiên làm việc, tải giỏ hàng gần nhất và lịch sử chat với AI.\n"
        "(7) Hệ thống chuyển hướng người dùng đến giao diện tương ứng với quyền hạn (Customer vào Shop, Admin vào Dashboard).",
        "(2a) Người dùng chọn \"Ghi nhớ đăng nhập\": Hệ thống lưu Refresh Token trong Cookie an toàn (HttpOnly).\n"
        "(2b) Đăng nhập qua Google: Hệ thống xác thực qua Google OpenID Connect.",
        "(3.1) Email không tồn tại hoặc mật khẩu sai: Hệ thống báo lỗi \"Email hoặc mật khẩu không chính xác!\".\n"
        "(3.2) Tài khoản đã bị khóa bởi Admin: Hệ thống thông báo \"Tài khoản của bạn đã bị tạm khóa. Vui lòng liên hệ hỗ trợ!\".\n"
        "(4.1) Nhập sai quá 5 lần: Hệ thống khóa tạm thời trong 15 phút để chống tấn công Brute-force."
    )

    # 3. UC03
    add_h4("2.5.3. Use Case 3: Quên mật khẩu (UC03)")
    add_srs_table(
        "UC03",
        "Quên mật khẩu",
        "Cho phép người dùng khôi phục mật khẩu thông qua việc xác thực địa chỉ Email và nhập mã xác thực OTP 6 số để thiết lập mật khẩu mới.",
        "Customer, Admin / Merchant",
        'Người dùng bấm vào liên kết "Quên mật khẩu?" tại form Đăng nhập.',
        "Người dùng có Email hợp lệ đã đăng ký và hệ thống gửi thư điện tử (SMTP) đang hoạt động ổn định.",
        "Thành công: Mật khẩu mới được cập nhật vào CSDL, vô hiệu hóa các phiên làm việc cũ, yêu cầu đăng nhập lại.\nThất bại: Không đổi được mật khẩu, hiển thị thông báo lỗi.",
        "(1) Người dùng bấm vào liên kết \"Quên mật khẩu?\".\n"
        "(2) Hệ thống mở form Khôi phục mật khẩu.\n"
        "(3) Người dùng nhập Email tài khoản và nhấn nút \"Gửi mã xác nhận\".\n"
        "(4) Hệ thống kiểm tra sự tồn tại của Email trong CSDL.\n"
        "(5) Hệ thống sinh mã OTP ngẫu nhiên 6 chữ số có hiệu lực trong 5 phút và gửi qua Email.\n"
        "(6) Người dùng nhận mã OTP từ hộp thư, nhập mã OTP, Mật khẩu mới và Nhập lại mật khẩu mới.\n"
        "(7) Người dùng nhấn nút \"Xác nhận đổi mật khẩu\".\n"
        "(8) Hệ thống kiểm tra mã OTP, mã hóa mật khẩu mới và lưu vào CSDL, sau đó thông báo thành công.",
        "(3a) Người dùng bấm \"Hủy bỏ\": Hệ thống quay lại màn hình Đăng nhập.",
        "(4.1) Email không tồn tại trong hệ thống: Báo lỗi \"Địa chỉ Email không tồn tại trong hệ thống!\".\n"
        "(8.1) Mã OTP không chính xác hoặc đã hết hạn: Báo lỗi \"Mã OTP không hợp lệ hoặc đã hết hạn!\".\n"
        "(8.2) Mật khẩu mới trùng mật khẩu cũ: Báo lỗi yêu cầu đặt mật khẩu khác mật khẩu gần nhất."
    )

    # 4. UC04
    add_h4("2.5.4. Use Case 4: Tìm kiếm bằng ngôn ngữ tự nhiên (UC04)")
    add_srs_table(
        "UC04",
        "Tìm kiếm sản phẩm bằng ngôn ngữ tự nhiên (AI Natural Language Discovery)",
        "Cho phép người dùng nhập mô tả nhu cầu bằng câu văn tự nhiên (ví dụ: 'Tìm giày thể thao chạy bộ êm chân dưới 1 triệu cho nam'), hệ thống sử dụng AI để phân tích ý định và tìm kiếm ngữ nghĩa.",
        "Guest, Customer",
        'Người dùng nhập văn bản vào thanh tìm kiếm thông minh "AI Search" hoặc bấm phím Enter.',
        "Hệ thống cơ sở dữ liệu Vector (ChromaDB / pgvector) và dịch vụ Embedding đang hoạt động ổn định.",
        "Thành công: Hiển thị danh sách sản phẩm phù hợp nhất với ngữ cảnh và nhu cầu thực tế kèm theo lý do gợi ý của AI.\nThất bại: Không tìm thấy sản phẩm phù hợp, gợi ý các tiêu chí mở rộng.",
        "(1) Người dùng nhập câu mô tả nhu cầu vào thanh tìm kiếm AI.\n"
        "(2) Hệ thống gửi truy vấn đến AI Intent Parser để trích xuất các thực thể: Loại sản phẩm, Giới tính, Khoảng giá, Đặc tính mong muốn.\n"
        "(3) Hệ thống tạo vector embedding cho câu truy vấn và thực hiện Hybrid Search (kết hợp Semantic Search và Filter truyền thống).\n"
        "(4) Hệ thống xếp hạng sản phẩm theo điểm tương đồng ngữ nghĩa (Cosine Similarity) và độ uy tín của người bán.\n"
        "(5) Hệ thống hiển thị kết quả trực quan gồm: Danh sách thẻ sản phẩm, tóm tắt lý do gợi ý ('Phù hợp với tiêu chí chạy bộ, đệm êm, giá dưới 1 triệu') và các bộ lọc gợi ý bổ sung.\n"
        "(6) Người dùng nhấp vào sản phẩm để xem chi tiết hoặc yêu cầu AI so sánh.",
        "(1a) Người dùng tìm kiếm bằng giọng nói: Hệ thống sử dụng công nghệ Speech-to-Text để chuyển đổi giọng nói thành văn bản.",
        "(3.1) Lỗi kết nối dịch vụ AI Embedding: Hệ thống tự động chuyển đổi sang cơ chế tìm kiếm từ khóa SQL truyền thống (FTS) để không làm gián đoạn trải nghiệm người dùng.\n"
        "(5.1) Không tìm thấy sản phẩm phù hợp: Hệ thống gợi ý mở rộng khoảng giá hoặc đổi tiêu chuẩn tìm kiếm."
    )

    # 5. UC05
    add_h4("2.5.5. Use Case 5: Tương tác với AI Shopping Assistant (UC05)")
    add_srs_table(
        "UC05",
        "Mua sắm tương tác với Trợ lý AI (Conversational Shopping Assistant)",
        "Cung cấp giao diện trò chuyện hội thoại thông minh (AI Chatbot), hỗ trợ khách hàng so sánh tính năng sản phẩm, kiểm tra độ phù hợp, gợi ý phối đồ và tư vấn quà tặng.",
        "Guest, Customer",
        'Người dùng bấm vào biểu tượng "AI Shopping Assistant" ở góc màn hình hoặc từ trang chi tiết sản phẩm.',
        "Người dùng đang truy cập hệ thống; mô hình AI Agent Platform đang trực tuyến.",
        "Thành công: Trợ lý AI giải đáp thấu đáo thắc mắc của khách hàng, hiển thị thẻ sản phẩm tương tác (Interactive Product Card) có nút Mua ngay.\nThất bại: Báo lỗi gián đoạn hội thoại.",
        "(1) Người dùng mở khung chat AI Shopping Assistant.\n"
        "(2) Hệ thống tải lịch sử hội thoại gần nhất và thông tin ngữ cảnh trang hiện tại.\n"
        "(3) Người dùng gửi tin nhắn hỏi: 'Tôi muốn so sánh điện thoại A và B về khả năng chụp đêm và thời lượng pin'.\n"
        "(4) AI Shopping Assistant nhận diện ý định (Intent), gọi Tool tra cứu thông số kỹ thuật của 2 sản phẩm từ CSDL.\n"
        "(5) AI phân tích, tổng hợp câu trả lời so sánh khách quan dưới dạng bảng tóm tắt ưu/nhược điểm.\n"
        "(6) AI gửi kèm 2 thẻ sản phẩm tương tác có giá bán, đánh giá sao và nút \"Thêm vào giỏ hàng\".\n"
        "(7) Người dùng có thể bấm trực tiếp vào nút trên khung chat để đưa sản phẩm vào giỏ hàng.",
        "(3a) Người dùng yêu cầu tư vấn theo ngân sách cụ thể: AI lọc các sản phẩm phù hợp và gợi ý voucher hiện có.\n"
        "(3b) Người dùng hỏi câu hỏi ngoài phạm vi mua sắm: AI khéo léo từ chối và hướng người dùng quay lại chủ đề sản phẩm.",
        "(4.1) Sản phẩm người dùng hỏi đã ngừng kinh doanh: AI thông báo và gợi ý dòng sản phẩm tương đương thay thế.\n"
        "(5.1) Phản hồi AI vượt ngưỡng thời gian (Timeout > 5s): Hệ thống hiển thị câu thông báo tạm và tự động thử lại."
    )

    # 6. UC06
    add_h4("2.5.6. Use Case 6: Quản lý giỏ hàng thông minh (UC06)")
    add_srs_table(
        "UC06",
        "Quản lý giỏ hàng thông minh (Smart Cart Management)",
        "Cho phép khách hàng thêm sản phẩm vào giỏ, điều chỉnh số lượng, thay đổi biến thể (kích cỡ, màu sắc), tự động cảnh báo tồn kho và nhận gợi ý gom đơn tiết kiệm phí ship từ AI.",
        "Customer",
        'Khách hàng bấm nút "Thêm vào giỏ hàng" hoặc truy cập biểu tượng Giỏ hàng trên thanh điều hướng.',
        "Khách hàng đã đăng nhập vào hệ thống; sản phẩm còn hàng trong kho.",
        "Thành công: Sản phẩm được cập nhật vào giỏ hàng, tổng tiền tạm tính được tính toán chính xác theo thời gian thực.\nThất bại: Báo lỗi và giữ nguyên trạng thái giỏ hàng.",
        "(1) Khách hàng bấm nút \"Thêm vào giỏ hàng\" từ trang sản phẩm hoặc từ khung chat AI.\n"
        "(2) Hệ thống kiểm tra số lượng tồn kho khả dụng của sản phẩm theo biến thể được chọn.\n"
        "(3) Hệ thống thêm món hàng vào giỏ hàng của User trong CSDL (hoặc tăng số lượng nếu đã có).\n"
        "(4) Khách hàng mở màn hình Giỏ hàng để xem danh sách món đã chọn.\n"
        "(5) Khách hàng có thể tăng/giảm số lượng, xóa từng món hoặc tích chọn những món cần thanh toán đợt này.\n"
        "(6) AI Smart Cart tự động tính toán tổng tiền hàng và đưa ra gợi ý: 'Mua thêm 50.000đ để được miễn phí vận chuyển'.\n"
        "(7) Khách hàng bấm nút \"Tiến hành đặt hàng\" để chuyển sang bước thanh toán.",
        "(5a) Khách hàng muốn đổi size/màu trực tiếp trong giỏ: Hệ thống mở popup cho phép đổi biến thể mà không cần quay lại trang sản phẩm.",
        "(2.1) Sản phẩm đã hết hàng trong kho: Hệ thống cảnh báo \"Sản phẩm này hiện đã hết hàng, vui lòng chọn sản phẩm khác!\".\n"
        "(5.1) Số lượng khách chọn vượt quá số lượng tồn kho còn lại: Hệ thống tự động giới hạn ở mức tối đa hiện có."
    )

    # 7. UC07
    add_h4("2.5.7. Use Case 7: Đặt hàng và áp dụng khuyến mãi tự động (UC07)")
    add_srs_table(
        "UC07",
        "Đặt hàng và áp dụng khuyến mãi tự động (Checkout & Auto Promotion)",
        "Xử lý quá trình tạo đơn hàng từ các sản phẩm trong giỏ, tự động tìm và áp dụng mã giảm giá có lợi nhất cho khách, tính toán phí vận chuyển và xuất thông tin đơn hàng.",
        "Customer",
        'Khách hàng bấm nút "Tiến hành đặt hàng" từ màn hình Giỏ hàng.',
        "Giỏ hàng có ít nhất một sản phẩm hợp lệ; khách hàng đã chọn địa chỉ giao hàng.",
        "Thành công: Đơn hàng mới được tạo ở trạng thái Chờ thanh toán (Pending Payment), mã đơn hàng được sinh ra, giữ chỗ tồn kho (Hold Inventory).\nThất bại: Đơn hàng không được tạo, hệ thống báo lỗi.",
        "(1) Khách hàng vào màn hình Checkout.\n"
        "(2) Hệ thống tải địa chỉ nhận hàng mặc định của khách và danh sách sản phẩm được chọn.\n"
        "(3) Khách hàng chọn đơn vị vận chuyển (Giao hàng nhanh, Giao hàng tiết kiệm).\n"
        "(4) Động cơ khuyến mãi (Promotion Engine) tự động phân tích đơn hàng và áp dụng voucher giảm giá sâu nhất hiện có của khách.\n"
        "(5) Hệ thống tính toán tổng thanh toán: Tiền hàng - Giảm giá + Phí vận chuyển.\n"
        "(6) Khách hàng chọn phương thức thanh toán (Thanh toán trực tuyến VNPay hoặc Thanh toán khi nhận hàng COD).\n"
        "(7) Khách hàng bấm nút \"Xác nhận đặt hàng\".\n"
        "(8) Hệ thống lưu đơn hàng vào bảng Orders, tạo các bản ghi chi tiết OrderItems và khóa tạm tồn kho trong 15 phút.",
        "(4a) Khách hàng muốn tự nhập mã voucher riêng: Khách hàng nhập mã vào ô Voucher và nhấn \"Áp dụng\", hệ thống kiểm tra điều kiện và tính lại tiền.",
        "(2.1) Chưa có địa chỉ giao hàng: Hệ thống yêu cầu thêm địa chỉ nhận hàng mới trước khi tiếp tục.\n"
        "(8.1) Trong quá trình đặt hàng có sản phẩm bị khách khác mua hết: Hệ thống báo lỗi cập nhật giỏ hàng và yêu cầu chọn lại."
    )

    # 8. UC08
    add_h4("2.5.8. Use Case 8: Thanh toán trực tuyến (UC08)")
    add_srs_table(
        "UC08",
        "Thanh toán trực tuyến (Online Payment Gateway)",
        "Kết nối với cổng thanh toán điện tử (VNPay / Thẻ ATM / QR Pay) để thực hiện giao dịch thanh toán an toàn, cập nhật trạng thái đơn hàng sang Đã thanh toán (Paid).",
        "Customer",
        'Khách hàng chọn phương thức thanh toán trực tuyến và bấm "Thanh toán ngay".',
        "Đơn hàng đã được tạo thành công và đang ở trạng thái Chờ thanh toán.",
        "Thành công: Giao dịch được xác nhận thành công, đơn hàng chuyển sang trạng thái Đã thanh toán, gửi email xác nhận cho khách.\nThất bại: Báo lỗi giao dịch thất bại, giữ nguyên đơn hàng để khách thử lại.",
        "(1) Khách hàng chọn cổng thanh toán VNPay và bấm nút \"Thanh toán ngay\".\n"
        "(2) Hệ thống sinh mã giao dịch duy nhất, tạo URL thanh toán có chữ ký bảo mật (HMAC-SHA512) và chuyển hướng khách sang cổng thanh toán VNPay.\n"
        "(3) Khách hàng thực hiện quét mã VNPAY-QR hoặc nhập thông tin thẻ ngân hàng tại cổng VNPay.\n"
        "(4) Khách hàng xác thực OTP ngân hàng để hoàn tất trừ tiền.\n"
        "(5) Cổng thanh toán xử lý và gửi phản hồi kết quả (IPN Webhook) về máy chủ hệ thống AI-Native Commerce.\n"
        "(6) Hệ thống kiểm tra chữ ký dữ liệu phản hồi để đảm bảo tính toàn vẹn.\n"
        "(7) Hệ thống cập nhật trạng thái đơn hàng thành \"Đã thanh toán\", trừ tồn kho chính thức và gửi thông báo đơn hàng mới cho nhà bán hàng.\n"
        "(8) Hệ thống chuyển hướng khách về trang \"Đặt hàng thành công\" kèm mã đơn hàng.",
        "(3a) Khách hàng bấm \"Hủy giao dịch\" tại cổng thanh toán: Cổng thanh toán chuyển hướng về lại trang thanh toán của cửa hàng kèm thông báo đã hủy.",
        "(5.1) Tài khoản không đủ số dư hoặc nhập sai OTP quá số lần: Cổng thanh toán báo lỗi, hệ thống cập nhật trạng thái \"Thanh toán thất bại\" và cho phép thanh toán lại.\n"
        "(6.1) Sai lệch chữ ký bảo mật (Checksum failed): Hệ thống cảnh báo giao dịch giả mạo, ghi nhận log bảo mật và từ chối cập nhật đơn hàng."
    )

    # 9. UC09
    add_h4("2.5.9. Use Case 9: Tra cứu đơn hàng và theo dõi vận chuyển (UC09)")
    add_srs_table(
        "UC09",
        "Tra cứu đơn hàng và theo dõi vận chuyển (Order Tracking)",
        "Cho phép khách hàng tra cứu lịch sử các đơn hàng đã đặt, xem chi tiết hành trình vận chuyển theo thời gian thực và xem lịch sử hóa đơn điện tử.",
        "Customer",
        'Khách hàng truy cập mục "Đơn hàng của tôi" từ menu tài khoản hoặc hỏi AI Assistant.',
        "Khách hàng đã đăng nhập tài khoản vào hệ thống.",
        "Thành công: Hiển thị đầy đủ danh sách và chi tiết trạng thái đơn hàng (Chờ xác nhận, Đang đóng gói, Đang giao, Đã giao thành công).\nThất bại: Báo lỗi tải dữ liệu.",
        "(1) Khách hàng chọn menu \"Đơn hàng của tôi\".\n"
        "(2) Hệ thống truy vấn CSDL và hiển thị danh sách các đơn hàng đã đặt phân loại theo các tab trạng thái.\n"
        "(3) Khách hàng bấm vào một đơn hàng cụ thể để xem chi tiết.\n"
        "(4) Hệ thống hiển thị: Danh sách món, đơn giá, địa chỉ giao hàng, tổng tiền, phương thức thanh toán và dòng thời gian trạng thái (Timeline).\n"
        "(5) Khách hàng có thể bấm nút \"Theo dõi vị trí\" để xem hành trình bưu kiện liên kết từ đối tác vận chuyển.\n"
        "(6) Khi đơn hàng đã giao thành công, khách hàng có thể bấm nút \"Đánh giá sản phẩm\" hoặc \"Mua lại\".",
        "(1a) Khách hàng hỏi trực tiếp qua AI Chatbot: 'Kiểm tra giúp tôi đơn hàng mới nhất', AI tra cứu và phản hồi ngay trạng thái đơn hàng.",
        "(2.1) Khách hàng chưa có đơn hàng nào: Hệ thống hiển thị thông báo \"Bạn chưa có đơn hàng nào\" kèm nút Tiếp tục mua sắm."
    )

    # 10. UC10
    add_h4("2.5.10. Use Case 10: Quản lý danh mục & sản phẩm chuẩn hóa cho AI (UC10)")
    add_srs_table(
        "UC10",
        "Quản lý danh mục & sản phẩm chuẩn hóa cho AI (Product Catalog Management)",
        "Cung cấp công cụ cho Quản trị viên/Nhà bán hàng quản lý thông tin sản phẩm, danh mục đa cấp, giá bán, biến thể và tự động sinh Embedding Vector cho công cụ tìm kiếm AI.",
        "Admin / Merchant",
        'Admin bấm chọn mục "Quản lý sản phẩm" trên trang quản trị Dashboard.',
        "Đã đăng nhập vào hệ thống với vai trò Admin hoặc Merchant.",
        "Thành công: Dữ liệu sản phẩm được thêm/sửa/xóa trong CSDL quan hệ, đồng bộ ngay lập tức sang Vector Database để phục vụ AI Search.\nThất bại: Báo lỗi, giữ nguyên dữ liệu cũ.",
        "(1) Admin truy cập module Quản lý sản phẩm.\n"
        "(2) Hệ thống tải và hiển thị danh sách toàn bộ sản phẩm hiện có.\n"
        "(3) Thêm mới sản phẩm: Admin bấm \"Thêm mới\", nhập Tên sản phẩm, chọn Danh mục, nhập Giá niêm yết, Giá khuyến mãi, Tồn kho, tải hình ảnh và mô tả chi tiết.\n"
        "(4) Admin thiết lập các biến thể (Màu sắc, Kích cỡ) và cấu hình từ khóa thuộc tính.\n"
        "(5) Admin bấm nút \"Lưu sản phẩm\".\n"
        "(6) Hệ thống lưu sản phẩm vào bảng Products trong SQL Server.\n"
        "(7) Hệ thống tự động kích hoạt dịch vụ tạo Vector Embedding từ mô tả sản phẩm và lưu vào Vector Database phục vụ Semantic Search.\n"
        "(8) Hệ thống thông báo thành công và cập nhật lại danh sách.",
        "(3a) Sửa sản phẩm: Admin chọn sản phẩm, sửa giá hoặc ảnh và bấm \"Cập nhật\".\n"
        "(3b) Xóa sản phẩm: Admin bấm \"Xóa\", hệ thống kiểm tra ràng buộc đơn hàng cũ và thực hiện xóa mềm (ẩn sản phẩm).",
        "(3.1) Nhập thiếu thông tin bắt buộc hoặc giá bán <= 0: Hệ thống báo lỗi và đánh dấu đỏ các trường sai sót.\n"
        "(7.1) Lỗi dịch vụ Vector Embedding: Hệ thống vẫn lưu thành công sản phẩm vào CSDL SQL Server và đưa việc tạo vector vào hàng đợi (Queue) xử lý lại sau."
    )

    # 11. UC11
    add_h4("2.5.11. Use Case 11: Quản lý đơn hàng và trạng thái đơn hàng (UC11)")
    add_srs_table(
        "UC11",
        "Quản lý đơn hàng và trạng thái xử lý (Order Management)",
        "Cho phép Admin và Nhà bán hàng kiểm soát toàn bộ vòng đời của các đơn hàng: tiếp nhận, xác nhận đơn, chuyển đóng gói, bàn giao vận chuyển và xử lý hủy đơn.",
        "Admin / Merchant",
        'Admin chọn mục "Quản lý đơn hàng" trên menu quản trị.',
        "Đã đăng nhập với tài khoản có quyền Quản trị hoặc Nhà bán hàng.",
        "Thành công: Trạng thái đơn hàng được cập nhật, đồng bộ thông báo thời gian thực đến khách hàng qua Web/Email/Zalo.\nThất bại: Báo lỗi cập nhật trạng thái.",
        "(1) Admin vào danh sách Quản lý đơn hàng.\n"
        "(2) Hệ thống hiển thị các đơn hàng mới phát sinh cần xử lý.\n"
        "(3) Admin xem chi tiết đơn: danh sách sản phẩm, địa chỉ giao hàng, phương thức thanh toán.\n"
        "(4) Admin bấm \"Xác nhận đơn hàng\", hệ thống chuyển trạng thái sang \"Đang xử lý / Đóng gói\".\n"
        "(5) Sau khi đóng gói, Admin chọn \"Bàn giao vận chuyển\", nhập mã vận đơn đối tác.\n"
        "(6) Hệ thống cập nhật trạng thái \"Đang giao hàng\" và gửi thông báo mã vận đơn cho khách.\n"
        "(7) Khi bên vận chuyển báo giao thành công, đơn hàng tự động chuyển sang \"Hoàn tất\".",
        "(3a) Hủy đơn hàng: Khách hàng yêu cầu hủy đơn trước khi giao, Admin kiểm tra và bấm \"Hủy đơn\", hệ thống hoàn tiền (nếu đã thanh toán online) và hoàn lại tồn kho.",
        "(4.1) Tồn kho thực tế bị thiếu hụt: Admin bấm \"Tạm hoãn đơn\" và liên hệ khách hàng để thương lượng đổi món hoặc hủy đơn."
    )

    # 12. UC12
    add_h4("2.5.12. Use Case 12: Quản lý tài khoản và phân quyền RBAC (UC12)")
    add_srs_table(
        "UC12",
        "Quản lý tài khoản và phân quyền người dùng (Role-Based Access Control)",
        "Cho phép Quản trị viên cấp cao (Super Admin) quản lý danh sách tài khoản toàn hệ thống, gán vai trò người dùng (Customer, Merchant, Staff, Admin) và khóa tài khoản vi phạm chính sách.",
        "Admin (Super Admin)",
        'Admin bấm chọn mục "Quản lý tài khoản" trong phân hệ Quản trị hệ thống.',
        "Đã đăng nhập với tài khoản Super Admin cấp cao nhất.",
        "Thành công: Thông tin tài khoản và ma trận quyền hạn được cập nhật chính xác trong CSDL.\nThất bại: Báo lỗi không đủ thẩm quyền hoặc lỗi CSDL.",
        "(1) Admin chọn chức năng \"Quản lý tài khoản\".\n"
        "(2) Hệ thống hiển thị danh sách toàn bộ người dùng kèm vai trò và trạng thái hoạt động.\n"
        "(3) Thêm tài khoản nội bộ: Admin bấm \"Tạo tài khoản\", điền thông tin và chọn vai trò phân quyền (ví dụ: Merchant hoặc Staff).\n"
        "(4) Sửa quyền hạn: Admin chọn một tài khoản, điều chỉnh nhóm quyền được phép truy cập trên hệ thống.\n"
        "(5) Khóa tài khoản: Khi phát hiện tài khoản có hành vi gian lận hoặc vi phạm chính sách, Admin chọn \"Vô hiệu hóa tài khoản\".\n"
        "(6) Hệ thống ghi nhận thay đổi vào CSDL và hủy ngay lập tức các phiên làm việc (JWT Revocation) của tài khoản đó.",
        "(2a) Admin lọc tài khoản theo từng vai trò (Customer, Merchant, Admin) hoặc tìm theo Email/SĐT.",
        "(5.1) Admin thao tác tự khóa chính tài khoản của mình: Hệ thống ngăn chặn với cảnh báo \"Bạn không thể tự khóa tài khoản quản trị đang đăng nhập!\".\n"
        "(3.1) Email đã tồn tại: Hệ thống báo lỗi trùng lặp dữ liệu."
    )

    # 13. UC13
    add_h4("2.5.13. Use Case 13: Báo cáo thống kê và phân tích hành vi AI (UC13)")
    add_srs_table(
        "UC13",
        "Báo cáo thống kê doanh thu và phân tích hành vi AI (Analytics & Reporting)",
        "Cung cấp cho Ban quản lý các số liệu tổng hợp về doanh thu, số lượng đơn hàng, top sản phẩm bán chạy, tỷ trọng doanh thu đến từ gợi ý của AI Agent và xuất báo cáo ra Excel.",
        "Admin / Merchant",
        'Admin chọn mục "Báo cáo thống kê" trên thanh công cụ quản trị.',
        "Đã đăng nhập vào hệ thống với vai trò Quản trị viên hoặc Chủ cửa hàng.",
        "Thành công: Hiển thị đầy đủ số liệu thống kê trực quan qua bảng biểu và đồ thị; hỗ trợ xuất file Excel phục vụ kế toán.\nThất bại: Báo lỗi truy vấn hoặc không có dữ liệu giao dịch.",
        "(1) Admin truy cập màn hình Báo cáo thống kê.\n"
        "(2) Hệ thống hiển thị bảng Dashboard tổng quan doanh thu hôm nay, tuần này, tháng này.\n"
        "(3) Admin lựa chọn tiêu chí lọc báo cáo: Theo ngày/tháng/năm, Theo ngành hàng, hoặc Theo hiệu suất chuyển đổi của AI Shopping Assistant.\n"
        "(4) Admin bấm nút \"Xem báo cáo\".\n"
        "(5) Hệ thống truy vấn CSDL, tổng hợp số liệu và kết xuất trực quan: Biểu đồ tăng trưởng doanh thu, Biểu đồ tròn cơ cấu mặt hàng, Top 10 sản phẩm bán chạy nhất.\n"
        "(6) Hệ thống phân tích tỷ lệ khách chốt đơn qua AI Assistant (Conversion Rate by AI).\n"
        "(7) Admin có thể bấm nút \"Xuất Excel\" để tải tệp báo cáo về máy tính.",
        "(3a) Admin lọc doanh thu riêng của từng Nhà bán hàng (Merchant) để tính toán tiền đối soát thanh toán định kỳ.",
        "(5.1) Khoảng thời gian lọc không phát sinh giao dịch nào: Hệ thống thông báo \"Không có dữ liệu giao dịch trong khoảng thời gian đã chọn\" với số liệu hiển thị là 0đ."
    )

    # 14. UC14
    add_h4("2.5.14. Use Case 14: Thực thi giao dịch qua giao thức tác tử AI (UC14)")
    add_srs_table(
        "UC14",
        "Thực thi giao dịch qua giao thức Agentic Commerce Protocol (ACP)",
        "Cho phép các tác tử AI tự hành (của khách hàng hoặc hệ sinh thái đối tác) truy vấn dữ liệu sản phẩm chuẩn hóa, tạo giỏ hàng và thực thi đặt hàng an toàn thông qua API và Tool Use có kiểm soát.",
        "AI Agent Platform, Customer",
        "Tác tử AI nhận lệnh ủy quyền mua sắm từ người dùng hoặc hệ thống điều phối kích hoạt lệnh mua.",
        "Agent đã được cấp API Token xác thực; tài khoản người dùng đã ủy quyền giới hạn ngân sách (Spending Limit).",
        "Thành công: Đơn hàng được tạo tự động thông qua giao thức ACP, ghi nhận Audit Log đầy đủ, thông báo xác nhận đến điện thoại của khách hàng.\nThất bại: Giao dịch bị từ chối nếu vượt hạn mức hoặc vi phạm chính sách bảo vệ (Guardrails).",
        "(1) Khách hàng ra lệnh cho AI Agent: 'Hãy đặt mua 2 hộp sữa bột cho bé loại A nếu giá dưới 800.000đ'.\n"
        "(2) AI Agent kết nối đến cổng giao thức ACP của hệ thống với Bearer Token xác thực.\n"
        "(3) AI Agent gọi Tool API kiểm tra giá và tồn kho khả dụng của sản phẩm.\n"
        "(4) AI Agent kiểm tra điều kiện ngân sách được người dùng cấp quyền (Spending Limit Policy).\n"
        "(5) AI Agent gửi yêu cầu tạo đơn hàng thông qua endpoint /acp/orders của hệ thống.\n"
        "(6) Hệ thống kiểm tra chữ ký số và chính sách an toàn (Guardrail Verification).\n"
        "(7) Hệ thống tạo đơn hàng thành công, trừ tồn kho và gửi thông báo xác nhận (Push Notification) đến điện thoại khách hàng.\n"
        "(8) Hệ thống lưu vết chi tiết giao dịch vào bảng Audit Logs để phục vụ kiểm toán.",
        "(6a) Đơn hàng vượt hạn mức 1.000.000đ: Hệ thống yêu cầu xác thực 2 lớp (2FA OTP) từ người dùng trước khi duyệt lệnh của Agent.",
        "(4.1) Giá sản phẩm vượt quá ngân sách khách hàng yêu cầu: Agent hủy thực thi và gửi thông báo 'Giá hiện tại là 850.000đ, vượt mức 800.000đ của bạn, bạn có muốn mua không?'.\n"
        "(6.1) Vi phạm quy tắc bảo mật (Token hết hạn hoặc gọi hàm sai phép): Hệ thống từ chối kết nối và ghi nhận log an ninh mạng."
    )

    # ==================== HEADING 1: TÀI LIỆU THAM KHẢO ====================
    doc.add_page_break()
    add_h1("TÀI LIỆU THAM KHẢO")
    p_bullet("Trường Cao đẳng FPT Polytechnic (2024), Giáo trình môn học Dự án Mẫu / Dự án .NET 1 (NET108), NXB FPT Edu.", "[1] ")
    p_bullet("IEEE Computer Society (1998), IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications.", "[2] ")
    p_bullet("Microsoft Learn (2024), ASP.NET Core documentation - Building Modern Web Apps and APIs with C# and .NET 8, Microsoft.", "[3] ")
    p_bullet("Microsoft Learn (2024), Entity Framework Core & SQL Server Documentation, Microsoft.", "[4] ")
    p_bullet("Anthropic & OpenAI (2024), Multi-Agent Systems, Function Calling and Tool Use in Autonomous AI Platforms.", "[5] ")
    p_bullet("ChromaDB / LangChain Documentation (2024), Vector Databases and Semantic Hybrid Search for E-Commerce Architectures.", "[6] ")
    p_bullet("VNPay Gateway (2024), Tài liệu tích hợp thanh toán điện tử VNPay dành cho nhà phát triển.", "[7] ")

    # Save to file
    out_dir = r"C:\Net108Khai\Các Bài Lab"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "Lab1_NET108_AI_Native_Commerce.docx")
    doc.save(out_file)
    print(f"File created successfully: {out_file}")

    # Also try overwriting Lab1_NET108_AINativeCommerce.docx if unlocked
    alt_file = os.path.join(out_dir, "Lab1_NET108_AINativeCommerce.docx")
    try:
        doc.save(alt_file)
        print(f"Also updated: {alt_file}")
    except Exception as e:
        print(f"Notice: {alt_file} is currently open in Word/WPS, saved to {out_file} instead.")

    return out_file

if __name__ == "__main__":
    create_lab1_document()
