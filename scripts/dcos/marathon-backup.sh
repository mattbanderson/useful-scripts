#!/bin/sh

DATE=`date +%Y-%m-%d`
MARATHON_ROOT_URL=$1

mkdir -p ./marathon-backup
curl -s $MARATHON_ROOT_URL/v2/apps > ./marathon-backup/marathon-backup-raw-${DATE}.json
cat ./marathon-backup/marathon-backup-raw-${DATE}.json | jq '.[] | del(.[].version)' > ./marathon-backup/marathon-backup-stripped-${DATE}.json