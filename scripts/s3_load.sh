#!/bin/bash

cd /root/electiongauge/collector
python s3loader.py >> /var/log/s3loader.log
date >> /var/log/s3loader.log
