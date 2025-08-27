# 配置文件說明

## 概述
本應用程式現在支援透過 `config.yml` 配置文件來自訂服務器和應用程式設定。

## 配置文件位置
- 配置文件名稱: `config.yml`
- 位置: 與 `app_standalone.py` 相同目錄
- 編碼: UTF-8

## 配置選項

### 服務器配置 (server)

#### host
- 描述: 服務器綁定的主機地址
- 預設值: `'127.0.0.1'`
- 選項:
  - `'127.0.0.1'` - 僅本機存取
  - `'0.0.0.0'` - 允許外部存取 (不建議在生產環境使用)

#### port
- 描述: 服務器監聽的端口號
- 預設值: `5000`
- 範圍: 1-65535 (建議使用 1024 以上的端口)
- 常見選擇: 5000, 8080, 8000, 3000

#### debug
- 描述: Flask 調試模式
- 預設值: `false`
- 選項:
  - `true` - 開啟調試模式 (開發環境)
  - `false` - 關閉調試模式 (生產環境)

#### use_reloader
- 描述: 是否啟用自動重載
- 預設值: `false`
- 選項:
  - `true` - 開啟自動重載 (開發環境)
  - `false` - 關閉自動重載 (生產環境)

### 應用程式配置 (app)

#### name
- 描述: 應用程式顯示名稱
- 預設值: `'Everything Flask 搜尋應用程式'`
- 用途: 日誌顯示和應用識別

#### browser_delay
- 描述: 瀏覽器自動開啟延遲時間 (秒)
- 預設值: `2`
- 建議範圍: 1-5 秒
- 用途: 等待服務器完全啟動後再開啟瀏覽器

## 配置文件範例

### 基本配置 (預設)
```yaml
server:
  host: '127.0.0.1'
  port: 5000
  debug: false
  use_reloader: false

app:
  name: 'Everything Flask 搜尋應用程式'
  browser_delay: 2
```

### 開發環境配置
```yaml
server:
  host: '127.0.0.1'
  port: 8080
  debug: true
  use_reloader: false  # 注意: PyInstaller 環境下建議保持 false

app:
  name: 'Everything Flask 搜尋應用程式 - 開發版'
  browser_delay: 1
```

### 網路共享配置 (謹慎使用)
```yaml
server:
  host: '0.0.0.0'  # 允許網路存取
  port: 5000
  debug: false
  use_reloader: false

app:
  name: 'Everything Flask 搜尋應用程式 - 網路版'
  browser_delay: 3
```

## 注意事項

1. **配置文件遺失**: 如果配置文件不存在或無法讀取，應用程式會使用預設配置並顯示警告信息。

2. **端口衝突**: 如果指定的端口已被佔用，應用程式會顯示錯誤信息並退出。

3. **安全考量**: 
   - 在生產環境中，建議 `debug` 設為 `false`
   - 僅在信任的網路環境中使用 `host: '0.0.0.0'`

4. **檔案編碼**: 確保配置文件使用 UTF-8 編碼，特別是包含中文字符時。

## 測試配置

使用包含的測試腳本驗證配置:
```
python test_config.py
```

## 疑難排解

### 配置載入失敗
- 檢查檔案路徑和名稱 (`config.yml`)
- 確認 YAML 語法正確
- 檢查檔案編碼為 UTF-8

### 端口無法綁定
- 更改 `port` 為其他可用端口
- 確認沒有其他程式佔用該端口
- 在 Windows 上可使用 `netstat -an | findstr :5000` 檢查端口使用狀況

### 無法外部存取
- 確認 `host` 設為 `'0.0.0.0'`
- 檢查防火牆設定
- 確認網路連接正常
