# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['app.py'],
             pathex=[],
             binaries=[],
             datas=[('dbsqlcli/dbsqlclirc', 'dbsqlcli')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

# Avoid warning
for b in a.binaries:
    found = "pyarrow/lib.cpython-39-darwin.so" in b[1] 
    if found:
        a.binaries.remove(b)
        break
       

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
