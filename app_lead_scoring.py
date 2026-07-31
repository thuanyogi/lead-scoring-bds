import streamlit as st
import pandas as pd
import re
import os
import io

# ---------------------------------------------------------
# CONSTANTS & PATHS
# ---------------------------------------------------------
DEFAULT_SHEET_URL = "https://docs.google.com/spreadsheets/d/1WUvvkEBjt23qyzcnTK0OmAqGip5KPSX0UCdYGl57gRc/export?format=csv&gid=1542775777"
KNOWLEDGE_FILE_PATH = os.path.join("knowledge-base", "tieu_chi_cham_diem.txt")

# ---------------------------------------------------------
# HELPER & SCORING FUNCTIONS
# ---------------------------------------------------------
def load_raw_data_from_sheets(sheet_url=DEFAULT_SHEET_URL):
    """Tải dữ liệu trực tiếp từ Google Sheets CSV Export URL"""
    try:
        df = pd.read_csv(sheet_url, dtype={'sdt': str})
        if 'sdt' in df.columns:
            df['sdt'] = df['sdt'].astype(str)
        return df
    except Exception as e:
        st.error(f"Lỗi kết nối Google Sheets: {e}")
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
# MAIN STREAMLIT APP RUNNER
# ---------------------------------------------------------
def main():
    st.set_page_config(
        page_title="Hệ Thống Lead Scoring Bất Động Sản",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom Styling
    st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: #e0e6ed;
        }
        .header-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        .header-title {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .header-subtitle {
            color: #94a3b8;
            font-size: 14px;
        }
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
        st.image("https://img.icons8.com/color/96/real-estate.png", width=64)
        st.title("⚙️ Lead Scoring AI Control")
        
        st.markdown("---")
        st.subheader("📡 Nguồn Dữ Liệu")
        sheet_url_input = st.text_input(
            "Google Sheets CSV URL:",
            value=DEFAULT_SHEET_URL,
            help="Đường dẫn CSV Export của trang tính Google Sheets"
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

        st.markdown("---")
        st.subheader("📚 Knowledge Base (Tiêu chí)")
        kb_text = load_knowledge_base()
        
        with st.expander("📖 Xem Quy Tắc Chấm Điểm", expanded=False):
            st.text_area("File tieu_chi_cham_diem.txt:", value=kb_text, height=280, disabled=True)
        
        st.markdown("---")
        st.caption("🤖 Antigravity AI Workspace v2.0 | Lead Scoring Agent")

    # MAIN INTERFACE
    st.markdown("""
    <div class="header-card">
        <div class="header-title">🏠 Hệ Thống Quản Lý & AI Lead Scoring Bất Động Sản</div>
        <div class="header-subtitle">Tự động quét nhu cầu khách hàng từ Google Sheets, áp dụng quy tắc Knowledge Base (+50/-50 điểm) và hỗ trợ phê duyệt trực tiếp.</div>
    </div>
    """, unsafe_allow_html=True)

    # Top Actions Toolbar
    col_act1, col_act2, col_act3 = st.columns([2, 1, 1])

    with col_act1:
        if st.button("🤖 Chạy AI Scoring (Scan & Auto Score Tất Cả Lead)", type="primary", use_container_width=True):
            with st.spinner("AI Agent đang phân tích nội dung nhu cầu & áp dụng tri thức chấm điểm..."):
                scores = []
                tiers = []
                reasons = []
                
                for idx, row in st.session_state.df_leads.iterrows():
                    mo_ta = str(row.get("nhu_cau_mo_ta", ""))
                    sc, tr, rs = ai_scoring_agent(mo_ta)
                    scores.append(sc)
                    tiers.append(tr)
                    reasons.append(rs)
                    
                st.session_state.df_leads["Diem_So"] = scores
                st.session_state.df_leads["Phan_Loai"] = tiers
                st.session_state.df_leads["Ly_Do_Cham_Diem"] = reasons
                st.success(f"⚡ Đã hoàn thành chấm điểm AI cho {len(st.session_state.df_leads)} leads!")
                st.rerun()

    with col_act2:
        tier_filter = st.selectbox(
            "Lọc Phân Loại:",
            ["Tất cả", "🌟 VIP", "🟢 Tiềm năng", "🔴 Khách rác/Spam", "Chưa chấm"]
        )

    with col_act3:
        status_filter = st.selectbox(
            "Trạng Thái Duyệt:",
            ["Tất cả", "Chưa duyệt", "Đã duyệt", "Cần liên hệ lại", "Bỏ qua"]
        )

    # Metrics Summary
    df_current = st.session_state.df_leads.copy()
    total_leads = len(df_current)
    vip_count = len(df_current[df_current["Phan_Loai"] == "🌟 VIP"])
    approved_count = len(df_current[df_current["Trang_Thai_Duyet"] == "Đã duyệt"])
    avg_score = round(df_current["Diem_So"].mean(), 1) if total_leads > 0 else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tổng Số Lead", f"{total_leads}")
    m2.metric("🌟 Khách VIP (+50pt)", f"{vip_count}", delta=f"{round(vip_count/total_leads*100, 1) if total_leads>0 else 0}%")
    m3.metric("✅ Đã Duyệt", f"{approved_count}")
    m4.metric("📊 Điểm Trung Bình", f"{avg_score} pts")

    st.markdown("---")

    # Filtering logic
    filtered_df = df_current.copy()
    if tier_filter != "Tất cả":
        filtered_df = filtered_df[filtered_df["Phan_Loai"] == tier_filter]
    if status_filter != "Tất cả":
        filtered_df = filtered_df[filtered_df["Trang_Thai_Duyet"] == status_filter]

    st.subheader("📋 Bảng Quản Lý Lead (Human-in-the-Loop Data Editor)")
    st.caption("💡 Bạn có thể chỉnh sửa trực tiếp điểm số, xếp loại, trạng thái duyệt và ghi chú trên bảng bên dưới.")

    # Data Editor
    edited_df = st.data_editor(
        filtered_df,
        key="data_editor_leads",
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

    # Synchronize edited changes back to session_state
    if not edited_df.equals(filtered_df):
        for idx in edited_df.index:
            st.session_state.df_leads.loc[idx] = edited_df.loc[idx]

    st.markdown("---")

    # Export & Download Tools
    col_exp1, col_exp2 = st.columns([1, 1])

    with col_exp1:
        csv_data = st.session_state.df_leads.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 Tải Bảng Lead Đã Duyệt (CSV)",
            data=csv_data,
            file_name="lead_scoring_results.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_exp2:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.df_leads.to_excel(writer, index=False, sheet_name='Lead_Scoring')
        excel_data = buffer.getvalue()
        
        st.download_button(
            label="📊 Xuất Báo Cáo Excel (XLSX)",
            data=excel_data,
            file_name="lead_scoring_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

if __name__ == "__main__":
    main()
