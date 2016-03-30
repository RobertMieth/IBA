# -*- mode: python -*-

block_cipher = None


a = Analysis(['IBAv2beta.py'],
             pathex=['C:\\Users\\RobertM\\Desktop\\solandeo_IBA_v2.0\\release 2.0beta'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='IBAv2beta',
          debug=False,
          strip=False,
          upx=True,
          console=True )
