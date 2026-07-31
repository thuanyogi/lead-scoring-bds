import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def load_env_file():
    """
    Tự động đọc file .env thủ công nếu thư viện python-dotenv chưa được cài đặt.
    """
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    # Loại bỏ dấu nháy đơn/kép bao quanh giá trị nếu có
                    val = val.strip().strip("'").strip('"')
                    os.environ[key.strip()] = val

# Nạp file cấu hình .env
load_env_file()

# Cố gắng nạp bằng thư viện dotenv chính thống nếu có
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Lấy các biến môi trường
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError(
        "Lỗi bảo mật: Thiếu cấu hình TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID trong file .env!\n"
        "Vui lòng sao chép file .env.example thành .env và điền thông tin kết nối hợp lệ."
    )

def escape_html(text):
    """
    Escape các ký tự HTML đặc biệt để tránh lỗi cú pháp parse_mode='HTML' của Telegram API.
    """
    if not text:
        return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def translate_to_vi(text):
    """
    Dịch văn bản từ tiếng Anh sang tiếng Việt sử dụng Google Translate API miễn phí (gtx)
    mà không cần dùng thư viện googletrans.
    """
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "vi",
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        # Parse kết quả JSON trả về từ Google Translate
        result = response.json()
        translated_text = "".join([sentence[0] for sentence in result[0] if sentence[0]])
        return translated_text
    except Exception as e:
        print(f"Lỗi khi dịch văn bản: {e}")
        return text

def get_ai_news(limit=3):
    """
    Lấy tin tức AI mới nhất từ Google News RSS (từ khóa: AI, OpenAI, Google AI).
    Trả về danh sách các tin tức (mặc định tối đa 3 tin).
    """
    try:
        url = "https://news.google.com/rss/search?q=AI+OR+OpenAI+OR+%22Google+AI%22&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse XML từ RSS Feed
        root = ET.fromstring(response.content)
        items = root.findall(".//item")
        
        if not items:
            print("Không tìm thấy tin tức nào từ RSS.")
            return []
        
        news_list = []
        for i in range(min(limit, len(items))):
            item = items[i]
            title = item.find("title").text
            link = item.find("link").text
            news_list.append({
                "title": title,
                "link": link
            })
        return news_list
    except Exception as e:
        print(f"Lỗi khi lấy tin tức từ Google News RSS: {e}")
        return []

