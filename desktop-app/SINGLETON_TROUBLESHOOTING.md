# Singleton 功能快速故障排除檢查清單

## 🚨 緊急問題快速診斷

### 問題1: "多個實例同時運行" 
```bash
# 快速檢查
python test_filelock_singleton.py
```
**預期結果**: 
- ✅ 第一個實例運行
- ✅ 第二/三個實例立即退出

**如果失敗**:
1. 檢查 filelock 是否安裝: `pip list | findstr filelock`
2. 檢查是否有 `input()` 阻塞: 搜索 `input("按 Enter` 
3. 檢查鎖文件權限: `ls -la linkeveryword.lock`

### 問題2: "測試腳本卡住不動"
**原因**: 通常是 `input()` 函數等待用戶輸入

**快速修復**:
```python
# 移除所有 input() 調用
# 將這個:
input("按 Enter 鍵退出...")
sys.exit(1)

# 改為這個:
sys.exit(1)
```

### 問題3: "鎖文件無法刪除"
```bash
# Windows
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force
Remove-Item -Path "linkeveryword.lock" -ErrorAction SilentlyContinue

# Linux/Mac
pkill python
rm -f linkeveryword.lock
```

### 問題4: "PowerShell 命令語法錯誤"
```bash
# ❌ 錯誤
cd "path" && python script.py

# ✅ 正確
cd "path"; python script.py
Set-Location "path"; python script.py
```

## 🔧 快速驗證腳本

```python
# 創建這個測試文件: quick_verify.py
import os
from filelock import FileLock

def quick_test():
    lock_file = "test.lock"
    try:
        lock1 = FileLock(lock_file)
        lock1.acquire(timeout=0.1)
        print("✅ 第一個鎖獲取成功")
        
        lock2 = FileLock(lock_file)
        lock2.acquire(timeout=0.1)
        print("❌ 第二個鎖不應該成功")
    except:
        print("✅ 第二個鎖被正確阻止")
    finally:
        try:
            lock1.release()
            os.remove(lock_file)
        except:
            pass

if __name__ == "__main__":
    quick_test()
```

## 📋 部署前檢查清單

- [ ] filelock 包已安裝
- [ ] 移除所有 input() 調用  
- [ ] 清理機制已設置 (atexit + signal)
- [ ] 測試腳本通過
- [ ] 鎖文件路徑正確
- [ ] PowerShell 命令語法正確

## 🎯 成功標準

運行測試後應該看到:
```
✅ 第一个实例正在运行（符合预期）
✅ 第二个实例已退出（符合预期）
✅ 第三个实例已退出（符合预期）
✅ 锁文件存在
✨ 测试完成!
```
