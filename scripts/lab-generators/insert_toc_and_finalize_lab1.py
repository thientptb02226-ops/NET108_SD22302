# -*- coding: utf-8 -*-
"""
Script to finalize Lab 1 document:
1. Rename Chapter 1 to: CHƯƠNG 1: GIỚI THIỆU DỰ ÁN VÀ CƠ SỞ LÝ THUYẾT
2. Rename Section 3.2.2 to: 3.2.2. Thiết kế các chức năng dành cho nhân viên bán hàng và khách hàng
3. Insert Page Break after Table 0 (Jira table)
4. Insert DANH MỤC BẢNG (22 tables with dot leaders & page numbers) + Page Break
5. Insert DANH MỤC HÌNH (12 figures with dot leaders & page numbers) + Page Break
6. Insert MỤC LỤC (Hierarchical Table of Contents matching user's image with dot leaders & page numbers) + Page Break
All placed cleanly before PHẦN MỞ ĐẦU, without altering cover page or Jira table formatting.
"""

import os
import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

DOC_PATH = r"C:\Net108Khai\Các Bài Lab\Lab1_NET108_AI_Native_Commerce.docx"

def make_toc_heading(title_text):
    xml = f'''<w:p {nsdecls("w")}>
        <w:pPr>
            <w:jc w:val="center"/>
            <w:spacing w:before="240" w:after="160" w:line="280" w:lineRule="auto"/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                <w:b/>
                <w:sz w:val="32"/>
                <w:color w:val="1F4E79"/>
            </w:rPr>
            <w:t>{title_text}</w:t>
        </w:r>
    </w:p>'''
    return parse_xml(xml)

def make_page_break():
    xml = f'''<w:p {nsdecls("w")}>
        <w:r>
            <w:br w:type="page"/>
        </w:r>
    </w:p>'''
    return parse_xml(xml)

def make_toc_row(title_text, page_str, level=1, bold=False):
    title_escaped = title_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    page_escaped = page_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Indent based on level
    ind_dxa = 0 if level == 1 else (280 if level == 2 else 560)
    sz_val = "24" if level == 1 else ("22" if level == 2 else "21")
    b_xml = "<w:b/>" if bold or level == 1 else ""
    color_val = "1F4E79" if level == 1 else ("203040" if level == 2 else "405060")
    space_before = "70" if level == 1 else ("35" if level == 2 else "25")
    space_after = "35" if level == 1 else ("25" if level == 2 else "20")

    xml = f'''<w:p {nsdecls("w")}>
        <w:pPr>
            <w:tabs>
                <w:tab w:val="right" w:leader="dot" w:pos="9072"/>
            </w:tabs>
            <w:spacing w:before="{space_before}" w:after="{space_after}" w:line="250" w:lineRule="auto"/>
            <w:ind w:left="{ind_dxa}"/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                {b_xml}
                <w:sz w:val="{sz_val}"/>
                <w:color w:val="{color_val}"/>
            </w:rPr>
            <w:t>{title_escaped}</w:t>
        </w:r>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                {b_xml}
                <w:sz w:val="{sz_val}"/>
                <w:color w:val="{color_val}"/>
            </w:rPr>
            <w:tab/>
            <w:t>{page_escaped}</w:t>
        </w:r>
    </w:p>'''
    return parse_xml(xml)

