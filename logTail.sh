#!/bin/bash

#tail -f log.txt

tail -f log.txt | cut -f 4- -d ' '

