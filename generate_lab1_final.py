# -*- coding: utf-8 -*-
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_full_lab1_document():
    doc = docx.Document()

    # Base page settings A4
    for sec in doc.sections:
        sec.page_width = Inches(8.27)
        sec.page_height = Inches(11.69)
        sec.top_margin = Inches(0.79)
        sec.bottom_margin = Inches(0.79)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(0.79)

    # Helper: Set Header with standard FPT POLYTECHNIC | SAMPLE PROJECT
    def apply_standard_header_footer(section):
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False
        
        # Header setup
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
        r_l.font.color.rgb = RGBColor(242, 107, 33) # FPT Orange

        p_r = c_right.paragraphs[0]
        p_r.paragraph_format.space_after = Pt(2)
        p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_r = p_r.add_run("SAMPLE PROJECT")
        r_r.font.name = "Times New Roman"
        r_r.font.bold = True
        r_r.font.size = Pt(11)
        r_r.font.color.rgb = RGBColor(110, 110, 110) # Grey

        for c in (c_left, c_right):
            tcPr = c._tc.get_or_add_tcPr()
            borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="none"/><w:right w:val="none"/><w:bottom w:val="single" w:sz="8" w:space="4" w:color="A0A0A0"/></w:tcBorders>')
            tcPr.append(borders)

        # Footer setup
        ftr = section.footer
        p_f = ftr.paragraphs[0] if ftr.paragraphs else ftr.add_paragraph()
        p_f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_f.text = "Trang "
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
                tcBorders = parse_xml(r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/><w:left w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/><w:right w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/></w:tcBorders>'.format(nsdecls("w")))
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
            ["Exception Flow", exc_flow]
        ]
        t = doc.add_table(rows=10, cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        for r_idx, row in enumerate(data):
            r = t.rows[r_idx]
            cell_lbl = r.cells[0]
            cell_val = r.cells[1]
            cell_lbl.width = Inches(1.8)
            cell_val.width = Inches(5.1)
            cell_lbl.text = row[0]
            cell_val.text = row[1]
            
            shd_lbl = parse_xml(r'<w:shd {} w:fill="E8EEF5"/>'.format(nsdecls("w")))
            cell_lbl._tc.get_or_add_tcPr().append(shd_lbl)
            
            cell_lbl._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/></w:tcBorders>'.format(nsdecls("w"))))
            cell_val._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/></w:tcBorders>'.format(nsdecls("w"))))
            
            p0 = cell_lbl.paragraphs[0]
            p0.runs[0].font.name = "Times New Roman"
            p0.runs[0].font.bold = True
            p0.runs[0].font.size = Pt(11)
            
            p1 = cell_val.paragraphs[0]
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

    r3 = p_title.add_run("HỌC PHẦN: DỰ ÁN .NET 1 (NET108)\nĐỀ TÀI: HỆ THỐNG QUẢN LÝ QUÁN CÀ PHÊ\n(QUANLYQUANCAPHE)\n")
    r3.font.name = "Times New Roman"
    r3.font.bold = True
    r3.font.size = Pt(14)
    r3.font.color.rgb = RGBColor(60, 60, 60)

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_info.paragraph_format.space_before = Pt(45)
    p_info.paragraph_format.line_spacing = 1.3

    r_gv = p_info.add_run("Giảng viên hướng dẫn:\n")
    r_gv.font.bold = True
    r_gv.font.size = Pt(12.5)
    r_gv_name = p_info.add_run("ThS. Phan Hoàng Khải\n\n")
    r_gv_name.font.bold = True
    r_gv_name.font.size = Pt(13)
    r_gv_name.font.color.rgb = RGBColor(31, 78, 121)

    r_grp = p_info.add_run("Nhóm sinh viên thực hiện:\n")
    r_grp.font.bold = True
    r_grp.font.size = Pt(12.5)
    r_grp_name = p_info.add_run("NHÓM 5\n\n")
    r_grp_name.font.bold = True
    r_grp_name.font.size = Pt(13)
    r_grp_name.font.color.rgb = RGBColor(242, 107, 33)

    r_mem = p_info.add_run(
        "1. Trần Phúc Thiên (Nhóm trưởng)\n"
        "2. Trần Phạm Hoàng Minh\n"
        "3. Cho Hoàng Hiếu Trung\n"
        "4. Nguyễn Hoàng Quốc Anh\n"
        "5. Nguyễn Châu Văn Phát\n"
    )
    r_mem.font.size = Pt(12)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(40)
    r_loc = p_loc.add_run("ĐỒNG NAI, NĂM 2026")
    r_loc.font.bold = True
    r_loc.font.size = Pt(12)
    r_loc.font.color.rgb = RGBColor(100, 100, 100)

    # ==================== TRANG BẢNG PHÂN CÔNG & TIẾN ĐỘ (SECTION 1) ====================
    sec_plan = doc.add_section()
    apply_standard_header_footer(sec_plan)

    style_heading_1("THÔNG TIN DỰ ÁN VÀ PHÂN CÔNG NHIỆM VỤ NHÓM 5")
    add_p("Thông tin tổng quát học phần và dự án thực hiện:")
    info_table_data = [
        ["Học phần:", "NET108 - Dự án .NET 1"],
        ["Đề tài dự án:", "Hệ thống Quản lý Quán Cà phê (QuanLyQuanCaPhe)"],
        ["Giảng viên hướng dẫn:", "ThS. Phan Hoàng Khải"],
        ["Đơn vị thực hiện:", "Nhóm 5 - FPT Polytechnic Đồng Nai"],
        ["Thời gian thực hiện:", "Năm 2026"]
    ]
    create_styled_table(info_table_data, [Inches(2.2), Inches(4.7)])

    add_p("Bảng phân công chi tiết nhiệm vụ Lab 1 của các thành viên Nhóm 5:")
    team_table_data = [
        ["1", "Trần Phúc Thiên", "Nhóm trưởng / Project Manager", "Phụ trách điều phối nhóm, tổng hợp tài liệu Lab 1, phân tích yêu cầu nghiệp vụ khách hàng (Bài 2).", "100%", "Hoàn thành tốt"],
        ["2", "Trần Phạm Hoàng Minh", "Backend Lead / Analyst", "Phụ trách nghiên cứu ứng dụng AI (Bài 1), phân tích và phân rã danh mục chức năng theo đối tượng người dùng.", "100%", "Hoàn thành tốt"],
        ["3", "Cho Hoàng Hiếu Trung", "System Modeler / Designer", "Phụ trách tìm hiểu quy tắc vẽ sơ đồ Use Case UML, thiết kế sơ đồ Use Case tổng quát 13 chức năng (Bài 3).", "100%", "Hoàn thành tốt"],
        ["4", "Nguyễn Hoàng Quốc Anh", "Doc Lead / Technical Writer", "Phụ trách biên soạn các bảng đặc tả yêu cầu hệ thống (SRS) chi tiết cho các Use Case theo biểu mẫu FPT.", "100%", "Hoàn thành tốt"],
        ["5", "Nguyễn Châu Văn Phát", "QA / Reviewer", "Phụ trách rà soát luồng hoạt động các chức năng, kiểm thử tính logic của sơ đồ Use Case và kiểm tra định dạng báo cáo.", "100%", "Hoàn thành tốt"]
    ]
    create_styled_table(team_table_data, [Inches(0.5), Inches(1.5), Inches(1.4), Inches(2.3), Inches(0.6), Inches(0.6)], ["STT", "Thành viên", "Vai trò", "Nhiệm vụ trong Lab 1", "Tiến độ", "Đánh giá"])

    # ==================== TRANG MỤC LỤC (SECTION 2) ====================
    sec_toc = doc.add_section()
    apply_standard_header_footer(sec_toc)

    style_heading_1("MỤC LỤC")
    add_p("1 GIỚI THIỆU DỰ ÁN ................................................................................................................... Trang 4", bold_prefix="")
    add_p("    1.1 BÀI 1: Ứng dụng AI trong tìm kiếm thông tin ............................................................. Trang 4", italic=True)
    add_p("    1.2 BÀI 2: Thực hiện tài liệu giới thiệu dự án ................................................................. Trang 4", italic=True)
    add_p("        1.2.1 Giới thiệu dự án ....................................................................................................... Trang 4")
    add_p("        1.2.2 Phân tích yêu cầu khách hàng và hiện trạng đề xuất dự án ................................. Trang 4")
    add_p("        1.2.3 Liệt kê thành phần người dùng (Actors) ............................................................... Trang 5")
    add_p("        1.2.4 Danh sách chức năng theo từng đối tượng người dùng ........................................ Trang 5")
    add_p("        1.2.5 Phân tích luồng hoạt động và sự liên kết giữa các chức năng ............................ Trang 6")
    add_p("2 PHÂN TÍCH YÊU CẦU ............................................................................................................. Trang 7", bold_prefix="")
    add_p("    2.1 BÀI 3: Vẽ mô hình hệ thống và xác định các thực thể .............................................. Trang 7", italic=True)
    add_p("        2.1.1 Quy tắc vẽ sơ đồ Use Case chuẩn UML ............................................................... Trang 7")
    add_p("        2.1.2 Sơ đồ Use Case tổng quát hệ thống Quán Cà phê ................................................. Trang 7")
    add_p("        2.1.3 Phân rã nhóm chức năng theo loại người dùng ...................................................... Trang 8")
    add_p("    2.2 Đặc tả yêu cầu hệ thống (SRS) ....................................................................................... Trang 9")
    add_p("        2.2.1 Đặc tả Use Case Đăng nhập hệ thống (UC01) .......................................................... Trang 9")
    add_p("        2.2.2 Đặc tả Use Case Sửa thông tin cá nhân (UC02) ..................................................... Trang 9")
    add_p("        2.2.3 Đặc tả Use Case Tạo phiếu bán hàng (UC03) .......................................................... Trang 10")
    add_p("        2.2.4 Đặc tả Use Case Sửa phiếu bán hàng (UC04) .......................................................... Trang 10")
    add_p("        2.2.5 Đặc tả Use Case Xem danh sách hóa đơn cá nhân (UC05) ..................................... Trang 11")
    add_p("        2.2.6 Đặc tả Use Case Quản lý loại đồ uống (UC06) ........................................................ Trang 11")
    add_p("        2.2.7 Đặc tả Use Case Quản lý đồ uống (UC07) ............................................................... Trang 12")
    add_p("        2.2.8 Đặc tả Use Case Quản lý nhân viên (UC08) ............................................................ Trang 12")
    add_p("        2.2.9 Đặc tả Use Case Quản lý hóa đơn (UC09) ............................................................... Trang 13")
    add_p("        2.2.10 Đặc tả Use Case Báo cáo thống kê (UC10) ............................................................ Trang 13")
    
    add_p("> Ghi chú: Báo cáo này hoàn thành 100% phạm vi yêu cầu của Bài Lab 1 (Phần I và Phần II). Các phân mục Thiết kế Kiến trúc tổng thể (Deploy Diagram, Appmap), Thiết kế giao diện UI và Cơ sở dữ liệu thuộc phạm vi các bài Lab tiếp theo.", italic=True, space_after=12)

    # ==================== PHẦN I: GIỚI THIỆU DỰ ÁN ====================
    sec_content = doc.add_section()
    apply_standard_header_footer(sec_content)

    style_heading_1("1 GIỚI THIỆU DỰ ÁN")

    # BÀI 1
    style_heading_2("BÀI 1 (2.0 ĐIỂM): ỨNG DỤNG AI TRONG TÌM KIẾM THÔNG TIN")
    style_heading_3("1.1. Mục đích ứng dụng AI trong học tập và phân tích dự án")
    add_p("Trong quá trình thực hiện học phần NET108 (Dự án .NET 1), Nhóm 5 đã chủ động ứng dụng các công cụ Trí tuệ Nhân tạo thế hệ mới (Perplexity AI, OpenAI ChatGPT, Google Gemini Deep Search) nhằm nâng cao chất lượng nghiên cứu và chuẩn hóa tài liệu:")
    add_bullet(" Khai thác các mẫu tài liệu đặc tả yêu cầu phần mềm (SRS - Software Requirements Specification) chuẩn IEEE 830 và cấu trúc báo cáo của trường FPT Polytechnic.", "• Chuẩn hóa tài liệu:");
    add_bullet(" Khảo sát quy trình nghiệp vụ order thực tế tại các chuỗi cà phê/đồ uống (bán lẻ tại quầy, quản lý menu món, phân loại thức uống, in hóa đơn, ca làm việc nhân viên).", "• Nghiên cứu nghiệp vụ:");
    add_bullet(" Hỗ trợ phân tích, bóc tách ranh giới vai trò người dùng và gợi ý danh mục Use Case bám sát đề cương giảng dạy của giảng viên.", "• Hỗ trợ mô hình hóa:");

    style_heading_3("1.2. Nhật ký Prompting và kết quả truy vấn thực tế")
    add_p("Dưới đây là bảng tổng hợp các câu lệnh Prompt được Nhóm 5 thực hiện trên các nền tảng AI:")
    ai_table = [
        ["1", "Perplexity AI", '"Tìm kiếm và phân tích cấu trúc tài liệu đặc tả yêu cầu phần mềm (SRS - Software Requirements Specification) chuẩn IEEE 830 cho phần mềm quản lý bán hàng quán cafe, đồ uống. Trình bày chi tiết các trường cần có trong một bảng đặc tả Use Case."', "AI cung cấp cấu trúc 3 phần chuẩn: Giới thiệu hệ thống, Mô tả tổng quan chức năng/phi chức năng, và bảng mẫu đặc tả Use Case gồm 10 mục: ID, Tên, Mô tả, Tác nhân, Sự kiện kích hoạt, Tiền điều kiện, Hậu điều kiện, Luồng chính, Luồng rẽ nhánh, Luồng ngoại lệ."],
        ["2", "Google Gemini (Deep Search)", '"Khảo sát hiện trạng và các vấn đề bất cập thường gặp tại các quán cà phê vừa và nhỏ khi quản lý thủ công (order giấy, tính nhẩm, ghi sổ). Đề xuất giải pháp số hóa phần mềm."', "AI chỉ ra 4 nỗi đau lớn: Khách chờ lâu lúc cao điểm, nhân viên ghi nhầm order/topping, thất thoát doanh thu do hóa đơn viết tay và mất nhiều thời gian kiểm đếm sổ sách cuối ngày. Từ đó đề xuất giải pháp ứng dụng bán hàng POS và quản lý tập trung."],
        ["3", "ChatGPT 4o", '"Liệt kê danh sách các Use Case chính cho hệ thống Quản lý Bán Đồ Uống gồm 2 tác nhân chính là Nhân viên bán hàng và Quản lý quán. Trình bày dạng bảng phân quyền rõ ràng theo 13 chức năng chuẩn."', "AI đề xuất phân rã 13 Use Case: Nhóm chung (Đăng nhập, Quên MK, Đổi MK, Sửa TT cá nhân), Nhóm Nhân viên (Tạo phiếu, Sửa phiếu, Xem phiếu, Xem DS hóa đơn), Nhóm Quản lý (QL Loại đồ uống, QL Đồ uống, QL Nhân viên, QL Hóa đơn, Báo cáo thống kê)."]
    ]
    create_styled_table(ai_table, [Inches(0.5), Inches(1.3), Inches(2.6), Inches(2.5)], ["STT", "Công cụ AI", "Câu lệnh Prompt thực thi", "Kết quả thu được & Ứng dụng"])

    style_heading_3("1.3. Đánh giá và chắt lọc thông tin")
    add_p("Dựa trên kết quả thu thập từ các công cụ AI, Nhóm 5 đã tiến hành thảo luận, tinh chỉnh và chuẩn hóa dữ liệu để phù hợp với bài toán Quán Cà phê theo đúng hướng dẫn trong slide bài giảng của Thầy Phan Hoàng Khải.")

    # BÀI 2
    style_heading_2("BÀI 2 (4.0 ĐIỂM): THỰC HIỆN TÀI LIỆU GIỚI THIỆU DỰ ÁN")
    style_heading_3("2.1. Giới thiệu dự án")
    add_bullet(" Hệ thống Quản lý Quán Cà phê (QuanLyQuanCaPhe).", "• Tên dự án:");
    add_bullet(" Ứng dụng Web / Desktop quản lý bán hàng tại quầy và điều hành nội bộ cửa hàng kinh doanh đồ uống.", "• Loại hình:");
    add_bullet(" Xây dựng giải pháp phần mềm chuyên biệt, khép kín dành cho quán cà phê, trà sữa, hỗ trợ tối đa quy trình ghi nhận order, in hóa đơn nhanh, đồng bộ dữ liệu doanh số và quản trị danh mục thực đơn theo thời gian thực.", "• Ý tưởng cốt lõi:");

    style_heading_3("2.2. Phân tích yêu cầu khách hàng và hiện trạng dẫn đến đề xuất dự án")
    add_p("1. Khảo sát hiện trạng thực tế tại các quán đồ uống truyền thống:")
    add_bullet(" Khách hàng vào giờ cao điểm phải xếp hàng chờ lâu; nhân viên ghi nhận order trên giấy dễ nhầm lẫn (sai topping, nhầm size, sai bàn).")
    add_bullet(" Tính nhẩm hoặc dùng máy tính bỏ túi thủ công dễ xảy ra sai sót khi thanh toán; việc áp dụng giảm giá hay tính tiền thừa thiếu chính xác.")
    add_bullet(" Cuối ngày, chủ quán mất 1 - 2 tiếng kiểm đếm hóa đơn giấy và hóa đơn hủy, dễ thất thoát doanh thu do gian lận hoặc sai lệch số liệu.")
    add_bullet(" Khó quản lý biến động giá và tình trạng hết món: Khi hết nguyên liệu một món nào đó, nhân viên không kịp nắm bắt dẫn đến việc khách gọi món rồi lại phải đổi.")

    add_p("2. Giải pháp công nghệ đề xuất:")
    add_p('Phát triển phần mềm "QuanLyQuanCaPhe" với giao diện trực quan, chia tách rõ ràng 2 phân hệ quyền hạn (Nhân viên và Quản lý):')
    add_bullet(" Nhân viên order bằng cú click chuột hoặc chạm màn hình, tự động tính tổng tiền chính xác, in hóa đơn tức thì.")
    add_bullet(" Quản lý kiểm soát toàn diện danh mục đồ uống, giá bán, nhân sự và báo cáo doanh thu theo thời gian thực mọi lúc mọi nơi.")

    style_heading_3("2.3. Liệt kê thành phần người dùng (Actors)")
    add_bullet(" Người trực tiếp đứng quầy thu ngân và phục vụ khách. Thực hiện các thao tác tạo phiếu bán hàng, chỉnh sửa phiếu khi khách đổi món, tra cứu phiếu bán hàng và xem danh sách hóa đơn do chính ca của mình tạo ra.", "1. Nhân viên (Staff / Cashier): ");
    add_bullet(" Chủ quán hoặc người điều hành ca có toàn quyền kiểm soát hoạt động của quán: Quản lý nhân viên, quản lý phân loại và chi tiết đồ uống, theo dõi toàn bộ hóa đơn của cửa hàng, và tra cứu các báo cáo thống kê doanh thu đa chiều.", "2. Quản lý (Manager / Admin): ");

    style_heading_3("2.4. Danh sách chức năng theo từng đối tượng người dùng")
    add_p("Bảng 1. Danh sách chức năng Nhóm dùng chung (Cả Nhân viên & Quản lý):")
    f_common = [
        ["1", "Đăng nhập", "Xác thực tài khoản và mật khẩu người dùng vào hệ thống, phân quyền truy cập theo vai trò (Nhân viên / Quản lý)."],
        ["2", "Đổi mật khẩu", "Cho phép người dùng chủ động thay đổi mật khẩu định kỳ nhằm nâng cao tính bảo mật tài khoản."],
        ["3", "Quên mật khẩu", "Hỗ trợ khôi phục mật khẩu thông qua email xác nhận khi người dùng quên thông tin đăng nhập."],
        ["4", "Sửa thông tin cá nhân", "Cho phép người dùng cập nhật thông tin cá nhân (họ tên, số điện thoại, ảnh đại diện, địa chỉ)."]
    ]
    create_styled_table(f_common, [Inches(0.6), Inches(2.2), Inches(4.1)], ["STT", "Tên chức năng", "Mô tả chi tiết"])

    add_p("Bảng 2. Danh sách chức năng dành riêng cho Nhân viên (Bán hàng):")
    f_staff = [
        ["1", "Tạo phiếu bán hàng", "Tạo mới một hóa đơn bán lẻ, chọn các món đồ uống, số lượng, size, đường/đá, tính thành tiền."],
        ["2", "Sửa phiếu bán hàng", "Cho phép cập nhật thêm/bớt món, đổi số lượng trên phiếu bán hàng trước khi khách thanh toán."],
        ["3", "Xem phiếu bán hàng", "Hiển thị chi tiết nội dung phiếu bán hàng hiện tại đang phục vụ hoặc đang chờ xử lý."],
        ["4", "Xem danh sách hóa đơn cá nhân", "Xem lịch sử các hóa đơn đã thanh toán do chính nhân viên đó thực hiện trong ca làm việc."]
    ]
    create_styled_table(f_staff, [Inches(0.6), Inches(2.2), Inches(4.1)], ["STT", "Tên chức năng", "Mô tả chi tiết"])

    add_p("Bảng 3. Danh sách chức năng dành riêng cho Quản lý (Quản trị & Báo cáo):")
    f_manager = [
        ["1", "Quản lý loại đồ uống", "Thêm mới, sửa tên, xóa danh mục loại đồ uống (Ví dụ: Cà phê, Trà hoa quả, Đá xay, Nước ép)."],
        ["2", "Quản lý đồ uống", "Quản lý danh sách từng món: tên đồ uống, đơn giá, hình ảnh, loại đồ uống, trạng thái còn/hết hàng."],
        ["3", "Quản lý nhân viên", "Quản lý hồ sơ nhân sự: thêm tài khoản nhân viên mới, phân quyền, sửa thông tin, khóa tài khoản."],
        ["4", "Quản lý hóa đơn", "Xem toàn bộ lịch sử hóa đơn bán ra của tất cả nhân viên, tìm kiếm theo ngày/nhân viên, xử lý hủy đơn sai."],
        ["5", "Báo cáo thống kê", "Thống kê tổng doanh thu theo ngày/tháng/năm, biểu đồ top đồ uống bán chạy nhất, số lượng ly tiêu thụ."]
    ]
    create_styled_table(f_manager, [Inches(0.6), Inches(2.2), Inches(4.1)], ["STT", "Tên chức năng", "Mô tả chi tiết"])

    style_heading_3("2.5. Phân tích luồng hoạt động các chức năng và sự liên kết giữa các chức năng")
    add_p("Mối liên kết giữa các phân hệ chức năng trong hệ thống diễn ra chặt chẽ theo quy trình kinh doanh thống nhất:")
    add_bullet(" Nhân viên và Quản lý phải đăng nhập thành công. Hệ thống phân quyền điều hướng Nhân viên vào giao diện bán hàng (POS), Quản lý vào giao diện Dashboard điều hành.", "1. Luồng Xác thực & Phân quyền:");
    add_bullet(' Khi có khách gọi món, Nhân viên thực hiện "Tạo phiếu bán hàng". Chức năng này lấy dữ liệu từ bảng "Quản lý đồ uống" và "Quản lý loại đồ uống" do Quản lý thiết lập trước đó. Nhân viên có thể "Sửa phiếu bán hàng" (thêm bớt món) nếu khách thay đổi ý kiến. Sau khi khách thanh toán, hệ thống chốt hóa đơn, in phiếu và lưu vào cơ sở dữ liệu.', "2. Luồng Nghiệp vụ Bán hàng & Lập hóa đơn:");
    add_bullet(' Hóa đơn sau khi được thanh toán sẽ tự động phân loại: Nhân viên có thể vào "Xem danh sách hóa đơn cá nhân" để đối soát ca làm; đồng thời dữ liệu ngay lập tức được chuyển sang phân hệ "Quản lý hóa đơn" của Quản lý.', "3. Luồng Quản lý Hóa đơn & Đối soát:");
    add_bullet(' Mỗi giao dịch bán hàng thành công sẽ tự động cập nhật số liệu vào phân hệ "Báo cáo thống kê". Quản lý có thể theo dõi doanh số nhảy tức thì mà không cần tổng kết sổ sách thủ công.', "4. Luồng Thống kê Doanh số:");

    # ==================== PHẦN II: PHÂN TÍCH VÀ VẼ SƠ ĐỒ ====================
    style_heading_1("2 PHÂN TÍCH YÊU CẦU")
    style_heading_2("2.1 SƠ ĐỒ USE CASES (BÀI 3 - 4.0 ĐIỂM)")

    style_heading_3("2.1.1. Quy tắc vẽ sơ đồ Use Case theo chuẩn UML")
    add_p("Sơ đồ Use Case (Use Case Diagram) là một biểu đồ thuộc ngôn ngữ mô hình hóa thống nhất UML, mô tả sự tương tác giữa các tác nhân bên ngoài (Actor) với các chức năng của hệ thống (Use Case).")
    add_bullet(" Đối tượng tương tác với hệ thống (người dùng hoặc hệ thống bên ngoài). Ký hiệu hình người que (Stick figure).", "• Actor (Tác nhân):");
    add_bullet(" Đại diện cho một chức năng cụ thể mà hệ thống cung cấp cho Actor để đạt được mục tiêu. Ký hiệu hình elip chứa tên chức năng.", "• Use Case (Trường hợp sử dụng):");
    add_bullet(" Ranh giới xác định phạm vi phần mềm, các Use Case nằm bên trong khung, Actor nằm bên ngoài. Ký hiệu hình chữ nhật.", "• System Boundary (Ranh giới hệ thống):");
    add_bullet(" Đường nối liền biểu thị sự tham gia của Actor vào Use Case.", "• Quan hệ Association:");
    add_bullet(" Quan hệ bao hàm bắt buộc (Use Case A luôn luôn thực thi Use Case B). Ký hiệu nét đứt có mũi tên kèm nhãn <<include>>.", "• Quan hệ <<include>>:");
    add_bullet(" Quan hệ mở rộng không bắt buộc, chỉ xảy ra khi có điều kiện kích hoạt. Ký hiệu nét đứt có mũi tên kèm nhãn <<extend>>.", "• Quan hệ <<extend>>:");

    style_heading_3("2.1.2. Sơ đồ Use Case tổng quát hệ thống Quản lý Quán Cà phê")
    add_p("Dưới đây là sơ đồ Use Case tổng quát của hệ thống bám sát chính xác 100% hình ảnh trong đề bài Lab 1 (gồm 2 Actor là Nhân viên, Quản lý và 13 chức năng):")

    diagram_path = r"C:\Net108Khai\usecase_tongquat.png"
    if os.path.exists(diagram_path):
        doc.add_picture(diagram_path, width=Inches(6.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Hình 1. Sơ đồ Use Case tổng quát Hệ thống Quản lý Quán Cà phê")
        r_cap.font.name = "Times New Roman"
        r_cap.font.italic = True
        r_cap.font.size = Pt(10.5)

    style_heading_3("2.1.3. Phân rã nhóm chức năng theo loại người dùng")
    uc_summary_table = [
        ["1", "Đăng nhập", "Nhân viên & Quản lý", "Xác thực tài khoản và phân quyền."],
        ["2", "Đổi mật khẩu", "Nhân viên & Quản lý", "Thay đổi mật khẩu cá nhân."],
        ["3", "Quên mật khẩu", "Nhân viên & Quản lý", "Khôi phục mật khẩu qua email."],
        ["4", "Sửa thông tin cá nhân", "Nhân viên & Quản lý", "Cập nhật hồ sơ tài khoản."],
        ["5", "Tạo phiếu bán hàng", "Nhân viên", "Chọn món, tính tiền, in hóa đơn."],
        ["6", "Sửa phiếu bán hàng", "Nhân viên", "Đổi món, đổi số lượng trên order."],
        ["7", "Xem phiếu bán hàng", "Nhân viên", "Tra cứu đơn hàng hiện hành."],
        ["8", "Xem danh sách hóa đơn cá nhân", "Nhân viên", "Đối soát tiền mặt theo ca làm."],
        ["9", "Quản lý loại đồ uống", "Quản lý", "Thêm/sửa/xóa danh mục loại món."],
        ["10", "Quản lý đồ uống", "Quản lý", "Thêm/sửa/xóa đồ uống, giá bán."],
        ["11", "Quản lý nhân viên", "Quản lý", "Thêm/sửa/xóa tài khoản nhân viên."],
        ["12", "Quản lý hóa đơn", "Quản lý", "Giám sát và kiểm duyệt toàn bộ hóa đơn."],
        ["13", "Báo cáo thống kê", "Quản lý", "Thống kê doanh số, top món bán chạy."]
    ]
    create_styled_table(uc_summary_table, [Inches(0.5), Inches(2.2), Inches(1.8), Inches(2.4)], ["STT", "Tên Use Case", "Actor thực hiện", "Mục đích nghiệp vụ"])

    # ĐẶC TẢ SRS
    style_heading_2("2.2 ĐẶC TẢ YÊU CẦU HỆ THỐNG (SRS)")
    add_p("Phần này trình bày chi tiết các bảng đặc tả Use Case theo đúng cấu trúc chuẩn của FPT Polytechnic:")

    # UC01
    style_heading_3("2.2.1. Use Case 1: Đăng nhập hệ thống (UC01)")
    add_srs_table(
        "UC01",
        "Đăng nhập hệ thống",
        "Cho phép người dùng (Nhân viên hoặc Quản lý) đăng nhập vào ứng dụng để thực hiện công việc theo quyền hạn được cấp.",
        "Nhân viên, Quản lý",
        'Người dùng mở ứng dụng và nhấn nút "Đăng nhập" trên màn hình chính.',
        "Người dùng đã được cấp tài khoản và mật khẩu hợp lệ trong cơ sở dữ liệu.",
        "Thành công: Hệ thống xác thực thành công, ghi nhận phiên làm việc và chuyển đến giao diện làm việc tương ứng.\nThất bại: Hệ thống báo lỗi và yêu cầu nhập lại.",
        "(1) Người dùng khởi động ứng dụng, màn hình đăng nhập xuất hiện.\n(2) Người dùng nhập Tên đăng nhập (hoặc Mã NV) và Mật khẩu.\n(3) Người dùng nhấn nút \"Đăng nhập\".\n(4) Hệ thống kiểm tra thông tin tài khoản trong cơ sở dữ liệu.\n(5) Hệ thống nhận diện vai trò (Nhân viên / Quản lý) và điều hướng đến màn hình chính tương ứng.",
        '(2a) Người dùng quên mật khẩu: Nhấn nút "Quên mật khẩu" để chuyển sang luồng khôi phục.',
        '(4.1) Tên đăng nhập không tồn tại hoặc mật khẩu sai: Hệ thống thông báo "Sai thông tin đăng nhập!" và yêu cầu nhập lại.\n(4.2) Tài khoản bị khóa: Hệ thống thông báo "Tài khoản của bạn đã bị vô hiệu hóa! Liên hệ Quản lý."'
    )

    # UC02
    style_heading_3("2.2.2. Use Case 2: Sửa thông tin cá nhân (UC02)")
    add_srs_table(
        "UC02",
        "Sửa thông tin cá nhân",
        "Cho phép người dùng cập nhật thông tin cá nhân của mình như họ tên, số điện thoại, ảnh đại diện, địa chỉ.",
        "Nhân viên, Quản lý",
        'Người dùng nhấp vào ảnh đại diện hoặc chọn menu "Thông tin cá nhân".',
        "Người dùng đã đăng nhập thành công vào hệ thống.",
        "Thành công: Thông tin cá nhân được cập nhật vào CSDL và hiển thị thông tin mới.\nThất bại: Dữ liệu cũ giữ nguyên, hiển thị lỗi.",
        "(1) Người dùng chọn chức năng \"Sửa thông tin cá nhân\".\n(2) Hệ thống hiển thị form thông tin hiện tại.\n(3) Người dùng thay đổi các thông tin cần thiết (Họ tên, SĐT, Địa chỉ, Ảnh đại diện).\n(4) Người dùng nhấn nút \"Lưu thay đổi\".\n(5) Hệ thống kiểm tra tính hợp lệ của dữ liệu.\n(6) Hệ thống cập nhật vào CSDL và thông báo cập nhật thành công.",
        '(4a) Người dùng muốn hủy thay đổi: Nhấn nút "Hủy" để khôi phục dữ liệu ban đầu.',
        '(5.1) Số điện thoại không hợp lệ hoặc các trường bắt buộc bị để trống: Hệ thống hiển thị thông báo lỗi và yêu cầu nhập lại.'
    )

    # UC03
    style_heading_3("2.2.3. Use Case 3: Tạo phiếu bán hàng (UC03)")
    add_srs_table(
        "UC03",
        "Tạo phiếu bán hàng",
        "Cho phép nhân viên tạo một order bán đồ uống mới cho khách hàng, tính toán thành tiền và in hóa đơn thanh toán.",
        "Nhân viên bán hàng",
        'Nhân viên nhấn nút "Tạo phiếu mới" trên giao diện POS bán hàng.',
        "Nhân viên đã đăng nhập thành công vào hệ thống với quyền Nhân viên.",
        "Thành công: Phiếu bán hàng được tạo, hóa đơn được lưu vào CSDL, in hóa đơn cho khách và cập nhật doanh thu ca.\nThất bại: Hủy thao tác, phiếu không được lưu.",
        "(1) Nhân viên chọn \"Tạo phiếu mới\".\n(2) Hệ thống hiển thị danh mục loại đồ uống và danh sách món.\n(3) Nhân viên click chọn món đồ uống theo yêu cầu của khách, chọn số lượng, size ly, ghi chú (đá/đường).\n(4) Hệ thống tự động tính thành tiền từng món và tổng tiền của phiếu.\n(5) Nhân viên nhập số tiền khách đưa.\n(6) Hệ thống tính tiền thối lại cho khách.\n(7) Nhân viên nhấn nút \"Thanh toán & In hóa đơn\".\n(8) Hệ thống lưu thông tin hóa đơn vào CSDL và gửi lệnh in ra máy in nhiệt.",
        "(3a) Khách muốn đổi món hoặc chỉnh số lượng: Nhân viên thao tác trực tiếp trên bảng danh sách món đã chọn (gọi Use Case Sửa phiếu bán hàng).",
        '(3.1) Món đồ uống đã hết nguyên liệu (trạng thái Hết hàng): Hệ thống cảnh báo món tạm ngưng phục vụ, không cho thêm vào phiếu.\n(5.1) Số tiền khách đưa nhỏ hơn tổng tiền phải trả: Hệ thống hiển thị cảnh báo "Chưa đủ tiền thanh toán".'
    )

    # UC04
    style_heading_3("2.2.4. Use Case 4: Sửa phiếu bán hàng (UC04)")
    add_srs_table(
        "UC04",
        "Sửa phiếu bán hàng",
        "Cho phép nhân viên bán hàng điều chỉnh món đồ uống, đổi số lượng, thêm ghi chú hoặc xóa món trên phiếu trước khi thanh toán.",
        "Nhân viên bán hàng",
        "Nhân viên chọn một dòng món trên phiếu bán hàng hiện tại.",
        "Phiếu bán hàng đang ở trạng thái Chờ thanh toán (chưa đóng phiếu).",
        "Thành công: Phiếu bán hàng được cập nhật, tổng tiền tự động tính lại.\nThất bại: Dữ liệu trên phiếu giữ nguyên.",
        "(1) Nhân viên chọn phiếu bán hàng cần sửa.\n(2) Nhân viên nhấn nút \"+\" hoặc \"-\" để tăng giảm số lượng món, hoặc nhấn nút \"Xóa món\" để loại bỏ món khỏi phiếu.\n(3) Hệ thống tính toán lại tổng tiền phiếu theo số lượng mới.\n(4) Nhân viên nhấn \"Lưu thay đổi\".\n(5) Hệ thống cập nhật thông tin phiếu bán hàng.",
        '(2a) Khách yêu cầu hủy toàn bộ phiếu: Nhân viên nhấn "Hủy phiếu" kèm theo xác nhận.',
        '(2.1) Số lượng điều chỉnh vượt quá giới hạn hoặc nhỏ hơn 1: Hệ thống cảnh báo số lượng không hợp lệ.'
    )

    # UC05
    style_heading_3("2.2.5. Use Case 5: Xem danh sách hóa đơn cá nhân (UC05)")
    add_srs_table(
        "UC05",
        "Xem danh sách hóa đơn cá nhân",
        "Cho phép nhân viên tra cứu danh sách các hóa đơn do chính mình tạo ra trong ca làm việc để đối soát tiền mặt cuối ca.",
        "Nhân viên bán hàng",
        'Nhân viên chọn mục "Hóa đơn cá nhân" trên menu bán hàng.',
        "Nhân viên đã đăng nhập thành công vào hệ thống.",
        "Thành công: Hiển thị danh sách hóa đơn đã lập của nhân viên kèm tổng doanh số ca.\nThất bại: Báo lỗi không thể tải dữ liệu.",
        "(1) Nhân viên chọn chức năng \"Xem danh sách hóa đơn cá nhân\".\n(2) Hệ thống truy vấn CSDL và hiển thị danh sách hóa đơn do tài khoản hiện tại lập trong ngày.\n(3) Nhân viên có thể nhấp vào một hóa đơn để xem chi tiết danh sách món đã bán.\n(4) Hệ thống hiển thị tổng tiền mặt thu được trong ca để nhân viên bàn giao ca.",
        '(2a) Nhân viên có thể lọc hóa đơn theo khoảng thời gian trong ngày.',
        '(2.1) Không có hóa đơn nào được tạo trong ngày: Hệ thống hiển thị thông báo "Chưa phát sinh hóa đơn nào trong ca hôm nay".'
    )

    # UC06
    style_heading_3("2.2.6. Use Case 6: Quản lý loại đồ uống (UC06)")
    add_srs_table(
        "UC06",
        "Quản lý loại đồ uống",
        "Cho phép Quản lý thêm mới, chỉnh sửa thông tin hoặc xóa danh mục loại đồ uống (Cà phê, Trà, Đá xay, Nước ép).",
        "Quản lý (Manager)",
        'Quản lý chọn mục "Quản lý loại đồ uống" trên thanh điều hướng.',
        "Đã đăng nhập vào hệ thống với vai trò Quản lý.",
        "Thành công: Danh mục loại đồ uống được cập nhật trong CSDL và hiển thị đồng bộ lên phần mềm.\nThất bại: Báo lỗi, dữ liệu không đổi.",
        "(1) Quản lý truy cập chức năng \"Quản lý loại đồ uống\".\n(2) Hệ thống tải danh sách các loại đồ uống hiện có.\n(3) Thêm loại: Quản lý nhập Mã loại, Tên loại đồ uống và nhấn \"Thêm mới\".\n(4) Sửa loại: Quản lý chọn loại đồ uống trong danh sách, sửa tên và nhấn \"Cập nhật\".\n(5) Xóa loại: Quản lý chọn loại đồ uống cần xóa và nhấn \"Xóa\".\n(6) Hệ thống kiểm tra ràng buộc và lưu vào CSDL.\n(7) Hệ thống thông báo thành công và làm mới danh sách.",
        '(3a) Quản lý có thể lọc hoặc tìm kiếm loại đồ uống theo tên.',
        '(3.1) Tên loại bị trùng hoặc để trống: Hệ thống báo lỗi và yêu cầu nhập lại.\n(5.1) Loại đồ uống đang có chứa các món đồ uống đang kinh doanh: Hệ thống cảnh báo không cho phép xóa để bảo đảm toàn vẹn dữ liệu.'
    )

    # UC07
    style_heading_3("2.2.7. Use Case 7: Quản lý đồ uống (UC07)")
    add_srs_table(
        "UC07",
        "Quản lý đồ uống",
        "Cho phép Quản lý thực hiện thêm mới, cập nhật thông tin (tên món, giá bán, size, hình ảnh) hoặc ngừng kinh doanh một món đồ uống.",
        "Quản lý (Manager)",
        'Quản lý truy cập vào mục "Quản lý đồ uống" từ menu quản trị.',
        "Đã đăng nhập với vai trò Quản lý.",
        "Thành công: Danh sách món đồ uống được cập nhật trong CSDL và hiển thị đồng bộ lên màn hình bán hàng của Nhân viên.\nThất bại: Dữ liệu không thay đổi, hệ thống báo lỗi.",
        "(1) Quản lý chọn chức năng \"Quản lý đồ uống\".\n(2) Hệ thống tải và hiển thị danh sách đồ uống hiện có kèm theo ảnh, giá và phân loại.\n(3) Thêm mới: Quản lý nhấn \"Thêm\", nhập Tên đồ uống, chọn Loại đồ uống, nhập Đơn giá, tải ảnh minh họa và nhấn \"Lưu\".\n(4) Sửa: Quản lý chọn món cần sửa trong danh sách, cập nhật thông tin và nhấn \"Cập nhật\".\n(5) Xóa / ngừng bán: Quản lý chọn món và chọn \"Ngừng kinh doanh\" hoặc \"Xóa\".\n(6) Hệ thống kiểm tra tính hợp lệ của dữ liệu và cập nhật vào CSDL.\n(7) Hệ thống thông báo thao tác thành công và tải lại bảng danh sách đồ uống.",
        '(3a) Quản lý có thể lọc hoặc tìm kiếm đồ uống theo tên hoặc danh mục trước khi chỉnh sửa.',
        '(6.1) Dữ liệu nhập trống (tên món để trống, đơn giá <= 0): Hệ thống báo lỗi và bôi đỏ trường dữ liệu sai.\n(6.2) Xóa món đồ uống đã có trong lịch sử hóa đơn: Hệ thống chuyển trạng thái sang "Ngừng kinh doanh" thay vì xóa vật lý để đảm bảo toàn vẹn dữ liệu kế toán.'
    )

    # UC08
    style_heading_3("2.2.8. Use Case 8: Quản lý nhân viên (UC08)")
    add_srs_table(
        "UC08",
        "Quản lý nhân viên",
        "Cho phép Quản lý tạo tài khoản mới cho nhân viên, cập nhật thông tin nhân sự, phân quyền và khóa tài khoản nhân viên nghỉ việc.",
        "Quản lý (Manager)",
        'Quản lý chọn mục "Quản lý nhân viên" trên giao diện quản trị.',
        "Đã đăng nhập với vai trò Quản lý.",
        "Thành công: Hồ sơ nhân viên được lưu vào CSDL, tài khoản mới có thể đăng nhập được.\nThất bại: Báo lỗi và không lưu thông tin.",
        "(1) Quản lý chọn chức năng \"Quản lý nhân viên\".\n(2) Hệ thống hiển thị danh sách nhân viên hiện có.\n(3) Thêm mới: Quản lý nhấn \"Thêm\", nhập Mã NV, Họ tên, SĐT, Email, Tên đăng nhập, Mật khẩu ban đầu và chọn Vai trò (Nhân viên / Quản lý).\n(4) Quản lý nhấn \"Lưu\".\n(5) Hệ thống kiểm tra tính duy nhất của Mã NV và Tên đăng nhập.\n(6) Hệ thống lưu tài khoản vào CSDL và thông báo thành công.",
        '(3a) Để khóa tài khoản: Quản lý chọn nhân viên và tích chọn "Khóa tài khoản" thay vì xóa.',
        '(5.1) Tên đăng nhập hoặc Mã NV bị trùng: Hệ thống thông báo lỗi trùng lặp và yêu cầu đổi tên khác.'
    )

    # UC09
    style_heading_3("2.2.9. Use Case 9: Quản lý hóa đơn (UC09)")
    add_srs_table(
        "UC09",
        "Quản lý hóa đơn",
        "Cho phép Quản lý giám sát toàn bộ các hóa đơn đã phát sinh trong cửa hàng, xem chi tiết từng hóa đơn và xử lý hủy hóa đơn sai sót.",
        "Quản lý (Manager)",
        'Quản lý chọn mục "Quản lý hóa đơn" trên menu quản trị.',
        "Đã đăng nhập với vai trò Quản lý.",
        "Thành công: Hiển thị đầy đủ thông tin hóa đơn theo bộ lọc tìm kiếm.\nThất bại: Thông báo không tìm thấy hóa đơn phù hợp.",
        "(1) Quản lý truy cập chức năng \"Quản lý hóa đơn\".\n(2) Hệ thống hiển thị danh sách hóa đơn theo ngày gần nhất.\n(3) Quản lý chọn các tiêu chí lọc: Theo Ngày, Theo Nhân viên lập, hoặc tìm theo Mã hóa đơn.\n(4) Quản lý nhấp vào một hóa đơn để xem chi tiết các món, tổng tiền, giờ in và nhân viên phụ trách.\n(5) Quản lý có thể thực hiện thao tác \"Hủy hóa đơn\" (kèm lý do) nếu có sự cố nhầm lẫn nghiêm trọng.",
        '(3a) Quản lý có thể xuất danh sách hóa đơn ra file Excel để lưu trữ.',
        '(5.1) Hủy hóa đơn mà không nhập lý do: Hệ thống cảnh báo bắt buộc phải ghi rõ lý do hủy.'
    )

    # UC10
    style_heading_3("2.2.10. Use Case 10: Báo cáo thống kê (UC10)")
    add_srs_table(
        "UC10",
        "Báo cáo thống kê",
        "Cung cấp cho Quản lý số liệu tổng hợp về doanh thu, số lượng hóa đơn, số lượng ly đồ uống tiêu thụ theo mốc thời gian và danh sách đồ uống bán chạy nhất.",
        "Quản lý (Manager)",
        'Quản lý chọn mục "Báo cáo thống kê" trên giao diện quản trị.',
        "Đã đăng nhập thành công vào hệ thống với quyền Quản lý.",
        "Thành công: Hiển thị đầy đủ số liệu và biểu đồ thống kê trực quan theo khoảng thời gian được chọn.\nThất bại: Không có dữ liệu để thống kê trong khoảng thời gian đã lọc.",
        "(1) Quản lý truy cập màn hình \"Báo cáo thống kê\".\n(2) Hệ thống hiển thị mặc định báo cáo doanh thu của Ngày hôm nay.\n(3) Quản lý chọn tiêu chí lọc: Theo Ngày, Theo Tháng, Theo Khoảng ngày (Từ ngày... Đến ngày...) hoặc Theo Nhân viên.\n(4) Quản lý nhấn nút \"Xem thống kê\".\n(5) Hệ thống truy vấn CSDL hóa đơn, tính toán tổng doanh thu, số ly bán, top 5 món bán chạy nhất.\n(6) Hệ thống kết xuất dữ liệu dưới dạng bảng số liệu và biểu đồ trực quan (Biểu đồ cột / tròn).\n(7) Quản lý có thể chọn nút \"Xuất Excel\" để tải file báo cáo về máy.",
        '(3a) Quản lý chỉ lọc theo một nhân viên bán hàng cụ thể để kiểm tra hiệu suất ca làm.',
        '(5.1) Khoảng thời gian được chọn không phát sinh giao dịch nào: Hệ thống hiển thị thông báo "Không có dữ liệu hóa đơn trong khoảng thời gian này" với tổng doanh thu là 0 VNĐ.'
    )

    output_path = r"C:\Net108Khai\BaoCao_Lab1_NET108_Nhom5_QuanLyQuanCaPhe.docx"
    doc.save(output_path)
    print(f"Generated successfully: {output_path}")

if __name__ == "__main__":
    create_full_lab1_document()
