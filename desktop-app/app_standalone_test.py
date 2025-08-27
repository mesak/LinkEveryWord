"""
Everything Flask 搜尋應用程式 - 测试版本
支持通过环境变量禁用特定搜索引擎来测试备用方案
"""
import sys
import os
import webbrowser
import threading
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# 確保資源路徑正確


def get_resource_path(relative_path):
    """取得資源檔案的絕對路徑，適用於 PyInstaller 打包"""
    try:
        # PyInstaller 臨時資料夾
        base_path = sys._MEIPASS
    except AttributeError:
        # 開發環境
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 检查环境变量来决定是否禁用特定搜索引擎
DISABLE_EVERYTHING = os.getenv('DISABLE_EVERYTHING', '0') == '1'
DISABLE_WINDOWS_SEARCH = os.getenv('DISABLE_WINDOWS_SEARCH', '0') == '1'
DISABLE_SIMPLE_SEARCH = os.getenv('DISABLE_SIMPLE_SEARCH', '0') == '1'

print("=" * 60)
print("测试模式启动参数:")
print(f"DISABLE_EVERYTHING: {DISABLE_EVERYTHING}")
print(f"DISABLE_WINDOWS_SEARCH: {DISABLE_WINDOWS_SEARCH}")
print(f"DISABLE_SIMPLE_SEARCH: {DISABLE_SIMPLE_SEARCH}")
print("=" * 60)

# 嘗試載入 Everything SDK 並建立實例
everything_sdk_instance = None
mock_sdk_instance = None
windows_search_instance = None
simple_windows_search_instance = None

# 初始化所有状态为 False
EVERYTHING_AVAILABLE = False
DEMO_MODE = False
WINDOWS_SEARCH_MODE = False
SIMPLE_SEARCH_MODE = False

if not DISABLE_EVERYTHING:
    try:
        from everything_sdk import get_everything_sdk
        everything_sdk_instance = get_everything_sdk()
        EVERYTHING_AVAILABLE = True
        print("✓ Everything SDK 載入成功")
    except Exception as e:
        print(f"⚠ Everything SDK 載入失敗: {e}")
else:
    print("⚠ Everything SDK 已被环境变量禁用")

# 如果 Everything 不可用，尝试 Windows Search API
if not EVERYTHING_AVAILABLE and not DISABLE_WINDOWS_SEARCH:
    try:
        from windows_search_api import get_windows_search_api
        windows_search_instance = get_windows_search_api()

        # 測試 Windows Search API 是否可用
        if windows_search_instance.is_windows_search_available():
            WINDOWS_SEARCH_MODE = True
            print("✓ 使用 Windows Search API 作為備用搜索引擎")
        else:
            raise RuntimeError("Windows Search API 不可用")

    except Exception as ws_error:
        print(f"⚠ Windows Search API 無法使用: {ws_error}")
elif DISABLE_WINDOWS_SEARCH:
    print("⚠ Windows Search API 已被环境变量禁用")

# 如果前两个都不可用，尝试简化搜索
if not EVERYTHING_AVAILABLE and not WINDOWS_SEARCH_MODE and not DISABLE_SIMPLE_SEARCH:
    try:
        from simple_windows_search import get_simple_windows_search
        simple_windows_search_instance = get_simple_windows_search()

        if simple_windows_search_instance.is_windows_search_available():
            SIMPLE_SEARCH_MODE = True
            print("✓ 使用簡化 Windows Search 作為備用搜索引擎")
        else:
            raise RuntimeError("簡化 Windows Search 不可用")

    except Exception as sws_error:
        print(f"⚠ 簡化 Windows Search 無法使用: {sws_error}")
elif DISABLE_SIMPLE_SEARCH:
    print("⚠ 简化搜索已被环境变量禁用")

