import cv2
import re
import csv
import pytesseract
import numpy as np
#from PIL import Image
from geotext import GeoText
from dateutil.parser import _timelex, parser

#Developed by Deepak Nadiminti

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]


def convert_image_to_text(string):
   pytesseract.pytesseract.tesseract_cmd=r'C:\\Program Files\\Tesseract-OCR\tesseract.exe'

   img = cv2.imread(string)

   img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   kernel = np.ones((1, 1), np.uint8)
   img = cv2.dilate(img, kernel, iterations=1)
   img = cv2.erode(img, kernel, iterations=1)

   cv2.imwrite("removed_noise.png", img)

   cv2.imwrite("thres.png", img)

   img = cv2.imread('thres.png')

   text = pytesseract.image_to_string(img, lang='eng')
   #print(str(text))
   return (str(text))

#Extractig places DN
def extract_places(sring):
   places = GeoText(string)
       #removing unwanted names
   places = list(dict.fromkeys(places.cities))
   if 'Singapore' in string:
      places.append('Singapore')
   elif 'singapore' in string:
      places.append('Singapore')
   if 'Sydney' in string:
      places.append('Sydney')
   elif 'sydney' in string:
      places.append('sydney')
   
   for place in places:
       if place == 'Orion' or place == 'Bay' or place == 'Deal' or place == 'Mon' or place == 'Kati':
           places = remove_values_from_list(places, place)
      #reorder cities
   indices = {c: i for i, c in enumerate(string.split())}
   return sorted(places, key=indices.get)
#print (places)


#Extracting dates DN
def get_dates(string):

    a = string

    p = parser() #DN
    info = p.info

    def timetoken(token):
      try:
        float(token)
        return True
      except ValueError:
        pass
      return any(f(token) for f in (info.jump,info.weekday,info.month,info.hms,info.ampm,info.pertain,info.utczone,info.tzoffset))

    def timesplit(input_string):
      batch = []
      for token in _timelex(input_string):
        if timetoken(token):
          if info.jump(token):
            continue
          batch.append(token)
        else:
          if batch:
            yield " ".join(batch)
            batch = []
      if batch:
        yield " ".join(batch)
        
    for item in timesplit(a):
        if '2019' in item or '2020' in item:
            return item
      #date_value = str(p.parse(item))
      #print ("Parsed:", date_value[0:10])

# Get Flight fare rates
def get_fares (string):
   regexList = [r"(?:[\£\$\€]{1}[,\d]+.?\d*)", r"(?:[\£\$\€]{1} [,\d]+.?\d*)"]
   gotMatch = False
   regex_final = r"(?:[\£\$\€]{1}[,\d]+.?\d*)"
   for regex in regexList:
       s = re.search(regex,text)
       if s:
          gotMatch = True
          regex_final= regex
          break

   if gotMatch:
      r1 = re.findall(regex_final,text)
   return r1

string = convert_image_to_text('<insert image location here>')
flight_places = extract_places(string)
flight_dates = get_dates(string)

#print(string)
print(flight_places)
print(flight_dates)
