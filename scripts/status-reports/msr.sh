#!/bin/sh

# ./main.sh msr jira.csv 201804 [outfile-prefix]
./main.py $1 $2 $3 && pandoc -f markdown -t docx -o ./output/$4msr-$3.docx ./output/msr-$3.md
