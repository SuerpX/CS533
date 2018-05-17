import matplotlib.pyplot as plt
import pylab as pl
def generatePlot(x1, y1, x2, y2, x3, y3, filename):
    Fig = plt.figure(figsize=(8,4))
    Ax = Fig.add_subplot(111)
    pl.title(filename)# give plot a title
    pl.xlabel("lerning trial")# make axis labels
    pl.ylabel("value")
#    pl.xlim(0.0, 9.0)# set axis limits
#    pl.ylim(0.0, 30.)=
    Ax.plot(x1, y1, x2, y2, x3, y3)
    Ax.legend(["MC agent", "SARSA agent", "QL agent"]) 
    Fig.savefig(filename + ".pdf")
