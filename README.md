![Alt text](https://raw.githubusercontent.com/zevlee/passphraser/main/passphraser.svg)

# Passphraser

Phrase-based password generator that can use your own list of words. Available on Windows, macOS, and Linux.

Passphraser accepts any text file and treats each line as a possible input. So a text file like this...
```
alpha
bravo
charlie
delta
echo
```
...will result in a generated password like this with the default settings.
```
Delta-Charlie-6-Bravo-Charlie-Alpha-Echo
```

The included word lists are derived from the EFF's word lists found [here](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases) ([archive](https://web.archive.org/web/20210505043502/https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases)).

### Signing Key
[Download my signing key here.](https://zevlee.me/sign.txt)

### Building on Windows
1. MSYS2 is needed to build on Windows. [Get it from the MSYS2 website.](https://www.msys2.org/)
2. Download a copy of this repository, then extract it to your home folder for MSYS2 (Usually ``C:\msys64\home\<user>``).
3. Go to your folder for MSYS2 (Usually ``C:\msys64``) and run ``mingw32.exe``. The following commands will be executed in the console that appears.
4. Enter the ``windows`` directory of the extracted repository.
```
cd passphraser/windows
```
5. Run ``bootstrap.sh`` to install any missing dependencies.
```
chmod +x bootstrap.sh && ./bootstrap.sh
```
6. Run ``build.sh``.
```
chmod +x build.sh && ./build.sh
```

### Building on macOS
1. Brew is needed to install PyGObject. [Get it from the brew website.](https://brew.sh)
2. Clone this repository.
```
git clone https://github.com/zevlee/passphraser.git
```
3. Enter the ``macos`` directory.
```
cd passphraser/macos
```
4. Run ``bootstrap.sh`` to install any missing dependencies.
```
chmod +x bootstrap.sh && ./bootstrap.sh
```
5. Run ``build.sh``.
```
chmod +x build.sh && ./build.sh
```

### Building on Linux

1. Clone this repository
```
git clone https://github.com/zevlee/passphraser.git
```
2. Enter the ``linux`` directory
```
cd passphraser/linux
```
3. Run ``bootstrap.sh`` to install pyinstaller via pip if you haven't already. Ensure PyGObject is also installed.
```
chmod +x bootstrap.sh && ./bootstrap.sh
```
4. Run ``build.sh``.
```
chmod +x build.sh && ./build.sh
```
