#!/bin/bash

cd /opt/egauge/electiongauge/collector
/root/epd-7.1-2-rh5-x86/bin/python s3loader.py >> /var/log/s3loader.log 2>> /var/log/s3loader.log

cd /opt/egauge/electiongauge/visualizer
/root/epd-7.1-2-rh5-x86/bin/python timeline.py >> /var/log/s3loader.log 2>> /var/log/s3loader.log
/root/epd-7.1-2-rh5-x86/bin/python parallel_coords.py >> /var/log/s3loader.log 2>> /var/log/s3loader.log

date >> /var/log/s3loader.log


