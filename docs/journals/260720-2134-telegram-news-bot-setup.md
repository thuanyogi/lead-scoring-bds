---
title: "Telegram Bot Setup: Daily Schedule, .env Security & HTML formatting"
date: "2026-07-20T21:47:35+07:00"
author: "Vũ Đức Hoàng (AI Assistant)"
category: "automation"
---

# Journal Entry: Telegram Bot Setup: Daily Schedule, .env Security & HTML formatting

## Context
Thiết lập và cải tiến liên tục workflow lấy tin tức công nghệ AI tự động, dịch thuật tiếng Việt, tạo nhận xét xu hướng và gửi thông báo qua Telegram. Workflow yêu cầu chạy định kỳ hàng ngày, bảo mật các thông tin nhạy cảm, và hiển thị thông tin trực quan, trực tiếp, chuyên nghiệp trên Telegram.

---

## What Happened
1. **Thiết lập mã nguồn Python cốt lõi:**
   * Tạo script [send_telegram.py](file:///Users/thuanyogi/Downloads/_Project/AA/plans/260710-workspace-bridge/workspace-hv-v2/my-workspace/send_telegram.py).
   * Viết hàm `get_ai_news(limit=3)` parse XML của Google News RSS, nâng số lượng tin thu thập lên tối đa 3 tin tức mới nhất.
   * Viết hàm `translate_to_vi()` dịch thuật nhanh và không cần API key thông qua `gtx` Web API của Google.
   * Thiết lập hàm `escape_html()` làm sạch nội dung tin tức, bảo vệ bot khỏi lỗi cú pháp HTML đặc biệt.
2. **Cấu hình bảo mật thông tin (.env):**
   * Tách biệt các khóa bảo mật nhạy cảm (`BOT_TOKEN`, `CHAT_ID`) ra file [.env](file:///Users/thuanyogi/Downloads/_Project/AA/plans/260710-workspace-bridge/workspace-hv-v2/my-workspace/.env).
   * Tạo file mẫu [.env.example](file:///Users/thuanyogi/Downloads/_Project/AA/plans/260710-workspace-bridge/workspace-hv-v2/my-workspace/.env.example) và cấu hình [.gitignore](file:///Users/thuanyogi/Downloads/_Project/AA/plans/260710-workspace-bridge/workspace-hv-v2/my-workspace/.gitignore) để bỏ qua file môi trường thực.
   * Viết hàm fallback `load_env_file()` nạp động biến từ `.env` mà không ép buộc phải cài gói `python-dotenv`.
3. **Tích hợp phân tích insight tự động:**
   * Xây dựng hàm `generate_ai_insight(news_list_vi)` nạp từ khóa phân tích theo cơ chế Rule-based thông minh nhằm đưa ra nhận định xu hướng nổi bật (địa chính trị, bảo mật AI, cuộc đua mô hình, hạ tầng GPU).
   * Hỗ trợ gọi mô hình Gemini chuyên sâu (thông qua `GEMINI_API_KEY` nếu được khai báo trong `.env`).
4. **Trang trí và nâng cấp giao diện Telegram (HTML):**
   * Sử dụng định dạng HTML với các thẻ cấu trúc (`<b>`, `<i>`, `<blockquote>`, `<a>`) và phân cách dòng bằng thanh ngang `───────────────────`.
   * Sử dụng icon số lớn (`1️⃣`, `2️⃣`, `3️⃣`) và icon chỉ hướng để phân biệt rõ ràng các bài tin.
   * Kích hoạt `"disable_web_page_preview": True` để ẩn các khối preview link cồng kềnh từ Telegram.
5. **Lập lịch tự động hóa:**
   * Đăng ký cron job `0 10 * * *` thông qua Agent Scheduler để tự động chạy script lúc 10h sáng hàng ngày (Giờ Việt Nam).
6. **Nhật ký cải tiến:**
   * Ghi nhận đầy đủ PDCA Log #4, #5 và #6 vào file [pdca-log.md](file:///Users/thuanyogi/Downloads/_Project/AA/plans/260710-workspace-bridge/workspace-hv-v2/my-workspace/docs/pdca-log.md).

---

## Reflection
* **Tối giản hóa thư viện:** Việc sử dụng module `xml.etree.ElementTree` của thư viện chuẩn Python thay thế cho `feedparser` giúp giảm bớt phụ thuộc thư viện ngoài và tối ưu hóa tốc độ load.
* **Độ ổn định của API dịch thuật:** Chuyển đổi từ `googletrans` sang `gtx` API giúp loại bỏ hoàn toàn các lỗi chặn kết nối và lỗi token thường thấy, tạo trải nghiệm ổn định cho bot.
* **Xử lý ký tự đặc biệt:** Telegram API thường phát sinh lỗi Parse BadRequest nếu tiêu đề hoặc link chứa ký tự Markdown đặc biệt. Sử dụng định dạng Plain text giúp giải quyết triệt để lỗi này trong khi link nguồn vẫn click được bình thường.
* **Trang trí giao diện tinh tế:** Việc ẩn preview link thông qua API và định dạng khối trích dẫn thụt dòng (`<blockquote>`) cho phần Insight giúp bố cục tin nhắn trông vô cùng gọn gàng, mang tính mỹ thuật và chuyên nghiệp cao.
* **Bảo mật và Tương thích:** Việc tách key ra `.env` kết hợp fallback tự parse giúp hệ thống vừa an toàn vừa độc lập, dễ triển khai ở mọi nơi.

---

## Decisions
1. **Sử dụng định dạng HTML thay thế Plain Text:** Chuyển sang sử dụng `parse_mode="HTML"` kết hợp bắt buộc với hàm làm sạch dữ liệu `escape_html()` để đảm bảo giao diện đẹp nhưng vẫn tuyệt đối an toàn.
2. **Ẩn xem trước liên kết (disable_web_page_preview):** Giúp bản tin thu gọn diện tích, tập trung vào text và các liên kết hành động.
3. **Quản lý cấu hình nhạy cảm qua biến môi trường:** Loại bỏ hoàn toàn hardcode Token và Chat ID khỏi file mã nguồn chính.

---

## Next Steps
* Theo dõi hoạt động của cron job vào lúc 10h sáng hàng ngày để đảm bảo bot chạy trơn tru.
* Người dùng có thể tùy ý khai báo thêm `GEMINI_API_KEY=your_key` vào file `.env` bất kỳ lúc nào để chuyển đổi cơ chế sinh Insight từ Rule-based sang dùng mô hình AI Gemini chuyên sâu.
