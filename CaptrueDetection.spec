# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['CaptrueDetection.py'],
    pathex=['D:\\ProgramData\\anaconda3\\envs\\yolo7\\Lib\\site-packages'],
    binaries=[('utils/torch_utils.py','.'),('D:\\ProgramData\\anaconda3\\envs\\yolo7\\Lib\\site-packages\\torch\\lib\\caffe2_nvrtc.dll', '.')],
    datas=[('.\\weights','weights'),('traced_model.pt','traced_model.pt'),('.\\utils','utils')],
    hiddenimports=['models.yolo'],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CaptrueDetection',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
