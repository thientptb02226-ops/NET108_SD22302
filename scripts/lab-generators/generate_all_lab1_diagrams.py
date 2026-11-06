# -*- coding: utf-8 -*-
"""
Script to generate all diagrams for Lab 1 NET108 AI-Native Commerce:
1. usecase_ainative_tongquat.png (28 Use Cases)
2. usecase_ainative_customer.png (14 Use Cases)
3. usecase_ainative_admin.png (10 Use Cases)
4. usecase_ainative_agent.png (8 Use Cases)
5. erd_ainative_conceptual.png (Conceptual ERD with 10 entities)
6. deploy_diagram.png (UML Deployment Diagram)
7. appmap_diagram.png (Application Sitemap & Hierarchy Map)
8. tech_stack_diagram.png (Architecture Tech Stack Model)
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

DESIGN_DIR = r"C:\Net108Khai\docs\06-design"
UC_DIR = os.path.join(DESIGN_DIR, "use-cases")
os.makedirs(UC_DIR, exist_ok=True)

def get_fonts():
    try:
        f_title = ImageFont.truetype("arialbd.ttf", 22)
        f_sub = ImageFont.truetype("arialbd.ttf", 16)
        f_box = ImageFont.truetype("arialbd.ttf", 14)
        f_actor = ImageFont.truetype("arialbd.ttf", 13)
        f_uc = ImageFont.truetype("arial.ttf", 12)
        f_uc_bold = ImageFont.truetype("arialbd.ttf", 12)
        f_stereo = ImageFont.truetype("ariali.ttf", 11)
        f_small = ImageFont.truetype("arial.ttf", 11)
    except Exception:
        f_title = f_sub = f_box = f_actor = f_uc = f_uc_bold = f_stereo = f_small = ImageFont.load_default()
    return f_title, f_sub, f_box, f_actor, f_uc, f_uc_bold, f_stereo, f_small

def draw_actor(draw, x, y, name, font, color=(31, 78, 121)):
    # Head
    draw.ellipse([x-20, y-58, x+20, y-18], outline=color, width=2, fill=(245, 248, 252))
    # Body
    draw.line([x, y-18, x, y+32], fill=color, width=2)
    # Arms
    draw.line([x-28, y-4, x+28, y-4], fill=color, width=2)
    # Legs
    draw.line([x, y+32, x-22, y+78], fill=color, width=2)
    draw.line([x, y+32, x+22, y+78], fill=color, width=2)
    # Label
    lines = name.split("\n")
    for i, l in enumerate(lines):
        bb = draw.textbbox((0, 0), l, font=font)
        w = bb[2] - bb[0]
        draw.text((x - w//2, y + 84 + i*16), l, fill=color, font=font)

def draw_ellipse_uc(draw, cx, cy, rx, ry, name, font, border_color=(46, 117, 182), fill_color=(238, 245, 253), text_color=(20, 30, 50)):
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=border_color, width=2, fill=fill_color)
    lines = name.split("\n")
    total_h = len(lines) * 15
    start_y = cy - total_h // 2
    for i, l in enumerate(lines):
        bb = draw.textbbox((0, 0), l, font=font)
        w = bb[2] - bb[0]
        draw.text((cx - w//2, start_y + i*15), l, fill=text_color, font=font)

def draw_dashed_line(draw, x1, y1, x2, y2, fill=(120, 130, 140), width=1, dash=6, gap=4):
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy)
    if dist == 0: return
    ux, uy = dx/dist, dy/dist
    curr = 0
    drawing = True
    while curr < dist:
        seg = min(dash if drawing else gap, dist - curr)
        if drawing:
            draw.line([x1 + ux*curr, y1 + uy*curr, x1 + ux*(curr+seg), y1 + uy*(curr+seg)], fill=fill, width=width)
        curr += seg
        drawing = not drawing

def draw_arrow(draw, x1, y1, x2, y2, fill=(100, 110, 125), width=1, is_dashed=True, label=None, font_label=None, label_color=None):
    if is_dashed:
        draw_dashed_line(draw, x1, y1, x2, y2, fill=fill, width=width)
    else:
        draw.line([x1, y1, x2, y2], fill=fill, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    alen = 10
    aangle = math.radians(25)
    ax1 = x2 - alen * math.cos(angle - aangle)
    ay1 = y2 - alen * math.sin(angle - aangle)
    ax2 = x2 - alen * math.cos(angle + aangle)
    ay2 = y2 - alen * math.sin(angle + aangle)
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=fill)
    if label and font_label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 - 9
        bb = draw.textbbox((0, 0), label, font=font_label)
        w = bb[2] - bb[0]
        h = bb[3] - bb[1]
        draw.rectangle([mx - w//2 - 2, my - 1, mx + w//2 + 2, my + h + 1], fill=(255, 255, 255))
        c = label_color or ((160, 40, 40) if "extend" in label else (30, 120, 30))
        draw.text((mx - w//2, my), label, fill=c, font=font_label)

# ==============================================================================
# 1. SƠ ĐỒ USE CASE TỔNG QUÁT 28 USE CASES (1800 x 1350)
# ==============================================================================
def generate_general_usecase():
    w, h = 1800, 1380
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_actor, f_uc, f_uc_bold, f_stereo, f_small = get_fonts()

    # Title Banner
    title = "SƠ ĐỒ USE CASE TỔNG QUÁT HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ AI-NATIVE"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 20), title, fill=(31, 78, 121), font=f_title)

    sub = "Dự Án Mẫu .NET 1 (NET108) — Mô hình hóa 28 Ca Sử Dụng & 4 Nhóm Tác Nhân Cốt Lõi"
    bb_sub = draw.textbbox((0, 0), sub, font=f_sub)
    draw.text(((w - (bb_sub[2]-bb_sub[0]))//2, 54), sub, fill=(90, 105, 120), font=f_sub)

    # Boundary Box
    bx1, by1, bx2, by2 = 230, 95, 1570, 1340
    draw.rectangle([bx1, by1, bx2, by2], outline=(70, 80, 95), width=2)
    draw.text((bx1 + 20, by1 + 14), "Phạm vi Hệ thống AI-Native Commerce (System Boundary)", fill=(40, 50, 60), font=f_box)

    # Actors Positions
    pos_guest = (115, 280)
    pos_cust = (115, 840)
    pos_admin = (1685, 380)
    pos_agent = (1685, 960)

    draw_actor(draw, pos_guest[0], pos_guest[1], "Guest\n(Khách vãng lai)", f_actor, color=(180, 80, 20))
    draw_actor(draw, pos_cust[0], pos_cust[1], "Customer\n(Khách hàng)", f_actor, color=(31, 78, 121))
    draw_actor(draw, pos_admin[0], pos_admin[1], "Admin / Merchant\n(Quản trị & Nhà bán)", f_actor, color=(30, 126, 52))
    draw_actor(draw, pos_agent[0], pos_agent[1], "AI Agent Platform\n(Tác tử AI Tự hành)", f_actor, color=(111, 66, 193))

    # 4 Columns of Use Cases
    c1 = 410   # Guest & Customer Account
    c2 = 740   # Customer Shopping & AI
    c3 = 1070  # Admin & Merchant Management
    c4 = 1390  # AI Agent Platform & Operations

    ucs = {
        # Column 1: Guest & Account (5)
        "uc01": {"name": "UC01: Đăng ký tài khoản", "c": (c1, 170), "rx": 95, "ry": 26, "fill": (254, 243, 235), "border": (217, 119, 6)},
        "uc02": {"name": "UC02: Đăng nhập & JWT", "c": (c1, 280), "rx": 95, "ry": 26, "fill": (254, 243, 235), "border": (217, 119, 6)},
        "uc03": {"name": "UC03: Quên mật khẩu OTP", "c": (c1, 390), "rx": 98, "ry": 26, "fill": (254, 243, 235), "border": (217, 119, 6)},
        "uc04": {"name": "UC04: Tìm kiếm NLP / Hybrid", "c": (c1, 520), "rx": 100, "ry": 28, "fill": (238, 245, 253), "border": (46, 117, 182)},
        "uc05": {"name": "UC05: Xem so sánh sản phẩm", "c": (c1, 640), "rx": 100, "ry": 26, "fill": (238, 245, 253), "border": (46, 117, 182)},
        "uc06": {"name": "UC06: Quản lý hồ sơ & Địa chỉ", "c": (c1, 760), "rx": 100, "ry": 26, "fill": (238, 245, 253), "border": (46, 117, 182)},
        "uc08": {"name": "UC08: Quản lý Wishlist", "c": (c1, 880), "rx": 95, "ry": 26, "fill": (238, 245, 253), "border": (46, 117, 182)},
        "uc13": {"name": "UC13: Đánh giá & AI Review", "c": (c1, 1000), "rx": 100, "ry": 26, "fill": (238, 245, 253), "border": (46, 117, 182)},
        "uc14": {"name": "UC14: Đổi trả / Hoàn tiền AI", "c": (c1, 1120), "rx": 100, "ry": 26, "fill": (238, 245, 253), "border": (46, 117, 182)},

        # Column 2: Shopping & Orders (5)
        "uc07": {"name": "UC07: Mua sắm với AI Assistant", "c": (c2, 330), "rx": 108, "ry": 30, "fill": (245, 238, 253), "border": (111, 66, 193)},
        "uc09": {"name": "UC09: Giỏ hàng thông minh", "c": (c2, 530), "rx": 102, "ry": 28, "fill": (238, 245, 253), "border": (46, 117, 182)},
        "uc10": {"name": "UC10: Đặt hàng & Áp Voucher", "c": (c2, 730), "rx": 105, "ry": 30, "fill": (238, 245, 253), "border": (46, 117, 182)},
        "uc11": {"name": "UC11: Thanh toán qua VNPay", "c": (c2, 930), "rx": 102, "ry": 28, "fill": (238, 245, 253), "border": (46, 117, 182)},
        "uc12": {"name": "UC12: Tra cứu & Theo dõi đơn", "c": (c2, 1120), "rx": 102, "ry": 28, "fill": (238, 245, 253), "border": (46, 117, 182)},

        # Column 3: Admin & Merchant (7)
        "uc15": {"name": "UC15: Quản lý danh mục & SP", "c": (c3, 200), "rx": 102, "ry": 28, "fill": (238, 250, 240), "border": (30, 126, 52)},
        "uc16": {"name": "UC16: Quản lý tồn kho & Cảnh báo", "c": (c3, 340), "rx": 106, "ry": 28, "fill": (238, 250, 240), "border": (30, 126, 52)},
        "uc17": {"name": "UC17: Quản lý đơn & Vận chuyển", "c": (c3, 480), "rx": 105, "ry": 28, "fill": (238, 250, 240), "border": (30, 126, 52)},
        "uc18": {"name": "UC18: Quản lý Voucher & Khuyến mãi", "c": (c3, 620), "rx": 108, "ry": 28, "fill": (238, 250, 240), "border": (30, 126, 52)},
        "uc19": {"name": "UC19: Quản lý User & Phân quyền", "c": (c3, 760), "rx": 106, "ry": 28, "fill": (238, 250, 240), "border": (30, 126, 52)},
        "uc20": {"name": "UC20: Cấu hình Prompt & Guardrails", "c": (c3, 900), "rx": 108, "ry": 28, "fill": (238, 250, 240), "border": (30, 126, 52)},
        "uc21": {"name": "UC21: Báo cáo thống kê doanh thu", "c": (c3, 1040), "rx": 106, "ry": 28, "fill": (238, 250, 240), "border": (30, 126, 52)},
        "uc22": {"name": "UC22: Đối soát & Hoa hồng Merchant", "c": (c3, 1180), "rx": 108, "ry": 28, "fill": (238, 250, 240), "border": (30, 126, 52)},

        # Column 4: AI Agent Platform (6)
        "uc23": {"name": "UC23: Gợi ý cá nhân hóa", "c": (c4, 250), "rx": 100, "ry": 26, "fill": (245, 238, 253), "border": (111, 66, 193)},
        "uc24": {"name": "UC24: Điều phối Multi-Agent", "c": (c4, 420), "rx": 105, "ry": 28, "fill": (245, 238, 253), "border": (111, 66, 193)},
        "uc25": {"name": "UC25: Truy xuất Vector RAG", "c": (c4, 590), "rx": 102, "ry": 28, "fill": (245, 238, 253), "border": (111, 66, 193)},
        "uc26": {"name": "UC26: Giao dịch qua tác tử ACP", "c": (c4, 760), "rx": 108, "ry": 30, "fill": (245, 238, 253), "border": (111, 66, 193)},
        "uc27": {"name": "UC27: Giám sát Guardrails & Hạn mức", "c": (c4, 940), "rx": 110, "ry": 28, "fill": (245, 238, 253), "border": (111, 66, 193)},
        "uc28": {"name": "UC28: Audit Log & Giám sát Token", "c": (c4, 1120), "rx": 108, "ry": 28, "fill": (245, 238, 253), "border": (111, 66, 193)},
    }

    # Draw Actor Association Lines
    lc_guest = (217, 119, 6)
    lc_cust = (46, 117, 182)
    lc_admin = (30, 126, 52)
    lc_agent = (111, 66, 193)

    # Guest lines
    for k in ["uc01", "uc02", "uc04"]:
        cx, cy = ucs[k]["c"]
        rx = ucs[k]["rx"]
        draw.line([pos_guest[0] + 35, pos_guest[1], cx - rx, cy], fill=lc_guest, width=1)

    # Customer lines
    for k in ["uc02", "uc04", "uc06", "uc07", "uc08", "uc09", "uc10", "uc12", "uc13"]:
        cx, cy = ucs[k]["c"]
        rx = ucs[k]["rx"]
        draw.line([pos_cust[0] + 35, pos_cust[1], cx - rx, cy], fill=lc_cust, width=1)

    # Admin lines
    for k in ["uc15", "uc16", "uc17", "uc18", "uc19", "uc20", "uc21", "uc22"]:
        cx, cy = ucs[k]["c"]
        rx = ucs[k]["rx"]
        draw.line([pos_admin[0] - 35, pos_admin[1], cx + rx, cy], fill=lc_admin, width=1)

    # Agent lines
    for k in ["uc04", "uc07", "uc23", "uc24", "uc25", "uc26", "uc27", "uc28"]:
        cx, cy = ucs[k]["c"]
        rx = ucs[k]["rx"]
        draw.line([pos_agent[0] - 35, pos_agent[1], cx + rx, cy], fill=lc_agent, width=1)

    # UML Relationships (<<include>> / <<extend>>)
    # uc02 extend uc03
    draw_arrow(draw, ucs["uc03"]["c"][0], ucs["uc03"]["c"][1] - ucs["uc03"]["ry"],
               ucs["uc02"]["c"][0], ucs["uc02"]["c"][1] + ucs["uc02"]["ry"],
               is_dashed=True, label="<<extend>>", font_label=f_stereo)

    # uc04 extend uc05
    draw_arrow(draw, ucs["uc05"]["c"][0], ucs["uc05"]["c"][1] - ucs["uc05"]["ry"],
               ucs["uc04"]["c"][0], ucs["uc04"]["c"][1] + ucs["uc04"]["ry"],
               is_dashed=True, label="<<extend>>", font_label=f_stereo)

    # uc07 include uc04
    draw_arrow(draw, ucs["uc07"]["c"][0] - ucs["uc07"]["rx"], ucs["uc07"]["c"][1] + 10,
               ucs["uc04"]["c"][0] + ucs["uc04"]["rx"], ucs["uc04"]["c"][1] - 10,
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    # uc10 include uc09
    draw_arrow(draw, ucs["uc10"]["c"][0], ucs["uc10"]["c"][1] - ucs["uc10"]["ry"],
               ucs["uc09"]["c"][0], ucs["uc09"]["c"][1] + ucs["uc09"]["ry"],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    # uc10 include uc11
    draw_arrow(draw, ucs["uc10"]["c"][0], ucs["uc10"]["c"][1] + ucs["uc10"]["ry"],
               ucs["uc11"]["c"][0], ucs["uc11"]["c"][1] - ucs["uc11"]["ry"],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    # uc18 extend uc10
    draw_arrow(draw, ucs["uc18"]["c"][0] - ucs["uc18"]["rx"], ucs["uc18"]["c"][1],
               ucs["uc10"]["c"][0] + ucs["uc10"]["rx"], ucs["uc10"]["c"][1],
               is_dashed=True, label="<<extend>>", font_label=f_stereo)

    # uc12 extend uc14
    draw_arrow(draw, ucs["uc14"]["c"][0] + ucs["uc14"]["rx"], ucs["uc14"]["c"][1],
               ucs["uc12"]["c"][0] - ucs["uc12"]["rx"], ucs["uc12"]["c"][1],
               is_dashed=True, label="<<extend>>", font_label=f_stereo)

    # uc26 include uc11 (ACP Agent includes Payment)
    draw_arrow(draw, ucs["uc26"]["c"][0] - ucs["uc26"]["rx"], ucs["uc26"]["c"][1] + 20,
               ucs["uc11"]["c"][0] + ucs["uc11"]["rx"], ucs["uc11"]["c"][1] - 10,
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    # uc26 include uc27
    draw_arrow(draw, ucs["uc26"]["c"][0], ucs["uc26"]["c"][1] + ucs["uc26"]["ry"],
               ucs["uc27"]["c"][0], ucs["uc27"]["c"][1] - ucs["uc27"]["ry"],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    # Render Ellipses
    for key, data in ucs.items():
        cx, cy = data["c"]
        rx, ry = data["rx"], data["ry"]
        draw_ellipse_uc(draw, cx, cy, rx, ry, data["name"], f_uc, border_color=data["border"], fill_color=data["fill"])

    out_file = os.path.join(UC_DIR, "usecase_ainative_tongquat.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print("Saved:", out_file)

# ==============================================================================
# 2. SƠ ĐỒ PHÂN HỆ KHÁCH HÀNG (14 USE CASES)
# ==============================================================================
def generate_customer_usecase():
    w, h = 1380, 980
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_actor, f_uc, f_uc_bold, f_stereo, f_small = get_fonts()

    title = "SƠ ĐỒ USE CASE PHÂN HỆ KHÁCH HÀNG (GUEST & CUSTOMER)"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 18), title, fill=(31, 78, 121), font=f_title)

    bx1, by1, bx2, by2 = 210, 65, 1170, 940
    draw.rectangle([bx1, by1, bx2, by2], outline=(70, 80, 95), width=2)
    draw.text((bx1 + 18, by1 + 12), "Phân hệ Khách hàng (Customer Boundary)", fill=(40, 50, 60), font=f_box)

    pos_guest = (105, 240)
    pos_cust = (105, 680)
    pos_ai = (1275, 480)

    draw_actor(draw, pos_guest[0], pos_guest[1], "Guest\n(Khách)", f_actor, color=(180, 80, 20))
    draw_actor(draw, pos_cust[0], pos_cust[1], "Customer\n(Khách hàng)", f_actor, color=(31, 78, 121))
    draw_actor(draw, pos_ai[0], pos_ai[1], "AI Shopping\nAssistant", f_actor, color=(111, 66, 193))

    c1 = 430
    c2 = 850

    ucs = {
        "uc01": {"name": "UC01: Đăng ký tài khoản", "c": (c1, 130), "rx": 98, "ry": 26},
        "uc02": {"name": "UC02: Đăng nhập & Xác thực", "c": (c1, 230), "rx": 98, "ry": 26},
        "uc03": {"name": "UC03: Quên mật khẩu qua Email", "c": (c2, 170), "rx": 105, "ry": 26},
        "uc04": {"name": "UC04: Tìm kiếm NLP / Hybrid", "c": (c1, 350), "rx": 102, "ry": 28},
        "uc05": {"name": "UC05: Xem so sánh sản phẩm", "c": (c2, 310), "rx": 102, "ry": 26},
        "uc06": {"name": "UC06: Quản lý hồ sơ & Địa chỉ", "c": (c1, 470), "rx": 105, "ry": 26},
        "uc07": {"name": "UC07: Mua sắm với AI Assistant", "c": (c2, 450), "rx": 110, "ry": 30},
        "uc08": {"name": "UC08: Quản lý Wishlist yêu thích", "c": (c1, 580), "rx": 105, "ry": 26},
        "uc09": {"name": "UC09: Quản lý giỏ hàng thông minh", "c": (c1, 690), "rx": 110, "ry": 28},
        "uc10": {"name": "UC10: Đặt hàng & Áp dụng Voucher", "c": (c2, 650), "rx": 112, "ry": 30},
        "uc11": {"name": "UC11: Thanh toán qua VNPay", "c": (c2, 790), "rx": 105, "ry": 28},
        "uc12": {"name": "UC12: Tra cứu đơn hàng Realtime", "c": (c1, 800), "rx": 108, "ry": 28},
        "uc13": {"name": "UC13: Đánh giá & AI tóm tắt", "c": (c1, 900), "rx": 105, "ry": 26},
        "uc14": {"name": "UC14: Yêu cầu đổi trả / hoàn tiền", "c": (c2, 900), "rx": 110, "ry": 26},
    }

    lc = (135, 145, 160)
    for k in ["uc01", "uc02", "uc04"]:
        cx, cy = ucs[k]["c"]
        draw.line([pos_guest[0]+30, pos_guest[1], cx - ucs[k]["rx"], cy], fill=lc, width=1)
    for k in ["uc02", "uc04", "uc06", "uc07", "uc08", "uc09", "uc10", "uc12", "uc13"]:
        cx, cy = ucs[k]["c"]
        draw.line([pos_cust[0]+30, pos_cust[1], cx - ucs[k]["rx"], cy], fill=lc, width=1)
    for k in ["uc04", "uc07", "uc05"]:
        cx, cy = ucs[k]["c"]
        draw.line([pos_ai[0]-30, pos_ai[1], cx + ucs[k]["rx"], cy], fill=(111, 66, 193), width=1)

    draw_arrow(draw, ucs["uc03"]["c"][0] - ucs["uc03"]["rx"], ucs["uc03"]["c"][1],
               ucs["uc02"]["c"][0] + ucs["uc02"]["rx"], ucs["uc02"]["c"][1],
               is_dashed=True, label="<<extend>>", font_label=f_stereo)
    draw_arrow(draw, ucs["uc05"]["c"][0] - ucs["uc05"]["rx"], ucs["uc05"]["c"][1],
               ucs["uc04"]["c"][0] + ucs["uc04"]["rx"], ucs["uc04"]["c"][1],
               is_dashed=True, label="<<extend>>", font_label=f_stereo)
    draw_arrow(draw, ucs["uc07"]["c"][0] - ucs["uc07"]["rx"], ucs["uc07"]["c"][1],
               ucs["uc04"]["c"][0] + ucs["uc04"]["rx"], ucs["uc04"]["c"][1] + 20,
               is_dashed=True, label="<<include>>", font_label=f_stereo)
    draw_arrow(draw, ucs["uc10"]["c"][0] - ucs["uc10"]["rx"], ucs["uc10"]["c"][1],
               ucs["uc09"]["c"][0] + ucs["uc09"]["rx"], ucs["uc09"]["c"][1],
               is_dashed=True, label="<<include>>", font_label=f_stereo)
    draw_arrow(draw, ucs["uc10"]["c"][0], ucs["uc10"]["c"][1] + ucs["uc10"]["ry"],
               ucs["uc11"]["c"][0], ucs["uc11"]["c"][1] - ucs["uc11"]["ry"],
               is_dashed=True, label="<<include>>", font_label=f_stereo)
    draw_arrow(draw, ucs["uc14"]["c"][0] - ucs["uc14"]["rx"], ucs["uc14"]["c"][1],
               ucs["uc12"]["c"][0] + ucs["uc12"]["rx"], ucs["uc12"]["c"][1],
               is_dashed=True, label="<<extend>>", font_label=f_stereo)

    for k, d in ucs.items():
        cx, cy = d["c"]
        draw_ellipse_uc(draw, cx, cy, d["rx"], d["ry"], d["name"], f_uc)

    out_file = os.path.join(UC_DIR, "usecase_ainative_customer.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print("Saved:", out_file)

# ==============================================================================
# 3. SƠ ĐỒ PHÂN HỆ QUẢN TRỊ & NHÀ BÁN (10 USE CASES)
# ==============================================================================
def generate_admin_usecase():
    w, h = 1350, 920
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_actor, f_uc, f_uc_bold, f_stereo, f_small = get_fonts()

    title = "SƠ ĐỒ USE CASE PHÂN HỆ QUẢN TRỊ & NHÀ BÁN (MERCHANT & ADMIN)"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 18), title, fill=(30, 126, 52), font=f_title)

    bx1, by1, bx2, by2 = 210, 65, 1140, 880
    draw.rectangle([bx1, by1, bx2, by2], outline=(70, 80, 95), width=2)
    draw.text((bx1 + 18, by1 + 12), "Phân hệ Quản trị & Nhà bán (Admin & Merchant Boundary)", fill=(40, 50, 60), font=f_box)

    pos_admin = (1245, 420)
    pos_carrier = (105, 420)

    draw_actor(draw, pos_admin[0], pos_admin[1], "Admin / Merchant\n(Quản trị & Nhà bán)", f_actor, color=(30, 126, 52))
    draw_actor(draw, pos_carrier[0], pos_carrier[1], "Hệ thống kho &\nVận chuyển đối tác", f_actor, color=(70, 80, 95))

    c1 = 440
    c2 = 840

    ucs = {
        "uc15": {"name": "UC15: Quản lý danh mục & SP AI", "c": (c2, 130), "rx": 110, "ry": 28},
        "uc_vec": {"name": "Tự động sinh Vector Embeddings", "c": (c1, 130), "rx": 112, "ry": 28},
        "uc16": {"name": "UC16: Quản lý tồn kho & Cảnh báo", "c": (c2, 260), "rx": 112, "ry": 28},
        "uc17": {"name": "UC17: Quản lý đơn & Vận chuyển", "c": (c2, 380), "rx": 110, "ry": 28},
        "uc_ship": {"name": "Đồng bộ mã vận đơn đối tác", "c": (c1, 380), "rx": 110, "ry": 28},
        "uc18": {"name": "UC18: Quản lý Voucher & Giá bán", "c": (c2, 500), "rx": 110, "ry": 28},
        "uc19": {"name": "UC19: Quản lý User & RBAC Roles", "c": (c2, 620), "rx": 110, "ry": 28},
        "uc20": {"name": "UC20: Cấu hình Prompt & Guardrails", "c": (c1, 620), "rx": 112, "ry": 28},
        "uc21": {"name": "UC21: Báo cáo thống kê doanh thu", "c": (c2, 740), "rx": 110, "ry": 28},
        "uc22": {"name": "UC22: Đối soát & Hoa hồng Merchant", "c": (c1, 740), "rx": 112, "ry": 28},
    }

    lc = (30, 126, 52)
    for k in ["uc15", "uc16", "uc17", "uc18", "uc19", "uc21"]:
        cx, cy = ucs[k]["c"]
        draw.line([pos_admin[0]-30, pos_admin[1], cx + ucs[k]["rx"], cy], fill=lc, width=1)

    draw.line([pos_carrier[0]+30, pos_carrier[1], ucs["uc_ship"]["c"][0] - ucs["uc_ship"]["rx"], ucs["uc_ship"]["c"][1]], fill=(70, 80, 95), width=1)
    draw.line([pos_admin[0]-30, pos_admin[1], ucs["uc20"]["c"][0] + ucs["uc20"]["rx"], ucs["uc20"]["c"][1]], fill=lc, width=1)
    draw.line([pos_admin[0]-30, pos_admin[1], ucs["uc22"]["c"][0] + ucs["uc22"]["rx"], ucs["uc22"]["c"][1]], fill=lc, width=1)

    draw_arrow(draw, ucs["uc15"]["c"][0] - ucs["uc15"]["rx"], ucs["uc15"]["c"][1],
               ucs["uc_vec"]["c"][0] + ucs["uc_vec"]["rx"], ucs["uc_vec"]["c"][1],
               is_dashed=True, label="<<include>>", font_label=f_stereo)
    draw_arrow(draw, ucs["uc_ship"]["c"][0] + ucs["uc_ship"]["rx"], ucs["uc_ship"]["c"][1],
               ucs["uc17"]["c"][0] - ucs["uc17"]["rx"], ucs["uc17"]["c"][1],
               is_dashed=True, label="<<extend>>", font_label=f_stereo)

    for k, d in ucs.items():
        cx, cy = d["c"]
        draw_ellipse_uc(draw, cx, cy, d["rx"], d["ry"], d["name"], f_uc, border_color=(30, 126, 52), fill_color=(238, 250, 240))

    out_file = os.path.join(UC_DIR, "usecase_ainative_admin.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print("Saved:", out_file)

# ==============================================================================
# 4. SƠ ĐỒ PHÂN HỆ TÁC TỬ AI PLATFORM (8 USE CASES)
# ==============================================================================
def generate_agent_usecase():
    w, h = 1350, 880
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_actor, f_uc, f_uc_bold, f_stereo, f_small = get_fonts()

    title = "SƠ ĐỒ USE CASE PHÂN HỆ NỀN TẢNG TÁC TỬ AI (AI AGENT PLATFORM)"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 18), title, fill=(111, 66, 193), font=f_title)

    bx1, by1, bx2, by2 = 210, 65, 1140, 840
    draw.rectangle([bx1, by1, bx2, by2], outline=(70, 80, 95), width=2)
    draw.text((bx1 + 18, by1 + 12), "Phân hệ Tác tử AI (AI Agent Platform Boundary)", fill=(40, 50, 60), font=f_box)

    pos_agent = (1245, 420)
    pos_user = (105, 420)

    draw_actor(draw, pos_agent[0], pos_agent[1], "AI Agent\nPlatform", f_actor, color=(111, 66, 193))
    draw_actor(draw, pos_user[0], pos_user[1], "Customer /\nExternal API", f_actor, color=(31, 78, 121))

    c1 = 440
    c2 = 840

    ucs = {
        "uc23": {"name": "UC23: Gợi ý cá nhân hóa", "c": (c1, 140), "rx": 110, "ry": 28},
        "uc24": {"name": "UC24: Điều phối Multi-Agent", "c": (c2, 140), "rx": 112, "ry": 28},
        "uc25": {"name": "UC25: Truy xuất Vector RAG", "c": (c1, 320), "rx": 112, "ry": 28},
        "uc26": {"name": "UC26: Giao dịch qua tác tử ACP", "c": (c2, 320), "rx": 115, "ry": 30},
        "uc27": {"name": "UC27: Giám sát Guardrails", "c": (c2, 500), "rx": 110, "ry": 28},
        "uc_otp": {"name": "Xác thực 2FA OTP vượt ngưỡng", "c": (c1, 500), "rx": 112, "ry": 28},
        "uc28": {"name": "UC28: Audit Log & Giám sát Token", "c": (c2, 680), "rx": 115, "ry": 28},
        "uc_mem": {"name": "Quản lý bộ nhớ hội thoại Memory", "c": (c1, 680), "rx": 112, "ry": 28},
    }

    lc = (111, 66, 193)
    for k in ["uc23", "uc24", "uc25", "uc26", "uc27", "uc28"]:
        cx, cy = ucs[k]["c"]
        draw.line([pos_agent[0]-30, pos_agent[1], cx + ucs[k]["rx"], cy], fill=lc, width=1)
    for k in ["uc23", "uc25", "uc26"]:
        cx, cy = ucs[k]["c"]
        draw.line([pos_user[0]+30, pos_user[1], cx - ucs[k]["rx"], cy], fill=(31, 78, 121), width=1)

    draw_arrow(draw, ucs["uc26"]["c"][0], ucs["uc26"]["c"][1] + ucs["uc26"]["ry"],
               ucs["uc27"]["c"][0], ucs["uc27"]["c"][1] - ucs["uc27"]["ry"],
               is_dashed=True, label="<<include>>", font_label=f_stereo)
    draw_arrow(draw, ucs["uc_otp"]["c"][0] + ucs["uc_otp"]["rx"], ucs["uc_otp"]["c"][1],
               ucs["uc26"]["c"][0] - ucs["uc26"]["rx"], ucs["uc26"]["c"][1],
               is_dashed=True, label="<<extend>>", font_label=f_stereo)
    draw_arrow(draw, ucs["uc25"]["c"][0], ucs["uc25"]["c"][1] + ucs["uc25"]["ry"],
               ucs["uc_mem"]["c"][0], ucs["uc_mem"]["c"][1] - ucs["uc_mem"]["ry"],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    for k, d in ucs.items():
        cx, cy = d["c"]
        draw_ellipse_uc(draw, cx, cy, d["rx"], d["ry"], d["name"], f_uc, border_color=(111, 66, 193), fill_color=(245, 238, 253))

    out_file = os.path.join(UC_DIR, "usecase_ainative_agent.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print("Saved:", out_file)

# ==============================================================================
# 5. SƠ ĐỒ THỰC THỂ KHÁI NIỆM CONCEPTUAL ERD (1500 x 980)
# ==============================================================================
def generate_erd_diagram():
    w, h = 1500, 980
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_actor, f_uc, f_uc_bold, f_stereo, f_small = get_fonts()

    title = "SƠ ĐỒ MÔ HÌNH THỰC THỂ QUAN HỆ KHÁI NIỆM (CONCEPTUAL ERD)"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 18), title, fill=(31, 78, 121), font=f_title)

    sub = "Mô hình hóa 10 Thực thể Cốt lõi & Mối quan hệ Khái niệm (1-1, 1-N, N-N) trong AI-Native Commerce"
    bb_sub = draw.textbbox((0, 0), sub, font=f_sub)
    draw.text(((w - (bb_sub[2]-bb_sub[0]))//2, 52), sub, fill=(90, 105, 120), font=f_sub)

    entities = {
        "User": {"pos": (80, 110, 260, 290), "title": "USER / ACCOUNT", "color": (31, 78, 121),
                 "attrs": ["+ user_id (PK)", "- email / phone", "- password_hash", "- role (Guest/Cust/Admin)", "- created_at"]},
        "Customer": {"pos": (80, 370, 260, 550), "title": "CUSTOMER", "color": (46, 117, 182),
                     "attrs": ["+ customer_id (PK)", "+ user_id (FK)", "- full_name", "- address_default", "- loyalty_points"]},
        "Merchant": {"pos": (80, 650, 260, 830), "title": "MERCHANT", "color": (30, 126, 52),
                     "attrs": ["+ merchant_id (PK)", "+ user_id (FK)", "- store_name", "- commission_rate", "- status (Active)"]},
        "Cart": {"pos": (440, 370, 630, 530), "title": "CART", "color": (46, 117, 182),
                 "attrs": ["+ cart_id (PK)", "+ customer_id (FK)", "- total_price", "- updated_at"]},
        "CartItem": {"pos": (440, 600, 630, 780), "title": "CART_ITEM", "color": (46, 117, 182),
                     "attrs": ["+ item_id (PK)", "+ cart_id (FK)", "+ product_id (FK)", "- quantity", "- unit_price"]},
        "Product": {"pos": (810, 650, 1020, 860), "title": "PRODUCT", "color": (30, 126, 52),
                    "attrs": ["+ product_id (PK)", "+ merchant_id (FK)", "- title / slug", "- base_price", "- stock_quantity", "- embedding_vector"]},
        "Order": {"pos": (810, 330, 1020, 540), "title": "ORDER", "color": (180, 80, 20),
                  "attrs": ["+ order_id (PK)", "+ customer_id (FK)", "- total_amount", "- order_status (Saga)", "- idempotency_key"]},
        "OrderItem": {"pos": (1180, 480, 1400, 650), "title": "ORDER_ITEM", "color": (180, 80, 20),
                      "attrs": ["+ order_item_id (PK)", "+ order_id (FK)", "+ product_id (FK)", "- quantity", "- price_at_purchase"]},
        "Payment": {"pos": (1180, 240, 1400, 410), "title": "PAYMENT_TXN", "color": (180, 80, 20),
                    "attrs": ["+ payment_id (PK)", "+ order_id (FK)", "- provider (VNPay)", "- status (Success)", "- transaction_ref"]},
        "AIConv": {"pos": (440, 110, 660, 290), "title": "AI_CONVERSATION", "color": (111, 66, 193),
                   "attrs": ["+ conv_id (PK)", "+ customer_id (FK)", "- agent_type", "- memory_context", "- token_consumed"]}
    }

    def draw_entity(draw, ent):
        x1, y1, x2, y2 = ent["pos"]
        # Header Box
        draw.rectangle([x1, y1, x2, y1 + 32], fill=ent["color"], outline=(40, 50, 60), width=1)
        bb = draw.textbbox((0, 0), ent["title"], font=f_box)
        draw.text(((x1 + x2 - (bb[2]-bb[0]))//2, y1 + 7), ent["title"], fill=(255, 255, 255), font=f_box)
        # Body Box
        draw.rectangle([x1, y1 + 32, x2, y2], fill=(250, 252, 255), outline=(40, 50, 60), width=1)
        for i, attr in enumerate(ent["attrs"]):
            col = (180, 40, 40) if "PK" in attr else ((30, 100, 180) if "FK" in attr else (40, 50, 60))
            draw.text((x1 + 10, y1 + 38 + i*20), attr, fill=col, font=f_small)

    for k, ent in entities.items():
        draw_entity(draw, ent)

    # Connections with Cardinality (1 - 1, 1 - N)
    def draw_rel(p1, p2, card1="1", card2="N", label=""):
        draw.line([p1[0], p1[1], p2[0], p2[1]], fill=(60, 70, 85), width=2)
        draw.text((p1[0]+5, p1[1]-15), card1, fill=(200, 30, 30), font=f_box)
        draw.text((p2[0]-15, p2[1]-15), card2, fill=(200, 30, 30), font=f_box)
        if label:
            mx, my = (p1[0]+p2[0])//2, (p1[1]+p2[1])//2 - 10
            draw.text((mx, my), label, fill=(100, 110, 120), font=f_small)

    # User -> Customer (1 - 1)
    draw_rel((170, 290), (170, 370), "1", "1")
    # User -> Merchant (1 - 1)
    draw_rel((170, 550), (170, 650), "1", "1")
    # Customer -> Cart (1 - 1)
    draw_rel((260, 450), (440, 450), "1", "1")
    # Cart -> CartItem (1 - N)
    draw_rel((535, 530), (535, 600), "1", "N")
    # Product -> CartItem (1 - N)
    draw_rel((810, 700), (630, 700), "1", "N")
    # Merchant -> Product (1 - N)
    draw_rel((260, 740), (810, 740), "1", "N")
    # Customer -> Order (1 - N)
    draw.line([260, 490, 810, 440], fill=(60, 70, 85), width=2)
    draw.text((270, 475), "1", fill=(200, 30, 30), font=f_box)
    draw.text((790, 425), "N", fill=(200, 30, 30), font=f_box)
    # Order -> OrderItem (1 - N)
    draw_rel((1020, 450), (1180, 540), "1", "N")
    # Product -> OrderItem (1 - N)
    draw_rel((1020, 700), (1180, 600), "1", "N")
    # Order -> Payment (1 - N)
    draw_rel((1020, 380), (1180, 330), "1", "N")
    # Customer -> AIConv (1 - N)
    draw.line([260, 410, 440, 220], fill=(60, 70, 85), width=2)
    draw.text((270, 390), "1", fill=(200, 30, 30), font=f_box)
    draw.text((420, 205), "N", fill=(200, 30, 30), font=f_box)

    out_file = os.path.join(DESIGN_DIR, "erd_ainative_conceptual.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print("Saved:", out_file)

# ==============================================================================
# 6. SƠ ĐỒ TRIỂN KHAI HỆ THỐNG DEPLOY DIAGRAM (1500 x 980)
# ==============================================================================
def generate_deploy_diagram():
    w, h = 1500, 980
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_actor, f_uc, f_uc_bold, f_stereo, f_small = get_fonts()

    title = "SƠ ĐỒ TRIỂN KHAI HỆ THỐNG (DEPLOYMENT DIAGRAM)"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 18), title, fill=(31, 78, 121), font=f_title)

    sub = "Kiến trúc Triển khai Hạ tầng Đa tầng (Multi-tier Containerized Infrastructure) với Docker Compose"
    bb_sub = draw.textbbox((0, 0), sub, font=f_sub)
    draw.text(((w - (bb_sub[2]-bb_sub[0]))//2, 52), sub, fill=(90, 105, 120), font=f_sub)

    def draw_3d_node(x1, y1, x2, y2, title, items, fill=(245, 248, 253), border=(46, 117, 182)):
        depth = 12
        # Back/Top faces
        draw.polygon([(x1, y1), (x1 + depth, y1 - depth), (x2 + depth, y1 - depth), (x2, y1)], fill=(225, 235, 245), outline=border)
        draw.polygon([(x2, y1), (x2 + depth, y1 - depth), (x2 + depth, y2 - depth), (x2, y2)], fill=(210, 222, 235), outline=border)
        # Front face
        draw.rectangle([x1, y1, x2, y2], fill=fill, outline=border, width=2)
        # Header
        draw.rectangle([x1, y1, x2, y1 + 30], fill=border)
        bb = draw.textbbox((0, 0), title, font=f_box)
        draw.text(((x1 + x2 - (bb[2]-bb[0]))//2, y1 + 7), title, fill=(255, 255, 255), font=f_box)
        # Items
        for i, it in enumerate(items):
            draw.text((x1 + 14, y1 + 38 + i*20), it, fill=(30, 40, 50), font=f_small)

    # 1. Client Node
    draw_3d_node(60, 120, 360, 360, "<<device>> Client Tier", [
        "• Web Client: Next.js / React 19 (Port 3000)",
        "• AI Chat Widget: TailwindCSS + Vite",
        "• Desktop App: Electron / Tauri Client",
        "• Mobile Client: React Native / Expo",
        "• Browser Protocols: HTTPS / WSS"
    ])

    # 2. External Edge / Gateway
    draw_3d_node(60, 430, 360, 670, "<<service>> Edge & Gateway", [
        "• Nginx Reverse Proxy & Load Balancer",
        "• SSL/TLS Termination (Port 443/80)",
        "• Rate Limiter & IP Whitelisting",
        "• Static Assets CDN & Cache",
        "• CORS & Header Security Filter"
    ])

    # 3. External Cloud Services
    draw_3d_node(60, 730, 360, 930, "<<cloud>> External Services", [
        "• VNPay Sandbox Payment Gateway",
        "• Google Gemini 1.5 Pro / Flash API",
        "• Anthropic Claude 3.5 Sonnet API",
        "• Atlassian Jira Cloud Webhooks"
    ])

    # 4. Docker Container Boundary
    bx1, by1, bx2, by2 = 450, 100, 1440, 930
    draw.rectangle([bx1, by1, bx2, by2], outline=(31, 78, 121), width=3)
    draw.text((bx1 + 20, by1 + 15), "<<execution environment>> Docker Compose Production Host", fill=(31, 78, 121), font=f_box)

    # Application Services inside Docker
    draw_3d_node(490, 160, 920, 420, "<<container>> Core API Service", [
        "• ASP.NET Core 8 / Express.js REST API",
        "• JWT Authentication & RBAC Middleware",
        "• Cart & Checkout Saga Orchestration",
        "• Order Management & Idempotency Filter",
        "• WebSocket Server for Live Notifications (Port 5000)"
    ], border=(31, 78, 121))

    draw_3d_node(970, 160, 1400, 420, "<<container>> AI-RAG & Agent Engine", [
        "• Python 3.11+ FastAPI Service (Port 8000)",
        "• LangChain & LlamaIndex Orchestrator",
        "• Text Embeddings & Hybrid Search Service",
        "• Guardrail Engine & Token Rate Limiter",
        "• Agentic Commerce Protocol (ACP) Adapter"
    ], border=(111, 66, 193), fill=(250, 245, 255))

    draw_3d_node(490, 480, 920, 680, "<<container>> MCP Server", [
        "• Model Context Protocol Server (Port 3001)",
        "• Exposes Tools: query_boards, create_card",
        "• Read/Write Data Connectors for AI Agents",
        "• Secure Token Inspection & Audit Log"
    ], border=(217, 119, 6), fill=(255, 250, 245))

    draw_3d_node(970, 480, 1400, 680, "<<container>> Cache & Queue Tier", [
        "• Redis In-Memory Database (Port 6379)",
        "• Distributed Session & Cart Store",
        "• Pub/Sub Message Broker for Events",
        "• Idempotency Cache (TTL 24h)"
    ], border=(200, 35, 51), fill=(255, 245, 245))

    draw_3d_node(490, 720, 920, 900, "<<container>> Primary Relational DB", [
        "• PostgreSQL 16 Enterprise (Port 5432)",
        "• Transactional DDL: Users, Orders, Payments",
        "• ACID Compliant, WAL Replication & Outbox",
        "• Encrypted Connection & Automatic Backups"
    ], border=(30, 126, 52), fill=(245, 255, 248))

    draw_3d_node(970, 720, 1400, 900, "<<container>> Vector DB & Object Storage", [
        "• ChromaDB Vector Store (Port 8001)",
        "• Product Catalog Semantic Embeddings",
        "• MinIO S3-Compatible Object Store (Port 9000)",
        "• Product Media, PDF Invoices & Thumbnails"
    ], border=(30, 126, 52), fill=(245, 255, 248))

    # Connection Lines
    draw.line([360, 240, 450, 240], fill=(46, 117, 182), width=3)
    draw.line([360, 550, 490, 550], fill=(46, 117, 182), width=2)
    draw.line([920, 280, 970, 280], fill=(111, 66, 193), width=2)
    draw.line([705, 420, 705, 480], fill=(31, 78, 121), width=2)
    draw.line([705, 680, 705, 720], fill=(30, 126, 52), width=2)
    draw.line([1185, 420, 1185, 480], fill=(200, 35, 51), width=2)
    draw.line([1185, 680, 1185, 720], fill=(30, 126, 52), width=2)

    out_file = os.path.join(DESIGN_DIR, "deploy_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print("Saved:", out_file)

# ==============================================================================
# 7. SƠ ĐỒ TỔ CHỨC ỨNG DỤNG APPMAP / SITEMAP (1500 x 980)
# ==============================================================================
def generate_appmap_diagram():
    w, h = 1500, 980
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_actor, f_uc, f_uc_bold, f_stereo, f_small = get_fonts()

    title = "SƠ ĐỒ TỔ CHỨC CỦA ỨNG DỤNG (APPMAP / SITEMAP NAVIGATION FLOW)"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 18), title, fill=(31, 78, 121), font=f_title)

    sub = "Cấu trúc Phân cấp Điều hướng Màn hình & Luồng Chức năng Toàn hệ thống AI-Native Commerce"
    bb_sub = draw.textbbox((0, 0), sub, font=f_sub)
    draw.text(((w - (bb_sub[2]-bb_sub[0]))//2, 52), sub, fill=(90, 105, 120), font=f_sub)

    def draw_app_node(x, y, w_box, h_box, title, subtitle="", fill=(245, 248, 252), border=(46, 117, 182)):
        draw.rectangle([x, y, x + w_box, y + h_box], fill=fill, outline=border, width=2)
        bb = draw.textbbox((0, 0), title, font=f_box)
        draw.text((x + (w_box - (bb[2]-bb[0]))//2, y + 8), title, fill=border, font=f_box)
        if subtitle:
            bb2 = draw.textbbox((0, 0), subtitle, font=f_small)
            draw.text((x + (w_box - (bb2[2]-bb2[0]))//2, y + 28), subtitle, fill=(60, 70, 80), font=f_small)

    # Root Level (Top)
    draw_app_node(620, 100, 260, 52, "PORTAL CHÍNH (HOMEPAGE)", "Trang chủ Đa kênh / Web & Mobile", fill=(238, 245, 253), border=(31, 78, 121))

    # Level 2 (4 Main Branches)
    draw_app_node(80, 210, 280, 52, "1. PHÂN HỆ DÙNG CHUNG", "Đăng ký, Đăng nhập, Tìm kiếm NLP", fill=(254, 243, 235), border=(217, 119, 6))
    draw_app_node(420, 210, 310, 52, "2. KHÁCH HÀNG & MUA SẮM", "AI Assistant, Giỏ hàng, Checkout Saga", fill=(238, 245, 253), border=(46, 117, 182))
    draw_app_node(780, 210, 310, 52, "3. NHÀ BÁN HÀNG (MERCHANT)", "Quản lý SP, Đơn hàng, Tồn kho", fill=(238, 250, 240), border=(30, 126, 52))
    draw_app_node(1140, 210, 300, 52, "4. QUẢN TRỊ VIÊN (ADMIN)", "Dashboard, RBAC, Cấu hình AI", fill=(245, 238, 253), border=(111, 66, 193))

    # Connect Root to Level 2
    draw.line([750, 152, 750, 180], fill=(70, 80, 95), width=2)
    draw.line([220, 180, 1290, 180], fill=(70, 80, 95), width=2)
    draw.line([220, 180, 220, 210], fill=(70, 80, 95), width=2)
    draw.line([575, 180, 575, 210], fill=(70, 80, 95), width=2)
    draw.line([935, 180, 935, 210], fill=(70, 80, 95), width=2)
    draw.line([1290, 180, 1290, 210], fill=(70, 80, 95), width=2)

    # Level 3 Screens / Actions
    screens_b1 = [
        ("Màn hình Đăng ký tài khoản", "Xác thực OTP & Email kích hoạt"),
        ("Màn hình Đăng nhập", "Hỗ trợ JWT & OAuth Google/Github"),
        ("Màn hình Quên mật khẩu", "Reset mật khẩu qua Magic Link"),
        ("Màn hình Tìm kiếm NLP", "Gợi ý tự động & Bộ lọc thông minh"),
        ("Trang Chi tiết sản phẩm", "Thông số, Media 360 & So sánh AI")
    ]
    for i, (t, s) in enumerate(screens_b1):
        draw_app_node(80, 300 + i*70, 280, 52, t, s, border=(217, 119, 6))
        draw.line([220, 262, 220, 300 + i*70], fill=(217, 119, 6), width=1)

    screens_b2 = [
        ("Widget Trợ lý Mua sắm AI", "Tư vấn ngữ cảnh hội thoại 24/7"),
        ("Màn hình Giỏ hàng thông minh", "Kiểm tra tồn kho thời gian thực"),
        ("Màn hình Checkout Saga", "Chọn địa chỉ, Áp Voucher tối ưu"),
        ("Cổng Thanh toán VNPay", "Quét mã QR / Thẻ ATM / Visa"),
        ("Màn hình Theo dõi vận đơn", "Bản đồ thời gian thực & Đổi trả")
    ]
    for i, (t, s) in enumerate(screens_b2):
        draw_app_node(420, 300 + i*70, 310, 52, t, s, border=(46, 117, 182))
        draw.line([575, 262, 575, 300 + i*70], fill=(46, 117, 182), width=1)

    screens_b3 = [
        ("Merchant Dashboard", "Tổng quan doanh số & Tỷ lệ hủy đơn"),
        ("Quản lý Danh mục & Sản phẩm", "Soạn thảo bài đăng & AI Enrichment"),
        ("Quản lý Kho & Tồn kho", "Cảnh báo hết hàng tự động"),
        ("Quản lý Đơn & Vận chuyển", "In phiếu đóng gói & Giao shipper"),
        ("Báo cáo Đối soát hoa hồng", "Bảng kê rút tiền & Thuế GTGT")
    ]
    for i, (t, s) in enumerate(screens_b3):
        draw_app_node(780, 300 + i*70, 310, 52, t, s, border=(30, 126, 52))
        draw.line([935, 262, 935, 300 + i*70], fill=(30, 126, 52), width=1)

    screens_b4 = [
        ("Executive Admin Dashboard", "Biểu đồ KPI toàn sàn & Lưu lượng"),
        ("Quản lý User & Phân quyền", "Gán vai trò RBAC & Khóa tài khoản"),
        ("Cấu hình AI Guardrails", "Giới hạn ngân sách Agent & Lọc độc hại"),
        ("Giám sát Token & Audit Log", "Lịch sử can thiệp của AI Tự hành"),
        ("Quản lý Khuyến mãi toàn sàn", "Chiến dịch Flash Sale & Mã giảm giá")
    ]
    for i, (t, s) in enumerate(screens_b4):
        draw_app_node(1140, 300 + i*70, 300, 52, t, s, border=(111, 66, 193))
        draw.line([1290, 262, 1290, 300 + i*70], fill=(111, 66, 193), width=1)

    out_file = os.path.join(DESIGN_DIR, "appmap_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print("Saved:", out_file)

# ==============================================================================
# 8. SƠ ĐỒ MÔ HÌNH CÔNG NGHỆ TECH STACK (1500 x 980)
# ==============================================================================
def generate_tech_stack_diagram():
    w, h = 1500, 980
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_actor, f_uc, f_uc_bold, f_stereo, f_small = get_fonts()

    title = "SƠ ĐỒ PHÂN TẦNG MÔ HÌNH CÔNG NGHỆ (TECH STACK ARCHITECTURE)"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 18), title, fill=(31, 78, 121), font=f_title)

    sub = "Kiến trúc 5 Tầng Công nghệ Hiện đại Hợp nhất AI & Thương Mại Điện Tử (AI-Native Stack)"
    bb_sub = draw.textbbox((0, 0), sub, font=f_sub)
    draw.text(((w - (bb_sub[2]-bb_sub[0]))//2, 52), sub, fill=(90, 105, 120), font=f_sub)

    layers = [
        {"name": "TẦNG 1: TRẢI NGHIỆM NGƯỜI DÙNG (EXPERIENCE & CLIENT LAYER)", "color": (31, 78, 121), "fill": (238, 245, 253),
         "components": [
             ("Next.js 14 / React 19", "Server-Side Rendering, App Router, Tối ưu SEO sàn"),
             ("TailwindCSS & Shadcn UI", "Hệ thống giao diện Design System hiện đại, responsive"),
             ("Zustand & React Query", "Quản lý State giỏ hàng & đồng bộ cache bất đồng bộ"),
             ("DnD Kit & Lucide Icons", "Trải nghiệm kéo thả Kanban Board & bộ icon trực quan"),
             ("AI Conversational Widget", "Widget trợ lý hội thoại nhúng đa nền tảng (Web/Mobile)")
         ]},
        {"name": "TẦNG 2: CỔNG TRUYỀN THÔNG & BẢO MẬT (API GATEWAY & SECURITY LAYER)", "color": (217, 119, 6), "fill": (254, 243, 235),
         "components": [
             ("Nginx Reverse Proxy", "Cân bằng tải, SSL Termination, nén Gzip/Brotli"),
             ("JWT Authentication", "Xác thực token Stateless, phân quyền RBAC phân cấp"),
             ("Rate Limiting & DDoS Shield", "Chống spam request và bảo vệ điểm cuối nhạy cảm"),
             ("CORS & Helmet Policy", "Bảo mật Header trình duyệt, chống tấn công XSS/CSRF"),
             ("Model Context Protocol (MCP)", "Cổng kết nối an toàn cho AI Agents tương tác hệ thống")
         ]},
        {"name": "TẦNG 3: DỊCH VỤ NGHIỆP VỤ LÕI (APPLICATION & SERVICE LAYER)", "color": (30, 126, 52), "fill": (238, 250, 240),
         "components": [
             ("ASP.NET Core 8 / Express API", "Backend hiệu năng cao, Dependency Injection, Middleware"),
             ("Checkout Saga Coordinator", "Điều phối giao dịch phân tán, chống bán quá tồn kho"),
             ("Idempotency Engine", "Chống trùng lặp thanh toán và lặp đơn qua Unique Keys"),
             ("Prisma ORM / EF Core", "Truy vấn CSDL an toàn, Type-safe tuyệt đối"),
             ("VNPay SDK & Payment Hub", "Tích hợp cổng thanh toán trực tuyến chuẩn ngân hàng")
         ]},
        {"name": "TẦNG 4: TRÍ TUỆ NHÂN TẠO & TÁC TỬ (AI & INTELLIGENCE LAYER)", "color": (111, 66, 193), "fill": (245, 238, 253),
         "components": [
             ("Python FastAPI Microservice", "Xử lý RAG, tính toán vector và gọi LLMs tốc độ cao"),
             ("Google Gemini 1.5 Pro / Flash", "LLM đa phương thức nhận diện ý định và sinh nội dung"),
             ("LangChain & Vector Retriever", "Quy trình tìm kiếm lai (Hybrid Search: BM25 + Dense)"),
             ("Agentic Commerce Protocol (ACP)", "Chuẩn giao tiếp tác tử tự động chốt đơn an toàn"),
             ("AI Guardrail & Budget Monitor", "Hàng rào an toàn giới hạn hạn mức và lọc rủi ro")
         ]},
        {"name": "TẦNG 5: DỮ LIỆU & HẠ TẦNG LƯU TRỮ (PERSISTENCE & INFRASTRUCTURE LAYER)", "color": (180, 80, 20), "fill": (254, 243, 235),
         "components": [
             ("PostgreSQL 16 Enterprise", "Lưu trữ dữ liệu quan hệ ACID: Users, Products, Orders"),
             ("Redis In-Memory Data Store", "Cache giỏ hàng, Session, hàng đợi sự kiện và Pub/Sub"),
             ("ChromaDB Vector Database", "Lưu trữ Vector Embeddings tra cứu ngữ nghĩa mili-giây"),
             ("MinIO S3 Object Storage", "Lưu trữ ảnh sản phẩm, tài liệu hợp đồng và PDF hóa đơn"),
             ("Docker Compose & CI/CD", "Đóng gói container chuẩn hóa, triển khai tự động hóa")
         ]}
    ]

    y_offset = 100
    for l_idx, layer in enumerate(layers):
        draw.rectangle([60, y_offset, 1440, y_offset + 145], fill=layer["fill"], outline=layer["color"], width=2)
        # Layer Title Header
        draw.rectangle([60, y_offset, 1440, y_offset + 32], fill=layer["color"])
        draw.text((75, y_offset + 7), layer["name"], fill=(255, 255, 255), font=f_box)

        # 5 Component Cards inside Layer
        card_w = 260
        card_gap = 14
        start_x = 75
        for c_idx, (c_name, c_desc) in enumerate(layer["components"]):
            cx = start_x + c_idx * (card_w + card_gap)
            cy = y_offset + 42
            draw.rectangle([cx, cy, cx + card_w, cy + 92], fill=(255, 255, 255), outline=layer["color"], width=1)
            # Component Name
            draw.text((cx + 10, cy + 8), c_name, fill=layer["color"], font=f_uc_bold)
            # Component Desc (wrap)
            words = c_desc.split(" ")
            line1, line2 = "", ""
            for w_word in words:
                if len(line1 + " " + w_word) < 32:
                    line1 += (" " if line1 else "") + w_word
                else:
                    line2 += (" " if line2 else "") + w_word
            draw.text((cx + 10, cy + 32), line1, fill=(60, 70, 80), font=f_small)
            if line2:
                draw.text((cx + 10, cy + 52), line2, fill=(60, 70, 80), font=f_small)

        y_offset += 165

    out_file = os.path.join(DESIGN_DIR, "tech_stack_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print("Saved:", out_file)

if __name__ == "__main__":
    generate_general_usecase()
    generate_customer_usecase()
    generate_admin_usecase()
    generate_agent_usecase()
    generate_erd_diagram()
    generate_deploy_diagram()
    generate_appmap_diagram()
    generate_tech_stack_diagram()
    print("=== ALL 8 DIAGRAMS GENERATED SUCCESSFULLY! ===")
