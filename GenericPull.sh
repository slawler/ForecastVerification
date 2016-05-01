#!/bin/bash

d=$(date +"%Y-%m-%d")
period=".00z.grb"
dperiod=$d$period

echo $dperiod

find -name '*'$dperiod > /home/slawler/Desktop/MARFC/GribTesting/MARFC_FORECAST_$dperiod.txt

mkdir /home/slawler/Desktop/MARFC/GribTesting/$dperiod

for file in `cat FORECAST_$dperiod.txt`; do cp "$file" /home/slawler/Desktop/MARFC/GribTesting/$dperiod; done

#get *2016-02-15.00z.grb

