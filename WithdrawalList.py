from urllib import urlopen
import re

url = "https://fms.treas.gov/fmsweb/viewDTSFiles?dir=a&fname=12100100.txt"

text = urlopen(url).readlines()
go = 0
f = open("withdrawal.txt", 'w')

for line in text:
    x = re.search(r'Commodity Credit Corporation programs', line)
    if x:
        go += 1
    if go == 2:
        category = (re.findall(r'[a-zA-Z ,.]+[^0-9]', line))[0]
        category = re.sub(r' [ ]+', "", category)
        category = re.sub(r'$', "", category)
        f.write(category + "\n")
    y = re.search(r'Transfers to Depositaries', line)
    if y:
        go += 1

f.close()
