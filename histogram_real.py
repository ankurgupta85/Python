import sys, getopt
import pylab as plt
import math
import numpy as np




##read data from file
####################
def read_data (filein):
    data = []
    with open(filein) as f:
        for line in f:
            data.append(float(line.strip()))
    return data
#####################


##compute histogram for real numbers
####################
def histogram_from_real_data (data, bins):

    min_val = min(data)
    max_val = max(data)
    dx = (max_val - min_val) / bins

    hist = {}
    norm = 0.0
    for r in data:
        b = int( (r - min_val) / dx )
        if b not in hist :
            hist[b] = []
            hist[b].append(0.0)
            hist[b].append(0.0)
        hist[b][0] = hist[b][0] + 1.0
        hist[b][1] = hist[b][1] + r
        norm = norm + 1.0
        
    x = []
    px = []

    for b in hist:
        x.append(hist[b][1] / hist[b][0])
        px.append(hist[b][0] / dx / norm)
    
    return x, px, dx
#####################







filein = sys.argv[1]
bins = int(sys.argv[2])

                        
data = read_data(filein)

x, px, dx = histogram_from_real_data (data, bins)






###########################

fig = plt.figure()
plt.rcParams['xtick.major.pad'] = 8
plt.rcParams['ytick.major.pad'] = 8

y_label = '$P(x)$'
x_label = '$x$'
fontsize = 30


ax1 = fig.add_subplot(1,1,1)
ax1.set_xlabel(x_label, fontsize=fontsize)
ax1.set_ylabel(y_label, fontsize=fontsize)

ax1.bar(x, px, dx, align='center', color='r')




##draw normal distribution
#func_x = np.arange(-5, 5, 0.1)
#func_y = 1.0/np.sqrt(2.0*math.pi) * np.exp(-func_x*func_x/2.0)
#ax1.plot(func_x, func_y, linewidth=2.0, color='k')
#########################



plt.show()
