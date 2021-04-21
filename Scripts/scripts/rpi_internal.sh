#!/bin/bash
temp="$(/opt/vc/bin/vcgencmd measure_temp)"
IFS="=" read -r -a tmp_temp <<< "$temp"
IFS="'" read -r -a tmp_temp_nr <<< "${tmp_temp[1]}"
temp="${tmp_temp_nr[0]}"
ts=`date '+%d-%b-%Y %H:%M'`
echo "{\"timestamp\": \"$ts\", \"temperature\": \"${temp[0]}\"}" > /var/www/html/output/internal_params.json
echo "Internal CPU temperature ${temp}*C. JSON updated"
