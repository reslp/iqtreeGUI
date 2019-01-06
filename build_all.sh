#!/bin/bash
# This script builds the Linux and Windows Versions of iqtreeGUI using Docker


#Windows build: requires Docker
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows:python3

#Linux Build: requires Docker with custom command
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux:python3 "apt-get update -y && apt-get install -y python3-tk && pyinstaller --clean -y --dist ./dist/linux --workpath /tmp *.spec"

