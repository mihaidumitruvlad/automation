#!/bin/bash
echo Capturing image
fswebcam -q -d /dev/video0 --no-banner --no-timestamp --no-title --no-subtitle --no-info --no-underlay -p YUYV -r 640x480 -D 2 -S 4 -F 10 --png 9 -s brightness=70% -s contrast=50% -s gamma=50% -s sharpness=100% -s saturation=0% --crop 310x89,135x360 --save "/var/www/html/output/image.png"
