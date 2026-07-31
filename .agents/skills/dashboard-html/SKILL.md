---
name: dashboard-html
description: Skill tạo Dashboard HTML hiện đại theo chuẩn thiết kế Glassmorphism, Dark Mode, KPI layout, phối màu tương phản neon/vibrant và hiệu ứng nhảy số Real-time (animated counters).
---

# Skill Tạo Dashboard HTML Hiện Đại (dashboard-html)

## Mission (Sứ mệnh)
Bạn là một **Senior UI/UX Engineer & Data Visualization Expert**.
Nhiệm vụ của bạn là tự động thiết kế và xuất file Dashboard HTML đơn (Single-file HTML) hoặc ứng dụng Dashboard web hoàn chỉnh với giao diện siêu hiện đại, đẳng cấp chuyên nghiệp ("WOW Factor"). 

Dashboard do bạn tạo ra phải tuân thủ nghiêm ngặt **5 bộ tiêu chuẩn vàng**:
1. **Glassmorphism UI**: Thẻ mờ hiệu ứng kính trong suốt (`backdrop-filter: blur`), viền vi nét glowing border, đổ bóng nổi 3D sâu.
2. **Dark Mode & Mesh Ambient Background**: Phông nền tối sẫm (`#080d16` / `#0f172a`) kết hợp hiệu ứng đèn dạ quang (Ambient Radial Glow) mượt mà.
3. **KPI Card Grid Layout**: Bố cục trực quan gồm Header live status, lưới thẻ chỉ số KPI số lớn, biểu đồ tương tác đa chiều và bảng log chi tiết.
4. **Phối màu tương phản Neon/Vibrant**: Màu sắc nổi bật trên nền tối (Cyan, Indigo, Emerald, Rose, Amber) đảm bảo độ tương phảnWCAG AA+, dễ đọc và gây ấn tượng mạnh.
5. **Hiệu ứng nhảy số Real-time (Counter Animation)**: Tự động đếm số từ 0 đến giá trị đích khi tải trang và hỗ trợ nút/bộ đếm cập nhật dữ liệu tự động (simulation loop).

---

## Input (Đầu vào)
Để kích hoạt skill này, Agent nhận các tham số hoặc câu lệnh của người dùng:

| Tham số | Kiểu dữ liệu | Mô tả | Mặc định / Ví dụ |
|---|---|---|---|
| **title** | `string` | Tiêu đề của Dashboard | *"Executive Performance Dashboard"* |
| **data_source** | `file_path` \| `json` \| `text` | File dữ liệu (Excel/CSV/JSON) hoặc mô tả chỉ số KPI | File dữ liệu hoặc mô tả dữ liệu bài toán |
| **theme_accent** | `string` | Tông màu chủ đạo (Cyan, Emerald, Indigo, Purple, Rose) | `"Cyan-Indigo"` |
| **output_path** | `file_path` | Đường dẫn file HTML đầu ra | `outputs/reports/dashboard.html` |
| **realtime_interval**| `number` (giây) | Tần số tự động giả lập nhảy số Real-time (0 = tắt) | `5` |

⛔ **Xử lý Edge Cases khi thiếu Input:**
- Nếu không có dữ liệu thực tế: Tự động khởi tạo bộ dữ liệu mẫu (synthetic mockup data) phù hợp với ngữ cảnh kinh doanh / hợp nhất BCTC / quản lý dự án của workspace.
- Nếu không chỉ định `output_path`: Lưu mặc định vào `outputs/reports/dashboard.html`.

---

## Context (Bối cảnh áp dụng)
- Dùng cho báo cáo quản trị cấp cao (CEO/CFO/Board Dashboard), theo dõi tiến độ dự án, báo cáo tài chính hợp nhất, tình hình bán hàng, hoặc báo cáo vận hành ERP.
- Yêu cầu sản phẩm đầu ra chạy độc lập trên mọi trình duyệt web (Chrome, Edge, Safari, Firefox), không đòi hỏi server backend phức tạp, có thể mở trực tiếp từ file hoặc host lên Vercel/GitHub Pages.

---

## Standard Specifications (Bộ tiêu chuẩn thiết kế)

