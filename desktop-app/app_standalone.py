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
import yaml
import logging
import logging.handlers
from filelock import FileLock
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# 確保資源路徑正確


def get_resource_path(relative_path):
    """取得資源檔案的絕對路徑，適用於 PyInstaller 打包"""
    try:
        # PyInstaller 臨時資料夾
        base_path = sys._MEIPASS
        # 對於配置文件，我們希望它能被持久保存，所以放在 exe 檔案同目錄
        if relative_path == 'config.yml':
            # 獲取 exe 檔案所在目錄
            exe_dir = os.path.dirname(sys.executable) if getattr(
                sys, 'frozen', False) else os.path.abspath(".")
            return os.path.join(exe_dir, relative_path)
    except AttributeError:
        # 開發環境
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_config():
    """載入配置文件，如果不存在則創建預設配置"""
    config_path = get_resource_path('config.yml')
    default_config = {
        'server': {
            'host': '127.0.0.1',
            'port': 5000,
            'debug': False,
            'use_reloader': False
        },
        'app': {
            'name': 'Everything Flask 搜尋應用程式',
            'auto_open_browser': True,
            'browser_delay': 2
        },
        'logging': {
            'level': 'INFO',
            'enable_file': True,
            'filename': 'app.log',
            'max_size': 10,
            'backup_count': 5,
            'enable_console': True,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'date_format': '%Y-%m-%d %H:%M:%S'
        }
    }

    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                # 合併默認配置和載入的配置
                if config:
                    # 深度合併配置，確保新增的配置項目也會包含
                    for section, values in default_config.items():
                        if section in config:
                            if isinstance(values, dict):
                                for key, default_value in values.items():
                                    if key not in config[section]:
                                        config[section][key] = default_value
                        else:
                            config[section] = values
                    default_config = config
                print(f"✓ 配置文件載入成功: {config_path}")
        else:
            # 配置文件不存在，創建預設配置
            print(f"⚠ 配置文件不存在，正在創建預設配置: {config_path}")
            create_default_config(config_path, default_config)
            print(f"✓ 預設配置文件已創建: {config_path}")
    except Exception as e:
        print(f"⚠ 配置文件載入失敗，使用內建預設配置: {e}")

    return default_config


def create_default_config(config_path, config):
    """創建預設配置文件"""
    config_content = """# LinkEveryWord Desktop App Configuration
# 應用程式配置文件

server:
  # 服務器主機地址
  host: '127.0.0.1'
  
  # 服務器端口號
  port: 5000
  
  # 調試模式 (生產環境建議設為 false)
  debug: false
  
  # 是否使用自動重載 (生產環境建議設為 false)
  use_reloader: false

app:
  # 應用程式名稱
  name: 'Everything Flask 搜尋應用程式'
  
    # 是否啟動後自動開啟瀏覽器 (true=自動開啟, false=不自動開啟)
    auto_open_browser: true
    # 瀏覽器自動開啟延遲時間 (秒)
    browser_delay: 2

logging:
  # 日誌級別: DEBUG, INFO, WARNING, ERROR, CRITICAL
  level: 'INFO'
  
  # 是否啟用文件日誌
  enable_file: true
  
  # 日誌文件名
  filename: 'app.log'
  
  # 日誌文件最大大小 (MB)
  max_size: 10
  
  # 保留的日誌文件數量
  backup_count: 5
  
  # 是否啟用控制台日誌
  enable_console: true
  
  # 日誌格式
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  
  # 日期格式
  date_format: '%Y-%m-%d %H:%M:%S'
"""

    try:
        # 確保目錄存在
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
    except Exception as e:
        print(f"⚠ 無法創建配置文件: {e}")
        print("將使用內建預設配置")


