#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 20:12:13 2019

@author: cihat
"""

import numpy as np
import pandas as pd
#import time as tm
import linecache as gl
import glob
import os
from scipy.stats import ks_2samp
from scipy.stats import anderson_ksamp
from scipy.stats import linregress
import platform
from multiprocessing import Pool, Process
import matplotlib.pyplot as plt
import seaborn as sn
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

#%%  Only for BLUE-80km USe the next cell because, the next cell first calculates wl_flt which provides
# better constraint on the size of the aggregate. Then in the next step it filters
# the model runs based SSA constraint on nr, ni among the models that passes the
# the aggregates size filter.
Blue = pd.read_pickle(disr_dt+'Blue.pkl')
Red = pd.read_pickle(disr_dt+'Red.pkl')
Hyg_Blue = pd.read_pickle(disr_dt+'Hyg_Blue.pkl')
Hyg_Red = pd.read_pickle(disr_dt+'Hyg_Red.pkl')
ssa = pd.read_pickle(disr_dt+'SSA.pkl')
s=0
k=0

def ragg(dt):
    # SettingWithCopyWarning could indicate a serious problem, but this time, it is false positive
    # So let's silence the warning. See https://www.dataquest.io/blog/settingwithcopywarning/
    with pd.option_context('mode.chained_assignment', None):
        dt['Ragg'] = dt['Rm']*dt['N']**(1.0/3.)
def Reset_index(dt):
   dt = dt.reset_index()
   dt = dt.drop('index', axis=1)

dst = 'C:\\Users\\kurt_\\PARAM DATA\\final0\\'
src = 'D:\\final\\'
for wl in ['Blue', 'Red']:
    for alt in [ '80new', '200']:

#        vars()[wl+alt] = eval(wl)[eval(wl)[f'w0{alt}_Rerr'] <= 0.05]
#        vars()[wl+alt] = eval(wl+alt)[eval(wl+alt)['Rel_err_b'] <= 0.155]
        if wl == 'Blue':
            # First Constrain the N and SP from the DISR Phase (most relevant for 80 km)
            vars()[f'{wl}_flt'] = eval(wl)[eval(wl)['Rel_err_b'] < 0.15] # ***
            # Now constraint from SSA
            vars()[wl+alt] = eval(wl)[eval(wl)[f'w0{alt}_Rerr'] <= 0.05]
            if alt == '80new':
                vars()[wl+alt] = eval(wl+alt)[eval(wl+alt)['Rel_err_b'] <= 0.22]
                # Let's limit the parameters in the limits of N obtained there ***
                vars()[wl+alt] = eval(wl+alt)[(eval(wl+alt).N <= np.max(eval(f'{wl}_flt').N)) & (eval(wl+alt).N >= np.min(eval(f'{wl}_flt').N))]
            elif alt == '200':
                vars()[wl+alt] = eval(wl+alt)[eval(wl+alt)['Rel_err_b'] <= 0.15]

        elif wl == 'Red':
            vars()[wl+alt] = eval(wl)[eval(wl)[f'w0{alt}_Rerr'] <= 0.05]
            vars()[wl+alt] = eval(wl+alt)[eval(wl+alt)['Rel_err_b'] <= 0.11]
            ragg(vars()[wl+alt])

            vars()[f'{wl}_flt'] = eval(wl)[eval(wl)['Rel_err_b'] < 0.11]

#            vars()[wl+alt] = eval(wl+alt)[eval(wl+alt)['Rm'] > 0.035]

        for dt in [eval(wl+alt), eval(f'{wl}_flt')]:
            with pd.option_context('mode.chained_assignment', None):
                dt['filter'] = dt['Rel_err_fw']*dt['Rel_err_b']*dt[f'w0{alt}_Rerr']
            ragg(dt)
            Reset_index(dt)
#        vars()[wl+alt] = eval(wl+alt)[(eval(wl+alt).N <= np.max(eval(f'{wl}_flt').N)) & (eval(wl+alt).N >= np.min(eval(f'{wl}_flt').N))]
#        vars()[wl+alt]['Rel_err_fw'] = np.sqrt(eval(wl+alt)['MSEf']/(Hyg_Blue.P11[0]**2))
#        vars()[wl+alt]['Rel_err_fw'] = np.sqrt(eval(wl+alt)['MSEf']/(Hyg_Blue.P11[0]**2))


#        for i in eval(wl+alt).Mdl:
#            try:
#                copy2(f'{src}new{i}.dat', f'{dst}{i}.dat')
#            except:
#                s+=1
#        for i in eval(wl+alt).Mdl:
#
#            my_file = Path(f'{src}new{i}.dat')
#            if my_file.is_file():
#                k+=1
#print(f'Number of missing file is {s}')
#print(f'Number of file available is {k}')