### 1. Glassmorphism System Specs (CSS)
```css
:root {
  --bg-dark: #080d16;
  --glass-bg: rgba(15, 23, 42, 0.65);
  --glass-border: rgba(255, 255, 255, 0.08);
  --glass-hover-border: rgba(255, 255, 255, 0.2);
  --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
  --glass-glow: rgba(56, 189, 248, 0.15);
  
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;

  --accent-cyan: #38bdf8;
  --accent-indigo: #6366f1;
  --accent-emerald: #10b981;
  --accent-rose: #f43f5e;
  --accent-amber: #f59e0b;
}

body {
  background-color: var(--bg-dark);
  background-image: 
    radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.18) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.18) 0px, transparent 50%),
    radial-gradient(at 50% 100%, rgba(16, 185, 129, 0.12) 0px, transparent 50%);
  background-attachment: fixed;
  color: var(--text-primary);
  font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  margin: 0;
  padding: 24px;
}

.glass-card {
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  box-shadow: var(--glass-shadow);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
  border-color: var(--glass-hover-border);
  box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5), 0 0 25px var(--glass-glow);
  transform: translateY(-4px);
}
```

### 2. Live Pulse & Counter Animation Engine (JS)
```javascript
// Hàm đếm số Real-time mượt mà (Ease Out Cubic)
function animateCounter(element, targetValue, duration = 1500, prefix = '', suffix = '', decimals = 0) {
  let startTimestamp = null;
  const startValue = 0;
  
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const easeProgress = 1 - Math.pow(1 - progress, 3); // easeOutCubic
    const currentValue = startValue + (targetValue - startValue) * easeProgress;
    
    const formatted = currentValue.toLocaleString('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
    
    element.innerText = `${prefix}${formatted}${suffix}`;
    
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

// Khởi chạy nhảy số khi DOM tải xong
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-counter]').forEach(el => {
    const target = parseFloat(el.getAttribute('data-target') || '0');
    const prefix = el.getAttribute('data-prefix') || '';
    const suffix = el.getAttribute('data-suffix') || '';
    const decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    animateCounter(el, target, 1800, prefix, suffix, decimals);
  });
});
```

---

## Output Structure & Template HTML Master

Mọi file Dashboard HTML xuất ra bởi skill này phải áp dụng khung HTML Master chuẩn bên dưới:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{DASHBOARD_TITLE}}</title>
  <!-- Google Fonts & FontAwesome & Chart.js -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  
  <style>
    /* Nhúng Glassmorphism CSS ở trên */
    /* Utility CSS cho Grid, Badge, Pulse Dot, Chart container */
    .dashboard-container { max-width: 1440px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; }
    .header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; }
    .live-badge { display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; color: #10b981; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); padding: 6px 14px; border-radius: 20px; }
    .pulse-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; box-shadow: 0 0 10px #10b981; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); } 70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); } 100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } }

    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }
    .kpi-card { padding: 24px; display: flex; flex-direction: column; gap: 12px; position: relative; overflow: hidden; }
    .kpi-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
    .kpi-value { font-size: 32px; font-weight: 800; letter-spacing: -1px; margin-top: 4px; }
    .kpi-trend { font-size: 13px; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; border-radius: 6px; padding: 2px 8px; }
    .trend-up { color: #34d399; background: rgba(52, 211, 153, 0.1); }
    .trend-down { color: #f43f5e; background: rgba(244, 63, 94, 0.1); }

    .charts-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
    @media (max-width: 1024px) { .charts-grid { grid-template-columns: 1fr; } }
    .chart-card { padding: 24px; min-height: 380px; }

    .data-table-card { padding: 24px; overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; text-align: left; }
    th { padding: 14px 16px; font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); border-bottom: 1px solid var(--glass-border); }
    td { padding: 16px; font-size: 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.04); color: var(--text-secondary); }
    tr:hover td { background: rgba(255, 255, 255, 0.02); color: var(--text-primary); }
  </style>
