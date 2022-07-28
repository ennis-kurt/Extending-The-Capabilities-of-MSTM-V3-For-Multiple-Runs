#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 00:17:10 2019

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
from multiprocessing import Pool, Process
import matplotlib.pyplot as plt
from functools import partial
import platform
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


#%%

print('Remove this cell, and put the actual code into the above loop')
Valid_aero = []
for pm_id in file_names:
    #pm_eff = vars()[pm_id+'_eff']
    pm = vars()[pm_id+'_mx']
    maxpol_pm = max(-pm.P12/pm.P11)

    if maxpol_pm >= 0.85 and maxpol_pm <= 0.90:
        Valid_aero.append(pm_id)

#%%file=glob.glob(dtdir+'final{}*.dat'.format(_sl))
file_names = []
for par in file:
    param_run = par[par.find('pm'):par.find('.dat')]
    file_names.append(param_run)
    q = gl.getline(par, 2)
    q = q.split()
    qabs = [float(q[0])]
    qsca = [float(q[1])]
    qext = [float(q[2])]

    try:
        csca = [float(q[3])]
    except ValueError:
        print('csca value error',param_run)
    cabs =[float(q[4])]
    taus_out = [float(q[5])]
    taua_out = [float(q[6])]

    eff = {'qa': qabs, 'qs': qsca, 'qe': qext, 'cs': csca, 'ca': cabs, 'taus': taus_out, 'taua': taua_out}
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

if op_sys == 'Windows':
    dtdir = 'C:\\Users\\kurt_\\Dropbox\\Code\\special\\data\\'
    _sl = '\\'
elif op_sys == 'Linux':
    dtdir = '/home/cihat/Dropbox/code/special/data/'
    _sl = '/'
os.chdir(dtdir)


#%%
# Comparing models to DISR AEROLO P11 to find the best fitting model


#Blue = pd.read_pickle(disr_dt+'Blue.pkl')
#Red = pd.read_pickle(disr_dt+'Red.pkl')
Hyg_Blue = pd.read_pickle(disr_dt+'Hyg_Blue.pkl')
Hyg_Red = pd.read_pickle(disr_dt+'Hyg_Red.pkl')

for wl in ['Blue', 'Red']:
    Phase = []
    if wl == 'Blue':
        lmd=0.4909
    elif wl == 'Red':
        lmd=0.9348
    for pm_id in file_names:
        try:
            pm = vars()[pm_id+'_mx']
        except KeyError:
            print(pm_id+'_mx', 'not found')
            continue
        sp = pm_id[7:12]
        sp = float(".".join(sp[0:2]) + sp[2:])
        N = int(pm_id[pm_id.find('pm')+2:pm_id.find('_')])

        sp = pm_id[7:12]
        sp = float(".".join(sp[0:2]) + sp[2:])

        n_real = pm_id[13:16]
        n_real = float(".".join(n_real[0:2]) + n_real[2:])

        n_img = pm_id[17:22]
        n_img = float(".".join(n_img[0:2]) + n_img[2:])

        A = vars()['Hyg_'+wl].set_index('theta').join(pm[['theta','P11','ASb']].set_index('theta'), how='inner', lsuffix='obs', rsuffix='mdl')
        #KSf = ks_2samp(A.P11obs[0], A.P11mdl[0])
        KSb = ks_2samp(A.P11obs[17:36], A.P11mdl[17:36])
        #ASf = anderson_ksamp([A.P11obs[0], A.P11mdl[0] ])
        ASb = anderson_ksamp([A.P11obs[17:36], A.P11mdl[17:36] ])
        #R2f = linregress(A.P11obs[0], A.P11mdl[0])
        #R2b= linregress(A.P11obs[17:36], A.P11mdl[17:36])
        MSEf = ((A.P11obs[0] - A.P11mdl[0])**2).mean()
        MSEb = ((A.P11obs[17:36] - A.P11mdl[17:36])**2).mean()
        Rerr_fw = (abs(A.P11obs[0] - A.P11mdl[0])/A.P11obs[0]).mean()
        Rerr_b = (abs(A.P11obs[17:36] - A.P11mdl[17:36])/A.P11obs[17:36]).mean()
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

        aw['KSpvalue_b'] = KSb.pvalue
