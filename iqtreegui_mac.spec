# -*- mode: python -*-
import sys

block_cipher = None

a = Analysis(['iqtreegui.py'],
             pathex=['/Users/sinnafoch/Dropbox/Philipp/iqtreegui3'],
             binaries=[],
             datas=[("./config.txt","."), ("./icon/iqtreegui.gif","./icon/")],
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
          name=os.path.join('dist', 'iqtreeGUI'),
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          icon='./icon/iqtreegui.icns')

# Build a .app if on OS X
#osx needs icns files
if sys.platform == 'darwin':
   app = BUNDLE(exe,
                name='iqtreeGUI.app',
                icon='./icon/iqtreegui.icns',
        		bundle_identifier=None,
         		info_plist={'NSHighResolutionCapable': 'True'},
         )