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
			'module-versions': {
				'Gtk': '3.0'
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
	[],
	exclude_binaries=True,
	name='passphraser',
	icon='passphraser.icns',
	debug=False,
	bootloader_ignore_signals=False,
	strip=False,
	upx=True,
	console=False,
	codesign_identity='',
	entitlements_file='entitlements.plist'
)

coll = COLLECT(
	exe,
	a.binaries,
	a.zipfiles,
	a.datas,
	strip=False,
	upx=True,
	upx_exclude=[],
	name='passphraser'
)

app = BUNDLE(
	coll,
	name='Passphraser.app',
	icon='passphraser.icns',
	bundle_identifier='me.zevlee.Passphraser',
	version='VERSION'
)
