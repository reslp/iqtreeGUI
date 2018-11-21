iqtreeGUI
=========

This repository contains source code and executables for a graphical user interface for [IQ-TREE](http://www.iqtree.org). 

__Note:__ There is a proplem with iqtreeGUI on MacOS Mojave (10.14). Buttons don't appear at all or without labels (although they are there and work). The problem is the underlying Tk framework I am using to create the GUI. I am aware of the problem and a fix is incoming. As a workaround you can resize the affected window slightly and all buttons should re-appear.
 

Description
===========

iqtreeGUI is a graphical front-end for [IQ-TREE](http://www.iqtree.org). The goal is to implement all features of IQ-TREE 1.6.1. It is under active development and therefore several features are still missing (eg. a GUI for likelihood mapping, topology tests). iqtreeGUI is written in Python and executables are available for Windows, Linux and MacOS.

![Screenshot of iqtreeGUI](screenshot.png)
*Figure: iqtreeGUi running on MacOS High Sierra*

A work in progress
==============
One of the great things about IQ-TREE is that is has lots of possibilities to combine different parameters and analyses. While iqtreeGUI aims to provide a graphical way to access all these features, it is almost impossible to test every possible combination of parameters IQ-TREE allows. At the moment iqtreeGUI is still under active developement. Therefore there may still be a large number of bugs. I am greatful for every bug report I receive. Reporting bugs will help to improve iqtreeGUI.

Features
===========

iqtreeGUI aims to implement all features of IQ-TREE v1.6. It has been tested with v1.6.1 but it may also run with newer versions of IQ-TREE.

Currently implemented features:

- loading alignment files, creating partitions
- specify models for each partition (at the moment only for DNA and AA alignments)  
- perform bootstrap resampling
- advanced IQ-TREE settings (starting tree, outgroup, prefix, etc.)
- advanced model selection settings
- advanced tree search settings (no. of starting trees, no. of iterations, ...)
- advanced bootstrap settings
- creating consensus trees
- calculate Robinson-Foulds distances
- generate random trees


Obtaining and configuring iqtreeGUI
================
Executables are available for Linux, MacOS and Windows. The Windows and Linux versions were built using a combination of Docker and pyinstaller. 

For iqtreeGUI to work you will also need to download and install [IQ-TREE](http://www.iqtree.org). Once you have started iqtreeGUI you will have to set the correct path to the IQ-TREE executable. Click on iqtreeGUI -> GUI settings and select the iqtree executable.

Another possibility is to download the complete source code using git clone:

`git clone https://github.com/reslp/iqtreeGUI`

This will download the complete iqtreeGUI repository, meaning that it will download the most recent version of iqtreeGUI. This version may differ from the provided binaries and may contain additional features and bugs.
You can then start iqtreeGUI directly from the newly downloaded directory:

`python iqtreegui.py`




Building executables
===================
If you are on Linux or MacOS you may execute the `build_all.sh` script to build iqtreeGUI for Linux, MacOS and Windows. This requires pyinstaller and Docker to be installed.

**Locally from source:**

If you would like to use the very latest version of iqtreegui you can also build an executable from source code. However, these versions are experimental and may contain additional bugs.

Prerequisites to build from source:

- MacOS X, Linux or Windows operating system
- [python](http://www.python.org) 2.7.8+, which comes with most Unix like systems
- [pyinstaller](http://www.pyinstaller.org) v3.3.1, for creating the executable
- git

Make sure to install and configure pyinstaller correctly for your operating system: [pyinstaller install instructions](http://pyinstaller.readthedocs.io/en/stable/installation.html)

1. Clone repository: `git clone https://github.com/reslp/iqtreegui`

The cloned repository already contains everything you need and if you have python installed you may execute iqtreegui with the command: `python iqtreegui.py`

2. To create a stand-alone executable of iqtreegui use pyinstaller: `pyinstaller iqtreegui.spec`

**Compile Linux and Windows version with Docker on Mac:**

If you have Docker installed you can also compile the Linux and Windows versions within a Docker container:

1. First you have to install the appropriate container: 
`docker pull cdrx/pyinstaller-linux:python2`
or
`docker pull cdrx/pyinstaller-windows:python2`
2. Clone repository: `git clone https://github.com/reslp/iqtreegui`
3. Compile the desired version of iqtreeGUI by executing this in the iqtreeGUI source directory:
`docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux:python2 "apt-get update -y && apt-get install -y python-tk && pyinstaller --clean -y --dist ./dist/linux --workpath /tmp *.spec"`
or
`docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows:python2`

How to cite?
============
A manuscript is in preparation.


LICENSE
========

iqtreeGUI a graphical user interface for IQ-TREE

Copyright (C) 2018  Philipp Resl

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation version 2
of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.





