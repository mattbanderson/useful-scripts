#!/bin/bash

USAGE="
$(basename "$0") <marathon-root-url> -- Creates a backup of all Marathon configurations for a DC/OS cluster

where:
    <marathon-root-url>  The Marathon hostname/IP address and port; e.g. 192.168.0.1:8080
"

if [ "$1" = "" ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "$USAGE"
  exit 0
fi

DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="./output"
MARATHON_ROOT_URL=$1

echo "Starting backup, configuration files will be placed in $OUTPUT_DIR..."
mkdir -p $OUTPUT_DIR

# Get all configs from Marathon API
curl -s "$MARATHON_ROOT_URL/v2/apps" > "./output/marathon-backup-raw-${DATE}.json"

# Pipe configs through jq to remove unwanted properties and output to file
echo "Creating full configuration file..."
jq '.[] | del(.[].version) | del(.[].versionInfo) | del(.[].tasksStaged) | del(.[].tasksRunning) | del(.[].tasksHealthy) | del(.[].tasksUnhealthy) | del(.[].deployments) | del(.[].executor)' < "./output/marathon-backup-raw-${DATE}.json" > "./output/marathon-backup-full-cleaned-${DATE}.json"

configs=$(cat "./output/marathon-backup-full-cleaned-${DATE}.json")

# Get unique top-level app group identifiers
#IFS=" " read -r -a appGroups <<< $(echo $configs | jq -r '[.[] | .id | split("/")[1]] | flatten | unique | .[]')
appGroups=($(echo $configs | jq -r '[.[] | .id | split("/")[1]] | flatten | unique | .[]'))

# Create app-specific config files, which are subsets of the full config (helpful for organization or if a full backup is unnecessary
echo "Creating app-specific configuration files..."

for i in "${appGroups[@]}"
do
   : 
   echo $configs | jq '.[] | select(.id | contains("'"$i"'"))' > "./output/$i.json"
done

echo "Backup complete."
