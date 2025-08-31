# Gemini 專案：LinkEveryWord

## 專案概觀

本專案「LinkEveryWord」是一個全面的檔案搜尋和連結管理解決方案。它包含三個主要元件：

1.  **桌面應用程式：** 一個功能強大的本機檔案搜尋桌面應用程式，使用 Python、Flask 和 Everything SDK 建置。這是目前唯一可運作的元件。
2.  **Web 應用程式：** 一個規劃中的雲端版本，用於檔案搜尋和管理。
3.  **Chrome 擴充功能：** 一個規劃中的瀏覽器擴充功能，用於快速搜尋和連結檔案。

本專案目前的主要重點是桌面應用程式。

## 桌面應用程式詳細資料

### 架構

桌面應用程式是一個主從式架構的應用程式：

*   **後端：** 一個用 Python 編寫的 Flask 伺服器，提供用於搜尋檔案的 RESTful API。它使用 Everything SDK 進行快速的索引搜尋。如果 Everything SDK 無法使用，它會備援使用 Windows 搜尋或示範模式。
*   **前端：** 一個網頁版使用者介面，與 Flask 伺服器通訊以顯示搜尋結果。前端是使用 HTML、CSS 和 JavaScript 建置的。

### 主要檔案

*   `desktop-app/app_standalone.py`：Flask 應用程式的主要進入點。它處理伺服器設定、API 端點以及與搜尋後端的通訊。
*   `desktop-app/config.yml`：應用程式的設定檔，允許使用者自訂伺服器設定、日誌記錄和應用程式行為。
*   `desktop-app/CONFIG.md`：`config.yml` 中可用設定選項的文件。
*   `desktop-app/utils/everything_sdk.py`：Everything SDK 的 Python 包裝器，是主要的搜尋後端。
*   `desktop-app/templates/index.html`：網頁版使用者介面的主要 HTML 檔案。
*   `desktop-app/build.bat`：一個批次腳本，用於使用 PyInstaller 將應用程式建置為獨立的可執行檔。
*   `desktop-app/run_with_dependencies.bat`：一個批次腳本，用於在開發環境中執行應用程式。

## 建置和執行桌面應用程式

### 在開發模式中執行

若要在開發環境中執行桌面應用程式，您可以使用提供的批次腳本：

```bash
cd desktop-app
run_with_dependencies.bat
```

此腳本將安裝必要的相依性並啟動 Flask 伺服器。然後，您可以透過開啟網頁瀏覽器並導覽至 `http://127.0.0.1:5000` 來存取應用程式。

或者，您可以手動安裝相依性並執行應用程式：

```bash
cd desktop-app
pip install flask flask-cors pywin32
python app_standalone.py
```

### 建置可執行檔

若要建置桌面應用程式的獨立可執行檔，您可以使用提供的批次腳本：

```bash
cd desktop-app
build.bat
```

此腳本將使用 PyInstaller 在 `dist` 目錄中建立一個單一的可執行檔。

## 開發慣例

*   **設定：** 應用程式使用 `config.yml` 檔案進行設定。提供了預設值，並且該檔案在 `CONFIG.md` 中有詳細的文件說明。
*   **日誌記錄：** 應用程式具有一個全面的日誌記錄系統，可以在 `config.yml` 中進行設定。日誌會寫入主控台和檔案。
*   **模組化：** 搜尋後端（Everything SDK、Windows 搜尋、示範模式）在 `utils` 目錄中實作為獨立的模組，以便於擴充或修改。
*   **錯誤處理：** 應用程式包含針對 Everything SDK 無法使用情況的錯誤處理，並且會正常地備援至替代的搜尋方法。

## 持續運行的開發伺服器測試

為了模擬真實使用情況並測試需要持續運行的伺服器，請遵循以下步驟：

1.  **啟動背景服務**：在專案根目錄下，使用以下指令在背景啟動伺服器。這將允許您繼續在終端中執行其他指令。

    ```bash
    cd desktop-app && start /b python app_standalone.py
    ```

2.  **檢查服務狀態**：伺服器啟動後，可以透過瀏覽器或工具（如 `curl` 或 `web_fetch`）訪問狀態端點，以確認其是否正常運行。

    ```
    http://127.0.0.1:5000/status
    ```

3.  **查看日誌檔案**：由於服務在背景運行，輸出不會直接顯示在主控台。您可以查看 `desktop-app/app.log` 檔案來獲取詳細的執行日誌。

4.  **停止服務**：測試完成後，您需要手動停止背景程序。您可以使用任務管理器，或透過在啟動服務時獲得的程序 ID (PID) 來停止它。
