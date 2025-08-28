// 監聽來自content script的消息
chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.action === "openSidePanel") {
    try {
      // 打開side panel
      await chrome.sidePanel.open({ windowId: sender.tab?.windowId })

      // 將選中的文字傳遞給side panel
      setTimeout(() => {
        chrome.runtime.sendMessage({
          action: "setSelectedText",
          selectedText: message.selectedText
        })
      }, 100)
    } catch (error) {
      console.error("Error opening side panel:", error)
    }
  } else if (message.action === "setSelectedText") {
    // 直接將文字轉發給side panel
    chrome.runtime.sendMessage({
      action: "setSelectedText",
      selectedText: message.selectedText
    })
  }
})

// 處理side panel的設置
chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true })
