#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fullstack AI Engineer & Data Analyst - Công ty TNHH Alpha
Real-Time Sales Dashboard Server (Port 9090)
Polling frequency: Every 2 seconds
"""

import os
import sys
import json
import time
import socket
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pandas as pd

EXCEL_PATH = "/Users/thuanyogi/Downloads/DEMO_sales_data.xlsx"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "outputs/reports/dashboard_demo.html")
PORT = 9090

def get_dashboard_data():
    """Đọc file sales_data.xlsx và trích xuất chỉ số KPI, Biểu đồ & Bảng chi tiết."""
    if not os.path.exists(EXCEL_PATH):
        return {"error": f"Không tìm thấy file {EXCEL_PATH}"}

    try:
        # Đọc dữ liệu từ file Excel
        df = pd.read_excel(EXCEL_PATH)

        # Tính toán tổng quan KPI
        tot_revenue = float(df['Doanh_Thu_Thuan'].sum())
        tot_cost = float(df['Tong_Chi_Phi'].sum())
        net_profit = float(df['Loi_Nhuan'].sum())
        profit_margin = (net_profit / tot_revenue * 100.0) if tot_revenue > 0 else 0.0
        tot_quantity = int(df['So_Luong'].sum())

        # Thống kê theo Tháng (Monthly Trend)
        monthly_df = df.groupby('Thang').agg({
            'Doanh_Thu_Thuan': 'sum',
            'Tong_Chi_Phi': 'sum',
            'Loi_Nhuan': 'sum'
        }).reset_index().sort_values('Thang')

        monthly_list = []
        for _, row in monthly_df.iterrows():
            monthly_list.append({
                "month": str(row['Thang']),
                "revenue": float(row['Doanh_Thu_Thuan']),
                "cost": float(row['Tong_Chi_Phi']),
                "profit": float(row['Loi_Nhuan'])
            })

        # Thống kê theo Danh Mục Sản Phẩm (Category Breakdown)
        cat_df = df.groupby('Danh_Muc_San_Pham').agg({
            'Doanh_Thu_Thuan': 'sum',
            'Tong_Chi_Phi': 'sum',
            'Loi_Nhuan': 'sum',
            'So_Luong': 'sum'
        }).reset_index()

        cat_list = []
        for _, row in cat_df.iterrows():
            rev = float(row['Doanh_Thu_Thuan'])
            cat_list.append({
                "category": str(row['Danh_Muc_San_Pham']),
                "revenue": rev,
                "cost": float(row['Tong_Chi_Phi']),
                "profit": float(row['Loi_Nhuan']),
                "quantity": int(row['So_Luong']),
                "share_percent": (rev / tot_revenue * 100.0) if tot_revenue > 0 else 0.0
            })

        # 10 Đơn hàng mới nhất (Recent Orders)
        recent_df = df.sort_values(by='Ngay_Giao_Dich', ascending=False).head(10)
        recent_list = []
        for _, row in recent_df.iterrows():
            recent_list.append({
                "id": str(row['Ma_Don_Hang']),
                "date": str(row['Ngay_Giao_Dich'])[:10],
                "customer": str(row['Ten_Khach_Hang']),
                "category": str(row['Danh_Muc_San_Pham']),
                "revenue": float(row['Doanh_Thu_Thuan']),
                "profit": float(row['Loi_Nhuan'])
            })

        return {
            "timestamp": time.strftime("%H:%M:%S %d/%m/%Y"),
            "kpis": {
                "total_revenue": tot_revenue,
                "total_cost": tot_cost,
                "net_profit": net_profit,
                "profit_margin": profit_margin,
                "total_quantity": tot_quantity
            },
            "monthly": monthly_list,
            "categories": cat_list,
            "recent_orders": recent_list
        }
    except Exception as e:
        return {"error": str(e)}

class AlphaRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/data'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            data = get_dashboard_data()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        elif self.path in ['/', '/index.html']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            if os.path.exists(HTML_PATH):
                with open(HTML_PATH, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write("<h1>Không tìm thấy dashboard HTML!</h1>".encode('utf-8'))
        else:
            super().do_GET()

    def log_message(self, format, *args):
        # Tránh log rác polling mỗi 2s vào terminal
        if '/api/data' in args[0]:
            return
        super().log_message(format, *args)

def auto_open_browser():
    time.sleep(1.2)
    url = f"http://localhost:{PORT}"
    print(f"🚀 Tự động mở trình duyệt: {url}")
    webbrowser.open(url)

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, AlphaRequestHandler)
    print("=" * 65)
    print("🔥 CÔNG TY TNHH ALPHA - REALTIME SALES DASHBOARD SERVER")
    print(f"📍 Server đang chạy tại: http://localhost:{PORT}")
    print(f"📊 Nguồn dữ liệu: {EXCEL_PATH}")
    print(f"⏱️ Tần số Polling: Mỗi 2 giây")
    print("=" * 65)

    # Khởi động thread mở trình duyệt
    threading.Thread(target=auto_open_browser, daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server đã dừng.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
