# -*- coding: utf-8 -*-
"""
Generate publication-quality diagram of the Waterfall Development Model
for FPT Polytechnic NET108 (matching the classroom lecture slide).
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = r"c:\Net108Khai\docs\06-design\waterfall_model_diagram.png"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

FONT_REGULAR_PATH = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_ITALIC_PATH = r"C:\Windows\Fonts\segoeuii.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

font_header_title = get_font(FONT_BOLD_PATH, 24)
font_header_sub = get_font(FONT_REGULAR_PATH, 13)
font_badge_title = get_font(FONT_BOLD_PATH, 19)
font_badge_sub = get_font(FONT_REGULAR_PATH, 14)
font_step_num = get_font(FONT_BOLD_PATH, 20)
font_step_title = get_font(FONT_BOLD_PATH, 17)
font_step_desc = get_font(FONT_REGULAR_PATH, 12)
font_footer = get_font(FONT_REGULAR_PATH, 12)
font_footer_bold = get_font(FONT_BOLD_PATH, 12)

def draw_chevron(draw, x, y, width, height, fill_color, border_color, point_offset=26):
    """Draws a horizontal chevron/arrow polygon pointing right."""
    pts = [
        (x, y),
        (x + width - point_offset, y),
        (x + width, y + height / 2),
        (x + width - point_offset, y + height),
        (x, y + height),
        (x + point_offset, y + height / 2)
    ]
    draw.polygon(pts, fill=fill_color, outline=border_color)

def draw_curved_dashed_arrow(draw, x1, y1, x2, y2, color="#94A3B8"):
    """Draws a gentle curved dashed line connecting steps."""
    steps = 40
    prev_pt = None
    dash_on = True
    dist_accum = 0
    for i in range(steps + 1):
        t = i / steps
        # Quadratic bezier curve with control point
        cx = (x1 + x2) / 2 - 25
        cy = (y1 + y2) / 2 + 10
        px = (1 - t)**2 * x1 + 2 * (1 - t) * t * cx + t**2 * x2
        py = (1 - t)**2 * y1 + 2 * (1 - t) * t * cy + t**2 * y2
        curr_pt = (px, py)
        if prev_pt is not None:
            seg_len = math.hypot(curr_pt[0] - prev_pt[0], curr_pt[1] - prev_pt[1])
            dist_accum += seg_len
            if int(dist_accum // 7) % 2 == 0:
                draw.line([prev_pt, curr_pt], fill=color, width=2)
        prev_pt = curr_pt

    # Arrowhead at end
    angle = math.atan2(y2 - cy, x2 - cx)
    arrow_len = 10
    a1 = (x2 - arrow_len * math.cos(angle - 0.45), y2 - arrow_len * math.sin(angle - 0.45))
    a2 = (x2 - arrow_len * math.cos(angle + 0.45), y2 - arrow_len * math.sin(angle + 0.45))
    draw.polygon([(x2, y2), a1, a2], fill=color)

def main():
    width, height = 1200, 680
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Outer subtle border
    draw.rectangle([0, 0, width - 1, height - 1], outline="#CBD5E1", width=1)

    # Header Bar (Orange/Navy gradient aesthetic matching FPT Poly)
    draw.rectangle([0, 0, width, 68], fill="#EA580C")  # Deep Orange
    draw.rectangle([0, 68, width, 72], fill="#C2410C")
    # Top Text
    draw.text((40, 12), "QUY TRÌNH THỰC HIỆN DỰ ÁN (NET108)", fill="#FFFFFF", font=font_header_title)
    draw.text((40, 42), "Mô Hình Phát Triển Ứng Dụng Thác Nước (Waterfall Model) | FPT Polytechnic", fill="#FFEDD5", font=font_header_sub)
    # Right badge in header
    draw.rounded_rectangle([1030, 18, 1160, 52], radius=6, fill="#C2410C", outline="#FDBA74", width=1)
    draw.text((1045, 27), "Dự Án Mẫu NET108", fill="#FFFFFF", font=font_footer_bold)

    # Right Circle: "Mô hình phát triển ứng dụng Waterfall"
    # Matching the exact circle in the classroom slide
    circle_center = (960, 270)
    circle_radius = 165
    draw.ellipse([circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                  circle_center[0] + circle_radius, circle_center[1] + circle_radius],
                 fill="#F1F5F9", outline="#94A3B8", width=3)
    draw.ellipse([circle_center[0] - circle_radius + 8, circle_center[1] - circle_radius + 8,
                  circle_center[0] + circle_radius - 8, circle_center[1] + circle_radius - 8],
                 fill="#E2E8F0", outline="#CBD5E1", width=1)

    # Text inside circle
    lines_circle = [
        ("Mô hình", font_badge_title, "#334155"),
        ("phát triển ứng dụng", font_badge_title, "#334155"),
        ("WATERFALL", get_font(FONT_BOLD_PATH, 26), "#0F172A"),
        ("(Mô hình Thác nước)", font_badge_sub, "#64748B"),
        ("Đặc điểm: Tuần tự, chặt chẽ,", font_footer, "#475569"),
        ("đầu ra giai đoạn này là", font_footer, "#475569"),
        ("đầu vào của giai đoạn sau.", font_footer, "#475569")
    ]
    cy = circle_center[1] - 85
    for text, f, col in lines_circle:
        bbox = f.getbbox(text)
        tw = bbox[2] - bbox[0]
        draw.text((circle_center[0] - tw / 2, cy), text, fill=col, font=f)
        cy += 24 if f == font_footer else (30 if f != get_font(FONT_BOLD_PATH, 26) else 34)

    # 5 Waterfall Steps (Staircase from top-left downwards)
    steps_data = [
        {
            "num": "1",
            "title": "Requirements Analysis",
            "vn_title": "Phân tích yêu cầu",
            "desc": "Khảo sát AI Deepsearch, phân tích Actor, lập đặc tả SRS, sơ đồ Use Case tổng quát & 14 Use Case chi tiết.",
            "deliverable": "Sản phẩm bàn giao: Tài liệu SRS, Sơ đồ Use Case UML (Trọng tâm Lab 1)",
            "fill": "#F59E0B",      # Amber/Orange
            "dark_fill": "#D97706",
            "x": 60, "y": 105, "w": 650, "h": 85
        },
        {
            "num": "2",
            "title": "Design",
            "vn_title": "Thiết kế hệ thống",
            "desc": "Thiết kế Deploy Diagram, Appmap, Tech Stack phân tầng, Conceptual ERD, UI Wireframes & Controller.",
            "deliverable": "Sản phẩm bàn giao: Bản vẽ kiến trúc, ERD CSDL, UI Wireframe (Trọng tâm Lab 1 & 2)",
            "fill": "#10B981",      # Emerald Green
            "dark_fill": "#059669",
            "x": 115, "y": 210, "w": 650, "h": 85
        },
        {
            "num": "3",
            "title": "Development",
            "vn_title": "Phát triển & Lập trình",
            "desc": "Xây dựng Backend REST API (Node.js/Prisma), AI RAG & MCP Server (FastAPI), Web Frontend (React/Next.js).",
            "deliverable": "Sản phẩm bàn giao: Mã nguồn Backend, Frontend & AI Services (Trọng tâm Lab 3 & 4)",
            "fill": "#EF4444",      # Red
            "dark_fill": "#DC2626",
            "x": 170, "y": 315, "w": 650, "h": 85
        },
        {
            "num": "4",
            "title": "Testing",
            "vn_title": "Kiểm thử phần mềm",
            "desc": "Kiểm thử chức năng, tích hợp theo ma trận Test Cases P0/P1, kiểm thử AI Agent và xử lý lỗi phần mềm.",
            "deliverable": "Sản phẩm bàn giao: Báo cáo Test Cases, Test Run Evidence (Trọng tâm Lab 4 & Assignment)",
            "fill": "#8B5CF6",      # Purple
            "dark_fill": "#7C3AED",
            "x": 225, "y": 420, "w": 650, "h": 85
        },
        {
            "num": "5",
            "title": "Maintenance",
            "vn_title": "Triển khai & Bảo trì",
            "desc": "Đóng gói Docker Container, thiết lập đường ống CI/CD, triển khai Cloud Hosting và giám sát vận hành.",
            "deliverable": "Sản phẩm bàn giao: Dockerfile, CI/CD Pipeline, Hướng dẫn cài đặt & Vận hành",
            "fill": "#3B82F6",      # Blue
            "dark_fill": "#2563EB",
            "x": 280, "y": 525, "w": 650, "h": 85
        }
    ]

    # Draw steps
    for idx, s in enumerate(steps_data):
        x, y, w, h = s["x"], s["y"], s["w"], s["h"]
        
        # Draw chevron shape
        draw_chevron(draw, x, y, w, h, s["fill"], s["dark_fill"], point_offset=26)

        # Number badge (white hexagon/rounded rect on left)
        badge_w, badge_h = 42, 42
        bx = x + 34
        by = y + (h - badge_h) / 2
        draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=8, fill="#FFFFFF", outline=s["dark_fill"], width=2)
        # Number text
        nb_box = font_step_num.getbbox(s["num"])
        nw = nb_box[2] - nb_box[0]
        draw.text((bx + (badge_w - nw) / 2, by + 7), s["num"], fill=s["dark_fill"], font=font_step_num)

        # Text inside chevron
        tx = bx + badge_w + 16
        # Title: English + Vietnamese
        full_title = f"{s['title']} ({s['vn_title']})"
        draw.text((tx, y + 10), full_title, fill="#FFFFFF", font=font_step_title)
        # Description
        draw.text((tx, y + 36), s["desc"], fill="#F8FAFC", font=font_step_desc)
        # Deliverable note (italicized/highlighted)
        draw.text((tx, y + 56), s["deliverable"], fill="#FEF3C7", font=font_step_desc)

        # Draw connecting curved dashed arrow to next step
        if idx < len(steps_data) - 1:
            next_s = steps_data[idx + 1]
            ax1 = x + 120
            ay1 = y + h
            ax2 = next_s["x"] + 55
            ay2 = next_s["y"]
            draw_curved_dashed_arrow(draw, ax1, ay1, ax2, ay2, color="#64748B")

    # Bottom Footer Legend
    draw.rectangle([0, 630, width, height], fill="#F8FAFC")
    draw.line([0, 630, width, 630], fill="#E2E8F0", width=1)
    footer_text = "Ghi chú: Mô hình Thác nước (Waterfall) yêu cầu hoàn tất 100% phê duyệt kết quả đầu ra của từng giai đoạn trước khi chuyển sang giai đoạn kế tiếp. Toàn bộ tiến độ dự án được giám sát qua Jira Cloud (thientptb02226.atlassian.net - Project NET108)."
    draw.text((40, 645), footer_text, fill="#475569", font=font_footer)

    img.save(OUTPUT_PATH, quality=95)
    print("Successfully generated Waterfall diagram at:", OUTPUT_PATH)

if __name__ == "__main__":
    main()

