#!/bin/zsh
# This script builds Linux, Windows and MacOS Versions of iqtreeGUI using cdrx/pyinstallers Docker containers.


#Windows build: requires Docker
docker run -t --rm -v "$(pwd):/src/" cdrx/pyinstaller-windows:python3 "apt-get update -y && apt-get install -y python3-tk && pyinstaller --clean -y --dist ./dist/windows --workpath /tmp *.spec"

#Linux Build: requires Docker with custom command
docker run --rm  -v "$(pwd):/src/" cdrx/pyinstaller-linux:python3 "apt-get update -y && apt-get install -y python3-tk && pyinstaller --clean -y --dist ./dist/linux --workpath /tmp *.spec"

pyinstaller iqtreegui_mac.spec
cp -r tcltk_lib/lib dist/iqtreeGUI.app/Contents/