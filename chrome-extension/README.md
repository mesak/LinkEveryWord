# LinkEveryWord Chrome Extension

一個強大的Chrome擴展，讓您能夠快速搜尋網頁中選取的文字。

## 功能特色

- **快速文字搜尋**：在任何網頁上選取文字，按下快速鍵即可搜尋
- **側邊面板**：美觀的側邊面板顯示搜尋結果
- **自訂設定**：設定後端API和搜尋參數
- **靈活快速鍵**：可自訂觸發搜尋的快速鍵組合

## 安裝方式

1. 複製此專案
2. 運行 `npm install` 安裝依賴
3. 運行 `npm run dev` 啟動開發模式
4. 在Chrome中載入 `build/chrome-mv3-dev` 目錄作為未打包擴展

## 使用方法

### 基本使用
1. 在任何網頁上選取文字
2. 按下預設快速鍵 `Ctrl+Shift+F` (或自訂快速鍵)
3. 側邊面板將自動打開並顯示搜尋結果

### 設定
1. 點擊擴展圖示 > 設定
2. 設定您的後端API網址 (例如: `http://127.0.0.1:5000/search`)
3. 設定查詢參數鍵 (預設: `q`)
4. 設定快速鍵組合

## 技術架構

- **框架**：React + TypeScript
- **UI框架**：shadcn/ui + Tailwind CSS
- **建構工具**：Plasmo
- **Manifest**：Chrome Extension Manifest V3

## 開發

```bash
# 安裝依賴
npm install

# 開發模式
npm run dev

# 建構生產版本
npm run build

# 打包
npm run package
```

## 檔案結構

```
chrome-extension-app/
├── assets/                 # 靜態資源
├── components/            # React組件
│   └── ui/               # shadcn/ui組件
├── contents/             # Content scripts
├── background.ts         # Background script
├── popup.tsx            # 擴展彈出視窗
├── sidepanel.tsx        # 側邊面板
├── options.tsx          # 設定頁面
└── package.json         # 專案配置
```

## API格式

後端API應接受GET請求，格式如下：

```
GET {backendUrl}?{queryKey}={selectedText}
```

回應格式：
```json
{
  "results": [
    {
      "title": "搜尋結果標題",
      "description": "搜尋結果描述",
      "url": "選用的結果連結"
    }
  ]
}
```

## 授權

MIT License

## 開發者

Mesak
