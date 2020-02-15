"""
A simple implementation of Ultimatum Game visualization
@date: 2020.2.10
@author: Tingyu Mo
"""

import numpy as np
import pandas as pd
import os
import time
import fractions
import matplotlib.pyplot as plt 
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

def viz_frequency_map(RecordName,Epoch):
    result_dir = './result'
    
    if RecordName != None:
        Record_dir = os.path.join(result_dir,RecordName)
        Epoch_list = os.listdir(Record_dir)
        Epoch_template_str = Epoch_list[0].split('_')
        Epoch_str = Epoch_template_str[0]+'_ep{}_'.format(Epoch)+Epoch_template_str[2]
        f_str = 'frequency_'+Epoch_str+'.csv'

        frequency_path = os.path.join(Record_dir,Epoch_str,f_str)
        # frequency_path = os.path.join(result_dir,'2020-02-09-23-11-44\w100_ep9400000_u0.0562\frequency_w100_ep9400000_u0.0562.csv')
        outputname =   os.path.join(Record_dir,Epoch_str,'Gragh.jpg')
        frequency = pd.read_csv(frequency_path)

    w = Epoch_template_str[0][1:]
    f = np.around(frequency.values,4)
    meta_element = np.arange(14)/12
    p = meta_element.copy()
    q = meta_element.copy()
    
    np.set_printoptions(formatter={'all':lambda x: str(fractions.Fraction(x).limit_denominator())})# decimals to fractions

    plt.figure(figsize=(12.8,9.6),dpi=100,frameon=True)
    # set the grids density
    levels = MaxNLocator(nbins=10).tick_values(np.min(f),np.max(f))
    cm = plt.cm.get_cmap('autumn_r')
    nm = BoundaryNorm(levels,ncolors=cm.N,clip=True)

    plt.pcolormesh(p,q,f,cmap=cm,norm=nm)
    # contourf method is much smoother than pcolormesh!
    # plt.contourf(p,q,f,levels=levels,cmap=cm)

    bar = 'bar'
    if bar == 'bar':
        cbar = plt.colorbar()
        cbar.set_label('Frequency',rotation=-90,va='bottom',fontsize=40)
        tic = np.around(np.arange(np.min(f),np.max(f),(np.max(f)-np.min(f))/10),4)
        cbar.set_ticks(tic)
        
        # set the font size of colorbar
        cbar.ax.tick_params(labelsize=32) 

    ax_label = ['0',' ','1/6',' ','1/3',' ','1/2',' ','2/3',' ','5/6',' ','1']

    plt.title("w={}".format(w),fontsize = 40)
    plt.xticks(meta_element,ax_label,fontsize=16)
    plt.yticks(meta_element,ax_label,fontsize=16)
    plt.xlabel('Offer(p)',fontsize=40)
    plt.ylabel('Demand(q)',fontsize=40)
    plt.tight_layout()
    plt.savefig(outputname,dpi=300)
    plt.show()

if __name__ == '__main__':
    # RecordName = '2020-02-09-23-11-44'
    # RecordName = '2020-02-09-23-12-51'
    # RecordName = '2020-02-11-10-46-10'
    RecordName ='2020-02-15-13-35-16'
    # RecordName ='2020-02-15-13-36-11'
    
    Epoch = 900000
    viz_frequency_map(RecordName,Epoch)