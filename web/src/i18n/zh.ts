import type { Dict } from './types'

export const zh: Dict = {
  common: {
    brand: 'LinkEveryWord',
  nav: { home: '首頁', chrome: 'Chrome 安裝', desktop: 'Desktop 安裝', privacy: '隱私政策', github: 'GitHub', lang: '語言', donate: '請我喝咖啡' },
  },
  home: {
    title: '讓連結無所不在',
    intro: 'LinkEveryWord 提供兩個組件：Chrome 擴充功能與 Windows 桌面應用程式，協助你快速查找與連結需要的資訊。',
    quickStart: '快速開始',
    items: {
      chrome: '安裝 Chrome 擴充功能（側邊面板、選字搜尋、快捷鍵）',
      desktop: '安裝 Desktop App（Everything 本地檔案搜尋 + Web 介面）',
    },
  },
  chrome: {
    title: 'Chrome 擴充功能安裝教學',
    installFromStore: '從 Chrome 線上應用程式商店安裝',
    steps: [
      '點擊下方的「從 Chrome 線上應用程式商店安裝」按鈕。',
      '在彈出的 Chrome 商店頁面中，點擊「加到 Chrome」。',
      '安裝完成後，建議將擴充功能釘選到工具列以便快速存取。'
    ],
    usageTitle: '基本使用',
    usageItems: [
      '選取網頁文字，按下預設快捷鍵 Ctrl+Shift+F（可自訂）。',
      '側邊面板會顯示由你設定後端所回傳的結果。',
      '前往「擴充圖示 → 設定」可自訂：後端 API、查詢鍵、快捷鍵。',
    ],
    privacyNote: '我們尊重你的隱私。完整政策見 隱私權政策。',
    detailsNote: '詳細說明請見 repo 中 chrome-extension/README.md。',
  },
  desktop: {
    title: 'Desktop App 安裝教學',
    method1: ['方法一：直接執行（建議）', '下載發行版壓縮檔（若有提供）並解壓。', '直接執行 dist/EverythingFlaskSearch.exe。'],
    method2: [
      '方法二：開發模式啟動',
      '安裝 Python 3.13+。',
      '進入 desktop-app 目錄，安裝相依：pip install flask flask-cors。',
      '啟動：python app_standalone.py。',
    ],
    reqTitle: '系統需求',
    reqList: ['Windows 10/11', '建議安裝 Everything（非必須，亦可使用示範模式）'],
    more: '更多細節與疑難排解，請參閱 repo 中 desktop-app/README.md。',
  },
  privacy: {
    title: '隱私權政策',
  },
}

export default zh
