#!/bin/sh

wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"

conda install -c conda-forge opencv
pip install pyyaml
pip install git+https://github.com/dpallot/simple-websocket-server.git

sudo apt-get install apache2

echo 'all done.'
