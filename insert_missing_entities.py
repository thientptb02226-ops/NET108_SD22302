# -*- coding: utf-8 -*-
import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def style_table(table, widths, header_bg="1F4E79", alt_bg="F2F5F8"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    borders_xml = (
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'</w:tcBorders>'
    )
    for row_idx, row in enumerate(table.rows):
        is_hdr = (row_idx == 0)
        bg = header_bg if is_hdr else (alt_bg if row_idx % 2 == 1 else "FFFFFF")
        for col_idx, cell in enumerate(row.cells):
            if col_idx < len(widths):
                cell.width = widths[col_idx]
            tcPr = cell._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(borders_xml))
            shading = f'<w:shd {nsdecls("w")} w:fill="{bg}"/>'
            tcPr.append(parse_xml(shading))
            tcMar = f'<w:tcMar {nsdecls("w")}><w:top w:w="80"/><w:bottom w:w="80"/><w:left w:w="120"/><w:right w:w="120"/></w:tcMar>'
            tcPr.append(parse_xml(tcMar))

            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.05
                if is_hdr or col_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10.5 if is_hdr else 10)
                    if is_hdr:
                        r.font.bold = True
                        r.font.color.rgb = RGBColor(255, 255, 255)
                    else:
                        r.font.color.rgb = RGBColor(30, 30, 30)

