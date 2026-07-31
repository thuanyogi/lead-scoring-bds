import os
import pandas as pd

def process_erp_data(file_path, output_dir_drafts, output_dir_reports):
    # Ensure directories exist
    os.makedirs(output_dir_drafts, exist_ok=True)
    os.makedirs(output_dir_reports, exist_ok=True)
    
    # 1. Read data
    df = pd.read_excel(file_path)
    initial_rows = len(df)
    
    # 2. Clean data
    # Strip whitespace from string columns
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()
        
    # Drop exact duplicates
    df = df.drop_duplicates()
    rows_after_dedup = len(df)
    duplicates_removed = initial_rows - rows_after_dedup
    
    # Validate numeric columns (convert to positive if negative, or handle)
    df['Base_Salary'] = df['Base_Salary'].apply(lambda x: abs(x))
    df['Bonus'] = df['Bonus'].apply(lambda x: abs(x))
    df['Penalty'] = df['Penalty'].apply(lambda x: abs(x))
    
    # Calculate Net Salary (Thực lĩnh)
    df['Net_Salary'] = df['Base_Salary'] + df['Bonus'] - df['Penalty']
    
    # 3. Export separate file for each Manager
    managers = df['Manager'].unique()
    exported_files = []
    
    for manager in managers:
        manager_df = df[df['Manager'] == manager].copy()
        # Sort by Net_Salary descending
        manager_df = manager_df.sort_values(by='Net_Salary', ascending=False)
        
        # Output file name
        sanitized_manager_name = str(manager).replace(" ", "_")
        filename = f"ERP_OP_Report_{sanitized_manager_name}.xlsx"
        full_path = os.path.join(output_dir_drafts, filename)
        
        # Save to Excel
        manager_df.to_excel(full_path, index=False)
        exported_files.append((manager, filename, len(manager_df)))
        
    # 4. Generate Summaries & Insights
    total_base = int(df['Base_Salary'].sum())
    total_bonus = int(df['Bonus'].sum())
    total_penalty = int(df['Penalty'].sum())
    total_net = int(df['Net_Salary'].sum())
    total_employees = len(df)
    
    # Department summary
    dept_summary = df.groupby('Department').agg(
        Total_Employees=('Employee_ID', 'count'),
        Total_Net_Salary=('Net_Salary', 'sum'),
        Avg_Net_Salary=('Net_Salary', 'mean')
    ).reset_index()
    dept_summary['Avg_Net_Salary'] = dept_summary['Avg_Net_Salary'].round(0).astype(int)
    dept_summary = dept_summary.sort_values(by='Total_Net_Salary', ascending=False)
    
    # Manager summary
    manager_summary = df.groupby('Manager').agg(
        Total_Employees=('Employee_ID', 'count'),
        Total_Net_Salary=('Net_Salary', 'sum'),
        Avg_Net_Salary=('Net_Salary', 'mean')
    ).reset_index()
    manager_summary['Avg_Net_Salary'] = manager_summary['Avg_Net_Salary'].round(0).astype(int)
    manager_summary = manager_summary.sort_values(by='Total_Net_Salary', ascending=False)
    
    # Top 5 employees by Net_Salary
    top_5 = df.sort_values(by='Net_Salary', ascending=False).head(5)[
        ['Employee_ID', 'Employee_Name', 'Department', 'Manager', 'Net_Salary']
    ]
    
    # Bottom 5 employees by Net_Salary
    bottom_5 = df.sort_values(by='Net_Salary', ascending=True).head(5)[
        ['Employee_ID', 'Employee_Name', 'Department', 'Manager', 'Net_Salary']
    ]
    
    # Write Markdown Report
    report_filename = "ERP_OP_Summary_Report.md"
    report_path = os.path.join(output_dir_reports, report_filename)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# BÁO CÁO PHÂN TÍCH TIẾN ĐỘ & CHI PHÍ NHÂN SỰ ERP\n\n")
        f.write(f"- **Tháng báo cáo**: {df['Month'].iloc[0] if len(df) > 0 else 'N/A'}\n")
        f.write("- **Người thực hiện**: AI Operations Analyst\n")
        f.write("- **Dữ liệu nguồn**: `THỰC HÀNH_ERP_OP_BigData_200rows.xlsx`\n\n")
        
        f.write("## 1. Tóm tắt Tổng quan (Executive Summary)\n\n")
        f.write(f"- **Tổng số nhân sự**: {total_employees} nhân viên\n")
        f.write(f"- **Tổng lương cơ bản**: {total_base:,.0f} VND\n")
        f.write(f"- **Tổng thưởng (Bonus)**: {total_bonus:,.0f} VND\n")
        f.write(f"- **Tổng phạt (Penalty)**: {total_penalty:,.0f} VND\n")
        f.write(f"- **Tổng thực lĩnh (Net Salary)**: {total_net:,.0f} VND\n")
        f.write(f"- **Số bản ghi trùng lặp đã loại bỏ**: {duplicates_removed}\n\n")
        
        f.write("## 2. Phân tích Theo Bộ phận (Department Analysis)\n\n")
        f.write("| Bộ phận | Số nhân viên | Tổng thực lĩnh (VND) | Trung bình thực lĩnh (VND) |\n")
        f.write("|---|---|---|---|\n")
        for _, row in dept_summary.iterrows():
            f.write(f"| {row['Department']} | {row['Total_Employees']} | {row['Total_Net_Salary']:,.0f} | {row['Avg_Net_Salary']:,.0f} |\n")
        f.write("\n")
        
        f.write("## 3. Phân tích Quản lý (Manager Analysis)\n\n")
        f.write("| Quản lý | Số nhân viên quản lý | Tổng thực lĩnh (VND) | Trung bình thực lĩnh (VND) |\n")
        f.write("|---|---|---|---|\n")
        for _, row in manager_summary.iterrows():
            f.write(f"| {row['Manager']} | {row['Total_Employees']} | {row['Total_Net_Salary']:,.0f} | {row['Avg_Net_Salary']:,.0f} |\n")
        f.write("\n")
        
        f.write("## 4. Top 5 Nhân viên Lương cao nhất\n\n")
        f.write("| Mã NV | Tên Nhân viên | Bộ phận | Quản lý | Thực lĩnh (VND) |\n")
        f.write("|---|---|---|---|---|\n")
        for _, row in top_5.iterrows():
            f.write(f"| {row['Employee_ID']} | {row['Employee_Name']} | {row['Department']} | {row['Manager']} | {row['Net_Salary']:,.0f} |\n")
        f.write("\n")
        
        f.write("## 5. Bottom 5 Nhân viên Lương thấp nhất\n\n")
        f.write("| Mã NV | Tên Nhân viên | Bộ phận | Quản lý | Thực lĩnh (VND) |\n")
        f.write("|---|---|---|---|---|\n")
        for _, row in bottom_5.iterrows():
            f.write(f"| {row['Employee_ID']} | {row['Employee_Name']} | {row['Department']} | {row['Manager']} | {row['Net_Salary']:,.0f} |\n")
        f.write("\n")
        
        f.write("## 6. Danh sách File Manager đã xuất (outputs/drafts/)\n\n")
        f.write("| Quản lý | Tên File Excel | Số nhân viên |\n")
        f.write("|---|---|---|\n")
        for manager, fname, count in exported_files:
            f.write(f"| {manager} | [{fname}](file://{os.path.join(output_dir_drafts, fname)}) | {count} |\n")
            
    print("Processing complete!")
    print(f"Report written to: {report_path}")
    print(f"Manager files written to: {output_dir_drafts}")

if __name__ == "__main__":
    import sys
    file_path = "/Users/thuanyogi/Downloads/_Project/AA/plans/260710-workspace-bridge/workspace-hv-v2/my-workspace/sample-data/THỰC HÀNH_ERP_OP_BigData_200rows.xlsx"
    output_dir_drafts = "/Users/thuanyogi/Downloads/_Project/AA/plans/260710-workspace-bridge/workspace-hv-v2/my-workspace/outputs/drafts"
    output_dir_reports = "/Users/thuanyogi/Downloads/_Project/AA/plans/260710-workspace-bridge/workspace-hv-v2/my-workspace/outputs/reports"
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir_drafts = sys.argv[2]
    if len(sys.argv) > 3:
        output_dir_reports = sys.argv[3]
        
    process_erp_data(file_path, output_dir_drafts, output_dir_reports)
