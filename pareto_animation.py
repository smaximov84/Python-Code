# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:53:55 2019

@author: s1348875
"""

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import pandas as pd
os.chdir('C:\TRNSYS18\MyProjects\Script to run TRNSYS from python')


pareto=[]


for i in range(10): #range is the number of pareto fronts generated -1
    df = pd.DataFrame(pd.read_csv(os.getcwd()+"\\240 ind - 200 gen - 3var - 250120 - STS and boiler fixed\DLSC_Temuco_multiobj_hof_"+str(10*i+10)+".csv",sep=",",header=None,names=['Cost', 'Emissions', 'Solar', 'LTS', 'Angle'],index_col=False))
    pareto.append(df) 
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlabel('Emissions')
ax.set_ylabel('Cost')
ax.set(xlim=(0, 2000), ylim=(0, 6000))
scat = ax.scatter(pareto[0]['Emissions'],pareto[0]['Cost'])

#%%
def animate(j):
    scat.set_offsets(pareto[j][['Emissions','Cost']])
anim = FuncAnimation(fig, animate, frames=10, interval=1000, repeat_delay=1000)
 
plt.draw()
plt.show()
