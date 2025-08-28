﻿# LinkEveryWord

<p align="center"><img src="image.png" width="100%"></p>

 **LinkEveryWord** 是一個全面的檔案搜尋和連結管理解決方案，讓您可以快速找到並連結任何檔案。

##  專案架構

本專案包含三個主要元件：

###  Desktop App (電腦版應用程式)
**位置**: /desktop-app/  
**技術**: Python + Flask + Everything SDK  
**描述**: 基於 voidtools Everything 搜尋引擎的桌面應用程式，提供強大的本地檔案搜尋功能。

**主要功能**:
-  即時檔案搜尋
-  Web 介面操作
-  獨立執行檔 (15MB)
-  示範模式支援
-  中文介面

###  Web App (網站版)
**位置**: /web-app/  
**技術**: 待規劃  
**描述**: 雲端版本的檔案搜尋和管理平台。

**規劃功能**:
-  雲端檔案索引
-  多用戶支援
-  跨平台同步
-  響應式設計

###  Chrome Extension (瀏覽器套件)
**位置**: /chrome-extension/  
**技術**: 待規劃  
**描述**: Chrome 瀏覽器套件，讓您在瀏覽時快速搜尋和連結檔案。

**規劃功能**:
-  快速檔案連結
-  網頁內容整理
-  快捷鍵操作
-  右鍵選單搜尋

##  快速開始

### Desktop App
`ash
cd desktop-app
python app_standalone.py
# 或直接執行
dist/EverythingFlaskSearch.exe
`

### Web App
`ash
# 待開發
cd web-app
`

### Chrome Extension
`ash
# 待開發
cd chrome-extension
`

##  目錄結構

`
LinkEveryWord/
  README.md                    # 主專案說明
  desktop-app/                # 電腦版應用程式
    app_standalone.py          # 主程式
    everything_sdk.py          # Everything SDK
    dist/EverythingFlaskSearch.exe  # 執行檔
    README.md                  # 桌面版說明
  web-app/                    # 網站版
    README.md                  # 網站版說明 (待開發)
  chrome-extension/           # Chrome 套件
     README.md                  # Chrome 套件說明 (待開發)
`

##  開發狀態

| 元件 | 狀態 | 進度 | 說明 |
|------|------|------|------|
|  Desktop App |  完成 | 100% | 功能完整，已打包 |
|  Web App |  規劃中 | 0% | 待開發 |
|  Chrome Extension |  規劃中 | 0% | 待開發 |

##  技術文件
- [Desktop App 使用指南](desktop-app/README.md)

##  貢獻指南

1. Fork 專案
2. 創建功能分支 (git checkout -b feature/AmazingFeature)
3. 提交變更 (git commit -m 'Add some AmazingFeature')
4. 推送到分支 (git push origin feature/AmazingFeature)
5. 開啟 Pull Request

##  授權

本專案採用 MIT 授權條款 - 查看 [LICENSE](LICENSE) 檔案了解詳情。

##  專案願景

LinkEveryWord 致力於打造最直觀、最高效的檔案搜尋和連結管理體驗，讓每個人都能輕鬆找到並組織自己的數位資產。

---

**開發者**: 專注於提供最佳的檔案搜尋體驗 
