#!/bin/bash


python -m app.leisu_resty >flash.log 2>&1 &

PID=$!
echo $PID>pid