#        aw['KSpvalue_fw'] = KSf.pvalue
        #aw['pvalue'] = (KSf.pvalue*KSb.pvalue)
        #aw['KSb'] = KSb.statistic
        #aw['KSf'] = KSf.statistic
        #aw['KS'] = (KSf.statistic + KSb.statistic)/2.0

        aw['ASb'] = ASb.significance_level
#        aw['ASf'] = ASf.significance_level
        #aw['AS'] = ASb.significance_level*ASf.significance_level
        #aw['Rel_err'] = (Rerr_fw*Rerr_b)
        aw['Rel_err_fw'] = Rerr_fw
        aw['Rel_err_b'] = Rerr_b
        aw['MSEf'] = MSEf
        aw['MSEb'] = MSEb
        aw['Wave_Length'] = wl
        Phase.append(aw)

    vars()[wl+'_phase'] = pd.DataFrame(Phase)
    vars()[wl+'_phase']['Filter'] = (1-vars()[wl+'_phase']['MSEf'])*vars()[wl+'_phase']['ASb']

#    vars()[wl] = vars()[wl].set_index('Mdl').join(dt.set_index('Mdl'), how = 'outer')
#    vars()[wl].reset_index(inplace=True)
#    vars()[wl]['all_crt'] = vars()[wl]['pvalue_b']*vars()[wl]['pvalue_fw']*(1 - vars()[wl]['Rel_err_fw'])*(1 - vars()[wl]['Rel_err_b'])
#Red_filtered = Red_phase[(Red_phase.MSEf < 80)]
#Blue_filtered = Blue_phase[(Blue_phase.MSEf < 950)]

Red_filtered = Red_phase[(Red_phase.MSEb < 0.0006) & (Red_phase.Rel_err_fw <= 0.05)]
Blue_filtered = Blue_phase[(Blue_phase.MSEb < 0.004 ) & (Blue_phase.Rel_err_fw <= 0.05 )]
Red_filtered.to_pickle(disr_dt+'Red_filtered.pkl')
Blue_filtered.to_pickle(disr_dt+'Blue_filtered.pkl')
#Red_filtered = Red_phase[(Red_phase.MSEb < 0.0006) & (Red_phase.MSEf < 150)]
#Blue_filtered = Blue_phase[(Blue_phase.MSEb < 0.004 ) & (Blue_phase.MSEf < 460)]


#%%
for mdls in file_names:
    if (mdls not in Blue_phase.Mdl) and (mdls not in Red_phase.Mdl):
        del vars()[mdls+'_mx']
        del vars()[mdls+'_eff']


#%%
Pm_obj=[]
for pm_id in file_names:
    pm = vars()[pm_id+'_mx']
    Pm_obj.append(pm)

#%%
# Comparing models to DISR AEROLO P11 to find the best fitting model


Blue = pd.read_pickle(disr_dt+'Blue.pkl')
Red = pd.read_pickle(disr_dt+'Red.pkl')
Hyg_Blue = pd.read_pickle(disr_dt+'Hyg_Blue.pkl')
Hyg_Red = pd.read_pickle(disr_dt+'Hyg_Red.pkl')

