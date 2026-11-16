/**
 * teppayナビ - 店舗追加・修正リクエスト受信用 Google Apps Script
 * 
 * 【設定手順（初回のみ・所要時間1分）】
 * 1. スプレッドシート（teppayナビ - 店舗追加・修正リクエスト）を開く
 * 2. メニューの「拡張機能」>「Apps Script」をクリック
 * 3. エディタにこのコードをすべて貼り付けて保存（Ctrl+S / Cmd+S）
 * 4. 右上の青い「デプロイ」ボタン >「新しいデプロイ」をクリック
 *    - 種類の選択: 「ウェブアプリ」
 *    - 説明: teppay店舗追加リクエストAPI
 *    - 次のユーザーとして実行: 「自分」
 *    - アクセスできるユーザー: 「全員」（ログイン不要で受付可能にするため）
 * 5. 「デプロイ」を押して、発行された「ウェブアプリのURL」をコピー
 */

function doPost(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName("Requests") || ss.getActiveSheet();
    
    let data = {};
    if (e && e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    } else if (e && e.parameter) {
      data = e.parameter;
    }
    
    // 自動検証ボットからのステータス更新
    if (data.action === "update_status" && data.row_index) {
      const rowIdx = parseInt(data.row_index, 10);
      const nowStr = Utilities.formatDate(new Date(), "Asia/Tokyo", "yyyy-MM-dd HH:mm:ss");
      sheet.getRange(rowIdx, 8, 1, 3).setValues([[data.status || "", data.reason || "", nowStr]]);
      return ContentService.createTextOutput(JSON.stringify({ status: "success", updated_row: rowIdx }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    // 一般ユーザーからの新規リクエスト追加
    const timestamp = Utilities.formatDate(new Date(), "Asia/Tokyo", "yyyy-MM-dd HH:mm:ss");
    const chainName = (data.chain_name || "").toString().trim();
    const storeName = (data.store_name || "").toString().trim();
    const lat = (data.lat || "").toString().trim();
    const lon = (data.lon || "").toString().trim();
    const address = (data.address || "").toString().trim();
    const note = (data.note || "").toString().trim();
    const status = "PENDING";
    const vLog = "";
    const procAt = "";
    
    // スプレッドシートに追記
    sheet.appendRow([timestamp, chainName, storeName, lat, lon, address, note, status, vLog, procAt]);
    
    const output = ContentService.createTextOutput(JSON.stringify({
      status: "success",
      message: "店舗追加リクエストを受け付けました。自動検証を経てマップに反映されます！"
    }));
    output.setMimeType(ContentService.MimeType.JSON);
    return output;
  } catch (err) {
    const output = ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    }));
    output.setMimeType(ContentService.MimeType.JSON);
    return output;
  }
}

function doGet(e) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("Requests") || ss.getActiveSheet();
  const rows = sheet.getDataRange().getValues();
  
  if (rows.length <= 1) {
    return ContentService.createTextOutput(JSON.stringify({ status: "success", count: 0, data: [] }))
      .setMimeType(ContentService.MimeType.JSON);
  }
  
  const headers = rows[0];
  const items = [];
  for (let i = 1; i < rows.length; i++) {
    const row = rows[i];
    items.push({
      row_index: i + 1,
      timestamp: row[0],
      chain_name: row[1],
      store_name: row[2],
      lat: row[3],
      lon: row[4],
      address: row[5],
      note: row[6],
      status: row[7],
      verification_log: row[8],
      processed_at: row[9]
    });
  }
  
  return ContentService.createTextOutput(JSON.stringify({
    status: "success",
    count: items.length,
    data: items
  })).setMimeType(ContentService.MimeType.JSON);
}
