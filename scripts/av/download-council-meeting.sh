#!/bin/sh

set -e

# check if enough args
if [ $# -lt 1 ]; then
    echo 1>&2 "Usage: $0 <MMDDYY>"
    exit 2
fi

FLV_FILE=cc$1.flv
MP4_FILE=cc$1.mp4
MP3_FILE=cc$1.mp3

wget http://video.ci.beavercreek.oh.us/Videos/$FLV_FILE
ffmpeg -i $FLV_FILE -vcodec libx264 -acodec copy $MP4_FILE
ffmpeg -i $MP4_FILE -b:a 192K -vn $MP3_FILE
rm -f $FLV_FILE
