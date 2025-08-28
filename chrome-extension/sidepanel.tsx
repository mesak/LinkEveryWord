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
  // 內部解析後的參數物件
  const parseQueryParams = (text: string) => {
    try {
      const obj = JSON.parse(text)
      return obj
    } catch (err) {
      return null
    }
  }

  // 檢查物件內是否包含 '{{QUERY}}' 字串（遞迴）
  const containsPlaceholder = (obj: any): boolean => {
    if (obj == null) return false
    if (typeof obj === "string") return obj.includes("{{QUERY}}")
    if (typeof obj === "number" || typeof obj === "boolean") return false
    if (Array.isArray(obj)) return obj.some((v) => containsPlaceholder(v))
    if (typeof obj === "object") return Object.values(obj).some((v) => containsPlaceholder(v))
    return false
  }

  // 對參數物件做占位符取代（遞迴）
  const replacePlaceholder = (obj: any, value: string): any => {
    if (obj == null) return obj
    if (typeof obj === "string") return obj.replace(/\{\{QUERY\}\}/g, value)
    if (typeof obj === "number" || typeof obj === "boolean") return obj
    if (Array.isArray(obj)) return obj.map((v) => replacePlaceholder(v, value))
    if (typeof obj === "object") {
      const out: any = {}
      for (const [k, v] of Object.entries(obj)) {
        out[k] = replacePlaceholder(v, value)
      }
      return out
    }
    return obj
  }

  // 搜索功能
  const handleSearch = async (textToSearch: string) => {
    if (!textToSearch.trim()) return

    setIsLoading(true)
    setSearchResults([]) // 開始新搜尋前清空舊結果
    try {
      // 從儲存中獲取最新設定
      const settings = await chrome.storage.sync.get({
        backendUrl: "http://127.0.0.1:5000/search", // 提供預設值
        queryKey: "query",
        queryParams: JSON.stringify({ max_results: 50, query: "xxxx" })
      })
      const { backendUrl, queryKey } = settings
      // 讀取並解析 query params
      const rawParams = settings.queryParams || JSON.stringify({ max_results: 50, query: "xxxx" })
      let params = parseQueryParams(rawParams) || { max_results: 50, query: "xxxx" }

      // 如果使用者在 params 中放了 '{{QUERY}}'，則以該位置做替換；否則嘗試寫入 params.query
      const hasPlaceholder = containsPlaceholder(params)
      if (hasPlaceholder) {
        params = replacePlaceholder(params, textToSearch)
      } else {
        params.query = textToSearch
      }


      const response = await fetch(backendUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params)
      })

      const data = await response.json()
      setSearchResults(data.results || [])
    } catch (error) {
      console.error("Search error:", error)
      setSearchResults([])
    } finally {
      setIsLoading(false)
    }
  }

  // (Query params are configured in Options as key/value pairs)

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
    <div className="w-full h-full bg-background flex flex-col overflow-hidden">
      <div className="flex-1 p-2 overflow-y-auto">
        <Card className="w-full h-full shadow-none border-0">
          <CardHeader className="pb-1">
            <CardTitle className="text-lg">LinkEveryWord</CardTitle>
            <CardDescription className="text-sm">快速文字搜尋工具</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {/* 選中的文字 */}
            <div>
              <Label htmlFor="selected-text" className="text-sm">選取的文字</Label>
              <Input
                id="selected-text"
                value={selectedText}
                onChange={(e) => setSelectedText((e.target as HTMLInputElement).value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleSearch(selectedText)
                  }
                }}
                placeholder="請在網頁上選取文字或在此輸入"
                className="text-sm py-1"
              />
            </div>

            {/* 手動搜尋按鈕 */}
            <Button
              onClick={() => handleSearch(selectedText)}
              disabled={!selectedText.trim() || isLoading}
              className="w-full text-sm py-1"
            >
              {isLoading ? "搜尋中..." : "重新搜尋"}
            </Button>

            {/* 查詢參數請在 Options 中以 key/value 配置 */}

            {/* 搜尋結果 */}
            {isLoading && <div className="text-center py-4">搜尋中...</div>}
            {!isLoading && searchResults.length > 0 && (
              <div className="space-y-2">
                <Label className="text-sm">搜尋結果</Label>
                <div className="overflow-y-auto space-y-1">
                  {searchResults.map((result: any, index: number) => (
                    <div key={index} className="p-2 border rounded bg-white">
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex-1 min-w-0">
                          <div className="font-medium text-sm truncate">{result.title || result.filename}</div>
                          <div className="text-xs text-muted-foreground truncate">{result.description || result.path}</div>
                        </div>
                        <div className="text-xs text-muted-foreground ml-2">{result.size_formatted || ''}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default SidePanel
