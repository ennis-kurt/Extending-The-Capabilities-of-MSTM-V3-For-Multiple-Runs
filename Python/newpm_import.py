# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 14:09:21 2018

@author: kurt_
"""
import numpy as np
import pandas as pd
import time as tm
import linecache as gl
import glob
import os
import xarray as xr
import platform
op_sys = platform.system()
if op_sys == 'Windows':
    dtdir = 'C:\\Users\\kurt_\\Google Drive\\dell_github\\T-Matrix-Titan\\special\\data\\'
    _sl = '\\'
elif op_sys == 'Linux':
    dtdir = '/home/cihat/Dropbox/code/special/data/'
    _sl = '/'
os.chdir(dtdir)

file = glob.glob(dtdir+'FAFAS{}newpm*.dat'.format(_sl))

print(" Warning!!! Plot paramP34 vs tmP43 to see\n if these two are equal for \
smaller particles.")
# %%
for par in file:
    param_run = par[par.find('newpm'):par.find('.dat')]
    q = gl.getline(par, 2)
    q = q.split()
    qabs = [float(q[0])]
    qsca = [float(q[1])]
    qext = [float(q[2])]

    try:
        csca = [float(q[3])]
    except ValueError:
        print(param_run)
    cabs = [float(q[4])]
    taus_out = [float(q[5])]
    taua_out = [float(q[6])]

    eff = {'qa': qabs, 'qs': qsca, 'qe': qext, 'cs': csca,
           'ca': cabs, 'taus': taus_out, 'taua': taua_out}
    vars()[param_run+'_eff'] = pd.DataFrame(eff)

    # Now I will collect scattering matrix data in a data frame
    data = []
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
        data.append(rw)

    # Now Converting to a Dataframe
    dt = pd.DataFrame(data)
    del(rw)

    # Let's convert the string values to numeric all at once
    vars()[param_run+'_mx'] = dt.apply(pd.to_numeric)
    vars()[param_run+'_mx']['theta'] = np.arange(0, 181)

    # For now I will not convert the data to xarray. I do not see any benefit
    # doing that other than being able to collect matrix elements and efficien-
    # ies in the same dataset. Hence, below code block is commented

#    # Now collecting everything in an xarray dataset
#    # Note that PXX are saved as variable, but Qx and g are saved as dimension
#    vars()[param_run] = xr.Dataset.from_dataframe(dt)
#    vars()[param_run]['qext'] = qext
#    vars()[param_run]['qabs'] = qabs
#    vars()[param_run]['qsca'] = qsca
#    vars()[param_run]['g'] = g
