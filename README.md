iqtreeGUI
=========

This repository contains source code and executables for a graphical user interface for [IQ-TREE](http://www.iqtree.org). 
 

Description
===========

iqtreeGUI is a graphical front-end for [IQ-TREE](http://www.iqtree.org). The goal is to implement all features of IQ-TREE 1.6.* graphically. It is under active development and therefore several features are still missing (eg. a GUI for likelihood mapping, topology tests). iqtreeGUI is written in Python3 and executables are available for Windows, Linux and MacOS.


![Screenshot of iqtreeGUI](screenshot.png)
*Figure: iqtreeGUi running on MacOS 10.14*

Feedback appreciated
==============
One of the great things about IQ-TREE is that is has lots of possibilities to combine different parameters and analyses. While iqtreeGUI aims to provide a graphical way to access all these features, it is almost impossible to test every possible combination of parameters IQ-TREE allows. At the moment iqtreeGUI is still under active development. Therefore there may still be a large number of bugs. I am greatful for every bug report I receive. Reporting bugs will help to improve iqtreeGUI.

Features
===========

iqtreeGUI aims to implement all features of IQ-TREE v1.6. It has been tested with v1.6.9 but it may also run with newer versions of IQ-TREE.

Currently implemented features:

- loading alignment files, creating partitions
- specify models for each partition (at the moment only for DNA and AA alignments)  
- perform bootstrap resampling (different settings)
- advanced IQ-TREE settings (starting tree, outgroup, prefix, etc.)
- advanced model selection settings
- advanced tree search settings (no. of starting trees, no. of iterations, ...)
- advanced bootstrap settings
- creating consensus trees
- calculate Robinson-Foulds distances
- generate random trees

Special features of iqtreeGUI:
- load and save configured analyses as XML files for maximum reproducibility


Obtaining and configuring iqtreeGUI
================

**Packaged releases:**

Get the latest release [here] (https://github.com/reslp/iqtreeGUI/releases).
For iqtreeGUI to work you will also need to download and install [IQ-TREE](http://www.iqtree.org).  

Once you have started iqtreeGUI you will have to set the correct path to the IQ-TREE executable. Click on iqtreeGUI -> GUI settings and select the iqtree executable.

**Source code:**

If you would like to try the latest version of iqtreeGUI with additional features (and maybe additional bugs), you can also download the complete source code:

`git clone https://github.com/reslp/iqtreeGUI`

This will download the complete iqtreeGUI repository, meaning that it will download the most recent version of iqtreeGUI. You can then start iqtreeGUI directly from the newly downloaded directory:

`python iqtreegui.py`

**Note:** iqtreeGUI needs Python3 (tested with v.3.6.8). I recommend installing it with [Anaconda] (https://www.anaconda.com).




Building executables
===================

**Note:** These builing instructions are probably outdated and may not work. I will update them soon.


Prerequisites to build from source:

- MacOS X, Linux or Windows operating system
- [python](http://www.python.org) 3.6+, which comes with most Unix like systems
- [pyinstaller](http://www.pyinstaller.org) v3.4, for creating the executable
- git


On MacOS you may execute the `build_all.sh` script to build iqtreeGUI for Linux, Windows and MacOS. 


**Building iqtreeGUI locally from source:**

Make sure to install and configure pyinstaller correctly for your operating system: [pyinstaller install instructions](http://pyinstaller.readthedocs.io/en/stable/installation.html)

1. Clone repository: `git clone https://github.com/reslp/iqtreegui`

The cloned repository already contains everything you need and if you have python installed you may execute iqtreegui with the command: `python iqtreegui.py`

2. To create a stand-alone executable of iqtreegui use pyinstaller: `pyinstaller iqtreegui.spec` for the Linux and Windows version
`pyinstaller iqtreegui_mac.spec` for the Mac version


**Compile Linux and Windows version with Docker on Mac:**

If you have Docker installed you can also compile the Linux and Windows versions within a Docker container:

1. First you have to install the appropriate container: 
`docker pull cdrx/pyinstaller-linux:python3`
or
`docker pull cdrx/pyinstaller-windows:python3`
2. Clone repository: `git clone https://github.com/reslp/iqtreegui`
3. Compile the desired version of iqtreeGUI by executing this in the iqtreeGUI source directory:
`docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux:python3 "apt-get update -y && apt-get install -y python3-tk && pyinstaller --clean -y --dist ./dist/linux --workpath /tmp *.spec"`
or
`docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows:python3`

How to cite?
============
A manuscript is in preparation.


LICENSE
========

iqtreeGUI a graphical user interface for IQ-TREE

Copyright (C) 2019  Philipp Resl

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





