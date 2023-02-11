# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
	['../passphraser'],
	pathex=[],
	binaries=[],
	datas=[
		('../gui', 'gui'),
		('../lib', 'lib'),
		('../wordlists', 'wordlists'),
		('../me.zevlee.Passphraser.svg', '.'),
		('../LICENSE', '.'),
		('../VERSION', '.')
	],
	hooksconfig={
		'gi': {
			'icons': ['Adwaita'],
			'themes': ['Adwaita'],
			'module-versions': {
				'Gtk': '4.0'
			}
		}
	},
	hiddenimports=[],
	hookspath=[],
	runtime_hooks=[],
	excludes=[],
	win_no_prefer_redirects=False,
	win_private_assemblies=False,
	cipher=block_cipher,
	noarchive=False
)

pyz = PYZ(
	a.pure,
	a.zipped_data,
	cipher=block_cipher
)

exe = EXE(
	pyz,
	a.scripts,
	a.binaries,
	a.zipfiles,
	a.datas,
	[],
	name='passphraser',
	icon='passphraser.ico',
	debug=False,
	bootloader_ignore_signals=False,
	strip=False,
	upx=True,
	console=False
)
