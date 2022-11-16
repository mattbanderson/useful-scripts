#!/bin/bash

for file in *.json; do cat $file | jq > "$file.pretty"; done
rm *.json
rename 's/.json.pretty/.json/' *.pretty