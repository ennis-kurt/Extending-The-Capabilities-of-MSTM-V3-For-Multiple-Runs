# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:12:47 2020

@author: kurt_
"""

# %%
from import_tm import *
from par_import import *
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym
from scipy.stats import linregress as linreg
from astropy import units as U, constants as C
import linecache as gl
import pandas as pd
import glob
import os
import platform
op_sys = platform.system()
if op_sys == 'Windows':
    dtdir = 'C:\\Users\\kurt_\\PARAM DATA\\'
    disr_dt = 'C:\\Users\\kurt_\\Google Drive\\dell_github\\T-Matrix-Titan'
    # 'C:\\Users\\kurt_\\Dropbox\\Code\\'
    dt_directory = 'C:\\Users\\kurt_\\Google Drive\\dell_github\\T-Matrix-Titan\\special\\data'
    _sl = '\\'
elif op_sys == 'Linux':
    dtdir = '/home/cihat/programs/gdl/'
    disr_dt = '/home/cihat/Dropbox/code/'
    dt_directory = '/home/cihat/Dropbox/code/special/data/'
    _sl = '/'
os.chdir(f'{disr_dt}{_sl}special{_sl}data{_sl}')
pi = np.pi
lg = np.log10
# %%
# %% Plotting Fc for different multiple N values
#lstyle = ['--', '-.','-']
#Ns = [128, 1024,  4096]
# Select x axis data. Theta ot q
lmd = 0.4908
rm = 0.05
xm = 2*np.pi*rm/lmd
Ns = [512, 2048, 6000, 8000]
x_data = 'th'  # 'th'
xscl = 'log'  # 'linear'
if x_data == 'q':
    dct = {'a': [320, 580, 1400], 'Ns': Ns, 'lstyle': [':', '--', '-.', '-']}
    if xscl == 'log':
        dct['x'] = [[1.5, 12], [2, 26.5], [0.5, 7]]
    if xscl == 'linear':
        dct['x'] = [[0.25, 2.2], [3.5, 16.5], [11, 18.5]]
elif x_data == 'th':
    dct = {'x': [[10, 55], [7, 55], [7, 55]], 'a': [
        1030, 2500, 6080], 'Ns': Ns, 'lstyle': [':', '--', '-.', '-']}


fig, ax = plt.subplots()  # figsize=(8,6)
ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
ax.set_yscale('log')
ax.set_xscale(xscl)
ax.set_xlabel('q', fontsize=19)
ax.set_ylabel('$F_c$', fontsize=19)

# Remove the tick marks; they are unnecessary with the tick lines we just
# plotted. Make sure your axis ticks are large enough to be easily read.
# You don't want your viewers squinting to read your plot.
ax.set_ylim(20, dct['Ns'][-1]**2.2)
ax2 = ax.twinx()
ax2.set_ylim(20, dct['Ns'][-1]**2.2)
ax2.set_yscale('log')
ax2.yaxis.set_major_locator(plt.MaxNLocator(4))
ax2.set_yticks([10**2, 10**4, 10**6, 10**7])

# this set works for Df = 2.0 only. I believe dcut should be changed too
# dcut = 3.194
#    R2 = 4.7 # original 3.478
#    R1 = 1.598
yticks = []
yticklabel = []
for i, N in enumerate(dct['Ns']):
    if i < len(dct['Ns']) - 1:
        yticks.append(dct['Ns'][i]**2)
    elif i == len(dct['Ns']) - 1:
        yticks.append(dct['Ns'][i]**2.12)

    yticklabel.append('$N_{}^2$'.format({N}))
    lst = dct['lstyle'][i]
    dcut = 3.194
    R2 = 3.478
    R1 = 1.598  # 1.1201 make k0=1 and Sq vs. q or Fc vs. q log-log plot an
    # excellent match to other studies like Sorensen 2001. However, Phase functions
    # obtained by r1 = 1.1201 does not make sense. Somewhat weak forward peak
    # and too weak backward intesnities when theta > 90. So Back to normal k0
    Rcut = 1. / 0.0001
    Df = 2.0
    Rmin = 2.0
    theta = np.arange(181)
    rtheta = np.deg2rad(theta)

    q0 = 4*pi*np.sin(rtheta/2.)/lmd
    q = np.sin(rtheta/2.)
    #dstep = 1/(8*xm)
    ds = 1/(8*xm)
    Rmax = R1*(N*np.log(Rcut))**(1.0/Df)
    nstep = int((Rmax - Rmin) / ds)
    nstep = np.where(nstep < 100, 100, nstep)
    dstep = (Rmax - Rmin)/(nstep-1)

    R0 = np.arange(nstep)*dstep + Rmin

    dist = R0 * xm
    nc = ((1.0 - np.exp(-(R0/R1)**(Df) / N)) *
          (1.0 - np.exp(-(R0/R2)**dcut)) + (2.0/N))/(1 + (2.0/N))
    #nc=1.0 - np.exp(-(R0/R1)**(Df) /N)
    f0 = np.zeros(nstep)
    # this seems to include nc[0] erronously
    f0[0] = 0.5 * (nc[1]-nc[0]) + nc[0]
    #f0[0] = 0.5 * (nc[1]-nc[0])
    f0[nstep-1] = 1. - nc[nstep-1] + 0.5 * (nc[nstep-1]-nc[nstep-2])
    #f0[nstep-1] = 0.5 * (nc[nstep-1]-nc[nstep-2]) #
    f0[1:(nstep-1)] = (nc[2:(nstep)] - nc[0:(nstep-2)])/(2)

    r0 = Rmax
    Sq = []
    # with plt.style.context(('seaborn-paper')):
    for th, rth in enumerate(rtheta):
        if rth == 0.:
            Fi = 1.
        elif rth > 0:
            #Fi in q-space
            Fi = np.sin(q0[th]*R0*rm)/(q0[th]*R0*rm)
            # Fi in theta space
#            Fi = np.sin(2*q[th]*R0*xm)/(2*q[th]*R0*xm)
        Fc = N + N*(N-1)*np.sum(f0*Fi)
        Sq.append(Fc)
    print(f'Sq[0] = {Sq[0]/N**2}')
    print(f'Fc[-1]/N = {Sq[-1]/N}')
    print(f'Fc(min)/N = {np.min(Sq)/N}')
    #ax.plot(q[th], np.sum(Fi)/N**2,marker='+')
    if x_data == 'q':
        x = q0
    elif x_data == 'th':
        x = theta

    ax.plot(x, Sq, linestyle=lst, label=str(N))  # q*R0[:181]

#    x_lim = dct['x'][i]
#    a = dct['a'][i]
#    x=np.linspace(x_lim[0],x_lim[1],100)
# y=a**1.88*x**-1.72
#    y=a**2*x**-Df
#
#    # Add label to power law line only once at the final step
#    if i < np.size(dct['Ns'])-1:
#        ax.plot(x, y, linestyle='-',color='black', linewidth=1, alpha=0.8)
#    elif i == np.size(dct['Ns'])-1:
#        if x_data =='q':
#            xlbl = '$q^{-D_f}$'
#        elif x_data == 'th':
#            xlbl = '$ \Theta ^{-D_f}$'
#        ax.plot(x, y, linestyle='-',color='black', label=xlbl, linewidth=1, alpha=0.6)

    ax.legend()
    for item in (ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(14)

    slope_q = linreg(lg(q[10:40]), lg(Sq[10:40])).slope
    slope_th = linreg(lg(theta[10:40]), lg(Sq[10:40])).slope
    print('-------------------')
    print(f'     N     |  {N}  |')
    print('-------------------')
    print(f'slope_theta| {slope_th:.3}  |')
    print('-------------------')
    print(f'slope_q    | {slope_q:.3}  |')

ax.set_yticks(yticks)
ax.set_yticklabels(yticklabel)
ax.grid(True)
ax.tick_params(axis='both', which='both', labelsize=14,
               bottom=True, top=True, labelbottom=True,
               left=True, right=False, labelleft=True, labelright=False)
# ax2.tick_params(axis='both', which='both', labelsize=14,
#               bottom=False, top=False, labelbottom=False,
#               left=True, right=True, labelleft=False, labelright=True)


# ax.legend()
plt.tight_layout()
plt.show()
plt.close()

# %% Compare T-MAtrix vs. Param for P11

_pm = ['2575_03277_158_00040', '2950_05120_200_00660']
_chn = 'Blue'
for pm_id in _pm:
    file = glob.glob(dtdir+'final{}newpm{}.dat'.format(_sl, pm_id))
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
            print('csca value error', param_run)
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
# %%
os.chdir(f'{disr_dt}{_sl}special{_sl}data{_sl}')
# %%
xscl = 'linear'
phase = 'P22'  # 'P22' or 'P11'
x_data = 'th'  # 'q' or 'th'
run = '512_05600_190_00620_mx'
tm = vars()[f'tm{run}']
pm = vars()[f'newpm{run}']
xm = 0.64
rm = 0.05
lmd = 2*pi*rm/xm
theta = np.arange(181)
rtheta = np.deg2rad(theta)
q = 4*pi*np.sin(rtheta/2.)/lmd
fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xscale(xscl)
ax.set_xlabel('q', fontsize=19)
ax.set_ylabel('$P_{11}$', fontsize=19)
if x_data == 'q':
    x = q
elif x_data == 'th':
    x = theta
for dt, lbl, lns, alp, clr in [[tm, 'T-Matrix', '-', 0.6, 'red'], [pm, 'Model', ':', 1, 'black']]:
    if phase == 'P22':
        if lbl == 'Model':
            ds = dt.P22/dt.P11
        elif lbl == 'T-Matrix':
            ds = dt.P22
    elif phase == 'P11':
        ds = dt.P11
    ax.plot(x, ds, label=lbl, linestyle=lns, alpha=alp, color=clr)
    ax.tick_params(axis='both', which='both', labelsize=14,
                   bottom=True, top=True, labelbottom=True,
                   left=True, right=False, labelleft=True, labelright=False)

    slope_q = linreg(lg(q[4:40]), lg(ds[4:40])).slope
    slope_th = linreg(lg(theta[4:40]), lg(ds[4:40])).slope
    print('-------------------')
    print(f'     data     |  {lbl}  |')
    print('-------------------')
    print(f'slope_theta| {slope_th:.3}  |')
    print('-------------------')
    print(f'slope_q    | {slope_q:.3}  |')
ax.legend()
# %%
xscl = 'linear'
phase = 'P22'  # 'P22' or 'P11'
x_data = 'th'  # 'q' or 'th'
run = '512_08300_190_00800_mx'
tm = vars()[f'tm{run}']
pm = vars()[f'newpm{run}']
xm = 0.64
rm = 0.05
lmd = 2*pi*rm/xm
theta = np.arange(181)
rtheta = np.deg2rad(theta)
q = 4*pi*np.sin(rtheta/2.)/lmd
fig, axs = plt.subplots(2, 1, constrained_layout=True, figsize=(6, 6))
axs[1].set_yscale('log')
for ax in axs:
    ax.set_xscale(xscl)
    ax.set_xlabel('q', fontsize=19)
    ax.set_ylabel('$P_{11}$', fontsize=19)
if x_data == 'q':
    x = q
elif x_data == 'th':
    x = theta
for dt, lbl, lns, alp, clr in [[tm, 'T-Matrix', '-', 0.6, 'red'], [pm, 'Model', ':', 1, 'black']]:
    if phase == 'P22':
        if lbl == 'Model':
            ds = -dt.P22 + dt.P11  # dt.P22/dt.P11
            lpr = dt.P22/dt.P11
        elif lbl == 'T-Matrix':
            ds = -dt.P22*dt.P11 + dt.P11  # dt.P22
            lpr = dt.P22
    elif phase == 'P11':
        ds = dt.P11
    print(f'{lbl} {lpr[0]}')
    axs[0].plot(x, ds, label=lbl, linestyle=lns, alpha=alp, color=clr)
    axs[0].tick_params(axis='both', which='both', labelsize=14,
                       bottom=True, top=True, labelbottom=True,
                       left=True, right=False, labelleft=True, labelright=False)

    axs[1].plot(x, dt.P11, label=lbl, linestyle=lns, alpha=alp, color=clr)
    slope_q = linreg(lg(q[4:40]), lg(ds[4:40])).slope
    slope_th = linreg(lg(theta[4:40]), lg(ds[4:40])).slope
    print('-------------------')
    print(f'     data     |  {lbl}  |')
    print('-------------------')
    print(f'slope_theta| {slope_th:.3}  |')
    print('-------------------')
    print(f'slope_q    | {slope_q:.3}  |')
for ax in axs:
    ax.legend()
plt.show()
plt.close()
depol = (1 - np.cos(rtheta)**2)/(5+np.cos(rtheta)**2)
plt.plot(theta, depol)
plt.show()
plt.close()
