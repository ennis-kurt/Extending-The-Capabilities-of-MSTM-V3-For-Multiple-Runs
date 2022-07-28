# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:43:19 2022

@author: kurt_

This is the final version of coefficient calculations. 
It is under development as of now. 
"""

from numpy.polynomial import Legendre as L
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from par_import import *
from import_tm import *
import glob
import os
import platform
op_sys = platform.system()
if op_sys == 'Windows':
    path = 'C:\\Users\\kurt_\\Google Drive\\dell_github\\T-Matrix-Titan\\special\\data\\'

elif op_sys == 'Linux':
    path = '/home/cihat/Dropbox/code/special/data/'
os.chdir(path)
# from newpm_import import *
# %config InlineBackend.figure_format = 'svg'
dtdir = 'C:\\Users\\kurt_\\Google Drive\\dell_github\\T-Matrix-Titan\\special\\data\\output\\'
os.chdir(dtdir)
# %%
# Functions


def linearize(data, sec_lin=False):
    # This function linearize the m0. The linerization functions has to be modified each time.
    # For Forward Scattering Excluding GE256GE063 which uses defaults
    k1 = 1
    l1 = 0.6
    k2 = 3.4
    l2 = 1.78
    e = 1
    data['Rf'] = np.log((abs(((k1*data.nr + np.log(k2*data.ni)*1j)
                              ** 2 - 1)/((l1*data.nr + np.log10(l2*data.ni)*1j)**2 + 2)))**e)
    # Defaults
#    k1 = 1.20; l1 = 0.66; k2 = 4.3; l2 = 1
#    e = 2 # Better Multiple Regression comparing to e = 1
#    data['Rf'] = np.log((abs(((k1*data.nr + np.log10(k2*data.ni)*1j )**2 -1)/((l1*data.nr + np.log10(l2*data.ni)*1j)**2 + 2)))**e)

    if sec_lin:
        # this needs to be modified. It is the best fit of LPi against m0. fit function obtained from matlab. Needs to be modified for each LPi
        # Incase of LP4 both linear sinisoidal function and 1st degre pol. regression fit well. Thus 2nd linearization may not be necessary
        data[m] = (-1.605e-09)*(np.sin(data.m0/2 - 0.7*np.pi)) + \
            2.237e-09*((data.m0 + 1))
    return data


def Leg_Pol(x, deg):
    """
    deg is the degree of legendre pol. 3 means Legendre polynomials include
    Po + P1 + P2 + P3

    x is the independent variable in the Leg. Pol
    """

    P0 = 1
    P1 = x
    lps = [P0, P1]

    for n in range(1, deg):
        p = 'P{}'.format(n)
        p_next = 'P{}'.format(n+1)
        p_prev = 'P{}'.format(n-1)
        vars()[p_next] = ((2*n + 1)*x*vars()[p] - n*vars()[p_prev])/(n+1)
        lps.append(vars()[p_next])

        return lps


# %%
# Reading the output_list file wich contains the available T-Matrix outputs
# Note that it contains the incomplete runs too.
variables = pd.read_csv(dtdir+'output_list.csv',
                        dtype={'N': int, 'xm': str, 'nr': str, 'ni': str})
variables.info()
# %%
# Converting variables to float and str format. Strings will be used for mathcing file names
variables['x_m'] = variables['xm'].str.replace('.', '', regex=False)
variables.loc[:, 'xm'] = variables['xm'].apply(float)
variables['n_r'] = variables['nr'].str.replace('.', '', regex=False)
variables.loc[:, 'nr'] = variables['nr'].apply(float)
variables['n_i'] = variables['ni'].str.replace('.', '', regex=False)
variables.loc[:, 'ni'] = variables['ni'].apply(float)
# %%
# Fitting Coefficients

s = 0
alpha_value = 1.0
_log = []
theta = np.arange(0, 181)

# Setting boundaries for angular fit
b1 = 0
b2 = 4
b_end = 181

# Setting the b2 to fit forward scattering (where b1=0)
# if b1 == 0:
#    if N <= 256:
#        b2 = 20
#    elif N == 512:
#        b2 = 13
#    elif N == 1024:
#        b2 = 6
# else:
#    b2 = b2
#b2 = 7

# Set te degree of Legendre Polynomials
dg = 2

# Setting angular boundaries for the plots
theta = np.arange(0, 181)
a1 = b1
a2 = b2+7
x1 = theta[a1:a2]

dt = []  # to be used to write Legend. Pol. coefficients data


for i in variables.index:
    N = variables.loc[i, 'N']
    xm = variables.loc[i, 'xm']
    nr = variables.loc[i, 'nr']
    ni = variables.loc[i, 'ni']
    x_m = variables.loc[i, 'x_m']
    n_r = variables.loc[i, 'n_r']
    n_i = variables.loc[i, 'n_i']
    runid = '{}_{}_{}_{}'.format(N, x_m, n_r, n_i)
    try:
        missing = 't-matrix'
        tm_eff = vars()['tm'+runid+'_eff']
        missing = ' f-fasm'
        pm_eff = vars()['newpm'+runid+'_eff']
        s += 1

    except KeyError:
        #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
        _log.append('missing run {} {}_{}_{}_{}_eff'.format(
            missing, N, xm, nr, ni))
        continue

    tm_eff['cs'] = tm_eff.qs[0]*np.pi*(xm*N**(1/3))**2
    tm = vars()['tm'+runid+'_mx']
    pm = vars()['newpm'+runid+'_mx']
    old_pm = vars()['param'+runid+'_mx']

    # Some parameters to use later
    alpha_value = 1.0
    _log = []
    theta = np.arange(0, 181)
    # Setting b2 manually
    # b2=13

    x = theta[b1:b2]

    new_p22_err = (tm.P22*tm.P11 - pm.P22)[b1:b2]
    old_p22_err = (tm.P22*tm.P11 - old_pm.P22)[b1:b2]
    maxpol_tm = tm.theta[-tm.P12 == max(-tm.P12)].values[0]
    maxpol_pm = pm.theta[-pm.P12/pm.P11 == max(-pm.P12/pm.P11)].values[0]

    # Now the correction
    # First fit the error function with a 3rd Degree Legendre Polynomial
    xw = 2*(x-x[0])/(x[-1]-x[0]) - 1

    # coeffs are mapped to [-1,1] window since L.P. are orthogonal in this domain
    coeffs = L.fit(x, old_p22_err, deg=dg)
    coeff = coeffs.convert()  # this converts the coeffs in to the original domain. These are the coeffs that will be analyzed statistically and passed to New Parameterization model
    plotting = False
    if plotting:
        if np.mod(s, 7) == 0:
            # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
            #                    p22_corr = pd.Series(np.polynomial.legendre.legval(x, coeffs), index=x)
            #                    new_pm = pm.copy()
            #                    new_pm.P22 = pm.P22.add(p22_corr, fill_value=0)
            fig, ax = plt.subplots(ncols=2, figsize=(12, 6))
            p22_err = (tm.P11 - old_pm.P11)[a1:a2]
            ax[0].plot(((-old_pm.P12/old_pm.P11)), '.', label='Old pm')
            ax[0].plot((-tm.P12)[a1:a2], '.', label='tm')
            ax[0].set_title('Old P22'+runid)
    #                    ax[0].set_yscale('log')
            ax[0].legend()

            # new fit
            ax[1].plot((-pm.P12/pm.P11), '.', label='new_pm')
            ax[1].plot((-tm.P12), '.', label='tm')
            ax[1].legend()
            ax[1].set_title('New P22'+runid)

            # Error Function and the Fit
    #                    ax[2].plot(x, new_p22_err, '.', label = 'new_p22_err')
            #ax[2].plot(x, old_p22_err,'.', label = 'old_p22_err' )
            # ax[2].legend()
    #                    ax[2].set_title('p22 error & the fit')

            # old and new p22
    #                    ax[3].plot((old_pm.P22), '.', label = 'old_pm')
    #                    ax[3].plot((pm.P22), '.', label = 'new_pm')
    #                    ax[3].set_title('Old & New P22'+runid)
    #                    ax[3].legend()

            plt.tight_layout()
            plt.show()
            plt.close()

        # Calculating Param Csca from Qs
    aprj = ((np.pi * xm**2) * (N**(2/3)))
    c_sca_m_1 = 0.200
    c_sca_m_2 = 0.164
    c_sca_m_3 = 1.047
    c_sca_m_4 = 0.127
    c_sca_x_1 = 3.082
    c_sca_x_2 = 0.757
    m = complex(nr, ni)
    m0 = abs((m**2-1)/(m**2+2))
    corr_sca = 1. + c_sca_m_3 * (m0-c_sca_m_4) * \
        np.sin(c_sca_x_1 * xm) * np.exp(-xm * c_sca_x_2)
    sw = {}

    sw['N'] = N
    sw['xm'] = xm
    sw['nr'] = nr
    sw['ni'] = ni
    sw['taus_out'] = pm_eff.taus[0]
    sw['taua_out'] = pm_eff.taua[0]
#                sw['qa_tm'] = tm_eff.qa[0]
    sw['qs_tm'] = tm_eff.qs[0]
#                sw['qa_pm'] = pm_eff.qa[0]
    sw['qs_pm'] = pm_eff.qs[0]
#                sw['cs_pm'] = pm_eff.cs[0]
#                sw['cs_tm'] = tm_eff.cs[0]
#                sw['Aproj'] = aprj
#                sw['corr_sca'] = corr_sca
    sw['m0'] = m0
#                sw['maxpol_tm'] = maxpol_tm
#                sw['maxpol_pm'] = maxpol_pm
    sw['p1'] = coeff.coef[0]
    sw['p2'] = coeff.coef[1]
    sw['p3'] = coeff.coef[2]
    if dg == 3:
        sw['p4'] = coeff.coef[3]
    dt.append(sw)

# Should you need the plots, edit the "if" below

    plotting = False

    if plotting:
        if np.mod(s, 13) == 0:
            # if np.mod(s,7) == 0:
            # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
            p22_corr = pd.Series(coeffs(x), index=x)

            new_pm = old_pm.copy()
            # P22_corr does not cover the whole domain, so fill_value is necessary
            new_pm.P22 = (old_pm.P22).add(p22_corr, fill_value=0)
            fig, ax = plt.subplots(ncols=3, figsize=(12, 6))

            ax[0].plot(np.log10((new_pm.P22))[a1:a2], label='new_pm python')
            ax[0].plot((np.log10(tm.P22*tm.P11))[a1:a2], '.', label='tm')
            ax[0].set_title('New P22 Python Correction'+runid)
            ax[0].legend()
            plt.grid()

            # Old fit
            ax[1].plot((np.log10(old_pm.P22))[a1:a2], label='old_pm')
            ax[1].plot((np.log10(tm.P22*tm.P11))[a1:a2], '.', label='tm')
            ax[1].legend()
            ax[1].set_title('Old P22'+runid)

            # Error Function and the Fit
    #                    ax[2].plot(x, old_p22_err , '.', label = 'p22_err')
    #                    ax[2].plot(x, p22_corr,'.', label = 'p22_corr' )
    #                    ax[2].legend()
    #                    ax[2].set_title('p22 error & the fit')
    #                    plt.grid()
    #                    plt.tight_layout()
    #                    plt.show()
            ax[2].plot(x, old_p22_err, '.', label='p22_err')
            ax[2].plot(x, p22_corr, '.', label='p22_corr')
            ax[2].legend()
            ax[2].set_title('P22 error & the fit')
            plt.grid()
            plt.tight_layout()
            plt.show()

lp = 1
if lp == 1:
    p = "p1"
elif lp == 2:
    p = 'p2'
elif lp == 3:
    p = 'p3'
elif lp == 4:
    p = 'p4'
else:
    print('wrong p values')


LP_Coeff = pd.DataFrame(dt)
linearize(LP_Coeff)
# optional parameters which makes filtering easier visually.
LP_Coeff['xm_m0'] = LP_Coeff['xm']*LP_Coeff['m0']
LP_Coeff['N_m0'] = LP_Coeff['N']*LP_Coeff['m0']*0.05
LP_Coeff['N_xm'] = LP_Coeff['N']*LP_Coeff['xm']

# Breaking in to 4 regimes
LP512_lt063 = LP_Coeff[(LP_Coeff.N <= 512) & (LP_Coeff.xm < 0.63)]
LP512_gt063 = LP_Coeff[(LP_Coeff.N <= 512) & (LP_Coeff.xm >= 0.63)]
LP1024_lt063 = LP_Coeff[(LP_Coeff.N >= 512) & (LP_Coeff.xm < 0.63)]
LP1024_gt063 = LP_Coeff[(LP_Coeff.N >= 512) & (LP_Coeff.xm >= 0.63)]
LP1024 = LP_Coeff[LP_Coeff.N >= 512]
LP_lt063 = LP_Coeff[LP_Coeff.xm < 0.63]
LP_gt063 = LP_Coeff[LP_Coeff.xm >= 0.63]
