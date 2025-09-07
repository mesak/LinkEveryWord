# LinkEveryWord Web 平台

<p align="center"><img src="assets/image.png" width="100%"></p>

基於 Cloudflare Pages 和 Hono 框架構建的現代化多語言 Web 平台，作為 LinkEveryWord 專案的中央樞紐，提供文檔、安裝指南和隱私政策服務。

## 🎨 最新設計更新

### 現代化 UI 設計
- **深色主題**: 採用現代深色配色方案，提供舒適的視覺體驗
- **漸層效果**: 使用精美的漸層背景和按鈕效果
- **響應式設計**: 完全適配桌面、平板和手機設備
- **微互動**: 添加 hover 效果和平滑過渡動畫

### 改進的用戶體驗
- **清晰的導航**: 重新設計的頂部導航欄，更好的視覺層次
- **功能卡片**: 首頁採用卡片式佈局展示主要功能
- **視覺圖標**: 為每個功能添加表意圖標，提升可讀性
- **優化排版**: 改善文字層次和間距，提升閱讀體驗

### 保留核心功能
- ✅ **Buy Me a Coffee 整合**: 保留原有的贊助功能
- ✅ **多語言支援**: 繁體中文和英文無縫切換
- ✅ **所有原有功能**: 安裝指南、隱私政策等頁面全部保留

## 核心功能

- **🌍 多語言支援**: 繁體中文和英文之間的無縫語言切換
- **📱 響應式設計**: 移動優先的現代 UI 設計
- **⚡ 邊緣效能**: 基於 Cloudflare Pages 的全球低延遲交付
- **🔒 隱私合規**: 完整的隱私政策管理和託管
- **📖 文檔中心**: 集中化的安裝指南和專案資訊
- **🎨 現代技術堆疊**: 使用 Hono 框架和 TypeScript 確保類型安全
- **🔄 自動化內容管理**: Markdown 到 TypeScript 的自動同步系統
- **🎯 智慧語言檢測**: 基於 URL 參數、Cookie 和 Accept-Language 的語言偵測

## 技術架構

### 技術堆疊
- **框架**: Hono (輕量級 Web 框架)
- **運行時**: Cloudflare Workers/Pages Functions
- **語言**: TypeScript (完整類型安全)
- **部署**: Cloudflare Pages (自動 CI/CD)
- **路由**: 基於檔案的動態路由系統
- **內容管理**: Markdown + 自動化同步腳本
- **國際化**: 完整的 i18n 系統

### 路由結構
```
/                    # 專案首頁
/install/chrome      # Chrome 擴充功能安裝指南
/install/desktop     # 桌面應用程式安裝指南
/privacy             # 隱私政策頁面
```

### 語言系統
支援智慧語言檢測和切換：
- **URL 參數**: `?lang=zh` 或 `?lang=en`
- **Cookie 持久化**: 自動記住用戶語言偏好
- **Accept-Language**: 瀏覽器語言偏好檢測
- **預設語言**: 繁體中文

## 開發指南

### 環境需求
- Node.js 18+
- 網路連接 (Wrangler 引導需要)
- Cloudflare 帳戶 (部署需要)

### 本地開發
```bash
# 進入專案目錄
cd web

# 安裝依賴
npm install

# 啟動開發伺服器
npm run dev

# 開啟瀏覽器訪問顯示的 URL (例如 http://localhost:8788)
```

### 語言切換測試
```bash
# 繁體中文 (預設)
http://localhost:8788/?lang=zh
http://localhost:8788/install/chrome?lang=zh

# 英文
http://localhost:8788/?lang=en
http://localhost:8788/install/desktop?lang=en
```

## 內容管理系統

### 隱私政策自動化系統
平台具備完整的隱私政策自動化管理系統：

**源檔案（需保留，請直接編輯這些 Markdown）** 位於 `web/content/`：
- `privacy-policy.md`（繁體中文）
- `privacy-policy.en.md`（英文）

**生成檔案（由腳本自動產生，請勿手動編輯）** 位於 `web/src/content/`：
- `privacy.zh.ts`（由繁中 Markdown 生成，供執行時載入）
- `privacy.en.ts`（由英文 Markdown 生成，供執行時載入）

說明：網站在執行時會直接匯入上述 TypeScript 內容檔（`privacy.zh.ts`/`privacy.en.ts`）。Markdown 是唯一來源（source of truth），請只修改 `web/content` 下的檔案，然後執行同步腳本生成 TS 檔。

**同步流程**:
```bash
# 手動同步隱私政策 (從 Markdown 到 TypeScript)
npm run sync:privacy

# 自動同步 (在 npm install 後自動執行)
npm run postinstall
```

### 資源管理
共用資源自動同步機制：
```bash
# 資源映射
shared/app_icon.svg → web/assets/logo.svg
shared/image.png → web/assets/image.png

# 同步腳本位置
scripts/sync-privacy.mjs
```

### 國際化 (i18n) 系統
```typescript
// 語言檔案結構
src/i18n/
├── types.ts          # TypeScript 類型定義
├── zh.ts            # 繁體中文翻譯
└── en.ts            # 英文翻譯

// 使用方式
const { dict, code } = getLang(c)
const title = dict.home.title
```

## 部署

### Cloudflare Pages 部署
```bash
# 部署到生產環境
npm run deploy

# 預覽部署
npm run preview

# 類型檢查
npm run typecheck
```

### 配置檔案
- `wrangler.jsonc`: Cloudflare Pages 配置
- `tsconfig.json`: TypeScript 編譯配置
- `package.json`: 專案依賴和腳本

## 專案結構

