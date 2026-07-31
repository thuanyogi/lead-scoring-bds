#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KỊCH BẢN TỰ ĐỘNG HÓA ĐỒNG BỘ DỮ LIỆU GOOGLE SHEETS
--------------------------------------------------
Tác giả: Chuyên gia Tự động hóa (Google Antigravity)
Mục tiêu:
1. Kết nối Google Sheets qua OAuth 2.0 (credentials.json chuẩn bảo mật từ Google Cloud).
2. Phát hiện dữ liệu mới chưa đồng bộ từ file 'Data Nhan Vien'.
3. Chèn nối tiếp (Append) dữ liệu mới vào cuối file 'Admin Expense Tracker' (Tuyệt đối không ghi đè).
4. Đánh dấu 'Done' tại cột 'SyncStatus' trên file 'Data Nhan Vien' sau khi ghi thành công (Anti-duplication).
"""

import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import gspread

# ---------------------------------------------------------------------------
# CONFIGURATION & CONSTANTS
# ---------------------------------------------------------------------------
CLIENT_SECRET_FILE = "/Users/thuanyogi/Downloads/client_secret_814827956614-27ngklg7a44kg64vfpimi7qe0j8l55c8.apps.googleusercontent.com.json"
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")

# Quần thể Scope cần thiết cho Google Sheets & Google Drive API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Thông tin 2 File Google Sheets
SOURCE_SPREADSHEET_KEY = "1ZO1aFoX3JFaIuVq7NZSKVZMHgKyfbbWa3Febl8GAmT0"
SOURCE_GID = "1177273027"  # Sheet 'Data Nhan Vien'

DEST_SPREADSHEET_KEY = "1dpof1sefTNbHBXdu4UABvCb_lt5pAJxKvyncVUjuy80"
DEST_GID = "472636171"     # Sheet 'Admin Expense Tracker'

# ---------------------------------------------------------------------------
# AUTHENTICATION FUNCTION (OAuth 2.0)
# ---------------------------------------------------------------------------
def authenticate_google_services():
    """
    Xác thực chuẩn Google OAuth 2.0 bằng file client credentials JSON.
    Tự động lưu và làm mới Access Token thông qua token.json.
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"⚠️ Cảnh báo: File token cũ không hợp lệ ({e}), tiến hành xác thực lại...", flush=True)

    # Nếu chưa có credentials hợp lệ hoặc hết hạn
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Đang làm mới Access Token bằng Refresh Token...", flush=True)
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET_FILE):
                raise FileNotFoundError(f"❌ KHÔNG TÌM THẤY file OAuth Credentials tại: {CLIENT_SECRET_FILE}")
            
            print("🔑 Khởi tạo luồng đăng nhập OAuth 2.0...", flush=True)
            print("👉 Vui lòng hoàn tất xác thực trên cửa sổ trình duyệt vừa mở...", flush=True)
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Lưu token đã xác thực để dùng lại lần sau
        with open(TOKEN_FILE, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())
            print(f"✅ Đã lưu token xác thực vào: {TOKEN_FILE}", flush=True)

    # Kết nối gspread với OAuth 2.0 Credentials
    gc = gspread.authorize(creds)
    return gc

# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------
def get_worksheet_by_gid(spreadsheet, gid_str):
    """
    Tìm worksheet theo GID. Nếu không tìm thấy sẽ mặc định lấy sheet đầu tiên.
    """
    for ws in spreadsheet.worksheets():
        if str(ws.id) == str(gid_str):
            return ws
    print(f"⚠️ Không tìm thấy Worksheet có GID {gid_str}, sử dụng Sheet đầu tiên: {spreadsheet.sheet1.title}")
    return spreadsheet.sheet1

