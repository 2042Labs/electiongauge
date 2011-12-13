#!/bin/sh

dropdb egauge
createdb -T template_postgis egauge
django-admin.py syncdb