def generate_ai_insight(news_list_vi):
    """
    Sinh insight/nhận xét ngắn gọn dựa trên các tiêu đề tin tức đã dịch.
    Sử dụng Gemini API nếu có cấu hình GEMINI_API_KEY trong file .env.
    Nếu không có, tự động phân tích và sinh nhận xét thông qua bộ phân tích từ khóa Rule-based.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            print("Đang gọi Gemini API để sinh insight...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            headers = {"Content-Type": "application/json"}
            
            prompt = (
                "Dựa trên các tiêu đề tin tức AI dưới đây, hãy đưa ra một câu nhận định/insight ngắn gọn "
                "(khoảng 30-50 từ) bằng tiếng Việt phân tích xu hướng chung hoặc mối liên kết giữa các tin này. "
                "Yêu cầu phản hồi ngắn, cô đọng, chuyên nghiệp và chỉ chứa câu nhận định trực tiếp, không thêm lời dẫn:\n"
            )
            for idx, title in enumerate(news_list_vi, 1):
                prompt += f"{idx}. {title}\n"
                
            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            insight_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            return insight_text
        except Exception as e:
            print(f"Không thể gọi Gemini API sinh insight ({e}). Chuyển sang fallback tự động...")
            
    # Cơ chế fallback Rule-based phân tích từ khóa thông minh
    keywords = {
        "china": ["Trung Quốc", "Alibaba", "Tencent", "Baidu", "Huawei"],
        "openai": ["OpenAI", "ChatGPT", "GPT", "Sora"],
        "google": ["Google", "Gemini", "DeepMind", "Alphabet"],
        "safety": ["bảo mật", "danh sách đen", "pháp lý", "chính phủ", "quy định", "bản quyền", "hạn chế", "án phạt"],
        "chips": ["Nvidia", "chip", "bán dẫn", "Intel", "AMD"],
        "agent": ["agent", "trợ lý", "tác nhân", "tự động hóa"]
    }
    
    found = set()
    for title in news_list_vi:
        title_lower = title.lower()
        for key, words in keywords.items():
            if any(w.lower() in title_lower for w in words):
                found.add(key)
                
    insights = []
    if "china" in found and "safety" in found:
        insights.append("Mâu thuẫn địa chính trị và quy định kiểm soát công nghệ AI đang siết chặt, khiến các ông lớn Mỹ lẫn Trung Quốc phải tìm cách tối ưu hóa hoặc tự chủ phần cứng.")
    elif "china" in found:
        insights.append("Sự vươn lên mạnh mẽ của các tập đoàn công nghệ Trung Quốc như Alibaba đang đẩy cuộc cạnh tranh mô hình AI toàn cầu sang giai đoạn khốc liệt mới.")
    elif "safety" in found:
        insights.append("Các vấn đề về pháp lý, bảo mật dữ liệu và đạo đức AI đang trở thành trọng tâm xem xét hàng đầu khi công nghệ AI thâm nhập sâu vào các tổ chức lớn.")
    
    if "openai" in found or "google" in found:
        insights.append("Cuộc đua nâng cấp tính năng mô hình nền tảng đang chuyển hướng mạnh mẽ sang việc tối ưu hóa ứng dụng thực tế và thị trường thương mại toàn cầu.")
    if "chips" in found:
        insights.append("Cơn khát chip bán dẫn và năng lực hạ tầng tính toán (GPU) vẫn là yếu tố xương sống quyết định vị thế của các bên trong cuộc đua AI.")

    if not insights:
        insights.append("Các xu hướng tin tức phản ánh sự dịch chuyển rõ rệt của ngành AI từ các nghiên cứu lý thuyết sang giai đoạn ứng dụng thực tế sâu rộng vào đời sống và doanh nghiệp.")

    return " ".join(insights[:2])

def send_telegram(message):
    """
    Gửi tin nhắn đã format vào Telegram sử dụng requests với parse_mode='HTML'.
    """
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True  # Ẩn preview link giúp tin nhắn gọn gàng, chuyên nghiệp
        }
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        print("Gửi tin nhắn Telegram thành công!")
        return True
    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn Telegram: {e}")
        return False

def main():
    print("--- Khởi động Workflow OIPO ---")
    
    # 1. Lấy 3 tin tức mới nhất từ RSS
    print("Đang lấy 3 tin tức AI mới nhất từ Google News RSS...")
    news_list = get_ai_news(limit=3)
    if not news_list:
        print("Workflow kết thúc do không lấy được tin tức.")
        return
        
    print(f"Đã lấy được {len(news_list)} tin tức.")
    
    # 2. Xử lý dịch thuật và định dạng nội dung HTML
    titles_vi = []
    message_items = []
    today_str = datetime.now().strftime("%d/%m/%Y")
    
    for idx, item in enumerate(news_list, 1):
        orig_title = item["title"]
        link = item["link"]
        
        # Tách tên nguồn ở cuối tiêu đề (nếu có, phân tách bằng dấu gạch ngang)
        source_name = "Google News"
        clean_title = orig_title
        if " - " in orig_title:
            parts = orig_title.rsplit(" - ", 1)
            clean_title = parts[0]
            source_name = parts[1]
            
        print(f"Đang xử lý tin {idx}: {clean_title}")
        
        # Dịch tiêu đề sang tiếng Việt
        translated_title = translate_to_vi(clean_title)
        titles_vi.append(translated_title)
        
        # Escape các ký tự đặc biệt tránh lỗi XML/HTML của Telegram
        esc_translated = escape_html(translated_title)
        esc_original = escape_html(clean_title)
        esc_source = escape_html(source_name)
        
        # Chọn icon số thứ tự
        num_icons = ["1️⃣", "2️⃣", "3️⃣"]
        icon = num_icons[idx-1] if idx-1 < len(num_icons) else "🔹"
        
        # Định dạng HTML cho từng tin tức
        item_html = (
            f"{icon} <b>{esc_translated}</b>\n"
            f"   <i>({esc_original})</i>\n"
            f"   👉 <a href=\"{link}\">Đọc tin tại {esc_source}</a>"
        )
        message_items.append(item_html)
        
    # 3. Sinh nhận xét / Insight xu hướng AI
    print("Đang phân tích và tạo nhận xét xu hướng AI...")
    insight = generate_ai_insight(titles_vi)
    esc_insight = escape_html(insight)
    
    # 4. Tổng hợp toàn bộ tin nhắn định dạng HTML
    message = (
        f"🧠 <b>BẢN TIN AI HÀNG NGÀY</b> 📅 <i>{today_str}</i>\n"
        f"───────────────────\n\n"
        f"{'\n\n'.join(message_items)}\n\n"
        f"───────────────────\n"
        f"💡 <b>INSIGHT XU HƯỚNG AI:</b>\n"
        f"<blockquote>{esc_insight}</blockquote>\n"
        f"#AI #TinCongNghe #Antigravity"
    )
    
    # 5. Gửi lên Telegram
    print("Đang gửi tin nhắn định dạng HTML vào Telegram...")
    send_telegram(message)

if __name__ == "__main__":
    main()
