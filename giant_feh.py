# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 09:42:39 2023

@author: lenovo
"""

import numpy as np,matplotlib.pyplot as plt
import pandas as pd
import glob
import os

error=(0.01**2+0.01**2)**0.5        #given magnitude error

data=pd.read_csv('giant_feh.csv')
u0=data.loc[:,['u']].values
g0=data.loc[:,['g']].values
i0=data.loc[:,['i']].values
u,g,i=u0.flatten(),g0.flatten(),i0.flatten()
xdata,ydata=g-i,u-g



#First step: refuse data beyond the applicability range
m=[]
n=[]
a,b=0.53,1.24   #a,b denote lower and upper limit of given (g-i), respectively
ind=np.where((xdata>a)&(xdata<b))
xdata=xdata[ind]
ydata=ydata[ind]  
c=-4*np.ones(len(xdata))  # c is given [Fe/H]   
#given fitting coefficients         
a00=1.97584409
a01=0.08416027
a02=0.00132534
a03=-0.00096423
a10=-3.19403124
a11=0.30032519
a12=0.04930566
a20=4.62297161
a21=0.01655657
a30=-1.43240477
need=a00+a01*c+a02*c**2+a03*c**3+a10*xdata+a11*xdata*c+a12*xdata*c**2\
             +a20*xdata**2+a21*xdata**2*c+a30*xdata**3 
ind=np.where(ydata>=need)     # choose data that above [Fe/H]=-4 line
xdata=xdata[ind]
ydata=ydata[ind]  
for i in np.arange(0,len(xdata)):
    x=xdata[i]
    y=ydata[i]
    m.append(x)   # m is an empty list to restore (g-i) data
    n.append(y)   # n is an empty list to restore (u-g) data
np.savetxt("g-i_use.csv",m)
np.savetxt("u-g_use.csv",n)  
      
 
        
#Second step: predict [Fe/H] with derived polynomial
m=[]
n=[]
xdata=np.loadtxt("g-i_use.csv",delimiter=',') 
ydata=np.loadtxt("u-g_use.csv",delimiter=',')
for i in np.arange(0,len(xdata)):
    x1=xdata[i]                        # x1 denotes (g-i) 
    y1=ydata[i]                        # y1 denotes (u-g) 
    f1=np.linspace(-4,0.5,91)           # given [Fe/H]
    x10=x1+error*np.random.randn(91)       #given (g-i) with error
    y10=y1+error*np.random.randn(91)       #given (u-g) with error
    need=a00+a01*f1+a02*f1**2+a03*f1**3+a10*x10+a11*x10*f1+a12*x10*f1**2\
             +a20*x10**2+a21*x10**2*f1+a30*x10**3    
    sigma1=0.013062754676023238-0.002093386575314095 *x1   #(g-i) random error
    sigma2=0.02765716484703738-0.0019499350415479824 *y1   #(u-g) random error                  
    sigma=sigma2
    likelihood=((2*np.pi)**0.5*sigma)**(-1)*(np.e)**(-((y10-need)**2)/(2*sigma**2))
    f=np.argmax(likelihood)
    sigma_feh=((sigma2**2-sigma1**2*(a10+a11*f1[f]+a12*(f1[f])**2+\
                    2*a20*x1+2*a21*x1*f1[f]+3*a30*x1**2)**2)/(a01+2*a02*f1[f]\
    +3*a03*(f1[f])**2+a11*x1+2*a12*x1*f1[f]+a21*x1**2))**0.5
    sigma3=(sigma_feh**2+0.22**2)**0.5 
    m.append(f1[f])
    n.append(sigma3)
np.savetxt("giant_feh_predicted.csv",m)
np.savetxt("giant_feh_error.csv",n)

#Last step: delete intermediate files
os.remove("u-g_use.csv")
os.remove("g-i_use.csv")