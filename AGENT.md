# LinkEveryWord AI 開發指南

## 專案概述

LinkEveryWord 是一個強大的跨平台檔案搜尋生態系統，提供閃電般快速的檔案發現和無縫的文字到檔案連結功能。本專案採用現代網頁技術構建，在桌面和瀏覽器環境中提供即時搜尋能力。

### 專案架構

```
LinkEveryWord/
├── desktop-app/          # 桌面應用程式
├── chrome-extension/     # Chrome 擴充功能
├── web/                  # Web 平台
├── shared/              # 共用資源 (圖示、圖片等)
└── 文檔檔案             # README、授權、配置指南等
```

## 核心組件詳解

### 1. 桌面應用程式 (Desktop App) - 已完成

**技術堆疊**: Python 3.13 + Flask + Everything SDK + PyInstaller
**狀態**: 生產就緒，功能完整
**檔案位置**: `/desktop-app/`

#### 主要功能
- ⚡ 毫秒級檔案搜尋 (基於 Everything SDK)
- 🔄 智慧備援系統 (Everything → Windows Search → Demo Mode)
- 🌐 現代 Web 介面 (HTML5 + CSS3 + JavaScript)
- 📦 15MB 獨立執行檔，免安裝
- ⚙️ 高度可配置 (config.yml)
- 🎯 示範模式支援
- 🔒 單例保護機制
- 📊 完整日誌系統
- 🌍 中文介面支援

#### 核心檔案結構
```
desktop-app/
├── app_standalone.py          # 主應用程式進入點
├── config.yml                 # 應用程式配置檔
├── utils/                     # 核心模組
│   ├── everything_sdk.py      # Everything SDK 整合
│   ├── windows_search.py      # Windows 搜尋備援
│   └── demo_mode.py          # 示範模式實作
├── templates/                 # Jinja2 網頁介面模板
├── build.bat                 # 自動化建置腳本
├── app_standalone.spec       # PyInstaller 建置規格
└── dist/                     # 建置輸出目錄
    └── EverythingFlaskSearch.exe  # 主執行檔
```

#### API 端點
```http
# POST 搜尋 (JSON)
POST /search
Content-Type: application/json
{
  "query": "搜尋關鍵字",
  "max_results": 50
}

# GET 搜尋 (查詢參數)
GET /api/search/{query}?limit=50

# 狀態檢查
GET /status
```

#### 配置系統
透過 `config.yml` 進行完整配置：
- 伺服器設定 (host, port, debug)
- 應用程式行為 (browser_delay, name)
- 日誌系統 (level, file rotation, format)

### 2. Chrome 擴充功能 (Chrome Extension) - 已完成

**技術堆疊**: React 18 + TypeScript + shadcn/ui + Tailwind CSS + Plasmo Framework
**狀態**: 生產就緒，已上架 Chrome Web Store
**檔案位置**: `/chrome-extension/`

#### 主要功能
- 🔍 即時文字搜尋 (選取文字自動觸發搜尋)
- 📋 優雅側邊面板 (Chrome Side Panel API)
- ⚙️ 靈活後端 API 配置 (支援 JSON 格式參數)
- ⌨️ 可自訂快捷鍵 (預設 Ctrl+Shift+F)
- 🎨 現代 UI 設計 (shadcn/ui + Tailwind CSS)
- 🌍 完整多語言支援 (繁體中文/英文)
- 🔧 進階參數模板 ({{QUERY}} 佔位符系統)

#### 核心檔案結構
```
chrome-extension/
├── assets/                    # 靜態資源和圖示
├── components/                # React 組件
│   └── ui/                   # shadcn/ui 組件庫
│       ├── button.tsx        # 按鈕組件
│       ├── card.tsx          # 卡片組件
│       ├── input.tsx         # 輸入框組件
│       └── label.tsx         # 標籤組件
├── contents/                  # 內容腳本
│   └── content.ts            # 網頁互動和快捷鍵監聽
├── lib/                      # 工具函數
│   └── utils.ts              # 通用工具函數
├── locales/                  # 國際化檔案
│   ├── en/messages.json      # 英文翻譯
│   └── zh_TW/messages.json   # 繁體中文翻譯
├── _locales/                 # Chrome 擴充功能國際化 (自動生成)
├── build/                    # 建置輸出
│   ├── chrome-mv3-dev/       # 開發版本
│   └── chrome-mv3-prod/      # 生產版本
├── background.ts             # 服務工作者 (背景腳本)
├── sidepanel.tsx             # 主搜尋介面
├── options.tsx               # 擴充功能設定頁面
├── package.json              # 專案配置
└── manifest (自動生成)       # Chrome Extension Manifest V3
```

#### API 整合系統
```http
# POST 請求格式
POST {backendUrl}
Content-Type: application/json

{
  "query": "{{QUERY}}",        # 自動替換選取的文字
  "max_results": 50,
  // 其他自訂參數...
}

# 回應格式
{
  "results": [
    {
      "title": "檔案標題",
      "filename": "檔案名稱", 
      "path": "完整路徑",
      "size_formatted": "檔案大小"
    }
  ]
}
```

