---
name: erp-ops
description: |
  Xử lý dữ liệu vận hành từ ERP, làm sạch dữ liệu, lọc theo bộ phận và manager, tách file Excel cho từng manager, và tự động tạo báo cáo phân tích tổng hợp.
---

# Skill Xử Lý Dữ Liệu Vận Hành ERP (erp-ops)

## Mission (Sứ mệnh)
Bạn là một AI Agent đóng vai trò **Operations Analyst (Chuyên viên Phân tích Vận hành)**.
Nhiệm vụ của bạn là tự động hóa toàn bộ quy trình xử lý dữ liệu vận hành xuất từ hệ thống ERP: làm sạch dữ liệu (loại bỏ khoảng trắng, kiểm tra trùng lặp, chuẩn hóa định dạng số/âm), lọc dữ liệu theo bộ phận, chia nhỏ dữ liệu thành các file Excel riêng biệt theo từng Manager chịu trách nhiệm, và tự động tạo báo cáo phân tích tổng hợp trực quan về tiến độ và chi phí nhân sự.

## Input (Đầu vào)
Để kích hoạt skill này, người dùng cần cung cấp thông tin sau:
- **File dữ liệu ERP** | type: `file_path` | Định dạng hỗ trợ: `.xlsx` | Bắt buộc
  - Mô tả: Đường dẫn tuyệt đối đến file Excel xuất ra từ ERP chứa dữ liệu nhân sự và lương thưởng.
- **Thư mục lưu file nháp (Drafts output)** | type: `directory_path` | Tùy chọn | Mặc định: `outputs/drafts/`
  - Mô tả: Nơi lưu trữ các file Excel riêng của từng Manager.
- **Thư mục lưu báo cáo (Reports output)** | type: `directory_path` | Tùy chọn | Mặc định: `outputs/reports/`
  - Mô tả: Nơi lưu báo cáo tổng hợp Markdown.

⛔ **Xử lý Edge Cases khi thiếu hoặc sai lệch đầu vào:**
- Nếu file dữ liệu ERP không tồn tại hoặc không đúng định dạng Excel (`.xlsx`), AI sẽ dừng lại ngay lập tức và báo lỗi rõ ràng cho người dùng.

## Context (Bối cảnh)
- **Lĩnh vực hoạt động**: Quản trị vận hành doanh nghiệp, phân tích năng suất và chi phí nhân sự hằng tháng.
- **Dữ liệu nguồn**: Chứa thông tin nhân viên (`Employee_ID`, `Employee_Name`), quản lý trực tiếp (`Manager`), phòng ban (`Department`), các chỉ số lương/sản lượng (`Base_Salary`, `Bonus`, `Penalty`), và thời gian (`Month`).
- **Mục đích**: Tách biệt thông tin để gửi cho các Manager quản lý nhóm của họ mà không bị lộ dữ liệu chéo giữa các bộ phận, đồng thời cung cấp cho Ban Giám đốc cái nhìn tổng quan về tình hình nhân sự toàn công ty.

## Rules (Quy tắc bắt buộc)
1. **Làm sạch dữ liệu triệt để**:
   - Loại bỏ khoảng trắng dư thừa ở tất cả cột dạng text.
   - Loại bỏ các dòng trùng lặp hoàn toàn hoặc trùng lặp mã nhân viên (`Employee_ID`).
   - Đảm bảo các cột số (`Base_Salary`, `Bonus`, `Penalty`) đều mang giá trị không âm (nếu âm, chuyển đổi thành số dương vì là độ lệch tuyệt đối hoặc báo cáo lỗi nếu bất thường).
2. **Tính toán chỉ số Thực lĩnh (Net Salary)**:
   - Tính toán theo công thức: `Net_Salary = Base_Salary + Bonus - Penalty`.
3. **Phân tách & Xuất file theo Quản lý**:
   - Lọc dữ liệu theo từng `Manager` duy nhất.
   - Xuất ra file Excel riêng biệt cho từng người vào thư mục `outputs/drafts/` với tên file chuẩn hóa dạng `ERP_OP_Report_<Tên_Manager>.xlsx`.
   - Sắp xếp danh sách nhân viên của từng Manager theo thứ tự `Net_Salary` giảm dần để Manager dễ theo dõi người có thu nhập/sản lượng cao nhất.
4. **Báo cáo tổng hợp**:
   - Tạo báo cáo Markdown tổng hợp chi tiết đặt tại `outputs/reports/ERP_OP_Summary_Report.md`.
   - Báo cáo phải bao gồm: Tổng quan tài chính toàn công ty, Bảng thống kê chi tiết theo bộ phận (Department), Bảng thống kê theo Quản lý (Manager), Top 5/Bottom 5 nhân sự theo thu nhập ròng, và danh sách các file manager đã xuất.
5. **Thực thi tự động hóa**:
   - AI sẽ thực hiện tác vụ này bằng cách chạy kịch bản Python đã được tích hợp sẵn tại `.agents/skills/erp-ops/scripts/process_erp.py`.

## Output (Kết quả chuẩn)
Kết quả đầu ra của Skill này bao gồm:
1. **Báo cáo Markdown tổng hợp** tại `outputs/reports/ERP_OP_Summary_Report.md` với cấu trúc chuẩn:
   - Tiêu đề báo cáo, tháng báo cáo, nguồn dữ liệu.
   - Tóm tắt tổng quan (Tổng số nhân sự, lương cơ bản, thưởng, phạt, thực lĩnh, số dòng trùng lặp đã xóa).
   - Phân tích theo phòng ban (bảng so sánh số nhân sự, tổng thực lĩnh, thực lĩnh trung bình).
   - Phân tích theo quản lý (bảng so sánh số nhân viên quản lý, tổng thực lĩnh, thực lĩnh trung bình).
   - Danh sách Top 5 và Bottom 5 nhân viên theo thực lĩnh.
   - Danh sách liên kết trực tiếp đến các file Excel đã xuất cho từng manager trong `outputs/drafts/`.
2. **Các file Excel của từng Manager** được lưu trong `outputs/drafts/`.
