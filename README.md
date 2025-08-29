# LinkEveryWord

<p align="center"><img src="image.png" width="100%"></p>

**LinkEveryWord** 是一個全面的檔案搜尋與連結管理解決方案，旨在幫助您高效地尋找並管理您的數位檔案。本專案包含一個功能強大的桌面搜尋應用程式、一個無縫整合的瀏覽器擴充功能，以及一個仍在規劃中的 Web 平台。

## 專案元件

本專案由三個主要元件組成，各自擁有不同的用途：

### 🖥️ 桌面應用程式 (已完成)

**位置**: [`/desktop-app/`](./desktop-app/)
**技術**: `Python` `Flask` `Everything SDK` `PyInstaller`
**描述**: 一個功能強大的 Windows 桌面應用程式，由 Everything SDK 驅動，提供即時的本機檔案搜尋功能。它具備現代化的網頁操作介面，並可作為獨立的執行檔運行。

詳細資訊請參閱 [桌面應用程式 README](./desktop-app/README.md)。

### 🌐 Chrome 擴充功能 (已完成)

**位置**: [`/chrome-extension/`](./chrome-extension/)
**技術**: `React` `TypeScript` `shadcn/ui` `Plasmo`
**描述**: 一個 Chrome 瀏覽器擴充功能，讓您可以在任何網頁上選取文字，並使用可自訂的後端（例如 LinkEveryWord 桌面應用程式）進行即時搜尋。搜尋結果會顯示在一個簡潔的側邊面板中。

詳細資訊請參閱 [Chrome 擴充功能 README](./chrome-extension/README.md)。

### ☁️ Web 應用程式 (規劃中)

**位置**: [`/web-app/`](./web-app/)
**技術**: 待定
**描述**: 一個仍在規劃中的雲端檔案搜尋與管理平台。其願景是提供跨平台的檔案同步、團隊協作，並讓您能隨時隨地存取您的檔案。

詳細規劃文件請參閱 [Web 應用程式 README](./web-app/README.md)。

## 開發狀態

| 元件               | 狀態        | 進度 | 描述                                         |
| ------------------ | ----------- | -------- | --------------------------------------------------- |
| **桌面應用程式**   | ✅ 已完成   | 100%     | 核心功能穩定，並已提供發行版本。                   |
| **Chrome 擴充功能** | ✅ 已完成   | 100%     | 功能完備，可用於開發與建置。                       |
| **Web 應用程式**   | 📝 規劃中   | 0%       | 目前處於架構設計與規劃階段。                     |

## 快速入門

### 桌面應用程式

1.  前往 `desktop-app/dist` 目錄。
2.  執行 `EverythingFlaskSearch.exe` 執行檔。
3.  您的瀏覽器將會自動開啟並顯示搜尋介面。

若需進行開發：
```bash
# 開發模式
cd desktop-app
pip install flask flask-cors
python app_standalone.py
```

### Chrome 擴充功能

1.  前往 `chrome-extension` 目錄。
2.  安裝依賴套件: `npm install`
3.  啟動開發伺服器: `npm run dev`
4.  在 Chrome 中，從 `build/chrome-mv3-dev` 目錄載入未封裝的擴充功能。

### Web 應用程式

Web 應用程式目前尚未進入開發階段。

## 貢獻指南

1.  Fork 本專案。
2.  建立您的功能分支 (`git checkout -b feature/AmazingFeature`)。
3.  提交您的變更 (`git commit -m 'Add some AmazingFeature'`)。
4.  將分支推送到遠端 (`git push origin feature/AmazingFeature`)。
5.  開啟一個 Pull Request。

## 授權

本專案採用 MIT 授權條款 - 詳情請參閱 [LICENSE](LICENSE) 檔案。
