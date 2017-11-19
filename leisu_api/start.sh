#!/bin/bash


python leisu_resty.py $1 >flash.log 2>&1 &

PID=$!
echo $PID>pid
