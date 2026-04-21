# 系統架構設計文件 (Architecture Document)：大學生校園活動報名系統

本文件基於產品需求文件 (PRD) ，規劃大學生校園活動報名系統的技術架構與模組設計。

## 1. 技術架構說明

本專案採用經典的伺服器渲染 (Server-Side Rendering) 架構，不採用前後端分離，以求快速開發與易於部署。

### 1.1 選用技術與原因
*   **後端框架**：**Python + Flask**。Flask 是一個輕量級的框架，非常適合 MVP 開發。它具備直覺的路由設定與高度彈性，能夠快速建立活動與管理 API，滿足核心需求裡「建立活動」、「顯示人數」等動態功能。
*   **模板引擎**：**Jinja2**。直接整合於 Flask 內，用來動態渲染 HTML。因為不需要複雜的前端框架 (如 React / Vue)，使用 Jinja2 配合簡單的 CSS 可以快速實作出「極簡視覺風格」與「手機優先」的前台報名頁面。
*   **資料庫**：**SQLite (透過 SQLAlchemy)**。這是一個輕量級的關聯式資料庫，無需設置獨立資料庫伺服器，資料直接存在本地檔案中 (`database.db`)。對於此 MVP 來說，管理幾百人報名的效能已非常充足，並且 SQLAlchemy ORM 能讓我們輕鬆將名單匯出成 Excel/CSV。

### 1.2 Flask MVC 模式說明
雖然 Flask 本身是 Microframework，但我們將依循 MVC (Model-View-Controller) 的概念來組織程式碼：
*   **Model (模型)**：負責與 SQLite 資料庫溝通的 SQLAlchemy 架構。主要分為 `Event` (活動表單資料與人數上限) 與 `Registration` (報名者名單與學號) 兩種模型。
*   **View (視圖)**：負責呈現給使用者的介面，即 Jinja2 HTML 模板 (`templates/`) 與靜態資源 (`static/`)。包含了學生看到的表單、主辦方看到的中央控制台。
*   **Controller (控制器)**：由 Flask 的路由 (`routes/`) 扮演。職責為接收網頁請求、驗證業務邏輯 (如是否額滿、必填欄位檢查)、呼叫模型存取資料，最後把資料拋給 View 渲染。

---

## 2. 專案資料夾結構

以下為本專案的基礎資料夾結構及檔案用途說明：

```
web_app_development/
├── app/                        # 主要應用程式邏輯目錄
│   ├── __init__.py             # Flask app 實例化與初始化 (如 DB)
│   ├── models/                 # 資料庫模型 (Model)
│   │   └── models.py           # 定義 Event, Registration 結構
│   ├── routes/                 # 路由與業務邏輯 (Controller)
│   │   ├── main.py             # 前台：學生活動報名介面路由 
│   │   └── admin.py            # 後台：主辦方建立/管理/匯出路由
│   ├── templates/              # Jinja2 模板 (View)
│   │   ├── base.html           # 基礎共同 HTML 佈局設計
│   │   ├── index.html          # 活動列表頁面
│   │   ├── event_detail.html   # 學生報名頁面 (顯示人數與欄位)
│   │   └── admin_dashboard.html# 主辦方中央控制台與名單
│   └── static/                 # 靜態資源檔案
│       ├── css/
│       │   └── style.css       # 負責實現 Mobile-First 極簡 UI
│       └── js/
│           └── script.js       # 提示或簡單的 UI 互動腳本
├── instance/                   # 機密或動態產生的檔案
│   └── database.db             # 自動生成的 SQLite 資料庫檔案
├── docs/                       # 專案文件
│   ├── PRD.md                  # 產品需求文件
│   └── ARCHITECTURE.md         # 系統架構文件 (本文件)
├── requirements.txt            # Python 套件套件清單 (Flask 等)
└── app.py                      # 系統執行進入點 (Entry Point)
```

---

## 3. 元件關係圖

以下圖示描繪了從使用者（大學生/管理者）造訪網站時的資料流與系統互動方式。

```mermaid
flowchart TD
    %% 定義角色
    Student([大學生 (手機瀏覽器)])
    Admin([活動主辦方 (電腦端)])

    %% 定義系統元件
    subgraph Flask 伺服器
        direction TB
        Router[Flask 路由 Controller \n (routes/)]
        JinjaTemplate[Jinja2 模板 View \n (templates/)]
        Model[SQLAlchemy 模型 Model \n (models/)]
    end

    %% 資料庫
    DB[(SQLite 資料庫 \n database.db)]
    
    %% 互動流程
    Student -- 1. 請求報名頁 / 送出表單 --> Router
    Admin -- 1. 請求管理頁 / 建立活動 --> Router
    
    Router -- 2. 驗證邏輯與操作資料 --> Model
    Model -. 3. 執行 SQL 指令 .-> DB
    DB -. 4. 回傳查詢結果 .-> Model
    Model -. 5. 轉換為 Python 物件 .-> Router
    
    Router -- 6. 傳遞活動與報名資料 --> JinjaTemplate
    JinjaTemplate -- 7. 渲染完成的 HTML --> Student
    JinjaTemplate -- 7. 渲染完成的 HTML --> Admin
```

---

## 4. 關鍵設計決策

1.  **採用不分離架構 (Flask + Jinja2) 取代 前後端分離 (React + API)**
    *   *原因*：作為大學生活動報名的 MVP 專案，重點在於能在極短時間內開發上線。如果做前後端分離，會多出跨域 (CORS) 處理、API 介接、Token 驗證等成本。統一利用 Flask + Jinja 渲染，能大幅降低學習與除錯時間，且初始頁面加載速度極快。
2.  **自動滿額控管交由 Controller 在後端強制處理**
    *   *原因*：單純隱藏前台的按鈕是不夠的。在接收到 `POST` 報名請求時，Controller 必須立刻在資料庫查詢「目前活動的成功報名數」，並且跟「人數上限」做比較。若超收則強烈拒絕寫入。這能避免系統滿檔熱門時，同時有多個學生點擊造成的超賣爭議。
3.  **採用基於「學號」的免帳號報名機制**
    *   *原因*：要落實 PRD 中「直觀不複雜」的要求，要求學生用 Email 驗證或註冊帳戶會導致極高的跳出率。將「學號」直接作為主要識別碼 (Key)，確保可以快速填表，同時方便後台比對防止重複亂填，符合校園特殊封閉場景的最佳實踐。
4.  **採用 SQLAlchemy ORM 進行資料庫操作**
    *   *原因*：直接寫原生 SQL 語法雖然效能快，但是一旦未來因為需求變更而要增加欄位，會非常難以維護。利用 SQLAlchemy ORM 可以把資料表變為物件操作，並且在未來匯出 Excel/CSV 表格時，可以非常直覺地把物件清單轉為目標格式。
