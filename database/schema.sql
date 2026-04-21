-- 資料庫遷移與建表描述檔
-- SQLite Dialect

-- 1. 建立 Event (活動表)
CREATE TABLE IF NOT EXISTS event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    location TEXT NOT NULL,
    event_date DATETIME NOT NULL,
    capacity_limit INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 建立 Registration (報名紀錄表)
CREATE TABLE IF NOT EXISTS registration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    student_id TEXT NOT NULL,
    student_name TEXT NOT NULL,
    department_grade TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(event_id) REFERENCES event(id) ON DELETE CASCADE
);

-- (選用) 加快查詢報名人數的 Index (當活動大量時有用)
CREATE INDEX IF NOT EXISTS idx_registration_event_id ON registration (event_id);
