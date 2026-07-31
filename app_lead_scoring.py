import streamlit as st
import pandas as pd
import re
import os
import io
import requests
import plotly.express as px
import plotly.graph_objects as go

# Google Auth imports for private Google Sheets access
try:
    from google.oauth2 import service_account
    import google.auth.transport.requests
    HAS_GOOGLE_AUTH = True
except ImportError:
    HAS_GOOGLE_AUTH = False

# ---------------------------------------------------------
# CONSTANTS & PATHS
# ---------------------------------------------------------
DEFAULT_SHEET_URL = "https://docs.google.com/spreadsheets/d/1WUvvkEBjt23qyzcnTK0OmAqGip5KPSX0UCdYGl57gRc/export?format=csv&gid=1542775777"
KNOWLEDGE_FILE_PATH = os.path.join("knowledge-base", "tieu_chi_cham_diem.txt")

# ---------------------------------------------------------
# HELPER & SCORING FUNCTIONS
# ---------------------------------------------------------
def load_raw_data_from_sheets(sheet_url=DEFAULT_SHEET_URL):
    """
    Tải dữ liệu trực tiếp từ Google Sheets CSV Export URL.
    Hỗ trợ cả đọc công khai và tự động xác thực bằng Google Service Account (từ st.secrets) khi Sheet để chế độ riêng tư.
    """
    if not sheet_url or not sheet_url.strip():
        st.error("Vui lòng nhập đường dẫn Google Sheets hợp lệ.")
        return pd.DataFrame()

    # Tự động chuẩn hóa URL nhập vào sang dạng CSV export
    csv_url = sheet_url.strip()
    if "/edit" in csv_url or "docs.google.com/spreadsheets" in csv_url:
        match_id = re.search(r'/d/([a-zA-Z0-9-_]+)', csv_url)
        match_gid = re.search(r'[#&?]gid=([0-9]+)', csv_url)
        if match_id:
            sheet_id = match_id.group(1)
            gid = match_gid.group(1) if match_gid else "0"
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    headers = {}
    
    # 1. Tự động kiểm tra nếu có Google Service Account Credentials trong st.secrets
    if HAS_GOOGLE_AUTH:
        try:
            if "gcp_service_account" in st.secrets:
                sa_info = dict(st.secrets["gcp_service_account"])
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets.readonly',
                    'https://www.googleapis.com/auth/drive.readonly'
                ]
                creds = service_account.Credentials.from_service_account_info(sa_info, scopes=scopes)
                auth_req = google.auth.transport.requests.Request()
                creds.refresh(auth_req)
                headers["Authorization"] = f"Bearer {creds.token}"
        except Exception:
            pass

    # 2. Gửi yêu cầu HTTP tải dữ liệu CSV
    try:
        resp = requests.get(csv_url, headers=headers, timeout=15)
        
        # Xử lý khi gặp lỗi Unauthorized / Forbidden (HTTP 401 / 403)
        if resp.status_code in [401, 403]:
            st.error("🔒 **Lỗi kết nối Google Sheets: HTTP Error 401 (Unauthorized)**")
            st.markdown("""
            > **Giải thích nguyên nhân & Vấn đề nằm ở đâu?**
            > 
            > 1. **Vấn đề cốt lõi**: Trang tính Google Sheet của bạn hiện đang ở trạng thái **"Hạn chế" (Restricted)**.
            > 2. **Vì sao đã thêm Email Service Account mà vẫn lỗi 401?**  
            >    Khi bạn tải dữ liệu bằng link URL CSV (`/export?format=csv`), trình duyệt hoặc server sẽ gửi yêu cầu ẩn danh. Việc cấp quyền cho Email Service Account chỉ hoạt động khi ứng dụng đính kèm **OAuth Access Token** trong Header yêu cầu. Nếu không có Token xác thực, Google Security sẽ chặn lại và báo lỗi **401 Unauthorized**.
            >
            > ---
            > 💡 **CÁCH KHẮC PHỤC (Chọn 1 trong 2 cách):**
            >
            > - **Cách 1 (Đơn giản & Nhanh nhất - Khuyên dùng)**:  
            >   1. Mở trang Google Sheet của bạn.  
            >   2. Bấm nút **Chia sẻ (Share)** ở góc trên bên phải.  
            >   3. Tại mục *Quyền truy cập chung (General Access)*, chuyển từ **Hạn chế** sang **"Bất kỳ ai có liên kết đều có thể xem" (Anyone with the link can view)**.  
            >   4. Bấm **Xong** và quay lại đây bấm nút **🔄 Tải Lại Dữ Liệu Gốc**.
            >
            > - **Cách 2 (Sử dụng Service Account Secrets)**:  
            >   Copy cấu hình TOML của Service Account dán vào phần **App Secrets** trên Streamlit Cloud. Ứng dụng đã được tích hợp tự động gửi OAuth Bearer Token để mở khóa trang tính riêng tư của bạn!
            """)
            return pd.DataFrame()
        
        resp.raise_for_status()
        
        # Đọc dữ liệu CSV vào Pandas DataFrame
        df = pd.read_csv(io.StringIO(resp.text), dtype={'sdt': str})
        if 'sdt' in df.columns:
            df['sdt'] = df['sdt'].astype(str)
        return df
        
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu từ Google Sheets: {e}")
        return pd.DataFrame()

