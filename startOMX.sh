#!/bin/bash

find /home/pi/simpsonstv/videos -name "*.mp4" -print0 | shuf -z | while IFS= read -r -d '' video; do
    filename=$(basename "$video")
    filename_no_ext="${filename%.*}"

    omxplayer \
        --no-osd \
        --no-keys \
        --aspect-mode fill \
        "$video"
done
