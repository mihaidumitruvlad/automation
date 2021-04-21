#!/bin/bash
cd "$(dirname "$0")/scripts"

case $1 in

  sensor)
    ./sensor.sh
    ;;

  internal)
    ./rpi_internal.sh
    ;;

  power)
    ./webcam.sh
    ./power.sh
    ;;

  *)
    printf "Please add the following options: 'sensor', 'internal' or 'power' as scripts to be triggered\r\n"
    ;;
esac
