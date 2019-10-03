binner
=========

binner is a wrapper script to run several metagenome binning programs using Docker.


Supported Binners
===========

Currently binner supports these metagenome binning programs:

CONCOCT: https://github.com/BinPro/CONCOCT

MaxBin2: https://sourceforge.net/projects/maxbin2/

MetaBat: https://bitbucket.org/berkeleylab/metabat/src/master/

blobtools: https://github.com/DRL/blobtools


REQUIREMENTS
============

- MacOS X or other Unix like operating system
- Docker: https://www.docker.com/get-started


INSTALLATION
=======
Assuming Docker is installed and configured properly, it is straightforward to install binner:

```
$ git clone git clone https://github.com/reslp/binner.git
$ cd binner
$ chmod +x binner
$ ./binner -h
Welcome to binner. A script to quickly run metagenomic binning software using Docker.

Usage: ./binner.sh [-v] [-a <assembly_file>] [-f <read_file1>] [-r <read_file2>] [-m maxbin,metabat,blobtools,concoct] [-t nthreads] [[-b /path/to/diamonddb -p /path/to/prot.accession2taxid]]

Options:
	-a <assembly_file> Assembly file in FASTA format (needs to be in current folder)
	-f <read_file1> Forward read file in FASTQ format (can be gzipped)
	-r <read_file2> Reverse read file in FASTQ format (can be gzipped)
	-m <maxbin,metabat,blobtools,concoct> specify binning software to run.
	   Seperate multiple options by a , (eg. -o maxbin,blobtools).
	-t number of threads for multi threaded parts
	-v Display program version

Options specific to blobtools:
	The blobtools container used here uses diamond instead of blast to increase speed.
	Options needed when blobtools should be run. The blobtools container used here uses diamond instead of blast to increase speed.
  	-b full (absolute) path to diamond database
  	-p full (absolute) path to directory containing prot.accession2taxid file provided by NCBI
```




USAGE
========

binner can run multiple binning software. The components of different binners are contained as individual Docker containers. It is not necessary to install them individually. Most metagenomic binners need an assembly and the associated read files used to create the assembly. Binner expects that the Assembly to filter is provided in FASTA format and the read files in FASTQ format. Assembly and reads should be in the same directory. binner should be executed in this directory.

**Running MetaBat with binner:**

```$ binner -a metagenome.fasta -f forward_readfile.fq -r reverse_readfile.fq -m metabat```

**Running MaxBin with binner:**

```$ binner -a metagenome.fasta -f forward_readfile.fq -r reverse_readfile.fq -m maxbin```

**Running CONCOCT with binner:**

```$ binner -a metagenome.fasta -f forward_readfile.fq -r reverse_readfile.fq -m concoct```

**Running blobtools with binner:**

Blobtools requires blast results to get the taxonomic identity (by using NCBI taxids) of individual contigs in the assembly. binner creates these blast results with diamond blastx. However you will need a diamond based sequence database (typically the NCBI nr database). If you don't already have one you can set it up like this.

```
$ wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz
$ docker run --rm reslp/diamond diamond makedb --in nr.gz -d nr
```

Using this command has the advantage that the database is compatible with the used diamond Docker container used in binner which is reslp/binner.

Because diamond cannot output taxids directly binner maps the ids retrieved by diamond blastx to NCBI taxids. This is done using the file `prot.accession2taxid` provided by NCBI. If you don't have this file already download by running the following commands:

```
$ wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz
$ gunzip prot.accession2taxid.gz
```

```$ binner -a metagenome.fasta -f forward_readfile.fq -r reverse_readfile.fq -m metabat -b /path/to/diamonddb -p /path/to/prot.accession2taxid```




COPYRIGTH AND LICENSE
=====================

Copyright (C) 2019 Philipp Resl

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program in the file LICENSE. If not, see http://www.gnu.org/licenses/.
