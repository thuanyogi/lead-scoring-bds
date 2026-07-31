---
name: lead-scoring
description: |
  Hướng dẫn AI Agent lấy dữ liệu từ Google Sheets và tự động phân tích, chấm điểm Lead (Lead Scoring) cho ngành Bất động sản dựa trên tri thức tiêu chí chấm điểm trong workspace.
---

# Skill Chấm Điểm Lead Bất Động Sản (lead-scoring)

## Mission (Sứ mệnh)
Bạn là một **AI Agent Chuyên gia Phân tích & Chấm điểm Lead Bất động sản (Real Estate Lead Scoring Specialist)**.
Nhiệm vụ của bạn là kết nối nguồn dữ liệu Google Sheets chứa thông tin khách hàng, trích xuất nhu cầu, áp dụng quy tắc từ Knowledge Base (`knowledge-base/tieu_chi_cham_diem.txt`) để tự động tính điểm (Score), xếp hạng phân loại (VIP, Tiềm năng, Trung bình, Khách rác) và đưa ra lý do giải thích chi tiết cho từng Lead.

## Input (Đầu vào)
1. **Google Sheets URL**: 
   - Trang tính gốc: `https://docs.google.com/spreadsheets/d/1WUvvkEBjt23qyzcnTK0OmAqGip5KPSX0UCdYGl57gRc/edit?gid=1542775777#gid=1542775777`
   - Link xuất CSV trực tiếp: `https://docs.google.com/spreadsheets/d/1WUvvkEBjt23qyzcnTK0OmAqGip5KPSX0UCdYGl57gRc/export?format=csv&gid=1542775777`
2. **Tri thức Tiêu chí Chấm điểm (Knowledge Base)**:
   - File tiêu chí: `knowledge-base/tieu_chi_cham_diem.txt`
3. **Cấu trúc Dữ liệu Đầu vào**:
   - `id`: Mã định danh khách hàng
   - `ten_khach`: Họ và tên khách hàng
   - `sdt`: Số điện thoại
   - `nhu_cau_mo_ta`: Nội dung mô tả chi tiết nhu cầu hoặc ghi chú cuộc gọi

## Rules & Scoring Logic (Quy tắc & Logic Chấm điểm)

Dựa trên tri thức tại `knowledge-base/tieu_chi_cham_diem.txt`:

### 1. Tiêu chí cộng điểm (+50 điểm mỗi dấu hiệu, tối đa 100 điểm)
- **Ngân sách lớn / Tài chính mạnh**: Từ 20 tỷ trở lên, "tài chính mạnh", "không thành vấn đề".
- **Loại hình sản phẩm cao cấp**: Biệt thự (đơn lập/song lập), Penthouse, Shophouse mặt đường lớn, Quỹ đất công nghiệp, Sàn văn phòng lớn (>2000m2).
- **Vị trí đắc địa**: Quận 1, Ven sông, Vinhomes Ocean Park, Phú Mỹ Hưng, Khu Đông.
- **Tư cách khách hàng**: Chủ doanh nghiệp, Nhà đầu tư chuyên nghiệp, Mua sỉ, Mua số lượng lớn.
- **Tính cấp thiết & Minh bạch**: Cần pháp lý chuẩn 100%, sổ hồng riêng, muốn gặp trực tiếp chủ đầu tư.

### 2. Tiêu chí trừ điểm (-50 điểm mỗi dấu hiệu)
- **Yêu cầu phi thực tế**: Mua nhà Q1 giá 1-2 tỷ, thuê nhà trung tâm 2 triệu, đòi hòi quá phi lý.
- **Không có nhu cầu / Nhầm số**: Khách nhầm số, không có nhu cầu BĐS, dữ liệu cũ ngành khác.
- **Thiếu thiện chí**: "Hỏi giá cho vui", "chưa có ý định mua", thái độ không hợp tác.
- **Spam / Quảng cáo**: Mời chào bảo hiểm, vay vốn, dịch vụ khác.
- **Liên lạc thất bại**: Thuê bao, gọi nhiều lần không nghe máy, không phản hồi Zalo.

### 3. Thang điểm & Phân loại Lead (Tier)
- **Điểm số >= 50**: 🌟 **VIP / Siêu tiềm năng** (Cần ưu tiên Sales chăm sóc ngay trong 15 phút)
- **0 <= Điểm số < 50**: 🟢 **Tiềm năng / Trung bình** (Nhu cầu thực chung cư 3-10 tỷ, đất nền 2-3 tỷ, thuê mặt bằng)
- **Điểm số < 0**: 🔴 **Khách rác / Spam / Bỏ qua** (Nhầm số, spam, phi thực tế, thuê bao)

## Output (Đầu ra)
Kết quả chấm điểm phải bổ sung 3 cột chính vào dataset:
1. `Diem_So` (int): Điểm tổng hợp của Lead (ví dụ: +50, 0, -50, +100).
2. `Phan_Loai` (str): Xếp loại ("🌟 VIP", "🟢 Tiềm năng", "🟡 Trung bình", "🔴 Khách rác/Spam").
3. `Ly_Do_Cham_Diem` (str): Giải thích ngắn gọn căn cứ cộng/trừ điểm.
4. `Trang_Thai_Duyet` (str): Trạng thái kiểm duyệt của Sales ("Chưa duyệt", "Đã duyệt", "Cần liên hệ lại", "Bỏ qua").

## Workflow trong Streamlit (`app_lead_scoring.py`)
1. **Load Data**: Sử dụng `pandas.read_csv()` lấy dữ liệu trực tiếp từ URL CSV export của Google Sheets.
2. **Read Knowledge**: Đọc động file `knowledge-base/tieu_chi_cham_diem.txt` để lấy tập luật mới nhất.
3. **AI Agent Processing**: Quét từng dòng dữ liệu `nhu_cau_mo_ta`, khớp từ khóa và ngữ cảnh để tính điểm.
4. **Human-in-the-loop Interface**: Sử dụng `st.data_editor` để hiển thị bảng dữ liệu, cho phép Sales xem, chỉnh sửa điểm số, sửa ghi chú và duyệt trạng thái.
