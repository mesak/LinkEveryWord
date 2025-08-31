﻿#  LinkEveryWord Desktop App

<p align="center"><img src="../image.png" width="128"></p>

基於 voidtools Everything 搜尋引擎的桌面應用程式，提供強大的本地檔案搜尋功能。

##  主要功能

-  **即時搜尋**: 基於 Everything SDK 的毫秒級檔案搜尋
-  **彈性備援機制**: 自動在 Everything、Windows Search 和示範模式之間切換
-  **Web 介面**: 現代化的響應式 Web 操作介面
-  **獨立執行**: 15MB 的單一執行檔，無需安裝
-  **高度可配置**: 透過 `config.yml` 檔案自訂服務器和應用程式行為
-  **示範模式**: 即使沒有 Everything 也能體驗功能
-  **單實例保護**: 改用基於文件鎖的機制，確保只有一個應用程式實例在運行
-  **完整日誌系統**: 支援多級別、文件輪轉和控制台輸出 (詳見 LOGGER_GUIDE.md)
-  **中文支援**: 完整的繁體中文介面
-  **萬用字元**: 支援 *.txt, *.pdf 等搜尋模式
-  **詳細資訊**: 顯示檔案大小、修改時間等詳細資訊

##  快速開始

### 方法一：直接執行 (推薦)
`ash
# 下載並執行
dist/EverythingFlaskSearch.exe
`

### 方法二：開發模式
`ash
# 安裝 Python 3.13+
pip install flask flask-cors

# 執行開發版本
python app_standalone.py
`

##  系統需求

- **作業系統**: Windows 10/11
- **Everything**: 建議安裝 voidtools Everything (非必需，有示範模式)
- **瀏覽器**: Chrome, Firefox, Edge 等現代瀏覽器
- **記憶體**: 至少 50MB 可用記憶體

##  建置說明

### 重新打包
`ash
# 使用 PyInstaller 重新打包
python -m PyInstaller app_standalone.spec --clean
`

### 專案結構
`
desktop-app/
 app_standalone.py          # 主應用程式入口
 config.yml                 # 應用程式配置文件
 CONFIG.md                  # 配置文件說明文件
 LOGGER_GUIDE.md            # 日誌系統說明文件
 utils/                     # 核心模組
     ...                    # (包含 Everything, Windows Search 等 SDK 模組)
 templates/                 # Web 介面模板
 static/                    # 靜態檔案 (CSS, JS)
 build.bat                  # 自動打包腳本
 create_release.bat         # 發布包建立腳本
 version_info.txt           # 執行檔版本資訊
 app_standalone.spec        # PyInstaller 打包規格
 dist/                      # 打包輸出目錄
     EverythingFlaskSearch.exe  # 主執行檔
`

##  使用說明

1. **啟動應用程式**
   - 執行 EverythingFlaskSearch.exe
   - 應用程式會自動開啟瀏覽器

2. **搜尋檔案**
   - 在搜尋框輸入關鍵字
   - 支援檔名、路徑、副檔名搜尋
   - 使用 *.txt 搜尋特定類型檔案

3. **檢視結果**
   - 點擊檔案名稱開啟檔案
   - 檢視檔案大小、修改時間等詳細資訊
   - 查看完整檔案路徑

##  技術架構

- **後端**: Python 3.13 + Flask
- **前端**: HTML5 + CSS3 + JavaScript
- **搜尋引擎**: voidtools Everything SDK
- **跨域支援**: Flask-CORS
- **打包工具**: PyInstaller 6.15.0

##  問題排除

### Everything 未安裝
- 應用程式會自動切換到示範模式
- 顯示模擬搜尋結果供測試

### 執行檔無法啟動
- 確認 Windows Defender 沒有阻擋
- 檢查是否有足夠的記憶體空間
- 嘗試以管理員身份執行

### 搜尋結果為空
- 確認 Everything 服務正在運行
- 檢查搜尋關鍵字是否正確
- 訪問 /status 端點檢查狀態

##  API 文件

### 搜尋 API
`
POST /search
{
  "query": "搜尋關鍵字",
  "max_results": 50
}
`

### 狀態檢查
`
GET /status
`

### RESTful 搜尋
`
GET /api/search/{query}?limit=50
`

## ⚙️ 設定與自訂化

本應用程式支援透過 `config.yml` 檔案進行高度自訂化。如果 `config.yml` 不存在，應用程式在首次啟動時會自動創建一份預設的配置文件。

您可以自訂的項目包括：
- **服務器設定**: `host`, `port`, `debug` 模式等。
- **應用程式行為**: `browser_delay` (瀏覽器自動開啟延遲時間)。
- **日誌系統**: `level`, `filename`, `max_size` 等。

詳細的配置選項和說明，請參考 **CONFIG.md** 和 **LOGGER_GUIDE.md** 文件。

##  版本歷史

- **v2.1 (功能增強)**: 新增 `config.yml` 配置文件、備用搜尋引擎、日誌系統並重構專案結構。
- **v2.0**: 性能優化版本，實例預載入
- **v1.0**: 初始版本，基本搜尋功能

##  貢獻

歡迎提交 Issue 和 Pull Request！

---

**LinkEveryWord Desktop App** - 讓檔案搜尋變得簡單高效 