def compare_phase( wl, pm_id ):


    if wl == 'Blue':
        lmd=0.4909
    elif wl == 'Red':
        lmd=0.9348
    Hyg = pd.read_pickle(disr_dt+'Hyg_'+wl+'.pkl')

    pm = eval(pm_id+'_mx')


    sp = pm_id[7:12]
    sp = float(".".join(sp[0:2]) + sp[2:])
    N = int(pm_id[pm_id.find('pm')+2:pm_id.find('_')])

    sp = pm_id[7:12]
    sp = float(".".join(sp[0:2]) + sp[2:])

    n_real = pm_id[13:16]
    n_real = float(".".join(n_real[0:2]) + n_real[2:])

    n_img = pm_id[17:22]
    n_img = float(".".join(n_img[0:2]) + n_img[2:])

    A = Hyg.set_index('theta').join(pm[['theta','P11']].set_index('theta'), how='inner', lsuffix='obs', rsuffix='mdl')
    KSf = ks_2samp(A.P11obs[:10], A.P11mdl[:10])
    KSb = ks_2samp(A.P11obs[17:36], A.P11mdl[17:36])
    ASf = anderson_ksamp([A.P11obs[:10], A.P11mdl[:10] ])
    ASb = anderson_ksamp([A.P11obs[17:36], A.P11mdl[17:36] ])
    #R2f = linregress(A.P11obs[0:2], A.P11mdl[0:2])
    #R2b= linregress(A.P11obs[17:36], A.P11mdl[17:36])
    MSEf = ((A.P11obs[:10] - A.P11mdl[:10])**2).mean()
    MSEb = ((A.P11obs[17:36] - A.P11mdl[17:36])**2).mean()
    Rerr_fw = (abs(A.P11obs[:10] - A.P11mdl[:10])/A.P11obs[:10]).mean()
    Rerr_b = (abs(A.P11obs[17:36] - A.P11mdl[17:36])/A.P11obs[17:36]).mean()
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

    aw['KSpvalue_b'] = KSb.pvalue
    aw['KSpvalue_fw'] = KSf.pvalue
    #aw['pvalue'] = (KSf.pvalue*KSb.pvalue)
    #aw['KSb'] = KSb.statistic
    #aw['KSf'] = KSf.statistic
    #aw['KS'] = (KSf.statistic + KSb.statistic)/2.0

    aw['ASb'] = ASb.significance_level
    aw['ASf'] = ASf.significance_level
    #aw['AS'] = ASb.significance_level*ASf.significance_level
    #aw['Rel_err'] = (Rerr_fw*Rerr_b)
    aw['Rel_err_fw'] = Rerr_fw
    aw['Rel_err_b'] = Rerr_b
    aw['MSEf'] = MSEf
    aw['MSEb'] = MSEb
    aw['Wave_Length'] = wl

    return aw

#for wl in ['Blue', 'Red']:
#    PhaseBlue = []
#    PhaseRed = []
#    Hyg = vars()['Hyg_'+wl]
if __name__ == '__main__':
    for wl in ['Blue', 'Red']:
        p = Pool(4)
        func = partial(compare_phase, wl)
    #        Phase = p.map(func, Pm_obj)
        Phase = p.map(func, file_names)
#
        vars()[wl+'_phase'] = pd.DataFrame(Phase)
        vars()[wl+'_phase']['Filter'] = (1/vars()[wl+'_phase']['MSEf'])*vars()[wl+'_phase']['ASb']

#    vars()[wl] = vars()[wl].set_index('Mdl').join(dt.set_index('Mdl'), how = 'outer')
#    vars()[wl].reset_index(inplace=True)
#    vars()[wl]['all_crt'] = vars()[wl]['pvalue_b']*vars()[wl]['pvalue_fw']*(1 - vars()[wl]['Rel_err_fw'])*(1 - vars()[wl]['Rel_err_b'])
#Red_filtered = Red_phase[(Red_phase.MSEb < 0.00039) & (Red_phase.MSEf < 14)]
#Blue_filtered = Blue_phase[(Blue_phase.MSEb < 0.004 ) & (Blue_phase.MSEf < 800)]

#%%
#Red_filtered = Red_phase[(Red_phase.MSEb > 0.00039) & (Red_phase.MSEf < 80)]
#Blue_filtered = Blue_phase[(Blue_phase.MSEb < 0.004 ) & (Blue_phase.MSEf < 950)]

