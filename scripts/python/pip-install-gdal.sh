#! /bin/bash

pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')

