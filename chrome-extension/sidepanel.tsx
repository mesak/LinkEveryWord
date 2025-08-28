import React, { useState, useEffect } from "react"
import "./style.css"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card"
import { Button } from "./components/ui/button"
import { Input } from "./components/ui/input"
import { Label } from "./components/ui/label"

function SidePanel() {
  const [selectedText, setSelectedText] = useState("")
  const [searchResults, setSearchResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  // 搜索功能
  const handleSearch = async (textToSearch: string) => {
    if (!textToSearch.trim()) return

    setIsLoading(true)
    setSearchResults([]) // 開始新搜尋前清空舊結果
    try {
      // 從儲存中獲取最新設定
      const settings = await chrome.storage.sync.get({
        backendUrl: "http://127.0.0.1:5000", // 提供預設值
        queryKey: "q"
      })

      const { backendUrl, queryKey } = settings
      const searchUrl = `${backendUrl}?${queryKey}=${encodeURIComponent(textToSearch)}`
      const response = await fetch(searchUrl)
      const data = await response.json()
      setSearchResults(data.results || [])
    } catch (error) {
      console.error("Search error:", error)
      setSearchResults([])
    } finally {
      setIsLoading(false)
    }
  }

  // 監聽來自 background script 的消息
  useEffect(() => {
    const handleMessage = (message: any) => {
      if (message.action === "setSelectedText" && message.selectedText) {
        setSelectedText(message.selectedText)
      }
    }

    chrome.runtime.onMessage.addListener(handleMessage)

    return () => {
      chrome.runtime.onMessage.removeListener(handleMessage)
    }
  }, [])

  // 當 selectedText 變化時，自動觸發搜尋
  useEffect(() => {
    if (selectedText) {
      handleSearch(selectedText)
    }
  }, [selectedText])

  return (
    <div className="w-80 h-full bg-background p-4 space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>LinkEveryWord</CardTitle>
          <CardDescription>快速文字搜尋工具</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* 選中的文字 */}
          <div>
            <Label htmlFor="selected-text">選取的文字</Label>
            <Input
              id="selected-text"
              value={selectedText}
              readOnly
              placeholder="請在網頁上選取文字"
            />
          </div>

          {/* 手動搜尋按鈕 */}
          <Button
            onClick={() => handleSearch(selectedText)}
            disabled={!selectedText.trim() || isLoading}
            className="w-full"
          >
            {isLoading ? "搜尋中..." : "重新搜尋"}
          </Button>

          {/* 搜尋結果 */}
          {isLoading && <div className="text-center">搜尋中...</div>}
          {!isLoading && searchResults.length > 0 && (
            <div className="space-y-2">
              <Label>搜尋結果</Label>
              <div className="max-h-96 overflow-y-auto space-y-2">
                {searchResults.map((result: any, index: number) => (
                  <Card key={index} className="p-3">
                    <div className="text-sm">
                      <div className="font-medium">{result.title}</div>
                      <div className="text-muted-foreground">{result.description}</div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default SidePanel
