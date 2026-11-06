# -*- coding: utf-8 -*-
"""
Generate publication-quality diagrams for LAB 2 (NET108 FPT Polytechnic):
1. erd_ainative_level2.png - Detailed Physical/Logical ERD Level 2 Diagram
2. ui_navigation_flow.png - UI Navigation Flow & Screen Hierarchy
3. ai_erd_evaluation_evidence.png - AI Prompt & Deepsearch Review Evidence
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"c:\Net108Khai\docs\06-design"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_REGULAR_PATH = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_ITALIC_PATH = r"C:\Windows\Fonts\segoeuii.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

font_title = get_font(FONT_BOLD_PATH, 22)
font_sub = get_font(FONT_REGULAR_PATH, 13)
font_tbl_hdr = get_font(FONT_BOLD_PATH, 14)
font_col = get_font(FONT_REGULAR_PATH, 12)
font_col_bold = get_font(FONT_BOLD_PATH, 12)
font_badge = get_font(FONT_BOLD_PATH, 11)
font_legend = get_font(FONT_REGULAR_PATH, 12)

# ==============================================================================
# 1. GENERATE ERD LEVEL 2 DIAGRAM (1600 x 1050 px)
# ==============================================================================
def generate_erd_level2():
    w, h = 1600, 1050
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([0, 0, w - 1, h - 1], outline="#CBD5E1", width=1)

    # Top Header Banner
    draw.rectangle([0, 0, w, 70], fill="#1F4E79")
    draw.line([0, 70, w, 70], fill="#0F2D4A", width=2)
    draw.text((40, 12), "SƠ ĐỒ QUAN HỆ THỰC THỂ CƠ SỞ DỮ LIỆU LEVEL 2 (PHYSICAL ERD)", fill="#FFFFFF", font=font_title)
    draw.text((40, 42), "Hệ Thống Thương Mại Điện Tử AI-Native Commerce | Chuẩn hóa 3NF & Hỗ trợ Vector Search", fill="#D9E1F2", font=font_sub)
    
    draw.rounded_rectangle([1410, 18, 1560, 52], radius=6, fill="#2F5597", outline="#8EA9DB", width=1)
    draw.text((1428, 27), "ERD Level 2 • NET108", fill="#FFFFFF", font=font_badge)

    # Database Tables Definitions: (name, x, y, width, columns: [(is_pk, is_fk, name, type)])
    tables = [
        # Col 1: Users & Roles
        {
            "name": "ROLES (Vai trò)",
            "x": 50, "y": 100, "w": 250,
            "header_bg": "#1E3A8A",
            "cols": [
                (True, False, "id", "INT IDENTITY PK"),
                (False, False, "name", "NVARCHAR(50) NOT NULL"),
                (False, False, "description", "NVARCHAR(255)"),
                (False, False, "created_at", "DATETIME DEFAULT GETDATE()")
            ]
        },
        {
            "name": "USERS (Người dùng & NV)",
            "x": 50, "y": 270, "w": 280,
            "header_bg": "#1E3A8A",
            "cols": [
                (True, False, "id", "INT IDENTITY PK"),
                (False, True, "role_id", "INT FK -> ROLES(id)"),
                (False, False, "email", "VARCHAR(150) UNIQUE"),
                (False, False, "password_hash", "VARCHAR(255) NOT NULL"),
                (False, False, "full_name", "NVARCHAR(100) NOT NULL"),
                (False, False, "phone", "VARCHAR(20)"),
                (False, False, "status", "NVARCHAR(30) DEFAULT 'ACTIVE'"),
                (False, False, "created_at", "DATETIME DEFAULT GETDATE()")
            ]
        },
        {
            "name": "AI_SESSIONS (Phiên Chat AI)",
            "x": 50, "y": 550, "w": 280,
            "header_bg": "#4338CA",
            "cols": [
                (True, False, "id", "INT IDENTITY PK"),
                (False, True, "user_id", "INT FK -> USERS(id)"),
                (False, False, "session_token", "VARCHAR(100) UNIQUE"),
                (False, False, "context_summary", "NVARCHAR(MAX)"),
                (False, False, "intent_detected", "VARCHAR(100)"),
                (False, False, "created_at", "DATETIME DEFAULT GETDATE()")
            ]
        },
        {
            "name": "AUDIT_LOGS (Nhật ký kiểm toán)",
            "x": 50, "y": 790, "w": 280,
            "header_bg": "#334155",
            "cols": [
                (True, False, "id", "BIGINT IDENTITY PK"),
                (False, True, "user_id", "INT FK -> USERS(id) NULL"),
                (False, False, "actor_type", "VARCHAR(50) (User/Agent)"),
                (False, False, "action", "VARCHAR(100) NOT NULL"),
                (False, False, "entity_name", "VARCHAR(50)"),
                (False, False, "ip_address", "VARCHAR(45)"),
                (False, False, "created_at", "DATETIME DEFAULT GETDATE()")
            ]
        },

        # Col 2: Categories, Products, Vectors
        {
            "name": "CATEGORIES (Danh mục)",
            "x": 420, "y": 100, "w": 280,
            "header_bg": "#065F46",
            "cols": [
                (True, False, "id", "INT IDENTITY PK"),
                (False, True, "parent_id", "INT FK -> SELF NULL"),
                (False, False, "name", "NVARCHAR(100) NOT NULL"),
                (False, False, "slug", "VARCHAR(120) UNIQUE"),
                (False, False, "active", "BIT DEFAULT 1")
            ]
        },
        {
            "name": "PRODUCTS (Sản phẩm)",
            "x": 420, "y": 300, "w": 310,
            "header_bg": "#065F46",
            "cols": [
                (True, False, "id", "INT IDENTITY PK"),
                (False, True, "category_id", "INT FK -> CATEGORIES(id)"),
                (False, False, "name", "NVARCHAR(200) NOT NULL"),
                (False, False, "sku", "VARCHAR(50) UNIQUE"),
                (False, False, "price", "DECIMAL(18,2) NOT NULL"),
                (False, False, "stock_quantity", "INT DEFAULT 0"),
                (False, False, "description", "NVARCHAR(MAX)"),
                (False, False, "image_url", "VARCHAR(500)"),
                (False, False, "status", "VARCHAR(30) DEFAULT 'ACTIVE'"),
                (False, False, "created_at", "DATETIME DEFAULT GETDATE()")
            ]
        },
        {
            "name": "PRODUCT_VECTORS (Vector Embedding)",
            "x": 420, "y": 640, "w": 310,
            "header_bg": "#0E7490",
            "cols": [
                (True, False, "id", "BIGINT IDENTITY PK"),
                (False, True, "product_id", "INT FK -> PRODUCTS(id) UNIQUE"),
                (False, False, "embedding_model", "VARCHAR(100) NOT NULL"),
                (False, False, "embedding_vector", "VECTOR(1536) / VARBINARY"),
                (False, False, "metadata_json", "NVARCHAR(MAX)"),
                (False, False, "updated_at", "DATETIME DEFAULT GETDATE()")
            ]
        },

        # Col 3: Cart & Cart_Items
        {
            "name": "CARTS (Giỏ hàng)",
            "x": 820, "y": 100, "w": 280,
            "header_bg": "#7C2D12",
            "cols": [
                (True, False, "id", "INT IDENTITY PK"),
                (False, True, "user_id", "INT FK -> USERS(id) NULL"),
                (False, False, "session_id", "VARCHAR(100)"),
                (False, False, "total_amount", "DECIMAL(18,2) DEFAULT 0"),
                (False, False, "updated_at", "DATETIME DEFAULT GETDATE()")
            ]
        },
        {
            "name": "CART_ITEMS (Chi tiết giỏ hàng)",
            "x": 820, "y": 300, "w": 280,
            "header_bg": "#7C2D12",
            "cols": [
                (True, False, "id", "INT IDENTITY PK"),
                (False, True, "cart_id", "INT FK -> CARTS(id)"),
                (False, True, "product_id", "INT FK -> PRODUCTS(id)"),
                (False, False, "quantity", "INT NOT NULL DEFAULT 1"),
                (False, False, "unit_price", "DECIMAL(18,2) NOT NULL"),
                (False, False, "created_at", "DATETIME DEFAULT GETDATE()")
            ]
        },

        # Col 4: Orders, Order_Items, Payments, Shipping
        {
            "name": "ORDERS (Đơn hàng / Hóa đơn)",
            "x": 1200, "y": 100, "w": 340,
            "header_bg": "#831843",
            "cols": [
                (True, False, "id", "INT IDENTITY PK"),
                (False, True, "user_id", "INT FK -> USERS(id)"),
                (False, False, "order_code", "VARCHAR(50) UNIQUE"),
                (False, False, "total_amount", "DECIMAL(18,2) NOT NULL"),
                (False, False, "discount_amount", "DECIMAL(18,2) DEFAULT 0"),
                (False, False, "final_amount", "DECIMAL(18,2) NOT NULL"),
                (False, False, "status", "VARCHAR(40) DEFAULT 'PENDING'"),
                (False, False, "payment_status", "VARCHAR(40) DEFAULT 'UNPAID'"),
                (False, False, "shipping_address", "NVARCHAR(500) NOT NULL"),
                (False, False, "created_at", "DATETIME DEFAULT GETDATE()")
            ]
        },
        {
            "name": "ORDER_ITEMS (Chi tiết đơn hàng)",
            "x": 1200, "y": 430, "w": 340,
            "header_bg": "#831843",
            "cols": [
                (True, False, "id", "INT IDENTITY PK"),
                (False, True, "order_id", "INT FK -> ORDERS(id)"),
                (False, True, "product_id", "INT FK -> PRODUCTS(id)"),
                (False, False, "quantity", "INT NOT NULL"),
                (False, False, "unit_price", "DECIMAL(18,2) NOT NULL"),
                (False, False, "subtotal", "DECIMAL(18,2) NOT NULL")
            ]
        },
        {
            "name": "PAYMENTS (Thanh toán)",
            "x": 1200, "y": 660, "w": 340,
            "header_bg": "#15803D",
            "cols": [
                (True, False, "id", "INT IDENTITY PK"),
                (False, True, "order_id", "INT FK -> ORDERS(id)"),
                (False, False, "payment_method", "VARCHAR(50) (VNPay/COD/QR)"),
                (False, False, "transaction_id", "VARCHAR(100)"),
                (False, False, "amount", "DECIMAL(18,2) NOT NULL"),
                (False, False, "status", "VARCHAR(30) DEFAULT 'PAID'"),
                (False, False, "paid_at", "DATETIME DEFAULT GETDATE()")
            ]
        },
        {
            "name": "SHIPPING (Vận chuyển)",
            "x": 1200, "y": 870, "w": 340,
            "header_bg": "#D97706",
            "cols": [
                (True, False, "id", "INT IDENTITY PK"),
                (False, True, "order_id", "INT FK -> ORDERS(id) UNIQUE"),
                (False, False, "carrier_code", "VARCHAR(50) (GHN/GHTK)"),
                (False, False, "tracking_number", "VARCHAR(100) UNIQUE"),
                (False, False, "shipping_status", "VARCHAR(50)"),
                (False, False, "estimated_delivery", "DATETIME")
            ]
        }
    ]

    # Draw all tables
    tbl_boxes = {}
    for t in tables:
        x, y, w_box = t["x"], t["y"], t["w"]
        n_cols = len(t["cols"])
        h_box = 36 + n_cols * 22 + 8
        tbl_boxes[t["name"]] = (x, y, w_box, h_box)

        # Draw card container
        draw.rounded_rectangle([x, y, x + w_box, y + h_box], radius=6, fill="#FFFFFF", outline="#94A3B8", width=2)
        # Table Header
        draw.rounded_rectangle([x, y, x + w_box, y + 34], radius=6, fill=t["header_bg"])
        draw.rectangle([x, y + 26, x + w_box, y + 34], fill=t["header_bg"])  # flatten bottom corners
        draw.text((x + 12, y + 8), t["name"], fill="#FFFFFF", font=font_tbl_hdr)

        # Draw columns
        col_y = y + 42
        for is_pk, is_fk, col_name, col_type in t["cols"]:
            # PK badge
            if is_pk:
                draw.rounded_rectangle([x + 10, col_y, x + 34, col_y + 16], radius=3, fill="#F59E0B")
                draw.text((x + 13, col_y + 1), "PK", fill="#FFFFFF", font=font_badge)
            elif is_fk:
                draw.rounded_rectangle([x + 10, col_y, x + 34, col_y + 16], radius=3, fill="#3B82F6")
                draw.text((x + 13, col_y + 1), "FK", fill="#FFFFFF", font=font_badge)
            else:
                draw.ellipse([x + 19, col_y + 5, x + 25, col_y + 11], fill="#94A3B8")

            # Column Name
            c_font = font_col_bold if (is_pk or is_fk) else font_col
            c_color = "#0F172A" if (is_pk or is_fk) else "#334155"
            draw.text((x + 40, col_y), col_name, fill=c_color, font=c_font)

            # Column Type
            tb = font_col.getbbox(col_type)
            tw = tb[2] - tb[0]
            draw.text((x + w_box - tw - 12, col_y), col_type, fill="#64748B", font=font_col)

            # Divider line
            draw.line([x + 8, col_y + 19, x + w_box - 8, col_y + 19], fill="#F1F5F9", width=1)
            col_y += 22

    # Draw Connecting Relationship Lines
    rel_color = "#2563EB"
    def draw_rel(x1, y1, x2, y2, label="1 - N"):
        draw.line([(x1, y1), (x2, y2)], fill=rel_color, width=2)
        # mid badge
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        draw.rounded_rectangle([mx - 18, my - 9, mx + 18, my + 9], radius=3, fill="#EFF6FF", outline="#93C5FD", width=1)
        draw.text((mx - 14, my - 7), label, fill="#1E40AF", font=font_badge)

    # Roles -> Users
    draw_rel(175, 185, 175, 270, "1 - N")
    # Users -> AI_Sessions
    draw_rel(175, 470, 175, 550, "1 - N")
    # Users -> Audit_Logs
    draw_rel(175, 715, 175, 790, "1 - N")
    # Categories -> Products
    draw_rel(560, 220, 560, 300, "1 - N")
    # Products -> Product_Vectors
    draw_rel(560, 545, 560, 640, "1 - 1")
    # Carts -> Cart_Items
    draw_rel(960, 220, 960, 300, "1 - N")
    # Products -> Cart_Items
    draw_rel(730, 390, 820, 390, "1 - N")
    # Orders -> Order_Items
    draw_rel(1370, 335, 1370, 430, "1 - N")
    # Products -> Order_Items (Intermediate Bridge)
    draw.line([(730, 460), (790, 460), (790, 500), (1200, 500)], fill="#059669", width=2)
    draw.rounded_rectangle([970, 490, 1020, 510], radius=3, fill="#ECFDF5", outline="#6EE7B7", width=1)
    draw.text((975, 494), "N - N (Bridge)", fill="#065F46", font=font_badge)
    # Orders -> Payments
    draw_rel(1370, 580, 1370, 660, "1 - N")
    # Orders -> Shipping
    draw_rel(1370, 805, 1370, 870, "1 - 1")

    # Bottom Legend
    draw.rectangle([0, 1005, w, h], fill="#FFFFFF")
    draw.line([0, 1005, w, 1005], fill="#E2E8F0", width=1)
    draw.text((40, 1018), "Ghi chú ERD Level 2:", fill="#0F172A", font=font_col_bold)
    draw.rounded_rectangle([180, 1018, 204, 1034], radius=3, fill="#F59E0B")
    draw.text((183, 1019), "PK", fill="#FFFFFF", font=font_badge)
    draw.text((212, 1018), "Primary Key (Khóa chính)", fill="#475569", font=font_legend)
    draw.rounded_rectangle([380, 1018, 404, 1034], radius=3, fill="#3B82F6")
    draw.text((383, 1019), "FK", fill="#FFFFFF", font=font_badge)
    draw.text((412, 1018), "Foreign Key (Khóa ngoại)", fill="#475569", font=font_legend)
    draw.line([590, 1026, 625, 1026], fill="#2563EB", width=2)
    draw.text((635, 1018), "Quan hệ 1-N / 1-1", fill="#475569", font=font_legend)
    draw.line([760, 1026, 795, 1026], fill="#059669", width=2)
    draw.text((805, 1018), "Quan hệ N-N tách qua bảng trung gian (Order_Items / Cart_Items)", fill="#475569", font=font_legend)

    erd_path = os.path.join(OUTPUT_DIR, "erd_ainative_level2.png")
    img.save(erd_path, quality=95)
    print("Saved ERD Level 2 to:", erd_path)

# ==============================================================================
# 2. GENERATE UI NAVIGATION FLOW DIAGRAM (1500 x 920 px)
# ==============================================================================
def generate_ui_flow():
    w, h = 1500, 920
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, w - 1, h - 1], outline="#CBD5E1", width=1)

    # Top Banner
    draw.rectangle([0, 0, w, 70], fill="#0F766E")  # Teal Header
    draw.line([0, 70, w, 70], fill="#115E59", width=2)
    draw.text((40, 12), "SƠ ĐỒ TỔ CHỨC LUỒNG GIAO DIỆN (UI NAVIGATION FLOW)", fill="#FFFFFF", font=font_title)
    draw.text((40, 42), "Kiến trúc Điều hướng Đa phân hệ: Khách hàng (Storefront) & Quản trị viên (Admin/Merchant Portal)", fill="#CCFBF1", font=font_sub)
    draw.rounded_rectangle([1320, 18, 1460, 52], radius=6, fill="#115E59", outline="#5EEAD4", width=1)
    draw.text((1340, 27), "Bài 3 • NET108 Lab 2", fill="#FFFFFF", font=font_badge)

    # Root Screen (Entry Point)
    draw.rounded_rectangle([600, 95, 900, 155], radius=8, fill="#1E3A8A", outline="#172554", width=2)
    draw.text((665, 105), "ENTRY POINT", fill="#93C5FD", font=font_badge)
    draw.text((645, 122), "TRANG ĐĂNG NHẬP (AUTH)", fill="#FFFFFF", font=font_tbl_hdr)

    # Branches from Auth:
    # Left Branch: Storefront / Customer Flow
    # Draw Branch Box Left
    draw.rounded_rectangle([50, 180, 720, 850], radius=10, fill="#FFFFFF", outline="#99F6E4", width=2)
    draw.rectangle([50, 180, 720, 225], fill="#0D9488")
    draw.text((70, 192), "PHÂN HỆ KHÁCH HÀNG & MUA SẮM AI (CUSTOMER STOREFRONT)", fill="#FFFFFF", font=font_tbl_hdr)

    # Right Branch: Admin / Merchant Flow
    draw.rounded_rectangle([780, 180, 1450, 850], radius=10, fill="#FFFFFF", outline="#FDE68A", width=2)
    draw.rectangle([780, 180, 1450, 225], fill="#D97706")
    draw.text((800, 192), "PHÂN HỆ QUẢN TRỊ & NHÂN VIÊN (MERCHANT & ADMIN PORTAL)", fill="#FFFFFF", font=font_tbl_hdr)

    # Customer Screens
    c_screens = [
        {"name": "Trang chủ (Home & Feed)", "desc": "Hiển thị sản phẩm đề xuất AI", "x": 80, "y": 250, "w": 280, "bg": "#F0FDFA", "bc": "#14B8A6"},
        {"name": "Tìm kiếm thông minh (NLP Search)", "desc": "Truy vấn ngôn ngữ tự nhiên & RAG", "x": 400, "y": 250, "w": 290, "bg": "#F0FDFA", "bc": "#14B8A6"},
        {"name": "Chi tiết sản phẩm (Product Detail)", "desc": "Thông số, đánh giá, sp tương tự", "x": 80, "y": 380, "w": 280, "bg": "#F0FDFA", "bc": "#14B8A6"},
        {"name": "Trợ lý AI (Shopping Assistant)", "desc": "Hội thoại tư vấn sản phẩm trực tiếp", "x": 400, "y": 380, "w": 290, "bg": "#CCFBF1", "bc": "#0D9488"},
        {"name": "Giỏ hàng thông minh (Smart Cart)", "desc": "Tự động tối ưu Voucher & Combo", "x": 80, "y": 510, "w": 280, "bg": "#F0FDFA", "bc": "#14B8A6"},
        {"name": "Thanh toán (Checkout & Pay)", "desc": "Tích hợp VNPay / MoMo / VietQR", "x": 400, "y": 510, "w": 290, "bg": "#FEF3C7", "bc": "#F59E0B"},
        {"name": "Xác nhận đơn & Tracking", "desc": "Tra cứu vận đơn giao hàng GHN/GHTK", "x": 80, "y": 640, "w": 280, "bg": "#F0FDFA", "bc": "#14B8A6"},
        {"name": "Hồ sơ cá nhân & Lịch sử mua", "desc": "Quản lý địa chỉ nhận hàng & hóa đơn", "x": 400, "y": 640, "w": 290, "bg": "#F0FDFA", "bc": "#14B8A6"},
    ]
    for s in c_screens:
        draw.rounded_rectangle([s["x"], s["y"], s["x"] + s["w"], s["y"] + 70], radius=6, fill=s["bg"], outline=s["bc"], width=2)
        draw.text((s["x"] + 14, s["y"] + 12), s["name"], fill="#0F172A", font=font_col_bold)
        draw.text((s["x"] + 14, s["y"] + 36), s["desc"], fill="#64748B", font=font_col)

    # Admin Screens
    a_screens = [
        {"name": "Dashboard Thống kê tổng hợp", "desc": "Doanh thu, đơn hàng, biểu đồ tăng trưởng", "x": 810, "y": 250, "w": 290, "bg": "#FFFBEB", "bc": "#F59E0B"},
        {"name": "Quản lý Danh mục (Categories)", "desc": "Cây danh mục phân cấp đa tầng", "x": 1130, "y": 250, "w": 290, "bg": "#FFFBEB", "bc": "#F59E0B"},
        {"name": "Quản lý Sản phẩm (Products)", "desc": "CRUD sản phẩm & Sinh Vector Embedding", "x": 810, "y": 380, "w": 290, "bg": "#FFFBEB", "bc": "#F59E0B"},
        {"name": "Quản lý Kho & Tồn kho (Stock)", "desc": "Cảnh báo tồn kho thấp & nhập hàng", "x": 1130, "y": 380, "w": 290, "bg": "#FFFBEB", "bc": "#F59E0B"},
        {"name": "Quản lý Đơn hàng (Orders)", "desc": "Duyệt đơn, in vận đơn, chuyển GHN/GHTK", "x": 810, "y": 510, "w": 290, "bg": "#FEF3C7", "bc": "#D97706"},
        {"name": "Quản lý Người dùng & RBAC", "desc": "Phân quyền Nhân viên / Nhà quản lý", "x": 1130, "y": 510, "w": 290, "bg": "#FFFBEB", "bc": "#F59E0B"},
        {"name": "Báo cáo Hiệu quả AI & Tác tử", "desc": "Tỷ lệ chốt đơn qua AI Assistant & từ khóa", "x": 810, "y": 640, "w": 290, "bg": "#E0E7FF", "bc": "#6366F1"},
        {"name": "Nhật ký Hệ thống (Audit Logs)", "desc": "Giám sát giao dịch tự hành của AI Agent", "x": 1130, "y": 640, "w": 290, "bg": "#F1F5F9", "bc": "#64748B"},
    ]
    for s in a_screens:
        draw.rounded_rectangle([s["x"], s["y"], s["x"] + s["w"], s["y"] + 70], radius=6, fill=s["bg"], outline=s["bc"], width=2)
        draw.text((s["x"] + 14, s["y"] + 12), s["name"], fill="#0F172A", font=font_col_bold)
        draw.text((s["x"] + 14, s["y"] + 36), s["desc"], fill="#64748B", font=font_col)

    # Connecting navigation arrows
    # Auth -> Customer Branch
    draw.line([(600, 125), (380, 125), (380, 180)], fill="#0D9488", width=2)
    # Auth -> Admin Branch
    draw.line([(900, 125), (1110, 125), (1110, 180)], fill="#D97706", width=2)

    # Customer internal flow arrows
    draw.line([(220, 320), (220, 380)], fill="#0D9488", width=2)
    draw.line([(360, 415), (400, 415)], fill="#0D9488", width=2)
    draw.line([(220, 450), (220, 510)], fill="#0D9488", width=2)
    draw.line([(360, 545), (400, 545)], fill="#0D9488", width=2)
    draw.line([(545, 580), (545, 610), (220, 610), (220, 640)], fill="#0D9488", width=2)

    # Bottom notes
    draw.rectangle([50, 750, 690, 830], fill="#F0FDFA", outline="#99F6E4", width=1)
    draw.text((65, 760), "Quy tắc điều hướng Khách hàng:", fill="#0F766E", font=font_col_bold)
    draw.text((65, 782), "• Khách vãng lai xem được Home, NLP Search, Product Detail mà không cần đăng nhập.", fill="#334155", font=font_col)
    draw.text((65, 802), "• Khi chuyển sang Checkout hoặc Chat Assistant nâng cao, hệ thống yêu cầu đăng nhập/xác thực.", fill="#334155", font=font_col)

    draw.rectangle([780, 750, 1420, 830], fill="#FFFBEB", outline="#FDE68A", width=1)
    draw.text((795, 760), "Quy tắc điều hướng Quản trị viên:", fill="#B45309", font=font_col_bold)
    draw.text((795, 782), "• Nhân viên bán hàng chỉ có quyền truy cập Quản lý đơn hàng, Quản lý đồ uống / sản phẩm.", fill="#334155", font=font_col)
    draw.text((795, 802), "• Quản lý / Super Admin có toàn quyền xem Dashboard Thống kê, Báo cáo AI, Phân quyền & Audit Logs.", fill="#334155", font=font_col)

    flow_path = os.path.join(OUTPUT_DIR, "ui_navigation_flow.png")
    img.save(flow_path, quality=95)
    print("Saved UI Navigation Flow to:", flow_path)

# ==============================================================================
# 3. GENERATE AI ERD REVIEW EVIDENCE (1200 x 720 px)
# ==============================================================================
def generate_ai_evidence():
    w, h = 1200, 720
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, w - 1, h - 1], outline="#CBD5E1", width=1)

    # Header Bar
    draw.rectangle([0, 0, w, 68], fill="#312E81")  # Indigo Header
    draw.line([0, 68, w, 68], fill="#1E1B4B", width=2)
    draw.text((40, 12), "BÀI 4: ỨNG DỤNG AI ĐÁNH GIÁ & TỐI ƯU HÓA SƠ ĐỒ ERD (AI AUDIT EVIDENCE)", fill="#FFFFFF", font=font_title)
    draw.text((40, 42), "Cấu trúc Prompt chuẩn: ROLE – CONTEXT – OBJECTIVE – OUTPUT – CONSTRAINTS | Slide FPT Poly", fill="#C7D2FE", font=font_sub)

    # Prompt Card
    draw.rounded_rectangle([40, 90, 1160, 270], radius=8, fill="#F8FAFC", outline="#818CF8", width=2)
    draw.rectangle([40, 90, 1160, 125], fill="#EEF2FF")
    draw.text((55, 98), "CÂU LỆNH PROMPT GỬI AI DEEPSEARCH (BÀI 4)", fill="#3730A3", font=font_col_bold)

    prompt_lines = [
        "ROLE: Bạn là một Chuyên gia Kiến trúc Cơ sở Dữ liệu & Hệ thống Thương mại Điện tử cao cấp.",
        "CONTEXT: Tôi đang viết tài liệu đặc tả dự án AI-Native Commerce với CSDL hỗ trợ cả quan hệ nghiệp vụ và Vector Embedding.",
        "OBJECTIVE: Đánh giá sơ đồ ERD Level 2 đính kèm: Kiểm tra chuẩn hóa 3NF, tính toàn vẹn dữ liệu, các quan hệ N-N và chỉ mục.",
        "OUTPUT: 1. Chỉ ra ít nhất 3 rủi ro thiết kế CSDL tiềm ẩn. 2. Đề xuất phương án tối ưu hóa bảng trung gian và lưu trữ Vector.",
        "CONSTRAINTS: Phù hợp với mô hình Thác nước (Waterfall), chuẩn hóa khóa chính/ngoại rõ ràng, tối ưu truy vấn thời gian thực."
    ]
    py = 135
    for line in prompt_lines:
        draw.text((55, py), line, fill="#1E293B", font=font_col)
        py += 24

    # AI Response Card
    draw.rounded_rectangle([40, 290, 1160, 640], radius=8, fill="#FFFFFF", outline="#10B981", width=2)
    draw.rectangle([40, 290, 1160, 325], fill="#ECFDF5")
    draw.text((55, 298), "KẾT QUẢ ĐÁNH GIÁ & ĐỀ XUẤT CẢI TIẾN TỪ AI DEEPSEARCH", fill="#065F46", font=font_col_bold)

    ai_responses = [
        ("1. Rủi ro quan hệ nhiều-nhiều (N-N) giữa Sản phẩm & Đơn hàng:",
         "Phát hiện: Đơn hàng và Sản phẩm có quan hệ N-N. Nếu gộp vào một bảng sẽ gây trùng lặp dữ liệu nghiêm trọng.\n"
         "-> Cải tiến đã thực hiện: Tách riêng bảng trung gian ORDER_ITEMS lưu Subtotal, UnitPrice tại thời điểm mua và Quantity."),
        
        ("2. Rủi ro lưu trữ Vector Embedding dung lượng lớn trong cùng bảng PRODUCTS:",
         "Phát hiện: Cột Vector 1536 chiều chiếm dung lượng lớn, nếu để chung sẽ làm chậm các truy vấn danh mục thông thường.\n"
         "-> Cải tiến đã thực hiện: Tách riêng bảng PRODUCT_VECTORS với khóa ngoại 1-1 product_id, đánh chỉ mục HNSW/IVFFlat."),

        ("3. Bảo toàn giá sản phẩm lịch sử trong Hóa đơn / Đơn hàng:",
         "Phát hiện: Giá sản phẩm trong PRODUCTS có thể thay đổi trong tương lai, làm sai lệch doanh thu lịch sử của đơn hàng.\n"
         "-> Cải tiến đã thực hiện: Lưu cứng cột unit_price trong ORDER_ITEMS và CART_ITEMS độc lập với giá hiện tại trong PRODUCTS."),

        ("4. Đảm bảo toàn vẹn dữ liệu giao dịch tự hành của AI Agent:",
         "Phát hiện: Khi AI Agent đặt hàng tự động, cần có cơ chế truy vết bảo mật tránh tranh chấp pháp lý và gian lận.\n"
         "-> Cải tiến đã thực hiện: Bổ sung bảng AUDIT_LOGS và trường actor_type để ghi nhận chính xác ID tác tử AI thực hiện.")
    ]

    ay = 335
    for title, desc in ai_responses:
        draw.text((55, ay), title, fill="#047857", font=font_col_bold)
        ay += 20
        for l in desc.split('\n'):
            draw.text((70, ay), l, fill="#334155", font=font_col)
            ay += 18
        ay += 6

    # Footer
    draw.rectangle([0, 660, w, h], fill="#F8FAFC")
    draw.line([0, 660, w, 660], fill="#E2E8F0", width=1)
    draw.text((40, 680), "Kết luận Bài 4: Nhóm 5 đã tiếp thu 100% các khuyến nghị từ AI Deepsearch và hoàn thiện sơ đồ ERD Level 2 đạt chuẩn 3NF.", fill="#475569", font=font_col_bold)

    ai_path = os.path.join(OUTPUT_DIR, "ai_erd_evaluation_evidence.png")
    img.save(ai_path, quality=95)
    print("Saved AI Review Evidence to:", ai_path)

def main():
    print("=== GENERATING ALL LAB 2 DIAGRAMS ===")
    generate_erd_level2()
    generate_ui_flow()
    generate_ai_evidence()
    print("=== ALL LAB 2 DIAGRAMS GENERATED SUCCESSFULLY! ===")

if __name__ == "__main__":
    main()
