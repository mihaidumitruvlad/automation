import gspread
import sys
import os.path
from os import path
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import subprocess

book_name = "KW" #google_sheets bookwork name
sheet_name = "Data" #google_sheets sheet name
sheet_link = "https://docs.google.com/spreadsheets/d/<sheet_id>" #replace <sheet_id> with the actual id of your google sheet

f = open(sys.argv[2], 'r')
power = int(float(f.read()))
f.close()

last_power = 0

if path.exists('data/last_ghseet_val.txt'):
  f = open('data/last_ghseet_val.txt', 'r')
  val = f.read().strip()
  if val != "":
    last_power = int(float(val))
    f.close()
    print("Retrieved last value pushed to google sheets of " + str(last_power))

if last_power < power:
  key_file = sys.argv[1]
  timeCol = 6 #column where to update the time
  powerCol = 7 #column where to update the value
  countCol = 10 #column where total row count information is available (google sheet formula) -> used to reduce the total number of API calls to google sheets
  time = datetime.now().strftime('%H:%M')
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  creds = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
  print("Connecting to google sheets")
  client = gspread.authorize(creds)
  print("Opening workbook: " + book_name + ", sheet: " + sheet_name)
  book = client.open_by_url(sheet_link)
  #sheet = book.get_worksheet(0)
  #sheet = book.worksheet(sheet_name)
  sheet = client.open(book_name).worksheet(sheet_name)
  lastRow = int(sheet.cell(1, countCol).value)
  print("Last row is " + str(lastRow))

  last_power_gsheet = int(float(sheet.cell(lastRow,powerCol).value))

  if last_power_gsheet < power:
    print("Previous value in sheet is lower than current value. Pushing data")
    sheet.update_cell(lastRow + 1,timeCol,time) #update time column
    sheet.update_cell(lastRow + 1,powerCol,power) #update power information
    print("Done. updating JSON")
    with open(sys.argv[3], 'w') as f:
      f.write('{{"timestamp": "{0} {1}", "power": "{2}"}}'.format(datetime.now().strftime('%d-%b-%Y'), time, str(power)))
      f.close
    print("Done. Saving last value pushed to google sheets")
  elif last_power_gsheet == power:
    print("Previous value in sheet is the same with the current value. Not pushing value to google sheets")
  with open('data/last_ghseet_val.txt', 'w') as f:
    f.write(str(power));
    f.close
else:
  print("Last value pushed to google sheets is still the same. Not pushing value to google sheets")
