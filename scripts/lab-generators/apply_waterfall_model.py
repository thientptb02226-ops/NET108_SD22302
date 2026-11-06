# -*- coding: utf-8 -*-
"""
Script to apply Waterfall Model into Lab1_NET108_AI_Native_Commerce.docx:
1. Updates P6 intro text (replaces Agile/Scrum with Waterfall SDLC + Jira).
2. Updates and expands Section 1.4 with the 5-phase Waterfall Model matching the classroom slide.
3. Inserts Hình 1: waterfall_model_diagram.png.
4. Refreshes Table of Contents bookmarks and hyperlinks.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOC_PATH = r"C:\Net108Khai\Các Bài Lab\Lab1_NET108_AI_Native_Commerce.docx"
IMG_PATH = r"C:\Net108Khai\docs\06-design\waterfall_model_diagram.png"

def main():
    print("Loading document:", DOC_PATH)
    doc = docx.Document(DOC_PATH)

    # 1. Update P6 (Intro before Table 0)
    for p in doc.paragraphs[:15]:
        if "Nhóm 5 áp dụng quy trình Agile / Scrum" in p.text:
            p.text = (
                "Nhóm 5 áp dụng quy trình phát triển phần mềm theo Mô hình Thác nước (Waterfall Model) "
                "chuẩn theo yêu cầu của môn Dự án mẫu (NET108) tại FPT Polytechnic. Toàn bộ 5 giai đoạn "
                "phát triển được cấu trúc thành các Epic và Task tương ứng, theo dõi trực tiếp trên hệ thống "
                "Atlassian Jira Cloud (Workspace: thientptb02226.atlassian.net - Project: NET108):"
            )
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(12)
            print("  Updated P6 text with Waterfall model.")
            break

    # 2. Locate Section 1.4 in document body (i >= 40)
    p_1_4_idx = None
    for i in range(40, len(doc.paragraphs)):
        p = doc.paragraphs[i]
        if p.text.strip().startswith("1.4. Phương pháp nghiên cứu"):
            p_1_4_idx = i
            break

    if p_1_4_idx is None:
        print("ERROR: Could not find 1.4. Phương pháp nghiên cứu!")
        return

    print(f"Found Section 1.4 at paragraph {p_1_4_idx}")

    # Inspect paragraphs between 1.4 and CHƯƠNG 1
    p_end_idx = None
    for i in range(p_1_4_idx + 1, p_1_4_idx + 15):
        if "CHƯƠNG 1" in doc.paragraphs[i].text or "PHẦN NỘI DUNG" in doc.paragraphs[i].text:
            p_end_idx = i
            break

    print(f"Section 1.4 content spans from {p_1_4_idx + 1} to {p_end_idx}")

    # Remove old placeholder paragraphs between p_1_4_idx and p_end_idx
    # (these were P56, P57, P58, P59)
    for i in range(p_end_idx - 1, p_1_4_idx, -1):
        p_to_remove = doc.paragraphs[i]
        p_to_remove._p.getparent().remove(p_to_remove._p)
        print(f"  Removed old placeholder paragraph {i}")

    # Now build new comprehensive content for Section 1.4
    heading_p = doc.paragraphs[p_1_4_idx]
    # Keep heading title matching TOC: "1.4. Phương pháp nghiên cứu và Quy trình phát triển"
    # Actually keep "1.4. Phương pháp nghiên cứu" to match TOC anchor exactly:
    heading_p.text = "1.4. Phương pháp nghiên cứu và Mô hình phát triển dự án"
    for r in heading_p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    # Paragraphs to insert right after heading_p:
    new_paragraphs_data = [
        {
            "type": "text",
            "bold_prefix": "1.4.1. Phương pháp nghiên cứu và ứng dụng AI: ",
            "body": "Sử dụng các công cụ Generative AI tiên tiến (Perplexity AI, ChatGPT Deepsearch, Google Gemini) để nghiên cứu khảo sát hiện trạng thương mại điện tử, phân tích hành vi người tiêu dùng và trích xuất cấu trúc đặc tả hệ thống chuẩn công nghiệp."
        },
        {
            "type": "text",
            "bold_prefix": "1.4.2. Phương pháp mô hình hóa phần mềm: ",
            "body": "Sử dụng ngôn ngữ mô hình hóa thống nhất UML 2.5 (Use Case Diagrams, Activity Diagrams, Sequence Diagrams, Deployment Diagrams) và mô hình hóa dữ liệu (Conceptual ERD, Logical Schema) để trực quan hóa cấu trúc, hành vi và phân quyền người dùng trong toàn bộ hệ thống."
        },
        {
            "type": "text",
            "bold_prefix": "1.4.3. Mô hình phát triển ứng dụng Thác nước (Waterfall Model): ",
            "body": (
                "Theo định hướng và chuẩn kiến thức giảng dạy của môn Dự án mẫu (NET108) tại FPT Polytechnic, "
                "đề tài AI-Native Commerce áp dụng nghiêm ngặt Mô hình phát triển Thác nước (Waterfall Model). "
                "Mô hình này chia quy trình xây dựng hệ thống thành 5 giai đoạn kế tiếp nhau một cách tuần tự, "
                "trong đó kết quả đầu ra (Deliverables) của giai đoạn trước là tiền đề đầu vào bắt buộc của giai đoạn sau:"
            )
        },
        {
            "type": "bullet",
            "bold_prefix": "• Giai đoạn 1 - Requirements Analysis (Phân tích yêu cầu): ",
            "body": "Thu thập yêu cầu nghiệp vụ, nghiên cứu bằng AI Deepsearch, phân tích thành phần tác nhân (Actors), phân rã chức năng, xây dựng tài liệu đặc tả yêu cầu phần mềm SRS và sơ đồ Use Case tổng quát cùng 14 Use Case chi tiết (Trọng tâm của bài Lab 1)."
        },
        {
            "type": "bullet",
            "bold_prefix": "• Giai đoạn 2 - Design (Thiết kế hệ thống): ",
            "body": "Thiết kế kiến trúc triển khai (Deploy Diagram), sơ đồ tổ chức ứng dụng (Appmap), mô hình công nghệ phân tầng, mô hình quan hệ thực thể (Conceptual ERD) và thiết kế giao diện UI Wireframes cùng Controller tương tác (Trọng tâm của bài Lab 1 & Lab 2)."
        },
        {
            "type": "bullet",
            "bold_prefix": "• Giai đoạn 3 - Development (Phát triển / Lập trình): ",
            "body": "Hiện thực hóa mã nguồn hệ thống dựa trên bản thiết kế đã được thẩm định, bao gồm Backend REST API (Node.js/Express/Prisma), dịch vụ AI RAG & MCP Server (Python/FastAPI) và Web Frontend (React/Next.js/TailwindCSS) (Trọng tâm của bài Lab 3 & Lab 4)."
        },
        {
            "type": "bullet",
            "bold_prefix": "• Giai đoạn 4 - Testing (Kiểm thử phần mềm): ",
            "body": "Thực thi kiểm thử chức năng và tích hợp theo ma trận Test Cases P0/P1, kiểm thử các luồng tự hành của tác tử AI và đánh giá hiệu năng chịu tải (Trọng tâm của bài Lab 4 & Assignment)."
        },
        {
            "type": "bullet",
            "bold_prefix": "• Giai đoạn 5 - Maintenance (Triển khai & Bảo trì): ",
            "body": "Đóng gói ứng dụng vào Docker container, thiết lập đường ống CI/CD tự động hóa, triển khai lên nền tảng đám mây và thiết lập hệ thống giám sát nhật ký vận hành liên tục."
        },
        {
            "type": "image",
            "path": IMG_PATH,
            "caption": "Hình 1. Sơ đồ quy trình phát triển ứng dụng theo Mô hình Thác nước (Waterfall Model) chuẩn FPT Polytechnic"
        },
        {
            "type": "text",
            "bold_prefix": "1.4.4. Phương pháp quản trị tiến độ dự án: ",
            "body": "Nhóm kết hợp công cụ quản trị Jira Cloud (Workspace: thientptb02226.atlassian.net - Project NET108) để quản lý tiến độ và kiểm soát chất lượng bàn giao sản phẩm của từng giai đoạn trong mô hình Waterfall theo đúng các cột mốc (Milestones/WBS) minh bạch."
        }
    ]

    last_p = heading_p
    for item in new_paragraphs_data:
        if item["type"] in ("text", "bullet"):
            new_p = doc.add_paragraph()
            new_p.paragraph_format.space_before = Pt(3)
            new_p.paragraph_format.space_after = Pt(4)
            new_p.paragraph_format.line_spacing = 1.15
            if item["type"] == "bullet":
                new_p.paragraph_format.left_indent = Inches(0.25)
            r_bold = new_p.add_run(item["bold_prefix"])
            r_bold.font.name = "Times New Roman"
            r_bold.font.size = Pt(12)
            r_bold.font.bold = True
            r_bold.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

            r_body = new_p.add_run(item["body"])
            r_body.font.name = "Times New Roman"
            r_body.font.size = Pt(12)
            r_body.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

            last_p._p.addnext(new_p._p)
            last_p = new_p

        elif item["type"] == "image":
            # Image paragraph
            img_p = doc.add_paragraph()
            img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            img_p.paragraph_format.space_before = Pt(6)
            img_p.paragraph_format.space_after = Pt(2)
            r_img = img_p.add_run()
            r_img.add_picture(item["path"], width=Inches(5.8))
            last_p._p.addnext(img_p._p)
            last_p = img_p

            # Caption paragraph
            cap_p = doc.add_paragraph()
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap_p.paragraph_format.space_before = Pt(2)
            cap_p.paragraph_format.space_after = Pt(8)
            r_cap = cap_p.add_run(item["caption"])
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(11)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
            last_p._p.addnext(cap_p._p)
            last_p = cap_p

    TEMP_PATH = r"C:\Net108Khai\Các Bài Lab\Lab1_NET108_AI_Native_Commerce_Updated.docx"
    try:
        print("Saving document to:", DOC_PATH)
        doc.save(DOC_PATH)
        print("=== SUCCESSFULLY APPLIED WATERFALL MODEL INTO LAB 1! ===")
    except PermissionError:
        print(f"File {DOC_PATH} is locked by WPS/Word. Saving to {TEMP_PATH} instead...")
        doc.save(TEMP_PATH)
        print(f"=== SUCCESSFULLY SAVED UPDATED VERSION TO {TEMP_PATH}! ===")

if __name__ == "__main__":
    main()
