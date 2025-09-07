# LinkEveryWord Chrome 擴充功能

<p align="center"><img src="../shared/image.png" width="100%"></p>

強大的 Chrome 擴充功能，連接網頁瀏覽和本地檔案搜尋，讓您能從任何網頁文字選取中即時發現檔案。

## 核心功能

- **🔍 即時文字搜尋**: 在網頁上選取任何文字並即時搜尋您的本地檔案
- **📋 優雅側邊面板**: 簡潔響應式介面顯示搜尋結果
- **⚙️ 靈活配置**: 可自訂後端 API 端點和搜尋參數
- **⌨️ 智慧快捷鍵**: 可配置的鍵盤快捷鍵，無縫整合工作流程
- **🎨 現代 UI**: 使用 shadcn/ui 組件和 Tailwind CSS 打造精美體驗
- **🌍 多語言支援**: 完整的繁體中文和英文介面
- **🔧 進階參數配置**: 支援 JSON 格式的複雜查詢參數
- **⚡ 自動搜尋**: 選取文字後自動觸發搜尋

## 安裝方式

### 從 Chrome 線上應用程式商店安裝 (推薦)
1. 訪問 [Chrome Web Store](https://chromewebstore.google.com/detail/linkeveryword-extension/lkpkimhpldonggkkcoidicbeembcpemj)
2. 點擊「加到 Chrome」
3. 確認安裝並釘選到工具列

### 開發環境設定
```bash
# 複製並安裝依賴
git clone <repository-url>
cd chrome-extension
npm install

# 啟動開發伺服器
npm run dev

# 在 Chrome 中載入擴充功能
# 1. 開啟 Chrome 擴充功能頁面 (chrome://extensions/)
# 2. 啟用開發者模式
# 3. 點擊「載入未封裝項目」並選擇 build/chrome-mv3-dev 目錄
```

### 生產環境建置
```bash
# 建置生產版本
npm run build

# 打包為 .zip 檔案
npm run package
```

## 使用指南

### 快速開始
1. **選取文字**: 在任何網頁上選取文字
2. **按下快捷鍵**: `Ctrl+Shift+F` (可自訂)
3. **查看結果**: 側邊面板會自動開啟並顯示搜尋結果

### 詳細配置
透過以下方式存取擴充功能設定：
- 點擊擴充功能圖示 → 選項
- 配置後端 API URL (例如: `http://127.0.0.1:5000/search`)
- 設定查詢參數 (支援 Key/Value 格式)
- 自訂鍵盤快捷鍵

### 進階功能
- **自動搜尋**: 選取文字後自動觸發搜尋，無需手動點擊
- **參數模板**: 使用 `{{QUERY}}` 佔位符在查詢參數中動態替換選取的文字
- **JSON 參數**: 支援複雜的 JSON 格式查詢參數
- **多語言介面**: 根據瀏覽器語言自動切換中英文介面

## 技術架構

### 技術堆疊
- **框架**: React 18 + TypeScript
- **UI 庫**: shadcn/ui + Tailwind CSS
- **建置工具**: Plasmo Framework
- **清單版本**: Chrome Extension Manifest V3
- **架構**: 現代組件化設計與 Hooks

### 核心組件
- **Background Script**: 處理快捷鍵和訊息傳遞
- **Content Script**: 監聽網頁文字選取和快捷鍵
- **Side Panel**: 主要搜尋介面和結果顯示
- **Options Page**: 擴充功能設定頁面
- **國際化系統**: 完整的中英文支援

## 開發指南

### 開發指令
```bash
# 安裝依賴
npm install

# 開發模式 (熱重載)
npm run dev

# 生產建置
npm run build

# 建立發布包
npm run package
```

### 專案結構
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
│   └── content.ts            # 網頁互動腳本
├── lib/                      # 工具函數和輔助程式
│   └── utils.ts              # 通用工具函數
├── locales/                  # 國際化檔案
│   ├── en/                   # 英文翻譯
│   │   └── messages.json
│   └── zh_TW/                # 繁體中文翻譯
│       └── messages.json
├── _locales/                 # Chrome 擴充功能國際化 (自動生成)
├── build/                    # 建置輸出目錄
│   ├── chrome-mv3-dev/       # 開發版本
│   └── chrome-mv3-prod/      # 生產版本
├── background.ts             # 服務工作者 (背景腳本)
├── sidepanel.tsx             # 主要搜尋介面
├── options.tsx               # 擴充功能設定頁面
├── package.json              # 專案配置
├── tailwind.config.js        # Tailwind CSS 配置
└── tsconfig.json             # TypeScript 配置
```

## API 整合

### 後端需求
擴充功能期望後端提供 REST API 端點，接受 POST 請求：

```http
POST {backendUrl}
Content-Type: application/json

{
  "query": "選取的文字",
  "max_results": 50,
  // 其他自訂參數...
}
```

### 回應格式
```json
{
  "results": [
    {
      "title": "檔案或結果標題",
      "filename": "檔案名稱",
      "description": "簡短描述或檔案路徑",
      "path": "完整檔案路徑",
      "size_formatted": "檔案大小",
      "url": "可選的直接連結"
    }
  ]
}
```

### 與 LinkEveryWord Desktop App 整合
完美配合 LinkEveryWord 桌面應用程式：
```bash
# 預設配置
後端 URL: http://127.0.0.1:5000/search
查詢參數: {
  "query": "{{QUERY}}",
  "max_results": 50
}
```

## 配置系統

### 基本設定
- **後端 URL**: 搜尋 API 的端點位址
- **查詢參數**: 使用 Key/Value 列表配置，支援 JSON 格式
- **快捷鍵**: 透過 Chrome 內建快捷鍵管理設定

### 進階配置
```json
{
  "query": "{{QUERY}}",
  "max_results": 50,
  "search_type": "files",
  "filters": {
    "extensions": [".txt", ".md", ".pdf"],
    "size_limit": "10MB"
  }
}
```

### 參數模板
使用 `{{QUERY}}` 佔位符在任何參數值中動態替換選取的文字：
- 字串值: `"search_term": "{{QUERY}}"`
- 物件屬性: `"filter": {"name": "{{QUERY}}"}`
- 陣列元素: `"terms": ["{{QUERY}}", "additional"]`

## 國際化支援

### 支援語言
- **繁體中文** (zh_TW): 預設語言
- **英文** (en): 完整支援

### 語言檔案
- `locales/zh_TW/messages.json`: 繁體中文翻譯
- `locales/en/messages.json`: 英文翻譯

### 新增語言
1. 在 `locales/` 目錄下建立新的語言資料夾
2. 複製現有的 `messages.json` 並翻譯
3. 更新 `package.json` 中的 `default_locale` 設定

## 故障排除

### 常見問題

#### 1. 擴充功能無法載入
- 確認已啟用開發者模式
- 檢查 `build/chrome-mv3-dev` 目錄是否存在
- 查看 Chrome 擴充功能頁面的錯誤訊息

#### 2. 快捷鍵不生效
- 前往 `chrome://extensions/shortcuts` 檢查快捷鍵設定
- 確認快捷鍵沒有與其他擴充功能衝突
- 重新載入擴充功能

#### 3. 搜尋無結果
- 檢查後端 URL 是否正確
- 確認 LinkEveryWord Desktop App 正在運行
- 查看瀏覽器開發者工具的網路請求

#### 4. 側邊面板無法開啟
- 確認 Chrome 版本支援 Side Panel API (114+)
- 檢查擴充功能權限設定
- 重新安裝擴充功能

#### 5. 參數配置錯誤
- 確認 JSON 格式正確
- 檢查是否包含 `{{QUERY}}` 佔位符
- 查看設定頁面的錯誤提示

## 開發最佳實踐

### 程式碼規範
- 使用 TypeScript 進行類型檢查
- 遵循 React Hooks 最佳實踐
- 使用 Prettier 進行程式碼格式化
- 組件化設計，提高可重用性

### 效能優化
- 使用 React.memo 避免不必要的重新渲染
- 實作防抖機制避免頻繁 API 請求
- 優化 CSS 和圖片資源大小
- 使用 Chrome Storage API 快取設定

### 安全考量
- 驗證所有使用者輸入
- 使用 HTTPS 進行 API 通訊
- 遵循 Chrome 擴充功能安全指南
- 最小化權限請求

## 貢獻指南

### 開發流程
1. Fork 專案倉庫
2. 建立功能分支: `git checkout -b feature/new-feature`
3. 進行開發和測試
4. 確保程式碼品質: `npm run build`
5. 提交 Pull Request

### 程式碼提交規範
- 使用清晰的提交訊息
- 遵循現有的程式碼風格
- 包含適當的測試
- 更新相關文檔

### 測試要求
- 在多個網站測試文字選取功能
- 驗證不同的後端 API 配置
- 測試快捷鍵在各種情況下的表現
- 確認多語言介面正常運作

## 授權資訊

MIT License - 詳見 [LICENSE](../LICENSE) 檔案。

---

## 總結

LinkEveryWord Chrome 擴充功能是一個功能完整的現代化瀏覽器擴充功能，提供：
- 無縫的網頁到本地檔案搜尋體驗
- 直觀的使用者介面和豐富的配置選項
- 完整的多語言支援和國際化
- 與 LinkEveryWord 生態系統的完美整合

擴充功能已準備好用於生產環境，並在 Chrome Web Store 上架供使用者下載使用。
