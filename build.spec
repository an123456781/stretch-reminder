# -*- mode: python ; coding: utf-8 -*-
import os
import customtkinter

_ctk_dir = os.path.dirname(customtkinter.__file__)

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("assets/icon.ico", "assets"),
        (_ctk_dir, "customtkinter"),
    ],
    hiddenimports=[
        "customtkinter",
        "pystray._win32",
        "winotify",
        "PIL",
        "PIL.Image",
        "PIL.ImageDraw",
        "winsound",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="StretchReminder",
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon="assets/icon.ico",
)
