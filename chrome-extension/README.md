#  LinkEveryWord Chrome Extension

Chrome 瀏覽器套件，讓您在瀏覽時快速搜尋和連結檔案 (規劃中)

##  專案願景

LinkEveryWord Chrome Extension 將瀏覽器與本地檔案系統無縫連接，讓使用者可以在瀏覽網頁時快速找到相關的本地檔案，或將網頁內容與本地檔案建立連結。

##  規劃功能

### 核心功能
-  **快速搜尋**: 在任何網頁上快速搜尋本地檔案
-  **智慧連結**: 自動識別網頁內容並建議相關檔案
-  **快捷鍵操作**: 自訂快捷鍵快速呼叫搜尋
-  **右鍵選單**: 選取文字後直接搜尋相關檔案

### 進階功能
-  **網頁標籤**: 為網頁添加標籤並與本地檔案連結
-  **書籤增強**: 增強瀏覽器書籤功能，連結本地檔案
-  **同步功能**: 與 Desktop App 和 Web App 同步搜尋歷史
-  **使用統計**: 追蹤最常搜尋的檔案和關鍵字

### 整合功能
-  **Desktop App 通訊**: 直接與本地桌面應用程式通訊
-  **Web App 整合**: 雲端搜尋和本地搜尋統一介面
-  **跨瀏覽器**: 支援 Chrome, Firefox, Edge 等主流瀏覽器
-  **第三方整合**: 與 Notion, Obsidian 等知識管理工具整合

##  技術堆疊 (規劃)

### 核心技術
- **Manifest V3**: 使用最新的 Chrome Extension API
- **框架**: Vanilla JS / React / Vue.js
- **打包工具**: Webpack / Vite / Rollup
- **UI 庫**: Material Web Components / Ant Design / 自訂 CSS

### 通訊機制
- **Native Messaging**: 與 Desktop App 原生通訊
- **WebSocket**: 與 Web App 即時通訊
- **Storage API**: 本地資料存儲和同步
- **Content Scripts**: 網頁內容分析和互動

### 開發工具
- **TypeScript**: 型別安全的 JavaScript
- **ESLint + Prettier**: 程式碼品質和格式化
- **Jest**: 單元測試框架
- **Chrome DevTools**: 擴展程式除錯

##  預期目錄結構

`
chrome-extension/
  README.md                   # 專案說明
  manifest.json               # 擴展程式設定檔
  src/                        # 原始碼
    background/                # 背景腳本
       service-worker.js      # 主要背景服務
    content/                   # 內容腳本
       content-script.js      # 網頁內容互動
       content-style.css      # 內容樣式
    popup/                     # 彈出視窗
       popup.html             # 彈出視窗 HTML
       popup.js               # 彈出視窗邏輯
       popup.css              # 彈出視窗樣式
    options/                   # 設定頁面
       options.html           # 設定頁面 HTML
       options.js             # 設定頁面邏輯
       options.css            # 設定頁面樣式
    shared/                    # 共用元件
       api.js                 # API 通訊模組
       storage.js             # 資料存儲模組
       utils.js               # 工具函數
    assets/                    # 靜態資源
        icons/                 # 圖示檔案
        images/                # 圖片資源
        fonts/                 # 字型檔案
  build/                      # 建置工具
    webpack.config.js          # Webpack 設定
    build.js                   # 建置腳本
    package.js                 # 打包腳本
  docs/                       # 文件
    user-guide.md              # 使用指南
    developer-guide.md         # 開發指南
    api.md                     # API 文件
  tests/                      # 測試檔案
    unit/                      # 單元測試
    integration/               # 整合測試
    e2e/                       # 端對端測試
  dist/                       # 建置輸出
    linkeveryword-extension.zip # 發布包
  package.json                # 專案依賴
`

##  UI/UX 設計

### 設計原則
- **最小干擾**: 不影響使用者正常瀏覽體驗
- **快速存取**: 一鍵搜尋，即時結果
- **視覺一致**: 與 Desktop App 和 Web App 保持設計一致
- **直觀操作**: 符合 Chrome 擴展程式的操作習慣

### 介面元件
-  **工具列按鈕**: 快速開啟搜尋面板
-  **搜尋面板**: 浮動搜尋介面
-  **右鍵選單**: 快速搜尋選取文字
-  **設定頁面**: 偏好設定和快捷鍵配置
-  **統計面板**: 搜尋歷史和使用分析

##  功能規格

### 搜尋功能
- **即時搜尋**: 輸入關鍵字即時顯示結果
- **模糊搜尋**: 支援拼字錯誤容錯
- **檔案類型篩選**: 依副檔名快速篩選
- **路徑搜尋**: 支援目錄路徑搜尋

### 互動功能
- **檔案預覽**: 滑鼠懸停顯示檔案資訊
- **快速開啟**: 點擊結果直接開啟檔案
- **拖拽操作**: 拖拽檔案到網頁輸入框
- **複製路徑**: 一鍵複製檔案路徑

### 智慧功能
- **內容分析**: 分析網頁內容建議相關檔案
- **關鍵字提取**: 自動提取網頁關鍵字進行搜尋
- **學習偏好**: 記住使用者搜尋習慣
- **個人化推薦**: 基於歷史推薦相關檔案

##  開發階段

### Phase 1: 基礎功能
- [ ] 基本擴展程式架構
- [ ] 與 Desktop App 通訊
- [ ] 簡單搜尋介面
- [ ] 工具列按鈕和彈出視窗

### Phase 2: 核心功能
- [ ] 內容腳本注入
- [ ] 右鍵選單整合
- [ ] 快捷鍵支援
- [ ] 搜尋結果優化

### Phase 3: 進階功能
- [ ] 智慧內容分析
- [ ] 與 Web App 整合
- [ ] 跨瀏覽器支援
- [ ] 進階設定選項

##  隱私與安全

### 資料保護
- **本地優先**: 搜尋資料優先在本地處理
- **最小權限**: 只請求必要的瀏覽器權限
- **透明度**: 清楚說明資料使用方式
- **使用者控制**: 使用者完全控制資料同步

### 安全措施
- **Content Security Policy**: 防止 XSS 攻擊
- **權限驗證**: 確保與 Desktop App 通訊安全
- **資料加密**: 敏感資料加密存儲
- **定期審查**: 定期進行安全審查

##  安裝與發布

### Chrome Web Store
- [ ] 準備商店資料 (圖示、截圖、描述)
- [ ] 通過 Chrome Web Store 審查
- [ ] 設定自動更新機制
- [ ] 收集使用者回饋

### 其他瀏覽器
- [ ] Firefox Add-ons 適配
- [ ] Microsoft Edge Add-ons 適配
- [ ] Safari Extension 考量

##  如何參與

目前 Chrome Extension 還在規劃階段，歡迎：

1. **功能建議**: 分享您希望的瀏覽器整合功能
2. **使用案例**: 描述您的典型使用情境
3. **技術討論**: 參與技術架構和實作討論
4. **測試協助**: 協助測試早期版本

##  聯絡我們

-  Email: [待添加]
-  Discord: [待建立]
-  Twitter: [待建立]

---

**即將推出** - 將瀏覽器與檔案系統無縫連接！ 
