import React, { useState, useEffect } from "react"
import "./style.css"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card"
import { Button } from "./components/ui/button"
import { Input } from "./components/ui/input"
import { Label } from "./components/ui/label"

function Options() {
  const [backendUrl, setBackendUrl] = useState("http://127.0.0.1:5000")
  const [queryKey, setQueryKey] = useState("q")
  const [shortcut, setShortcut] = useState("Ctrl+Shift+L")
  const [isRecording, setIsRecording] = useState(false)

  // 載入設定
  useEffect(() => {
    chrome.storage.sync.get(["backendUrl", "queryKey", "shortcut"], (result) => {
      if (result.backendUrl) setBackendUrl(result.backendUrl)
      if (result.queryKey) setQueryKey(result.queryKey)
      if (result.shortcut) setShortcut(result.shortcut)
    })
  }, [])

  // 保存設定
  const saveSettings = () => {
    chrome.storage.sync.set({
      backendUrl,
      queryKey,
      shortcut
    }, () => {
      // 顯示保存成功訊息
      const status = document.getElementById("status")
      if (status) {
        status.textContent = "設定已保存！"
        status.style.color = "green"
        setTimeout(() => {
          status.textContent = ""
        }, 2000)
      }
    })
  }

  // 處理快速鍵錄製
  const handleShortcutRecording = (event: React.KeyboardEvent) => {
    if (!isRecording) return

    event.preventDefault()
    const keys = []

    if (event.ctrlKey || event.metaKey) keys.push("Ctrl")
    if (event.shiftKey) keys.push("Shift")
    if (event.altKey) keys.push("Alt")
    if (event.key && !["Control", "Shift", "Alt", "Meta"].includes(event.key)) {
      keys.push(event.key.toUpperCase())
    }

    if (keys.length > 1) {
      setShortcut(keys.join("+"))
      setIsRecording(false)
    }
  }

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold">LinkEveryWord 設定</h1>
          <p className="text-muted-foreground mt-2">
            設定您的搜尋偏好和快速鍵
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>搜尋設定</CardTitle>
            <CardDescription>
              設定後端API和查詢參數
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="backend-url">後端網址</Label>
              <Input
                id="backend-url"
                value={backendUrl}
                onChange={(e) => setBackendUrl(e.target.value)}
                placeholder="http://127.0.0.1:5000"
              />
              <p className="text-sm text-muted-foreground mt-1">
                您的搜尋API端點
              </p>
            </div>

            <div>
              <Label htmlFor="query-key">查詢參數鍵</Label>
              <Input
                id="query-key"
                value={queryKey}
                onChange={(e) => setQueryKey(e.target.value)}
                placeholder="q"
              />
              <p className="text-sm text-muted-foreground mt-1">
                API查詢參數的名稱（預設為q）
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>快速鍵設定</CardTitle>
            <CardDescription>
              設定觸發搜尋的快速鍵
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="shortcut">快速鍵</Label>
              <div className="flex gap-2">
                <Input
                  id="shortcut"
                  value={shortcut}
                  readOnly
                  onKeyDown={handleShortcutRecording}
                  className={isRecording ? "ring-2 ring-primary" : ""}
                  placeholder="點擊錄製按鈕設定快速鍵"
                />
                <Button
                  onClick={() => setIsRecording(!isRecording)}
                  variant={isRecording ? "destructive" : "outline"}
                >
                  {isRecording ? "停止錄製" : "錄製快速鍵"}
                </Button>
              </div>
              <p className="text-sm text-muted-foreground mt-1">
                按下錄製按鈕後，輸入您想要的快速鍵組合
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-center">
          <Button onClick={saveSettings} size="lg">
            儲存所有設定
          </Button>
        </div>

        <div id="status" className="text-center text-sm"></div>
      </div>
    </div>
  )
}

export default Options
