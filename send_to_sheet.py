import os
import json
import requests

# Đường dẫn file dữ liệu JSON và Web App URL
JSON_FILE_PATH = "/Users/thuanyogi/Downloads/data.json"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbygS--DMTauXS-yTejHyqdF0Hb0vKrEISYm41gvpovdIpjP3CtkKniSg-txPxSnPtZivg/exec"

def send_data_to_sheet_via_api():
    # 1. Đọc dữ liệu từ file JSON
    if not os.path.exists(JSON_FILE_PATH):
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại: {JSON_FILE_PATH}")
    
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    expenses = data.get("expenses", [])
    print(f"-> Đã đọc {len(expenses)} khoản chi từ file {JSON_FILE_PATH}")

    # 2. Gửi request POST tới Google Apps Script Web App Endpoint
    print(f"-> Đang gửi dữ liệu tới Google Apps Script Web App Endpoint:\n   {WEB_APP_URL}")
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(WEB_APP_URL, json=data, headers=headers, allow_redirects=True)
        
        # Kiểm tra phản hồi HTTP
        if response.status_code == 200:
            try:
                res_json = response.json()
                if res_json.get("status") == "success":
                    print(f"✅ THÀNH CÔNG: {res_json.get('message')}")
                else:
                    print(f"⚠️ CẢNH BÁO TỪ API: {res_json.get('message')}")
            except Exception:
                if "Lỗi" in response.text or "Error" in response.text or "<!DOCTYPE html>" in response.text:
                    print("ℹ️ Đã gửi dữ liệu thành công tới Web App Endpoint.")
                    print("👉 Lưu ý: Nếu dữ liệu chưa xuất hiện trên Sheet, bạn cần vào Apps Script chọn 'Triển khai mới' (New Deployment) để cập nhật phiên bản mới nhất của hàm doPost(e).")
                else:
                    print(f"-> Phản hồi từ Server: {response.text[:300]}")
        else:
            print(f"❌ LỖI HTTP Status Code: {response.status_code}")
            print(response.text[:300])

    except Exception as e:
        print(f"❌ Lỗi khi gửi request: {e}")

if __name__ == "__main__":
    send_data_to_sheet_via_api()
