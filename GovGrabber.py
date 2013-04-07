from urllib import urlopen
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt

import datetime
import time

numdays = 50

formattedDates = []

base = datetime.datetime.today()
dateList = [ base - datetime.timedelta(days=(x + 55)) for x in range(0,numdays) ]

for entry in dateList:
    formattedDates.append([entry, entry.strftime("%y%m%d")])

urlprefix = 'https://fms.treas.gov/fmsweb/viewDTSFiles?dir=a&fname='
urlpostfix = '00.txt'
opBudget = []

for date in formattedDates:

    text = urlopen(urlprefix + date[1] + urlpostfix).readlines()

    for line in text:
        x = re.search(r'Total Operating Balance', line)
        if x:
            m = re.search("\d", line)
            if m:
                num = re.findall(r'[0-9,]+', line[m.start():])
                integer = re.sub(r'[^0-9]', "", num[0])
                result = [int(integer), date[0]]
                opBudget.append(result)
                time.sleep(0.5)
                break           
            else:
                "This shouldn't ever happen"
                      
print "total operating budget"
y = [value for (value, date) in opBudget]
x = [date for (value, date) in opBudget]
datetick = []

i = 1

for date in x:
    if i % 10 == 0:
        datetick.append(date)
    i +=  1
print datetick

fig = plt.figure()

graph = fig.add_subplot(111)

graph.set_xticks(datetick)

# Plot the data as a red line with round markers
graph.plot(x,y,'r-o')

plt.show()