def main():
    print("Opening docx:", DOC_PATH)
    doc = docx.Document(DOC_PATH)

    # 1. Rename Chapter 1 heading
    for p in doc.paragraphs:
        if "CHƯƠNG 1:" in p.text:
            print("Found Chapter 1:", p.text)
            p.text = "CHƯƠNG 1: GIỚI THIỆU DỰ ÁN VÀ CƠ SỞ LÝ THUYẾT"
            p.style = doc.styles["Heading 2"]
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.bold = True
                r.font.color.rgb = docx.shared.RGBColor(31, 78, 121)
            print("Renamed Chapter 1 to:", p.text)
            break

    # 2. Rename Section 3.2.2 heading
    for p in doc.paragraphs:
        if "3.2.2." in p.text:
            print("Found Section 3.2.2:", p.text)
            p.text = "3.2.2. Thiết kế các chức năng dành cho nhân viên bán hàng và khách hàng"
            p.style = doc.styles["Heading 4"]
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.bold = True
                r.font.color.rgb = docx.shared.RGBColor(0, 0, 0)
            print("Renamed Section 3.2.2 to:", p.text)
            break

    # 3. Locate insertion point before PHẦN MỞ ĐẦU
    body = doc._body._body
    p_modau_idx = None
    for i, child in enumerate(body):
        tag = child.tag.split("}")[-1]
        if tag == "p":
            txt = "".join(child.itertext()).strip()
            if "PHẦN MỞ ĐẦU" in txt:
                p_modau_idx = i
                print("Found PHẦN MỞ ĐẦU at child index:", i)
                break

    target_elem = body[p_modau_idx]

    # Elements to insert (in order)
    new_elements = []

    # Page Break after Jira table
    new_elements.append(make_page_break())

    # ==================== DANH MỤC BẢNG ====================
    new_elements.append(make_toc_heading("DANH MỤC BẢNG"))
    tables_list = [
        ("Bảng 1. Kế hoạch triển khai và theo dõi tiến độ trên hệ thống Jira Cloud", "2"),
        ("Bảng 2. Nhật ký câu lệnh Prompting AI nghiên cứu và đặc tả hệ thống", "6"),
        ("Bảng 3. Ma trận phân loại vai trò và trách nhiệm các tác nhân (Actors)", "8"),
        ("Bảng 4. Danh mục 16 module nền tảng của hệ thống AI-Native Commerce", "9"),
        ("Bảng 5. Đặc tả SRS UC01 — Đăng ký tài khoản", "17"),
        ("Bảng 6. Đặc tả SRS UC02 — Đăng nhập hệ thống", "18"),
        ("Bảng 7. Đặc tả SRS UC03 — Quên mật khẩu", "19"),
        ("Bảng 8. Đặc tả SRS UC04 — Tìm kiếm bằng ngôn ngữ tự nhiên", "20"),
        ("Bảng 9. Đặc tả SRS UC05 — Tương tác với AI Shopping Assistant", "21"),
        ("Bảng 10. Đặc tả SRS UC06 — Quản lý giỏ hàng thông minh", "22"),
        ("Bảng 11. Đặc tả SRS UC07 — Đặt hàng và áp dụng khuyến mãi tự động", "23"),
        ("Bảng 12. Đặc tả SRS UC08 — Thanh toán trực tuyến qua VNPay", "24"),
        ("Bảng 13. Đặc tả SRS UC09 — Tra cứu đơn hàng và theo dõi vận chuyển", "25"),
        ("Bảng 14. Đặc tả SRS UC10 — Quản lý danh mục & sản phẩm chuẩn hóa cho AI", "26"),
        ("Bảng 15. Đặc tả SRS UC11 — Quản lý đơn hàng và trạng thái đơn hàng", "27"),
        ("Bảng 16. Đặc tả SRS UC12 — Quản lý tài khoản và phân quyền RBAC", "28"),
        ("Bảng 17. Đặc tả SRS UC13 — Báo cáo thống kê và phân tích hành vi AI", "29"),
        ("Bảng 18. Đặc tả SRS UC14 — Thực thi giao dịch qua giao thức tác tử AI", "30"),
        ("Bảng 19. Bảng danh mục các thực thể dữ liệu cốt lõi trong hệ thống", "32"),
        ("Bảng 20. Bảng thiết kế Controller và Luồng tương tác các chức năng dùng chung", "38"),
        ("Bảng 21. Bảng thiết kế Controller và Luồng tương tác phân hệ Khách hàng", "40"),
        ("Bảng 22. Bảng thiết kế Controller và Luồng tương tác phân hệ Quản lý & Nhà bán", "42"),
    ]
    for title, pg in tables_list:
        new_elements.append(make_toc_row(title, pg, level=1, bold=False))

    new_elements.append(make_page_break())

    # ==================== DANH MỤC HÌNH ====================
    new_elements.append(make_toc_heading("DANH MỤC HÌNH"))
    figures_list = [
        ("Hình 1. Sơ đồ quy trình làm việc và tương tác giữa các tác tử AI", "7"),
        ("Hình 2. Sơ đồ Use Case tổng quát Hệ thống AI-Native Commerce (28 UCs)", "13"),
        ("Hình 3. Sơ đồ Use Case Phân hệ Khách hàng (Guest & Customer)", "14"),
        ("Hình 4. Sơ đồ Use Case Phân hệ Quản trị & Nhà bán hàng (Merchant & Admin)", "15"),
        ("Hình 5. Sơ đồ Use Case Phân hệ Nền tảng Tác tử AI (AI Agent Platform)", "16"),
        ("Hình 6. Sơ đồ mô hình quan hệ thực thể mức khái niệm (Conceptual ERD)", "34"),
        ("Hình 7. Sơ đồ triển khai hệ thống (Deployment Diagram)", "35"),
        ("Hình 8. Sơ đồ tổ chức của ứng dụng (Appmap / Sitemap Navigation Flow)", "36"),
        ("Hình 9. Sơ đồ phân tầng mô hình công nghệ (Tech Stack Architecture)", "37"),
        ("Hình 10. Thiết kế giao diện (UI Wireframe) các chức năng dùng chung", "39"),
        ("Hình 11. Thiết kế giao diện (UI Wireframe) phân hệ Khách hàng & Mua sắm AI", "40"),
        ("Hình 12. Thiết kế giao diện (UI Wireframe) phân hệ Quản trị & Nhà bán hàng", "42"),
    ]
    for title, pg in figures_list:
        new_elements.append(make_toc_row(title, pg, level=1, bold=False))

    new_elements.append(make_page_break())

    # ==================== MỤC LỤC CHÍNH (TABLE OF CONTENTS) ====================
    new_elements.append(make_toc_heading("MỤC LỤC"))
    toc_structure = [
        ("PHẦN MỞ ĐẦU", "3", 1, True),
        ("1.1. Tính cấp thiết của đề tài", "3", 2, False),
        ("1.2. Mục tiêu của đề tài", "3", 2, False),
        ("1.3. Đối tượng và phạm vi nghiên cứu", "3", 2, False),
        ("1.4. Phương pháp nghiên cứu", "4", 2, False),
        ("1 GIỚI THIỆU DỰ ÁN", "4", 1, True),
        ("1.1. Giới thiệu về Technical Stack", "4", 2, False),
        ("1.2. Giới thiệu về AI-Native Commerce Stack", "5", 2, False),
        ("1.3. Ứng dụng AI trong tìm kiếm thông tin", "6", 2, False),
        ("1.4. Giới thiệu tổng quan hệ thống AI-Native Commerce", "8", 2, False),
        ("2 PHÂN TÍCH YÊU CẦU", "11", 1, True),
        ("2.1. Sơ đồ Use Cases", "11", 2, True),
        ("2.1.1. Khảo sát các giải pháp E-Commerce hiện nay", "11", 3, False),
        ("2.1.2. Các quy tắc vẽ sơ đồ Use Case UML chuẩn", "12", 3, False),
        ("2.1.3. Sơ đồ Use Case tổng quát hệ thống AI-Native Commerce", "13", 3, False),
        ("2.1.4. Sơ đồ Use Case phân rã theo phân hệ", "14", 3, False),
        ("2.1.5. Phân loại danh sách chức năng theo từng Actor", "16", 3, False),
        ("2.2. Đặc tả yêu cầu hệ thống (SRS)", "17", 2, True),
        ("2.3. Xác định các thực thể dữ liệu cốt lõi trong hệ thống", "32", 2, True),
        ("2.3.1. Mô hình quan hệ thực thể mức khái niệm (Conceptual ERD)", "34", 3, False),
        ("3 THIẾT KẾ HỆ THỐNG", "35", 1, True),
        ("3.1. Thiết kế tổng thể", "35", 2, True),
        ("3.1.1. Sơ đồ triển khai (Deploy Diagram)", "35", 3, False),
        ("3.1.2. Sơ đồ tổ chức của ứng dụng (Appmap)", "36", 3, False),
        ("3.1.3. Mô hình công nghệ", "37", 3, False),
        ("3.2. Thiết kế UI (giao diện) và Controller (tương tác)", "38", 2, True),
        ("3.2.1. Thiết kế các chức năng dùng chung", "38", 3, False),
        ("3.2.2. Thiết kế các chức năng dành cho nhân viên bán hàng", "39", 3, False),
        ("3.2.3. Thiết kế các chức năng dành cho nhân viên quản lý", "41", 3, False),
        ("TÀI LIỆU THAM KHẢO", "43", 1, True),
    ]

    for title, pg, lvl, is_b in toc_structure:
        new_elements.append(make_toc_row(title, pg, level=lvl, bold=is_b))

    new_elements.append(make_page_break())

    # Insert all elements right before target_elem
    print(f"Inserting {len(new_elements)} TOC elements before PHẦN MỞ ĐẦU...")
    for elem in new_elements:
        target_elem.addprevious(elem)

    print("Saving finalized document to:", DOC_PATH)
    doc.save(DOC_PATH)
    print("=== FINISHED INSERTING TOC & FINALIZING REPORT! ===")

if __name__ == "__main__":
    main()
