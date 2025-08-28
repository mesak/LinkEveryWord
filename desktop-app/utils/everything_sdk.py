"""
Everything SDK Python wrapper
基於 voidtools Everything 搜尋引擎的 Python 介面
"""
import ctypes
import datetime
import struct
import os
from typing import List, Dict, Optional, Tuple

# 定義常數
EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME = 0x00000004
EVERYTHING_REQUEST_EXTENSION = 0x00000008
EVERYTHING_REQUEST_SIZE = 0x00000010
EVERYTHING_REQUEST_DATE_CREATED = 0x00000020
EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040
EVERYTHING_REQUEST_DATE_ACCESSED = 0x00000080
EVERYTHING_REQUEST_ATTRIBUTES = 0x00000100
EVERYTHING_REQUEST_FILE_LIST_FILE_NAME = 0x00000200
EVERYTHING_REQUEST_RUN_COUNT = 0x00000400
EVERYTHING_REQUEST_DATE_RUN = 0x00000800
EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED = 0x00001000
EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME = 0x00002000
EVERYTHING_REQUEST_HIGHLIGHTED_PATH = 0x00004000

# Windows FILETIME 轉換常數
WINDOWS_TICKS = int(1/10**-7)  # 10,000,000 (100 nanoseconds)
WINDOWS_EPOCH = datetime.datetime.strptime(
    '1601-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
POSIX_EPOCH = datetime.datetime.strptime(
    '1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
EPOCH_DIFF = (POSIX_EPOCH - WINDOWS_EPOCH).total_seconds()
WINDOWS_TICKS_TO_POSIX_EPOCH = EPOCH_DIFF * WINDOWS_TICKS


class EverythingSearchResult:
    """表示一個搜尋結果的類別"""

    def __init__(self):
        self.filename: str = ""
        self.path: str = ""
        self.full_path: str = ""
        self.extension: str = ""
        self.size: int = 0
        self.date_created: Optional[datetime.datetime] = None
        self.date_modified: Optional[datetime.datetime] = None
        self.date_accessed: Optional[datetime.datetime] = None
        self.is_file: bool = True
        self.is_folder: bool = False

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


class EverythingSDK:
    """Everything SDK 的 Python 包裝類別"""

    def __init__(self):
        self.everything_dll = None
        self._dll_loaded = False

    def _load_dll(self):
        """載入 Everything DLL"""
        dll_paths = [
            # 嘗試從系統路徑載入
            r"dll\Everything64.dll",
            r"dll\Everything32.dll",
            # 嘗試從 Everything 安裝目錄載入
            r"C:\Program Files\Everything\Everything64.dll",
            r"C:\Program Files (x86)\Everything\Everything32.dll",
            r"C:\Program Files\Everything\Everything32.dll",
            # 嘗試從當前目錄載入
            r".\Everything64.dll",
            r".\Everything32.dll"
        ]

        for dll_path in dll_paths:
            try:
                self.everything_dll = ctypes.WinDLL(dll_path)
                print(f"成功載入 DLL: {dll_path}")
                return
            except OSError:
                continue

        # 如果都找不到，拋出詳細的錯誤訊息
        raise RuntimeError(
            "找不到 Everything DLL。請確保:\n"
            "1. Everything 搜尋引擎已安裝\n"
            "2. Everything 正在運行\n"
            "3. 或者將 Everything64.dll 或 Everything32.dll 複製到此目錄\n"
            f"嘗試的路徑: {', '.join(dll_paths)}"
        )

    def _setup_function_signatures(self):
        """設定 DLL 函數簽名"""
        # 設定查詢函數
        self.everything_dll.Everything_SetSearchW.argtypes = [ctypes.c_wchar_p]
        self.everything_dll.Everything_SetRequestFlags.argtypes = [
            ctypes.c_uint]
        self.everything_dll.Everything_QueryW.argtypes = [ctypes.c_bool]
        self.everything_dll.Everything_QueryW.restype = ctypes.c_bool

        # 設定結果函數
        self.everything_dll.Everything_GetNumResults.restype = ctypes.c_uint
        self.everything_dll.Everything_GetResultFullPathNameW.argtypes = [
            ctypes.c_uint, ctypes.c_wchar_p, ctypes.c_uint]
        self.everything_dll.Everything_GetResultFullPathNameW.restype = ctypes.c_uint
        self.everything_dll.Everything_GetResultFileNameW.argtypes = [
            ctypes.c_uint]
        self.everything_dll.Everything_GetResultFileNameW.restype = ctypes.c_wchar_p
        self.everything_dll.Everything_GetResultPathW.argtypes = [
            ctypes.c_uint]
        self.everything_dll.Everything_GetResultPathW.restype = ctypes.c_wchar_p
        self.everything_dll.Everything_GetResultExtensionW.argtypes = [
            ctypes.c_uint]
        self.everything_dll.Everything_GetResultExtensionW.restype = ctypes.c_wchar_p

        # 設定檔案資訊函數
        self.everything_dll.Everything_GetResultSize.argtypes = [
            ctypes.c_uint, ctypes.POINTER(ctypes.c_ulonglong)]
        self.everything_dll.Everything_GetResultDateModified.argtypes = [
            ctypes.c_uint, ctypes.POINTER(ctypes.c_ulonglong)]
        self.everything_dll.Everything_GetResultDateCreated.argtypes = [
            ctypes.c_uint, ctypes.POINTER(ctypes.c_ulonglong)]
        self.everything_dll.Everything_GetResultDateAccessed.argtypes = [
            ctypes.c_uint, ctypes.POINTER(ctypes.c_ulonglong)]

        # 設定檔案類型檢查函數
        self.everything_dll.Everything_IsFileResult.argtypes = [ctypes.c_uint]
        self.everything_dll.Everything_IsFileResult.restype = ctypes.c_bool
        self.everything_dll.Everything_IsFolderResult.argtypes = [
            ctypes.c_uint]
        self.everything_dll.Everything_IsFolderResult.restype = ctypes.c_bool

    def _convert_filetime_to_datetime(self, filetime: ctypes.c_ulonglong) -> Optional[datetime.datetime]:
        """將 Windows FILETIME 轉換為 Python datetime"""
        try:
            if filetime.value == 0:
                return None
            winticks = filetime.value
            microsecs = (winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / \
                WINDOWS_TICKS
            return datetime.datetime.fromtimestamp(microsecs)
        except (ValueError, OSError):
            return None

    def _ensure_dll_loaded(self):
        """確保 DLL 已載入"""
        if not self._dll_loaded:
            self._load_dll()
            self._setup_function_signatures()
            self._dll_loaded = True

    def search(self, query: str, max_results: int = 100) -> Tuple[List[EverythingSearchResult], int]:
        """
        執行搜尋

        Args:
            query: 搜尋查詢字串
            max_results: 最大結果數量

        Returns:
            (results, total_count): 搜尋結果列表和總結果數
        """
        self._ensure_dll_loaded()

        if not self.everything_dll:
            raise RuntimeError("Everything DLL 未載入")

        # 設定搜尋查詢
        self.everything_dll.Everything_SetSearchW(query)

        # 設定要取得的資訊
        request_flags = (
            EVERYTHING_REQUEST_FILE_NAME |
            EVERYTHING_REQUEST_PATH |
            EVERYTHING_REQUEST_EXTENSION |
            EVERYTHING_REQUEST_SIZE |
            EVERYTHING_REQUEST_DATE_MODIFIED |
            EVERYTHING_REQUEST_DATE_CREATED |
            EVERYTHING_REQUEST_DATE_ACCESSED
        )
        self.everything_dll.Everything_SetRequestFlags(request_flags)

        # 設定最大結果數
        self.everything_dll.Everything_SetMax(max_results)

        # 執行查詢
        if not self.everything_dll.Everything_QueryW(True):
            raise RuntimeError("查詢失敗")

        # 取得結果數量
        total_results = self.everything_dll.Everything_GetNumResults()
        actual_results = min(total_results, max_results)

        results = []

        # 處理每個結果
        for i in range(actual_results):
            result = EverythingSearchResult()

            # 取得檔案名稱
            filename = self.everything_dll.Everything_GetResultFileNameW(i)
            if filename:
                result.filename = filename

            # 取得路徑
            path = self.everything_dll.Everything_GetResultPathW(i)
            if path:
                result.path = path
                result.full_path = os.path.join(path, result.filename)

            # 取得副檔名
            extension = self.everything_dll.Everything_GetResultExtensionW(i)
            if extension:
                result.extension = extension

            # 取得檔案大小
            file_size = ctypes.c_ulonglong()
            self.everything_dll.Everything_GetResultSize(i, file_size)
            result.size = file_size.value

            # 取得修改日期
            date_modified = ctypes.c_ulonglong()
            self.everything_dll.Everything_GetResultDateModified(
                i, date_modified)
            result.date_modified = self._convert_filetime_to_datetime(
                date_modified)

            # 取得建立日期
            date_created = ctypes.c_ulonglong()
            self.everything_dll.Everything_GetResultDateCreated(
                i, date_created)
            result.date_created = self._convert_filetime_to_datetime(
                date_created)

            # 取得存取日期
            date_accessed = ctypes.c_ulonglong()
            self.everything_dll.Everything_GetResultDateAccessed(
                i, date_accessed)
            result.date_accessed = self._convert_filetime_to_datetime(
                date_accessed)

            # 檢查是檔案還是資料夾
            result.is_file = self.everything_dll.Everything_IsFileResult(i)
            result.is_folder = self.everything_dll.Everything_IsFolderResult(i)

            results.append(result)

        return results, total_results

    def is_everything_running(self) -> bool:
        """檢查 Everything 是否正在運行"""
        try:
            self._ensure_dll_loaded()
            # 執行一個簡單的查詢來測試連接
            self.everything_dll.Everything_SetSearchW("")
            self.everything_dll.Everything_SetMax(1)
            return self.everything_dll.Everything_QueryW(True)
        except (OSError, RuntimeError):
            return False


# 創建全域實例，但延遲載入
everything_sdk = None


def get_everything_sdk():
    """取得 Everything SDK 實例"""
    global everything_sdk
    if everything_sdk is None:
        everything_sdk = EverythingSDK()
    return everything_sdk
