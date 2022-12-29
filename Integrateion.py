from threading import Thread
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from time import perf_counter

# Calculates Limit Integral using Reimanns sum Right rule
# Where a and b are integral limits and N are number of iterations of the sum(numer of Rectangles)
# Calculates result, and plot two plot where the first plot illustrates Rectangles, Numer of Retangles depands on N
funk = "x**2"
a, b = 0, 1
N = 10000
#
#
#
# Calculate Integral
def RightReimannsSum(a, b, N,funk):
    def func(x):
        return eval(funk)

    x = np.linspace(a, b * 1.5, 1000)
    y = func(x)

    # Configure plot and write out Integral result
    RectangleCounter = 0
    threadnumber = 10
    partOfArray = N / threadnumber
    deltax = (b-a)/N #  Delta X
    sumArea = 0

    # calculate integral
    for i in range(N):
        endpointX = a + deltax*i
        sumArea += deltax * func(endpointX)

    # Create Region
    polyArray = []
    def CreateRectangles():
        deltax = (b - a) / N  # Delta X
        for j in range(N):
            endpointX = a + deltax * j
            poly = Rectangle([endpointX - deltax, 0], deltax, func(endpointX),
                             edgecolor='0', facecolor='orange')
            polyArray.append(poly)
    CreateRectangles()

    # Add Region to plot
    start = 0
    end = partOfArray
    fig, ax = plt.subplots()
    ax.plot(x, y, 'r', linewidth=2)
    ax.set_title(r"$\int_a^b" + funk + "\mathrm{d}x = $" + str(sumArea))
    ax.set_ylim(bottom=0)

    def AddRegionToPlot(start, end):
        if end <= N:
            for x in range(int(start), int(end)):
                ax.add_patch(polyArray[x])

    start_time = perf_counter()
    threads = []
    for i in range(0, threadnumber):
        t = Thread(target=AddRegionToPlot(start, end))
        threads.append(t)
        t.start()
        start += partOfArray
        end += partOfArray

    for t in threads:
        t.join()
    end_time = perf_counter()
    print(f'It took {end_time - start_time: 0.2f} second(s) to complete.')
    # Finish plott
    fig.text(0.9, 0.05, '$x$')
    fig.text(0.1, 0.9, '$y$')
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks([a, b], labels=['$a$', '$b$'])
    ax.set_yticks([])
    plt.show()
    return sumArea
