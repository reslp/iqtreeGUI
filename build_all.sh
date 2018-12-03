#!/bin/bash
# This is the script to the Linux and Windows Versions of iqtreeGUI


#Windows build: requires Docker
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows:python2

#Linux Build: requires Docker with custom command
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux:python2 "apt-get update -y && apt-get install -y python-tk && pyinstaller --clean -y --dist ./dist/linux --workpath /tmp *.spec"

#clean up environment
rm *.pyc
