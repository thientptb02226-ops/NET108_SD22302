# -*- coding: utf-8 -*-
import math
import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    try:
        f_title = ImageFont.truetype("arialbd.ttf", 20)
        f_box = ImageFont.truetype("arialbd.ttf", 15)
        f_actor = ImageFont.truetype("arialbd.ttf", 13)
        f_uc = ImageFont.truetype("arial.ttf", 12)
        f_uc_bold = ImageFont.truetype("arialbd.ttf", 12)
        f_stereo = ImageFont.truetype("ariali.ttf", 11)
    except Exception:
        f_title = f_box = f_actor = f_uc = f_uc_bold = f_stereo = ImageFont.load_default()
    return f_title, f_box, f_actor, f_uc, f_uc_bold, f_stereo

def draw_actor(draw, x, y, name, font, color=(31, 78, 121)):
    draw.ellipse([x-18, y-55, x+18, y-19], outline=color, width=2, fill=(245, 248, 252))
    draw.line([x, y-19, x, y+28], fill=color, width=2)
    draw.line([x-25, y-5, x+25, y-5], fill=color, width=2)
    draw.line([x, y+28, x-20, y+70], fill=color, width=2)
    draw.line([x, y+28, x+20, y+70], fill=color, width=2)
    lines = name.split("\n")
    for i, l in enumerate(lines):
        bb = draw.textbbox((0, 0), l, font=font)
        w = bb[2] - bb[0]
        draw.text((x - w//2, y + 78 + i*16), l, fill=color, font=font)

def draw_ellipse_uc(draw, cx, cy, rx, ry, name, font, border_color=(46, 117, 182), fill_color=(238, 245, 253)):
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=border_color, width=2, fill=fill_color)
    lines = name.split("\n")
    total_h = len(lines) * 15
    start_y = cy - total_h // 2
    for i, l in enumerate(lines):
        bb = draw.textbbox((0, 0), l, font=font)
        w = bb[2] - bb[0]
        draw.text((cx - w//2, start_y + i*15), l, fill=(20, 30, 50), font=font)

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

def draw_arrow(draw, x1, y1, x2, y2, fill=(100, 110, 125), width=1, is_dashed=True, label=None, font_label=None):
    if is_dashed:
        draw_dashed_line(draw, x1, y1, x2, y2, fill=fill, width=width)
    else:
        draw.line([x1, y1, x2, y2], fill=fill, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    alen = 9
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
        draw.text((mx - w//2, my), label, fill=(160, 40, 40) if "extend" in label else (30, 120, 30), font=font_label)

# ==================== 1. SƠ ĐỒ TỔNG QUÁT (1400 x 980) ====================
def build_general_diagram():
    w, h = 1400, 980
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_box, f_actor, f_uc, f_uc_bold, f_stereo = get_fonts()

    # Title
    title = "SƠ ĐỒ USE CASE TỔNG QUÁT HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ AI-NATIVE"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 18), title, fill=(31, 78, 121), font=f_title)

    # Boundary Box
    bx1, by1, bx2, by2 = 210, 60, 1190, 940
    draw.rectangle([bx1, by1, bx2, by2], outline=(70, 80, 95), width=2)
    draw.text((bx1 + 18, by1 + 12), "Hệ thống AI-Native Commerce (Boundary)", fill=(40, 50, 60), font=f_box)

    # Actors
    pos_guest = (105, 220)
    pos_cust = (105, 620)
    pos_admin = (1295, 300)
    pos_agent = (1295, 730)

    draw_actor(draw, pos_guest[0], pos_guest[1], "Guest\n(Khách vãng lai)", f_actor)
    draw_actor(draw, pos_cust[0], pos_cust[1], "Customer\n(Khách hàng)", f_actor)
    draw_actor(draw, pos_admin[0], pos_admin[1], "Admin / Merchant\n(Quản trị & Nhà bán)", f_actor)
    draw_actor(draw, pos_agent[0], pos_agent[1], "AI Agent Platform\n(Nền tảng Tác tử AI)", f_actor)

    c1_x = 370
    c2_x = 700
    c3_x = 1030

    ucs = {
        "uc1": {"name": "UC01: Đăng ký tài khoản", "c": (c1_x, 130), "rx": 92, "ry": 28},
        "uc2": {"name": "UC02: Đăng nhập & JWT", "c": (c1_x, 235), "rx": 92, "ry": 28},
        "uc3": {"name": "UC03: Quản lý hồ sơ cá nhân", "c": (c1_x, 345), "rx": 95, "ry": 28},
        "uc4": {"name": "UC04: Tìm kiếm bằng NLP", "c": (c1_x, 460), "rx": 95, "ry": 28},
        "uc5": {"name": "UC05: Mua sắm với AI Assistant", "c": (c1_x, 575), "rx": 98, "ry": 28},
        "uc6": {"name": "UC06: Quản lý giỏ hàng thông minh", "c": (c1_x, 695), "rx": 100, "ry": 28},
        "uc7": {"name": "UC07: Đặt hàng & Khuyến mãi", "c": (c1_x, 820), "rx": 98, "ry": 28},

        # Column 2 - Shared / Transaction / Operations
        "uc_pwd": {"name": "Quên / Khôi phục mật khẩu", "c": (c2_x, 155), "rx": 95, "ry": 28},
        "uc8": {"name": "UC08: Thanh toán qua VNPay", "c": (c2_x, 820), "rx": 96, "ry": 28},
        "uc9": {"name": "UC09: Tra cứu đơn & Vận chuyển", "c": (c2_x, 690), "rx": 100, "ry": 28},
        "uc14": {"name": "UC14: Giao thức tác tử ACP", "c": (c2_x, 540), "rx": 96, "ry": 28},
        "uc_chat": {"name": "Hỗ trợ khách hàng AI (24/7)", "c": (c2_x, 380), "rx": 98, "ry": 28},

        # Column 3 - Admin / Merchant
        "uc10": {"name": "UC10: Quản lý danh mục & SP AI", "c": (c3_x, 180), "rx": 102, "ry": 28},
        "uc11": {"name": "UC11: Quản lý đơn & Trạng thái", "c": (c3_x, 320), "rx": 102, "ry": 28},
        "uc12": {"name": "UC12: Quản lý tài khoản & RBAC", "c": (c3_x, 460), "rx": 102, "ry": 28},
        "uc_promo": {"name": "Quản lý khuyến mãi & Giá", "c": (c3_x, 600), "rx": 98, "ry": 28},
        "uc13": {"name": "UC13: Báo cáo & Thống kê AI", "c": (c3_x, 740), "rx": 102, "ry": 28},
    }

    # Draw Actor Associations (Solid Lines)
    line_color = (135, 145, 160)
    for key in ["uc1", "uc2", "uc4"]:
        cx, cy = ucs[key]["c"]
        rx = ucs[key]["rx"]
        draw.line([pos_guest[0] + 30, pos_guest[1], cx - rx, cy], fill=line_color, width=1)

    for key in ["uc2", "uc3", "uc4", "uc5", "uc6", "uc7", "uc9", "uc_chat"]:
        cx, cy = ucs[key]["c"]
        rx = ucs[key]["rx"]
        draw.line([pos_cust[0] + 30, pos_cust[1], cx - rx, cy], fill=line_color, width=1)

    for key in ["uc10", "uc11", "uc12", "uc_promo", "uc13"]:
        cx, cy = ucs[key]["c"]
        rx = ucs[key]["rx"]
        draw.line([pos_admin[0] - 30, pos_admin[1], cx + rx, cy], fill=line_color, width=1)

    for key in ["uc4", "uc5", "uc14", "uc11", "uc13"]:
        cx, cy = ucs[key]["c"]
        rx = ucs[key]["rx"]
        draw.line([pos_agent[0] - 30, pos_agent[1], cx + rx, cy], fill=line_color, width=1)

    # Draw UML Stereotypes (<<include>> / <<extend>>)
    draw_arrow(draw, ucs["uc7"]["c"][0] + ucs["uc7"]["rx"], ucs["uc7"]["c"][1],
               ucs["uc8"]["c"][0] - ucs["uc8"]["rx"], ucs["uc8"]["c"][1],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    draw_arrow(draw, ucs["uc7"]["c"][0], ucs["uc7"]["c"][1] - ucs["uc7"]["ry"],
               ucs["uc6"]["c"][0], ucs["uc6"]["c"][1] + ucs["uc6"]["ry"],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    draw_arrow(draw, ucs["uc5"]["c"][0], ucs["uc5"]["c"][1] - ucs["uc5"]["ry"],
               ucs["uc4"]["c"][0], ucs["uc4"]["c"][1] + ucs["uc4"]["ry"],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    draw_arrow(draw, ucs["uc_pwd"]["c"][0] - ucs["uc_pwd"]["rx"], ucs["uc_pwd"]["c"][1] + 15,
               ucs["uc2"]["c"][0] + ucs["uc2"]["rx"], ucs["uc2"]["c"][1] - 10,
               is_dashed=True, label="<<extend>>", font_label=f_stereo)

    draw_arrow(draw, ucs["uc14"]["c"][0], ucs["uc14"]["c"][1] + ucs["uc14"]["ry"],
               ucs["uc8"]["c"][0], ucs["uc8"]["c"][1] - ucs["uc8"]["ry"],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    for key, data in ucs.items():
        cx, cy = data["c"]
        rx, ry = data["rx"], data["ry"]
        draw_ellipse_uc(draw, cx, cy, rx, ry, data["name"], f_uc)

    out_path = r"C:\Net108Khai\usecase_ainative_tongquat.png"
    img.save(out_path, "PNG")
    print("Generated:", out_path)

# ==================== 2. SƠ ĐỒ PHÂN HỆ KHÁCH HÀNG (1150 x 820) ====================
def build_customer_diagram():
    w, h = 1150, 820
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_box, f_actor, f_uc, f_uc_bold, f_stereo = get_fonts()

    title = "SƠ ĐỒ USE CASE PHÂN HỆ KHÁCH HÀNG (GUEST & CUSTOMER)"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 18), title, fill=(31, 78, 121), font=f_title)

    bx1, by1, bx2, by2 = 190, 60, 960, 780
    draw.rectangle([bx1, by1, bx2, by2], outline=(70, 80, 95), width=2)
    draw.text((bx1 + 15, by1 + 10), "Phân hệ Khách hàng (Customer Boundary)", fill=(40, 50, 60), font=f_box)

    pos_guest = (95, 200)
    pos_cust = (95, 520)
    pos_ai = (1055, 380)

    draw_actor(draw, pos_guest[0], pos_guest[1], "Guest\n(Khách)", f_actor)
    draw_actor(draw, pos_cust[0], pos_cust[1], "Customer\n(Khách hàng)", f_actor)
    draw_actor(draw, pos_ai[0], pos_ai[1], "AI Shopping\nAssistant", f_actor)

    c1_x = 380
    c2_x = 760

    ucs = {
        "uc1": {"name": "UC01: Đăng ký tài khoản", "c": (c1_x, 120), "rx": 95, "ry": 26},
        "uc2": {"name": "UC02: Đăng nhập hệ thống", "c": (c1_x, 210), "rx": 95, "ry": 26},
        "uc3": {"name": "UC03: Quản lý hồ sơ & Đổi MK", "c": (c1_x, 300), "rx": 100, "ry": 26},
        "uc4": {"name": "UC04: Tìm kiếm bằng NLP", "c": (c1_x, 400), "rx": 95, "ry": 26},
        "uc5": {"name": "UC05: Mua sắm với AI Assistant", "c": (c1_x, 500), "rx": 100, "ry": 26},
        "uc6": {"name": "UC06: Quản lý giỏ hàng thông minh", "c": (c1_x, 600), "rx": 105, "ry": 26},
        "uc7": {"name": "UC07: Đặt hàng & Áp mã ưu đãi", "c": (c1_x, 700), "rx": 102, "ry": 26},

        "uc_pwd": {"name": "Quên / Khôi phục MK", "c": (c2_x, 160), "rx": 90, "ry": 25},
        "uc8": {"name": "UC08: Thanh toán qua VNPay", "c": (c2_x, 700), "rx": 95, "ry": 26},
        "uc9": {"name": "UC09: Tra cứu đơn hàng", "c": (c2_x, 560), "rx": 95, "ry": 26},
        "uc_rec": {"name": "Gợi ý SP theo ngữ cảnh AI", "c": (c2_x, 400), "rx": 100, "ry": 26},
    }

    line_color = (135, 145, 160)
    for key in ["uc1", "uc2", "uc4"]:
        cx, cy = ucs[key]["c"]
        rx = ucs[key]["rx"]
        draw.line([pos_guest[0] + 30, pos_guest[1], cx - rx, cy], fill=line_color, width=1)

    for key in ["uc2", "uc3", "uc4", "uc5", "uc6", "uc7", "uc9"]:
        cx, cy = ucs[key]["c"]
        rx = ucs[key]["rx"]
        draw.line([pos_cust[0] + 30, pos_cust[1], cx - rx, cy], fill=line_color, width=1)

    for key in ["uc4", "uc5", "uc_rec"]:
        cx, cy = ucs[key]["c"]
        rx = ucs[key]["rx"]
        draw.line([pos_ai[0] - 30, pos_ai[1], cx + rx, cy], fill=line_color, width=1)

    draw_arrow(draw, ucs["uc7"]["c"][0] + ucs["uc7"]["rx"], ucs["uc7"]["c"][1],
               ucs["uc8"]["c"][0] - ucs["uc8"]["rx"], ucs["uc8"]["c"][1],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    draw_arrow(draw, ucs["uc7"]["c"][0], ucs["uc7"]["c"][1] - ucs["uc7"]["ry"],
               ucs["uc6"]["c"][0], ucs["uc6"]["c"][1] + ucs["uc6"]["ry"],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    draw_arrow(draw, ucs["uc5"]["c"][0], ucs["uc5"]["c"][1] - ucs["uc5"]["ry"],
               ucs["uc4"]["c"][0], ucs["uc4"]["c"][1] + ucs["uc4"]["ry"],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    draw_arrow(draw, ucs["uc_pwd"]["c"][0] - ucs["uc_pwd"]["rx"], ucs["uc_pwd"]["c"][1] + 10,
               ucs["uc2"]["c"][0] + ucs["uc2"]["rx"], ucs["uc2"]["c"][1] - 5,
               is_dashed=True, label="<<extend>>", font_label=f_stereo)

    draw_arrow(draw, ucs["uc_rec"]["c"][0] - ucs["uc_rec"]["rx"], ucs["uc_rec"]["c"][1],
               ucs["uc4"]["c"][0] + ucs["uc4"]["rx"], ucs["uc4"]["c"][1],
               is_dashed=True, label="<<extend>>", font_label=f_stereo)

    for key, data in ucs.items():
        cx, cy = data["c"]
        rx, ry = data["rx"], data["ry"]
        draw_ellipse_uc(draw, cx, cy, rx, ry, data["name"], f_uc)

    out_path = r"C:\Net108Khai\usecase_ainative_customer.png"
    img.save(out_path, "PNG")
    print("Generated:", out_path)

# ==================== 3. SƠ ĐỒ PHÂN HỆ QUẢN TRỊ (1150 x 750) ====================
def build_admin_diagram():
    w, h = 1150, 750
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_box, f_actor, f_uc, f_uc_bold, f_stereo = get_fonts()

    title = "SƠ ĐỒ USE CASE PHÂN HỆ QUẢN TRỊ & NHÀ BÁN (MERCHANT & ADMIN)"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 18), title, fill=(31, 78, 121), font=f_title)

    bx1, by1, bx2, by2 = 180, 60, 950, 710
    draw.rectangle([bx1, by1, bx2, by2], outline=(70, 80, 95), width=2)
    draw.text((bx1 + 15, by1 + 10), "Phân hệ Quản trị & Nhà bán (Admin / Merchant Boundary)", fill=(40, 50, 60), font=f_box)

    pos_admin = (1045, 360)
    pos_carrier = (95, 360)

    draw_actor(draw, pos_admin[0], pos_admin[1], "Admin / Merchant\n(Quản trị & Nhà bán)", f_actor)
    draw_actor(draw, pos_carrier[0], pos_carrier[1], "Hệ thống kho &\nVận chuyển", f_actor)

    c1_x = 420
    c2_x = 750

    ucs = {
        "uc10": {"name": "UC10: Quản lý danh mục & SP AI", "c": (c2_x, 140), "rx": 105, "ry": 26},
        "uc_vec": {"name": "Đồng bộ Vector Embeddings", "c": (c1_x, 140), "rx": 100, "ry": 26},
        "uc11": {"name": "UC11: Quản lý đơn hàng & Xử lý", "c": (c2_x, 270), "rx": 105, "ry": 26},
        "uc_ship": {"name": "Cập nhật mã vận đơn hãng ship", "c": (c1_x, 270), "rx": 105, "ry": 26},
        "uc12": {"name": "UC12: Quản lý tài khoản & RBAC", "c": (c2_x, 400), "rx": 105, "ry": 26},
        "uc_promo": {"name": "Quản lý khuyến mãi & Giá", "c": (c2_x, 520), "rx": 102, "ry": 26},
        "uc13": {"name": "UC13: Báo cáo & Thống kê AI", "c": (c2_x, 630), "rx": 105, "ry": 26},
    }

    line_color = (135, 145, 160)
    for key in ["uc10", "uc11", "uc12", "uc_promo", "uc13"]:
        cx, cy = ucs[key]["c"]
        rx = ucs[key]["rx"]
        draw.line([pos_admin[0] - 30, pos_admin[1], cx + rx, cy], fill=line_color, width=1)

    draw.line([pos_carrier[0] + 30, pos_carrier[1], ucs["uc_ship"]["c"][0] - ucs["uc_ship"]["rx"], ucs["uc_ship"]["c"][1]], fill=line_color, width=1)

    draw_arrow(draw, ucs["uc10"]["c"][0] - ucs["uc10"]["rx"], ucs["uc10"]["c"][1],
               ucs["uc_vec"]["c"][0] + ucs["uc_vec"]["rx"], ucs["uc_vec"]["c"][1],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    draw_arrow(draw, ucs["uc_ship"]["c"][0] + ucs["uc_ship"]["rx"], ucs["uc_ship"]["c"][1],
               ucs["uc11"]["c"][0] - ucs["uc11"]["rx"], ucs["uc11"]["c"][1],
               is_dashed=True, label="<<extend>>", font_label=f_stereo)

    for key, data in ucs.items():
        cx, cy = data["c"]
        rx, ry = data["rx"], data["ry"]
        draw_ellipse_uc(draw, cx, cy, rx, ry, data["name"], f_uc)

    out_path = r"C:\Net108Khai\usecase_ainative_admin.png"
    img.save(out_path, "PNG")
    print("Generated:", out_path)

# ==================== 4. SƠ ĐỒ PHÂN HỆ TÁC TỬ AI (1150 x 740) ====================
def build_agent_diagram():
    w, h = 1150, 740
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_title, f_box, f_actor, f_uc, f_uc_bold, f_stereo = get_fonts()

    title = "SƠ ĐỒ USE CASE PHÂN HỆ NỀN TẢNG TÁC TỬ AI (AI AGENT PLATFORM)"
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((w - (bb[2]-bb[0]))//2, 18), title, fill=(31, 78, 121), font=f_title)

    bx1, by1, bx2, by2 = 190, 60, 960, 700
    draw.rectangle([bx1, by1, bx2, by2], outline=(70, 80, 95), width=2)
    draw.text((bx1 + 15, by1 + 10), "Phân hệ Tác tử AI (AI Agent Platform Boundary)", fill=(40, 50, 60), font=f_box)

    pos_user = (95, 360)
    pos_agent = (1055, 360)

    draw_actor(draw, pos_user[0], pos_user[1], "Customer /\nExternal Agent", f_actor)
    draw_actor(draw, pos_agent[0], pos_agent[1], "AI Agent\nPlatform", f_actor)

    c1_x = 420
    c2_x = 740

    ucs = {
        "uc_router": {"name": "Định tuyến ý định (Intent Router)", "c": (c1_x, 150), "rx": 105, "ry": 26},
        "uc_rag": {"name": "Tìm kiếm ngữ nghĩa lai (Hybrid RAG)", "c": (c1_x, 290), "rx": 110, "ry": 26},
        "uc14": {"name": "UC14: Giao thức giao dịch ACP", "c": (c1_x, 440), "rx": 105, "ry": 26},
        "uc_cs": {"name": "Chăm sóc khách hàng tự động 24/7", "c": (c1_x, 580), "rx": 110, "ry": 26},

        "uc_token": {"name": "Xác thực Token & Hạn mức", "c": (c2_x, 380), "rx": 100, "ry": 26},
        "uc_otp": {"name": "Xác thực 2FA OTP vượt ngưỡng", "c": (c2_x, 500), "rx": 105, "ry": 26},
    }

    line_color = (135, 145, 160)
    for key in ["uc_router", "uc_rag", "uc14", "uc_cs"]:
        cx, cy = ucs[key]["c"]
        rx = ucs[key]["rx"]
        draw.line([pos_user[0] + 30, pos_user[1], cx - rx, cy], fill=line_color, width=1)
        draw.line([pos_agent[0] - 30, pos_agent[1], cx + rx, cy], fill=line_color, width=1)

    draw_arrow(draw, ucs["uc14"]["c"][0] + ucs["uc14"]["rx"], ucs["uc14"]["c"][1] - 15,
               ucs["uc_token"]["c"][0] - ucs["uc_token"]["rx"], ucs["uc_token"]["c"][1],
               is_dashed=True, label="<<include>>", font_label=f_stereo)

    draw_arrow(draw, ucs["uc_otp"]["c"][0] - ucs["uc_otp"]["rx"], ucs["uc_otp"]["c"][1],
               ucs["uc14"]["c"][0] + ucs["uc14"]["rx"], ucs["uc14"]["c"][1] + 15,
               is_dashed=True, label="<<extend>>", font_label=f_stereo)

    for key, data in ucs.items():
        cx, cy = data["c"]
        rx, ry = data["rx"], data["ry"]
        draw_ellipse_uc(draw, cx, cy, rx, ry, data["name"], f_uc)

    out_path = r"C:\Net108Khai\usecase_ainative_agent.png"
    img.save(out_path, "PNG")
    print("Generated:", out_path)

if __name__ == "__main__":
    build_general_diagram()
    build_customer_diagram()
    build_admin_diagram()
    build_agent_diagram()
    print("ALL 4 ENHANCED USE CASE DIAGRAMS GENERATED SUCCESSFULLY!")