#### 與桌面應用整合
- 預設後端 URL: `http://127.0.0.1:5000/search`
- 查詢參數模板: `{"query": "{{QUERY}}", "max_results": 50}`
- 支援複雜 JSON 參數配置
- 自動佔位符替換系統

#### 開發和建置
```bash
# 開發模式
npm install
npm run dev

# 生產建置
npm run build
npm run package

# Chrome 載入 (開發)
# 載入 build/chrome-mv3-dev 目錄
```

### 3. Web 平台 (Web Platform) - 已完成

**技術堆疊**: Hono + TypeScript + Cloudflare Pages/Workers
**狀態**: 生產就緒，功能完整
**檔案位置**: `/web/`

#### 主要功能
- � 完平整多語言支援 (繁體中文/英文)
- � 專用案文檔和安裝指南中心
- �  隱私政策管理和託管
- ⚡ 全球邊緣部署 (Cloudflare Pages)
- 📱 響應式現代 UI 設計
- 🔄 自動化內容管理系統
- 🎯 智慧語言檢測和切換

#### 核心檔案結構
```
web/
├── functions/
│   └── [[_path]].ts          # Cloudflare Pages Functions 入口
├── src/
│   ├── content/              # 自動生成的內容檔案
│   │   ├── privacy.zh.ts     # 繁中隱私政策 (自動生成)
│   │   └── privacy.en.ts     # 英文隱私政策 (自動生成)
│   ├── i18n/                # 國際化系統
│   │   ├── types.ts         # TypeScript 類型定義
│   │   ├── zh.ts            # 繁體中文翻譯
│   │   └── en.ts            # 英文翻譯
│   └── types/               # TypeScript 類型定義
├── content/                 # 源 Markdown 檔案
│   ├── privacy-policy.md    # 繁中隱私政策源檔案
│   └── privacy-policy.en.md # 英文隱私政策源檔案
├── assets/                  # 靜態資源
├── scripts/
│   └── sync-privacy.mjs     # 內容同步腳本
├── package.json             # 依賴和腳本配置
├── wrangler.jsonc           # Cloudflare 配置
└── tsconfig.json            # TypeScript 配置
```

#### 路由系統
```http
# 主要頁面
GET /                    # 專案首頁
GET /install/chrome      # Chrome 擴充功能安裝指南
GET /install/desktop     # 桌面應用程式安裝指南
GET /privacy             # 隱私政策頁面

# 語言切換
GET /?lang=zh           # 繁體中文
GET /?lang=en           # 英文
```

#### 內容管理系統
- **自動化同步**: Markdown → TypeScript 自動轉換
- **多語言管理**: 完整的 i18n 系統
- **資源同步**: 從 shared 目錄自動同步圖片和圖示
- **類型安全**: 完整的 TypeScript 類型定義

#### 部署和開發
```bash
# 本地開發
npm install
npm run dev

# 內容同步
npm run sync:privacy

# 部署到 Cloudflare Pages
npm run deploy

# 類型檢查
npm run typecheck
```

## 開發指導原則

### 技術原則
1. **設計一致性**: 三個組件保持視覺和操作一致
2. **無縫整合**: 組件間資料和功能互通
3. **跨平台支援**: 支援各種作業系統和設備
4. **隱私優先**: 本地優先，使用者資料控制
5. **效能優化**: 毫秒級響應，最小資源佔用

### 程式碼規範
1. **模組化設計**: 功能獨立，易於維護和擴展
2. **錯誤處理**: 完整的異常處理和優雅降級
3. **日誌記錄**: 詳細的操作日誌和錯誤追蹤
4. **配置化**: 所有設定都可透過配置檔調整
5. **國際化**: 支援多語言，預設中文

### 開發環境設定

#### 桌面應用程式
```bash
cd desktop-app
pip install -r requirements.txt
python app_standalone.py
```

#### Chrome 擴充功能 (規劃)
```bash
cd chrome-extension
npm install
npm run dev
```

## 建置和部署

### 桌面應用程式建置
```bash
cd desktop-app
# 開發模式
python app_standalone.py

# 建置執行檔
./build.bat
# 或
python -m PyInstaller app_standalone.spec --clean
```

### 測試指南

#### 持續運行測試
```bash
# 背景啟動服務
cd desktop-app && start /b python app_standalone.py

# 檢查服務狀態
curl http://127.0.0.1:5000/status

# 查看日誌
type desktop-app/app.log

# 停止服務
taskkill /f /im python.exe
```

## 配置管理

### 桌面應用程式配置 (config.yml)
```yaml
server:
  host: '127.0.0.1'
  port: 5000
  debug: false
  use_reloader: false

app:
  name: 'Everything Flask 搜尋應用程式'
  browser_delay: 2

logging:
  level: 'INFO'
  enable_file: true
  filename: 'app.log'
  max_size: 10
  backup_count: 5
  enable_console: true
```

### 日誌系統
- **多級別**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **雙重輸出**: 控制台 + 檔案
- **自動輪轉**: 檔案大小管理和備份
- **UTF-8 編碼**: 完整中文支援