Blue = []
Red = []
for wl in ['Blue', 'Red']:
    for pm_id in vars()[wl+'_filtered'].Mdl:

        N = int(pm_id[pm_id.find('pm')+2:pm_id.find('_')])

        sp = pm_id[7:12]
        sp = float(".".join(sp[0:2]) + sp[2:])

        n_real = pm_id[13:16]
        n_real = float(".".join(n_real[0:2]) + n_real[2:])

        n_img = pm_id[17:22]
        n_img = float(".".join(n_img[0:2]) + n_img[2:])

        pm_eff = vars()[pm_id+'_eff']
        pm = vars()[pm_id+'_mx']
        maxpol_pm = max(-pm.P12/pm.P11)

        m = complex(n_real, n_img)
        m0 = abs((m**2-1)/(m**2+2))
        ASb = eval(wl+'_filtered')[eval(wl+'_filtered').Mdl == pm_id].ASb.values[0]
        MSEb = eval(wl+'_filtered')[eval(wl+'_filtered').Mdl == pm_id].MSEb.values[0]
        MSEf = eval(wl+'_filtered')[eval(wl+'_filtered').Mdl == pm_id].MSEf.values[0]
        Rel_err_b = eval(wl+'_filtered')[eval(wl+'_filtered').Mdl == pm_id].Rel_err_b.values[0]
        Rel_err_fw = eval(wl+'_filtered')[eval(wl+'_filtered').Mdl == pm_id].Rel_err_fw.values[0]

        # 85–90% at 491 nm
        if maxpol_pm >= 0.85 and maxpol_pm <= 0.90:

            sw={}

            sw['N'] = N
            sw['sp'] = sp
            sw['Rm'] = sp*0.4909/(2*np.pi)
            sw['nr'] = n_real
            sw['ni'] = n_img
            sw['taus'] = pm_eff.taus[0]
            sw['taua'] = pm_eff.taua[0]
            sw['qa_pm'] = pm_eff.qa[0]
            sw['qs_pm'] = pm_eff.qs[0]
            sw['cs_pm'] = pm_eff.cs[0]

    #                sw['srf'] = srf
    #                sw['corr_sca'] = corr_sca
            sw['m0'] = m0
            sw['maxpol'] = maxpol_pm
            sw['P11'] = pm.P11
            sw['Mdl'] = pm_id
            sw['ASb'] = ASb
            sw['MSEb'] = MSEb
            sw['MSEf'] = MSEf
            sw['Rel_err_fw'] = Rel_err_fw
            sw['Rel_err_b'] = Rel_err_b

            Blue.append(sw)


        # 98% at 934 nm
        elif maxpol_pm >= 0.977 and maxpol_pm <= 0.983:
            sw={}

            sw['N'] = N
            sw['sp'] = sp
            sw['Rm'] = sp*0.9348/(2*np.pi)
            sw['nr'] = n_real
            sw['ni'] = n_img
            sw['taus'] = pm_eff.taus[0]
            sw['taua'] = pm_eff.taua[0]
            sw['qa_pm'] = pm_eff.qa[0]
            sw['qs_pm'] = pm_eff.qs[0]
            sw['cs_pm'] = pm_eff.cs[0]
    #                sw['srf'] = srf
            sw['m0'] = m0
            sw['maxpol'] = maxpol_pm
            sw['P11'] = pm.P11
            sw['Mdl'] = pm_id
            sw['ASb'] = ASb
            sw['MSEb'] = MSEb
            sw['MSEf'] = MSEf
            sw['Rel_err_fw'] = Rel_err_fw
            sw['Rel_err_b'] = Rel_err_b
            Red.append(sw)

Blue = pd.DataFrame(Blue)
Red = pd.DataFrame(Red)

