#!/bin/sh

# ./msr.sh msr jira.csv 201804 pe-
./main.py $1 $2 $3 $4 && pandoc -f markdown -t docx -o ./output/$4msr-$3.docx ./output/$4msr-$3.md
