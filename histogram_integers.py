import sys, getopt
import pylab as plt





##read data from file
####################
def read_data (filein):
    data = []
    with open(filein) as f:
        for line in f:
            data.append(float(line.strip()))
    return data
#####################


##compute histogram for integer numbers
####################
def histogram_from_data (data):
    hist = {}
    norm = 0.0
    for n in data:
        if n not in hist:
            hist[n] = 0.0
        hist[n] = hist[n] + 1.0
        norm = norm + 1.0
        
    x = []
    px = []

    for n in hist:
        x.append(n)
        px.append(hist[n]/norm)

    return x, px
#####################







filein = sys.argv[1]

                        
data = read_data(filein)

x, px = histogram_from_data (data)






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

ax1.bar(x, px, 1, align='center', color='r')

plt.show()
