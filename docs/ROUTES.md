# 路由與頁面設計文件 (ROUTES)：大學生校園活動報名系統

本文件基於 PRD 與 DB_DESIGN 設計，詳細列出了 Flask 路由（Routes）與 Jinja2 模板之間的對應關係，確保系統流程串接順暢。

## 1. 路由總覽列表

| 區域 | 功能名稱 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **前台** | 活動總覽清單 | GET | `/` | `index.html` | 呈現所有活動並提供各自連結 |
| **前台** | 活動報名頁面 | GET | `/event/<int:event_id>` | `event_detail.html` | 顯示單一活動介紹與表單 |
| **前台** | 提交報名表單 | POST | `/event/<int:event_id>/register` | — | 檢查人數後寫入，成功則重導 |
| **前台** | 報名成功頁面 | GET | `/event/<int:event_id>/success` | `event_success.html` | 提交成功後看到的提示畫面 |
| **後台** | 管理者控制台 | GET | `/admin` | `admin/dashboard.html` | 列出主辦方的所有活動 |
| **後台** | 新增活動頁面 | GET | `/admin/event/new` | `admin/event_form.html`| 提供主辦方新建活動的表單 |
| **後台** | 建立活動請求 | POST | `/admin/event/new` | — | 寫入資料庫並重導至控制台 |
| **後台** | 檢視報名名單 | GET | `/admin/event/<int:event_id>/registrations` | `admin/registrations.html` | 條列檢視報名學生的表格明細 |
| **後台** | 匯出 CSV 名單 | GET | `/admin/event/<int:event_id>/export` | — | 產生並給予 CSV 檔案下載 |
| **後台** | 手動關閉報名 | POST | `/admin/event/<int:event_id>/close` | — | （擴充防呆）手動將人數上限設 0 |

---

## 2. 路由詳細邏輯說明

### 前台路由 (Student Face)

*   **`GET /`**
    *   **邏輯**：從 Event 模型撈出所有開放的活動清單 (`Event.get_all()`)。
    *   **輸出**：渲染 `index.html`。
*   **`GET /event/<id>`**
    *   **邏輯**：找出場次的資料與目前的報名人數。若「目前人數」等於「容納上限」，則給 View 傳遞額滿布林值。
    *   **輸出**：渲染 `event_detail.html`。
*   **`POST /event/<id>/register`**
    *   **輸入**：表單內容（姓名、學號等）。
    *   **邏輯**：執行 `Registration.get_registration_count()`。如果已滿，返回包含錯誤提示的 400 Bad Request。若未滿，呼叫 `Registration.create(...)` 寫入資料庫。
    *   **輸出**：`redirect(url_for('main.event_success', event_id=id))`。
*   **`GET /event/<id>/success`**
    *   **邏輯**：無特殊處理，僅從資料庫拉取活動基本資訊用於顯示。
    *   **輸出**：渲染 `event_success.html`。

### 後台路由 (Admin Face)

*   **`GET /admin`**
    *   **邏輯**：取得所有活動資料。
    *   **輸出**：渲染 `admin/dashboard.html`。
*   **`GET /admin/event/new`**
    *   **邏輯**：準備空表單給使用者介面。
    *   **輸出**：渲染 `admin/event_form.html`。
*   **`POST /admin/event/new`**
    *   **輸入**：名稱、地點、時間、人數上限等。
    *   **邏輯**：驗證欄位是否都有填上，執行 `Event.create(...)`。
    *   **輸出**：`redirect(url_for('admin.dashboard'))`。
*   **`GET /admin/event/<id>/registrations`**
    *   **邏輯**：呼叫 `Registration.get_by_event(id)` 撈出該場次的所有學生。
    *   **輸出**：渲染 `admin/registrations.html`。
*   **`GET /admin/event/<id>/export`**
    *   **邏輯**：拉取上述學生物件轉為 csv 字串或檔案格式 (`io.StringIO`)。
    *   **輸出**：`Response` (Mimetype 為 `text/csv`) 向客戶端派發下載動作。

---

## 3. Jinja2 模板清單 (Templates)

所有前台相關存放在根目錄，後台相關存放在 `admin/` 中：

1.  `base.html`：所有頁面繼承的基礎 Layout，包含 `<head>` 與共用主結構。
2.  `index.html`：**繼承自 base**。前台首頁。
3.  `event_detail.html`：**繼承自 base**。顯示活動詳細資訊。
4.  `event_success.html`：**繼承自 base**。成功報名提示頁。
5.  `admin/dashboard.html`：**繼承自 base**。主辦方管理總覽頁。
6.  `admin/event_form.html`：**繼承自 base**。建立活動用表單。
7.  `admin/registrations.html`：**繼承自 base**。詳細學生名單表。
