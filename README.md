![Alt text](https://raw.githubusercontent.com/zevlee/passphraser/main/passphraser.svg)

# Passphraser

Passphraser is a password generator that accepts any text file and treats each word as a possible input. So a text file like this...
```
alpha bravo
charlie delta echo
foxtrot
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
2. Go to your folder for MSYS2 and run ``mingw64.exe``. The following commands will be executed in the console that appears.
3. Install git.
```
pacman -S git
```
4. Clone this repository.
```
git clone https://github.com/zevlee/passphraser.git
```
5. Enter the ``windows`` directory.
```
cd passphraser/windows
```
6. Run ``bootstrap.sh`` to install any missing dependencies.
```
chmod +x bootstrap.sh && ./bootstrap.sh
```
7. Run ``build.sh``.
```
chmod +x build.sh && ./build.sh
```

### Building on macOS
1. Homebrew is needed to install PyGObject. [Get it from the Homebrew website.](https://brew.sh)
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
Enable code signing by adding the Common Name of the certificate as the first argument. Without this, adhoc signing will be used.
```
./build.sh "Developer ID Application: Name Here (TEAMIDHERE)"
```
Enable notarization by also adding the name of a stored keychain profile.
```
./build.sh "Developer ID Application: Name Here (TEAMIDHERE)" "keychain-profile-here"
```
Notarization can alternatively be enabled by adding Apple ID, Team ID, and an app-specific password as subsequent arguments.
```
./build.sh "Developer ID Application: Name Here (TEAMIDHERE)" "appleid@here.com" "TEAMIDHERE" "pass-word-goes-here"
```

### Building on Linux
1. Ensure PyGObject is installed.
2. Clone this repository.
```
git clone https://github.com/zevlee/passphraser.git
```
3. Enter the ``linux`` directory.
```
cd passphraser/linux
```
4. Run ``bootstrap.sh`` to install any missing dependencies.
```
chmod +x bootstrap.sh && ./bootstrap.sh
```
5. Run ``build.sh``.
```
chmod +x build.sh && ./build.sh
```
