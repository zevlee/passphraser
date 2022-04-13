#!/bin/sh

app=passphraser

version=$(cat ../VERSION)

echo "Running pyinstaller..."

python3 -OO -m PyInstaller $app.spec --noconfirm

mv dist/$app/$app dist/$app/AppRun
sed -i "s/X-AppImage-Version=VERSION/X-AppImage-Version="$version"/g" dist/$app/$app.desktop

wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-$(uname -m).AppImage
chmod +x appimagetool-$(uname -m).AppImage

echo "Running appimagetool..."

ARCH=$(uname -m) ./appimagetool*AppImage dist/$app

rm appimagetool-$(uname -m).AppImage

mv *.AppImage $app-$version-$(uname -m).AppImage

echo $(sha256sum $app-$version-$(uname -m).AppImage) > $app-$version-$(uname -m).AppImage.sha256

echo "Cleaning up..."

rm -r build dist

mv $app-$version-$(uname -m).AppImage* ../..
