import cv2
from pytesseract import image_to_string
from datetime import datetime
import os
import numpy as np
import os.path
from os import path
import sys

ts = datetime.now().strftime('%d-%b-%Y %H:%M')
current_hour = int(datetime.now().strftime('%H'))

path_to_image, image_name = os.path.split(sys.argv[1])
path_to_image = path_to_image + '/'
cfg = "--oem 0 --psm 8 -c tessedit_char_whitelist=0123456789 -l lcd_numbers"

image = cv2.imread(path_to_image + image_name)

image = cv2.Canny(image,100,200)

kernel = np.ones((10, 10), np.uint8)
image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

image = cv2.bitwise_not(image)
cv2.imwrite(path_to_image + image_name + '_processed.png', image)

power_val = str(int(float(str(image_to_string(image, None, config=cfg)))))
initial_val = int(power_val)

#reset starting index for current day
#reset e-mail sent tracker
if (current_hour == 0 or path.exists("data/day_start_index_kw.txt") == False):
  f = open('data/day_start_index_kw.txt',"w")
  f.write(power_val)
  f.close()
elif (path.exists("data/day_start_index_kw.txt") and current_hour >0 and current_hour <= 23):
  f = open('data/day_start_index_kw.txt',"r")
  val = f.read().strip()
  f.close()
  if val != "":
    initial_val = int(float(val))
if (current_hour == 0 or path.exists("data/email_sent_track.txt") == False):
  f = open('data/email_sent_track.txt',"w")
  f.write("0")
  f.close()

f = open('data/day_kw.txt',"w")
f.write(str(int(power_val)-initial_val))
f.close()

f = open(sys.argv[2],"w")
f.write(power_val)
f.close()

#export json data
with open(sys.argv[3], 'w') as f:
  f.write('{{"timestamp": "{0}", "power": "{1}"}}'.format(ts, power_val))
  f.close