# ---------------------------------------------------------------------------
# MAIN AUTOMATION WORKFLOW
# ---------------------------------------------------------------------------
def run_sync_process():
    print("==================================================================", flush=True)
    print("🚀 BẮT ĐẦU QUÁ TRÌNH TỰ ĐỘNG HÓA ĐỒNG BỘ DỮ LIỆU GOOGLE SHEETS", flush=True)
    print("==================================================================", flush=True)

    # 1. Xác thực OAuth 2.0
    print("\n[Bước 1] Kiểm tra và xác thực kết nối Google Cloud OAuth 2.0...", flush=True)
    gc = authenticate_google_services()
    print("✅ Kết nối OAuth 2.0 thành công!", flush=True)

    # 2. Mở File Dữ Liệu
    print("\n[Bước 2] Mở các file Google Sheets...", flush=True)
    try:
        sh_source = gc.open_by_key(SOURCE_SPREADSHEET_KEY)
        ws_source = get_worksheet_by_gid(sh_source, SOURCE_GID)
        print(f"  • File Nguồn (Data Nhan Vien): '{sh_source.title}' -> Tab: '{ws_source.title}'", flush=True)

        sh_dest = gc.open_by_key(DEST_SPREADSHEET_KEY)
        ws_dest = get_worksheet_by_gid(sh_dest, DEST_GID)
        print(f"  • File Đích (Admin Expense Tracker): '{sh_dest.title}' -> Tab: '{ws_dest.title}'", flush=True)
    except Exception as e:
        print(f"❌ Lỗi khi truy cập Google Sheets: {e}", flush=True)
        print("👉 Vui lòng kiểm tra lại quyền truy cập của tài khoản Google đã đăng nhập.", flush=True)
        sys.exit(1)

    # 3. Đọc dữ liệu từ File Nguồn (Data Nhan Vien)
    print("\n[Bước 3] Phân tích cấu trúc dữ liệu và cột trạng thái SyncStatus...", flush=True)
    all_source_values = ws_source.get_all_values()

    if not all_source_values or len(all_source_values) <= 1:
        print("ℹ️ File Nguồn chưa có dữ liệu giao dịch nào (chỉ có dòng tiêu đề hoặc trống).", flush=True)
        return

    headers = all_source_values[0]
    status_col_name = "SyncStatus"
    
    # Kiểm tra cột SyncStatus đã tồn tại chưa
    if status_col_name in headers:
        sync_status_col_idx = headers.index(status_col_name) + 1  # 1-indexed
        print(f"  • Tìm thấy cột '{status_col_name}' ở vị trí cột số {sync_status_col_idx}.", flush=True)
    else:
        # Nếu chưa có, tự động tạo mới cột SyncStatus ở cuối tiêu đề
        sync_status_col_idx = len(headers) + 1
        print(f"  ➕ Cột '{status_col_name}' chưa tồn tại. Tự động khởi tạo tại cột số {sync_status_col_idx}...", flush=True)
        ws_source.update_cell(1, sync_status_col_idx, status_col_name)
        headers.append(status_col_name)

    # Số cột dữ liệu gốc (không bao gồm cột SyncStatus nếu vừa chèn ở cuối)
    data_col_count = len(headers) - 1 if headers[-1] == status_col_name else len(headers)

    # 4. Lọc các dòng dữ liệu chưa đồng bộ (SyncStatus != 'Done')
    rows_to_sync = []
    synced_row_numbers = []

    for row_idx, row in enumerate(all_source_values[1:], start=2): # Start from row 2 in Sheets
        # Lấy giá trị trạng thái hiện tại
        status_val = ""
        if len(row) >= sync_status_col_idx:
            status_val = row[sync_status_col_idx - 1].strip()

        # Nếu dòng chưa được đánh dấu Done
        if status_val.lower() != "done":
            # Chỉ lấy các cột dữ liệu giao dịch (bỏ qua cột SyncStatus)
            row_data = row[:data_col_count]
            
            # Đảm bảo dòng không hoàn toàn trống
            if any(cell.strip() for cell in row_data):
                rows_to_sync.append(row_data)
                synced_row_numbers.append(row_idx)

    if not rows_to_sync:
        print("✅ Tất cả dòng dữ liệu đã được đồng bộ trước đó. Không có dòng mới cần xử lý.", flush=True)
        return

    print(f"  👉 Tìm thấy {len(rows_to_sync)} dòng dữ liệu MỚI chưa đồng bộ.", flush=True)

    # 5. Ghi nối tiếp (Append) dữ liệu mới vào Admin Expense Tracker
    print("\n[Bước 4] Ghi nối tiếp (Append) dữ liệu sang file Admin Expense Tracker...", flush=True)
    try:
        ws_dest.append_rows(rows_to_sync, value_input_option='USER_ENTERED')
        print(f"✅ Đã append thành công {len(rows_to_sync)} dòng mới vào dòng cuối của Admin Expense Tracker!", flush=True)
    except Exception as e:
        print(f"❌ Lỗi khi append dữ liệu sang file Admin: {e}", flush=True)
        sys.exit(1)

    # 6. Đánh dấu 'Done' cho các dòng vừa xử lý ở file Data Nhan Vien (Chống trùng lặp)
    print("\n[Bước 5] Cập nhật trạng thái 'Done' vào cột SyncStatus ở file Data Nhan Vien...", flush=True)
    try:
        cell_updates = []
        for r_num in synced_row_numbers:
            cell_updates.append(gspread.Cell(r_num, sync_status_col_idx, "Done"))
        
        ws_source.update_cells(cell_updates)
        print(f"✅ Đã đánh dấu 'Done' thành công cho {len(synced_row_numbers)} dòng trong file Data Nhan Vien!", flush=True)
    except Exception as e:
        print(f"⚠️ Cảnh báo khi cập nhật SyncStatus: {e}", flush=True)

    print("\n==================================================================", flush=True)
    print("🎉 HOÀN THÀNH QUÁ TRÌNH ĐỒNG BỘ DỮ LIỆU THÀNH CÔNG!", flush=True)
    print("==================================================================", flush=True)


if __name__ == "__main__":
    run_sync_process()
