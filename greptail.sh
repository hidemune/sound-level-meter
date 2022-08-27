#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "usage:"
    echo "greptail.sh file.log serch_word"
    exit 0
fi

tail -f $1 | grep --line-buffered $2
