import React, { useState, useEffect } from "react"
import "./style.css"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card"
import { Button } from "./components/ui/button"
import { Input } from "./components/ui/input"
import { Label } from "./components/ui/label"
import { Github, Earth } from 'lucide-react';

function Options() {
  const [backendUrl, setBackendUrl] = useState("http://127.0.0.1:5000/search")
  const [queryKey, setQueryKey] = useState("q")
  const [queryParamsText, setQueryParamsText] = useState(JSON.stringify({ max_results: 50, query: "{{QUERY}}" }, null, 2))
  const [kvEntries, setKvEntries] = React.useState<Array<{ key: string; value: string }>>([])
  const [newKey, setNewKey] = useState("")
  const [newValue, setNewValue] = useState("")

  // 載入設定
  useEffect(() => {
    chrome.storage.sync.get(["backendUrl", "queryKey", "queryParams"], (result) => {
      if (result.backendUrl) setBackendUrl(result.backendUrl)
      if (result.queryKey) setQueryKey(result.queryKey)
      if (result.queryParams) {
        setQueryParamsText(result.queryParams)
        try {
          const obj = JSON.parse(result.queryParams)
          const entries = Object.keys(obj).map((k) => ({ key: k, value: typeof obj[k] === 'string' ? obj[k] : JSON.stringify(obj[k]) }))
          setKvEntries(entries)
        } catch (e) {
          // ignore parse errors
        }
      } else {
        // default
        const def = JSON.stringify({ max_results: 50, query: "{{QUERY}}" }, null, 2)
        setQueryParamsText(def)
        setKvEntries([{ key: 'max_results', value: '50' }, { key: 'query', value: '{{QUERY}}' }])
      }
    })
  }, [])

  // 保存設定
  const saveSettings = () => {
    // 驗證 queryParamsText 必須是合法 JSON 且含有 {{QUERY}} 字串
    try {
      // build object from kvEntries (entries with JSON values are parsed where possible)
      const obj: any = {}
      kvEntries.forEach((e) => {
        // try parse e.value as JSON, otherwise keep as string
        try {
          obj[e.key] = JSON.parse(e.value)
        } catch (err) {
          obj[e.key] = e.value
        }
      })
      const parsed = obj
      const containsQuery = JSON.stringify(parsed).includes("{{QUERY}}")
      if (!containsQuery) {
        const status = document.getElementById("status")
        if (status) {
          status.textContent = chrome.i18n.getMessage("queryMustContainPlaceholder")
          status.style.color = "red"
          setTimeout(() => (status.textContent = ""), 3000)
        }
        return
      }

      chrome.storage.sync.set({
        backendUrl,
        queryKey,
        queryParams: JSON.stringify(parsed)
      }, () => {
        const status = document.getElementById("status")
        if (status) {
          status.textContent = chrome.i18n.getMessage("settingsSaved")
          status.style.color = "green"
          setTimeout(() => {
            status.textContent = ""
          }, 2000)
        }
      })
    } catch (err) {
      const status = document.getElementById("status")
      if (status) {
        status.textContent = chrome.i18n.getMessage("invalidJson")
        status.style.color = "red"
        setTimeout(() => (status.textContent = ""), 3000)
      }
    }
  }

  const addEntry = () => {
    if (!newKey.trim()) return
    setKvEntries([...kvEntries, { key: newKey.trim(), value: newValue }])
    setNewKey("")
    setNewValue("")
  }

  const removeEntry = (index: number) => {
    const copy = [...kvEntries]
    copy.splice(index, 1)
    setKvEntries(copy)
  }

  const updateEntry = (index: number, field: 'key' | 'value', value: string) => {
    const copy = [...kvEntries]
    copy[index] = { ...copy[index], [field]: value }
    setKvEntries(copy)
  }

  // 移除自定義快速鍵錄製功能

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold">{chrome.i18n.getMessage("settingsTitle")}</h1>
          <p className="text-muted-foreground mt-2">
            {chrome.i18n.getMessage("settingsDescription")}
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>{chrome.i18n.getMessage("searchSettings")}</CardTitle>
            <CardDescription>
              {chrome.i18n.getMessage("searchSettingsDescription")}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="backend-url">{chrome.i18n.getMessage("backendUrlLabel")}</Label>
              <Input
                id="backend-url"
                value={backendUrl}
                onChange={(e) => setBackendUrl(e.target.value)}
                placeholder="http://127.0.0.1:5000/search"
              />
              <p className="text-sm text-muted-foreground mt-1">
                {chrome.i18n.getMessage("backendUrlDescription")}
              </p>
            </div>

            <div>
              <Label>{chrome.i18n.getMessage("queryParamsLabel")}</Label>
              <p className="text-sm text-muted-foreground mt-1">{chrome.i18n.getMessage("queryParamsDescription")}</p>
              <div className="space-y-2 mt-2">
                {kvEntries.map((entry, idx) => (
                  <div key={idx} className="flex gap-2">
                    <Input value={entry.key} onChange={(e) => updateEntry(idx, 'key', e.target.value)} placeholder="key" />
                    <Input value={entry.value} onChange={(e) => updateEntry(idx, 'value', e.target.value)} placeholder="value (string or JSON)" />
                    <Button variant="destructive" onClick={() => removeEntry(idx)}>{chrome.i18n.getMessage("delete")}</Button>
                  </div>
                ))}

                <div className="flex gap-2">
                  <Input value={newKey} onChange={(e) => setNewKey(e.target.value)} placeholder="new key" />
                  <Input value={newValue} onChange={(e) => setNewValue(e.target.value)} placeholder="new value" />
                  <Button onClick={addEntry}>{chrome.i18n.getMessage("add")}</Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{chrome.i18n.getMessage("shortcutSettings")}</CardTitle>
            <CardDescription>
              {chrome.i18n.getMessage("shortcutSettingsDescription")}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-muted-foreground">
                {chrome.i18n.getMessage("shortcutDescription")}
              </p>
              <div className="flex justify-center mt-4">
                <Button
                  variant="outline"
                  onClick={() => {
                    try {
                      chrome.tabs.create({ url: "chrome://extensions/shortcuts" })
                    } catch (err) {
                      // 某些環境可能不允許直接開啟 chrome:// 頁面
                      console.error("Failed to open shortcuts page:", err)
                    }
                  }}
                >
                  {chrome.i18n.getMessage("openShortcutsPage")}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-center">
          <Button onClick={saveSettings} size="lg">
            {chrome.i18n.getMessage("saveSettings")}
          </Button>
        </div>
        <div id="status" className="text-center text-sm"></div>


        <div className="w-full flex flex-col md:flex-row items-center justify-center gap-3 py-2 text-xs text-muted-foreground border-t border-border/30">
          <div className="flex items-center space-x-1">
            <Github className="h-4 w-4" />
            <a
              href="https://github.com/mesak/LinkEveryWord"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline"
            >
              mesak/LinkEveryWord
            </a>
          </div>
          
          <div className="flex items-center space-x-1">
            <Earth className="h-3 w-3" />
            <span><a
              href="https://mesak.tw"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline"
            >Mesak</a></span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Options
