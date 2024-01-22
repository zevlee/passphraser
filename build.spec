# -*- mode: python ; coding: utf-8 -*-

from argparse import ArgumentParser
from platform import system

parser = ArgumentParser()
parser.add_argument("--binary", action="store_true")
options = parser.parse_args()

a = Analysis(
    ['passphraser.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('LICENSE', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={
        'gi': {
            'icons': ['Adwaita'],
            'themes': ['Adwaita'],
            'module-versions': {
                'Gtk': '4.0'
            }
        }
    },
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

if system() == "Linux":
    if not options.binary:
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
            console=False,
            disable_windowed_traceback=False,
            argv_emulation=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None,
        )
        coll = COLLECT(
            exe,
            a.binaries,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name='passphraser',
        )
    else:
        exe = EXE(
            pyz,
            a.scripts,
            a.binaries,
            a.datas,
            [],
            name='passphraser',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            upx_exclude=[],
            runtime_tmpdir=None,
            console=False,
            disable_windowed_traceback=False,
            argv_emulation=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None,
        )
elif system() == "Darwin":
    if not options.binary:
        exe = EXE(
            pyz,
            a.scripts,
            [],
            exclude_binaries=True,
            name='passphraser',
            icon='macos/me.zevlee.Passphraser.icns',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            console=False,
            disable_windowed_traceback=False,
            argv_emulation=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None,
        )
        coll = COLLECT(
            exe,
            a.binaries,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name='passphraser',
        )
        app = BUNDLE(
            coll,
            name='Passphraser.app',
            icon='macos/me.zevlee.Passphraser.icns',
            bundle_identifier=None,
            version=None,
        )
    else:
        exe = EXE(
            pyz,
            a.scripts,
            a.binaries,
            a.datas,
            [],
            name='passphraser',
            icon='macos/me.zevlee.Passphraser.icns',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            upx_exclude=[],
            runtime_tmpdir=None,
            console=False,
            disable_windowed_traceback=False,
            argv_emulation=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None,
        )
elif system() == "Windows":
    if not options.binary:
        exe = EXE(
            pyz,
            a.scripts,
            [],
            exclude_binaries=True,
            name='passphraser',
            icon='windows/me.zevlee.Passphraser.ico',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            console=False,
            disable_windowed_traceback=False,
            argv_emulation=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None,
        )
        coll = COLLECT(
            exe,
            a.binaries,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name='passphraser',
        )
    else:
        exe = EXE(
            pyz,
            a.scripts,
            a.binaries,
            a.datas,
            [],
            name='passphraser',
            icon='windows/me.zevlee.Passphraser.ico',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            upx_exclude=[],
            runtime_tmpdir=None,
            console=False,
            disable_windowed_traceback=False,
            argv_emulation=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None,
        )
