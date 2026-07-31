/**
 * Google Apps Script Web App Endpoint & Sheet Management
 * Web App URL: https://script.google.com/macros/s/AKfycbzDrQUDKMep9SWQQYtip74aHsXHmbOTLFG7VuuuSKSvTTS5z6iL_vqQWt5CQYYoqCZROQ/exec
 */

// 1. Xử lý HTTP POST request từ Python script hoặc API Client
function doPost(e) {
  try {
    let contents = e && e.postData ? e.postData.contents : null;
    if (!contents) {
      return ContentService.createTextOutput(JSON.stringify({
        status: "error",
        message: "Không tìm thấy dữ liệu POST body."
      })).setMimeType(ContentService.MimeType.JSON);
    }

    let parsed = JSON.parse(contents);
    let expenses = parsed.expenses || (Array.isArray(parsed) ? parsed : []);

    if (!expenses || expenses.length === 0) {
      return ContentService.createTextOutput(JSON.stringify({
        status: "error",
        message: "Không tìm thấy mảng 'expenses' hợp lệ trong dữ liệu JSON."
      })).setMimeType(ContentService.MimeType.JSON);
    }

    let count = processAndWriteToSheet(expenses);

    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      message: `Đã nạp thành công ${count} bản ghi chi phí vào Google Sheet!`,
      count: count
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// 2. Xử lý HTTP GET request (Kiểm tra trạng thái Web App)
function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: "online",
    message: "Google Apps Script Web App API Endpoint đang hoạt động sẵn sàng nhận dữ liệu!"
  })).setMimeType(ContentService.MimeType.JSON);
}

// 3. Tự động tạo Menu tùy chỉnh trên thanh công cụ của Google Sheet
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('📊 Quản lý Chi phí')
    .addItem('📥 Nạp dữ liệu từ data.json', 'importExpensesFromJSONData')
    .addItem('📋 Dán JSON mới để nạp', 'promptAndImportJSON')
    .addToUi();
}

// 4. Hàm nạp dữ liệu mặc định trực tiếp trong Sheet
function importExpensesFromJSONData() {
  const jsonData = {
    "expenses": [
      {
        "Date": "02/05",
        "Employee": "Mai",
        "Item": "An toi tiep khach",
        "Amount": 850000,
        "Category": "Tiep khach",
        "Status": "Can xem lai",
        "AI Note": "Khoản chi lớn hơn 500,000đ, cần phê duyệt cấp quản lý và bổ sung chứng từ tiếp khách."
      },
      {
        "Date": "02/05",
        "Employee": "Nam",
        "Item": "Taxi di gap khach",
        "Amount": 220000,
        "Category": "Di chuyen",
        "Status": "Can chung tu",
        "AI Note": "Khoản chi liên quan đến khách hàng, cần cung cấp hóa đơn/biên lai taxi."
      },
      {
        "Date": "02/05",
        "Employee": "Linh",
        "Item": "Ca phe team",
        "Amount": 180000,
        "Category": "An uong",
        "Status": "Hop le",
        "AI Note": "Chi phí ăn uống nội bộ, mức chi nằm trong hạn mức cho phép."
      },
      {
        "Date": "02/05",
        "Employee": "An",
        "Item": "Mua van phong pham",
        "Amount": 135000,
        "Category": "Van phong",
        "Status": "Hop le",
        "AI Note": "Mua sắm vật tư văn phòng, đầy đủ thông tin và mức chi hợp lý."
      }
    ]
  };
  processAndWriteToSheet(jsonData.expenses);
}

// 5. Hàm phụ: Dán JSON qua Prompt
function promptAndImportJSON() {
  const ui = SpreadsheetApp.getUi();
  const response = ui.prompt('Nạp dữ liệu JSON', 'Vui lòng dán chuỗi JSON chứa mảng "expenses" vào đây:', ui.ButtonSet.OK_CANCEL);

  if (response.getSelectedButton() == ui.Button.OK) {
    const text = response.getResponseText().trim();
    try {
      const parsed = JSON.parse(text);
      const expenses = parsed.expenses || (Array.isArray(parsed) ? parsed : []);
      if (expenses.length === 0) {
        ui.alert('Cảnh báo', 'Không tìm thấy mảng dữ liệu "expenses" trong JSON.', ui.ButtonSet.OK);
        return;
      }
      let count = processAndWriteToSheet(expenses);
      ui.alert('Thành công', `Đã nạp thành công ${count} bản ghi chi phí!`, ui.ButtonSet.OK);
    } catch (e) {
      ui.alert('Lỗi', 'Định dạng JSON không hợp lệ: ' + e.message, ui.ButtonSet.OK);
    }
  }
}

// 6. Hàm xử lý chính: Ghi dữ liệu vào Sheet
function processAndWriteToSheet(expenses) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const headers = ["Date", "Employee", "Item", "Amount", "Category", "Status", "AI Note"];

  // Dòng 1: Header
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setValues([headers]);
  headerRange.setFontWeight("bold");
  headerRange.setBackground("#4A154B");
  headerRange.setFontColor("#FFFFFF");
  headerRange.setHorizontalAlignment("center");

  // Xóa các dòng cũ từ dòng 2
  const lastRow = sheet.getLastRow();
  if (lastRow > 1) {
    sheet.getRange(2, 1, lastRow - 1, headers.length).clearContent();
  }

  if (!expenses || expenses.length === 0) return 0;

  const rows = expenses.map(item => [
    item.Date || "",
    item.Employee || "",
    item.Item || "",
    item.Amount || 0,
    item.Category || "",
    item.Status || "",
    item["AI Note"] || ""
  ]);

  const dataRange = sheet.getRange(2, 1, rows.length, headers.length);
  dataRange.setValues(rows);

  // Định dạng Cột Amount (Cột D)
  const amountRange = sheet.getRange(2, 4, rows.length, 1);
  amountRange.setNumberFormat('#,##0 "VNĐ"');
  amountRange.setHorizontalAlignment("right");

  sheet.getRange(2, 1, rows.length, 2).setHorizontalAlignment("center");
  sheet.getRange(2, 5, rows.length, 2).setHorizontalAlignment("center");

  for (let c = 1; c <= headers.length; c++) {
    sheet.autoResizeColumn(c);
  }

  return rows.length;
}
