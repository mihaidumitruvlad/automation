#!/bin/bash
#Power daily consumption threshold
thresh=10
#Margin difference accepted compared to last value (absolute difference between current and last value)
margin_value=9
sleep=9
unreadable_max_delta=30
max_retries=5
retries=$(<data/retries.txt)

if [ $retries == 1 ] ; then
  rm /var/www/html/output/data.txt
fi

ts=`date '+%d-%b-%Y %H:%M'`

echo "$ts - Process starting (attempt $retries)" >> /var/www/html/output/data.txt
echo "$ts - Process starting (attempt $retries)"

#email to alert
email="mihaidumitruvlad@gmail.com,alexandra.brad@yahoo.com"

echo "$ts - Starting image processor" >> /var/www/html/output/data.txt
echo "$ts - Starting image processor"
python3 getDigits.py "/var/www/html/output/image.png" data/digits.txt "/var/www/html/output/power.json"
power=$(<data/digits.txt)
last_power=$(<data/last_ghseet_val.txt)
abs_diff=$((power-last_power))

ts=`date '+%d-%b-%Y %H:%M'`
echo "$ts - Value retrieved: '${power}'. Total character length '${#power}'. Last power value '${last_power}'. Absolute difference: '${abs_diff#-}'. Accepted margin is '${margin_value}'; margin when unreadable is '${unreadable_max_delta}'." >> /var/www/html/output/data.txt
echo "$ts - Value retrieved: '${power}'. Total character length '${#power}'. Last power value '${last_power}'. Absolute difference: '${abs_diff#-}'. Accepted margin is '${margin_value}'; margin when unreadable is '${unreadable_max_delta}'."
if [[ ("${#power}" -ge 6 || "${power}" -le 0 || ( "${abs_diff#-}" -gt "${margin_value}" && "${last_power}" -gt 0)) && "${retries}" -lt "${max_retries}"  ]] ; then
  echo "$ts - Wrong value, waiting 8 seconds to switch back to current consumption" >> /var/www/html/output/data.txt
  echo "$ts - Wrong value, waiting 8 seconds to switch back to current consumption"
  echo $((retries+1)) > data/retries.txt
  sleep $sleep
  ./webcam.sh
  $0
  exit
elif [[ "${#power}" -lt 6 && "${power}" -gt "${last_power}" && "${power}" -gt 0 && "${last_power}" -gt 0 && "${abs_diff#-}" -le "${unreadable_max_delta}" ]] ; then
  echo "1" > data/retries.txt
  echo "$ts - Pushing information to google sheets" >> /var/www/html/output/data.txt
  echo "$ts - Pushing information to google sheets"
  python3 push2gsheets.py keys/api_key.json data/digits.txt "/var/www/html/output/push2gsheets.json"

  daykw=$(($(<data/day_kw.txt)))
  email_sent=$(<data/email_sent_track.txt)
  ts=`date '+%d-%b-%Y %H:%M'`  
  echo "$ts - Current day power consumption ${daykw}" >> /var/www/html/output/data.txt
  echo "$ts - Current day power consumption ${daykw}"
  if [ $daykw -ge $thresh ] ; then
    if [ $email_sent == "0" ] ; then
      echo "$ts - Power daily threshold of ${thresh} reached. Sending e-mail to ${email}" >> /var/www/html/output/data.txt
      echo "$ts - Power daily threshold of ${thresh} reached. Sending e-mail to ${email}"
      python3 sendmail.py $email "Daily power limit reached" "Current power index: ${power}kW<br>Threshold: ${thresh}kW<br>Current day power consumption: ${daykw}kW"
      echo 1 > data/email_sent_track.txt
    else
      echo "$ts - E-mail already sent today." >> /var/www/html/output/data.txt
      echo "$ts - E-mail already sent today."
    fi
  else
    echo "$ts - Current daily consumption is: $daykw, which is below daily threshold. Not sending e-mail." >> /var/www/html/output/data.txt
    echo "$ts - Current daily consumption is: $daykw, which is below daily threshold. Not sending e-mail."
  fi
else
  echo "1" > data/retries.txt
  echo "$ts - Could not read display or last value pushed to google sheets is still the same. No further action is performed." >> /var/www/html/output/data.txt
  echo "$ts - Could not read display or last value pushed to google sheets is still the same. No further action is performed."
fi
