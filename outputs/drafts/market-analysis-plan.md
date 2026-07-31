# Kế hoạch Triển khai: Phân tích Thị trường Quán Cà phê Quận 1

Kế hoạch này phác thảo các bước thu thập, xử lý dữ liệu từ Internet, xây dựng Dashboard trực quan trên Excel, và thực hiện phân tích để đưa ra các insight cùng đề xuất kinh doanh cho thị trường quán cà phê tại Quận 1, TP. Hồ Chí Minh.

---

## 📋 Thông tin chung
- **Mục tiêu:** Thu thập tối thiểu 20 quán cà phê tại Quận 1, chuẩn hóa dữ liệu, thiết kế Dashboard Excel chuyên nghiệp và báo cáo 03 insight + 02 đề xuất hành động.
- **Đường dẫn file kế hoạch:** [market-analysis-plan.md](file:///Users/thuanyogi/Downloads/_Project/AA/plans/260710-workspace-bridge/workspace-hv-v2/my-workspace/outputs/drafts/market-analysis-plan.md)
- **Đường dẫn thư mục đầu ra:** 
  - File Excel sạch & Dashboard: `outputs/reports/cafe_market_analysis.xlsx`
  - Báo cáo Insight: `outputs/reports/cafe_market_insight_report.md` (và phiên bản HTML trực quan)

---

## 🗺️ Lộ trình triển khai (4 Pha)

### Pha 1: Thu thập Dữ liệu (Data Collection)
- **Mục tiêu:** Thu thập thông tin thực tế từ Internet cho tối thiểu 20 quán cà phê tiêu biểu tại các phường thuộc Quận 1.
- **Phương pháp:**
  - Viết script Python sử dụng `requests` và các nguồn dữ liệu công khai hoặc tìm kiếm tự động qua Internet để tổng hợp thông tin.
  - Các nguồn tham khảo: Google Maps, Fanpage Facebook chính thức, Foody, ShopeeFood, và các trang đánh giá ẩm thực uy tín.
- **Các trường dữ liệu cần thu thập:**
  1. Tên quán
  2. Địa chỉ
  3. Phường (ví dụ: Bến Nghé, Bến Thành, Đa Kao, Tân Định...)
  4. Giá thấp nhất (VNĐ)
  5. Giá cao nhất (VNĐ)
  6. Đánh giá (Rating - từ 1.0 đến 5.0)
  7. Số lượng đánh giá (Review Count)
  8. Giờ mở cửa (ví dụ: 07:00 - 22:00 hoặc 24/7)
  9. Loại hình quán (Coffee, Specialty Coffee, Rooftop, Work Café, Garden Coffee...)
  10. Website/Fanpage (Link URL nếu có)
- **Output:** File dữ liệu thô dạng JSON/CSV lưu tại `outputs/drafts/raw_cafe_data.json`.

### Pha 2: Làm sạch & Chuẩn hóa Dữ liệu (Data Cleaning & Standardization)
- **Mục tiêu:** Đảm bảo dữ liệu nhất quán, chính xác và sẵn sàng cho việc phân tích.
- **Các bước thực hiện:**
  - **Xử lý trùng lặp:** Loại bỏ các quán trùng tên và địa chỉ.
  - **Đồng bộ hóa địa danh:** Chuẩn hóa cột "Phường" thành danh sách chính thức (loại bỏ tiền tố không đồng nhất như "P.", "Phường", khoảng trắng thừa).
  - **Chuẩn hóa giá cả:** Định dạng giá thành số nguyên (integer) đại diện cho VNĐ. Xử lý các quán có giá bị thiếu bằng cách đối chiếu menu hoặc điền giá trung bình của loại hình đó.
  - **Đồng bộ loại hình:** Gom nhóm các loại hình quán vào các nhóm chuẩn: *Specialty Coffee, Work Café, Rooftop, Modern/Chain Coffee, Traditional Coffee, Garden Coffee*.
  - **Xử lý dữ liệu thiếu:** Điền `N/A` cho các trường Website/Fanpage không tìm thấy.
- **Output:** File dữ liệu sạch dạng JSON/CSV tại `outputs/drafts/cleaned_cafe_data.json`.

### Pha 3: Xây dựng Excel Workbook & Dashboard (Excel Generation)
- **Mục tiêu:** Tạo file Excel chuyên nghiệp với cấu trúc dữ liệu tối ưu và Dashboard trực quan.
- **Công cụ:** Script Python sử dụng thư viện `openpyxl` hoặc `xlsxwriter`.
- **Cấu trúc file Excel (`cafe_market_analysis.xlsx`):**
  1. **Sheet 1: `Dashboard`**
     - Thiết kế theo phong cách tối giản, hiện đại với tông màu "Warm Coffee" (Nâu đậm, kem latte, xám espresso).
     - **Thẻ chỉ số KPI (KPI Cards):** Tổng số quán khảo sát, Giá trung bình thị trường, Điểm đánh giá trung bình, Tổng số lượt đánh giá.
     - **Các biểu đồ (Charts):**
       - *Biểu đồ 1:* Cột dọc (Column Chart) thể hiện số lượng quán theo phường để thấy mật độ phân bố địa lý.
       - *Biểu đồ 2:* Biểu đồ phân bố mức giá trung bình của các quán (hoặc theo loại hình).
       - *Biểu đồ 3:* Biểu đồ thanh ngang (Bar Chart) hiển thị Top 10 quán có đánh giá (Rating) cao nhất.
       - *Biểu đồ 4:* Biểu đồ cột so sánh số lượng đánh giá (Review Count) để đo lường mức độ phổ biến/tương tác.
       - *Biểu đồ 5:* Biểu đồ hình tròn/bánh (Pie/Doughnut Chart) thể hiện tỷ lệ phần trăm các loại hình quán.
  2. **Sheet 2: `Data_Cleaned`**
     - Bảng dữ liệu sạch được định dạng đẹp mắt (tiêu đề có màu nền nổi bật, dòng kẻ xen kẽ dễ nhìn, định dạng tiền tệ VNĐ rõ ràng, bật tính năng lọc dữ liệu AutoFilter).
  3. **Sheet 3: `Data_Analysis`**
     - Các bảng Pivot và dữ liệu phụ trợ làm nguồn cấp trực tiếp cho các biểu đồ trên Dashboard để đảm bảo Dashboard không bị rối và công thức rõ ràng.
- **Output:** File Excel chuyên nghiệp tại `outputs/reports/cafe_market_analysis.xlsx`.

### Pha 4: Phân tích Insight & Lập Báo cáo (Insight & Actionable Recommendations)
- **Mục tiêu:** Rút ra giá trị từ dữ liệu để hỗ trợ quyết định kinh doanh.
- **Nội dung Báo cáo:**
  - **Phân tích 03 Insight quan trọng:**
    1. *Phân bổ địa lý:* Phường nào tập trung mật độ quán cao nhất và tại sao? Sự phân cực giữa khu kinh doanh sầm uất (Bến Nghé, Bến Thành) và các khu vực khác.
    2. *Mối quan hệ Giá - Đánh giá:* Các quán phân khúc giá cao (ví dụ: Specialty) có thực sự nhận được điểm đánh giá tốt hơn từ khách hàng không?
    3. *Mô hình tối ưu:* Loại hình quán nào đang thu hút nhiều lượt đánh giá nhất và có điểm Rating trung bình cao nhất?
  - **Đưa ra 02 Đề xuất hành động thực tiễn:**
    1. *Lựa chọn địa điểm:* Gợi ý khu vực (Phường) tiềm năng để mở quán mới dựa trên mức độ cạnh tranh (mật độ quán thấp nhưng lưu lượng khách tốt hoặc điểm rating trung bình ở khu vực đó chưa cao).
    2. *Định vị mô hình & Phân khúc giá:* Đề xuất mô hình quán và khoảng giá mục tiêu có tiềm năng cạnh tranh cao nhất dựa trên khoảng trống thị trường đã phân tích.
- **Output:** Báo cáo markdown tại `outputs/reports/cafe_market_insight_report.md` và phiên bản HTML dashboard báo cáo chuyên nghiệp.

---

## 🎨 Tiêu chuẩn Thẩm mỹ & Kỹ thuật
- **Dashboard Excel:** 
  - Ẩn đường lưới (gridlines) trên sheet `Dashboard` để tạo giao diện ứng dụng sạch sẽ.
  - Sử dụng font chữ hiện đại (Segoe UI hoặc Arial).
  - Không sử dụng màu sắc quá sặc sỡ, tuân thủ bảng màu cà phê chuyên nghiệp.
- **Mã nguồn Python:** Tách biệt rõ ràng các file script thu thập, làm sạch và tạo Excel để dễ bảo trì.

---

## 🔄 Quy trình PDCA áp dụng
1. **PLAN:** Thảo luận và thống nhất kế hoạch này với người dùng (USER).
2. **DO:** Thực hiện cào dữ liệu, xử lý và tạo file Excel + Báo cáo.
3. **CHECK:** Kiểm tra tính chính xác của công thức Excel, biểu đồ hiển thị đúng định dạng, các insight có logic và thực tế không.
4. **ACT:** Lưu nhật ký cải tiến vào `docs/pdca-log.md` và rút ra bài học cho các dự án sau.

---

## ❓ Câu hỏi cần làm rõ trước khi thực hiện
1. **Bảng màu Dashboard Excel:** Bạn có thích tông màu "Warm Coffee" (Nâu/Kem) không hay muốn một bảng màu khác (ví dụ: Sleek Blue hoặc Dark Mode)?
2. **Dữ liệu quán cà phê:** Bạn có muốn chỉ định trước bất kỳ quán cà phê lớn nào tại Quận 1 (ví dụ: The Workshop, Okkio, L'Usine...) vào danh sách thu thập không?