```
web/
├── functions/
│   └── [[_path]].ts      # Cloudflare Pages Functions 入口點
├── src/
│   ├── content/          # 自動生成的內容檔案
│   │   ├── privacy.zh.ts # 繁中隱私政策（自動生成，請勿手改）
│   │   └── privacy.en.ts # 英文隱私政策（自動生成，請勿手改）
│   ├── i18n/            # 國際化系統
│   │   ├── types.ts     # 類型定義
│   │   ├── zh.ts        # 繁體中文
│   │   └── en.ts        # 英文
│   └── types/           # TypeScript 類型定義
├── content/             # 源 Markdown 檔案（請編輯這裡）
│   ├── privacy-policy.md    # 繁中隱私政策（來源）
│   └── privacy-policy.en.md # 英文隱私政策（來源）
├── assets/              # 靜態資源
│   ├── logo.svg         # 專案 Logo (從 shared 同步)
│   ├── image.png        # 專案圖片 (從 shared 同步)
│   └── favicon.ico      # 網站圖示
├── scripts/
│   └── sync-privacy.mjs # 內容同步腳本
├── package.json         # 依賴和腳本配置
├── wrangler.jsonc       # Cloudflare 配置
└── tsconfig.json        # TypeScript 配置
```

## 核心功能實作

### 動態路由系統
```typescript
// functions/[[_path]].ts 中的路由處理
app.get('/', homePage)                    # 首頁
app.get('/install/chrome', chromePage)    # Chrome 安裝
app.get('/install/desktop', desktopPage)  # Desktop 安裝
app.get('/privacy', privacyPage)          # 隱私政策
```

### 語言檢測邏輯
```typescript
const getLang = (c: Context): { dict: Dict; code: 'zh' | 'en' } => {
  // 1. URL 參數優先
  // 2. Cookie 持久化
  // 3. Accept-Language 檢測
  // 4. 預設繁體中文
}
```

### 內容渲染系統
- **靜態內容**: 透過 i18n 系統提供多語言支援
- **動態內容**: Markdown 轉 HTML (使用 marked 庫)
- **樣式系統**: 內嵌 CSS，支援深色主題

## 開發工作流程

### 新增內容頁面
1. 在 `src/i18n/zh.ts` 和 `src/i18n/en.ts` 中新增翻譯
2. 更新 `src/i18n/types.ts` 中的類型定義
3. 在 `functions/[[_path]].ts` 中新增路由處理
4. 測試多語言功能

### 更新隱私政策
1. 編輯 `content/privacy-policy.md`（繁中）
2. 編輯 `content/privacy-policy.en.md`（英文）
3. 執行 `npm run sync:privacy` 生成 `src/content/privacy.zh.ts`、`src/content/privacy.en.ts`
4. 測試隱私政策頁面

注意：`src/content/privacy.zh.ts` 與 `src/content/privacy.en.ts` 為自動生成且被程式直接匯入的執行時檔案，請勿直接修改；請以 `content/` 下的 Markdown 作為唯一來源。

### 新增靜態資源
1. 將檔案放入 `assets/` 目錄
2. 在 HTML 中使用 `/assets/filename` 路徑
3. 考慮從 `shared/` 目錄同步共用資源

## 效能優化

### Cloudflare Pages 優勢
- **全球 CDN**: 自動邊緣快取和分發
- **零冷啟動**: Cloudflare Workers 運行時
- **自動壓縮**: Gzip/Brotli 壓縮
- **HTTP/2 支援**: 現代協議支援

### 程式碼優化
- **最小化依賴**: 僅使用必要的 npm 套件
- **TypeScript**: 編譯時類型檢查和優化
- **內嵌樣式**: 減少 HTTP 請求
- **智慧快取**: Cookie 和 URL 參數管理

## 故障排除

### 常見問題

#### 1. 開發伺服器無法啟動
```bash
# 檢查 Node.js 版本
node --version  # 需要 18+

# 清除快取重新安裝
rm -rf node_modules package-lock.json
npm install
```

#### 2. 語言切換不生效
- 檢查 URL 參數格式: `?lang=zh` 或 `?lang=en`
- 清除瀏覽器 Cookie
- 檢查 `src/i18n/` 檔案是否正確

#### 3. 隱私政策內容未更新
```bash
# 手動同步內容
npm run sync:privacy

# 檢查生成的檔案
ls src/content/privacy.*.ts
```

#### 4. 部署失敗
- 確認 Cloudflare 帳戶設定
- 檢查 `wrangler.jsonc` 配置
- 確認專案名稱唯一性

## 貢獻指南

### 開發流程
1. Fork 專案倉庫
2. 建立功能分支: `git checkout -b feature/new-feature`
3. 進行開發和測試
4. 確保類型檢查通過: `npm run typecheck`
5. 提交 Pull Request

### 程式碼規範
- 使用 TypeScript 進行開發
- 遵循現有的程式碼風格
- 新增功能需包含多語言支援
- 更新相關文檔

### 測試要求
- 本地測試: `npm run dev`
- 類型檢查: `npm run typecheck`
- 多語言測試: 測試 `?lang=zh` 和 `?lang=en`
- 響應式測試: 測試不同螢幕尺寸

## 授權資訊

MIT License - 詳見 [LICENSE](../LICENSE) 檔案。

---

## 總結

LinkEveryWord Web 平台是一個功能完整的現代化 Web 應用程式，提供：
- 完整的多語言支援系統
- 自動化的內容管理流程
- 高效能的全球部署
- 優雅的使用者體驗

平台已準備好用於生產環境，並具備良好的擴展性和維護性。
