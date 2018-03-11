#!/bin/sh

wget https://github.com/jjhelmus/berryconda/releases/download/v2.0.0/Berryconda3-2.0.0-Linux-armv7l.sh -O ~/barryconda.sh
bash ~/miniconda.sh

conda install -c rpi opencv
pip install pyyaml
pip install git+https://github.com/dpallot/simple-websocket-server.git

sudo apt-get install apache2 -y

echo 'all done.'
