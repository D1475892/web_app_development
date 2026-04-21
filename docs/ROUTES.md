# 路由設計文件 (API & Routes Design)

這份文件根據 PRD, Architecture 與 DB Design 規劃了系統所有的 Flask 路由及對應的 Jinja2 頁面。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (餘額總覽) | GET | `/` | `index.html` | 計算總餘額並顯示主選單區塊 |
| 新增收入頁面 | GET | `/income` | `income.html` | 顯示新增收入的填寫表單 |
| 送出新增收入 | POST | `/income` | — | 寫入資料庫後重導向至首頁 (`/`) |
| 新增支出頁面 | GET | `/expense` | `expense.html` | 顯示新增支出的填寫表單 |
| 送出新增支出 | POST | `/expense` | — | 寫入資料庫後重導向至首頁 (`/`) |
| 歷史紀錄清單 | GET | `/history` | `history.html` | 撈取歷史明細並以表格呈現 |
| 支出分類圖表 | GET | `/statistics` | `statistics.html` | 撈取各分類支出總和並顯示圖表 |
| 刪除單筆紀錄 | POST | `/transaction/<id>/delete`| — | 以表單形式發送刪除動作後，重導至原記錄頁 |

## 2. 每個路由的詳細說明

### `GET /`
- **處理邏輯**：使用 `TransactionModel.get_all()` 取得所有資料，並區分 `income` 與 `expense` 計算加總。算出「總餘額 = 總收入 - 總支出」。
- **輸出**：將計算後的金額傳遞給 `index.html`。

### `GET /income` 與 `POST /income`
- **輸入**：(POST 時) 表單欄位包含 `amount`, `category`, `transaction_date`。
- **處理邏輯**：
  - GET: 直接回傳填寫畫面。
  - POST: 檢查數值是否為空或不合法 > 使用 `TransactionModel.create(type_='income', ...)` 存入 DB。
- **輸出 / 出錯處理**：成功後重導回 `/`；失敗或缺漏則用 Flask `flash` 發送錯誤訊息，並重新渲染 `income.html`。

### `GET /expense` 與 `POST /expense`
- **輸入**：(POST 時) 表單欄位包含 `amount`, `category`, `transaction_date`。
- **處理邏輯**：同收入的處理，差別在於寫入 DB 時帶入 `type_='expense'`。
- **輸出 / 出錯處理**：成功後重導向至 `/`；失敗則重新渲染 `expense.html` 並提示錯誤。

### `GET /history`
- **處理邏輯**：使用 `TransactionModel.get_all()` 取得完整歷史清單列表。
- **輸出**：傳入清單物件到 `history.html`。

### `GET /statistics`
- **處理邏輯**：撈取 `type='expense'` 的紀錄並依據 `category` 進行分類加總。
- **輸出**：渲染 `statistics.html` 帶入各分類的名稱與加總金額，以提供前端套用如 Chart.js 畫成圖表。

### `POST /transaction/<id>/delete`
- **輸入**：不需要額外參數，利用 URL `id` 識別。
- **處理邏輯**：呼叫 `TransactionModel.delete(transaction_id=id)`。
- **輸出**：刪除後重導向到 `/history`。

## 3. Jinja2 模板清單

所有模板皆將存放在 `app/templates/` 中。

| 檔案名稱 | 介紹 | 繼承對象 |
| --- | --- | --- |
| `base.html` | **核心 HTML 骨架**：包含通用的 `<head>`、頂部導航條 (Navbar)、底部宣告 (Footer) | (此為基礎底底) |
| `index.html` | **首頁**：顯示當前餘額數字與各功能的快速啟動按鈕 | `base.html` |
| `income.html` | **新增收入**：包含輸入金額與來源的 `<form>` 表單 | `base.html` |
| `expense.html`| **新增支出**：包含輸入金額與分類的 `<form>` 表單 | `base.html` |
| `history.html`| **收支明細**：將紀錄透過 `<table>` 陳列每一筆，包含「刪除按鈕」 | `base.html` |
| `statistics.html` | **分類視圖**：預計用 Canvas 呈現各支出類別的佔比圖表 | `base.html` |

## 4. 路由骨架程式碼

路由的骨架已經寫入 `app/routes/` 的對應 Python 檔案中：
- `main.py`: 首頁相關路由 (`/`)
- `income.py`: 收入處理路由 (`/income`)
- `expense.py`: 支出處理路由 (`/expense`)
- `report.py`: 查詢與圖表相關路由 (`/history` 及 `/statistics`)
