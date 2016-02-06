#!/bin/bash

start_ts=1454191428
interval=3600
nbproc=24

for i in `seq 0 $nbproc`;
do
    start_tmp=$(($start_ts+($i*$interval)))
    end_tmp=$(($start_tmp+$interval))
    python MyBGPStream.py -s $start_tmp -e $end_tmp &
done

