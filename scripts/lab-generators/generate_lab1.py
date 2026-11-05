# -*- coding: utf-8 -*-
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()

# Page Margins (Normal 2cm)
for sec in doc.sections:
    sec.top_margin = Inches(0.79)
    sec.bottom_margin = Inches(0.79)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(0.79)

def style_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(31, 78, 121)
    return p

def style_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(46, 117, 182)
    return p

def style_heading_3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.italic = True
    r.font.color.rgb = RGBColor(0, 32, 96)
    return p

def add_p(text, bold_prefix='', italic=False, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.italic = italic
    return p

def add_bullet(text, bold_prefix=''):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def create_styled_table(rows_data, col_widths, headers=None):
    total_rows = len(rows_data) + (1 if headers else 0)
    cols = len(col_widths)
    t = doc.add_table(rows=total_rows, cols=cols)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False

    curr_row = 0
    if headers:
        hdr_row = t.rows[0]
        for c_idx, title in enumerate(headers):
            cell = hdr_row.cells[c_idx]
            cell.width = col_widths[c_idx]
            cell.text = title
            shd = parse_xml(r'<w:shd {} w:fill="1F4E79"/>'.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(shd)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.bold = True
                run.font.size = Pt(11)
                run.font.color.rgb = RGBColor(255, 255, 255)
        curr_row = 1

    for r_idx, row_values in enumerate(rows_data):
        row = t.rows[curr_row + r_idx]
        bg_color = "F2F5F9" if (r_idx % 2 == 1) else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            cell.text = str(val)
            shd = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), bg_color))
            cell._tc.get_or_add_tcPr().append(shd)
            tcBorders = parse_xml(r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/><w:left w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/><w:right w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/></w:tcBorders>'.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(tcBorders)
            p = cell.paragraphs[0]
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(11)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return t

# ==================== TRANG BÌA & THÔNG TIN ====================
p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
r1 = p_top.add_run('TRƯỜNG CAO ĐẲNG FPT POLYTECHNIC\nKHOA CÔNG NGHỆ THÔNG TIN\n')
r1.font.name = 'Times New Roman'
r1.font.bold = True
r1.font.size = Pt(13)
r1.font.color.rgb = RGBColor(242, 107, 33)

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(30)
p_title.paragraph_format.space_after = Pt(20)
r2 = p_title.add_run('BÁO CÁO LAB 1\n')
r2.font.name = 'Times New Roman'
r2.font.bold = True
r2.font.size = Pt(22)
r2.font.color.rgb = RGBColor(31, 78, 121)

r3 = p_title.add_run('MÔN HỌC: DỰ ÁN MẪU (NET108 / PRO1041)\nĐỀ TÀI: HỆ THỐNG QUẢN LÝ QUÁN ĐỒ UỐNG (POLY DRINK)\n')
r3.font.name = 'Times New Roman'
r3.font.bold = True
r3.font.size = Pt(14)
r3.font.color.rgb = RGBColor(89, 89, 89)

p_info = doc.add_paragraph()
p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_info.paragraph_format.space_before = Pt(40)
r_info = p_info.add_run('Sinh viên thực hiện: Trịnh Quốc Khải\nMã số sinh viên: PS38237\nLớp: WD19301\nGiảng viên hướng dẫn: Giảng viên Bộ môn CNTT - FPT Polytechnic\n')
r_info.font.name = 'Times New Roman'
r_info.font.size = Pt(12)
r_info.font.italic = True

doc.add_page_break()

# ==================== PHẦN I: GIỚI THIỆU DỰ ÁN ====================
style_heading_1('PHẦN I: GIỚI THIỆU DỰ ÁN')

# BÀI 1
style_heading_1('BÀI 1 (2.0 ĐIỂM): ỨNG DỤNG AI TRONG TÌM KIẾM THÔNG TIN')
style_heading_2('1.1. Mục tiêu ứng dụng AI trong học tập và phân tích dự án')
add_p('Trong kỷ nguyên phát triển mạnh mẽ của Trí tuệ Nhân tạo (AI), việc khai thác các công cụ như Perplexity AI, OpenAI ChatGPT và Google Gemini ở chế độ nghiên cứu sâu (Deepsearch / Research) mang lại hiệu quả vượt trội trong việc:')
add_bullet(' Nhanh chóng thu thập các khung sườn tài liệu chuẩn công nghiệp (như chuẩn IEEE 830, SRS Template của FPT Polytechnic).', '• Chuẩn hóa tài liệu:');
add_bullet(' Mô phỏng luồng nghiệp vụ thực tế của một quán cà phê/đồ uống (POS, pha chế, thanh toán, kiểm soát tồn).', '• Nghiên cứu nghiệp vụ:');
add_bullet(' Đề xuất cấu trúc phân chia Actor, chức năng theo đặc thù mô hình cửa hàng đồ uống.', '• Hỗ trợ phân tích:');

style_heading_2('1.2. Nhật ký Prompting và kết quả truy vấn thực tế')
add_p('Dưới đây là nhật ký chi tiết các câu lệnh Prompt được thực thi trên các công cụ AI:')

ai_table_data = [
    ['1', 'Perplexity AI', '"Tìm kiếm và phân tích cấu trúc tài liệu đặc tả yêu cầu phần mềm (SRS - Software Requirements Specification) chuẩn IEEE 830 cho phần mềm quản lý bán hàng quán cafe, đồ uống."', 'AI trả về cấu trúc gồm 3 phần chính: Giới thiệu dự án, Mô tả tổng quan hệ thống (Actors, Use Cases, Ràng buộc nghiệp vụ), và Đặc tả chi tiết từng Use Case theo bảng chuẩn (ID, Actor, Pre/Post condition, Flow).'],
    ['2', 'Google Gemini (Deep Search)', '"Khảo sát hiện trạng và các vấn đề bất cập thường gặp tại các quán cà phê vừa và nhỏ khi quản lý thủ công (order giấy, tính nhẩm, ghi sổ). Đề xuất giải pháp số hóa phần mềm."', 'AI chỉ ra 5 vấn đề cốt lõi: thất thoát đơn, nhầm lẫn món pha chế, thời gian chờ thanh toán lâu, không kiểm soát được ca làm việc của nhân viên và mất nhiều ngày để tổng hợp doanh số.'],
    ['3', 'ChatGPT 4o', '"Liệt kê danh sách các Use Case chính cho hệ thống Quản lý Bán Đồ Uống gồm 2 tác nhân chính là Nhân viên bán hàng và Quản lý quán. Trình bày dạng bảng phân quyền rõ ràng."', 'AI đề xuất phân rã 13 chức năng chuẩn: Nhóm chung (Đăng nhập, Quên MK, Đổi MK, Sửa TT cá nhân), Nhóm Nhân viên (Tạo phiếu, Sửa phiếu, Xem phiếu, Xem DS hóa đơn), Nhóm Quản lý (QL Loại đồ uống, QL Đồ uống, QL Nhân viên, QL Hóa đơn, Báo cáo thống kê).']
]
create_styled_table(ai_table_data, [Inches(0.5), Inches(1.3), Inches(2.6), Inches(2.7)], ['STT', 'Công cụ AI', 'Prompt chi tiết', 'Kết quả thu được & Ứng dụng'])

style_heading_2('1.3. Đánh giá và chắt lọc thông tin')
add_p('Từ các dữ liệu AI cung cấp, nhóm đã chọn lọc ra khung sườn tài liệu đặc tả hệ thống phù hợp nhất với biểu mẫu của FPT Polytechnic, đồng thời bám sát chính xác sơ đồ Use Case tổng quát được giao trong bài Lab (gồm 2 Actor và 13 chức năng).')

# BÀI 2
style_heading_1('BÀI 2 (4.0 ĐIỂM): THỰC HIỆN TÀI LIỆU GIỚI THIỆU DỰ ÁN')
style_heading_2('2.1. Giới thiệu dự án')
add_bullet(' Hệ thống Quản lý Bán hàng Quán Đồ Uống (Poly Drink Management System).', '• Tên dự án:');
add_bullet(' Ứng dụng Desktop / Web quản lý bán hàng và vận hành nội bộ quán đồ uống.', '• Loại hình:');
add_bullet(' Xây dựng giải pháp phần mềm chuyên biệt, khép kín dành cho quán cà phê, trà sữa, hỗ trợ tối đa quy trình ghi nhận order, in hóa đơn nhanh, đồng bộ dữ liệu doanh số và quản trị danh mục thực đơn.', '• Ý tưởng cốt lõi:');

style_heading_2('2.2. Phân tích yêu cầu khách hàng và hiện trạng dẫn đến đề xuất dự án')
add_p('1. Hiện trạng thực tế tại các quán đồ uống truyền thống:')
add_bullet(' Khách hàng vào giờ cao điểm phải xếp hàng chờ lâu; nhân viên ghi nhận order trên giấy dễ nhầm lẫn (sai topping, nhầm size, sai bàn).')
add_bullet(' Tính nhẩm hoặc dùng máy tính bỏ túi thủ công dễ xảy ra sai sót khi thanh toán; việc áp dụng giảm giá hay tính tiền thừa thiếu chính xác.')
add_bullet(' Cuối ngày, chủ quán mất 1 - 2 tiếng kiểm đếm hóa đơn giấy và hóa đơn hủy, dễ thất thoát doanh thu do gian lận hoặc sai lệch số liệu.')
add_bullet(' Khó quản lý biến động giá và tình trạng hết món: Khi hết nguyên liệu một món nào đó, nhân viên không kịp nắm bắt dẫn đến việc khách gọi món rồi lại phải đổi.')

add_p('2. Giải pháp công nghệ đề xuất:')
add_p('Phát triển phần mềm "Poly Drink" với giao diện trực quan, chia tách rõ ràng 2 phân hệ quyền hạn (Nhân viên và Quản lý):')
add_bullet(' Nhân viên order bằng cú click chuột hoặc chạm màn hình, tự động tính tổng tiền chính xác, in hóa đơn tức thì.')
add_bullet(' Quản lý kiểm soát toàn diện danh mục đồ uống, giá bán, nhân sự và báo cáo doanh thu theo thời gian thực mọi lúc mọi nơi.')

style_heading_2('2.3. Liệt kê thành phần người dùng (Actors)')
add_bullet(' Người trực tiếp đứng quầy thu ngân và phục vụ khách. Thực hiện các thao tác tạo phiếu bán hàng, chỉnh sửa phiếu khi khách đổi món, tra cứu phiếu bán hàng và xem danh sách hóa đơn do chính ca của mình tạo ra.', '1. Nhân viên (Staff / Cashier): ');
add_bullet(' Chủ quán hoặc người điều hành ca có toàn quyền kiểm soát hoạt động của quán: Quản lý nhân viên, quản lý phân loại và chi tiết đồ uống, theo dõi toàn bộ hóa đơn của cửa hàng, và tra cứu các báo cáo thống kê doanh thu đa chiều.', '2. Quản lý (Manager / Admin): ');

style_heading_2('2.4. Danh sách chức năng theo từng đối tượng người dùng')
add_p('Bảng 1. Danh sách chức năng Nhóm dùng chung (Cả Nhân viên & Quản lý):')
f_common = [
    ['1', 'Đăng nhập', 'Xác thực tài khoản và mật khẩu người dùng vào hệ thống, phân quyền truy cập theo vai trò (Nhân viên / Quản lý).'],
    ['2', 'Đổi mật khẩu', 'Cho phép người dùng chủ động thay đổi mật khẩu định kỳ nhằm nâng cao tính bảo mật tài khoản.'],
    ['3', 'Quên mật khẩu', 'Hỗ trợ khôi phục mật khẩu thông qua email xác nhận khi người dùng quên thông tin đăng nhập.'],
    ['4', 'Sửa thông tin cá nhân', 'Cho phép người dùng cập nhật thông tin cá nhân (họ tên, số điện thoại, ảnh đại diện, địa chỉ).']
]
create_styled_table(f_common, [Inches(0.6), Inches(2.2), Inches(4.3)], ['STT', 'Tên chức năng', 'Mô tả chi tiết'])

add_p('Bảng 2. Danh sách chức năng dành riêng cho Nhân viên:')
f_staff = [
    ['1', 'Tạo phiếu bán hàng', 'Tạo mới một hóa đơn bán lẻ, chọn các món đồ uống, số lượng, size, đường/đá, tính thành tiền.'],
    ['2', 'Sửa phiếu bán hàng', 'Cho phép cập nhật thêm/bớt món, đổi số lượng trên phiếu bán hàng trước khi khách thanh toán.'],
    ['3', 'Xem phiếu bán hàng', 'Hiển thị chi tiết nội dung phiếu bán hàng hiện tại đang phục vụ hoặc đang chờ xử lý.'],
    ['4', 'Xem danh sách hóa đơn cá nhân', 'Xem lịch sử các hóa đơn đã thanh toán do chính nhân viên đó thực hiện trong ca làm việc.']
]
create_styled_table(f_staff, [Inches(0.6), Inches(2.2), Inches(4.3)], ['STT', 'Tên chức năng', 'Mô tả chi tiết'])

add_p('Bảng 3. Danh sách chức năng dành riêng cho Quản lý:')
f_manager = [
    ['1', 'Quản lý loại đồ uống', 'Thêm mới, sửa tên, xóa danh mục loại đồ uống (Ví dụ: Cà phê, Trà hoa quả, Đá xay, Nước ép).'],
    ['2', 'Quản lý đồ uống', 'Quản lý danh sách từng món: tên đồ uống, đơn giá, hình ảnh, loại đồ uống, trạng thái còn/hết hàng.'],
    ['3', 'Quản lý nhân viên', 'Quản lý hồ sơ nhân sự: thêm tài khoản nhân viên mới, phân quyền, sửa thông tin, khóa tài khoản.'],
    ['4', 'Quản lý hóa đơn', 'Xem toàn bộ lịch sử hóa đơn bán ra của tất cả nhân viên, tìm kiếm theo ngày/nhân viên, xử lý hủy đơn sai.'],
    ['5', 'Báo cáo thống kê', 'Thống kê tổng doanh thu theo ngày/tháng/năm, biểu đồ top đồ uống bán chạy nhất, số lượng ly tiêu thụ.']
]
create_styled_table(f_manager, [Inches(0.6), Inches(2.2), Inches(4.3)], ['STT', 'Tên chức năng', 'Mô tả chi tiết'])

style_heading_2('2.5. Phân tích luồng hoạt động các chức năng và sự liên kết giữa các chức năng')
add_p('Mối liên kết giữa các phân hệ chức năng trong hệ thống Poly Drink diễn ra chặt chẽ theo quy trình kinh doanh thống nhất:')
add_bullet(' Nhân viên và Quản lý phải đăng nhập thành công. Hệ thống phân quyền điều hướng Nhân viên vào giao diện bán hàng (POS), Quản lý vào giao diện Dashboard điều hành.', '1. Luồng Xác thực & Phân quyền:');
add_bullet(' Khi có khách gọi món, Nhân viên thực hiện "Tạo phiếu bán hàng". Chức năng này lấy dữ liệu từ bảng "Quản lý đồ uống" và "Quản lý loại đồ uống" do Quản lý thiết lập trước đó. Nhân viên có thể "Sửa phiếu bán hàng" (thêm bớt món) nếu khách thay đổi ý kiến. Sau khi khách thanh toán, hệ thống chốt hóa đơn, in phiếu và lưu vào cơ sở dữ liệu.', '2. Luồng Nghiệp vụ Bán hàng & Lập hóa đơn:');
add_bullet(' Hóa đơn sau khi được thanh toán sẽ tự động phân loại: Nhân viên có thể vào "Xem danh sách hóa đơn cá nhân" để đối soát ca làm; đồng thời dữ liệu ngay lập tức được chuyển sang phân hệ "Quản lý hóa đơn" của Quản lý.', '3. Luồng Quản lý Hóa đơn & Đối soát:');
add_bullet(' Mỗi giao dịch bán hàng thành công sẽ tự động cập nhật số liệu vào phân hệ "Báo cáo thống kê". Quản lý có thể theo dõi doanh số nhảy tức thì mà không cần tổng kết sổ sách thủ công.', '4. Luồng Thống kê Doanh số:');

doc.add_page_break()

# ==================== PHẦN II: PHÂN TÍCH VÀ VẼ SƠ ĐỒ ====================
style_heading_1('PHẦN II: PHÂN TÍCH VÀ VẼ SƠ ĐỒ')
style_heading_1('BÀI 3 (4.0 ĐIỂM): VẼ MÔ HÌNH HỆ THỐNG VÀ XÁC ĐỊNH CÁC THỰC THỂ')

style_heading_2('3.1. Tìm hiểu các quy tắc vẽ sơ đồ Use Case theo chuẩn UML')
add_p('Sơ đồ Use Case (Use Case Diagram) là một biểu đồ thuộc ngôn ngữ mô hình hóa thống nhất UML, mô tả sự tương tác giữa các tác nhân bên ngoài (Actor) với các chức năng của hệ thống (Use Case).')
add_bullet(' Đối tượng tương tác với hệ thống (người dùng hoặc hệ thống bên ngoài). Ký hiệu hình người que.', '• Actor (Tác nhân):');
add_bullet(' Đại diện cho một chức năng cụ thể mà hệ thống cung cấp cho Actor để đạt được mục tiêu. Ký hiệu hình elip chứa tên chức năng.', '• Use Case (Trường hợp sử dụng):');
add_bullet(' Ranh giới xác định phạm vi phần mềm, các Use Case nằm bên trong khung, Actor nằm bên ngoài. Ký hiệu hình chữ nhật.', '• System Boundary (Ranh giới hệ thống):');
add_bullet(' Đường nối liền biểu thị sự tham gia của Actor vào Use Case.', '• Quan hệ Association:');
add_bullet(' Quan hệ bao hàm bắt buộc (Use Case A luôn luôn thực thi Use Case B). Ký hiệu nét đứt có mũi tên kèm nhãn <<include>>.', '• Quan hệ <<include>>:');
add_bullet(' Quan hệ mở rộng không bắt buộc, chỉ xảy ra khi có điều kiện kích hoạt. Ký hiệu nét đứt có mũi tên kèm nhãn <<extend>>.', '• Quan hệ <<extend>>:');

style_heading_2('3.2. Sơ đồ Use Case tổng quát hệ thống Quản lý Đồ Uống')
add_p('Sơ đồ tổng quát thể hiện đầy đủ 2 Tác nhân (Nhân viên, Quản lý) và 13 Use Cases theo đúng yêu cầu đề bài Lab 1:')

uc_summary_table = [
    ['1', 'Đăng nhập', 'Cả 2 (Nhân viên & Quản lý)', 'Xác thực tài khoản'],
    ['2', 'Đổi mật khẩu', 'Cả 2 (Nhân viên & Quản lý)', 'Bảo mật tài khoản cá nhân'],
    ['3', 'Quên mật khẩu', 'Cả 2 (Nhân viên & Quản lý)', 'Khôi phục mật khẩu'],
    ['4', 'Sửa thông tin cá nhân', 'Cả 2 (Nhân viên & Quản lý)', 'Cập nhật hồ sơ cá nhân'],
    ['5', 'Tạo phiếu bán hàng', 'Nhân viên', 'Tạo order và lập bill thanh toán'],
    ['6', 'Sửa phiếu bán hàng', 'Nhân viên', 'Thêm/bớt món, sửa số lượng trên phiếu'],
    ['7', 'Xem phiếu bán hàng', 'Nhân viên', 'Kiểm tra chi tiết đơn hàng hiện hành'],
    ['8', 'Xem danh sách hóa đơn cá nhân', 'Nhân viên', 'Theo dõi doanh thu ca cá nhân'],
    ['9', 'Quản lý loại đồ uống', 'Quản lý', 'CRUD nhóm thực đơn đồ uống'],
    ['10', 'Quản lý đồ uống', 'Quản lý', 'CRUD món, giá bán, hình ảnh, trạng thái'],
    ['11', 'Quản lý nhân viên', 'Quản lý', 'CRUD tài khoản nhân viên và quyền'],
    ['12', 'Quản lý hóa đơn', 'Quản lý', 'Giám sát toàn bộ hóa đơn quán, hủy đơn sai'],
    ['13', 'Báo cáo thống kê', 'Quản lý', 'Thống kê doanh thu, số lượng bán ra']
]
create_styled_table(uc_summary_table, [Inches(0.5), Inches(2.3), Inches(2.0), Inches(2.3)], ['STT', 'Tên Use Case', 'Actor thực hiện', 'Mục đích nghiệp vụ'])

style_heading_2('3.3. Đặc tả yêu cầu hệ thống (SRS - Software Requirements Specification)')
add_p('Dưới đây là bảng đặc tả chi tiết các Use Case cốt lõi của hệ thống theo đúng cấu trúc chuẩn của FPT Polytechnic:')

def add_srs_table(uc_id, uc_name, desc, actor, trigger, pre, post, main_flow, alt_flow, exc_flow):
    data = [
        ['Use Case ID', uc_id],
        ['Use Case', uc_name],
        ['Short Description', desc],
        ['Actors', actor],
        ['Trigger', trigger],
        ['Pre-conditions', pre],
        ['Post-conditions', post],
        ['Main Flow', main_flow],
        ['Alternative Flow', alt_flow],
        ['Exception Flow', exc_flow]
    ]
    t = doc.add_table(rows=10, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for r_idx, row in enumerate(data):
        r = t.rows[r_idx]
        cell_lbl = r.cells[0]
        cell_val = r.cells[1]
        cell_lbl.width = Inches(1.8)
        cell_val.width = Inches(5.3)
        cell_lbl.text = row[0]
        cell_val.text = row[1]
        
        shd_lbl = parse_xml(r'<w:shd {} w:fill="E8EEF5"/>'.format(nsdecls('w')))
        cell_lbl._tc.get_or_add_tcPr().append(shd_lbl)
        
        tcBorders = parse_xml(r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/></w:tcBorders>'.format(nsdecls('w')))
        cell_lbl._tc.get_or_add_tcPr().append(tcBorders)
        cell_val._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="A6B9D0"/></w:tcBorders>'.format(nsdecls('w'))))
        
        p0 = cell_lbl.paragraphs[0]
        p0.runs[0].font.name = 'Times New Roman'
        p0.runs[0].font.bold = True
        p0.runs[0].font.size = Pt(11)
        
        p1 = cell_val.paragraphs[0]
        p1.runs[0].font.name = 'Times New Roman'
        p1.runs[0].font.size = Pt(11)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

style_heading_3('Bảng đặc tả Use Case 1: Đăng nhập hệ thống (UC_AUTH_01)')
add_srs_table(
    'UC_AUTH_01',
    'Đăng nhập hệ thống',
    'Cho phép người dùng (Nhân viên hoặc Quản lý) đăng nhập vào ứng dụng để thực hiện công việc theo quyền hạn được cấp.',
    'Nhân viên, Quản lý',
    'Người dùng mở ứng dụng và nhấn nút "Đăng nhập" trên màn hình chính.',
    'Người dùng đã được cấp tài khoản và mật khẩu hợp lệ trong cơ sở dữ liệu.',
    'Thành công: Hệ thống xác thực thành công, ghi nhận phiên làm việc và chuyển đến giao diện làm việc tương ứng.\nThất bại: Hệ thống báo lỗi và yêu cầu nhập lại.',
    '(1) Người dùng khởi động ứng dụng, màn hình đăng nhập xuất hiện.\n(2) Người dùng nhập Tên đăng nhập (hoặc Mã NV) và Mật khẩu.\n(3) Người dùng nhấn nút "Đăng nhập".\n(4) Hệ thống kiểm tra thông tin tài khoản trong cơ sở dữ liệu.\n(5) Hệ thống nhận diện vai trò (Nhân viên / Quản lý) và điều hướng đến màn hình chính tương ứng.',
    '(2a) Người dùng quên mật khẩu: Nhấn nút "Quên mật khẩu" để chuyển sang luồng khôi phục.',
    '(4.1) Tên đăng nhập không tồn tại hoặc mật khẩu sai: Hệ thống thông báo "Sai thông tin đăng nhập!" và yêu cầu nhập lại.\n(4.2) Tài khoản bị khóa: Hệ thống thông báo "Tài khoản của bạn đã bị vô hiệu hóa! Liên hệ Quản lý."'
)

style_heading_3('Bảng đặc tả Use Case 2: Tạo phiếu bán hàng (UC_STAFF_01)')
add_srs_table(
    'UC_STAFF_01',
    'Tạo phiếu bán hàng',
    'Cho phép nhân viên tạo một order bán đồ uống mới cho khách hàng, tính toán thành tiền và in hóa đơn thanh toán.',
    'Nhân viên bán hàng',
    'Nhân viên nhấn nút "Tạo phiếu mới" trên giao diện POS bán hàng.',
    'Nhân viên đã đăng nhập thành công vào hệ thống với quyền Nhân viên.',
    'Thành công: Phiếu bán hàng được tạo, hóa đơn được lưu vào CSDL, in hóa đơn cho khách và cập nhật doanh thu ca.\nThất bại: Hủy thao tác, phiếu không được lưu.',
    '(1) Nhân viên chọn "Tạo phiếu mới".\n(2) Hệ thống hiển thị danh mục loại đồ uống và danh sách món.\n(3) Nhân viên click chọn món đồ uống theo yêu cầu của khách, chọn số lượng, size ly, ghi chú (đá/đường).\n(4) Hệ thống tự động tính thành tiền từng món và tổng tiền của phiếu.\n(5) Nhân viên nhập số tiền khách đưa.\n(6) Hệ thống tính tiền thối lại cho khách.\n(7) Nhân viên nhấn nút "Thanh toán & In hóa đơn".\n(8) Hệ thống lưu thông tin hóa đơn vào CSDL và gửi lệnh in ra máy in nhiệt.',
    '(3a) Khách muốn đổi món hoặc chỉnh số lượng: Nhân viên thao tác trực tiếp trên bảng danh sách món đã chọn (gọi Use Case Sửa phiếu bán hàng).',
    '(3.1) Món đồ uống đã hết nguyên liệu (trạng thái Hết hàng): Hệ thống cảnh báo món tạm ngưng phục vụ, không cho thêm vào phiếu.\n(5.1) Số tiền khách đưa nhỏ hơn tổng tiền phải trả: Hệ thống hiển thị cảnh báo "Chưa đủ tiền thanh toán".'
)

style_heading_3('Bảng đặc tả Use Case 3: Quản lý đồ uống (UC_MGR_01)')
add_srs_table(
    'UC_MGR_01',
    'Quản lý đồ uống',
    'Cho phép Quản lý thực hiện thêm mới, cập nhật thông tin (tên món, giá bán, size, hình ảnh) hoặc ngừng kinh doanh một món đồ uống.',
    'Quản lý (Manager)',
    'Quản lý truy cập vào mục "Quản lý đồ uống" từ thanh menu quản trị.',
    'Người dùng đã đăng nhập với vai trò Quản lý.',
    'Thành công: Danh sách món đồ uống được cập nhật trong CSDL và hiển thị đồng bộ lên màn hình bán hàng của Nhân viên.\nThất bại: Dữ liệu không thay đổi, hệ thống báo lỗi.',
    '(1) Quản lý chọn chức năng "Quản lý đồ uống".\n(2) Hệ thống tải và hiển thị danh sách đồ uống hiện có kèm theo ảnh, giá và phân loại.\n(3) Để thêm mới: Quản lý nhấn "Thêm", nhập Tên đồ uống, chọn Loại đồ uống, nhập Đơn giá, tải ảnh minh họa và nhấn "Lưu".\n(4) Để sửa: Quản lý chọn món cần sửa trong danh sách, cập nhật thông tin và nhấn "Cập nhật".\n(5) Để xóa / ngừng bán: Quản lý chọn món và chọn "Ngừng kinh doanh" hoặc "Xóa".\n(6) Hệ thống kiểm tra tính hợp lệ của dữ liệu và cập nhật vào CSDL.\n(7) Hệ thống thông báo thao tác thành công và tải lại bảng danh sách đồ uống.',
    '(3a) Quản lý có thể lọc hoặc tìm kiếm đồ uống theo tên hoặc danh mục trước khi chỉnh sửa.',
    '(6.1) Dữ liệu nhập trống (tên món để trống, đơn giá <= 0): Hệ thống báo lỗi và bôi đỏ trường dữ liệu sai.\n(6.2) Xóa món đồ uống đã có trong lịch sử hóa đơn: Hệ thống chuyển trạng thái sang "Ngừng kinh doanh" thay vì xóa vật lý để đảm bảo toàn vẹn dữ liệu kế toán.'
)

style_heading_3('Bảng đặc tả Use Case 4: Báo cáo thống kê (UC_MGR_02)')
add_srs_table(
    'UC_MGR_02',
    'Báo cáo thống kê',
    'Cung cấp cho Quản lý số liệu tổng hợp về doanh thu, số lượng hóa đơn, số lượng ly đồ uống tiêu thụ theo mốc thời gian và danh sách đồ uống bán chạy nhất.',
    'Quản lý (Manager)',
    'Quản lý chọn mục "Báo cáo thống kê" trên giao diện quản trị.',
    'Quản lý đã đăng nhập thành công vào hệ thống.',
    'Thành công: Hiển thị đầy đủ số liệu và biểu đồ thống kê trực quan theo khoảng thời gian được chọn.\nThất bại: Không có dữ liệu để thống kê trong khoảng thời gian đã lọc.',
    '(1) Quản lý truy cập màn hình "Báo cáo thống kê".\n(2) Hệ thống hiển thị mặc định báo cáo doanh thu của Ngày hôm nay.\n(3) Quản lý chọn tiêu chí lọc: Theo Ngày, Theo Tháng, Theo Khoảng ngày (Từ ngày... Đến ngày...) hoặc Theo Nhân viên.\n(4) Quản lý nhấn nút "Xem thống kê".\n(5) Hệ thống truy vấn CSDL hóa đơn, tính toán tổng doanh thu, số ly bán, top 5 món bán chạy nhất.\n(6) Hệ thống kết xuất dữ liệu dưới dạng bảng số liệu và biểu đồ trực quan (Biểu đồ cột / tròn).\n(7) Quản lý có thể chọn nút "Xuất Excel" để tải file báo cáo về máy.',
    '(3a) Quản lý chỉ lọc theo một nhân viên bán hàng cụ thể để kiểm tra hiệu suất ca làm.',
    '(5.1) Khoảng thời gian được chọn không phát sinh giao dịch nào: Hệ thống hiển thị thông báo "Không có dữ liệu hóa đơn trong khoảng thời gian này" với tổng doanh thu là 0 VNĐ.'
)

doc.save(r'C:\Net108Khai\BaoCao_Lab1_NET108_QuanLyDoUong.docx')
print('Successfully generated full BaoCao_Lab1_NET108_QuanLyDoUong.docx!')
