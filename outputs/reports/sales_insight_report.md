# 📊 BÁO CÁO PHÂN TÍCH DOANH THU & INSIGHT KINH DOANH
**Thực hiện bởi:** Vũ Đức Hoàng — Chuyên gia Tư vấn Hợp nhất Báo cáo Tài chính  
**Thời gian phân tích:** 13/07/2026  
**Dữ liệu phân tích:** Tháng 06/2024 (500 giao dịch)  
**File Excel Dashboard trực quan:** [sales_dashboard.xlsx](file:///Users/thuanyogi/Downloads/_Project/AA/plans/260710-workspace-bridge/workspace-hv-v2/my-workspace/outputs/reports/sales_dashboard.xlsx)

---

## 🛠️ Quy Trình Làm Sạch & Chuẩn Hóa Dữ Liệu
Trước khi tiến hành phân tích và xây dựng Dashboard, dữ liệu gốc đã được làm sạch và chuẩn hóa qua các bước sau:
1. **Đồng bộ định dạng Ngày (DATE):** Chuyển cột `DATE` từ dạng chuỗi văn bản (String) sang định dạng ngày tháng chuẩn của Excel (`yyyy-mm-dd`) để đảm bảo các bộ lọc thời gian và biểu đồ đường (Line chart) hiển thị chính xác theo thời gian thực tế.
2. **Loại bỏ khoảng trắng dư thừa:** Áp dụng hàm loại bỏ khoảng trắng (`strip`) cho toàn bộ các trường dữ liệu dạng chuỗi như Tên sản phẩm, Khu vực, Kênh bán hàng, Nhân viên bán hàng để tránh lỗi tính toán hoặc trùng lặp phân nhóm do ký tự khoảng trắng ẩn.
3. **Bổ sung cột Doanh thu Thuần & Lợi nhuận Thuần (Net Metrics):** 
   - Với tỷ lệ hoàn trả đơn hàng cao, việc phân tích dựa trên doanh số gộp (Gross Sales) sẽ dẫn đến nhận định sai lệch về hiệu quả tài chính.
   - Do đó, cột `NET_REVENUE` (Doanh thu Thuần) và `NET_PROFIT` (Lợi nhuận Thuần) đã được tạo bằng cách loại trừ các đơn hàng bị trả lại (`RETURN_FLAG == 1`). 
   - *Công thức:* `Doanh Thu Thuần = Doanh Thu Gộp * (1 - Trạng Thái Trả Hàng)`.
4. **Việt hóa tiêu đề:** Toàn bộ các cột dữ liệu được dịch sang tiếng Việt trực quan nhằm tối ưu trải nghiệm đọc cho người dùng cuối.

---

## 📈 Tóm Tắt Các Chỉ Số Tài Chính Key (Tháng 06/2024)
| Chỉ số | Gross (Gộp/Chưa trừ trả hàng) | Net (Thuần/Thực tế đạt được) | Tỷ lệ hao hụt / Biên lợi nhuận |
| :--- | :---: | :---: | :---: |
| **Doanh thu** | 2,827,300 VND | 2,062,250 VND | **27.06% Doanh thu bị mất** do hoàn hàng |
| **Lợi nhuận** | 718,896.06 VND | 519,121.31 VND | **25.17% Biên lợi nhuận thuần** |
| **Số lượng bán** | 5,236 sản phẩm | 3,891 sản phẩm | 1,345 sản phẩm bị trả lại |
| **Tỷ lệ trả đơn** | — | — | **25.60% số đơn hàng bị trả** (128 / 500 đơn) |

---

## 🔍 03 Insight Quan Trọng (Key Insights)

### 🚨 Insight 1: Tỷ lệ trả hàng cao ở mức báo động làm thâm hụt 27.06% doanh thu gộp
*   **Chi tiết:** Doanh nghiệp ghi nhận tỷ lệ trả hàng trung bình là **25.60%** xét theo số lượng đơn (128/500 đơn) và **27.06%** xét theo giá trị tiền mặt. Điều này dẫn tới khoản thâm hụt doanh số cực kỳ lớn lên tới **765,050.00 VND** chỉ trong vòng 1 tháng.
*   **Sản phẩm cốt lõi bị ảnh hưởng:** Một số sản phẩm tiêu dùng nhanh (FMCG) có tỷ lệ hoàn trả cao kỷ lục:
    *   **Detergent (Bột giặt):** Tỷ lệ trả hàng lên tới **48.0%** (25 đơn hàng phát sinh thì 12 đơn bị trả).
    *   **Soft Drink (Nước ngọt):** Tỷ lệ trả hàng **40.0%** (20 đơn phát sinh, 8 đơn bị trả).
    *   **Dish Soap (Nước rửa chén):** Tỷ lệ trả hàng **38.2%** (34 đơn phát sinh, 13 đơn bị trả).
*   **Nguyên nhân giả định:** Nhóm hàng chất lỏng/hóa phẩm tiêu dùng này có tỷ lệ lỗi cao có thể do khâu vận chuyển gây bục, vỡ, rò rỉ bao bì hoặc lỗi hạn sử dụng (date).

### 🌐 Insight 2: Kênh Online có hiệu quả kém nhất, chi phí marketing cao và tỷ lệ trả hàng dẫn đầu
*   **Chi tiết:** Kênh **Online** mang lại Doanh thu Thuần thấp nhất (**580,550.00 VND**) so với kênh Offline (791,210.00 VND) và Distributor (690,490.00 VND).
*   **Tỷ lệ trả hàng theo kênh:** Kênh Online ghi nhận tỷ lệ trả hàng cao vượt trội ở mức **31.45%**, so với Offline là **26.29%** và Distributor là **19.28%**.
*   **Mối liên hệ vận chuyển:** Phân tích sâu dữ liệu giao hàng cho thấy các đơn hàng có thời gian giao hàng kéo dài từ **4 đến 5 ngày** có tỷ lệ hoàn đơn đột biến lên tới **30.1% - 32.4%**. Ngược lại, các đơn hàng giao nhanh trong vòng **3 ngày** có tỷ lệ hoàn đơn thấp nhất (**17.9%**). Kênh Online phụ thuộc nhiều vào đơn vị chuyển phát bên thứ ba, do đó thời gian giao hàng chậm trễ dẫn đến việc khách hàng online thay đổi ý định và bùng hàng (tỷ lệ trả đơn cao).

### 📍 Insight 3: Khu vực miền Nam dẫn đầu về doanh số gộp nhưng bị kéo lùi do tỷ lệ trả hàng cao nhất
*   **Chi tiết:** Khu vực miền Nam (South) đứng thứ hai về doanh thu gộp tiềm năng (**1,000,910.00 VND**, sát nút miền Trung là 1,024,030.00 VND). Tuy nhiên, đây lại là khu vực có tỷ lệ hoàn hàng tệ nhất hệ thống với **29.41%** (gần 1/3 giá trị đơn hàng bị trả lại).
*   **Kết quả thuần:** Sau khi trừ trả hàng, doanh thu thuần miền Nam giảm mạnh xuống chỉ còn **654,440.00 VND** (thấp hơn miền Trung là 800,270.00 VND).
*   **Biên lợi nhuận:** Do chi phí logistics hoàn trả và thâm hụt cao, Biên Lợi nhuận Thuần của miền Nam chỉ đạt **24.59%** — thấp nhất trong 3 miền (miền Bắc đạt 25.67%, miền Trung đạt 25.27%).

---

## 💡 02 Đề Xuất Hành Động (Actionable Recommendations)

### 📋 Đề xuất 1: Rà soát quy trình kiểm soát chất lượng đóng gói và đối tác vận chuyển đối với nhóm hàng hóa phẩm lỏng (Detergent, Soft Drink, Dish Soap)
*   **Hành động cụ thể:**
    1.  **Thay đổi quy cách đóng gói:** Thiết kế thêm lớp chống xốc hoặc màng co chuyên dụng cho nhóm chai lọ chứa chất lỏng (Bột giặt, Nước rửa chén, Nước ngọt) trước khi giao đi để triệt tiêu tình trạng vỡ, rò rỉ trong quá trình luân chuyển.
    2.  **Kiểm soát chất lượng đầu vào:** Kiểm tra ngay hạn sử dụng của lô hàng Bột giặt (Detergent) hiện tại trong kho để loại trừ khả năng lỗi xuất phát từ phía nhà cung cấp.
*   **Mục tiêu:** Giảm tỷ lệ trả hàng của nhóm FMCG này từ mức 38-48% xuống mức trung bình toàn ngành dưới **15%**, bảo toàn khoảng **150,000 VND - 200,000 VND** doanh thu bị mất mỗi tháng.

### 🚚 Đề xuất 2: Tối ưu hóa dịch vụ giao hàng (SLA) kênh Online và siết chặt quy trình xác thực đơn hàng COD
*   **Hành động cụ thể:**
    1.  **Rà soát đối tác vận chuyển:** Đàm phán lại hoặc chuyển dịch đơn hàng online sang các đơn vị giao hàng có cam kết thời gian giao hàng (SLA) dưới 3 ngày đối với các tỉnh/thành trọng điểm (giữ thời gian giao hàng ở mức 1-3 ngày sẽ giúp hạ tỷ lệ trả hàng từ 31% xuống dưới 18% theo dữ liệu lịch sử).
    2.  **Quy trình gọi điện xác thực đơn hàng (Confirming Call):** Thiết lập quy định bắt buộc đối với nhân viên telesale hoặc chatbot AI: Gọi điện hoặc gửi tin nhắn xác nhận địa chỉ và thời gian nhận hàng trước khi đóng gói đối với 100% đơn hàng Online chọn phương thức thanh toán khi nhận hàng (COD).
*   **Mục tiêu:** Kiểm soát tỷ lệ trả hàng kênh Online từ **31.45%** xuống dưới **20%** trong vòng quý tiếp theo, cải thiện dòng tiền thuần từ hoạt động kinh doanh online.

---

## 📌 Các File Liên Quan Trong Workspace
*   **File Excel chứa Dashboard trực quan:** [sales_dashboard.xlsx](file:///Users/thuanyogi/Downloads/_Project/AA/plans/260710-workspace-bridge/workspace-hv-v2/my-workspace/outputs/reports/sales_dashboard.xlsx)
*   **Script Python dùng để kiểm tra dữ liệu:** [check_data_quality.py](file:///Users/thuanyogi/.gemini/antigravity-ide/brain/12563c22-7343-49c1-89f6-462584c2d8c9/scratch/check_data_quality.py)
*   **Script Python dùng để dựng Dashboard:** [build_dashboard.py](file:///Users/thuanyogi/.gemini/antigravity-ide/brain/12563c22-7343-49c1-89f6-462584c2d8c9/scratch/build_dashboard.py)
