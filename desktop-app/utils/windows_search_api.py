"""
Windows Search API Python wrapper
作为 Everything SDK 的备用搜索引擎
使用 Windows Search Service (WDS) 进行文件搜索
"""
import os
from typing import List, Tuple

try:
    import pythoncom
    import win32com.client
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("⚠ pywin32 模块未安装，Windows Search API 不可用")

from everything_sdk import EverythingSearchResult


class WindowsSearchAPI:
    """Windows Search API 的 Python 包装类"""

    def __init__(self):
        self._connection = None
        self._query_helper = None
        self._connected = False

    def _ensure_connection(self):
        """确保与 Windows Search Service 的连接"""
        if self._connected:
            return

        if not WIN32_AVAILABLE:
            raise RuntimeError("pywin32 模块未安装，无法使用 Windows Search API")

        try:
            # 初始化 COM
            pythoncom.CoInitialize()

            # 创建 Windows Search 连接
            self._connection = win32com.client.Dispatch(
                "Microsoft.Search.Interop.CSearchManager")
            catalog = self._connection.GetCatalog("SystemIndex")
            self._query_helper = catalog.GetQueryHelper()
            self._connected = True
            print("✓ Windows Search API 连接成功")

        except Exception as e:
            print(f"⚠ Windows Search API 连接失败: {e}")
            raise RuntimeError(f"无法连接到 Windows Search Service: {e}") from e

    def _execute_sql_query(self, sql_query: str, max_results: int = 100) -> List[EverythingSearchResult]:
        """执行 SQL 查询并返回结果"""
        results = []

        try:
            # 创建连接字符串
            connection_string = "Provider=Search.CollatorDSO;Extended Properties='Application=Windows';"

            # 创建 ADO 连接
            connection = win32com.client.Dispatch("ADODB.Connection")
            connection.Open(connection_string)

            # 创建记录集
            recordset = win32com.client.Dispatch("ADODB.Recordset")
            recordset.Open(sql_query, connection)

            count = 0
            while not recordset.EOF and count < max_results:
                result = EverythingSearchResult()

                try:
                    # 获取文件路径
                    system_path = recordset.Fields(
                        "System.ItemPathDisplay").Value
                    if system_path:
                        result.full_path = system_path
                        result.path = os.path.dirname(system_path)
                        result.filename = os.path.basename(system_path)

                        # 获取扩展名
                        _, ext = os.path.splitext(result.filename)
                        result.extension = ext.lstrip('.') if ext else ""

                    # 获取文件大小
                    try:
                        size_field = recordset.Fields("System.Size")
                        if size_field and size_field.Value:
                            result.size = int(size_field.Value)
                    except (AttributeError, ValueError, TypeError):
                        result.size = 0

                    # 获取修改日期
                    try:
                        date_modified_field = recordset.Fields(
                            "System.DateModified")
                        if date_modified_field and date_modified_field.Value:
                            result.date_modified = date_modified_field.Value
                    except (AttributeError, ValueError, TypeError):
                        pass

                    # 获取创建日期
                    try:
                        date_created_field = recordset.Fields(
                            "System.DateCreated")
                        if date_created_field and date_created_field.Value:
                            result.date_created = date_created_field.Value
                    except (AttributeError, ValueError, TypeError):
                        pass

                    # 检查是文件还是文件夹
                    try:
                        kind_field = recordset.Fields("System.Kind")
                        if kind_field and kind_field.Value:
                            kind = str(kind_field.Value).lower()
                            result.is_folder = "folder" in kind
                            result.is_file = not result.is_folder
                        else:
                            # 如果无法确定，根据路径判断
                            result.is_file = os.path.isfile(
                                result.full_path) if result.full_path else True
                            result.is_folder = not result.is_file
                    except (AttributeError, ValueError, TypeError):
                        result.is_file = True
                        result.is_folder = False

                    results.append(result)

                except Exception as field_error:
                    print(f"处理记录时出错: {field_error}")
                    continue

                recordset.MoveNext()
                count += 1

            recordset.Close()
            connection.Close()

        except Exception as e:
            print(f"SQL 查询执行失败: {e}")

        return results

    def search(self, query: str, max_results: int = 100) -> Tuple[List[EverythingSearchResult], int]:
        """
        执行搜索

        Args:
            query: 搜索查询字符串
            max_results: 最大结果数量

        Returns:
            (results, total_count): 搜索结果列表和总结果数
        """
        self._ensure_connection()

        if not query.strip():
            return [], 0

        # 清理查询字符串，避免 SQL 注入
        clean_query = query.replace("'", "''").strip()

        # 构建 SQL 查询
        # 搜索文件名包含查询字符串的文件
        sql_query = f"""
        SELECT TOP {max_results}
            System.ItemPathDisplay,
            System.FileName,
            System.Size,
            System.DateModified,
            System.DateCreated,
            System.Kind
        FROM SystemIndex 
        WHERE CONTAINS(System.FileName, '"{clean_query}"')
           OR System.FileName LIKE '%{clean_query}%'
        ORDER BY System.DateModified DESC
        """

        try:
            results = self._execute_sql_query(sql_query, max_results)
            total_count = len(results)  # Windows Search API 不容易获取确切的总数

            print(f"Windows Search API 找到 {total_count} 个结果")
            return results, total_count

        except Exception as e:
            print(f"Windows Search API 搜索失败: {e}")
            return [], 0

    def is_windows_search_available(self) -> bool:
        """检查 Windows Search Service 是否可用"""
        try:
            self._ensure_connection()
            return self._connected
        except Exception:
            return False


# 创建全局实例
_windows_search_api = None


def get_windows_search_api():
    """获取 Windows Search API 实例"""
    global _windows_search_api
    if _windows_search_api is None:
        _windows_search_api = WindowsSearchAPI()
    return _windows_search_api


def test_windows_search():
    """测试 Windows Search API 功能"""
    try:
        api = get_windows_search_api()
        results, total = api.search("txt", 10)
        print(f"测试搜索 'txt' - 找到 {total} 个结果")
        for i, result in enumerate(results[:3]):
            print(f"  {i+1}. {result.filename} - {result.full_path}")
        return True
    except Exception as e:
        print(f"Windows Search API 测试失败: {e}")
        return False


if __name__ == "__main__":
    test_windows_search()
