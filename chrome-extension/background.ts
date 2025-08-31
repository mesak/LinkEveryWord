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

// 處理 manifest.commands 發出的快捷鍵事件
chrome.commands.onCommand.addListener?.((command) => {
  try {
    if (command === "open-search-panel") {
      // 立即先開啟側邊面板（在用戶手勢的直接回應中）
      chrome.windows.getCurrent(undefined, (win) => {
        const windowId = win?.id;
        chrome.sidePanel.open({ windowId }).then(() => {
          // 側邊面板成功開啟後，獲取選中的文字
          chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
            if (tabs[0]?.id) {
              try {
                // 嘗試執行腳本以獲取選中的文字
                const results = await chrome.scripting.executeScript({
                  target: { tabId: tabs[0].id },
                  func: () => window.getSelection()?.toString().trim() || ""
                });
                
                const selectedText = results?.[0]?.result || "";
                
                // 如果有選中的文字，傳遞給側邊面板
                if (selectedText) {
                  setTimeout(() => {
                    chrome.runtime.sendMessage({
                      action: "setSelectedText",
                      selectedText: selectedText
                    });
                  }, 300); // 給側邊面板更多時間載入
                }
              } catch (scriptError) {
                console.error("Error executing script:", scriptError);
              }
            }
          });
        }).catch((err) => console.error("Failed to open side panel:", err));
      });
    }
  } catch (error) {
    console.error("Error handling command:", error);
  }
});
// 處理side panel的設置
chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true })
