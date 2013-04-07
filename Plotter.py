import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as dte
from pylab import figure, show, savefig

f = open("withdrawals.csv", 'r')

data = f.readlines()
foodDate = []
foodAmount = []
for entry in data:
    start = entry.find("\"", 5)
    if entry[1:start] == "Food and Nutrition Service":
        bits = (entry[start+2:].rstrip()).split(",")
        dt=datetime.datetime.strptime("20" + bits[1],'%Y%m%d')
        foodDate.append(dt)
        foodAmount.append(bits[0])
        
f.close()

dates = dte.date2num(foodDate)

months    = dte.MonthLocator(range(1,13), bymonthday=1, interval=2)
monthsFmt = dte.DateFormatter("%b '%y")

fig = figure()
ax = fig.add_subplot(111)
ax.plot_date(dates, foodAmount, '-')
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.autoscale_view()

##fig = plt.figure()
##
##graph = fig.add_subplot(111)
##
##graph.plot(foodDate, foodAmount,'r-o')

plt.plot_date(dates, foodAmount)

savefig("Food.png")
