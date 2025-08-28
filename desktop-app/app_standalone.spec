# -*- mode: python ; coding: utf-8 -*-

import os

# 獲取當前目錄
current_dir = os.path.abspath('.')

a = Analysis(
    ['app_standalone.py'],
    pathex=[current_dir],
    binaries=[
        # 包含 Everything DLL 檔案
        ('dll/Everything64.dll', 'dll'),
        ('dll/Everything32.dll', 'dll'),
    ],
    datas=[
        # 包含 templates 資料夾
        ('templates', 'templates'),
        # 包含其他必要檔案
        ('README.md', '.'),
        
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'everything_sdk',
        'mock_everything',
        'ctypes',
        'datetime',
        'struct',
        'threading',
        'webbrowser',
        'time'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EverythingFlaskSearch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='favicon.ico',  # 如果有圖示檔案，可以在這裡指定
    version='version_info.txt',
)