## 故障排除

### 常見問題

#### 1. Everything SDK 無法載入
- **症狀**: 搜尋結果為空或錯誤訊息
- **解決**: 自動切換到 Windows Search 或 Demo Mode
- **檢查**: 訪問 `/status` 端點確認當前搜尋引擎

#### 2. 端口被佔用
- **症狀**: 應用程式無法啟動
- **解決**: 修改 `config.yml` 中的 `port` 設定
- **檢查**: `netstat -an | findstr :5000`

#### 3. 執行檔無法啟動
- **可能原因**: Windows Defender、防毒軟體、權限不足
- **解決**: 添加例外、以管理員身分執行

#### 4. 中文字符亂碼
- **原因**: 編碼問題
- **解決**: 確保系統支援 UTF-8，使用支援 UTF-8 的編輯器

## 開發優先級

### 第一優先 (已完成)
- ✅ Desktop App 核心功能和完整建置流程
- ✅ Chrome Extension 完整功能和 Chrome Web Store 上架
- ✅ Web Platform 多語言文檔中心和全球部署
- ✅ 完整的生態系統整合和互操作性
- ✅ 詳細文檔和配置指南
- ✅ 自動化內容管理和建置系統

### 第二優先 (進行中)
- 🔄 使用者體驗優化和回饋收集
- 🔄 效能優化和穩定性提升
- 🔄 社群建設和使用者支援

### 第三優先 (未來)
- 📋 進階功能開發 (AI 搜尋、智慧連結、語義搜尋)
- 📋 團隊協作功能 (共享搜尋、協作標註)
- 📋 行動應用考量 (iOS/Android 支援)
- 📋 API 生態系統擴展 (第三方整合、插件系統)
- 📋 企業級功能 (SSO、權限管理、審計日誌)

## 貢獻指南

### 開發流程
1. Fork 專案倉庫
2. 建立功能分支
3. 進行開發和測試
4. 提交 Pull Request
5. 程式碼審查和合併

### 程式碼提交規範
- 使用清晰的提交訊息
- 遵循現有的程式碼風格
- 包含適當的測試
- 更新相關文檔

### 測試要求
- 單元測試覆蓋核心功能
- 整合測試驗證組件互動
- 效能測試確保響應速度
- 相容性測試支援多平台

## 專案資源

### 重要檔案
- `README.md` / `README_ZH.md`: 專案總覽
- `desktop-app/README.md`: 桌面應用詳細說明
- `desktop-app/CONFIG.md`: 配置檔案說明
- `desktop-app/LOGGER_GUIDE.md`: 日誌系統指南
- `PROJECT_RESTRUCTURE.md`: 專案重組記錄

### 外部依賴
- **Everything SDK**: voidtools Everything 搜尋引擎
- **Python 3.13+**: 桌面應用程式執行環境
- **Flask**: Web 框架
- **PyInstaller**: 執行檔打包工具

### 授權資訊
- **授權**: MIT License
- **檔案**: `LICENSE`
- **原則**: 開源、自由使用和修改

---

## 總結

LinkEveryWord 是一個功能完整的檔案搜尋生態系統，所有核心組件均已達到生產就緒狀態並正式發布。專案採用模組化設計，各組件可獨立開發和部署，同時保持整體的一致性和互操作性。

## 當前完成狀態
- **Desktop App (100%)**: 完整的本地檔案搜尋應用程式，15MB 獨立執行檔
- **Chrome Extension (100%)**: 已上架 Chrome Web Store 的瀏覽器擴充功能
- **Web Platform (100%)**: 多語言文檔中心，部署於 Cloudflare Pages

## 生態系統整合
三個組件形成完整的搜尋生態系統：
1. **Desktop App** 提供本地檔案索引和搜尋 API
2. **Chrome Extension** 連接網頁瀏覽和本地搜尋
3. **Web Platform** 提供文檔、安裝指南和專案展示

## 技術成就
- **跨平台整合**: Windows 桌面 + Chrome 瀏覽器 + 全球 Web 平台
- **多語言支援**: 完整的繁體中文和英文介面
- **現代技術堆疊**: Python/Flask、React/TypeScript、Hono/Cloudflare
- **自動化流程**: 建置、部署、內容管理全自動化
- **生產就緒**: 所有組件均已發布並可供使用者下載使用

對於 AI 開發助手，建議：
1. **深入理解完整生態系統**：三個組件的架構、功能和整合方式
2. **掌握多技術堆疊**：Python/Flask、React/TypeScript、Hono/Cloudflare Pages
3. **遵循既定的設計原則**：多語言支援、自動化流程、類型安全、使用者體驗
4. **利用現有的基礎設施**：建置系統、配置管理、國際化框架
5. **保持生態系統一致性**：UI 設計、API 規範、文檔風格、品牌形象
6. **關注使用者回饋**：持續優化和改進現有功能

專案已成功建立了完整的檔案搜尋生態系統，準備好進入下一階段的優化、擴展和創新！