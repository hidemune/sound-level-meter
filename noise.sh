#! /bin/bash

CURDIR=`dirname $0`
echo $CURDIR
cd $CURDIR

python3 noise_level_measurement.py &

tail -f log.txt

