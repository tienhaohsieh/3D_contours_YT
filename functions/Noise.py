#! /usr/bin/python
from scipy.optimize import curve_fit
from pylab import *
from numpy import *

def Gaussian(x,cen,top,sigma):
        Gau=top*exp(-(x-cen)**2/(2*sigma**2))
        return Gau
def Noise(Map,pl=False,pr=False,start=-300,end=300,cell=2):
    bins=int((end-start)/cell+1)
    Map=Map.reshape(1,product(shape(Map)))[0]
    Map=Map[~isnan(Map)]
    Hist=histogram(Map,bins=bins,range=(start-cell/2,end+cell/2))
    Hist=[arange(start,end+cell,cell),Hist[0]]
    peak=max(Hist[1])
    p0=[Hist[0][where(Hist[1]==peak)][0],peak,(end-start)*0.1]
    popt,pcov=curve_fit(Gaussian,Hist[0],Hist[1],p0=p0,maxfev=100000)
    if pl==True:
       x=arange(start,end,0.0002)
       step(Hist[0],Hist[1],where='mid')
       plot(x,Gaussian(x,popt[0],popt[1],popt[2]))
       xlim(start,end)
       show()
       close()
    Noi=popt[2]
    mea=popt[0]
    if pr==True:
       print("Noise = ",Noi, "Mean = ",mea)
    return [popt[0],popt[1],abs(popt[2])]

