# Logger 系統說明

## 概述

LinkEveryWord Desktop App 集成了完整的日誌記錄系統，支援多種日誌級別、文件輪轉、和靈活的配置選項。

## 功能特色

### 🎯 核心功能
- **多級別日誌**: 支援 DEBUG, INFO, WARNING, ERROR, CRITICAL 五個級別
- **雙重輸出**: 同時支援控制台和文件輸出
- **文件輪轉**: 自動管理日誌文件大小和備份
- **異常追蹤**: 完整的錯誤堆疊資訊記錄
- **UTF-8 編碼**: 完整支援中文字符
- **配置化管理**: 所有設定都可通過 config.yml 調整

### 🔧 配置選項

```yaml
logging:
  # 日誌級別: DEBUG, INFO, WARNING, ERROR, CRITICAL
  level: 'INFO'
  
  # 是否啟用文件日誌
  enable_file: true
  
  # 日誌文件名
  filename: 'app.log'
  
  # 日誌文件最大大小 (MB)
  max_size: 10
  
  # 保留的日誌文件數量
  backup_count: 5
  
  # 是否啟用控制台日誌
  enable_console: true
  
  # 日誌格式
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  
  # 日期格式
  date_format: '%Y-%m-%d %H:%M:%S'
```

## 日誌級別說明

### 1. DEBUG
- **用途**: 詳細的調試資訊
- **建議**: 僅在開發時啟用
- **內容**: 函數調用、變數值、執行流程

### 2. INFO
- **用途**: 一般資訊記錄
- **建議**: 生產環境預設級別
- **內容**: 應用啟動、配置載入、用戶操作

### 3. WARNING
- **用途**: 警告訊息
- **建議**: 需要注意但不影響運行
- **內容**: 配置問題、效能警告、降級使用

### 4. ERROR
- **用途**: 錯誤訊息
- **建議**: 記錄所有錯誤情況
- **內容**: 異常處理、API 錯誤、檔案操作失敗

### 5. CRITICAL
- **用途**: 嚴重錯誤
- **建議**: 應用無法繼續運行的錯誤
- **內容**: 系統崩潰、致命錯誤

## 日誌記錄位置

### 開發環境
- 控制台: 即時顯示所有級別的日誌
- 文件: 儲存在專案目錄 `/desktop-app/app.log`

### 打包環境
- 控制台: 根據配置顯示日誌
- 文件: 儲存在 exe 檔案同目錄 `/app.log`

## 日誌格式說明

### 預設格式
```
2025-08-28 02:43:15 - LinkEveryWord - INFO - 這是一條日誌訊息
```

### 格式組成
- **時間戳**: `2025-08-28 02:43:15`
- **Logger 名稱**: `LinkEveryWord`
- **日誌級別**: `INFO`
- **訊息內容**: `這是一條日誌訊息`

### 異常格式
```
2025-08-28 02:43:15 - LinkEveryWord - ERROR - 發生錯誤: 詳細描述
Traceback (most recent call last):
  File "...", line 123, in function_name
    problematic_code()
ExceptionType: 錯誤詳情
```

## 文件輪轉機制

### 自動輪轉
- **觸發條件**: 文件大小達到 max_size (預設 10MB)
- **輪轉方式**: 
  - `app.log` → `app.log.1`
  - `app.log.1` → `app.log.2`
  - 以此類推...

### 備份管理
- **保留數量**: backup_count 設定 (預設 5 個)
- **清理策略**: 超過數量的舊文件自動刪除
- **命名規則**: `app.log.1`, `app.log.2`, ..., `app.log.5`

## 主要日誌記錄點

### 1. 應用啟動
```
2025-08-28 02:43:15 - LinkEveryWord - INFO - 🚀 LinkEveryWord Desktop App 啟動
2025-08-28 02:43:15 - LinkEveryWord - INFO - 日誌系統初始化完成
2025-08-28 02:43:15 - LinkEveryWord - INFO - 開始初始化搜尋引擎...
```

### 2. 配置載入
```
2025-08-28 02:43:15 - root - INFO - ✓ 配置文件載入成功: config.yml
2025-08-28 02:43:15 - root - INFO - 日誌文件設置完成: app.log
```

### 3. 搜尋操作
```
2025-08-28 02:43:15 - LinkEveryWord - INFO - 搜尋查詢: 'test', 最大結果數: 50
2025-08-28 02:43:15 - LinkEveryWord - DEBUG - 使用 Everything SDK 執行搜尋
2025-08-28 02:43:15 - LinkEveryWord - INFO - 搜尋完成: 找到 100 個結果，返回 50 個，耗時 0.123 秒
```

### 4. 錯誤處理
```
2025-08-28 02:43:15 - LinkEveryWord - ERROR - 搜尋過程中發生錯誤: Connection refused
2025-08-28 02:43:15 - LinkEveryWord - WARNING - Everything SDK 載入失敗: Module not found
```

## 配置範例

### 開發環境配置
```yaml
logging:
  level: 'DEBUG'          # 顯示所有日誌
  enable_file: true       # 啟用文件記錄
  enable_console: true    # 啟用控制台輸出
  max_size: 5             # 較小的文件大小
  backup_count: 3         # 較少的備份數量
```

### 生產環境配置
```yaml
logging:
  level: 'INFO'           # 過濾除錯資訊
  enable_file: true       # 重要：保留文件記錄
  enable_console: false   # 可選：減少控制台輸出
  max_size: 50            # 較大的文件大小
  backup_count: 10        # 較多的備份數量
```

### 僅錯誤記錄配置
```yaml
logging:
  level: 'ERROR'          # 只記錄錯誤和嚴重錯誤
  enable_file: true       # 啟用文件記錄
  enable_console: true    # 啟用控制台輸出
  max_size: 20            # 中等文件大小
  backup_count: 5         # 標準備份數量
```

## 故障排除

### 日誌文件無法創建
**問題**: 提示無法創建日誌文件
**解決方案**:
1. 檢查目錄寫入權限
2. 確保磁碟空間充足
3. 檢查防毒軟體是否阻擋

### 日誌級別不生效
**問題**: 設定 DEBUG 但看不到 DEBUG 日誌
**解決方案**:
1. 重新啟動應用程式
2. 檢查 config.yml 語法是否正確
3. 確認日誌級別拼寫正確

### 日誌文件過大
**問題**: 日誌文件佔用過多磁碟空間
**解決方案**:
1. 降低 max_size 設定
2. 減少 backup_count 數量
3. 提高日誌級別 (例如從 DEBUG 改為 INFO)

### 中文字符亂碼
**問題**: 日誌中的中文顯示為亂碼
**解決方案**:
1. 確保系統支援 UTF-8 編碼
2. 使用支援 UTF-8 的文字編輯器開啟日誌文件
3. 檢查控制台編碼設定

## 最佳實踐

### 1. 級別選擇
- **開發**: 使用 DEBUG 級別，便於問題追蹤
- **測試**: 使用 INFO 級別，記錄重要操作
- **生產**: 使用 WARNING 或 ERROR 級別，減少日誌量

### 2. 文件管理
- 定期檢查日誌文件大小
- 根據需要調整 max_size 和 backup_count
- 重要的錯誤日誌應及時備份

### 3. 效能考量
- DEBUG 級別會影響效能，生產環境謹慎使用
- 考慮停用控制台輸出以提高效能
- 適當的文件輪轉可避免單一大文件影響效能

### 4. 安全性
- 避免在日誌中記錄敏感資訊 (密碼、金鑰等)
- 定期清理過期的日誌文件
- 考慮日誌文件的存取權限設定
