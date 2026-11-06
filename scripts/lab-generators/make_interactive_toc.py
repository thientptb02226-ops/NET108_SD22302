# -*- coding: utf-8 -*-
"""
Script to make all entries in MỤC LỤC interactive and clickable:
1. Places bookmarks on all 30 target headings in the document.
2. Re-creates the Table of Contents paragraphs with <w:hyperlink w:anchor="_Toc_NET108_X"> pointing to those bookmarks.
3. Preserves exact layout, dot leaders, font sizes and page numbers.
"""

import sys
import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

DEFAULT_DOC_PATH = r"C:\Net108Khai\Các Bài Lab\Lab1_NET108_AI_Native_Commerce.docx"
DOC_PATH = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DOC_PATH

toc_items = [
    # (title in TOC, search keyword, page, level, is_bold)
    ("PHẦN MỞ ĐẦU", "PHẦN MỞ ĐẦU", "3", 1, True),
    ("1.1. Tính cấp thiết của đề tài", "1.1. Tính cấp thiết", "3", 2, False),
    ("1.2. Mục tiêu của đề tài", "1.2. Mục tiêu của đề tài", "3", 2, False),
    ("1.3. Đối tượng và phạm vi nghiên cứu", "1.3. Đối tượng và phạm vi", "3", 2, False),
    ("1.4. Phương pháp nghiên cứu", "1.4. Phương pháp nghiên cứu", "4", 2, False),
    ("1 GIỚI THIỆU DỰ ÁN", "CHƯƠNG 1: GIỚI THIỆU DỰ ÁN", "4", 1, True),
    ("1.1. Giới thiệu về Technical Stack", "1.1. Giới thiệu về Technical Stack", "4", 2, False),
    ("1.2. Giới thiệu về AI-Native Commerce Stack", "1.2. Giới thiệu về AI-Native Commerce Stack", "5", 2, False),
    ("1.3. Ứng dụng AI trong tìm kiếm thông tin", "1.3. Ứng dụng AI trong tìm kiếm", "6", 2, False),
    ("1.4. Giới thiệu tổng quan hệ thống AI-Native Commerce", "1.4. Giới thiệu tổng quan hệ thống", "8", 2, False),
    ("2 PHÂN TÍCH YÊU CẦU", "CHƯƠNG 2: KHẢO SÁT VÀ PHÂN TÍCH YÊU CẦU", "11", 1, True),
    ("2.1. Sơ đồ Use Cases", "2.1. Sơ đồ Use Cases", "11", 2, True),
    ("2.1.1. Khảo sát các giải pháp E-Commerce hiện nay", "2.1.1. Khảo sát các giải pháp", "11", 3, False),
    ("2.1.2. Các quy tắc vẽ sơ đồ Use Case UML chuẩn", "2.1.2. Các quy tắc vẽ sơ đồ", "12", 3, False),
    ("2.1.3. Sơ đồ Use Case tổng quát hệ thống AI-Native Commerce", "2.1.3. Sơ đồ Use Case tổng quát", "13", 3, False),
    ("2.1.4. Sơ đồ Use Case phân rã theo phân hệ", "2.1.4. Sơ đồ Use Case phân rã", "14", 3, False),
    ("2.1.5. Phân loại danh sách chức năng theo từng Actor", "2.1.5. Phân loại danh sách chức năng", "16", 3, False),
    ("2.2. Đặc tả yêu cầu hệ thống (SRS)", "2.2. Đặc tả yêu cầu hệ thống", "17", 2, True),
    ("2.3. Xác định các thực thể dữ liệu cốt lõi trong hệ thống", "2.3. Xác định các thực thể dữ liệu", "32", 2, True),
    ("2.3.1. Mô hình quan hệ thực thể mức khái niệm (Conceptual ERD)", "2.3.1. Mô hình quan hệ thực thể", "34", 3, False),
    ("3 THIẾT KẾ HỆ THỐNG", "CHƯƠNG 3: THIẾT KẾ HỆ THỐNG", "35", 1, True),
    ("3.1. Thiết kế tổng thể", "3.1. Thiết kế tổng thể", "35", 2, True),
    ("3.1.1. Sơ đồ triển khai (Deploy Diagram)", "3.1.1. Sơ đồ triển khai", "35", 3, False),
    ("3.1.2. Sơ đồ tổ chức của ứng dụng (Appmap)", "3.1.2. Sơ đồ tổ chức của ứng dụng", "36", 3, False),
    ("3.1.3. Mô hình công nghệ", "3.1.3. Mô hình công nghệ", "37", 3, False),
    ("3.2. Thiết kế UI (giao diện) và Controller (tương tác)", "3.2. Thiết kế UI (giao diện)", "38", 2, True),
    ("3.2.1. Thiết kế các chức năng dùng chung", "3.2.1. Thiết kế các chức năng dùng chung", "38", 3, False),
    ("3.2.2. Thiết kế các chức năng dành cho nhân viên bán hàng", "3.2.2. Thiết kế các chức năng", "39", 3, False),
    ("3.2.3. Thiết kế các chức năng dành cho nhân viên quản lý", "3.2.3. Thiết kế các chức năng", "41", 3, False),
    ("TÀI LIỆU THAM KHẢO", "TÀI LIỆU THAM KHẢO", "43", 1, True),
]

