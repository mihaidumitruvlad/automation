## Description
This project aims to automate the process of reading LCD digits and dump information about time & value into google sheets.
Threshold with e-mail notification when reached can be configured.
Sample screenshots with graph charts are available in the project

## Prerequisites

**Apps / Packages**
 - tesseract - OCR
 - python3 - programming language - scripts
 - fswebcam - capture image of LCD
 - apache2 - Web, to display data

**Python libs**
 - pip
 - pipenv (maybe create an environment for this specific project)
 - pytesseract - OCR
 - Adafruit_DHT - Sensor DHT22 data retrieval
 - numpy - image processing
 - opencv - image processing

## Configuration

**Train Tesseract your own LCD font:**
 - You may use jTessBoxEditor: https://sourceforge.net/projects/vietocr/files/jTessBoxEditor/jTessBoxEditor-2.2.1.zip/download;
**Or**
 - copy my lcd_numbers.traineddata in /usr/share/tesseract/4.0/tessdata if is similar to my LCD font.

**Mailbox account**
 - mail: [e-mail@gmail.com]
 - pass: [something]
 - Switch less secure apps **ON**: https://myaccount.google.com/u/4/lesssecureapps?pageId=none&pli=1

**For google sheets API access**
 - Api Key JSON for Google Drive access with **Project Writer Role**:
 - Google cloud console -> Create new project -> Activate api -> Google drive -> Create service account -> Web app -> Role project writer

**Additional configuration**
To ensure accuracy for reading of the LCD (in my case the display loops through different value sets), I added some extra value-safe checks:
 - Found the pattern that the data I have it's in less than 5 length;
 - Added a **margin** variable in **power.sh** to compare current value with previous value;
 - Added a loop after **8** seconds with a re-capture of the image until I get the correct frame captured with a **max_retries** of 5.

**Google sheets**
 - push2gsheets.py -> data colmns index, book_name, sheet_name power.sh;
 - call script push2gsheets.py;
 - update api_key.json file or put key in "keys/api_key.json".

**E-mail alerts**
 - power.sh -> email (e-mail recipients CSV), thresh (limit value to send alerts when reached);
 - sendmail.py -> port, smtpserver, sender_email, password.

**Web**
 - To expose data to a simple local web server copy web archive content in / (it will be /var/www/html);
 - The scripts will export several JSON files containing data to /var/www/html/output;
 - The index.html page will use a few JS to display the data.

## Run

**Configure launcher.sh in CRON (crontab -e)**
Launcher supports a command line argument which is the set of scripts you want to trigger, to make it easier to handle the calling of the scripts.
 - 'internal' -> will run the scripts/rpi_internal.py which will create the JSON containing the last CPU temp value;
 - 'sensor' -> will run the scripts/sensor.sh which will trigger DHT_read.py with a few parameters where to export the JSON with sensor data;
 - 'power' -> will run several scripts - capture, process, check values against threshold and google sheets last value, send e-mail if threshold was reached.

**Sample value**
 - */17 * * * * /Stuff/Scripts/launcher.sh internal
 - */17 * * * * /Stuff/Scripts/launcher.sh sensor
 - */30 * * * * /Stuff/Scripts/launcher.sh power
