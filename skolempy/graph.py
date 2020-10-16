import matplotlib.pyplot as plt
import numpy as np
from math import exp, expm1

filename = "executiontime.txt"
f = open(filename, "r+")
data = f.readlines()
data = [x.strip() for x in data] 
f.close()
filename = "executiontimef.txt"
f = open(filename, "r+")
dataf = f.readlines()
dataf = [x.strip() for x in dataf] 
f.close()
x0 =[]
y0 = []
x1 = []
y1 = []
xf = []
yf = []

mode = []
colours = ["ro","bs"]
xtoy = {}

for i in range(1,len(data)):
    line = data[i]
    line = line.split(", ")
    if int(line[0]) == 0:
        x0.append(int(line[1]))
        if line[3][-4:-2] == "e-":
            y0.append(expm1(float(line[3])))

        else:
            y0.append(float(line[3]))

    if int(line[0]) == 1:
        x1.append(int(line[1]))
        if line[3][-4:-2] == "e-":
            y1.append(expm1(float(line[3])))

        else:
            y1.append(float(line[3]))

for i in range(1,len(dataf)):
    line = dataf[i]
    line = line.split(", ")

    xf.append(int(line[0]))
    if line[2][-4:-2] == "e-":
        yf.append(expm1(float(line[2])))

    else:
        yf.append(float(line[2]))


plt.plot(x0,y0, "r--")
plt.plot(x1,y1, "b:")
plt.plot(xf,yf, "g-.")
plt.yscale('log')
plt.xticks(x0)
plt.ylabel('runtime in s')
plt.show()

