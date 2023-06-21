# -*- mode: python ; coding: utf-8 -*-

import os.path
import platform
import shutil

from PyInstaller.utils.hooks import collect_data_files, copy_metadata

datas = []
datas += collect_data_files('torch')
datas += copy_metadata('tqdm')
datas += copy_metadata('torch')
datas += copy_metadata('regex')
datas += copy_metadata('asyncio')
datas += copy_metadata('rich')
datas += copy_metadata('requests')
datas += copy_metadata('packaging')
datas += copy_metadata('filelock')
datas += copy_metadata('numpy')
datas += copy_metadata('tokenizers')
datas += [('./inference.py', '.')]
datas += [('./python3.8', '.')]
datas += [('./ss_model=resunet30,querynet=at_soft,data=full.yaml', '.')]
datas += [('./pretrained.ckpt', '.')]

block_cipher = None

a = Analysis(
    ['USS-GUI.py'],
    pathex=[],
    binaries=[
    ('/Users/clamours/anaconda3/envs/uss/lib/python3.8/site-packages/torch/lib/libiomp5.dylib', 'functorch/.dylibs/')
    ],
    datas=datas,
    hiddenimports=[],
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
    icon='./assets/USS-GUI.ico',
    exclude_binaries=True,
    name='USS_GUI',
    debug=True,
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
    upx=False,
    upx_exclude=[],
    name='USS-GUI',
)
app = BUNDLE(
    coll,
    name='USS-GUI.app',
    icon='./assets/USS-GUI.icns',
    bundle_identifier='com.clamours.uss-gui',
    version='0.0.1',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True'
    }
)