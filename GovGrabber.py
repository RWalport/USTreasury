from urllib import urlopen
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt

import datetime
import time

numdays = 365

formattedDates = []

base = datetime.datetime.today()
dateList = [ base - datetime.timedelta(days=(x + 55)) for x in range(0,numdays) ]

for entry in dateList:
    formattedDates.append([entry, entry.strftime("%y%m%d")])

urlprefix = 'https://fms.treas.gov/fmsweb/viewDTSFiles?dir=a&fname='
urlpostfix = '00.txt'
Budget = []

f = open('withdrawal.txt', 'r')
categories = f.readlines()

f.close()
fileposition = 0

for date in formattedDates:

    text = urlopen(urlprefix + date[1] + urlpostfix).readlines()

    i = 0
    for line in text:
        fileposition = re.search(r'Commodity Credit Corporation programs', line)
        i += 1
        if fileposition:
            break

    for line in text[i:]:
        fileposition = re.search(r'Commodity Credit Corporation programs', line)
        i += 1
        if fileposition:
            break

    breaker = 0
    for line in text[i-1:]:
        for entry in categories:
            entry = entry.rstrip("\n")
            x = re.search(r'%s' %entry, line)
            if x:
                m = re.search("\d", line)
                if m:
                    num = re.findall(r'[0-9,]+', line[m.start():])
                    integer = re.sub(r'[^0-9]', "", num[0])
                    result = ["\"" + entry + "\"", int(integer), date[1]]
                    Budget.append(result)
                    if entry == "Transfers to Depositaries":
                        breaker = 1
                    break           
                else:
                    "This shouldn't ever happen"
        if breaker == 1:
            time.sleep(0.5)
            break

f = open("withdrawals.csv", "w")
f.write("Name of Account, Dollar Value in Millions, Date (yymmdd)\n")
for entry in Budget:
    outputfeed = entry[0] + "," + str(entry[1]) + "," + str(entry[2]) + "\n"
    f.write(outputfeed)
f.close()

