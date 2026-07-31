# FPT CFS - Giải Pháp Hợp Nhất Báo Cáo Tài Chính (Financial Consolidation Solution)
**Tài liệu Hướng dẫn Sử dụng & Vận hành Hệ thống v2.0.3 (Phiên bản Tài liệu 1.06 - 14/03/2025)**

---

## 1. Tổng Quan Hệ Thống / System Overview
- **Tên Hệ Thống / System Name:** Giải pháp Hợp nhất Báo cáo Tài chính FPT CFS (FPT Financial Consolidation Solution)
- **Phiên bản Phần mềm / Software Version:** 2.0.3
- **Phiên bản Tài liệu / Manual Version:** 1.06 (Phát hành ngày 14/03/2025)
- **Quy mô Tài liệu / Document Scope:** 112 Trang Hướng dẫn Vận hành Nghiệp vụ Chi tiết
- **Đơn vị Phát triển / Vendor:** Công ty Cổ phần FPT / FPT Information System (FPT IS)
- **Chuẩn mực Áp dụng / Accounting Standards:** VAS 25 (Chuẩn mực Kế toán Việt Nam về BCTC Hợp nhất) & IFRS 10 (Consolidated Financial Statements)

---

## 2. Các Tính Năng & Module Cốt Lõi / Core Features & Capabilities

1. **Quản lý Cây Hợp Nhất & Phạm Vi Hợp Nhất (Consolidation Tree & Scope Management):**
   - Quản lý đa cấp Nút Hợp Nhất (Consolidation Nodes) từ Công ty mẹ tối cao đến các Công ty con, Công ty liên kết, Chi nhánh.
   - Linh hoạt cập nhật tỷ lệ sở hữu (Direct & Indirect Ownership), tỷ lệ quyền biểu quyết/kiểm soát (Control Ratio), và phương pháp hợp nhất (Hợp nhất toàn phần, Phương pháp Vốn chủ sở hữu equity method, Hợp nhất theo tỷ lệ).

2. **Tự Động Đồng Bộ Dữ Liệu Kế Toán (Automated Data Synchronization & ERP Connectors):**
   - Tích hợp đa nền tảng ERP/Phần mềm kế toán: SAP S/4HANA, Oracle EBS, Microsoft Dynamics 365, Fast, Bravo, MISA, và kết nhập File Excel chuẩn hóa.
   - Cơ chế Đồng bộ theo lịch tự động (Scheduled Sync) hoặc Đồng bộ thủ công theo nhu cầu (On-demand Sync).
   - Tự động map Bảng hệ thống tài khoản riêng (CoA riêng) sang Bảng hệ thống tài khoản Tập đoàn (CoA Tập đoàn/Hợp nhất).

3. **Chuyển Đổi Tiền Tệ Đa Ngoại Tệ (Multi-Currency FX Translation Engine):**
   - Tự động quy đổi BCTC từ đồng tiền ghi sổ (Functional Currency) sang đồng tiền báo cáo (Reporting Currency - VND/USD/EUR...).
   - Áp dụng Tỷ giá Bảng Cân đối Kế toán (Tỷ giá cuối kỳ BS), Tỷ giá Báo cáo KQKD (Tỷ giá bình quân/thực tế PL), và Tỷ giá lịch sử Vốn chủ sở hữu.
   - Tự động hạch toán Chênh lệch tỷ giá do chuyển đổi BCTC vào tài khoản Chênh lệch tỷ giá thuộc Vốn CSH (OCI).

4. **Xử Lý & Loại Trừ Giao Dịch Nội Bộ IC (Intercompany Elimination Engine):**
   - Tự động quét và khớp giao dịch nội bộ (Doanh thu - Chi phí, Phải thu - Phải trả, Cổ tức được chia, Đầu tư - Vốn góp).
   - Cơ chế phát hiện lệch dòng (Mismatch Detection) & hỗ trợ xử lý giao dịch đại lý (Agency Transactions).
   - Tự động sinh Bút toán loại trừ IC ở cấp Nút hợp nhất tương ứng.

5. **Xử Lý Lợi Nhuận Chưa Thực Hiện (Unrealized Profit - UPR Elimination):**
   - Khai báo và tự động loại trừ Lợi nhuận nội bộ chưa thực hiện trong Hàng tồn kho và Tài sản cố định.
   - Tự động phân bổ lại thuế TNDN hoãn lại (Deferred Tax) phát sinh từ bút toán loại trừ UPR.

