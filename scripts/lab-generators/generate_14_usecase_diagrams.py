# -*- coding: utf-8 -*-
"""
Generate 14 individual, highly-detailed, publication-quality UML Use Case diagrams
for UC01 to UC14 of the AI-Native Commerce project (FPT Polytechnic NET108).
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"c:\Net108Khai\docs\06-design\use-cases"
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
font_subtitle = get_font(FONT_REGULAR_PATH, 13)
font_actor_name = get_font(FONT_BOLD_PATH, 15)
font_actor_badge = get_font(FONT_ITALIC_PATH, 12)
font_main_uc = get_font(FONT_BOLD_PATH, 15)
font_sub_uc = get_font(FONT_REGULAR_PATH, 13)
font_arrow_label = get_font(FONT_BOLD_PATH, 11)
font_legend = get_font(FONT_REGULAR_PATH, 12)
font_boundary = get_font(FONT_BOLD_PATH, 13)

def draw_header(draw, title, subtitle):
    # Header bar
    draw.rectangle([0, 0, 1200, 65], fill="#1F4E79")
    draw.line([0, 65, 1200, 65], fill="#0F2D4A", width=2)
    # Title & subtitle
    draw.text((35, 12), title, fill="#FFFFFF", font=font_title)
    draw.text((35, 39), subtitle, fill="#D9E1F2", font=font_subtitle)
    # Decorative badge on the right
    draw.rounded_rectangle([1030, 15, 1165, 48], radius=6, fill="#2F5597", outline="#8EA9DB", width=1)
    draw.text((1045, 23), "UML 2.5 Standard", fill="#FFFFFF", font=font_arrow_label)

def draw_actor(draw, x, y, name_lines, badge_text, is_system=False):
    if not is_system:
        # Stick figure
        # Head
        draw.ellipse([x - 16, y - 60, x + 16, y - 28], fill="#FFFFFF", outline="#1E293B", width=2)
        # Body
        draw.line([x, y - 28, x, y + 25], fill="#1E293B", width=2)
        # Arms
        draw.line([x - 30, y - 10, x + 30, y - 10], fill="#1E293B", width=2)
        # Legs
        draw.line([x, y + 25, x - 22, y + 65], fill="#1E293B", width=2)
        draw.line([x, y + 25, x + 22, y + 65], fill="#1E293B", width=2)
    else:
        # System / External Actor icon (Box with gear/server aesthetic)
        draw.rounded_rectangle([x - 36, y - 55, x + 36, y + 20], radius=8, fill="#F1F5F9", outline="#334155", width=2)
        # Inner server lines
        draw.rectangle([x - 26, y - 45, x + 26, y - 35], fill="#CBD5E1", outline="#64748B", width=1)
        draw.rectangle([x - 26, y - 28, x + 26, y - 18], fill="#CBD5E1", outline="#64748B", width=1)
        draw.rectangle([x - 26, y - 11, x + 26, y - 1], fill="#CBD5E1", outline="#64748B", width=1)
        # Small green led dots
        draw.ellipse([x + 16, y - 42, x + 22, y - 38], fill="#10B981")
        draw.ellipse([x + 16, y - 25, x + 22, y - 21], fill="#10B981")
        draw.ellipse([x + 16, y - 8, x + 22, y - 4], fill="#10B981")

    # Name text
    text_y = y + 72 if not is_system else y + 28
    for line in name_lines:
        bbox = font_actor_name.getbbox(line)
        w = bbox[2] - bbox[0]
        draw.text((x - w / 2, text_y), line, fill="#0F172A", font=font_actor_name)
        text_y += 18
    # Badge
    bbox = font_actor_badge.getbbox(badge_text)
    w = bbox[2] - bbox[0]
    draw.rounded_rectangle([x - w / 2 - 8, text_y + 4, x + w / 2 + 8, text_y + 22], radius=4, fill="#E2E8F0")
    draw.text((x - w / 2, text_y + 5), badge_text, fill="#475569", font=font_actor_badge)

def draw_oval(draw, cx, cy, rx, ry, fill_color, border_color, border_width, text_lines, font, text_color):
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill_color, outline=border_color, width=border_width)
    total_h = len(text_lines) * 18
    start_y = cy - total_h / 2 + 2
    for line in text_lines:
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        draw.text((cx - w / 2, start_y), line, fill=text_color, font=font)
        start_y += 18

def draw_dashed_arrow(draw, x1, y1, x2, y2, color, label="<<include>>"):
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux = dx / dist
    uy = dy / dist

    # Draw dashed line
    dash_len = 7
    gap_len = 5
    curr = 0
    while curr < dist - 10:
        p1 = (x1 + ux * curr, y1 + uy * curr)
        seg_end = min(curr + dash_len, dist - 10)
        p2 = (x1 + ux * seg_end, y1 + uy * seg_end)
        draw.line([p1, p2], fill=color, width=2)
        curr += dash_len + gap_len

    # Open arrowhead at (x2, y2)
    arrow_len = 12
    arrow_angle = 0.45
    angle = math.atan2(dy, dx)
    ax1 = x2 - arrow_len * math.cos(angle - arrow_angle)
    ay1 = y2 - arrow_len * math.sin(angle - arrow_angle)
    ax2 = x2 - arrow_len * math.cos(angle + arrow_angle)
    ay2 = y2 - arrow_len * math.sin(angle + arrow_angle)
    draw.line([(x2, y2), (ax1, ay1)], fill=color, width=2)
    draw.line([(x2, y2), (ax2, ay2)], fill=color, width=2)

    # Label on white pill background
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    bbox = font_arrow_label.getbbox(label)
    lw = bbox[2] - bbox[0]
    lh = bbox[3] - bbox[1]
    draw.rounded_rectangle([mx - lw/2 - 5, my - lh/2 - 3, mx + lw/2 + 5, my + lh/2 + 3], radius=3, fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((mx - lw / 2, my - lh / 2 - 1), label, fill=color, font=font_arrow_label)

def draw_solid_association(draw, x1, y1, x2, y2, color="#334155"):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=2)

def draw_legend(draw):
    y = 670
    draw.line([30, y - 5, 1170, y - 5], fill="#E2E8F0", width=1)
    # Legend items
    draw.text((45, y + 8), "Ghi chú UML:", fill="#0F172A", font=font_legend)
    
    # 1. Association
    draw.line([145, y + 16, 185, y + 16], fill="#334155", width=2)
    draw.text((195, y + 8), "Tương tác trực tiếp (Association)", fill="#475569", font=font_legend)
    
    # 2. Include
    draw_dashed_arrow(draw, 420, y + 16, 465, y + 16, "#1E40AF", "<<include>>")
    draw.text((475, y + 8), "Bắt buộc thực thi (Include)", fill="#475569", font=font_legend)
    
    # 3. Extend
    draw_dashed_arrow(draw, 680, y + 16, 725, y + 16, "#B45309", "<<extend>>")
    draw.text((735, y + 8), "Mở rộng / Rẽ nhánh (Extend)", fill="#475569", font=font_legend)

    # 4. Color boxes
    draw.ellipse([935, y + 9, 950, y + 23], fill="#DBEAFE", outline="#1E40AF", width=1)
    draw.text((955, y + 8), "Chính", fill="#475569", font=font_legend)
    draw.ellipse([1005, y + 9, 1020, y + 23], fill="#E0F2FE", outline="#0284C7", width=1)
    draw.text((1025, y + 8), "Include", fill="#475569", font=font_legend)
    draw.ellipse([1080, y + 9, 1095, y + 23], fill="#FEF3C7", outline="#D97706", width=1)
    draw.text((1100, y + 8), "Extend", fill="#475569", font=font_legend)

USE_CASES_DATA = [
    {
        "id": "UC01",
        "filename": "usecase_detail_uc01_register.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC01 - ĐĂNG KÝ TÀI KHOẢN (REGISTER)",
        "subtitle": "Phân hệ Khách hàng (Guest & Customer) | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["Guest", "(Khách vãng lai)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["OTP / Mail Service", "(SMS Gateway)"], "badge": "<<External Service>>", "system": True},
        "main_uc": {"text": ["Đăng ký", "tài khoản mới"], "cx": 480, "cy": 330, "rx": 105, "ry": 48},
        "includes": [
            {"text": ["Nhập thông tin", "& mật khẩu hợp lệ"], "cx": 780, "cy": 200, "rx": 100, "ry": 42, "to_right": False},
            {"text": ["Kiểm tra tính hợp lệ", "& trùng lặp Email/SĐT"], "cx": 780, "cy": 330, "rx": 105, "ry": 44, "to_right": False},
            {"text": ["Gửi mã OTP", "xác thực kích hoạt"], "cx": 780, "cy": 460, "rx": 100, "ry": 42, "to_right": True},
        ],
        "extends": [
            {"text": ["Đăng ký nhanh bằng", "Google OAuth 2.0"], "cx": 370, "cy": 510, "rx": 100, "ry": 42},
            {"text": ["Báo lỗi tài khoản", "đã tồn tại trên hệ thống"], "cx": 590, "cy": 510, "rx": 100, "ry": 42},
        ]
    },
    {
        "id": "UC02",
        "filename": "usecase_detail_uc02_login.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC02 - ĐĂNG NHẬP HỆ THỐNG (LOGIN)",
        "subtitle": "Phân hệ Dùng chung | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["User", "(Customer / Admin)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["JWT Auth Gateway", "(Redis Token Store)"], "badge": "<<External Service>>", "system": True},
        "main_uc": {"text": ["Đăng nhập", "hệ thống"], "cx": 480, "cy": 330, "rx": 105, "ry": 48},
        "includes": [
            {"text": ["Nhập Email", "& Mật khẩu"], "cx": 780, "cy": 200, "rx": 95, "ry": 40, "to_right": False},
            {"text": ["Xác thực tài khoản", "với Bcrypt Hash"], "cx": 780, "cy": 330, "rx": 105, "ry": 44, "to_right": True},
            {"text": ["Cấp Access Token", "& Refresh Token"], "cx": 780, "cy": 460, "rx": 100, "ry": 42, "to_right": True},
        ],
        "extends": [
            {"text": ["Đăng nhập qua", "Google Single Sign-On"], "cx": 370, "cy": 510, "rx": 100, "ry": 42},
            {"text": ["Ghi nhớ phiên", "đăng nhập (Remember Me)"], "cx": 590, "cy": 510, "rx": 100, "ry": 42},
        ]
    },
    {
        "id": "UC03",
        "filename": "usecase_detail_uc03_forgot_pwd.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC03 - QUÊN MẬT KHẨU (FORGOT PASSWORD)",
        "subtitle": "Phân hệ Tài khoản & Xác thực | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["User", "(Người dùng)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["Email Service", "(SMTP / SendGrid)"], "badge": "<<External Service>>", "system": True},
        "main_uc": {"text": ["Khôi phục", "mật khẩu"], "cx": 480, "cy": 330, "rx": 105, "ry": 48},
        "includes": [
            {"text": ["Nhập Email", "xác minh tài khoản"], "cx": 780, "cy": 200, "rx": 100, "ry": 40, "to_right": False},
            {"text": ["Tạo & Gửi liên kết", "OTP đặt lại mật khẩu"], "cx": 780, "cy": 330, "rx": 105, "ry": 44, "to_right": True},
            {"text": ["Thiết lập mật khẩu", "mới & Lưu Bcrypt Hash"], "cx": 780, "cy": 460, "rx": 105, "ry": 42, "to_right": False},
        ],
        "extends": [
            {"text": ["Báo lỗi Email", "không tồn tại"], "cx": 370, "cy": 510, "rx": 95, "ry": 40},
            {"text": ["Hủy yêu cầu &", "quay lại Đăng nhập"], "cx": 590, "cy": 510, "rx": 100, "ry": 40},
        ]
    },
    {
        "id": "UC04",
        "filename": "usecase_detail_uc04_nlp_search.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC04 - TÌM KIẾM BẰNG NGÔN NGỮ TỰ NHIÊN (NLP SEARCH)",
        "subtitle": "Phân hệ Mua sắm Thông minh | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["Customer", "(Khách mua hàng)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["AI Vector Database", "(pgvector / ChromaDB)"], "badge": "<<AI Engine>>", "system": True},
        "main_uc": {"text": ["Tìm kiếm sản phẩm", "bằng ngôn ngữ tự nhiên"], "cx": 480, "cy": 330, "rx": 115, "ry": 50},
        "includes": [
            {"text": ["Nhập câu truy vấn", "ngữ nghĩa (Semantic)"], "cx": 780, "cy": 200, "rx": 100, "ry": 40, "to_right": False},
            {"text": ["Trích xuất ý định", "& sinh Vector Embedding"], "cx": 780, "cy": 330, "rx": 105, "ry": 44, "to_right": False},
            {"text": ["Tìm kiếm tương đồng", "Cosine Distance"], "cx": 780, "cy": 460, "rx": 100, "ry": 42, "to_right": True},
        ],
        "extends": [
            {"text": ["Tìm kiếm đa phương thức", "bằng hình ảnh (Multimodal)"], "cx": 370, "cy": 510, "rx": 105, "ry": 42},
            {"text": ["Lọc theo mức giá,", "thương hiệu & đánh giá"], "cx": 590, "cy": 510, "rx": 100, "ry": 42},
        ]
    },
    {
        "id": "UC05",
        "filename": "usecase_detail_uc05_ai_assistant.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC05 - TƯƠNG TÁC VỚI AI SHOPPING ASSISTANT",
        "subtitle": "Phân hệ Tác tử Trí tuệ Nhân tạo | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["Customer", "(Khách hàng)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["Gemini 1.5 Pro / Flash", "(RAG Knowledge Base)"], "badge": "<<AI Engine>>", "system": True},
        "main_uc": {"text": ["Tư vấn mua sắm", "với AI Assistant"], "cx": 480, "cy": 330, "rx": 110, "ry": 50},
        "includes": [
            {"text": ["Gửi yêu cầu / câu hỏi", "văn bản hoặc giọng nói"], "cx": 780, "cy": 200, "rx": 100, "ry": 40, "to_right": False},
            {"text": ["Phân tích ngữ cảnh", "& truy vấn dữ liệu RAG"], "cx": 780, "cy": 330, "rx": 105, "ry": 44, "to_right": True},
            {"text": ["Đề xuất sản phẩm", "kèm giải thích lý do"], "cx": 780, "cy": 460, "rx": 100, "ry": 42, "to_right": False},
        ],
        "extends": [
            {"text": ["Thêm trực tiếp sản phẩm", "được gợi ý vào giỏ hàng"], "cx": 370, "cy": 510, "rx": 105, "ry": 42},
            {"text": ["Chuyển tiếp hỗ trợ", "nhân viên tư vấn (Handoff)"], "cx": 590, "cy": 510, "rx": 100, "ry": 42},
        ]
    },
    {
        "id": "UC06",
        "filename": "usecase_detail_uc06_smart_cart.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC06 - QUẢN LÝ GIỎ HÀNG THÔNG MINH (SMART CART)",
        "subtitle": "Phân hệ Mua sắm & Giỏ hàng | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["Customer", "(Khách hàng)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["Inventory & Recommendation", "Service (Kho hàng)"], "badge": "<<Core Service>>", "system": True},
        "main_uc": {"text": ["Quản lý giỏ hàng", "thông minh"], "cx": 480, "cy": 330, "rx": 105, "ry": 48},
        "includes": [
            {"text": ["Thêm / Sửa / Xóa", "sản phẩm trong giỏ"], "cx": 780, "cy": 200, "rx": 95, "ry": 40, "to_right": False},
            {"text": ["Kiểm tra số lượng", "tồn kho thời gian thực"], "cx": 780, "cy": 330, "rx": 100, "ry": 42, "to_right": True},
            {"text": ["Tính toán tạm tính,", "thuế & chiết khấu"], "cx": 780, "cy": 460, "rx": 100, "ry": 42, "to_right": False},
        ],
        "extends": [
            {"text": ["AI gợi ý combo", "sản phẩm tiết kiệm"], "cx": 370, "cy": 510, "rx": 100, "ry": 42},
            {"text": ["Lưu sản phẩm vào", "danh sách mua sau"], "cx": 590, "cy": 510, "rx": 100, "ry": 42},
        ]
    },
    {
        "id": "UC07",
        "filename": "usecase_detail_uc07_checkout.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC07 - ĐẶT HÀNG & ÁP DỤNG KHUYẾN MÃI TỰ ĐỘNG",
        "subtitle": "Phân hệ Đặt hàng & Khuyến mãi | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["Customer", "(Khách hàng)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["Promotion Engine", "(Auto Coupon Match)"], "badge": "<<Core Service>>", "system": True},
        "main_uc": {"text": ["Đặt hàng &", "Áp khuyến mãi"], "cx": 480, "cy": 330, "rx": 105, "ry": 48},
        "includes": [
            {"text": ["Xác nhận danh sách", "hàng hóa & địa chỉ nhận"], "cx": 780, "cy": 180, "rx": 100, "ry": 40, "to_right": False},
            {"text": ["Tối ưu mã giảm giá", "tốt nhất bằng AI"], "cx": 780, "cy": 300, "rx": 100, "ry": 42, "to_right": True},
            {"text": ["Kiểm tra giữ chỗ", "tồn kho (Hold Stock)"], "cx": 780, "cy": 420, "rx": 100, "ry": 40, "to_right": False},
            {"text": ["Tạo đơn hàng mới", "trạng thái PENDING"], "cx": 780, "cy": 530, "rx": 100, "ry": 40, "to_right": False},
        ],
        "extends": [
            {"text": ["Nhập ghi chú đặc biệt", "cho người giao hàng"], "cx": 370, "cy": 510, "rx": 100, "ry": 40},
            {"text": ["Hủy đơn hàng", "khi đang tạo"], "cx": 550, "cy": 510, "rx": 90, "ry": 40},
        ]
    },
    {
        "id": "UC08",
        "filename": "usecase_detail_uc08_payment.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC08 - THANH TOÁN TRỰC TUYẾN (ONLINE PAYMENT)",
        "subtitle": "Phân hệ Thanh toán & Giao dịch | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["Customer", "(Khách hàng)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["Payment Gateway", "(VNPay / MoMo / VietQR)"], "badge": "<<Payment Service>>", "system": True},
        "main_uc": {"text": ["Thanh toán", "trực tuyến"], "cx": 480, "cy": 330, "rx": 105, "ry": 48},
        "includes": [
            {"text": ["Chọn phương thức", "thanh toán (QR / Thẻ)"], "cx": 780, "cy": 200, "rx": 100, "ry": 40, "to_right": False},
            {"text": ["Khởi tạo giao dịch", "& Sinh cổng thanh toán"], "cx": 780, "cy": 330, "rx": 100, "ry": 42, "to_right": True},
            {"text": ["Xác nhận Webhook IPN", "& Cập nhật trạng thái PAID"], "cx": 780, "cy": 460, "rx": 105, "ry": 44, "to_right": True},
        ],
        "extends": [
            {"text": ["Thanh toán khi nhận", "hàng trực tiếp (COD)"], "cx": 370, "cy": 510, "rx": 100, "ry": 42},
            {"text": ["Xử lý giao dịch lỗi", "& Hướng dẫn thử lại"], "cx": 590, "cy": 510, "rx": 100, "ry": 42},
        ]
    },
    {
        "id": "UC09",
        "filename": "usecase_detail_uc09_order_tracking.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC09 - TRA CỨU ĐƠN HÀNG VÀ THEO DÕI VẬN CHUYỂN",
        "subtitle": "Phân hệ Đơn hàng & Vận chuyển | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["Customer", "(Khách hàng)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["Logistics Carrier API", "(GHN / GHTK Webhook)"], "badge": "<<Carrier Service>>", "system": True},
        "main_uc": {"text": ["Tra cứu &", "theo dõi đơn hàng"], "cx": 480, "cy": 330, "rx": 105, "ry": 48},
        "includes": [
            {"text": ["Xem lịch sử & danh sách", "đơn hàng cá nhân"], "cx": 780, "cy": 200, "rx": 100, "ry": 40, "to_right": False},
            {"text": ["Truy vấn lộ trình giao hàng", "theo thời gian thực"], "cx": 780, "cy": 330, "rx": 105, "ry": 42, "to_right": True},
            {"text": ["Nhận thông báo cập nhật", "trạng thái vận chuyển"], "cx": 780, "cy": 460, "rx": 105, "ry": 42, "to_right": False},
        ],
        "extends": [
            {"text": ["Yêu cầu hủy đơn", "khi đang PENDING"], "cx": 370, "cy": 510, "rx": 95, "ry": 40},
            {"text": ["Đánh giá & để lại nhận xét", "sau khi nhận hàng"], "cx": 590, "cy": 510, "rx": 105, "ry": 42},
        ]
    },
    {
        "id": "UC10",
        "filename": "usecase_detail_uc10_product_mgmt.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC10 - QUẢN LÝ SẢN PHẨM & CHUẨN HÓA AI",
        "subtitle": "Phân hệ Quản trị & Nhà bán hàng | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["Merchant / Admin", "(Quản trị viên)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["AI Embedding Worker", "(FastAPI / LangChain)"], "badge": "<<AI Service>>", "system": True},
        "main_uc": {"text": ["Quản lý sản phẩm", "& chuẩn hóa AI"], "cx": 480, "cy": 330, "rx": 105, "ry": 48},
        "includes": [
            {"text": ["Thêm / Sửa / Xóa", "thông tin sản phẩm"], "cx": 780, "cy": 200, "rx": 95, "ry": 40, "to_right": False},
            {"text": ["Phân loại danh mục đa cấp", "& thuộc tính kỹ thuật"], "cx": 780, "cy": 330, "rx": 105, "ry": 44, "to_right": False},
            {"text": ["Tự động sinh Vector Embedding", "& Metadata chuẩn cho AI"], "cx": 780, "cy": 460, "rx": 110, "ry": 44, "to_right": True},
        ],
        "extends": [
            {"text": ["Cập nhật nhanh giá", "& tồn kho hàng loạt"], "cx": 370, "cy": 510, "rx": 100, "ry": 42},
            {"text": ["Nhập / Xuất danh sách", "sản phẩm qua Excel/CSV"], "cx": 590, "cy": 510, "rx": 100, "ry": 42},
        ]
    },
    {
        "id": "UC11",
        "filename": "usecase_detail_uc11_order_mgmt.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC11 - QUẢN LÝ ĐƠN HÀNG VÀ TRẠNG THÁI",
        "subtitle": "Phân hệ Vận hành & Quản lý | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["Merchant / Admin", "(Nhân viên bán hàng)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["Shipping Carrier API", "(Đơn vị vận chuyển)"], "badge": "<<Logistics Service>>", "system": True},
        "main_uc": {"text": ["Quản lý & xử lý", "đơn hàng"], "cx": 480, "cy": 330, "rx": 105, "ry": 48},
        "includes": [
            {"text": ["Tiếp nhận & Xác nhận", "đơn hàng mới"], "cx": 780, "cy": 180, "rx": 95, "ry": 40, "to_right": False},
            {"text": ["Chuyển trạng thái đơn:", "Đóng gói -> Đang giao"], "cx": 780, "cy": 300, "rx": 100, "ry": 42, "to_right": False},
            {"text": ["Đẩy thông tin vận đơn", "sang đối tác vận chuyển"], "cx": 780, "cy": 420, "rx": 105, "ry": 42, "to_right": True},
            {"text": ["In phiếu đóng gói &", "vận đơn giao hàng"], "cx": 780, "cy": 530, "rx": 100, "ry": 40, "to_right": False},
        ],
        "extends": [
            {"text": ["Xác nhận hủy đơn &", "kích hoạt hoàn tiền"], "cx": 370, "cy": 510, "rx": 100, "ry": 40},
            {"text": ["Tiếp nhận & xử lý", "khiếu nại đổi trả hàng"], "cx": 550, "cy": 510, "rx": 100, "ry": 40},
        ]
    },
    {
        "id": "UC12",
        "filename": "usecase_detail_uc12_rbac_mgmt.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC12 - QUẢN LÝ TÀI KHOẢN VÀ PHÂN QUYỀN RBAC",
        "subtitle": "Phân hệ Bảo mật & Quản trị Hệ thống | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["Super Admin", "(Quản trị cấp cao)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["RBAC Policy Engine", "(Authorization Guard)"], "badge": "<<Security Service>>", "system": True},
        "main_uc": {"text": ["Quản lý tài khoản", "& phân quyền RBAC"], "cx": 480, "cy": 330, "rx": 110, "ry": 50},
        "includes": [
            {"text": ["Xem danh sách tài khoản", "& trạng thái kích hoạt"], "cx": 780, "cy": 200, "rx": 100, "ry": 40, "to_right": False},
            {"text": ["Gán vai trò người dùng", "(SuperAdmin, Merchant, User)"], "cx": 780, "cy": 330, "rx": 105, "ry": 44, "to_right": False},
            {"text": ["Thiết lập ma trận quyền hạn", "Permissions chi tiết"], "cx": 780, "cy": 460, "rx": 105, "ry": 42, "to_right": True},
        ],
        "extends": [
            {"text": ["Khóa / Mở khóa tài khoản", "nghi ngờ vi phạm"], "cx": 370, "cy": 510, "rx": 100, "ry": 42},
            {"text": ["Truy vấn nhật ký hoạt động", "kiểm toán (Audit Logs)"], "cx": 590, "cy": 510, "rx": 105, "ry": 42},
        ]
    },
    {
        "id": "UC13",
        "filename": "usecase_detail_uc13_analytics.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC13 - BÁO CÁO THỐNG KÊ & PHÂN TÍCH HÀNH VI AI",
        "subtitle": "Phân hệ Thông minh Kinh doanh (BI) | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["Merchant / Admin", "(Nhà quản lý)"], "badge": "<<Primary Actor>>", "system": False},
        "right_actor": {"name": ["AI Analytics Engine", "(Data Warehouse / ClickHouse)"], "badge": "<<BI Engine>>", "system": True},
        "main_uc": {"text": ["Báo cáo thống kê &", "phân tích hành vi AI"], "cx": 480, "cy": 330, "rx": 110, "ry": 50},
        "includes": [
            {"text": ["Thống kê doanh thu,", "đơn hàng & tồn kho"], "cx": 780, "cy": 200, "rx": 100, "ry": 40, "to_right": False},
            {"text": ["Báo cáo xu hướng tìm kiếm", "& từ khóa nổi bật của AI"], "cx": 780, "cy": 330, "rx": 105, "ry": 44, "to_right": True},
            {"text": ["Đo lường tỷ lệ chuyển đổi", "mua hàng qua AI Assistant"], "cx": 780, "cy": 460, "rx": 105, "ry": 42, "to_right": False},
        ],
        "extends": [
            {"text": ["Xuất báo cáo chi tiết", "ra file Excel / PDF"], "cx": 370, "cy": 510, "rx": 100, "ry": 42},
            {"text": ["Dự báo nhu cầu nhập hàng", "bằng Machine Learning"], "cx": 590, "cy": 510, "rx": 105, "ry": 42},
        ]
    },
    {
        "id": "UC14",
        "filename": "usecase_detail_uc14_ai_agent_tx.png",
        "title": "SƠ ĐỒ USE CASE CHI TIẾT: UC14 - THỰC THI GIAO DỊCH QUA GIAO THỨC TÁC TỬ AI",
        "subtitle": "Phân hệ Giao dịch Tự hành Tác tử | Hệ thống Thương Mại Điện Tử AI-Native Commerce",
        "left_actor": {"name": ["External AI Agent", "(Tác tử mua sắm AI)"], "badge": "<<AI Autonomous Actor>>", "system": False},
        "right_actor": {"name": ["AI Guardrails & Settlement", "(Chính sách an toàn giao dịch)"], "badge": "<<Safety Engine>>", "system": True},
        "main_uc": {"text": ["Thực thi giao dịch", "qua Agent Protocol"], "cx": 480, "cy": 330, "rx": 110, "ry": 50},
        "includes": [
            {"text": ["Xác thực định danh tác tử", "& khóa API Key"], "cx": 780, "cy": 180, "rx": 100, "ry": 40, "to_right": False},
            {"text": ["Kiểm tra hạn mức ngân sách", "chi tiêu (Budget Cap)"], "cx": 780, "cy": 300, "rx": 105, "ry": 42, "to_right": False},
            {"text": ["Kiểm duyệt qua bộ lọc", "an toàn (AI Guardrails)"], "cx": 780, "cy": 420, "rx": 105, "ry": 42, "to_right": True},
            {"text": ["Quyết toán giao dịch", "& sinh chứng thực tự hành"], "cx": 780, "cy": 530, "rx": 105, "ry": 40, "to_right": False},
        ],
        "extends": [
            {"text": ["Chặn giao dịch khi vi phạm", "hạn mức hoặc quy tắc an toàn"], "cx": 370, "cy": 510, "rx": 110, "ry": 42},
            {"text": ["Yêu cầu xác nhận thủ công", "từ chủ tài khoản (HITL)"], "cx": 590, "cy": 510, "rx": 105, "ry": 42},
        ]
    }
]

def render_diagram(data):
    img = Image.new("RGB", (1200, 720), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # 1. Outer subtle border
    draw.rectangle([0, 0, 1199, 719], outline="#CBD5E1", width=1)

    # 2. Header
    draw_header(draw, data["title"], data["subtitle"])

    # 3. System Boundary Box
    # x: 250 to 950, y: 85 to 650
    draw.rounded_rectangle([250, 85, 950, 650], radius=10, fill="#F8FAFC", outline="#94A3B8", width=2)
    # Boundary title
    draw.rounded_rectangle([265, 75, 595, 102], radius=4, fill="#FFFFFF", outline="#94A3B8", width=1)
    draw.text((275, 80), "Hệ thống AI-Native Commerce (System Boundary)", fill="#1E293B", font=font_boundary)

    # 4. Left Actor
    la = data["left_actor"]
    draw_actor(draw, 125, 290, la["name"], la["badge"], la.get("system", False))

    # 5. Right Actor
    ra = data["right_actor"]
    draw_actor(draw, 1075, 290, ra["name"], ra["badge"], ra.get("system", True))

    # 6. Main UC
    muc = data["main_uc"]
    # Draw association from Left Actor to Main UC
    draw_solid_association(draw, 155, 280, muc["cx"] - muc["rx"], muc["cy"], "#334155")
    # Draw Main UC
    draw_oval(draw, muc["cx"], muc["cy"], muc["rx"], muc["ry"], "#DBEAFE", "#1E40AF", 3, muc["text"], font_main_uc, "#1E3A8A")

    # 7. Includes
    incs = data["includes"]
    has_four = len(incs) == 4
    for inc in incs:
        # Arrow from Main UC to Inc UC
        # Compute start and end points
        # Start at right edge of Main UC
        sx = muc["cx"] + muc["rx"] * 0.8
        sy = muc["cy"] + (inc["cy"] - muc["cy"]) * 0.45
        ex = inc["cx"] - inc["rx"]
        ey = inc["cy"]
        draw_dashed_arrow(draw, sx, sy, ex, ey, "#1E40AF", "<<include>>")
        
        # Draw Inc UC
        draw_oval(draw, inc["cx"], inc["cy"], inc["rx"], inc["ry"], "#E0F2FE", "#0284C7", 2, inc["text"], font_sub_uc, "#075985")
        
        # If connects to right actor
        if inc.get("to_right", False):
            draw_solid_association(draw, inc["cx"] + inc["rx"], inc["cy"], 1035, 290, "#0284C7")

    # 8. Extends
    exts = data["extends"]
    for ext in exts:
        # If positioned at bottom
        if ext["cy"] > muc["cy"] + 50:
            # Arrow points UP from Extend UC to Main UC
            sx = ext["cx"]
            sy = ext["cy"] - ext["ry"]
            ex = muc["cx"] + (ext["cx"] - muc["cx"]) * 0.4
            ey = muc["cy"] + muc["ry"]
            draw_dashed_arrow(draw, sx, sy, ex, ey, "#B45309", "<<extend>>")
        else:
            # Normal connection
            sx = ext["cx"] + ext["rx"]
            sy = ext["cy"]
            ex = muc["cx"] - muc["rx"] * 0.6
            ey = muc["cy"] - muc["ry"] * 0.6
            draw_dashed_arrow(draw, sx, sy, ex, ey, "#B45309", "<<extend>>")

        # Draw Extend UC
        draw_oval(draw, ext["cx"], ext["cy"], ext["rx"], ext["ry"], "#FEF3C7", "#D97706", 2, ext["text"], font_sub_uc, "#92400E")

    # 9. Legend
    draw_legend(draw)

    # Save
    out_path = os.path.join(OUTPUT_DIR, data["filename"])
    img.save(out_path, quality=95)
    print(f"Generated: {data['filename']}")

def main():
    print("=== STARTING GENERATION OF 14 DETAILED USE CASE DIAGRAMS ===")
    for uc in USE_CASES_DATA:
        render_diagram(uc)
    print(f"=== ALL 14 DIAGRAMS GENERATED SUCCESSFULLY IN {OUTPUT_DIR}! ===")

if __name__ == "__main__":
    main()

