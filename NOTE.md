這邊紀錄一些簡單測試、與排除的指令。

```
Remove-Item test_auto_config.py, test_complete_config.py, test_config.py -ErrorAction SilentlyContinue
```


```
taskkill /f /im python.exe 2>$null; Start-Sleep 2   
```