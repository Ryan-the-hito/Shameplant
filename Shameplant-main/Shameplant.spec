# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

__version__ = '1.0.6'

info_plist = {
    'LSUIElement': True,
    #'LSBackgroundOnly': True,
    'NSHumanReadableCopyright': 'Copyright © 2025 Yixiang SHEN. All rights reserved.',
    'CFBundleVersion': '2',
    "LSApplicationCategoryType": "public.app-category.productivity",
    "com.apple.security.app-sandbox": True,
    "NSPrincipalClass": "NSApplication",
    "LSMinimumSystemVersion": "15.0",
    "ITSAppUsesNonExemptEncryption": False,
}

a = Analysis(
    ['Shameplant.py'],
    pathex=['/Users/ryanshenefield/Downloads/Shameplant.py'],
    binaries=[],
    datas=[('Shameplant_menu.icns', '.'), ('Shameplant_desk.icns', '.'), ('Shameplant_menu.png', '.'), ('wechat50.png', '.'), ('wechat20.png', '.'), ('wechat10.png', '.'), ('wechat5.png', '.'), ('alipay50.png', '.'), ('alipay20.png', '.'), ('alipay10.png', '.'), ('alipay5.png', '.'), ('ReLa.txt', '.'), ('DockRe.txt', '.'), ('Screen.txt', '.'), ('Screen2.txt', '.'), ('minus.png', '.'), ('plus.png', '.'), ('promote.png', '.'), ('access1.png', '.'), ('access2.png', '.'), ('access3.png', '.'), ('dock9.gif', '.'), ('com.ryanthehito.shameplant.plist', '.')],
    hiddenimports=['subprocess', 'AppKit'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Shameplant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Shameplant',
)
app = BUNDLE(
    coll,
    name='Shameplant.app',
    icon='Shameplant_desk.icns',
    info_plist=info_plist,
    bundle_identifier='com.ryanthehito.shameplant',
    version=__version__,
)