def make_clickable_toc_row(title_text, page_str, bookmark_name, level=1, bold=False):
    title_escaped = title_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    page_escaped = page_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    ind_dxa = 0 if level == 1 else (280 if level == 2 else 560)
    sz_val = "24" if level == 1 else ("22" if level == 2 else "21")
    b_xml = "<w:b/>" if bold or level == 1 else ""
    color_val = "1F4E79" if level == 1 else "000000"
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
        <w:hyperlink w:anchor="{bookmark_name}" w:tooltip="Nhấn giữ phím Ctrl + Click để chuyển đến mục này" w:history="1">
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
    return parse_xml(xml)

def main():
    print("Loading document:", DOC_PATH)
    doc = docx.Document(DOC_PATH)

    # 1. Locate and bookmark target headings
    found_map = {}
    for i in range(40, len(doc.paragraphs)):
        p = doc.paragraphs[i]
        t = p.text.strip()
        for idx, item in enumerate(toc_items):
            kw = item[1]
            if idx not in found_map and kw in t:
                found_map[idx] = p
                break

    print(f"Matched {len(found_map)} headings for bookmarking.")

    # Attach bookmarks to target headings
    for idx, item in enumerate(toc_items):
        if idx in found_map:
            target_p = found_map[idx]
            bm_id = str(200 + idx)
            bm_name = f"_Toc_NET108_{idx}"

            # Check if bookmark already exists
            if bm_name not in target_p._p.xml:
                bm_start = parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="{bm_id}" w:name="{bm_name}"/>')
                bm_end = parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="{bm_id}"/>')
                # Insert at beginning and end of target paragraph
                target_p._p.insert(0, bm_start)
                target_p._p.append(bm_end)
                print(f"  Attached bookmark {bm_name} to: {item[0][:30]}")

    # 2. Replace TOC paragraphs (P10 to P39) with clickable hyperlink rows
    print("Replacing static TOC rows with interactive hyperlinks...")
    # In doc.paragraphs, find index of "MỤC LỤC"
    muc_luc_idx = None
    for i in range(5, 15):
        if doc.paragraphs[i].text.strip() == "MỤC LỤC":
            muc_luc_idx = i
            break
    print("Found MỤC LỤC at paragraph index:", muc_luc_idx)

    # Paragraphs from muc_luc_idx + 1 up to muc_luc_idx + 30 are the TOC entries
    # Replace each paragraph's XML
    for idx, item in enumerate(toc_items):
        p_idx = muc_luc_idx + 1 + idx
        p_curr = doc.paragraphs[p_idx]
        bm_name = f"_Toc_NET108_{idx}"
        new_p_xml = make_clickable_toc_row(item[0], item[2], bm_name, level=item[3], bold=item[4])
        # Replace the paragraph element
        p_curr._p.getparent().replace(p_curr._p, new_p_xml)

    print("Saving document with interactive TOC to:", DOC_PATH)
    doc.save(DOC_PATH)
    print("=== FINISHED MAKING MỤC LỤC FULLY INTERACTIVE & CLICKABLE! ===")

if __name__ == "__main__":
    main()