Blue.to_pickle(disr_dt+'Blue.pkl')
Red.to_pickle(disr_dt+'Red.pkl')
#%%

#Hyg_Blue = pd.read_pickle(disr_dt+'Hyg_Blue.pkl')
#Blue = pd.read_pickle(disr_dt+'Blue.pkl')
#Red = pd.read_pickle(disr_dt+'Red.pkl')
#Red_filtered = Red_phase[(Red_phase.MSEb < 0.00039) & (Red_phase.MSEf < 80)]
#Blue_filtered = Blue_phase[(Blue_phase.MSEb < 0.004 ) & (Blue_phase.MSEf < 950)]
ssa = pd.read_pickle(disr_dt+'SSA.pkl')

for wl in ['Blue', 'Red']:
    w0144_Rerr = []
    w080_Rerr = []
    for _alt in ['144', '80']:
        if _alt == '144':
            w0DISR = 'w0144'
        else:
            w0DISR = 'w080'

        for pm_id in eval(wl).Mdl:
            pm_eff = vars()[pm_id+'_eff']
            w0mdl = pm_eff.qs[0]/pm_eff.qe[0]
            if wl == 'Blue':
                w0 = ssa[ssa.lmd == 491 ][w0DISR].values
                _lmd = 0.4909 # extra dec. just to be more accurate for monomer_size
            elif wl == 'Red':
                w0 = ssa[ssa.lmd == 934 ][w0DISR].values
                _lmd = 0.9348 # extra dec. just to be more accurate for monomer_size

            rel_err = abs(w0 - w0mdl )/w0
            eval('w0'+_alt+'_Rerr').append(rel_err)
    eval(wl)['w0144_Rerr'] = w0144_Rerr
    eval(wl)['w080_Rerr'] = w080_Rerr
    vars()[wl+'144'] = eval(wl)[eval(wl)['w0144_Rerr'] <= 0.05]
    vars()[wl+'80'] = eval(wl)[eval(wl)['w080_Rerr'] <= 0.05]
Blue.to_pickle(disr_dt+'Blue.pkl')
Red.to_pickle(disr_dt+'Red.pkl')
#%%
Hyg_Blue = pd.read_pickle(disr_dt+'Hyg_Blue.pkl')
Hyg_Red = pd.read_pickle(disr_dt+'Hyg_Red.pkl')
Blue = pd.read_pickle(disr_dt+'Blue.pkl')
Red = pd.read_pickle(disr_dt+'Red.pkl')
for wl in ['Blue', 'Red']:
    for alt in ['144', '80']:
        vars()[wl+alt] = eval(wl)[eval(wl)[f'w0{alt}_Rerr'] <= 0.12]
        vars()[wl+alt] = eval(wl+alt)[eval(wl+alt)['Rel_err_b'] <= 0.155]

        vars()[wl+alt]['filter'] = eval(wl+alt)['Rel_err_fw']*eval(wl+alt)['Rel_err_b']*eval(wl+alt)[f'w0{alt}_Rerr']
        vars()[wl+alt]['Ragg'] = eval(wl+alt)['Rm']*eval(wl+alt)['N']**(1.0/3.)
#        vars()[wl+alt]['Rel_err_fw'] = np.sqrt(eval(wl+alt)['MSEf']/(Hyg_Blue.P11[0]**2))
#        vars()[wl+alt]['Rel_err_fw'] = np.sqrt(eval(wl+alt)['MSEf']/(Hyg_Blue.P11[0]**2))
Red144=Red144[Red144.Rel_err_b <= 0.1]
Red80=Red80[Red80.Rel_err_b <= 0.1]

#%%
# Calculating New SSA From

w0abv200 = 0.935-0.41*(np.log(ssa.lmd/800))**2
w0bel80 = (0.565 + w0abv200)/1.5
w0200_80 = lambda z: w0abv200 + (200-z)*(w0bel80 - w0abv200)/(200-80)

