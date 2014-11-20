# -*- mode: python -*-
import os

path = os.path.dirname(__file__)
hiddenimports = [
    'subprocess',
    'shlex',
    'servicemanager',
    'win32api',
    'win32service',
    'win32serviceutil',
    'win32event',
    'psutil'
]

a = Analysis(['KennySrv.py'],
             pathex=[path,],
             hiddenimports=hiddenimports,
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='KennySrv.exe',
          debug=True,
          strip=None,
          upx=True,
          console=True)
