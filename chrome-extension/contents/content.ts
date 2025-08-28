import "../style.css"
import type { PlasmoCSConfig } from "plasmo"

export const config: PlasmoCSConfig = {
  matches: ["<all_urls>"],
  all_frames: true
}

// 預設快速鍵
let shortcutKeys = {
  ctrl: true,
  shift: true,
  key: "L"
}

// 載入用戶設定
chrome.storage.sync.get(["shortcut"], (result) => {
  if (result.shortcut) {
    const parts = result.shortcut.split("+")
    shortcutKeys = {
      ctrl: parts.includes("Ctrl"),
      shift: parts.includes("Shift"),
      key: parts[parts.length - 1]
    }
  }
})

// 監聽儲存變更，即時更新快速鍵
chrome.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === "sync" && changes.shortcut) {
    const newShortcut = changes.shortcut.newValue
    if (newShortcut) {
      const parts = newShortcut.split("+")
      shortcutKeys = {
        ctrl: parts.includes("Ctrl"),
        shift: parts.includes("Shift"),
        key: parts[parts.length - 1]
      }
    }
  }
})

// 監聽鍵盤事件
document.addEventListener("keydown", async (event) => {
  // 檢查是否按下設定的快速鍵
  const isCorrectShortcut =
    (event.ctrlKey || event.metaKey) === shortcutKeys.ctrl &&
    event.shiftKey === shortcutKeys.shift &&
    event.key.toUpperCase() === shortcutKeys.key

  if (isCorrectShortcut) {
    event.preventDefault()

    // 獲取選中的文字
    const selectedText = window.getSelection()?.toString()?.trim()

    if (selectedText) {
      // 打開side panel
      try {
        await chrome.runtime.sendMessage({
          action: "openSidePanel",
          selectedText: selectedText
        })
      } catch (error) {
        console.error("Error sending message:", error)
      }
    }
  }
})

// 監聽來自background script的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "getSelectedText") {
    const selectedText = window.getSelection()?.toString()?.trim() || ""
    sendResponse({ selectedText })
  }
})
