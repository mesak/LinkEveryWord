"""
Everything Flask 搜尋應用程式 - 打包版本入口點
專為 PyInstaller 打包優化
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


# 嘗試載入 Everything SDK 並建立實例
everything_sdk_instance = None
mock_sdk_instance = None

try:
    from everything_sdk import get_everything_sdk
    EVERYTHING_AVAILABLE = True
    DEMO_MODE = False
    # 建立 SDK 實例 (單例)
    everything_sdk_instance = get_everything_sdk()
    print("✓ Everything SDK 載入成功")
except Exception as e:
    EVERYTHING_AVAILABLE = False
    DEMO_MODE = True
    print(f"⚠ Everything SDK 載入失敗: {e}")
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
        else:
            results, total_count = everything_sdk_instance.search(query, max_results)

        # 轉換結果為字典格式
        results_data = [result.to_dict() for result in results]

        return jsonify({
            'success': True,
            'query': query,
            'results': results_data,
            'total_count': total_count,
            'displayed_count': len(results_data),
            'demo_mode': DEMO_MODE
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
            results, total_count = everything_sdk_instance.search(query, max_results)

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


def main():
    """主函數"""
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


if __name__ == '__main__':
    main()
