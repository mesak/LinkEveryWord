"""
Everything Flask 搜尋應用程式 - 打包版本入口點
專為 PyInstaller 打包優化
"""
import sys
import os
import webbrowser
import threading
import time
import socket
import signal
import atexit
from filelock import FileLock
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


# 嘗試載入 Everything SDK 並建立實例
everything_sdk_instance = None
mock_sdk_instance = None
windows_search_instance = None
simple_windows_search_instance = None

try:
    from everything_sdk import get_everything_sdk
    EVERYTHING_AVAILABLE = True
    DEMO_MODE = False
    WINDOWS_SEARCH_MODE = False
    SIMPLE_SEARCH_MODE = False
    # 建立 SDK 實例 (單例)
    everything_sdk_instance = get_everything_sdk()
    print("✓ Everything SDK 載入成功")
except Exception as e:
    print(f"⚠ Everything SDK 載入失敗: {e}")

    # 嘗試使用 Windows Search API 作為備用
    try:
        from windows_search_api import get_windows_search_api
        windows_search_instance = get_windows_search_api()

        # 測試 Windows Search API 是否可用
        if windows_search_instance.is_windows_search_available():
            EVERYTHING_AVAILABLE = False
            DEMO_MODE = False
            WINDOWS_SEARCH_MODE = True
            SIMPLE_SEARCH_MODE = False
            print("✓ 使用 Windows Search API 作為備用搜索引擎")
        else:
            raise RuntimeError("Windows Search API 不可用")

    except Exception as ws_error:
        print(f"⚠ Windows Search API 也無法使用: {ws_error}")

        # 嘗試使用簡化的 Windows Search
        try:
            from simple_windows_search import get_simple_windows_search
            simple_windows_search_instance = get_simple_windows_search()

            if simple_windows_search_instance.is_windows_search_available():
                EVERYTHING_AVAILABLE = False
                DEMO_MODE = False
                WINDOWS_SEARCH_MODE = False
                SIMPLE_SEARCH_MODE = True
                print("✓ 使用簡化 Windows Search 作為備用搜索引擎")
            else:
                raise RuntimeError("簡化 Windows Search 不可用")

        except Exception as sws_error:
            print(f"⚠ 簡化 Windows Search 也無法使用: {sws_error}")
            EVERYTHING_AVAILABLE = False
            DEMO_MODE = True
            WINDOWS_SEARCH_MODE = False
            SIMPLE_SEARCH_MODE = False
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
        'windows_search_mode': WINDOWS_SEARCH_MODE if 'WINDOWS_SEARCH_MODE' in globals() else False,
        'simple_search_mode': SIMPLE_SEARCH_MODE if 'SIMPLE_SEARCH_MODE' in globals() else False,
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
        elif WINDOWS_SEARCH_MODE:
            results, total_count = windows_search_instance.search(
                query, max_results)
        elif SIMPLE_SEARCH_MODE:
            results, total_count = simple_windows_search_instance.search(
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
            'windows_search_mode': WINDOWS_SEARCH_MODE if 'WINDOWS_SEARCH_MODE' in globals() else False,
            'simple_search_mode': SIMPLE_SEARCH_MODE if 'SIMPLE_SEARCH_MODE' in globals() else False
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/status')
def status():
    """檢查 Everything 服務狀態"""
    try:
        if DEMO_MODE:
            is_running = mock_sdk_instance.is_everything_running()
            message = '示範模式 - 使用模擬資料'
        else:
            is_running = everything_sdk_instance.is_everything_running()
            message = 'Everything 正在運行' if is_running else 'Everything 未運行或無法連接'

        return jsonify({
            'success': True,
            'everything_running': is_running,
            'message': message,
            'demo_mode': DEMO_MODE
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/search/<query>')
def api_search(query):
    """RESTful API 搜尋端點"""
    try:
        max_results = int(request.args.get('limit', 50))

        if DEMO_MODE:
            results, total_count = mock_sdk_instance.search(query, max_results)
        else:
            results, total_count = everything_sdk_instance.search(
                query, max_results)

        return jsonify({
            'query': query,
            'results': [result.to_dict() for result in results],
            'total': total_count,
            'limit': max_results,
            'demo_mode': DEMO_MODE
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/shutdown')
def shutdown():
    """關閉伺服器"""
    try:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            return jsonify({'error': '無法關閉伺服器'}), 500
        func()
        return jsonify({'message': '伺服器已關閉'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '找不到請求的資源'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '內部伺服器錯誤'}), 500


def open_browser():
    """延遲開啟瀏覽器"""
    time.sleep(1.5)  # 等待伺服器啟動
    webbrowser.open('http://127.0.0.1:5000')


# 全局变量保存锁对象
app_lock = None


def check_single_instance():
    """
    检查是否已有应用程序实例在运行
    使用文件锁实现 singleton 功能
    """
    global app_lock
    try:
        # 使用文件锁，确保真正的单实例
        lock_file = os.path.join(os.path.dirname(
            __file__), "linkeveryword.lock")
        app_lock = FileLock(lock_file)

        # 尝试获取锁，不阻塞
        app_lock.acquire(timeout=0.1)
        print("✅ 成功获取应用程序锁")
        return True

    except Exception as e:
        print(f"🔒 应用程序锁获取失败: {e}")
        app_lock = None
        return False


def cleanup_lock():
    """清理锁"""
    global app_lock
    if app_lock and app_lock.is_locked:
        try:
            app_lock.release()
            print("🔓 釋放應用程式實例鎖")
        except Exception:
            pass
        app_lock = None


def signal_handler(signum, frame):
    """信号处理函数"""
    print(f"\n📡 接收到信號 {signum}，正在清理...")
    cleanup_lock()
    sys.exit(0)


def setup_cleanup():
    """设置清理机制"""
    # 注册程序退出时的清理函数
    atexit.register(cleanup_lock)

    # 注册信号处理器（仅在支持的平台上）
    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    except AttributeError:
        # Windows 不支持某些信号
        pass


def check_flask_port_available():
    """检查 Flask 端口是否可用"""
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 同样不使用 SO_REUSEADDR 进行真正的检查
        test_socket.bind(('127.0.0.1', 5000))
        test_socket.close()
        return True
    except OSError:
        return False


def main():
    """主函數"""
    # 設置清理機制
    setup_cleanup()

    # 確保應用程式只執行一個實例 - 多重检查
    print("🔒 檢查應用程式實例...")

    # 检查 1: Singleton 锁端口
    if not check_single_instance():
        print("❌ 應用程式已經在執行中！(檢測到 Singleton 鎖)")
        print("請檢查系統托盤或工作管理員中是否已有此應用程式運行。")
        print("如果確認沒有運行，請等待幾秒後再試。")
        sys.exit(1)

    print("✓ Singleton 鎖檢查通過")

    # 检查 2: Flask 端口是否可用
    if not check_flask_port_available():
        print("❌ 應用程式已經在執行中！(端口 5000 被佔用)")
        print("另一個應用程式實例正在使用 Web 服務端口。")
        cleanup_lock()
        sys.exit(1)

    print("✓ Web 服務端口檢查通過")
    print("✓ 應用程式實例檢查完成")

    print("=" * 60)
    print("🔍 Everything Flask 搜尋應用程式")
    print("=" * 60)

    if DEMO_MODE:
        print("⚠ 以示範模式運行 - Everything SDK 不可用")
        print("要使用完整功能，請:")
        print("1. 安裝 Everything 搜尋引擎")
        print("2. 啟動 Everything")
        print("3. 重新啟動此應用程式")
    else:
        print("✓ Everything SDK 已載入")
        print("請確保 Everything 搜尋引擎正在運行")

    print()
    print("🌐 Web 介面將在瀏覽器中自動開啟")
    print("📍 服務地址: http://127.0.0.1:5000")
    print("📊 狀態檢查: http://127.0.0.1:5000/status")
    print()
    print("💡 按 Ctrl+C 停止服務")
    print("=" * 60)

    # 在新執行緒中開啟瀏覽器
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    try:
        # 啟動 Flask 應用程式
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 感謝使用 Everything Flask 搜尋應用程式！")
    except Exception as e:
        print(f"\n❌ 應用程式錯誤: {e}")
        input("按 Enter 鍵退出...")
    finally:
        # 清理锁套接字
        cleanup_lock()


if __name__ == '__main__':
    main()
