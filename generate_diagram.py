# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

width, height = 1150, 680
img = Image.new("RGB", (width, height), (255, 255, 255))
draw = ImageDraw.Draw(img)

try:
    font_bold = ImageFont.truetype("arialbd.ttf", 15)
    font_normal = ImageFont.truetype("arial.ttf", 13)
    font_title = ImageFont.truetype("arialbd.ttf", 18)
    font_actor = ImageFont.truetype("arialbd.ttf", 15)
except Exception:
    font_bold = font_normal = font_title = font_actor = ImageFont.load_default()

# Title
title = "SƠ ĐỒ USE CASE TỔNG QUÁT HỆ THỐNG QUẢN LÝ QUÁN CÀ PHÊ"
bbox = draw.textbbox((0, 0), title, font=font_title)
tw = bbox[2] - bbox[0]
draw.text(((width - tw) // 2, 20), title, fill=(31, 78, 121), font=font_title)

# System Boundary Box
box_left, box_top, box_right, box_bottom = 220, 65, 930, 640
draw.rectangle([box_left, box_top, box_right, box_bottom], outline=(60, 75, 95), width=2)
draw.text((box_left + 15, box_top + 10), "Hệ thống Quản lý Quán Cà phê (QuanLyQuanCaPhe)", fill=(60, 60, 60), font=font_bold)

# Use Cases layout
uc_list = [
    # Column 1 (Staff focused)
    {"id": "uc1", "name": "Tạo phiếu bán hàng", "center": (350, 135), "staff": True, "mgr": False},
    {"id": "uc2", "name": "Sửa phiếu bán hàng", "center": (350, 245), "staff": True, "mgr": False},
    {"id": "uc3", "name": "Xem phiếu bán hàng", "center": (350, 360), "staff": True, "mgr": False},
    {"id": "uc4", "name": "Xem danh sách\nhóa đơn cá nhân", "center": (350, 490), "staff": True, "mgr": False},

    # Column 2 (Shared & Menu)
    {"id": "uc5", "name": "Đăng nhập", "center": (575, 125), "staff": True, "mgr": True},
    {"id": "uc6", "name": "Đổi mật khẩu", "center": (575, 205), "staff": True, "mgr": True},
    {"id": "uc7", "name": "Quên mật khẩu", "center": (575, 285), "staff": True, "mgr": True},
    {"id": "uc8", "name": "Sửa thông tin\ncá nhân", "center": (575, 375), "staff": True, "mgr": True},
    {"id": "uc9", "name": "Quản lý\nloại đồ uống", "center": (575, 510), "staff": False, "mgr": True},

    # Column 3 (Manager focused)
    {"id": "uc10", "name": "Quản lý đồ uống", "center": (800, 155), "staff": False, "mgr": True},
    {"id": "uc11", "name": "Quản lý nhân viên", "center": (800, 270), "staff": False, "mgr": True},
    {"id": "uc12", "name": "Quản lý hóa đơn", "center": (800, 395), "staff": False, "mgr": True},
    {"id": "uc13", "name": "Báo cáo thống kê", "center": (800, 520), "staff": False, "mgr": True},
]

def draw_actor(draw, x, y, name):
    # Head
    draw.ellipse([x - 20, y - 60, x + 20, y - 20], outline=(30, 30, 30), width=2, fill=(245, 248, 252))
    # Body
    draw.line([x, y - 20, x, y + 30], fill=(30, 30, 30), width=2)
    # Arms
    draw.line([x - 30, y - 5, x + 30, y - 5], fill=(30, 30, 30), width=2)
    # Legs
    draw.line([x, y + 30, x - 25, y + 75], fill=(30, 30, 30), width=2)
    draw.line([x, y + 30, x + 25, y + 75], fill=(30, 30, 30), width=2)
    # Text
    bbox_a = draw.textbbox((0, 0), name, font=font_actor)
    aw = bbox_a[2] - bbox_a[0]
    draw.text((x - aw // 2, y + 85), name, fill=(31, 78, 121), font=font_actor)

actor_staff_pos = (105, 320)
actor_mgr_pos = (1045, 320)

# Draw Association lines
for uc in uc_list:
    cx, cy = uc["center"]
    if uc["staff"]:
        draw.line([actor_staff_pos[0] + 35, actor_staff_pos[1] - 5, cx - 85, cy], fill=(130, 140, 155), width=1)
    if uc["mgr"]:
        draw.line([actor_mgr_pos[0] - 35, actor_mgr_pos[1] - 5, cx + 85, cy], fill=(130, 140, 155), width=1)

draw_actor(draw, actor_staff_pos[0], actor_staff_pos[1], "Nhân viên")
draw_actor(draw, actor_mgr_pos[0], actor_mgr_pos[1], "Quản lý")

# Draw Use Cases
for uc in uc_list:
    cx, cy = uc["center"]
    rx, ry = 88, 34
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=(46, 117, 182), width=2, fill=(238, 245, 253))
    lines = uc["name"].split("\n")
    if len(lines) == 1:
        bb = draw.textbbox((0, 0), lines[0], font=font_normal)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        draw.text((cx - w // 2, cy - h // 2), lines[0], fill=(20, 30, 50), font=font_normal)
    else:
        bb1 = draw.textbbox((0, 0), lines[0], font=font_normal)
        bb2 = draw.textbbox((0, 0), lines[1], font=font_normal)
        w1, h1 = bb1[2] - bb1[0], bb1[3] - bb1[1]
        w2, h2 = bb2[2] - bb2[0], bb2[3] - bb2[1]
        draw.text((cx - w1 // 2, cy - h1 - 2), lines[0], fill=(20, 30, 50), font=font_normal)
        draw.text((cx - w2 // 2, cy + 3), lines[1], fill=(20, 30, 50), font=font_normal)

out_img = r"C:\Net108Khai\usecase_tongquat.png"
img.save(out_img, "PNG")
print("Saved Use Case diagram successfully at", out_img)