6. **Phân Bổ Lợi Thế Thương Mại & Cổ Đông Không Kiểm Soát (Goodwill & NCI Management):**
   - Tự động tính toán Lợi thế Thương mại (Goodwill) khi mua công ty con hoặc thay đổi tỷ lệ sở hữu.
   - Khai báo và phân bổ khấu hao/suy giảm giá trị Lợi thế Thương mại và giá trị hợp lý tài sản thuần.
   - Tự động tính toán và kiểm tra Lợi ích của cổ đông không kiểm soát (NCI - Non-Controlling Interest) trên BS và PL.

7. **Kiểm Tra Chéo Đẳng Thức & Kiểm Soát Rủi Ro (100% Automated Cross-Checking Validation):**
   - Hệ thống tự động chạy 100+ kịch bản kiểm tra chéo (Cross-check): Cân đối BS, Cân đối BS-PL, Cân đối Lưu chuyển tiền tệ (CF), Cân đối Thuyết minh.
   - Cảnh báo trực quan theo mã màu khi phát hiện sai số hoặc mất cân đối kế toán.

---

## 3. Quy Trình Vận Hành Hợp Nhất 5 Bước / 5-Phase Consolidation Process

```
[ BƯỚC 1: BẮT ĐẦU KỲ ] ➔ [ BƯỚC 2: CHUẨN BỊ DỮ LIỆU ] ➔ [ BƯỚC 3: ĐỐI CHIẾU & QUY ĐỔI ] ➔ [ BƯỚC 4: ĐIỀU CHỈNH HỢP NHẤT ] ➔ [ BƯỚC 5: PHÁT HÀNH BÁO CÁO ]
```

### Bước 1: Bắt Đầu Kỳ Kế Toán (Period Initialization)
- Mở kỳ kế toán mới, đóng kỳ kế toán cũ để bảo vệ dữ liệu.
- Hệ thống tự động mang sang số dư đầu kỳ (Carry Forward Balance) cho các tài khoản BS.
- Khai báo Tỷ giá chuyển đổi BCTC (BS Rate & PL Rate) với chế độ quy đổi Nhân/Chia linh hoạt.
- Cập nhật Phạm vi hợp nhất (Tỷ lệ sở hữu, tỷ lệ kiểm soát, phương pháp hợp nhất, mã số thuế).

### Bước 2: Chuẩn Bị & Đồng Bộ Dữ Liệu (Data Preparation & Sync)
- Đảm bảo dữ liệu tại các bộ sổ kế toán riêng đã hoàn tất chốt sổ.
- Đồng bộ dữ liệu tự động từ các phần mềm kế toán/ERP lên CFS.
- Chuẩn hóa và map tài khoản riêng sang tài khoản CoA Tập đoàn.
- Kiểm tra tính đầy đủ và cân đối của Bảng cân đối phát sinh riêng (Trial Balance).

### Bước 3: Chuyển Đổi Tiền Tệ & Đối Chiếu Nội Bộ (FX Translation & IC Reconciliation)
- Hệ thống chạy chuyển đổi BCTC ngoại tệ tự động; ghi nhận Chênh lệch tỷ giá OCI.
- Chạy công cụ quẹt đối chiếu giao dịch nội bộ IC (Phải thu - Phải trả, Doanh thu - Chi phí).
- Khai báo bổ sung các thông tin giao dịch đại lý, giao dịch ủy thác.
- Khai báo thông tin Lợi nhuận chưa thực hiện (UPR) trong hàng tồn kho và TSCĐ mua bán nội bộ.

### Bước 4: Điều Chỉnh Hợp Nhất & Bút Toán Loại Trừ (Consolidation Adjustments)
- Khai báo giao dịch đầu tư vốn (góp vốn mới, mua/bán cổ phần con, chia cổ tức cổ phiếu, mua cổ phiếu quỹ).
- Hệ thống tự động sinh bút toán khử vốn đầu tư vào công ty con & ghi nhận NCI ban đầu.
- Phân bổ Lợi thế thương mại (Goodwill) & Phân bổ chênh lệch giá trị hợp lý tài sản.
- Loại trừ Doanh thu/Giá vốn nội bộ & Phân bổ Lợi nhuận nội bộ chưa thực hiện (UPR).
- Tính toán và phân bổ Lợi ích Cổ đông không kiểm soát (NCI) kỳ hiện tại.
- Ghi nhận các Bút toán điều chỉnh hợp nhất thủ công (nếu có).

