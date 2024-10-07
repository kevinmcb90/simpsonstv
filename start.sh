#!/bin/bash

mpv \
  --input-ipc-server=/tmp/mpvsocket \
  --osd-duration=5000 \
  --osd-font-size=80 \
  --osd-playing-msg='${filename/no-ext}' \
  --osd-on-seek=msg-bar \
  --shuffle \
  /home/pi/simpsonstv/videos/*.mp4
