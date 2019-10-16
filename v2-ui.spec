# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['v2-ui.py'],
             pathex=['/root/v2-ui'],
             binaries=[],
             datas=[('static/axios/*', 'static/axios/'), ('static/base64/*', 'static/base64/'),
             ('static/clipboard/*', 'static/clipboard/'), ('static/css/*', 'static/css/'), ('static/js/*', 'static/js/'),
             ('static/qrcode/*', 'static/qrcode/'), ('static/qs/*', 'static/qs/'),
             ('translations/en/LC_MESSAGES/*', 'translations/en/LC_MESSAGES/'),
             ('translations/es/LC_MESSAGES/*', 'translations/es/LC_MESSAGES/'),
             ('translations/zh/LC_MESSAGES/*', 'translations/zh/LC_MESSAGES/'),
             ('templates/common/*', 'templates/common'),
             ('templates/v2ray/*', 'templates/v2ray'),
             ('templates/index.html', 'templates/'),
             ('./template_config.json', '.'),
             ('v2-ui.service', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='v2-ui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='v2-ui')