### Bước 5: Kiểm Tra & Phát Hành Báo Cáo Tài Chính (Validation & Report Issuance)
- Xuất các Báo cáo Tài chính Hợp nhất chuẩn hóa: BS, PL, CF (Trực tiếp & Gián tiếp).
- Xuất Thuyết minh Báo cáo Tài chính Hợp nhất & Bảng Cân đối Phát sinh Hợp nhất.
- Chạy hệ thống Kiểm Tra Chéo (Cross-Check): Đảm bảo 100% đẳng thức cân đối kế toán.
- Khóa sổ kỳ hợp nhất và phê duyệt phát hành BCTC Hợp nhất.

---

## 4. Bộ Báo Cáo Tài Chính Hợp Nhất / Consolidated Financial Reporting Suite

1. **Bảng Cân Đối Kế Toán Hợp Nhất (Consolidated Balance Sheet - BS):**
   - Tổng Tài Sản = Tổng Nợ Phải Trả + Vốn Chủ Sở Hữu (Bao gồm VCSH Mẹ + NCI).
   - Hiển thị chi tiết Chênh lệch Tỷ giá Chuyển đổi BCTC và Lợi thế Thương mại.
2. **Báo Cáo Kết Quả Hoạt Động Kinh Doanh Hợp Nhất (Consolidated Profit & Loss - PL):**
   - Loại trừ 100% doanh thu & chi phí nội bộ tập đoàn.
   - Phân chia Lợi nhuận sau thuế: Cổ đông Công ty mẹ & Cổ đông không kiểm soát (NCI).
3. **Báo Cáo Lưu Chuyển Tiền Tệ Hợp Nhất (Consolidated Cash Flow - CF):**
   - Hỗ trợ phương pháp Trực tiếp & Gián tiếp.
   - Loại trừ dòng tiền từ các giao dịch nội bộ tập đoàn.
4. **Thuyết Minh Báo Cáo Tài Chính Hợp Nhất (Consolidated FS Notes):**
   - Chi tiết biến động Vốn chủ sở hữu, danh sách các công ty con/liên kết.
   - Chi tiết giao dịch với các bên liên quan (Related Party Transactions).
5. **Nhật Ký Bút Toán Loại Trừ & Bảng Cân Đối Phát Sinh Hợp Nhất (Elimination Journals & Consolidated TB):**
   - Minh bạch toàn bộ đường đi dữ liệu (Audit Trail) từ sổ riêng → Bút toán loại trừ → BCTC Hợp nhất.

---

## 5. Danh Mục Kiểm Tra Chéo 100% (100% Audit Validation Checklist)

| STT | Tên Kiểm Tra Chéo | Công Thức Kiểm Tra | Trạng Thái Cân Đối |
| :---: | :--- | :--- | :---: |
| 1 | Cân đối BS | `Tổng Tài Sản - (Tổng Nợ + Vốn CSH)` | `= 0` |
| 2 | Cân đối BS - PL | `Lợi nhuận CPH trên BS - LNST lũy kế trên PL` | `= 0` |
| 3 | Khớp IC Phải thu/Trả | `Tổng Phải thu Nội bộ - Tổng Phải trả Nội bộ` | `= 0` |
| 4 | Khớp IC Doanh thu/Chi phí | `Tổng Doanh thu Nội bộ - Tổng Chi phí Nội bộ` | `= 0` |
| 5 | Cân đối NCI | `NCI BS - (Tỷ lệ NCI * VCSH con + Điều chỉnh GVHL)` | `= 0` |
| 6 | Cân đối Lưu Chuyển Tiền | `Tiền & Tương đương tiền cuối kỳ CF - Tiền trên BS` | `= 0` |

---

## 6. Citations & References
- PDF Source: *FPT CFS User Guide & Operations Manual (v1.06, 14/03/2025, Software v2.0.3)*
- Target File URL: `https://drive.google.com/file/d/13YP7FMkQ9L7lTLcOI9qocrXoNQ2au98F/view`
- Standard Regulations: VAS 25 (Vietnam Accounting Standard 25) & IFRS 10 (Consolidated Financial Statements).
