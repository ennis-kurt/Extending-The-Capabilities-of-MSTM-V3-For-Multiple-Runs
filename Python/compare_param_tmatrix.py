# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:14:20 2019

@author: kurt_
"""

import matplotlib.pyplot as plt
import pandas as pd
from par_import import *
from import_tm import *
import glob
import os
import platform
op_sys = platform.system()
if op_sys == 'Windows':
    dtdir = 'C:\\Users\\kurt_\\Dropbox\\Code\\special\\data\\'
    _sl = '\\'
elif op_sys == 'Linux':
    dtdir = '/home/cihat/Dropbox/Code/special/data/'
os.chdir(dtdir)
#from newpm_import import *
# %config InlineBackend.figure_format = 'svg'

# Re-write the functions.-
#
# add marker border to separate ni

# %%
# FUNCTIONS
# export the errors then using the matlab fit with basic fit tool
# List of all xm values

### NEEDS TO BE UPDATED ########
mon_size_par = ['01680', '02350', '03200', '03360', '04370', '04480',
                '05040', '06398', '08319', '09598']

# Functionst


def mark_size(sphere_num):
    """ This func chooses a markszie based on sphere number """
    if sphere_num >= 1024:
        marker_size = 36
    elif sphere_num == 512:
        marker_size = 24
    elif sphere_num == 256:
        marker_size = 15
    elif sphere_num == 128:
        marker_size = 8
    elif sphere_num <= 64:
        marker_size = 4
    return marker_size


def mark_color(mon_size):
    """ This func chooses a marker color based on Monomer Size parameter """
    # Let's convert the mon_size to float by adding "." after the first "0"


#    # We can choose a color using a color scheme module
#    mon_size = float( ".".join(mon_size[0:2]) + mon_size[2:] )
#    colorselect = plt.cm.gist_ncar #nipy_spectral, Set1,Paired
#    marker_color = colorselect(mon_size)
    # Or we can manually determine the color

#    if mon_size == '01680':
#        marker_color = "C0"
#    elif mon_size == '02350':
#        marker_color = "C1"
#    elif mon_size in [ '03200', '03360' ]:
#        marker_color = "C2"
#    elif mon_size in [ '04370', '04480' ]:
#        marker_color = "C3"
#    elif mon_size == '05040':
#        marker_color = "C4"
#    elif mon_size == '06398':
#        marker_color = "C7"
#    elif mon_size == '08319':
#        marker_color = "C8"
#    elif mon_size == '09598':
#        marker_color = "C9"

    if mon_size in ['01680', '02350', '03200', '03360']:
        marker_color = 'green'
    elif mon_size in ['04370', '04480', '05040']:
        marker_color = "purple"
    elif mon_size == '06398':
        marker_color = "blue"
    elif mon_size == '08319':
        marker_color = "red"
    elif mon_size == '09598':
        marker_color = "yellow"
    else:
        marker_color = "black"

    return marker_color


def mark_style(n_real):
    """ This func chooses a marker style based on Real linearizeactive Index """
    """ Note that nr = 1.66 and 1.68 have the same style."""
    if n_real == "200":
        marker_style = "o"  # Sphere
    elif n_real == "171":
        marker_style = "D"  # Diamond
    elif n_real == "166" or n_real == "168":
        marker_style = "*"  # Star
    elif n_real == "130":
        marker_style = "p"  # Pentagon
    else:
        marker_style = "+"
    return marker_style


def mark_edge_color(n_img):
    """ This func chooses a marker edge color based on Imaginary linearizeactive Index """
    # Let's convert the string type ni to float

    n_img = float(".".join(n_img[0:2]) + n_img[2:])
    if n_img < 0.02:
        m_color2 = 'yellow'
    elif n_img == 0.023:
        m_color2 = 'red'
    elif n_img == 0.045:
        m_color2 = 'pink'
    elif n_img == 0.09:
        m_color2 = 'green'
    else:
        m_color2 = 'black'
    return m_color2


def linearize(data, sec_lin=False):
    # This function linearize the m0. The linerization functions has to be modified each time.
    k1 = 1.20
    l1 = 0.66
    k2 = 4.3
    l2 = 1
    e = 2  # Better M. Regression comparing to e=1
    data['m0'] = np.log((abs(((k1*data.nr + np.log10(k2*data.ni)*1j)
                              ** 2 - 1)/((l1*data.nr + np.log10(l2*data.ni)*1j)**2 + 2)))**e)

    if sec_lin:
        # this needs to be modified. It is the best fit of LPi against m0. fit function obtained from matlab. Needs to be modified for each LPi
        # Incase of LP4 both linear sinisoidal function and 1st degre pol. regression fit well. Thus 2nd linearization may not be necessary
        data.m0 = (-1.605e-09)*(np.sin(data.m0/2 - 0.7*np.pi)) + \
            2.237e-09*((data.m0 + 1))
    return data


def calcm0(nr, ni, sec_lin=False):
    # This function linearize the m0. The linerization functions has to be modified each time.

    k1 = 1.20
    l1 = 0.66
    k2 = 4.3
    l2 = 1
    e = 2
    rf = (abs(((k1*nr + np.log10(k2*ni)*1j)**2 - 1) /
              ((l1*nr + np.log10(l2*ni)*1j)**2 + 2)))**2

    if sec_lin:
        # this needs to be modified. It is the best fit of LPi against m0. fit function obtained from matlab. Needs to be modified for each LPi
        # Incase of LP4 both linear sinisoidal function and 1st degre pol. regression fit well. Thus 2nd linearization may not be necessary
        data.m0 = (-1.605e-09)*(np.sin(data.m0/2 - 0.7*np.pi)) + \
            2.237e-09*((data.m0 + 1))
    return rf


def old_run_pm():
    # adding size parameters
    for item in old_xm:
        if item not in size_param:
            size_param.append(item)
    # adding nr
    for item in old_nr:
        if item not in real_ref:
            real_ref.append(item)
    # adding nr
    for item in old_ni:
        # ni = 0 values neglected, but this should be fixed later.\n Because They aren\'t 0, but a value smaller than 0.0001
        if item not in img_ref and item != '00000':
            img_ref.append(item)


sphere_number = [64, 128, 256, 512, 1024]
size_param = ['01680', '02350', '03200', '03360', '04299', '04370', '04480',
              '04795', '04799', '05040', '05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200', '230']
img_ref = ['00226', '00900', '00450', '00020',
           '00010', '00060', '03000', '00044']

old_run_pm()


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
        vars()[p_next] = ((2*n + 1)*x*vars()[p] - n*vars()[p_prev]) / \
            (n+1)  # Recursion formula to generate L.Ps
        lps.append(vars()[p_next])

    return lps


    # %% COMPARING OLD AND NEW PARAMETERIZATION FROM IDL OUTPUTS
sphere_number = [64, 128, 256, 512, 1024]
size_param = ['01680', '02350', '03200', '03360', '04299', '04370', '04480',
              '04795', '04799', '05040', '05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200', '230']
img_ref = ['00226', '00900', '00450', '00020',
           '00010', '00060', '03000', '00044']
old_run_pm()
#sphere_number = [128]
#size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
#real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
#img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
# adding parameters from old runs

#sphere_number = [256]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']

alpha_value = 1.0
_log = []
theta = np.arange(0, 181)
x = theta[65:]
b1 = 0
b2 = 181
dt = []  # to be used to write Legend. Pol. coefficients data
for N in sphere_number:

    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)

                try:
                    missing = 't-matrix'
                    tm_eff = vars()['tm'+runid+'_eff']
                    missing = ' f-fasm'
                    pm_eff = vars()['newpm'+runid+'_eff']

                    #print('There are at least one data to compare')

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(
                        missing, N, xm, nr, ni))
                    continue

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])

                tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                tm = vars()['tm'+runid+'_mx']
                pm = vars()['newpm'+runid+'_mx']
                old_pm = vars()['param'+runid+'_mx']

                new_p22_err = (tm.P22*tm.P11 - pm.P22)[b1:b2]
                old_p22_err = (tm.P22*tm.P11 - old_pm.P22)[b1:b2]

                plotting = True
                if plotting:
                    # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
                    #                    p22_corr = pd.Series(np.polynomial.legendre.legval(x, coeffs), index=x)
                    #                    new_pm = pm.copy()
                    #                    new_pm.P22 = pm.P22.add(p22_corr, fill_value=0)
                    fig, ax = plt.subplots(ncols=3, figsize=(22, 6))

                    ax[0].plot(np.log10(old_pm.P22)[
                               b1:b2], '.', label='old_pm')
                    ax[0].plot(np.log10(tm.P22*tm.P11)[b1:b2], '.', label='tm')
                    ax[0].set_title('Old P22'+runid)
                    ax[0].legend()

                    # new fit
                    ax[1].plot(np.log10(pm.P22)[b1:b2], '.', label='new_pm')
                    ax[1].plot(np.log10(tm.P22*tm.P11)[b1:b2], '.', label='tm')
                    ax[1].legend()
                    ax[1].set_title('New P22'+runid)

                    # Error Function and the Fit
#                    ax[2].plot(x, new_p22_err, '.', label = 'new_p22_err')
#                    ax[2].plot(x, old_p22_err,'.', label = 'old_p22_err' )
#                    ax[2].legend()
#                    ax[2].set_title('p22 error & the fit')

                    # old and new p22
                    ax[2].plot((new_p22_err)[b1:b2], '.', label='new_pm')
                    ax[2].plot((old_p22_err)[b1:b2], '.', label='old_pm')
                    ax[2].set_title('Old & New P22 Python'+runid)
                    ax[2].legend()
                    plt.tight_layout()
                    plt.show()
                    plt.close()

         # %% P11
sphere_number = [128, 256, 512, 1024]
size_param = ['01680', '02350', '03200', '03360', '04299', '04370', '04480',
              '04795', '04799', '05040', '05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200', '230']
img_ref = ['00226', '00900', '00450', '00020',
           '00010', '00060', '03000', '00044']
old_run_pm()
#sphere_number = [256, 512, 1024]
#size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
#real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
#img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
# adding parameters from old runs

#sphere_number = [256]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']

alpha_value = 1.0
_log = []
theta = np.arange(0, 181)
x = theta[65:]
b1 = 0
b2 = 181
dt = []  # to be used to write Legend. Pol. coefficients data
for N in sphere_number:

    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)

                try:
                    missing = 't-matrix'
                    tm_eff = vars()['tm'+runid+'_eff']
                    missing = ' f-fasm'
                    pm_eff = vars()['newpm'+runid+'_eff']

                    #print('There are at least one data to compare')

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(
                        missing, N, xm, nr, ni))
                    continue

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])

                tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                tm = vars()['tm'+runid+'_mx']
                pm = vars()['newpm'+runid+'_mx']
                old_pm = vars()['param'+runid+'_mx']

                new_p22_err = (tm.P22*tm.P11 - pm.P22)[65:]
                old_p22_err = (tm.P22*tm.P11 - old_pm.P22)[65:]

                plotting = True
                if plotting:
                    # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
                    #                    p22_corr = pd.Series(np.polynomial.legendre.legval(x, coeffs), index=x)
                    #                    new_pm = pm.copy()
                    #                    new_pm.P22 = pm.P22.add(p22_corr, fill_value=0)
                    fig, ax = plt.subplots(ncols=2, figsize=(22, 6))

                    ax[0].plot(np.log10(old_pm.P11)[
                               b1:b2], '.', label='old_pm')
                    ax[0].plot(np.log10(tm.P11)[b1:b2], '.', label='tm')
                    ax[0].set_title('Old P11'+runid)
                    ax[0].legend()

                    # new fit
                    ax[1].plot(np.log10(pm.P11)[b1:b2], '.', label='new_pm')
                    ax[1].plot(np.log10(tm.P11)[b1:b2], '.', label='tm')
                    ax[1].legend()
                    ax[1].set_title('New P11'+runid)
                    plt.show()
                    plt.close()


#                    # Error Function and the Fit
#                    ax[2].plot(x, new_p22_err, '.', label = 'new_p22_err')
#                    ax[2].plot(x, old_p22_err,'.', label = 'old_p22_err' )
#                    ax[2].legend()
#                    ax[2].set_title('p22 error & the fit')

                    # old and new p22
#                    ax[2].plot(np.log10(old_pm.P11), '.', label = 'old_pm')
#                    ax[2].plot(np.log10(pm.P11), '.', label = 'new_pm')
#                    ax[2].set_title('Old & New P11 Python'+runid)
#                    ax[2].legend()
#                    plt.tight_layout()
#                    plt.show()

                    # %% LINEAR POLARIZATION


sphere_number = [64, 128, 256, 512, 1024]
size_param = ['01680', '02350', '03200', '03360', '04299', '04370', '04480',
              '04795', '04799', '05040', '05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200', '230']
img_ref = ['00226', '00900', '00450', '00020',
           '00010', '00060', '03000', '00044']
old_run_pm()
sphere_number = [128, 256, 512, 1024]
size_param = ['06398', '07300', '08319', '09598']
real_ref = ['145', '166', '168', '171', '180', '200', '230']
img_ref = ['00226', '00900', '00450', '00020',
           '00010', '00060', '03000', '00044']
# adding parameters from old runs

#sphere_number = [256]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']

alpha_value = 1.0
_log = []
theta = np.arange(0, 181)
x = theta[65:]
ref = pd.Series(np.zeros((181,)))
bsth = 0  # Backscattering Theta starting angle
dt = []  # to be used to write Legend. Pol. coefficients data
for N in sphere_number:

    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)

                try:
                    missing = 't-matrix'
                    tm_eff = vars()['tm'+runid+'_eff']
                    missing = ' f-fasm'
                    pm_eff = vars()['newpm'+runid+'_eff']

                    #print('There are at least one data to compare')

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(
                        missing, N, xm, nr, ni))
                    continue

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])

                tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                tm = vars()['tm'+runid+'_mx']
                pm = vars()['newpm'+runid+'_mx']
                old_pm = vars()['param'+runid+'_mx']

                new_p22_err = (tm.P22*tm.P11 - pm.P22)[65:]
                old_p22_err = (tm.P22*tm.P11 - old_pm.P22)[65:]

                plotting = False
                if plotting:
                    # if sp >= 0.63:
                    # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
                    #                    p22_corr = pd.Series(np.polynomial.legendre.legval(x, coeffs), index=x)
                    #                    new_pm = pm.copy()
                    #                    new_pm.P22 = pm.P22.add(p22_corr, fill_value=0)
                    fig, ax = plt.subplots(ncols=3, figsize=(22, 6))

                    ax[0].plot((-old_pm.P12/old_pm.P11), '.', label='old_pm')
                    ax[0].plot((-tm.P12), '.', label='tm')
                    ax[0].set_title('Old Lin Polar'+runid)
                    ax[0].legend()

                    # new fit
                    ax[1].plot((-pm.P12/pm.P11), '.', label='new_pm')
                    ax[1].plot((-tm.P12), '.', label='tm')
                    ax[1].legend()
                    ax[1].set_title('New Lin. Polar'+runid)


#                    # Error Function and the Fit
#                    ax[2].plot(x, new_p22_err, '.', label = 'new_p22_err')
#                    ax[2].plot(x, old_p22_err,'.', label = 'old_p22_err' )
#                    ax[2].legend()
#                    ax[2].set_title('p22 error & the fit')

                    # old and new p22
                    ax[2].plot(old_pm.P12/old_pm.P11 -
                               tm.P12, '-', label='old_pm')
                    ax[2].plot(pm.P12/pm.P11 - tm.P12, '.', label='new_pm')
                    ax[2].set_title('Old & New Lin. Pol Error'+runid)
                    ax[2].legend()
                    plt.tight_layout()
                    plt.show()
                    plt.close()

                plotting = True

                if plotting:
                    #                if min(-tm.P12) < 0:
                    fig, ax = plt.subplots(ncols=3, figsize=(22, 6))

                    ax[0].plot((-old_pm.P12/old_pm.P11)
                               [bsth:], '.', label='old_pm')
                    ax[0].plot((-tm.P12)[bsth:], '.', label='tm')
                    ax[0].plot(ref[bsth:], '-.')
                    ax[0].set_title('Old Lin Polar'+runid)
                    ax[0].legend()

                    # new fit
                    ax[1].plot((-pm.P12/pm.P11)[bsth:], '.', label='new_pm')
                    ax[1].plot((-tm.P12)[bsth:], '.', label='tm')
                    ax[1].plot(ref[bsth:], '-.')
                    ax[1].legend()
                    ax[1].set_title('New Lin. Polar'+runid)


#                    # Error Function and the Fit
#                    ax[2].plot(x, new_p22_err, '.', label = 'new_p22_err')
#                    ax[2].plot(x, old_p22_err,'.', label = 'old_p22_err' )
#                    ax[2].legend()
#                    ax[2].set_title('p22 error & the fit')

                    # old and new p22
                    ax[2].plot((old_pm.P12/old_pm.P11 - tm.P12)
                               [bsth:], '-', label='old_pm')
                    ax[2].plot((pm.P12/pm.P11 - tm.P12)
                               [bsth:], '.', label='new_pm')
                    ax[2].plot(ref[bsth:], '-.')
                    ax[2].set_title('Old & New Lin. Pol Error'+runid)
                    ax[2].legend()
                    plt.tight_layout()
                    plt.show()
                    plt.close()
