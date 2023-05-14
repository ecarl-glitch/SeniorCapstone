#!/bin/bash

# executes first file of qiime commands for each trial
# enters each trial, makes a directory for QIIME 2 output and calls a shell file containing QIIME commands
for i in $(seq 1 4);
do
    echo "Trial" $i
    cd trial$i
    mkdir qiimeOutput
    sh qiime1.sh
    cd ../
done

# for second file of qiime commands, code is slightly modified (shown below)

#for i in $(seq 1 4);
#do
    #echo "Trial" $i
    #cd trial$i
    #sh qiime2.sh
    #cd ../
#done
