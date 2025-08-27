#  LinkEveryWord Desktop App

基於 voidtools Everything 搜尋引擎的桌面應用程式，提供強大的本地檔案搜尋功能。

##  主要功能

-  **即時搜尋**: 基於 Everything SDK 的毫秒級檔案搜尋
-  **Web 介面**: 現代化的響應式 Web 操作介面
-  **獨立執行**: 15MB 的單一執行檔，無需安裝
-  **示範模式**: 即使沒有 Everything 也能體驗功能
-  **單實例保護**: 確保同時只運行一個應用程式實例

## 📚 開發者指南

### Singleton 功能實現
- 📖 **[完整實現指南](SINGLETON_IMPLEMENTATION_GUIDE.md)** - 詳細的實現過程、遇到的問題和解決方案
- 🚨 **[故障排除檢查清單](SINGLETON_TROUBLESHOOTING.md)** - 快速診斷和解決常見問題
- 🧪 **測試腳本**: `test_filelock_singleton.py` - 自動化測試 singleton 功能
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
 app_standalone.py          # 主應用程式 (優化版)
 everything_sdk.py          # Everything SDK Python 包裝
 mock_everything.py         # 示範模式模組
 templates/index.html       # Web 介面模板
 Everything64.dll           # Everything SDK DLL (64位)
 Everything32.dll           # Everything SDK DLL (32位)
 app_standalone.spec        # PyInstaller 打包規格
 version_info.txt           # 執行檔版本資訊
 build.bat                  # 自動打包腳本
 create_release.bat         # 發布包建立腳本
 dist/                      # 打包輸出目錄
     EverythingFlaskSearch.exe  # 主執行檔 (15MB)
     README.txt             # 使用說明
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

##  性能特色

### 最新優化 (v2.0)
-  **消除重複函數調用**: 實例預載入，提升 5-15% 響應速度
-  **單例模式優化**: 減少記憶體佔用
-  **直接實例使用**: 零函數調用開銷

### 詳細報告
- [性能優化報告](PERFORMANCE_OPTIMIZATION.md)
- [專案整理總結](PROJECT_CLEANUP_SUMMARY.md)

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

##  自訂化

### 修改介面
- 編輯 	emplates/index.html
- 調整 CSS 樣式和佈局

### 修改搜尋邏輯
- 編輯 everything_sdk.py
- 調整搜尋參數和結果處理

##  版本歷史

- **v2.0**: 性能優化版本，實例預載入
- **v1.0**: 初始版本，基本搜尋功能

##  貢獻

歡迎提交 Issue 和 Pull Request！

---

**LinkEveryWord Desktop App** - 讓檔案搜尋變得簡單高效 