def insert_missing_section(target_path):
    print("Processing:", target_path)
    doc = docx.Document(target_path)

    # 1. Update image blobs in-place so diagrams are high-res with include/extend
    img_map = {
        "rId10": r"C:\Net108Khai\usecase_ainative_tongquat.png",
        "rId11": r"C:\Net108Khai\usecase_ainative_customer.png",
        "rId12": r"C:\Net108Khai\usecase_ainative_admin.png",
        "rId13": r"C:\Net108Khai\usecase_ainative_agent.png",
    }
    for rel_id, img_path in img_map.items():
        if rel_id in doc.part.rels and os.path.exists(img_path):
            with open(img_path, "rb") as f:
                doc.part.rels[rel_id].target_part._blob = f.read()
            print(f"Updated image {rel_id} from {os.path.basename(img_path)}")

    # 2. Check if 2.6 already exists
    for p in doc.paragraphs:
        if "2.6. Xác định các thực thể" in p.text:
            print("Section 2.6 already exists! Skipping insertion.")
            doc.save(target_path)
            return

    # 3. Create elements in a temporary document
    temp = docx.Document()

    # Heading 2
    h2 = temp.add_heading("2.6. Xác định các thực thể dữ liệu cốt lõi trong hệ thống (Entity Identification)", level=2)
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)
    h2.paragraph_format.keep_with_next = True
    pPr = h2._p.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="1"/>'))
    for r in h2.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(46, 117, 182)

    # Intro paragraph
    p_intro = temp.add_paragraph(
        "Theo yêu cầu trọng tâm của Bài 3 ('Vẽ mô hình hệ thống và xác định các thực thể'), việc định danh và mô hình hóa danh mục các thực thể dữ liệu nghiệp vụ (Entities) là tiền đề bắt buộc nhằm chuẩn bị trực tiếp cho Bài Lab 2 (Thiết kế sơ đồ quan hệ thực thể ERD, thiết kế cơ sở dữ liệu quan hệ Microsoft SQL Server và viết mã kịch bản SQL DDL). Căn cứ theo bản thiết kế kiến trúc AI-Native Commerce Blueprint, nhóm đã xác định được 18 thực thể dữ liệu cốt lõi phân chia thành 9 nhóm nghiệp vụ hoàn chỉnh như sau:"
    )
    p_intro.paragraph_format.space_before = Pt(0)
    p_intro.paragraph_format.space_after = Pt(6)
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for r in p_intro.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    # Table 23
    entity_headers = ["STT", "Nhóm nghiệp vụ", "Tên thực thể (Entity)", "Mô tả nghiệp vụ", "Các thuộc tính cốt lõi (Core Attributes)"]
    entity_data = [
        ["1", "Identity & Auth", "User", "Tài khoản người dùng đăng nhập hệ thống", "Id, Email, PasswordHash, FullName, PhoneNumber, Status, CreatedAt"],
        ["2", "Identity & Auth", "Role / Permission", "Định nghĩa vai trò (Admin, Merchant, Customer) & ma trận quyền RBAC", "Id, RoleName, Scope, Action, Description"],
        ["3", "Customer", "CustomerProfile", "Hồ sơ người dùng, sở thích mua sắm & ngân sách ủy quyền AI", "Id, UserId, PreferencesJson, SpendingLimit, ConsentPolicy, UpdatedAt"],
        ["4", "Merchant", "Merchant", "Thông tin doanh nghiệp / nhà bán hàng tham gia sàn thương mại", "Id, MerchantName, TaxCode, ContactEmail, LegalAddress, Status"],
        ["5", "Catalog", "Category", "Cây danh mục phân cấp sản phẩm chuẩn hóa cho AI tra cứu", "Id, CategoryName, Slug, ParentId, Description, IsActive"],
        ["6", "Catalog", "Product", "Thông tin sản phẩm cốt lõi (tên, mô tả, nhà sản xuất)", "Id, MerchantId, CategoryId, Name, Description, BasePrice, CreatedAt"],
        ["7", "Catalog", "ProductVariant", "Phiên bản biến thể chi tiết (màu sắc, kích thước, SKU)", "Id, ProductId, Sku, Color, Size, PriceAdjustment, StockQuantity"],
        ["8", "Catalog & AI", "ProductEmbedding", "Vector Embeddings (1536 chiều) phục vụ Hybrid Vector Search", "Id, ProductId, Sku, EmbeddingVector, MetadataJson, UpdatedAt"],
        ["9", "Shopping", "Cart", "Giỏ hàng thông minh của người dùng (hỗ trợ AI quản lý)", "Id, CustomerId, SessionId, Status, CreatedAt, UpdatedAt"],
        ["10", "Shopping", "CartItem", "Chi tiết mặt hàng và số lượng người dùng chọn trong giỏ", "Id, CartId, ProductVariantId, Quantity, UnitPrice, AddedByAgent"],
        ["11", "Order", "Order", "Đơn hàng hoàn tất bao gồm tổng tiền, khuyến mãi, trạng thái", "Id, CustomerId, OrderCode, TotalAmount, DiscountAmount, Status, CreatedAt"],
        ["12", "Order", "OrderItem", "Chi tiết từng dòng sản phẩm được xác nhận trong đơn hàng", "Id, OrderId, ProductVariantId, Quantity, UnitPrice, LineTotal"],
        ["13", "Payment", "PaymentTransaction", "Giao dịch thanh toán trực tuyến qua cổng VNPay / Ví điện tử", "Id, OrderId, Gateway, TransactionRef, Amount, Status, PaidAt"],
        ["14", "Fulfillment", "Shipment", "Thông tin vận chuyển, mã vận đơn và tiến độ giao nhận", "Id, OrderId, CarrierName, TrackingCode, ShippingFee, Status, ShippedAt"],
        ["15", "AI Platform", "AgentDefinition", "Cấu hình tác tử AI (Shopping Agent, Pricing Agent, CS Agent)", "Id, AgentName, ModelId, SystemPrompt, PolicyId, Version, IsActive"],
        ["16", "AI Platform", "AIConversation", "Phiên hội thoại mua sắm tương tác giữa người dùng và Trợ lý AI", "Id, CustomerId, AgentId, SessionTitle, ContextSummary, CreatedAt"],
        ["17", "AI Platform", "AgentRun", "Nhật ký thực thi tác tử AI và vết gọi công cụ (Tool Call Trace)", "Id, ConversationId, AgentId, IntentName, ToolCallsJson, ExecutionState"],
        ["18", "Governance", "AuditEvent", "Nhật ký kiểm toán an ninh và giao dịch tự động của tác tử ACP", "Id, ActorId, Action, Resource, IpAddress, Timestamp, GuardrailCheckResult"]
    ]

    widths = [Inches(0.4), Inches(1.3), Inches(1.5), Inches(2.2), Inches(2.0)]
    tbl = temp.add_table(rows=len(entity_data) + 1, cols=len(entity_headers))
    for c_idx, h in enumerate(entity_headers):
        tbl.rows[0].cells[c_idx].text = h
    for r_idx, row in enumerate(entity_data):
        for c_idx, val in enumerate(row):
            tbl.rows[r_idx + 1].cells[c_idx].text = val
    style_table(tbl, widths)

    # Caption
    p_cap = temp.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(4)
    p_cap.paragraph_format.space_after = Pt(8)
    r = p_cap.add_run("Bảng 23. Bảng danh mục các thực thể dữ liệu cốt lõi trong hệ thống (Entity Identification)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.italic = True

    # Heading 3
    h3 = temp.add_heading("2.6.1. Mô hình quan hệ thực thể mức khái niệm (Conceptual Entity Relationships)", level=3)
    h3.paragraph_format.space_before = Pt(8)
    h3.paragraph_format.space_after = Pt(3)
    h3.paragraph_format.keep_with_next = True
    pPr3 = h3._p.get_or_add_pPr()
    pPr3.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="2"/>'))
    for r in h3.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 78, 121)

    # Paragraph intro to bullets
    p_desc = temp.add_paragraph("Mối quan hệ nghiệp vụ giữa các thực thể dữ liệu cốt lõi của Hệ thống AI-Native Commerce được xác lập chặt chẽ:")
    p_desc.paragraph_format.space_before = Pt(0)
    p_desc.paragraph_format.space_after = Pt(4)
    p_desc.paragraph_format.line_spacing = 1.15
    for r in p_desc.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    # Bullets
    bullets_text = [
        "Một Customer sở hữu một Cart đang hoạt động (quan hệ 1 - 1) và có thể đặt nhiều Orders qua thời gian (quan hệ 1 - n).",
        "Một Merchant quản lý và kinh doanh nhiều Products (quan hệ 1 - n); mỗi Product có nhiều ProductVariants (quan hệ 1 - n) và liên kết với một ProductEmbedding phục vụ tìm kiếm ngữ nghĩa.",
        "Một Cart chứa nhiều CartItems (quan hệ 1 - n); một Order chứa nhiều OrderItems (quan hệ 1 - n).",
        "Một Order phát sinh một hoặc nhiều PaymentTransactions (quan hệ 1 - n) và liên kết với một bản ghi Shipment vận chuyển (quan hệ 1 - 1).",
        "Một Customer tham gia nhiều AIConversations với AgentDefinition (quan hệ 1 - n); mỗi Conversation ghi nhận nhiều lượt AgentRuns và mọi hành động nhạy cảm đều được lưu vết kiểm toán vào AuditEvents."
    ]
    bullet_elements = []
    for bt in bullets_text:
        pb = temp.add_paragraph()
        pb.paragraph_format.left_indent = Inches(0.25)
        pb.paragraph_format.space_before = Pt(0)
        pb.paragraph_format.space_after = Pt(3)
        pb.paragraph_format.line_spacing = 1.15
        r_pre = pb.add_run("• ")
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_txt = pb.add_run(bt)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(12)
        bullet_elements.append(pb._p)

    # Summary
    p_sum = temp.add_paragraph(
        "Bảng danh mục thực thể và mô hình quan hệ khái niệm trên đây đảm bảo đầy đủ và chính xác 100% cơ sở dữ liệu để nhóm 5 hiện thực hóa sơ đồ ERD, thiết kế khóa chính/khóa ngoại và kịch bản cơ sở dữ liệu trên Microsoft SQL Server trong Bài Lab 2."
    )
    p_sum.paragraph_format.space_before = Pt(4)
    p_sum.paragraph_format.space_after = Pt(8)
    p_sum.paragraph_format.line_spacing = 1.15
    p_sum.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for r in p_sum.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    # 4. Insert all elements right after Table 21 (UC14 table)
    # Find Table 21
    table_21 = doc.tables[21]._element
    elements_to_insert = [
        h2._p,
        p_intro._p,
        tbl._tbl,
        p_cap._p,
        h3._p,
        p_desc._p,
        *bullet_elements,
        p_sum._p
    ]

    curr = table_21
    for elem in elements_to_insert:
        curr.addnext(elem)
        curr = elem

    doc.save(target_path)
    print("SUCCESS: Missing entities section inserted cleanly into:", target_path)

if __name__ == "__main__":
    p1 = r"C:\Net108Khai\Các Bài Lab\Lab1_NET108_AI_Native_Commerce.docx"
    p2 = r"C:\Net108Khai\Các Bài Lab\Lab1_NET108_AINativeCommerce.docx"
    insert_missing_section(p1)
    try:
        insert_missing_section(p2)
    except Exception as e:
        print("Notice for p2:", e)

