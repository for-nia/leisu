#!/bin/bash


python leisu_resty.py $1 &

PID=$!
echo $PID>pid
