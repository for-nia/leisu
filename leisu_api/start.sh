#!/bin/bash


. /home/yearfu/flask_evn/bin/activate
python -m app.leisu_resty >flash.log 2>&1 &

PID=$!
echo $PID>pid
