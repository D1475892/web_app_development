# 流程圖文件 (Flowchart)

此文件根據 `docs/PRD.md` 的需求與 `docs/ARCHITECTURE.md` 的架構設計，繪製出個人記帳簿系統的使用者流程與系統序列流程。

## 1. 使用者流程圖 (User Flow)

此流程圖描述使用者從進入網站開始，在網頁上的所有操作路徑與可能的分支情境。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 顯示總餘額與功能選單]
    B --> C{要執行什麼操作？}
    
    C -->|新增收入| D[收入表單頁]
    D --> D1[填寫金額、來源、日期]
    D1 --> D2{資料是否有效？}
    D2 -->|是| D3[儲存並回到首頁]
    D2 -->|否| D[提示錯誤，要求重新填寫]
    
    C -->|新增支出| E[支出表單頁]
    E --> E1[填寫金額、分類、日期]
    E1 --> E2{資料是否有效？}
    E2 -->|是| E3[儲存並回到首頁]
    E2 -->|否| E[提示錯誤，要求重新填寫]
    
    C -->|查看紀錄| F[歷史紀錄頁]
    F --> F1[瀏覽所有歷史收支明細]
    
    C -->|查看圖表| G[分類統計頁]
    G --> G1[瀏覽依類別統計的圖表資料]
```

## 2. 系統序列圖 (Sequence Diagram)

此序列圖描述「使用者新增一筆收支紀錄」時的背後技術運作流程，涵蓋瀏覽器、Flask 後端與資料庫。以「新增支出」為例：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (View)
    participant Flask as Flask (Controller)
    participant Model as Transaction (Model)
    participant DB as SQLite 資料庫

    User->>Browser: 在表單輸入支出金額與細節，點擊「送出」
    Browser->>Flask: 發送 POST 請求 (POST /expense)
    Flask->>Flask: 驗證接收到的表單資料
    
    alt 資料無效或不完整
        Flask-->>Browser: 回傳錯誤訊息與原表單頁面
        Browser-->>User: 畫面顯示發生錯誤，請修正資料
    else 資料驗證通過
        Flask->>Model: 建立新的 Transaction 物件
        Model->>DB: 執行 SQL INSERT 指令將資料寫入
        DB-->>Model: 回傳寫入成功
        Model-->>Flask: 儲存完畢
        Flask-->>Browser: 回傳 HTTP Redirect (重導向至首頁)
        Browser->>Flask: 發送 GET / (請求首頁內容)
        Flask->>Model: 查詢最新收支以計算最新餘額
        Model->>DB: 執行 SQL SELECT 結算加總
        DB-->>Model: 回傳最新餘額數字
        Model-->>Flask: 提供餘額給 Controller
        Flask-->>Browser: 將資料注入 Jinja2 渲染後回傳 HTML 頁面
        Browser-->>User: 顯示成功新增的最新餘額畫面
    end
```

## 3. 功能清單對照表

依照前面設計的規劃，以下列出本系統所有的核心功能、對應的 HTTP 方法與預期的 URL 路由設計。

| 主要功能 | 說明 | HTTP 動作 | 預期 URL 路徑 |
| --- | --- | --- | --- |
| **首頁與餘額** | 系統首頁，包含導覽列與目前加總的總餘額 | GET | `/` |
| **新增收入頁面** | 呈現新增收入的 HTML 表單給使用者填寫 | GET | `/income` |
| **送出收入資料** | 接收表單提交的收入資料，處理寫入動作 | POST | `/income` |
| **新增支出頁面** | 呈現新增支出的 HTML 表單給使用者填寫 | GET | `/expense` |
| **送出支出資料** | 接收表單提交的支出資料，處理寫入動作 | POST | `/expense` |
| **歷史紀錄查詢** | 列出所有歷史以來的收支明細清單 | GET | `/history` |
| **分類統計結果** | 顯示各個支出類別的統計結果（如：圓餅圖） | GET | `/statistics` |
