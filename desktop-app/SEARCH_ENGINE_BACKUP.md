# LinkEveryWord Desktop App - 搜索引擎备用方案

## 概述

这个应用程序现在支持多种搜索引擎，当主要的 Everything 搜索引擎不可用时，会自动回退到备用搜索方案。

## 搜索引擎优先级

应用程序按以下优先级尝试搜索引擎：

1. **Everything SDK** (最优选择)
   - 使用 voidtools Everything 的 DLL 接口
   - 提供最快和最全面的搜索功能
   - 需要 Everything 程序已安装并运行

2. **Windows Search API** (第一备用)
   - 使用 Windows 内置的 Windows Search Service
   - 通过 COM 接口访问系统索引
   - 需要 pywin32 模块

3. **简化 Windows Search** (第二备用)
   - 使用 PowerShell 命令进行文件搜索
   - 不需要额外的 Python 模块
   - 搜索范围限制在常用目录

4. **演示模式** (最后备用)
   - 提供模拟数据用于演示
   - 当所有其他搜索引擎都不可用时使用

## 新增文件

### 核心搜索引擎模块

1. **windows_search_api.py**
   - 完整的 Windows Search API 实现
   - 使用 pywin32 和 COM 接口
   - 支持高级搜索功能

2. **simple_windows_search.py**
   - 简化的 Windows 搜索实现
   - 使用 subprocess 调用 PowerShell
   - 无需额外依赖

### 辅助文件

3. **check_pywin32.py**
   - 检查 pywin32 模块是否可用

4. **test_search_engines.py**
   - 测试不同搜索引擎的功能
   - 验证自动切换逻辑

5. **run_with_dependencies.bat**
   - 自动安装依赖并启动应用程序

## 主要改进

### app_standalone.py 的更新

1. **多搜索引擎支持**
   ```python
   # 尝试载入 Everything SDK
   try:
       everything_sdk_instance = get_everything_sdk()
       EVERYTHING_AVAILABLE = True
   except Exception:
       # 尝试 Windows Search API
       try:
           windows_search_instance = get_windows_search_api()
           WINDOWS_SEARCH_MODE = True
       except Exception:
           # 尝试简化搜索
           try:
               simple_windows_search_instance = get_simple_windows_search()
               SIMPLE_SEARCH_MODE = True
           except Exception:
               # 最后使用演示模式
               DEMO_MODE = True
   ```

2. **动态搜索路由**
   ```python
   # 根据可用的搜索引擎执行搜索
   if DEMO_MODE:
       results, total_count = mock_sdk_instance.search(query, max_results)
   elif WINDOWS_SEARCH_MODE:
       results, total_count = windows_search_instance.search(query, max_results)
   elif SIMPLE_SEARCH_MODE:
       results, total_count = simple_windows_search_instance.search(query, max_results)
   else:
       results, total_count = everything_sdk_instance.search(query, max_results)
   ```

3. **状态报告端点**
   ```python
   @app.route('/status')
   def app_status():
       return jsonify({
           'everything_available': EVERYTHING_AVAILABLE,
           'demo_mode': DEMO_MODE,
           'windows_search_mode': WINDOWS_SEARCH_MODE,
           'simple_search_mode': SIMPLE_SEARCH_MODE,
           'search_engine': current_engine_name
       })
   ```

### 前端界面更新

1. **智能状态显示**
   - 根据当前使用的搜索引擎显示不同状态
   - 在搜索结果中标明搜索引擎类型

2. **用户友好的反馈**
   - 清楚显示当前使用的搜索模式
   - 提供适当的警告和建议

## 使用方法

### 自动模式（推荐）

```bash
# 运行带依赖检查的启动脚本
run_with_dependencies.bat
```

这个脚本会：
1. 检查 Python 环境
2. 尝试安装 pywin32（如果需要）
3. 启动应用程序

### 手动模式

```bash
# 直接启动应用程序
python app_standalone.py
```

应用程序会自动检测可用的搜索引擎并选择最佳选项。

## 故障排除

### Everything 不可用时

当看到以下消息时：
```
⚠ Everything SDK 載入失敗: [错误信息]
✓ 使用 Windows Search API 作為備用搜尋引擎
```

这表示应用程序已成功切换到备用搜索引擎。

### 所有高级搜索引擎都不可用时

```
⚠ Windows Search API 也無法使用: [错误信息]
✓ 使用簡化 Windows Search 作為備用搜尋引擎
```

这时使用的是基于 PowerShell 的简化搜索。

### 完全备用模式

```
以示範模式運行 - 僅顯示模擬結果
```

当所有搜索引擎都不可用时，应用程序将显示演示数据。

## 性能对比

| 搜索引擎 | 速度 | 覆盖范围 | 依赖 |
|---------|------|----------|------|
| Everything | 极快 | 全盘 | Everything 程序 |
| Windows Search API | 快 | 已索引文件 | pywin32 |
| 简化搜索 | 中等 | 常用目录 | 无 |
| 演示模式 | 即时 | 模拟数据 | 无 |

## 技术细节

### 搜索引擎接口统一

所有搜索引擎都实现相同的接口：

```python
def search(self, query: str, max_results: int = 100) -> Tuple[List[EverythingSearchResult], int]:
    """
    执行搜索
    
    Returns:
        (results, total_count): 搜索结果列表和总结果数
    """
```

### 错误处理

- 每个搜索引擎都有独立的错误处理
- 失败时自动切换到下一个可用引擎
- 用户界面显示清晰的状态信息

### 配置管理

- 无需额外配置文件
- 自动检测和适配环境
- 优雅降级到可用功能

## 开发者指南

### 添加新的搜索引擎

1. 创建新的搜索引擎类，实现标准接口
2. 在 `app_standalone.py` 中添加检测逻辑
3. 更新前端状态显示

### 测试

```bash
# 运行搜索引擎测试
python test_search_engines.py
```

这个脚本会测试所有可用的搜索引擎并报告结果。

## 未来改进

1. **配置文件支持**
   - 允许用户自定义搜索路径
   - 配置搜索引擎优先级

2. **更多搜索引擎**
   - 支持其他第三方搜索工具
   - 网络搜索集成

3. **性能优化**
   - 缓存搜索结果
   - 异步搜索支持

4. **用户界面改进**
   - 搜索引擎切换按钮
   - 高级搜索选项
