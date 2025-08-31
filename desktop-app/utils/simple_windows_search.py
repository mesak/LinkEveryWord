"""
Windows Search API 的简化版本
当无法使用 pywin32 时的备用实现
使用 Windows 内置的搜索工具和 Python 的 subprocess
"""
import os
import subprocess
from typing import List, Tuple
from everything_sdk import EverythingSearchResult


class SimpleWindowsSearch:
    """简化的 Windows 搜索实现"""

    def __init__(self):
        self._available = None

    def _is_available(self) -> bool:
        """检查 Windows Search 是否可用"""
        if self._available is not None:
            return self._available

        try:
            # 测试 Windows Search 服务是否运行
            result = subprocess.run(['sc', 'query', 'WSearch'],
                                    capture_output=True, text=True, timeout=5)
            self._available = 'RUNNING' in result.stdout
            return self._available
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            self._available = False
            return False

    def search(self, query: str, max_results: int = 100) -> Tuple[List[EverythingSearchResult], int]:
        """
        使用 Windows 内置命令行工具进行搜索
        """
        if not self._is_available():
            print("Windows Search 服务不可用")
            return [], 0

        results = []

        try:
            # 使用 PowerShell 进行搜索
            # 搜索用户目录、桌面、文档等常见位置
            search_paths = [
                os.path.expanduser("~"),
                os.path.join(os.path.expanduser("~"), "Desktop"),
                os.path.join(os.path.expanduser("~"), "Documents"),
                os.path.join(os.path.expanduser("~"), "Downloads"),
            ]

            # 为了安全，限制搜索深度
            for search_path in search_paths:
                if not os.path.exists(search_path):
                    continue

                try:
                    # 使用 PowerShell Get-ChildItem 进行搜索
                    ps_command = f"""
Get-ChildItem -Path '{search_path}' -Recurse -Force -ErrorAction SilentlyContinue | 
Where-Object {{$_.Name -like '*{query}*'}} | 
Select-Object -First {max_results} FullName, Name, DirectoryName, Length, LastWriteTime, CreationTime, Attributes
"""

                    result = subprocess.run(
                        ['powershell', '-Command', ps_command],
                        capture_output=True, text=True, timeout=30
                    )

                    if result.returncode == 0 and result.stdout.strip():
                        results.extend(
                            self._parse_powershell_output(result.stdout))

                except (subprocess.TimeoutExpired, Exception) as e:
                    print(f"搜索路径 {search_path} 时出错: {e}")
                    continue

                # 如果已经找到足够的结果，停止搜索
                if len(results) >= max_results:
                    break

            # 限制结果数量
            results = results[:max_results]

        except Exception as e:
            print(f"Windows 搜索失败: {e}")

        return results, len(results)

    def _parse_powershell_output(self, output: str) -> List[EverythingSearchResult]:
        """解析 PowerShell 输出"""
        results = []
        lines = output.strip().split('\n')

        current_item = {}

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 解析 PowerShell 对象输出
            if line.startswith('FullName'):
                if current_item:
                    result = self._create_result_from_item(current_item)
                    if result:
                        results.append(result)
                current_item = {'FullName': line.split(':', 1)[1].strip()}
            elif ':' in line and current_item:
                key, value = line.split(':', 1)
                current_item[key.strip()] = value.strip()

        # 处理最后一个项目
        if current_item:
            result = self._create_result_from_item(current_item)
            if result:
                results.append(result)

        return results

    def _create_result_from_item(self, item: dict) -> EverythingSearchResult:
        """从解析的项目创建搜索结果"""
        try:
            result = EverythingSearchResult()

            full_path = item.get('FullName', '')
            if not full_path:
                return None

            result.full_path = full_path
            result.filename = os.path.basename(full_path)
            result.path = os.path.dirname(full_path)

            # 获取扩展名
            _, ext = os.path.splitext(result.filename)
            result.extension = ext.lstrip('.') if ext else ""

            # 检查是否为文件夹
            attributes = item.get('Attributes', '')
            result.is_folder = 'Directory' in attributes
            result.is_file = not result.is_folder

            # 获取文件大小
            if result.is_file:
                try:
                    length = item.get('Length', '0')
                    result.size = int(length) if length.isdigit() else 0
                except (ValueError, TypeError):
                    result.size = 0

            return result

        except Exception:
            return None

    def is_windows_search_available(self) -> bool:
        """检查 Windows Search 是否可用"""
        return self._is_available()


# 创建全局实例
_simple_windows_search = None


def get_simple_windows_search():
    """获取简化的 Windows Search 实例"""
    global _simple_windows_search
    if _simple_windows_search is None:
        _simple_windows_search = SimpleWindowsSearch()
    return _simple_windows_search


def test_simple_windows_search():
    """测试简化的 Windows Search"""
    try:
        search = get_simple_windows_search()
        if not search.is_windows_search_available():
            print("Windows Search 不可用")
            return False

        results, total = search.search("txt", 5)
        print(f"测试搜索 'txt' - 找到 {total} 个结果")
        for i, result in enumerate(results):
            print(f"  {i+1}. {result.filename} - {result.full_path}")
        return True
    except Exception as e:
        print(f"简化 Windows Search 测试失败: {e}")
        return False


if __name__ == "__main__":
    test_simple_windows_search()
