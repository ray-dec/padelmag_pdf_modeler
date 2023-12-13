# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('main.py', 'Scripts')],
    hiddenimports=['altgraph', 'beautifulsoup4', 'certifi', 'cffi', 'charset-normalizer', 'cryptography', 'idna', 'numpy', 'packaging', 'pandas', 'pdfminer.six', 'pdfplumber', 'pefile', 'Pillow', 'pyarrow', 'pycparser', 'pyinstaller', 'pyinstaller-hooks-contrib', 'pypdfium2', 'python-dateutil', 'pytz', 'pywin32-ctypes', 'requests', 'six', 'soupsieve', 'tzdata', 'Unidecode','unidecode', 'urllib3','pyarrow.vendored.version'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    win_no_prefer_redirects=False,
    win_private_assemblies=False
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