</head>
<body>
  <div class="dashboard-container">
    <!-- Header -->
    <header class="glass-card header">
      <div>
        <h1 style="margin: 0; font-size: 24px; font-weight: 800; background: linear-gradient(135deg, #fff 30%, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
          {{DASHBOARD_TITLE}}
        </h1>
        <p style="margin: 4px 0 0 0; color: var(--text-muted); font-size: 13px;">{{SUBTITLE}}</p>
      </div>
      <div class="live-badge">
        <span class="pulse-dot"></span>
        <span>REALTIME STREAMING</span>
      </div>
    </header>

    <!-- KPI Grid -->
    <section class="kpi-grid">
      <!-- Thẻ KPI mẫu với data-counter -->
      <div class="glass-card kpi-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="color: var(--text-secondary); font-size: 14px; font-weight: 600;">Tổng Doanh Thu</span>
          <div class="kpi-icon" style="background: rgba(56, 189, 248, 0.15); color: var(--accent-cyan);">
            <i class="fa-solid fa-chart-line"></i>
          </div>
        </div>
        <div class="kpi-value" data-counter data-target="{{KPI_1_VALUE}}" data-prefix="$" data-decimals="0">0</div>
        <div style="display:flex; align-items:center; gap: 8px;">
          <span class="kpi-trend trend-up"><i class="fa-solid fa-arrow-up"></i> +14.2%</span>
          <span style="color: var(--text-muted); font-size: 12px;">so với tháng trước</span>
        </div>
      </div>
      <!-- Các thẻ KPI khác... -->
    </section>

    <!-- Charts Section -->
    <section class="charts-grid">
      <div class="glass-card chart-card">
        <h3 style="margin-top:0; font-size: 16px;">Xu Hướng Doanh Thu & Lợi Nhuận</h3>
        <canvas id="mainAreaChart"></canvas>
      </div>
      <div class="glass-card chart-card">
        <h3 style="margin-top:0; font-size: 16px;">Cấu Trúc Tỷ Trọng</h3>
        <canvas id="donutChart"></canvas>
      </div>
    </section>

    <!-- Data Table -->
    <section class="glass-card data-table-card">
      <h3 style="margin-top:0; font-size: 16px;">Nhật Ký Giao Dịch Mới Nhất</h3>
      <table>
        <thead>
          <tr>
            <th>Mã Đơn</th>
            <th>Khách Hàng</th>
            <th>Bộ Phận</th>
            <th>Giá Trị</th>
            <th>Trạng Thái</th>
          </tr>
        </thead>
        <tbody>
          <!-- Dynamic Rows -->
        </tbody>
      </table>
    </section>
  </div>

  <script>
    /* Nhúng JS Counter Animation & Chart.js Config ở đây */
  </script>
</body>
</html>
```

---

## Workflow Thực Hiện Của Agent (Step-by-Step)

1. **Bước 1: Phân tích Dữ liệu / Mô tả:**
   - Trích xuất các chỉ số KPI quan trọng nhất (Tổng số, % tăng trưởng, chỉ số mục tiêu).
   - Xác định bộ dữ liệu chuỗi thời gian cho biểu đồ (Trend chart) và phân bổ tỷ trọng (Donut/Bar chart).
2. **Bước 2: Phối màu & Theme Customization:**
   - Cấu hình màu sắc Neon Accent (Cyan `#38bdf8`, Emerald `#10b981`, Indigo `#6366f1`, Rose `#f43f5e`, Amber `#f59e0b`).
   - Thiết lập gradient mượt cho Chart.js canvas contexts (`createLinearGradient`).
3. **Bước 3: Tạo File HTML Hoàn Chỉnh:**
   - Tạo các thẻ KPI với thuộc tính `data-counter`, `data-target`, `data-prefix`, `data-suffix`.
   - Cấu hình biểu đồ Chart.js dark theme (lưới x/y màu mờ `rgba(255,255,255,0.05)`, tooltip Glassmorphism).
   - Tạo bảng dữ liệu với các badge trạng thái glowing.
   - Thêm nút / vòng lặp `setInterval` giả lập cập nhật dữ liệu nhảy số Real-time cứ mỗi 5 giây.
4. **Bước 4: Ghi File & Kiểm Tra Output:**
   - Ghi nội dung vào đường dẫn chỉ định (mặc định `outputs/reports/dashboard.html`).
   - Cung cấp đường dẫn tuyệt đối dạng `file://` cho người dùng xem lại.

---

## Validation Checklist (Tiêu chí kiểm thử thành công)
- [x] Background có gradient tối sẫm kết hợp các vùng sáng dạ quang (Ambient glow).
- [x] Thẻ card áp dụng hiệu ứng mờ kính `backdrop-filter: blur(16px)` và viền mờ `rgba(255,255,255,0.08)`.
- [x] Khi di chuột qua card có hiệu ứng nâng nhẹ (`translateY(-4px)`) và viền sáng phát quang.
- [x] Giá trị chỉ số KPI có hiệu ứng nhảy số mượt từ 0 đến giá trị thật trong 1.5 - 2 giây.
- [x] Có chấm xanh pulse nhấp nháy hiển thị trạng thái Real-time Live.
- [x] Biểu đồ Chart.js hiển thị đường cong mượt (`cubicInterpolationMode: 'monotone'`) kết hợp vùng phủ Gradient mờ bên dưới.
- [x] File HTML chạy hoàn toàn độc lập, mở ra hiển thị đúng giao diện trên mọi máy tính.
