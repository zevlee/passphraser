# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
	['../passphraser'],
	pathex=[],
	binaries=[],
	datas=[
		('../lib/__init__.py', 'lib'),
		('../lib/passphraser.py', 'lib'),
		('../gui/menu.xml', 'gui'),
		('../passphraser.svg', '.'),
		('../wordlists/eff_large.txt', 'wordlists'),
		('../wordlists/eff_short_1.txt', 'wordlists'),
		('../wordlists/eff_short_2.txt', 'wordlists'),
		('../LICENSE', '.'),
		('../VERSION', '.'),
		('passphraser.desktop', '.')
	],
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
	debug=False,
	bootloader_ignore_signals=False,
	strip=False,
	upx=True,
	console=False
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
