# -*- mode: python -*-

from kivy_deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, hookspath, runtime_hooks

all_hooks = runtime_hooks()
all_hooks.append('force_utf8.py')

block_cipher = None

a = Analysis(['main.py'],
             pathex=['./'],
             datas=[],
             runtime_hooks=all_hooks,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             **get_deps_minimal(
                 audio=None,
                 camera=None,
                 video=None,
                 spelling=None
                 )
             )
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='SiegeMinion 6.2.5',
          debug=False,
          strip=False,
          upx=True,
          console=False, 
          icon='.//ui//images//Blue_Siege_MinionSquare2.ico',
          version='version.rc')
coll = COLLECT(exe,
               Tree('.//'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='SiegeMinion')
