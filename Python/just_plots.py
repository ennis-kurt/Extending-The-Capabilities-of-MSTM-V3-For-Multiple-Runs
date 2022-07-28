#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 09:56:53 2019

@author: cihat
"""
from pathlib import Path
import numpy as np
import pandas as pd
#import time as tm
import linecache as gl
import glob
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import platform
op_sys = platform.system()
if op_sys == 'Windows':
    dtdir = 'C:\\Users\\kurt_\\PARAM DATA\\'
    disr_dt = 'C:\\Users\\kurt_\\Dropbox\\Code\\'
    dt_directory='C:\\Users\\kurt_\\Dropbox\\Code\\special\\data\\'
    _sl = '\\'
elif op_sys == 'Linux':
    dtdir = '/home/cihat/programs/gdl/'
    disr_dt = '/home/cihat/Dropbox/code/'
    dt_directory = '/home/cihat/Dropbox/code/special/data/'
    _sl = '/'
os.chdir(f'{disr_dt}{_sl}special{_sl}data{_sl}')
from constraints import *
  #%% Plots


_pm = ['2575_03277_158_00040', '2950_05120_200_00660']
_chn = 'Blue'
for pm_id in _pm:
    file=glob.glob(dtdir+'final{}newpm{}.dat'.format(_sl, pm_id))
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


os.chdir(dtdir)



Hyg_Blue = pd.read_pickle(disr_dt+'Hyg_Blue.pkl')
Hyg_Red = pd.read_pickle(disr_dt+'Hyg_Red.pkl')
th = Hyg_Blue.theta
theta = np.arange(0,181)
with plt.style.context(('seaborn-poster')):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(18, 12))
    if _chn == 'Blue':
        axes[0,0].plot(th[:10],(Hyg_Blue.P11)[:10], label='DISR')
        axes[0,0].plot( theta[:10], (pm2575_03277_158_00040_mx.P11)[:10], label='Model')

        axes[0,0].set_title('Blue 2575_03277_158_00040')
        axes[0,0].legend()

        axes[0,1].plot(th, np.log10(Hyg_Blue.P11), label='DISR')
        axes[0,1].plot(theta, np.log10(pm2575_03277_158_00040_mx.P11), label='Model')
        axes[0,1].set_ylim(-1.0, 2.8)
        axes[0,1].set_title('Blue 2575_03277_158_00040')
        axes[0,1].legend()

        axes[1,0].plot(th[:10],(Hyg_Blue.P11)[:10], label='DISR')
        axes[1,0].plot( theta[:10], (pm2825_02941_165_00040_mx.P11)[:10], label='Model')
        axes[1,0].set_title('Blue 2825_02941_165_00040')
        axes[1,0].legend()
        #newpm2825_02941_165_00040_mx[65:] = newpm2825_02941_165_00040_mx[65:]*0.8333
        axes[1,1].plot(th, np.log10(Hyg_Blue.P11), label='DISR')
        axes[1,1].plot(theta, np.log10(pm2825_02941_165_00040_mx.P11), label='Model')
        axes[1,1].set_title('Blue 2825_02941_165_00040')
        axes[1,1].legend()
    elif _chn == 'Red':
        axes[0,0].plot(th[:10],(Hyg_Red.P11)[:10], label='DISR')
        axes[0,0].plot( theta[:10], (pm2575_03277_158_00040_mx.P11)[:10], label='Model')
        axes[0,0].set_ylim(20, 200)

        axes[0,0].set_title('Red 2575_03277_158_00040')
        axes[0,0].legend()

        axes[0,1].plot(th, np.log10(Hyg_Red.P11), label='DISR')
        axes[0,1].plot(theta, np.log10(pm2575_03277_158_00040_mx.P11), label='Model')
        axes[0,1].set_ylim(-1.0, 2.4)
        axes[0,1].set_title('Red 2575_03277_158_00040')
        axes[0,1].legend()

        axes[1,0].plot(th[:10],(Hyg_Red.P11)[:10], label='DISR')
        axes[1,0].plot( theta[:10], (pm2825_02941_165_00040_mx.P11)[:10], label='Model1700')
        axes[1,0].set_title('Red 2825_02941_165_00040')
        axes[0,0].set_ylim(20, 200)
        axes[1,0].legend()
        #newpm2825_02941_165_00040_mx[65:] = newpm2825_02941_165_00040_mx[65:]*0.8333
        axes[1,1].plot(th, np.log10(Hyg_Red.P11), label='DISR')
        axes[1,1].plot(theta, np.log10(pm2825_02941_165_00040_mx.P11), label='Model')
        axes[0,1].set_ylim(-1.0, 2.4)
        axes[1,1].set_title('Red 2825_02941_165_00040')
        axes[1,1].legend()
    plt.show()
    plt.close()

#%% Single plots

for combined in [True, False]:

    pm_dict = {'Red': {'lmd': 0.9348,'pm_id': ['3300_02857_165_00060','3575_02773_174_00100']}, 'Blue': {'lmd': 0.4909, 'pm_id': ['3325_05120_200_01260','2825_05280_198_01260']}}
    for _chn in pm_dict:
        #'Blue kesin : 3325_05120_200_01260' Red Kesin: 3300_02857_165_00060
        if combined:
            pm_id = pm_dict[_chn]['pm_id'][0]

        else:
            pm_id = pm_dict[_chn]['pm_id'][1]

        lmd = pm_dict[_chn]['lmd']


        sp = pm_id[5:10]
        sp = float(".".join(sp[0:2]) + sp[2:])

    #    Rm = np.around(sp*lmd/(2*np.pi), decimals=4)
        Rm = sp*lmd/(2*np.pi)
        Rm = f'{Rm}'[:5]
        N = int(pm_id[0:4])

        n_real = pm_id[11:14]
        n_real = float(".".join(n_real[0:2]) + n_real[2:])

        n_img = pm_id[15:20]
        n_img = float(".".join(n_img[0:2]) + n_img[2:])

        file=glob.glob(dtdir+'final{}newpm{}.dat'.format(_sl, pm_id))
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


        os.chdir(disr_dt)



        Hyg_Blue = pd.read_pickle(disr_dt+'Hyg_Blue.pkl')
        Hyg_Red = pd.read_pickle(disr_dt+'Hyg_Red.pkl')
        th = Hyg_Blue.theta
        theta = eval(f'pm{pm_id}_mx').theta
        u = 0
        v = -1
        x = 0
        w = -1
        th = th[u:v]
        theta = theta[x:w]
        hyg = np.log10(eval(f'Hyg_{_chn}').P11[u:v])
        _pc = 0.1
        _pc0 = 0
        hyg5pc_plus =  np.log10(eval(f'Hyg_{_chn}').P11[u:v] + eval(f'Hyg_{_chn}').P11[u:v]*_pc)
        hyg5pc_minus = np.log10(eval(f'Hyg_{_chn}').P11[u:v] - eval(f'Hyg_{_chn}').P11[u:v]*_pc)
        pm5pc_plus =  np.log10(eval(f'pm{pm_id}_mx').P11[x:w] + eval(f'pm{pm_id}_mx').P11[x:w]*_pc0)
        pm5pc_minus = np.log10(eval(f'pm{pm_id}_mx').P11[x:w] - eval(f'pm{pm_id}_mx').P11[x:w]*_pc0)
        _pm = np.log10(eval(f'pm{pm_id}_mx').P11[x:w])

        with plt.style.context(('seaborn-poster')):
            fig, axes = plt.subplots(tight_layout=True, figsize=(7,5))
            axes.plot(th, hyg, lw = 1.3, alpha = 0.8, color = 'blue', label='DISR')
            axes.fill_between(th, hyg5pc_minus, hyg5pc_plus, alpha = 0.2, color = 'blue', label='_nolegend_')
            axes.plot(theta, _pm,lw = 2,marker = 'o', alpha=0.2,markersize = 7, color = 'red', label = 'P. Model')
            axes.plot(theta, _pm,lw = 2, alpha=0.8, color = 'red', label = '_')
            axes.fill_between(theta, pm5pc_minus, pm5pc_plus,alpha=0.2, color = 'red',label='_nolegend_')
        #    axes.plot(theta, np.log10(eval(f'pm{pm_id}_mx').P11),marker='o',alpha=0.4, label='Model', color = 'orange')
        #    axes.set_ylim(-1, 2.7)
            axes.set_title(f'{_chn} Best Fitting Aggregate', fontweight='bold', fontsize=18)
            axes.legend()
            ant_dict = {'N': f'{N:.1e}'[:3]+f'$*10^3$',"$R_m$": Rm, "$n_r$": n_real,"$n_i$": n_img}
#            ant_dict = {'N': int(np.around(N*1e-4,2)*1e4),"$R_m$": Rm, "$n_r$": n_real,"$n_i$": n_img}
            for i,ant in enumerate(ant_dict):
                i=0.6 - i*0.05
                plt.annotate(f'{ant} = {ant_dict[ant]}', xy=(0.740,i), xycoords = ('figure fraction'), fontsize = (16), color = 'maroon')
            print (sp*lmd/(2*np.pi))

            plt.show()
            plt.close()

#%%Best single model polarization plot
for combined in [True, False]:
    pm_dict = {'Red': {'lmd': 0.9348,'pm_id': ['3300_02857_165_00060','3575_02773_174_00100']}, 'Blue': {'lmd': 0.4909, 'pm_id': ['3325_05120_200_01260','2825_05280_198_01260']}}

    sns.set(context='talk',font_scale=1.5, style = 'whitegrid')

    #sns.xkcd_palette(['red','blue'])
    fig, axes = plt.subplots(tight_layout=True, figsize=(8.5,7))
    for _chn in pm_dict:
        #'Blue kesin : 3325_05120_200_01260' Red Kesin: 3300_02857_165_00060
        if combined:
            pm_id = pm_dict[_chn]['pm_id'][0]

        else:
            pm_id = pm_dict[_chn]['pm_id'][1]

        lmd = pm_dict[_chn]['lmd']


        sp = pm_id[5:10]
        sp = float(".".join(sp[0:2]) + sp[2:])

    #    Rm = np.around(sp*lmd/(2*np.pi), decimals=4)
        Rm = sp*lmd/(2*np.pi)
        Rm = f'{Rm}'[:5]
        N = int(pm_id[0:4])

        n_real = pm_id[11:14]
        n_real = float(".".join(n_real[0:2]) + n_real[2:])

        n_img = pm_id[15:20]
        n_img = float(".".join(n_img[0:2]) + n_img[2:])

        file=glob.glob(dtdir+'final{}newpm{}.dat'.format(_sl, pm_id))
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
            del(rw)

            # Let's convert the string values to numeric all at once
            pm = pm.apply(pd.to_numeric)
            pm['theta'] = np.arange(0, 181)


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

        maxpol =max(-pm.P12/pm.P11)
        theta_maxpol = pm.theta[-pm.P12/pm.P11 == maxpol].values[0]
        os.chdir(disr_dt)
        theta = eval(f'pm{pm_id}_mx').theta
        axes.plot(theta, (-pm.P12/pm.P11), linewidth=3, alpha=0.5, color=_chn, label=_chn+f' max_pol: {maxpol:.2f}')
#        axes.set_title('N : '+f'{N:.1e}'[:3]+f'$ x 10^3$ $R_m$ : {Rm}')
        axes.set_title('The Best Fitting Aggregate')
        axes.plot(theta_maxpol, maxpol, marker='*', markeredgecolor=None, color=_chn )
        plt.legend(loc=1,prop={'size': 17} )



#%% ALL Phase Functions

Blue_plotting = Blue[Blue.Rel_err_b < 0.11]
Red_plotting = Red_flt
#some of the runs are missing
k=0
src = f'{dtdir}{_sl}final{_sl}'
pc_b = 0.1
pc_f = 0.05
w = 11
x = 11
v = 110
u = 21
mdl_clr = '#E94F4F'
meas_clr = 'purple'
sub_fnt = 20
fnt = 40
SMALL_SIZE = 14
m_size = 4
lw_pm = 0.4
err=0
missing = list()
for i in Red_plotting.Mdl:
    my_file = Path(f'{src}new{i}.dat')
    if my_file.is_file():
        a=1
    else:
        missing.append(i)
        k+=1

print(f'Number of file available is {k}')

for k in missing:
    Red_plotting  = Red_plotting[Red_plotting.Mdl != k]
Hyg_Blue = pd.read_pickle(disr_dt+'Hyg_Blue.pkl')
Hyg_Red = pd.read_pickle(disr_dt+'Hyg_Red.pkl')
th = Hyg_Blue.theta
theta = np.arange(0, 181)
w = 11
x = 11
v = 100
u = 20
mdl_clr = '#E94F4F'
meas_clr = 'Blue'
wl = 'Blue'
sub_fnt = 14
fnt = 26
SMALL_SIZE = 16
m_size = 3
ax_font_size = 22
err = 0
with plt.style.context(('seaborn-poster')):
    for wl in ['Red']:
        hyg5pc_plus =  np.log10(eval(f'Hyg_{wl}').P11 + eval(f'Hyg_{wl}').P11*pc_b)
        hyg5pc_minus = hyg5pc_minus_b = np.log10(eval(f'Hyg_{wl}').P11 - eval(f'Hyg_{wl}').P11*pc_b)
        hyg5pc_plus[:w] = np.log10(eval(f'Hyg_{wl}').P11[:w] - eval(f'Hyg_{wl}').P11[:w]*pc_f)
        hyg5pc_minus[:w] = np.log10(eval(f'Hyg_{wl}').P11[:w] + eval(f'Hyg_{wl}').P11[:w]*pc_f)

        mpl.rc('figure', figsize = (8,6))
        fig = plt.figure()
#        sn.set_context(font_scale=2)
        for pm_id in eval(f'{wl}').Mdl[:100]:
            try:
                par = open(f'{dtdir}final/new{pm_id}.dat')
            except IOError:
                err+=1
            else:

                with par:
                    pm = list()
                    mpl.rc('ytick', labelsize=SMALL_SIZE)
                    mpl.rc('xtick', labelsize=SMALL_SIZE)
                    mpl.rc('xtick', labelsize=SMALL_SIZE)


                    for i,line in enumerate(par):
                        if i==1:
                            dline = line.strip()
                            dline = dline.split()
                            qabs = float(dline[0])
                            qsca = float(dline[1])
                            qext = float(dline[2])
                            csca = float(dline[3])
                            cabs = float(dline[4])

                        elif i >=3 and i <= 184:
                            try:

                                columns = line.strip()
                                columns = columns.split()
                                rw = {}
                                rw['P11'] = columns[0]
                                rw['P12'] = columns[1]
                                rw['P22'] = columns[2]
                                rw['P33'] = columns[3]
                                rw['P34'] = columns[4]
                                rw['P44'] = columns[5]

                                pm.append(rw)
                            except IndexError:
                                print(f'{pm_id} is corrupted')
                                continue


                        else:
                            continue
                                        # Now Converting to a Dataframe
                    pm = pd.DataFrame(pm)
                    pm = pm.apply(pd.to_numeric)
                    sp = pm_id[7:12]
                    sp = float(".".join(sp[0:2]) + sp[2:])
                    N = int(pm_id[pm_id.find('pm')+2:pm_id.find('_')])
                    n_real = pm_id[13:16]
                    n_real = float(".".join(n_real[0:2]) + n_real[2:])
                    n_img = pm_id[17:22]
                    n_img = float(".".join(n_img[0:2]) + n_img[2:])

                ax1 = fig.add_axes([0,0,1,1])
                ax2 = fig.add_axes([0.49,0.63,0.45,0.35])
                ax3 = fig.add_axes([0.49,0.2,0.45,0.35])

                ax1.plot(theta, (np.log10(pm.P11)), linewidth=lw_pm, alpha=1, color=mdl_clr)
                ax2.plot(theta[v:], pm.P11[v:],linewidth=lw_pm, alpha=1, color=mdl_clr)
                ax3.plot(theta[:w], pm.P11[:w],linewidth=lw_pm, alpha=1, color=mdl_clr)
        mpl.rcdefaults()
        mpl.rc('axes', titleweight='bold')

        ax1.plot(th, np.log10(eval(f'Hyg_{wl}').P11), alpha = 0.5, linewidth = 1, color = meas_clr, marker='D', markersize=m_size,markerfacecolor='purple',markeredgecolor='black') #, marker='o', markersize=10,markerfacecolor='red',markeredgecolor='black'
        ax1.fill_between(th, hyg5pc_minus, hyg5pc_plus, alpha = 0.2, color = 'blue', label='_nolegend_')
        ax2.plot(th[u:], eval(f'Hyg_{wl}').P11[u:], color = meas_clr, marker='D', markersize=m_size, alpha = 0.5, linewidth = 1)
        ax2.fill_between(th[u:], 10**(hyg5pc_minus[u:]), 10**(hyg5pc_plus[u:]), alpha = 0.2, color = 'blue', label='_nolegend_')
        ax3.plot(th[:x], eval(f'Hyg_{wl}').P11[:x],marker='D', markersize=m_size, alpha = 0.5, linewidth = 1, color = meas_clr)
        ax3.fill_between(th[:x], 10**(hyg5pc_minus[:x]), 10**(hyg5pc_plus[:x]), alpha = 0.2, color = 'blue', label='_nolegend_')
#        ax2.set_title('Backscattering', fontsize = sub_fnt)
#        ax3.set_title('Forward Scattering', fontsize = sub_fnt)
        ax1.set_title(f'{wl} Phase Function', fontsize = fnt)
        ax1.set_xlabel(' $\Theta $ ', fontsize=ax_font_size)
        ax1.set_ylabel(' $\log\ P_{11}$ ', fontsize=ax_font_size)

        for ax in [ax2, ax3]:
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)


        plt.savefig(f'{disr_dt}figs{_sl}{wl}_all.png')
        plt.show()
        plt.close()
print(f'Number of missing files: {err}')

#%% Plottimg all polarization

Blue_plotting = Blue_flt[Blue_flt.Rel_err_b < 0.14]
Red_plotting = Red_flt
#some of the runs are missing
k=0
src = f'{dtdir}{_sl}final{_sl}'
missing = list()
for i in Red_plotting.Mdl:
    my_file = Path(f'{src}new{i}.dat')
    if my_file.is_file():
        a=1
    else:
        missing.append(i)
        k+=1

print(f'Number of file available is {k}')

for k in missing:
    Red_plotting  = Red_plotting[Red_plotting.Mdl != k]
Hyg_Blue = pd.read_pickle(disr_dt+'Hyg_Blue.pkl')
Hyg_Red = pd.read_pickle(disr_dt+'Hyg_Red.pkl')
th = Hyg_Blue.theta
theta = np.arange(0, 181)
w = 11
x = 21
v = 100
u = 15
mdl_clr = '#E94F4F'
meas_clr = 'Blue'
wl = 'Blue'
sub_fnt = 14
fnt = 22
SMALL_SIZE = 12
m_size = 6
err = 0
with plt.style.context(('seaborn-poster')):
    for wl in ['Red']:
        mpl.rc('figure', figsize = (12,8))
        fig = plt.figure()
        for pm_id in eval(f'{wl}').Mdl[:2]:
            try:
                par = open(f'{dtdir}final/new{pm_id}.dat')
            except IOError:
                err+=1
            else:

                with par:
                    pm = list()
                    mpl.rc('ytick', labelsize=SMALL_SIZE)
                    mpl.rc('xtick', labelsize=SMALL_SIZE)
                    mpl.rc('xtick', labelsize=SMALL_SIZE)


                    for i,line in enumerate(par):
                        if i==1:
                            dline = line.strip()
                            dline = dline.split()
                            qabs = float(dline[0])
                            qsca = float(dline[1])
                            qext = float(dline[2])
                            csca = float(dline[3])
                            cabs = float(dline[4])

                        elif i >=3 and i <= 184:
                            try:

                                columns = line.strip()
                                columns = columns.split()
                                rw = {}
                                rw['P11'] = columns[0]
                                rw['P12'] = columns[1]
                                rw['P22'] = columns[2]
                                rw['P33'] = columns[3]
                                rw['P34'] = columns[4]
                                rw['P44'] = columns[5]

                                pm.append(rw)
                            except IndexError:
                                print(f'{pm_id} is corrupted')
                                continue


                        else:
                            continue
                                        # Now Converting to a Dataframe
                    pm = pd.DataFrame(pm)
                    pm = pm.apply(pd.to_numeric)
                    sp = pm_id[7:12]
                    sp = float(".".join(sp[0:2]) + sp[2:])
                    N = int(pm_id[pm_id.find('pm')+2:pm_id.find('_')])
                    n_real = pm_id[13:16]
                    n_real = float(".".join(n_real[0:2]) + n_real[2:])
                    n_img = pm_id[17:22]
                    n_img = float(".".join(n_img[0:2]) + n_img[2:])

                    ax1 = fig.add_axes([0,0,1,1])
                    try:
                        ax1.plot(theta, (-pm.P12/pm.P11), linewidth=0.1, alpha=1, color='gray')
                    except ValueError:
                        err+=1
                        continue
        mpl.rcdefaults()
        mpl.rc('axes', titleweight='bold')

        if wl == 'Blue':
            mxpol1 = 0.85
            mxpol2 = 0.90
        else:
            mxpol1 = 0.97
            mxpol2 = 0.983
        ax1.fill_between(theta, mxpol1, mxpol2, color=meas_clr, alpha = 0.2) #, marker='o', markersize=10,markerfacecolor='red',markeredgecolor='black'

        ax1.set_title(f'{wl} Linear Polarization', fontsize = fnt)
        ax1.set_ylim(-0.05, 1)
        plt.show()
        plt.close()
print(f'Number of missing files: {err}')

#%% Violin Plots

# Indpendent filter
Flt = [Blue_flt, Red_flt]
Flt = pd.concat(Flt, sort=False)
_x = pd.Series([' ']*np.size(Flt.Mdl))

_ids=[]
_vls=[]
_include = [ 'N', 'Rm', 'Ragg']
for i in Flt:
    if i in _include:
        _vls.append(i)
    else:
        _ids.append(i)
        sn.set(style="whitegrid")
        sn.set_context("paper", font_scale=2)
Flt = pd.melt(Flt, id_vars = _ids, value_vars = _vls, value_name='Vars')
Flt['a'] = _x
g = sn.catplot(x="a", y="Vars", hue="Wave_Length", data=Flt, kind="violin", split=True,
               col='variable', sharex=False, sharey=False , palette=['#87CEFA','#FF6347'], inner=None)

#g.map(sns.violinplot,x="variable", y="Vars", hue="Wave_Length", data=Flt, split=True,
#                   inner="quart")margin_titles=True

#%% Violin Plots

# Combined filters
# 200 km

for alt in ['200', '80new']:
    Flt = [eval(f'Blue{alt}'), eval(f'Red{alt}')]
    Flt = pd.concat(Flt)
    _x = pd.Series([' ']*np.size(Flt.Mdl))
    Flt['x'] = _x
    _ids=[]
    _vls=[]
    _include = [ 'nr', 'ni']
    for i in Flt:
        if i in _include:
            _vls.append(i)
        else:
            _ids.append(i)
            sn.set(style="whitegrid")
            sn.set_context("paper", font_scale=2)
    Flt = pd.melt(Flt, id_vars = _ids, value_vars = _vls, value_name='Vars')
    Flt['x'] = Flt.where(Flt.x == 'nan',' ')
    if alt == '80new':
        _ct = 0.85
    else:
        _ct=0.85
    g = sn.catplot(x="x", y="Vars", hue="Wave_Length", data=Flt, kind="violin", split=True,cut=_ct,
                   col='variable', sharex=False, sharey=False , palette=['#87CEFA','#FF6347'], inner='quart')

#g.map(sns.violinplot,x="variable", y="Vars", hue="Wave_Length", data=Flt, split=True,
#                   inner="quart")margin_titles=True

#%% Violin Plots
# Refractive index
# Combined filters
# 200 km

for wl in ['Blue', 'Red']:

    Flt200 = eval(f'{wl}200').copy()
    Flt200['alt'] = pd.Series(['200']*np.size(Flt200.Mdl))
    Flt80 = eval(f'{wl}80new').copy()
    Flt80['alt'] = pd.Series(['80']*np.size(Flt80.Mdl))
    Flt = [Flt200, Flt80]
    Flt = pd.concat(Flt)
    _x = pd.Series([' ']*np.size(Flt.Mdl))
    Flt['x'] = _x
    _ids=[]
    _vls=[]
    _include = [ 'nr', 'ni']
    for i in Flt:
        if i in _include:
            _vls.append(i)
        else:
            _ids.append(i)
            sn.set(style="whitegrid")
            sn.set_context("paper", font_scale=2)
    Flt = pd.melt(Flt, id_vars = _ids, value_vars = _vls, value_name='Vars')
    Flt['x'] = Flt.where(Flt.x == 'nan',' ')
    if wl == 'Blue':

        pltt = ['blue','#87CEFA']
    else:
        pltt = ['#ff9999','#ff3333']
    g = sn.catplot(x="x", y="Vars", hue="alt", data=Flt, kind="violin", split=False, scale='count',
                   col='variable', sharex=False, sharey=False , palette = pltt, inner = 'quart')

#g.map(sns.violinplot,x="variable", y="Vars", hue="Wave_Length", data=Flt, split=True,
#%% Hex Plot

# Refractive Index
# 200 km
for alt in ['200', '80new']:
    for wl in ['Blue', 'Red']:
        for n in ['nr','ni']:
            with pd.option_context('mode.chained_assignment', None):
                Ragg = eval(wl+alt)['Rm']*eval(wl+alt)['N']**(1.0/3.)
            x = eval(f'{wl}{alt}')[f'{n}']
            y = eval(f'{wl}{alt}')[f'w0{alt}_Rerr']#[f'w0{alt}_Rerr']
            if wl == 'Blue':
                clr = 'blue'
            elif wl == 'Red':
                clr = 'red'
            sns.jointplot(x, y, kind="hex", color=clr)#"#4CB391")
            plt.title(f'{wl}')
            plt.show()
#            plt.close()
#                   inner="quart")margin_titles=True
#%% Violin Plots

# Refractive Index
# 200 km
#for alt in ['200', '80new']:
for wl in ['Blue', 'Red']:
    for n in ['nr', 'ni']:
        try:
            eval(wl).Ragg
        except AttributeError:
            with pd.option_context('mode.chained_assignment', None):
                eval(wl)['Ragg'] = eval(wl)['Rm']*eval(wl)['N']**(1.0/3.)

        x = eval(f'{wl}')[f'{n}']
#        x = eval(wl)['Ragg']
        y = eval(f'{wl}').w080new_Rerr
        if wl == 'Blue':

            clr = 'blue'#'#87CEFA'
        elif wl == 'Red':
            clr = 'red'#'#FF6347'
        sn.set_context(font_scale=2)
        sns.jointplot(x, y, kind="hex", color=clr)#"#4CB391")
#
        plt.show()
#        plt.close()
#                   inner="quart")margin_titles=True

#%% KDE BIVARIAT DENSITY
i=0
n=['nr','ni']
for wl in ['Blue', 'Red']:
    i+=1
    try:
        eval(wl).Ragg
    except AttributeError:
        with pd.option_context('mode.chained_assignment', None):
            eval(wl)['Ragg'] = eval(wl)['Rm']*eval(wl)['N']**(1.0/3.)

    vars()[f'fig{i}'] = plt.figure()
    for alt,cmp in [ ['200', f'{wl}s'], ['80new', f'{wl}s_r'] ]:
        sn.set(style="whitegrid")
        sn.set_context('paper',font_scale=2)
        x=eval(wl+alt)[n[0]]
        y=eval(wl+alt)[n[1]]
        vars()[f'ax{i}'] = sns.kdeplot(x, y, cmap=cmp, shade=True, shade_lowest=False)


#%%
#To calculate m0 use one of the following methods
#data['bidtime_hours'] = data.bidtime.map(lambda x: x * 24)
#data.loc[:, 'bidtime_hours'] = data.bidtime.apply(lambda x: x * 24)
#check the link
#https://www.dataquest.io/blog/settingwithcopywarning/
#A_	=	1e-3 * ( -0.323 + 34.89*taus_out + 0.000153*N  + 3.154*nr - 7.979*ni - 56.26*taus_out^2 + 0.00988*taus_out*N)
#I0 = 133
#ENH = A_*TH(0:47) + 1.
#
#P22_ = REPLICATE(P22(I0),181 - I0)
#P22(I0:180) = P22_ * ENH

#%%
os.chdir(dt_directory)
from import_tm import *
from par_import import *

#%% New and old model compare for synthethic corrections
sphere_number = [1024]
#sphere_number = [1024]
size_param = ['06398']
real_ref = ['200']
img_ref = ['00226']
# for 1024 064 2.0 0.0226 A=

#old_run_pm ()

# adding parameters from old runs

#sphere_number = [512]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']
s=0
alpha_value = 1.0
_log = []
th=np.arange(0,181)

ver = 'comp'
tmatrix='on'

for N in sphere_number:


    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)

                try:
                    if tmatrix == 'on':
                        missing = 't-matrix'
                        tm_eff = vars()['tm'+runid+'_eff']
                    missing = ' f-fasm'
                    pm_eff = vars()[f'{ver}{runid}_eff']
                    s+=1

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])
                if tmatrix == 'on':
                    tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                    tm =  vars()['tm'+runid+'_mx']
                    _tm = np.log10(tm.P11*tm.P22)
                    _tms = np.log10((tm.P11*tm.P22)[u:])
                pm = vars()[f'{ver}{runid}_mx']
                old_pm = vars()['param'+runid+'_mx']

                u = 0

                _pm = np.log10(pm.P22)
                _pms = np.log10(pm.P22[u:])
                _oldpm = np.log10(old_pm.P22)
                _oldpms = np.log10(old_pm.P22[u:])


                with plt.style.context(('seaborn-poster')):
                    sn.set_context('paper',font_scale=2)
#                    for _par, par_slice, version in [[_pm, _pms, 'New'],[_oldpm, _oldpms, 'Old']]:
                    fig, axes = plt.subplots(tight_layout=True, figsize=(7.7,6))
                    axes.plot(th, _pm, lw = 2, alpha = 0.8, color = 'blue', label=f'New Param.')
                    axes.plot(th, _oldpm, lw = 2, alpha = 0.8, color = 'black', ls='--', label=f'Old Param.')

                    if tmatrix == 'on':
                        ax2 = fig.add_axes([0.49,0.37,0.45,0.35])
                        axes.plot(th, _tm,lw = 2,marker = 'o', alpha=0.2,markersize = 7,
                                  color = 'red', label = 't - matrix')
                        title = 'Param. vs. T - Matrix'
                        p11err = (10**_tms - 10**_pms)/(10**_tms)
                        oldp11err = (10**_tms - 10**_oldpms)/(10**_tms)
                        ax2.plot(th[u:], oldp11err, lw = 2, alpha = 0.8, color = 'black', ls ='--')
                        ylbl = '      $ ^{\Delta P_{22}}/_{P_{22,t - matrix}}$'
                    else:
                        ax2 = fig.add_axes([0.47,0.4,0.45,0.35])
                        title = 'Old vs. New Param.'
                        p11err = (10**_pms - 10**_oldpms)/(10**_pms)
                        ylbl = '$ ^{\Delta P_{22}}/_{P_{22,new}}$'
                    ax2.set_ylabel(ylbl, fontsize=23)
                    ax2.plot(th[u:], p11err, lw = 2, alpha = 0.8, color = 'blue')
                    axes.set_title(title, fontweight='normal', fontsize=18)



#                    ax2.plot(th[u:], _oldpms, lw = 2, alpha = 0.8, color = 'black', ls='--')
#                    ax2.plot(th[u:], _tms,lw = 2,marker = 'o', alpha=0.2,markersize = 7,
#                              color = 'red', label = 't - matrix')
                    ax2.set_ylim(-0.15,0.45)
                    ax2.grid(linestyle='--')
                    ax2.set_yticks([-0.1,0,0.1,0.4])
#                    ax2.set_title('Relative Difference', fontsize=16)

                    for item in ( ax2.get_xticklabels() + ax2.get_yticklabels()):
                        item.set_fontsize(14)
                    ax2.xaxis.set_major_locator(plt.MaxNLocator(4))

                    axes.set_xlabel('$\Theta$',fontsize=16)
                    axes.set_ylabel('$P_{22}$')
#                    axes.set_ylim(-1.1,2.5)
                    axes.xaxis.set_major_locator(plt.MaxNLocator(5))
                    axes.yaxis.set_major_locator(plt.MaxNLocator(4))
                    axes.legend(fontsize=14)
#                    axes.grid()
#                    ax2.grid()
                    plt.show()
                    plt.close()

#%% New and old model compare Linear Polarization
sphere_number = [3000]
#sphere_number = [1024]
size_param = ['06398']
real_ref = ['171']
img_ref = ['00450']
tmatrix='off'
# for 1024 064 2.0 0.0226 A=

#old_run_pm ()

# adding parameters from old runs

#sphere_number = [512]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']
s=0
alpha_value = 1.0
_log = []
th=np.arange(0,181)

ver = 'comp'


for N in sphere_number:


    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)

                try:
                    missing = 't-matrix'
                    if tmatrix == 'on':
                        tm_eff = vars()['tm'+runid+'_eff']
                    missing = ' f-fasm'
                    pm_eff = vars()[f'{ver}{runid}_eff']
                    s+=1

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])
                if tmatrix == 'on':
                    tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                    tm =  vars()['tm'+runid+'_mx']
                    _tm = (-tm.P12)
                    _tms = ((-tm.P12)[u:])
                    #Setting linewidth. Thinner when t-matrix included
                    _lw = 2
                    #Setting Old param line color
                    _clr = 'black'
                else:
                    _lw = 3
                    _clr = 'maroon'
                pm = vars()[f'{ver}{runid}_mx']
                old_pm = vars()['param'+runid+'_mx']

                u = 70

                _pm = (-pm.P12/pm.P11)
                _pms = ((-pm.P12/pm.P11)[u:])
                _oldpm = (-old_pm.P12/old_pm.P11)
                _oldpms = ((-old_pm.P12/old_pm.P11)[u:])


                with plt.style.context(('seaborn-poster')):
                    sn.set_context('paper',font_scale=2)

                    fig, axes = plt.subplots(tight_layout=True, figsize=(7.7,6))
                    axes.plot(th, _pm, lw = _lw, alpha = 0.8, color = 'blue', label=f'New Param.')
                    axes.plot(th, _oldpm, lw = _lw, alpha = 0.8, color = _clr ,ls='--', label=f'Old Param.')
                    if tmatrix =='on':
                        axes.plot(th, _tm,lw = 2,marker = 'o', alpha=0.25,markersize = 7,
                                  color = 'red', label = 't - matrix')
                        axes.set_title(f'{version} Param. vs. T - Matrix', fontweight='normal', fontsize=18)
                    else:
                        axes.set_title(f'New vs. Old Param.', fontweight='normal', fontsize=18)
                    axes.set_xlabel('$\Theta$',fontsize=16)

                    axes.set_ylabel('$ ^{-P_{12}}/_{P_{11}}$', fontsize=22)
#                        axes.set_ylim(-1.1,2.5)
                    axes.xaxis.set_major_locator(plt.MaxNLocator(5))
                    axes.yaxis.set_major_locator(plt.MaxNLocator(4))
                    axes.legend(loc=1, fontsize=14)
#                    axes.grid()
#                    ax2.grid()
                    plt.show()
                    plt.close()
                    axes.plot()