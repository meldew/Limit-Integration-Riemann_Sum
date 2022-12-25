from threading import Thread
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from time import sleep, perf_counter
from matplotlib.patches import Polygon

# Calculates Limit Integral using Reimanns sum Right rule
# Where a and b are integral limits and N are number of iterations of the sum(numer of Rectangles)
# Calculates result, and plot two plot where the first plot illustrates Rectangles on the graph and the
# second plot illustrates the overall area under the function
funk = "(5*x+2)"
a, b = -2, 3
N = 1000
#
#
#
#
#
# Function
def func(x):
    f = eval(funk)
    return f

x = np.linspace(a, b*1.5, 1000)
y = func(x)
RectangleCounter = 0
threadnumber = 10
partOfArray = N/threadnumber
start = 0
end = partOfArray

# Calculate Integral
def RightReimannsSum(a, b, N,funk):
    #Right Reimann summ
    i = 1 # Starting sample
    deltax = (b-a)/N #  Delta X
    sumArea = 0

    def func(x):
        return eval(funk)

    for x in range(N):
        endpointX = a + deltax*i
        sumArea += deltax * func(endpointX)
        i=i+1
    return sumArea

val = str(RightReimannsSum(a, b, N,funk))

# Configure plot and write out Integral result
fig, ax = plt.subplots()
ax.plot(x, y, 'r', linewidth=2)
ax.set_title(r"$\int_a^b"+funk+"\mathrm{d}x = $"+val)
ax.set_ylim(bottom=0)

polyArray = []
# Create Region
def CreateRectangles():
    i = 1  # Starting sample
    deltax = (b - a) / N  # Delta X
    for x in range(N):
        endpointX = a + deltax * i
        poly = Rectangle([endpointX-deltax, 0], deltax, func(endpointX),
                                        edgecolor='0', facecolor='orange')
        polyArray.append(poly)
        i = i + 1
CreateRectangles()

#Add Region to plot
start = 0
end = partOfArray
def AddRegionToPlot(start, end):
    if end <= N:
        for x in range(int(start), int(end)):
            ax.add_patch(polyArray[x])

start_time = perf_counter()

threads = []
for i in range(0, threadnumber):
    print("start : " + str(start))
    print("end : " + str(end))
    t = Thread(target=AddRegionToPlot(start, end))
    threads.append(t)
    t.start()
    start += partOfArray
    end += partOfArray
    print(t.name)
    print("______________")

for t in threads:
    t.join()

end_time = perf_counter()
print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')

# Configure second plot
fig, jx = plt.subplots()
jx.plot(x, y, 'r', linewidth=2)
jx.set_title(r"$\int_a^b"+funk+"\mathrm{d}x = $"+val)
jx.set_ylim(bottom=0)

ix = np.linspace(a, b)
iy = func(ix)
verts = [(a, 0), *zip(ix, iy), (b, 0)]
poly = Polygon(verts, facecolor='0.8', edgecolor='0.4')
jx.add_patch(poly)

# Finish plott
fig.text(0.9, 0.05, '$x$')
fig.text(0.1, 0.9, '$y$')
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.set_xticks([a, b], labels=['$a$', '$b$'])
ax.set_yticks([])
plt.show()

