cd#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 20:43:28 2019

@author: cihat
"""

import numpy as np
import pandas as pd
#import time as tm
import linecache as gl
import glob
import os
#from scipy.stats import ks_2samp
#from scipy.stats import anderson_ksamp
#from scipy.stats import linregress
import platform
from multiprocessing import Pool, Process
import matplotlib.pyplot as plt
from functools import partial
op_sys = platform.system()
if op_sys == 'Windows':
    dtdir = 'C:\\Users\\kurt_\\PARAM DATA\\'
    disr_dt = 'C:\\Users\\kurt_\\Dropbox\\Code\\'
    _sl = '\\'
elif op_sys == 'Linux':
    dtdir = '/home/cihat/programs/gdl/'
    disr_dt = '/home/cihat/Dropbox/code/'
    _sl = '/'

os.chdir(dtdir)

print(" Warning!!! Plot paramP34 vs tmP43 to see\n if these two are equal for \
smaller particles.")

#%%
## Warning! When this code runs, it requires ~40gb ram and it takes a while to finish all the calculatations
# When it is done, close the terminal which has exeuted this code and open a new terminal for post processing.
def phase_comp (Hyg_Blue,Hyg_Red,wl, par):

    if wl == 'Blue':
        lmd=0.4909
    elif wl == 'Red':
        lmd=0.9348
    Hyg = pd.read_pickle(disr_dt+'Hyg_'+wl+'.pkl')


    pm = []
    for line in range(4, 185):
        a = gl.getline(par, line)
        columns = a.split()
        rw = {}
        rw['P11'] = columns[0]
        rw['P12'] = columns[1]
        rw['P22'] = columns[2]
        rw['P33'] = columns[3]
        rw['P34'] = columns[4]
        rw['P44'] = columns[5]

        pm.append(rw)

    # Now Converting to a Dataframe
    pm = pd.DataFrame(pm)
    # Let's convert the string values to numeric all at once

    pm = pm.apply(pd.to_numeric)
    pm['theta'] = np.arange(0, 181)
    pm_id = par[par.find('pm'):par.find('.dat')]

    # Getting the value of the paramaeters from the file name.
    sp = pm_id[7:12]
    sp = float(".".join(sp[0:2]) + sp[2:])
    N = int(pm_id[pm_id.find('pm')+2:pm_id.find('_')])

    sp = pm_id[7:12]
    sp = float(".".join(sp[0:2]) + sp[2:])

    n_real = pm_id[13:16]
    n_real = float(".".join(n_real[0:2]) + n_real[2:])

    n_img = pm_id[17:22]
    n_img = float(".".join(n_img[0:2]) + n_img[2:])

    A = vars()['Hyg_'+wl].set_index('theta').join(pm[['theta','P11']].set_index('theta'), how='inner', lsuffix='obs', rsuffix='mdl')
    #KSf = ks_2samp(A.P11obs[0], A.P11mdl[0])
#    KSb = ks_2samp(A.P11obs[17:36], A.P11mdl[17:36])
    #ASf = anderson_ksamp([A.P11obs[0], A.P11mdl[0] ])
#    ASb = anderson_ksamp([A.P11obs[17:36], A.P11mdl[17:36] ])
    #R2f = linregress(A.P11obs[0], A.P11mdl[0])
    #R2b= linregress(A.P11obs[17:36], A.P11mdl[17:36])
#    MSEf = ((A.P11obs[0] - A.P11mdl[0])**2).mean()
#    MSEb = ((A.P11obs[17:36] - A.P11mdl[17:36])**2).mean()
    Rerr_fw = (abs(A.P11obs[0] - A.P11mdl[0])/A.P11obs[0]).mean()
    Rerr_b = (abs(A.P11obs[17:36] - A.P11mdl[17:36])/A.P11obs[17:36]).mean()
    maxpol_pm = max(-pm.P12/pm.P11)
    aw = {}
    # The best criterias are Rel.Err._fw and AS_b or pvalue_b combined.
    # Because in the forward we have only two values. Does not make sense to
    # do Anderson-Darling or Kolmogrov-Smirnov test. A more sensitive test
    # in the frw ang;es would be just a simple distance (abs. error)
    # I removed linear regression R^2 because it does not make sense, since
    # a curve multiplied by a constant would match perfectly in regression to
    # the original curve with R^2 = 1.
    aw['Mdl'] = pm_id
    aw['N'] = N
    aw['sp'] = sp
    aw['Rm'] = sp*lmd/(2*np.pi)
    aw['nr'] = n_real
    aw['ni'] = n_img
    aw['Rel_err_fw'] = Rerr_fw
    aw['Rel_err_b'] = Rerr_b
    aw['maxpol'] = maxpol_pm
    aw['Wave_Length'] = wl

    return aw

Hyg_Blue = pd.read_pickle(disr_dt+'Hyg_Blue.pkl')
Hyg_Red = pd.read_pickle(disr_dt+'Hyg_Red.pkl')
if __name__ == '__main__':
    for wl in ['Blue', 'Red']:
        p = Pool(8)
        func = partial(phase_comp,Hyg_Blue,Hyg_Red, wl)
        file=glob.glob(dtdir+'final{}*.dat'.format(_sl))
        vars()[wl] = p.map(func, file[0:80000])
        vars()[wl]=pd.DataFrame(eval(wl))
        vars()[wl] = eval(wl)[eval(wl).Rel_err_fw <= 0.05]
        if wl == 'Blue':
            vars()[wl] = eval(wl)[(eval(wl).maxpol >= 0.85) & (eval(wl).maxpol <= 0.9)]
        else:
            vars()[wl] = eval(wl)[(eval(wl).maxpol >= 0.978) & (eval(wl).maxpol <= 0.982)]