def load_knowledge_base():
    """Đọc quy tắc chấm điểm từ file Knowledge (hỗ trợ nhiều đường dẫn linh hoạt)"""
    candidate_paths = [
        os.path.join("knowledge-base", "tieu_chi_cham_diem.txt"),
        os.path.join("plans", "260710-workspace-bridge", "workspace-hv-v2", "my-workspace", "knowledge-base", "tieu_chi_cham_diem.txt"),
        "tieu_chi_cham_diem.txt"
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return "Nội dung Knowledge chưa tồn tại."

def classify_lead_tier(score):
    """Xếp loại Tier dựa trên Điểm số"""
    if score >= 50:
        return "🌟 VIP"
    elif score >= 0:
        return "🟢 Tiềm năng"
    else:
        return "🔴 Khách rác/Spam"

def ai_scoring_agent(mo_ta):
    """
    AI Scoring Agent Engine:
    Phân tích câu mô tả nhu cầu dựa trên các quy tắc trong Knowledge Base
    (Cộng 50đ cho Biệt thự/Penthouse/Ngân sách lớn/VIP; Trừ 50đ cho Nhầm số/Spam/Phi thực tế)
    """
    if not isinstance(mo_ta, str) or not mo_ta.strip():
        return 0, "🟡 Trung bình", "Chưa có mô tả nhu cầu"

    text = mo_ta.lower()
    score = 0
    reasons_plus = []
    reasons_minus = []

    # 1. TIÊU CHÍ CỘNG ĐIỂM (+50 ĐIỂM NGUYÊN TẮC)
    # Ngân sách lớn & Tài chính mạnh
    if re.search(r'(20 tỷ|tài chính (cực )?mạnh|không thành vấn đề|ngân sách lớn)', text):
        score += 50
        reasons_plus.append("Ngân sách/Tài chính cực mạnh (≥20 tỷ)")

    # Loại hình cao cấp
    if re.search(r'(biệt thự|penthouse|duplex|shophouse|quỹ đất công nghiệp|sàn văn phòng|2000m2)', text):
        score += 50
        reasons_plus.append("BĐS cao cấp (Biệt thự/Penthouse/Đất CN/Văn phòng lớn)")

    # Vị trí đắc địa
    if re.search(r'(quận 1|ven sông|vinhomes ocean park|phú mỹ hưng|khu đông)', text):
        score += 50
        reasons_plus.append("Vị trí đắc địa/Trung tâm")

    # Đối tượng khách hàng
    if re.search(r'(chủ doanh nghiệp|nhà đầu tư|mua sỉ|số lượng lớn)', text):
        score += 50
        reasons_plus.append("Khách VIP (Chủ DN/NĐT mua sỉ)")

    # Pháp lý & Minh bạch
    if re.search(r'(pháp lý chuẩn|sổ hồng riêng|gặp trực tiếp chủ đầu tư)', text):
        score += 25
        reasons_plus.append("Yêu cầu pháp lý minh bạch/Muốn chốt ngay")

    # 2. TIÊU CHÍ TRỪ ĐIỂM (-50 ĐIỂM NGUYÊN TẮC)
    # Nhầm số / Không nhu cầu
    if re.search(r'(nhầm số|không có nhu cầu|dữ liệu cũ|nhầm ngành)', text):
        score -= 50
        reasons_minus.append("Khách nhầm số / Không có nhu cầu BĐS")

    # Phi thực tế
    if re.search(r'(phi thực tế|giá 1-2 tỷ|giá 1 tỷ|2 triệu|vài trăm triệu|giá thấp vô lý)', text):
        score -= 50
        reasons_minus.append("Yêu cầu phi thực tế so với thị trường")

    # Thiếu thiện chí / Không hợp tác
    if re.search(r'(hỏi giá cho vui|chưa có ý định|thái độ không hợp tác)', text):
        score -= 50
        reasons_minus.append("Khách không thiện chí/Hỏi giá cho vui")

    # Spam / Quảng cáo
    if re.search(r'(spam|bảo hiểm|vay vốn|mời chào|quảng cáo)', text):
        score -= 50
        reasons_minus.append("Spam/Mời chào dịch vụ khác")

    # Thuê bao / Không liên lạc được
    if re.search(r'(thuê bao|không bắt máy|không phản hồi zalo)', text):
        score -= 50
        reasons_minus.append("Số điện thoại thuê bao/Không tương tác")

    # 3. TRƯỜNG HỢP CÂN BẰNG TẬP DỮ LIỆU
    if not reasons_plus and not reasons_minus:
        if re.search(r'(căn hộ|2pn|3pn|nhà phố|3-10 tỷ|4-5 tỷ|8-10 tỷ|mặt bằng|spa|đất nền|long an|đồng nai|2-3 tỷ|vay ngân hàng)', text):
            score = 20
            reasons_plus.append("Nhu cầu thực tầm trung (Chung cư/Nhà phố/Đất nền/Mặt bằng)")
        else:
            score = 10
            reasons_plus.append("Nhu cầu cơ bản cần tư vấn thêm")

    # Chuẩn hóa lý do giải thích
    explanation_parts = []
    if reasons_plus:
        explanation_parts.append("➕ " + "; ".join(reasons_plus))
    if reasons_minus:
        explanation_parts.append("➖ " + "; ".join(reasons_minus))
    
    explanation = " | ".join(explanation_parts) if explanation_parts else "Đã phân tích nhu cầu"
    tier = classify_lead_tier(score)
    
    return score, tier, explanation

# ---------------------------------------------------------
# MAIN STREAMLIT APP RUNNER (PREMIUM ORANGE THEME)
# ---------------------------------------------------------
def main():
    st.set_page_config(
        page_title="Lead Scoring BĐS - Premium Orange Dashboard",
        page_icon="🍊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # ---------------------------------------------------------
    # CUSTOM CSS: PREMIUM DARK & ORANGE DOMINANT THEME
    # ---------------------------------------------------------
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background-color: #0d0f14;
            color: #f1f5f9;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #161922 0%, #0d0f14 100%);
            border-right: 1px solid rgba(249, 115, 22, 0.15);
        }

        .header-card {
            background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(30, 27, 24, 0.8) 50%, rgba(13, 15, 20, 0.95) 100%);
            border: 1px solid rgba(249, 115, 22, 0.35);
            border-radius: 20px;
            padding: 28px 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px -5px rgba(249, 115, 22, 0.25);
            backdrop-filter: blur(12px);
            position: relative;
            overflow: hidden;
        }
        .header-card::before {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 6px; height: 100%;
            background: linear-gradient(180deg, #ff6b00 0%, #f97316 50%, #fb923c 100%);
        }
        
        .header-title {
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(90deg, #ff6b00 0%, #f97316 40%, #fb923c 80%, #fed7aa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }
        
        .header-subtitle {
            color: #cbd5e1;
            font-size: 14px;
            font-weight: 400;
            line-height: 1.5;
        }

        .orange-metric-card {
            background: rgba(22, 25, 34, 0.7);
            border: 1px solid rgba(249, 115, 22, 0.2);
            border-radius: 16px;
            padding: 20px 16px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        .orange-metric-card:hover {
            transform: translateY(-4px);
            border-color: rgba(249, 115, 22, 0.6);
            box-shadow: 0 8px 25px rgba(249, 115, 22, 0.3);
        }
        .orange-metric-val {
            font-size: 30px;
            font-weight: 800;
            color: #ff8c00;
            margin-bottom: 2px;
        }
        .orange-metric-lbl {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #94a3b8;
        }
        .orange-metric-badge {
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 12px;
            margin-top: 6px;
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #ff6b00 0%, #ea580c 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            padding: 12px 24px !important;
            box-shadow: 0 4px 20px rgba(234, 88, 12, 0.4) !important;
            transition: all 0.25s ease !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #ff8c00 0%, #f97316 100%) !important;
            box-shadow: 0 6px 25px rgba(249, 115, 22, 0.6) !important;
            transform: translateY(-2px) !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: rgba(22, 25, 34, 0.5);
            padding: 8px;
            border-radius: 14px;
            border: 1px solid rgba(249, 115, 22, 0.15);
        }
        .stTabs [data-baseweb="tab"] {
            height: 44px;
            border-radius: 10px;
            color: #94a3b8;
            font-weight: 600;
            padding: 0 20px;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #ea580c 0%, #f97316 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(234, 88, 12, 0.35);
        }

        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #0d0f14; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #f97316; }
    </style>
    """, unsafe_allow_html=True)

    # INITIALIZE SESSION STATE
    if "df_leads" not in st.session_state:
        raw_df = load_raw_data_from_sheets()
        if not raw_df.empty:
            if "Diem_So" not in raw_df.columns:
                raw_df["Diem_So"] = 0
            if "Phan_Loai" not in raw_df.columns:
                raw_df["Phan_Loai"] = "Chưa chấm"
            if "Ly_Do_Cham_Diem" not in raw_df.columns:
                raw_df["Ly_Do_Cham_Diem"] = "Chưa chạy AI Agent"
            if "Trang_Thai_Duyet" not in raw_df.columns:
                raw_df["Trang_Thai_Duyet"] = "Chưa duyệt"
            if "Ghi_Chu_Sale" not in raw_df.columns:
                raw_df["Ghi_Chu_Sale"] = ""
            raw_df["sdt"] = raw_df["sdt"].astype(str)
            st.session_state.df_leads = raw_df
        else:
            st.session_state.df_leads = pd.DataFrame(columns=[
                "id", "ten_khach", "sdt", "nhu_cau_mo_ta", 
                "Diem_So", "Phan_Loai", "Ly_Do_Cham_Diem", "Trang_Thai_Duyet", "Ghi_Chu_Sale"
            ])

    # SIDEBAR CONTROL
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <img src="https://img.icons8.com/gradient/96/real-estate.png" width="72"/>
            <h2 style="margin-top: 10px; color: #ff8c00; font-size: 20px; font-weight: 800;">LEAD SCORING AI</h2>
            <p style="color: #94a3b8; font-size: 12px;">Real Estate Agentic System</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: rgba(249, 115, 22, 0.2);'>", unsafe_allow_html=True)
        st.subheader("📡 Nguồn Dữ Liệu Live")
        sheet_url_input = st.text_input(
            "Google Sheets CSV URL:",
            value=DEFAULT_SHEET_URL,
            help="Đường dẫn CSV Export từ Google Sheets"
        )
        
        if st.button("🔄 Tải Lại Dữ Liệu Gốc", use_container_width=True):
            fresh_df = load_raw_data_from_sheets(sheet_url_input)
            if not fresh_df.empty:
                fresh_df["Diem_So"] = 0
                fresh_df["Phan_Loai"] = "Chưa chấm"
                fresh_df["Ly_Do_Cham_Diem"] = "Chưa chạy AI Agent"
                fresh_df["Trang_Thai_Duyet"] = "Chưa duyệt"
                fresh_df["Ghi_Chu_Sale"] = ""
                fresh_df["sdt"] = fresh_df["sdt"].astype(str)
                st.session_state.df_leads = fresh_df
                st.success("Đã tải lại dữ liệu mới thành công!")
                st.rerun()

        st.markdown("<hr style='border-color: rgba(249, 115, 22, 0.2);'>", unsafe_allow_html=True)
        st.subheader("📚 Knowledge Base")
        kb_text = load_knowledge_base()
        
        with st.expander("📖 Quy Tắc Chấm Điểm (+50/-50)", expanded=False):
            st.text_area("Cấu trúc tieu_chi_cham_diem.txt:", value=kb_text, height=260, disabled=True)
        
        st.markdown("<hr style='border-color: rgba(249, 115, 22, 0.2);'>", unsafe_allow_html=True)
        st.caption("🍊 Orange Theme UI | Antigravity AI Workspace v2.5")

    # MAIN HEADER CARD
    st.markdown("""
    <div class="header-card">
        <div class="header-title">🍊 Real Estate AI Lead Scoring & Dashboard</div>
        <div class="header-subtitle">Hệ thống phân tích nhu cầu tự động, áp dụng tri thức chấm điểm BĐS và tự động phê duyệt Lead VIP (Điểm ≥ 100).</div>
    </div>
    """, unsafe_allow_html=True)

    # Calculate Summary Statistics
    df_leads = st.session_state.df_leads.copy()
    total_leads = len(df_leads)
    vip_leads = len(df_leads[df_leads["Phan_Loai"] == "🌟 VIP"])
    tiemnang_leads = len(df_leads[df_leads["Phan_Loai"] == "🟢 Tiềm năng"])
    rac_leads = len(df_leads[df_leads["Phan_Loai"] == "🔴 Khách rác/Spam"])
    auto_approved_leads = len(df_leads[df_leads["Diem_So"] >= 100])
    approved_leads = len(df_leads[df_leads["Trang_Thai_Duyet"] == "Đã duyệt"])
    avg_score = round(df_leads["Diem_So"].mean(), 1) if total_leads > 0 else 0

    # PREMIUM ORANGE STATS DASHBOARD CARDS
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        st.markdown(f"""
        <div class="orange-metric-card">
            <div class="orange-metric-val" style="color: #f8fafc;">{total_leads}</div>
            <div class="orange-metric-lbl">TỔNG SỐ LEAD</div>
            <div class="orange-metric-badge" style="background: rgba(255,255,255,0.1); color: #cbd5e1;">Google Sheets</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="orange-metric-card" style="border-color: rgba(249, 115, 22, 0.6); background: rgba(249, 115, 22, 0.12);">
            <div class="orange-metric-val" style="color: #ff8c00;">{vip_leads}</div>
            <div class="orange-metric-lbl" style="color: #ffaa00;">KHÁCH VIP (≥50pt)</div>
            <div class="orange-metric-badge" style="background: rgba(249, 115, 22, 0.25); color: #ffedd5;">{round(vip_leads/total_leads*100, 1) if total_leads>0 else 0}%</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="orange-metric-card">
            <div class="orange-metric-val" style="color: #10b981;">{tiemnang_leads}</div>
            <div class="orange-metric-lbl">TIỀM NĂNG (0-49pt)</div>
            <div class="orange-metric-badge" style="background: rgba(16, 185, 129, 0.2); color: #6ee7b7;">{round(tiemnang_leads/total_leads*100, 1) if total_leads>0 else 0}%</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="orange-metric-card">
            <div class="orange-metric-val" style="color: #f43f5e;">{rac_leads}</div>
            <div class="orange-metric-lbl">KHÁCH RÁC / SPAM</div>
            <div class="orange-metric-badge" style="background: rgba(244, 63, 94, 0.2); color: #fca5a5;">{round(rac_leads/total_leads*100, 1) if total_leads>0 else 0}%</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="orange-metric-card">
            <div class="orange-metric-val" style="color: #fb923c;">{auto_approved_leads}</div>
            <div class="orange-metric-lbl">TỰ ĐỘNG DUYỆT (≥100)</div>
            <div class="orange-metric-badge" style="background: rgba(251, 146, 60, 0.2); color: #ffedd5;">Auto Approved</div>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
        <div class="orange-metric-card">
            <div class="orange-metric-val" style="color: #38bdf8;">{approved_leads}</div>
            <div class="orange-metric-lbl">ĐÃ PHÊ DUYỆT</div>
            <div class="orange-metric-badge" style="background: rgba(56, 189, 248, 0.2); color: #bae6fd;">Sales Approved</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # MAIN TABS SYSTEM
    # ---------------------------------------------------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard Thống Kê Trực Quan",
        "📋 Bảng Quản Lý Lead (Data Editor)",
        "📚 Knowledge Base Rules",
        "📥 Export & Báo Cáo"
    ])

    # TAB 1: VISUAL ANALYTICS DASHBOARD (PLOTLY CHARTS)
    with tab1:
        st.markdown("### 📈 Phân Tích Dữ Liệu Lead Bất Động Sản")
        
        col_tb1, col_tb2, col_tb3 = st.columns([2, 1, 1])
        with col_tb1:
            if st.button("🤖 Chạy AI Scoring (Scan & Auto Score Tất Cả Lead)", type="primary", use_container_width=True):
                with st.spinner("AI Agent đang phân tích nội dung nhu cầu & áp dụng tri thức chấm điểm..."):
                    scores = []
                    tiers = []
                    reasons = []
                    statuses = []
                    auto_approved_cnt = 0
                    
                    for idx, row in st.session_state.df_leads.iterrows():
                        mo_ta = str(row.get("nhu_cau_mo_ta", ""))
                        sc, tr, rs = ai_scoring_agent(mo_ta)
                        scores.append(sc)
                        tiers.append(tr)
                        reasons.append(rs)
                        
                        # Tự động chuyển trạng thái các khách hàng có điểm AI >= 100 sang "Đã duyệt"
                        if sc >= 100:
                            statuses.append("Đã duyệt")
                            auto_approved_cnt += 1
                        else:
                            current_status = row.get("Trang_Thai_Duyet", "Chưa duyệt")
                            statuses.append(current_status if current_status != "Chưa chấm" else "Chưa duyệt")
                        
                    st.session_state.df_leads["Diem_So"] = scores
                    st.session_state.df_leads["Phan_Loai"] = tiers
                    st.session_state.df_leads["Ly_Do_Cham_Diem"] = reasons
                    st.session_state.df_leads["Trang_Thai_Duyet"] = statuses
                    st.success(f"⚡ Đã hoàn thành chấm điểm AI cho {len(st.session_state.df_leads)} leads! (Đã tự động duyệt {auto_approved_cnt} lead điểm ≥ 100)")
                    st.rerun()

        with col_tb2:
            st.metric("Tỷ Lệ Chuyển Đổi VIP", f"{round(vip_leads/total_leads*100, 1) if total_leads>0 else 0}%", delta="Lead Chất Lượng Cao")
        with col_tb3:
            st.metric("Điểm AI Trung Bình", f"{avg_score} pts", delta="Thang điểm BĐS")

        st.markdown("<br>", unsafe_allow_html=True)

        if total_leads > 0:
            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                st.markdown("#### 🍩 Tỷ Lệ Phân Bổ Tier Khách Hàng")
                tier_counts = df_leads["Phan_Loai"].value_counts().reset_index()
                tier_counts.columns = ["Tier", "Số_Lượng"]
                
                color_map = {
                    "🌟 VIP": "#ff7700",
                    "🟢 Tiềm năng": "#10b981",
                    "🟡 Trung bình": "#3b82f6",
                    "🔴 Khách rác/Spam": "#f43f5e",
                    "Chưa chấm": "#64748b"
                }
                
                fig_donut = px.pie(
                    tier_counts, 
                    values="Số_Lượng", 
                    names="Tier", 
                    hole=0.55,
                    color="Tier",
                    color_discrete_map=color_map
                )
                fig_donut.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#0d0f14', width=3)))
                fig_donut.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e2e8f0'),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_donut, use_container_width=True)

            with chart_col2:
                st.markdown("#### 📊 Trạng Thái Duyệt Của Đội Nguồn Sales")
                status_counts = df_leads["Trang_Thai_Duyet"].value_counts().reset_index()
                status_counts.columns = ["Trạng_Thái", "Số_Lượng"]
                
                fig_bar = px.bar(
                    status_counts, 
                    x="Trạng_Thái", 
                    y="Số_Lượng", 
                    color="Trạng_Thái",
                    text="Số_Lượng",
                    color_discrete_sequence=["#ff7700", "#38bdf8", "#fb923c", "#f43f5e"]
                )
                fig_bar.update_traces(textposition='outside', marker=dict(line=dict(color='#0d0f14', width=1.5)))
                fig_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e2e8f0'),
                    xaxis_title="Trạng Thái",
                    yaxis_title="Số Lượng Lead",
                    showlegend=False,
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("#### 📉 Phân Bố Điểm AI Chấm Điểm (Histogram Distribution)")
            fig_hist = px.histogram(
                df_leads, 
                x="Diem_So", 
                nbins=20,
                color_discrete_sequence=["#ff6b00"],
                labels={"Diem_So": "Điểm AI (Score)"}
            )
            fig_hist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(22, 25, 34, 0.5)',
                font=dict(color='#e2e8f0'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_hist, use_container_width=True)

    # TAB 2: DATA EDITOR & HUMAN-IN-THE-LOOP MANAGEMENT
    with tab2:
        st.markdown("### 📋 Bảng Hiệu Chỉnh & Phê Duyệt Lead")
        st.caption("💡 Chỉnh sửa điểm số, phân loại, trạng thái duyệt và ghi chú trực tiếp trên bảng. Hệ thống tự động đồng bộ.")

        col_f1, col_f2, col_f3 = st.columns([1, 1, 2])
        with col_f1:
            tier_filter = st.selectbox("Lọc Tier:", ["Tất cả", "🌟 VIP", "🟢 Tiềm năng", "🔴 Khách rác/Spam", "Chưa chấm"], key="f_tier")
        with col_f2:
            status_filter = st.selectbox("Lọc Trạng Thái:", ["Tất cả", "Chưa duyệt", "Đã duyệt", "Cần liên hệ lại", "Bỏ qua"], key="f_status")
        with col_f3:
            search_query = st.text_input("🔍 Tìm tên khách/SĐT/Mô tả:", placeholder="Nhập từ khóa...", key="f_search")

        filtered_df = df_leads.copy()
        if tier_filter != "Tất cả":
            filtered_df = filtered_df[filtered_df["Phan_Loai"] == tier_filter]
        if status_filter != "Tất cả":
            filtered_df = filtered_df[filtered_df["Trang_Thai_Duyet"] == status_filter]
        if search_query.strip():
            q = search_query.lower()
            filtered_df = filtered_df[
                filtered_df["ten_khach"].str.lower().str.contains(q, na=False) |
                filtered_df["sdt"].str.lower().str.contains(q, na=False) |
                filtered_df["nhu_cau_mo_ta"].str.lower().str.contains(q, na=False)
            ]

        edited_df = st.data_editor(
            filtered_df,
            key="data_editor_leads_main",
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "id": st.column_config.NumberColumn("ID", disabled=True, width="small"),
                "ten_khach": st.column_config.TextColumn("Tên Khách", width="medium"),
                "sdt": st.column_config.TextColumn("SĐT", width="medium"),
                "nhu_cau_mo_ta": st.column_config.TextColumn("Nhu Cầu Mô Tả", width="large"),
                "Diem_So": st.column_config.NumberColumn("Điểm AI", help="Điểm số đánh giá", width="small"),
                "Phan_Loai": st.column_config.SelectboxColumn(
                    "Phân Loại (Tier)",
                    options=["🌟 VIP", "🟢 Tiềm năng", "🟡 Trung bình", "🔴 Khách rác/Spam", "Chưa chấm"],
                    width="medium"
                ),
                "Ly_Do_Cham_Diem": st.column_config.TextColumn("Lý Do Chấm Điểm (AI)", width="large"),
                "Trang_Thai_Duyet": st.column_config.SelectboxColumn(
                    "Trạng Thái Duyệt",
                    options=["Chưa duyệt", "Đã duyệt", "Cần liên hệ lại", "Bỏ qua"],
                    width="medium"
                ),
                "Ghi_Chu_Sale": st.column_config.TextColumn("Ghi Chú của Sales", width="medium")
            },
            hide_index=True
        )

        if not edited_df.equals(filtered_df):
            for idx in edited_df.index:
                st.session_state.df_leads.loc[idx] = edited_df.loc[idx]

    # TAB 3: KNOWLEDGE BASE RULES VIEWER
    with tab3:
        st.markdown("### 📚 Tri Thức & Quy Tắc Chấm Điểm Lead BĐS")
        st.info("💡 File `knowledge-base/tieu_chi_cham_diem.txt` chứa tập luật nguyên tắc để AI Agent thực hiện phân tích nhu cầu.")
        
        st.markdown(f"""
        ```text
        {kb_text}
        ```
        """)

    # TAB 4: EXPORT & REPORTS
    with tab4:
        st.markdown("### 📥 Xuất Dữ Liệu & Báo Cáo Phê Duyệt")
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            st.markdown("#### 📄 Tải Dữ Liệu CSV")
            csv_data = st.session_state.df_leads.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                label="📥 Download CSV Dataset (Bao Gồm Điểm AI & Duyệt)",
                data=csv_data,
                file_name="lead_scoring_results.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary"
            )

        with col_exp2:
            st.markdown("#### 📊 Tải Báo Cáo Excel (XLSX)")
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                st.session_state.df_leads.to_excel(writer, index=False, sheet_name='Lead_Scoring')
            excel_data = buffer.getvalue()
            
            st.download_button(
                label="📊 Export Full Excel Report (.xlsx)",
                data=excel_data,
                file_name="lead_scoring_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