def setup_logging(config):
    """設置日誌系統"""
    log_config = config.get('logging', {})

    # 獲取日誌級別
    level_str = log_config.get('level', 'INFO').upper()
    level = getattr(logging, level_str, logging.INFO)

    # 創建根 logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # 清除現有的 handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 創建格式化器
    formatter = logging.Formatter(
        fmt=log_config.get(
            'format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        datefmt=log_config.get('date_format', '%Y-%m-%d %H:%M:%S')
    )

    # 設置控制台日誌
    if log_config.get('enable_console', True):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # 設置文件日誌
    if log_config.get('enable_file', True):
        try:
            # 獲取日誌文件路徑
            log_filename = log_config.get('filename', 'app.log')
            log_path = get_resource_path(log_filename)

            # 確保日誌目錄存在
            log_dir = os.path.dirname(log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)

            # 創建旋轉文件處理器
            max_size = log_config.get(
                'max_size', 10) * 1024 * 1024  # 轉換為 bytes
            backup_count = log_config.get('backup_count', 5)

            file_handler = logging.handlers.RotatingFileHandler(
                log_path,
                maxBytes=max_size,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            logger.info(f"日誌文件設置完成: {log_path}")

        except Exception as e:
            logger.warning(f"無法設置文件日誌: {e}")

    # 創建應用程式專用 logger
    app_logger = logging.getLogger('LinkEveryWord')
    app_logger.info("日誌系統初始化完成")

    return app_logger


# 載入配置
CONFIG = load_config()

# 設置日誌系統
APP_LOGGER = setup_logging(CONFIG)


# 嘗試載入 Everything SDK 並建立實例
everything_sdk_instance = None
mock_sdk_instance = None
windows_search_instance = None
simple_windows_search_instance = None

APP_LOGGER.info("開始初始化搜尋引擎...")

try:
    from utils.everything_sdk import get_everything_sdk
    EVERYTHING_AVAILABLE = True
    DEMO_MODE = False
    WINDOWS_SEARCH_MODE = False
    SIMPLE_SEARCH_MODE = False
    # 建立 SDK 實例 (單例)
    everything_sdk_instance = get_everything_sdk()
    APP_LOGGER.info("✓ Everything SDK 載入成功")
    print("✓ Everything SDK 載入成功")
except Exception as e:
    APP_LOGGER.warning(f"Everything SDK 載入失敗: {e}")
    print(f"⚠ Everything SDK 載入失敗: {e}")

    # 嘗試使用 Windows Search API 作為備用
    try:
        from utils.windows_search_api import get_windows_search_api
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
            from utils.simple_windows_search import get_simple_windows_search
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
            from utils.mock_everything import get_mock_everything_sdk
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


@app.route('/search', methods=['GET', 'POST'])
def search():
    """搜尋 API 端點"""
    try:
        APP_LOGGER.debug("收到搜尋請求")

        if request.method == 'GET':
            query = request.args.get('q', '')
            max_results = int(request.args.get('max', 50))
        else:  # POST
            data = request.get_json()
            query = data.get('query', '')
            max_results = int(data.get('max_results', 50))

        APP_LOGGER.info(f"搜尋查詢: '{query}', 最大結果數: {max_results}")

        if not query:
            APP_LOGGER.warning("搜尋請求缺少查詢參數")
            return jsonify({
                'success': False,
                'error': '請提供搜尋查詢'
            }), 400

        # 限制最大結果數
        max_results = min(max_results, 500)

        # 執行搜尋
        start_time = time.time()

        if DEMO_MODE:
            APP_LOGGER.debug("使用示範模式執行搜尋")
            results, total_count = mock_sdk_instance.search(query, max_results)
        elif WINDOWS_SEARCH_MODE:
            APP_LOGGER.debug("使用 Windows Search API 執行搜尋")
            results, total_count = windows_search_instance.search(
                query, max_results)
        elif SIMPLE_SEARCH_MODE:
            APP_LOGGER.debug("使用簡化搜尋模式執行搜尋")
            results, total_count = simple_windows_search_instance.search(
                query, max_results)
        else:
            APP_LOGGER.debug("使用 Everything SDK 執行搜尋")
            results, total_count = everything_sdk_instance.search(
                query, max_results)

        search_time = time.time() - start_time
        APP_LOGGER.info(
            f"搜尋完成: 找到 {total_count} 個結果，返回 {len(results)} 個，耗時 {search_time:.3f} 秒")

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
        APP_LOGGER.error(f"搜尋過程中發生錯誤: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/status')
def status():
    """檢查 Everything 服務狀態"""
    try:
        APP_LOGGER.debug("檢查 Everything 服務狀態")

        if DEMO_MODE:
            is_running = mock_sdk_instance.is_everything_running()
            message = '示範模式 - 使用模擬資料'
            APP_LOGGER.info("狀態檢查: 示範模式")
        else:
            is_running = everything_sdk_instance.is_everything_running()
            message = 'Everything 正在運行' if is_running else 'Everything 未運行或無法連接'
            APP_LOGGER.info(
                f"狀態檢查: Everything {'運行中' if is_running else '未運行'}")

        """取得應用程式狀態"""
        return jsonify({
            'success': True,
            'everything_available': EVERYTHING_AVAILABLE,
            'demo_mode': DEMO_MODE,
            'windows_search_mode': WINDOWS_SEARCH_MODE if 'WINDOWS_SEARCH_MODE' in globals() else False,
            'simple_search_mode': SIMPLE_SEARCH_MODE if 'SIMPLE_SEARCH_MODE' in globals() else False,
            'search_engine': ('Everything' if EVERYTHING_AVAILABLE else
                              ('Windows Search' if WINDOWS_SEARCH_MODE else
                               ('Simple Search' if SIMPLE_SEARCH_MODE else 'Demo'))),
            'message': message,
        })

    except Exception as e:
        APP_LOGGER.error(f"狀態檢查時發生錯誤: {str(e)}", exc_info=True)
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
    delay = CONFIG['app']['browser_delay']
    host = CONFIG['server']['host']
    port = CONFIG['server']['port']
    url = f'http://{host}:{port}'

    APP_LOGGER.info(f"等待 {delay} 秒後開啟瀏覽器...")
    time.sleep(delay)  # 等待伺服器啟動

    try:
        APP_LOGGER.info(f"開啟瀏覽器: {url}")
        webbrowser.open(url)
    except Exception as e:
        APP_LOGGER.error(f"無法開啟瀏覽器: {e}")
        print(f"⚠ 無法自動開啟瀏覽器，請手動訪問: {url}")


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
    port = CONFIG['server']['port']
    host = CONFIG['server']['host']
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 同样不使用 SO_REUSEADDR 进行真正的检查
        test_socket.bind((host, port))
        test_socket.close()
        return True
    except OSError:
        return False


def main():
    """主函數"""
    APP_LOGGER.info("=" * 60)
    APP_LOGGER.info("🚀 LinkEveryWord Desktop App 啟動")
    APP_LOGGER.info("=" * 60)

    # 設置清理機制
    setup_cleanup()

    # 確保應用程式只執行一個實例 - 多重检查
    APP_LOGGER.info("🔒 檢查應用程式實例...")
    print("🔒 檢查應用程式實例...")

    # 检查 1: Singleton 锁端口
    if not check_single_instance():
        error_msg = "應用程式已經在執行中！(檢測到 Singleton 鎖)"
        APP_LOGGER.error(error_msg)
        print("❌ 應用程式已經在執行中！(檢測到 Singleton 鎖)")
        print("請檢查系統托盤或工作管理員中是否已有此應用程式運行。")
        print("如果確認沒有運行，請等待幾秒後再試。")
        sys.exit(1)

    APP_LOGGER.info("✓ Singleton 鎖檢查通過")
    print("✓ Singleton 鎖檢查通過")

    # 检查 2: Flask 端口是否可用
    if not check_flask_port_available():
        host = CONFIG['server']['host']
        port = CONFIG['server']['port']
        error_msg = f"應用程式已經在執行中！(端口 {port} 被佔用)"
        APP_LOGGER.error(error_msg)
        print(f"❌ 應用程式已經在執行中！(端口 {port} 被佔用)")
        print("另一個應用程式實例正在使用 Web 服務端口。")
        cleanup_lock()
        sys.exit(1)

    APP_LOGGER.info("✓ Web 服務端口檢查通過")
    APP_LOGGER.info("✓ 應用程式實例檢查完成")
    print("✓ Web 服務端口檢查通過")
    print("✓ 應用程式實例檢查完成")

    print("=" * 60)
    print("🔍 Everything Flask 搜尋應用程式")
    print("=" * 60)

    if DEMO_MODE:
        APP_LOGGER.warning("以示範模式運行 - Everything SDK 不可用")
        print("⚠ 以示範模式運行 - Everything SDK 不可用")
        print("要使用完整功能，請:")
        print("1. 安裝 Everything 搜尋引擎")
        print("2. 啟動 Everything")
        print("3. 重新啟動此應用程式")
    else:
        APP_LOGGER.info("Everything SDK 已載入，準備提供搜尋服務")
        print("✓ Everything SDK 已載入")
        print("請確保 Everything 搜尋引擎正在運行")

    host = CONFIG['server']['host']
    port = CONFIG['server']['port']

    APP_LOGGER.info(f"Web 服務將啟動在 {host}:{port}")
    print()
    if CONFIG['app'].get('auto_open_browser', True):
        print("🌐 Web 介面將在瀏覽器中自動開啟")
        # 在新執行緒中開啟瀏覽器
        APP_LOGGER.info("啟動瀏覽器線程")
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
    else:
        print("🌐 Web 介面啟動後不會自動開啟瀏覽器 (已關閉 auto_open_browser)")
    print(f"📍 服務地址: http://{host}:{port}")
    print(f"📊 狀態檢查: http://{host}:{port}/status")
    print()
    print("💡 按 Ctrl+C 停止服務")
    print("=" * 60)

    try:
        # 啟動 Flask 應用程式
        server_config = CONFIG['server']
        APP_LOGGER.info("啟動 Flask Web 服務器...")
        app.run(
            debug=server_config['debug'],
            host=server_config['host'],
            port=server_config['port'],
            use_reloader=server_config['use_reloader']
        )
    except KeyboardInterrupt:
        APP_LOGGER.info("用戶中斷應用程式 (Ctrl+C)")
        print("\n👋 感謝使用 Everything Flask 搜尋應用程式！")
    except Exception as e:
        APP_LOGGER.error(f"應用程式運行時發生錯誤: {e}", exc_info=True)
        print(f"\n❌ 應用程式錯誤: {e}")
        input("按 Enter 鍵退出...")
    finally:
        APP_LOGGER.info("開始清理資源...")
        # 清理锁套接字
        cleanup_lock()
        APP_LOGGER.info("應用程式已完全關閉")
        APP_LOGGER.info("=" * 60)


if __name__ == '__main__':
    main()
