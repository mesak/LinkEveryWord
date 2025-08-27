"""
示範模式 - 模擬 Everything SDK 功能
"""
import datetime
from typing import List, Dict, Tuple


class MockEverythingSearchResult:
    """模擬搜尋結果的類別"""

    def __init__(self, filename: str, path: str, size: int = 0, is_file: bool = True):
        self.filename = filename
        self.path = path
        self.full_path = f"{path}\\{filename}" if path else filename
        self.extension = filename.split(
            '.')[-1] if '.' in filename and is_file else ""
        self.size = size
        self.date_created = datetime.datetime.now() - datetime.timedelta(days=30)
        self.date_modified = datetime.datetime.now() - datetime.timedelta(days=1)
        self.date_accessed = datetime.datetime.now()
        self.is_file = is_file
        self.is_folder = not is_file

    def to_dict(self) -> Dict:
        """轉換為字典格式"""
        return {
            'filename': self.filename,
            'path': self.path,
            'full_path': self.full_path,
            'extension': self.extension,
            'size': self.size,
            'size_formatted': self._format_size(self.size),
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_modified': self.date_modified.isoformat() if self.date_modified else None,
            'date_accessed': self.date_accessed.isoformat() if self.date_accessed else None,
            'is_file': self.is_file,
            'is_folder': self.is_folder
        }

    def _format_size(self, size_bytes: int) -> str:
        """格式化檔案大小"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"


class MockEverythingSDK:
    """模擬 Everything SDK 的類別"""

    def __init__(self):
        # 建立一些示範資料
        self.mock_files = [
            # Python 檔案
            MockEverythingSearchResult(
                "app.py", "D:\\Work\\pyeverything", 5120),
            MockEverythingSearchResult(
                "test.py", "D:\\Work\\projects\\myapp", 2048),
            MockEverythingSearchResult(
                "main.py", "C:\\Users\\User\\Documents\\python", 8192),
            MockEverythingSearchResult(
                "setup.py", "D:\\Work\\myproject", 1024),

            # 文件檔案
            MockEverythingSearchResult(
                "readme.txt", "D:\\Work\\projects", 3072),
            MockEverythingSearchResult(
                "notes.txt", "C:\\Users\\User\\Desktop", 1536),
            MockEverythingSearchResult("config.txt", "D:\\Apps\\myapp", 512),

            # 圖片檔案
            MockEverythingSearchResult(
                "image.jpg", "C:\\Users\\User\\Pictures", 2097152),
            MockEverythingSearchResult(
                "photo.png", "D:\\Photos\\vacation", 1048576),
            MockEverythingSearchResult(
                "screenshot.png", "C:\\Users\\User\\Desktop", 524288),

            # 資料夾
            MockEverythingSearchResult(
                "Documents", "C:\\Users\\User", 0, False),
            MockEverythingSearchResult("Projects", "D:\\Work", 0, False),
            MockEverythingSearchResult(
                "Downloads", "C:\\Users\\User", 0, False),

            # Office 檔案
            MockEverythingSearchResult(
                "presentation.pptx", "D:\\Work\\documents", 5242880),
            MockEverythingSearchResult(
                "report.docx", "C:\\Users\\User\\Documents", 204800),
            MockEverythingSearchResult(
                "data.xlsx", "D:\\Work\\analysis", 1048576),
        ]

    def search(self, query: str, max_results: int = 100) -> Tuple[List[MockEverythingSearchResult], int]:
        """
        模擬搜尋功能
        """
        query = query.lower()
        results = []

        # 簡單的搜尋邏輯
        for file in self.mock_files:
            match = False

            # 檢查檔名
            if query in file.filename.lower():
                match = True

            # 檢查副檔名模式 (如 *.txt)
            if query.startswith("*."):
                ext = query[2:]
                if file.extension.lower() == ext.lower():
                    match = True

            # 檢查路徑
            if query in file.path.lower():
                match = True

            if match:
                results.append(file)

        # 限制結果數量
        total_count = len(results)
        results = results[:max_results]

        return results, total_count

    def is_everything_running(self) -> bool:
        """模擬檢查 Everything 狀態 - 在示範模式下總是返回 True"""
        return True


# 創建全域實例，使用單例模式
_mock_sdk_instance = None


def get_mock_everything_sdk():
    """取得 Mock Everything SDK 實例 (單例模式)"""
    global _mock_sdk_instance
    if _mock_sdk_instance is None:
        _mock_sdk_instance = MockEverythingSDK()
    return _mock_sdk_instance


# 保持向後相容性 - 全域變數指向單例實例
mock_sdk = get_mock_everything_sdk()
