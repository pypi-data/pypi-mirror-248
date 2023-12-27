# PythonCliPipeline

This documentation shows how to pack a Python CLI Application to publish it as a package on Pypi, to make it available using `pip install` and also for chocolatey, a windows package manager, to make it available using `choco install`

## Requirements
* [Python](https://www.python.org/downloads/)
* Click
* Pyinstaller
    ```python
    pip install pyinstaller
    ```
* [Chocolatey](https://chocolatey.org/install)
* twine
    ```python
    pip install twine
    ```
* [Pypi account](https://pypi.org/account/register/)
* [Pypi Token](https://pypi.org/manage/account/token/)
* [Chocolatey account](https://community.chocolatey.org/account/Register)

## Producting an executable
Run
```bash
pyinstaller --onefile <filename.py>
```

## Pypi Publishing

1. You need a your <cli-tool>.py and a setup.py.

The setup.py should look like:

```python

from setuptools import setup

setup(
    name='<cli-name>',
    version='1.0.0',
    py_modules=['<cli_module_name>'],
    install_requires=['Click', '<any_other_requirements_here>', ],
    entry_points={
        'console_scripts': [
            '<cli-name> = <cli-name>:cli'
        ]
    })

```

2. Run twine:

```bash
twine upload dist/* --username __token__ --password "token_here"
```

## Chocolatey Publishing

You need a <cli-name>.spec and a <cli-name>.nuspec


.spec file:

```spec
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['<cli-name>.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='<cli-name>',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

```

* Run:

```bash
pyinstaller <file-name>.spec
```

* Run:

```bash
choco pack
```

Chocolatey will base itself in the .nuspec:

```nuspec

<?xml version="1.0"?>
<package >
  <metadata>
    <id><cli-name></id>
    <version>1.0.0</version>
    <title>CLI Name</title>
    <authors>Example Author</authors>
    <owners>Example Owner</owners>
    <projectUrl>https://github.com/daflongustavo/<cli-name></projectUrl>
    <iconUrl>https://avatars.githubusercontent.com/u/106110465?v=4</iconUrl>
    <requireLicenseAcceptance>false</requireLicenseAcceptance>
    <description>Teste para aprender a publicar CLI tools no Chocolatey</description>
    <releaseNotes>Sandbox version</releaseNotes>
    <copyright>Copyright (c) 2023</copyright>
    <tags>python, exercice, poc</tags>
  </metadata>
  <files>
    <file src="./tools/<cli-name>.exe" target="tools" />
  </files>
</package>

```

Now you run:

```bash
choco push <cli-name>.<version-number>.nupkg -s https://chocolatey.org/ --api-key <api-key-here>
```