# 如果所有搜索引擎都不可用，使用演示模式
if not EVERYTHING_AVAILABLE and not WINDOWS_SEARCH_MODE and not SIMPLE_SEARCH_MODE:
    DEMO_MODE = True
    print("  應用程式將以示範模式運行")

    # 載入示範模組並建立實例
    from mock_everything import get_mock_everything_sdk
    mock_sdk_instance = get_mock_everything_sdk()

# 設定 Flask 應用程式
app = Flask(__name__,
            template_folder=get_resource_path('templates'),
            static_folder=get_resource_path('static'))
CORS(app)


@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')


@app.route('/status')
def app_status():
    """取得應用程式狀態"""
    return jsonify({
        'everything_available': EVERYTHING_AVAILABLE,
        'demo_mode': DEMO_MODE,
        'windows_search_mode': WINDOWS_SEARCH_MODE,
        'simple_search_mode': SIMPLE_SEARCH_MODE,
        'search_engine': ('Everything' if EVERYTHING_AVAILABLE else
                          ('Windows Search' if WINDOWS_SEARCH_MODE else
                           ('Simple Search' if SIMPLE_SEARCH_MODE else 'Demo')))
    })


@app.route('/search', methods=['GET', 'POST'])
def search():
    """搜尋 API 端點"""
    try:
        if request.method == 'GET':
            query = request.args.get('q', '')
            max_results = int(request.args.get('max', 50))
        else:  # POST
            data = request.get_json()
            query = data.get('query', '')
            max_results = int(data.get('max_results', 50))

        if not query:
            return jsonify({
                'success': False,
                'error': '請提供搜尋查詢'
            }), 400

        # 限制最大結果數
        max_results = min(max_results, 500)

        # 執行搜尋
        if DEMO_MODE:
            results, total_count = mock_sdk_instance.search(query, max_results)
        elif SIMPLE_SEARCH_MODE:
            results, total_count = simple_windows_search_instance.search(
                query, max_results)
        elif WINDOWS_SEARCH_MODE:
            results, total_count = windows_search_instance.search(
                query, max_results)
        else:
            results, total_count = everything_sdk_instance.search(
                query, max_results)

        # 轉換結果為字典格式
        results_data = [result.to_dict() for result in results]

        return jsonify({
            'success': True,
            'query': query,
            'results': results_data,
            'total_count': total_count,
            'displayed_count': len(results_data),
            'demo_mode': DEMO_MODE,
            'windows_search_mode': WINDOWS_SEARCH_MODE,
            'simple_search_mode': SIMPLE_SEARCH_MODE
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'搜尋過程中發生錯誤: {str(e)}'
        }), 500


def open_browser():
    """在瀏覽器中開啟應用程式"""
    time.sleep(1.5)  # 給伺服器一點啟動時間
    webbrowser.open('http://127.0.0.1:5000')


def status():
    """顯示啟動狀態"""
    current_engine = "Unknown"
    if EVERYTHING_AVAILABLE:
        current_engine = "Everything"
    elif WINDOWS_SEARCH_MODE:
        current_engine = "Windows Search API"
    elif SIMPLE_SEARCH_MODE:
        current_engine = "简化 Windows Search"
    elif DEMO_MODE:
        current_engine = "演示模式"

    print("=" * 60)
    print("🔍 Everything Flask 搜尋應用程式 (测试模式)")
    print("=" * 60)
    print(f"✓ 当前搜索引擎: {current_engine}")

    if not EVERYTHING_AVAILABLE:
        print("⚠ Everything 搜尋引擎不可用")

    print()
    print("🌐 Web 介面將在瀏覽器中自動開啟")
    print("📍 服務地址: http://127.0.0.1:5000")
    print("📊 狀態檢查: http://127.0.0.1:5000/status")
    print()
    print("💡 按 Ctrl+C 停止服務")
    print("=" * 60)


if __name__ == '__main__':
    # 顯示啟動狀態
    status()

    # 在背景開啟瀏覽器
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # 啟動 Flask 應用程式
    try:
        app.run(host='127.0.0.1', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 應用程式已停止")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
        sys.exit(1)
