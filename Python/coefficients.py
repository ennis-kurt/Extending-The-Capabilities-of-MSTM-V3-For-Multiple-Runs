# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 14:08:28 2019

@author: kurt_
"""

from numpy.polynomial import Legendre as L
import matplotlib.pyplot as plt
import pandas as pd
from par_import import *
from import_tm import *
import glob
import os
import platform
op_sys = platform.system()
if op_sys == 'Windows':
    dtdir = 'C:\\Users\\kurt_\\Google Drive\\dell_github\\T-Matrix-Titan\\special\\data\\'

elif op_sys == 'Linux':
    dtdir = '/home/cihat/Dropbox/code/special/data/'
os.chdir(dtdir)
# from newpm_import import *
# %config InlineBackend.figure_format = 'svg'

# go to output dir
os.chdir(dtdir+"output\\")

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


# def linearize(data, sec_lin = False):
#    # This function linearize the m0. The linerization functions has to be modified each time.
#
#    for lp in [1, 2]:
#
#
#        if lp == 1:
#            k1=1; l1=0.73; k2=0.85; l2 = 18
#            k1 = 1.35; l1 = 0.60; k2 = 100; l2 = 100
#            e = -1.7218
#            e=2
#            data['m0_p1'] = (abs(((k1*data.nr + np.log10(k2*data.ni)*1j)**2 -1)/((l1*data.nr + np.log10(l2*data.ni)*1j)**2 + 2)))**e
#
#        else:
#            k1 = 1.35; l1 = 0.60; k2 = 100; l2 = 100
#            e = 2
#            data['m0'] = (abs(((k1*data.nr + np.log10(k2*data.ni)*1j)**2 -1)/((l1*data.nr + np.log10(l2*data.ni)*1j)**2 + 2)))**e

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
        vars()[p_next] = ((2*n + 1)*x*vars()[p] - n*vars()[p_prev])/(n+1)
        lps.append(vars()[p_next])

        return lps

        # %% Error P22 25-65 theta recording coefficients
sphere_number = [512, 1024]
#sphere_number = [1024]
size_param = ['01680', '02350', '03200', '03360', '04299', '04370', '04480',
              '04795', '04799', '05040', '05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200', '230']
img_ref = ['00226', '00900', '00450', '00020',
           '00010', '00060', '03000', '00044']
#old_run_pm ()

# adding parameters from old runs

#sphere_number = [512]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']
s = 0
alpha_value = 1.0
_log = []
theta = np.arange(0, 181)

# Setting boundaries for angular fit
b1 = 0
b2 = 7
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

# Setting angular boundaries for the plots
a1 = 0
a2 = 181
x1 = theta[a1:a2]

dt = []  # to be used to write Legend. Pol. coefficients data


# Set te degree of Legendre Polynomials
dg = 2

if dg == 3:
    columns_to_keep = ['Ns', 'sp', 'nr', 'ni', 'm0', 'Rf',
                       'maxpol_tm', 'maxpol_pm', 'p1', 'p2', 'p3', 'p4']
elif dg == 2:
    columns_to_keep = ['Ns', 'sp', 'nr', 'ni', 'm0',
                       'Rf', 'maxpol_tm', 'maxpol_pm', 'p1', 'p2', 'p3']

for N in sphere_number:

    # Setting b2 manually
    # b2=13
    b1 = 0
    b2 = 180
    x = theta[b1:b2]
    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)

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

                maxpol_tm = tm.theta[-tm.P12 == max(-tm.P12)].values[0]
                maxpol_pm = pm.theta[-pm.P12/pm.P11 ==
                                     max(-pm.P12/pm.P11)].values[0]

                # Now the correction
                # First fit the error function with a 3rd Degree Legendre Polynomial
                xw = 2*(x-x[0])/(x[-1]-x[0]) - 1
                #xw = np.cos(np.deg2rad(x))
                #coeffs = np.polynomial.legendre.legfit(x, old_p22_err, deg=2)

                ############
                # coeffs are mapped to [-1,1] window since L.P. are orthogonal in this domain
                coeffs = L.fit(x, old_p22_err, deg=dg)
                coeff = coeffs.convert()  # this converts the coeffs in to the original domain. These are the coeffs that will be analyzed statistically and passed to New Parameterization model

                #coeffs_w = np.polynomial.legendre.legfit(xw, old_p22_err, deg=3)
                #coeffs_w = L.fit(x, old_p22_err, deg=2)

                plotting = True
                if plotting:
                    #                if mod(s,7) == 0:
                    # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
                    #                    p22_corr = pd.Series(np.polynomial.legendre.legval(x, coeffs), index=x)
                    #                    new_pm = pm.copy()
                    #                    new_pm.P22 = pm.P22.add(p22_corr, fill_value=0)
                    fig, ax = plt.subplots(ncols=2)
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
                    plt.grid()
                    plt.tight_layout()
                    plt.show()
                    plt.close()

                    # Calculating Param Csca from Qs
                aprj = ((np.pi * sp**2) * (N**(2/3)))
                c_sca_m_1 = 0.200
                c_sca_m_2 = 0.164
                c_sca_m_3 = 1.047
                c_sca_m_4 = 0.127
                c_sca_x_1 = 3.082
                c_sca_x_2 = 0.757
                m = complex(n_real, n_img)
                m0 = abs((m**2-1)/(m**2+2))
                corr_sca = 1. + c_sca_m_3 * \
                    (m0-c_sca_m_4) * np.sin(c_sca_x_1 * sp) * \
                    np.exp(-sp * c_sca_x_2)

                sw = {}

                sw['N'] = N
                sw['xm'] = sp
                sw['nr'] = n_real
                sw['ni'] = n_img
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
#                sw['p1'] = coeff.coef[0]
#                sw['p2'] = coeff.coef[1]
#                sw['p3'] = coeff.coef[2]
#                if dg == 3:
#                    sw['p4'] = coeff.coef[3]
                dt.append(sw)

                # Should you need the plots, edit the "if" below

                plotting = False

                if plotting:
                    # if np.mod(s,7) == 0:
                    # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
                    p22_corr = pd.Series(coeffs(x), index=x)

                    new_pm = old_pm.copy()
                    # P22_corr does not cover the whole domain, so fill_value is necessary
                    new_pm.P22 = (old_pm.P22).add(p22_corr, fill_value=0)
                    fig, ax = plt.subplots(ncols=3)

                    ax[0].plot(((new_pm.P22))[a1:a2], label='new_pm python')
                    ax[0].plot(((tm.P22*tm.P11))[a1:a2], '.', label='tm')
                    ax[0].set_title('New P22 Python Correction'+runid)
                    ax[0].legend()
                    plt.grid()

                    # Old fit
                    ax[1].plot(((old_pm.P22))[a1:a2], label='old_pm')
                    ax[1].plot(((tm.P22*tm.P11))[a1:a2], '.', label='tm')
                    ax[1].legend()
                    ax[1].set_title('Old P22'+runid)
                    plt.grid()

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
LP_Coeff['sp_m0'] = LP_Coeff['sp']*LP_Coeff['m0']
LP_Coeff['N_m0'] = LP_Coeff['Ns']*LP_Coeff['m0']*0.05
LP_Coeff['N_sp'] = LP_Coeff['Ns']*LP_Coeff['sp']

# Breaking in to 4 regimes
LP512_lt063 = LP_Coeff[(LP_Coeff.Ns <= 512) & (LP_Coeff.sp < 0.63)]
LP512_gt063 = LP_Coeff[(LP_Coeff.Ns <= 512) & (LP_Coeff.sp >= 0.63)]
LP1024_lt063 = LP_Coeff[(LP_Coeff.Ns >= 512) & (LP_Coeff.sp < 0.63)]
LP1024_gt063 = LP_Coeff[(LP_Coeff.Ns >= 512) & (LP_Coeff.sp >= 0.63)]
LP1024 = LP_Coeff[LP_Coeff.Ns >= 512]
LP_lt063 = LP_Coeff[LP_Coeff.sp < 0.63]
LP_gt063 = LP_Coeff[LP_Coeff.sp >= 0.63]
# %%
# Selecting m0 data
# For p1 i cant decide if I should use the corrected m0 formula or not. They are both good, but wrong formula slightly better.
# I will try the new corrected formula fordef all the others.
#
#
#
# for p1 =  data['m0'] = (abs(((a1*data.nr + np.log10(b1*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b2*data.ni)*1j)**2 + 2)))**-1.7218 a1=1, b1=0.85,a2=0.73, b2 = 18 This behave perfectly linear. Hence no need to find a fit against p1.
# for p1 = data['m0'] = (abs(((0.82*data.nr + np.log10(data.ni)*1j)**2 -1)/((0.82*data.nr + 1.95*np.log10(data.ni)*1j)+2)))**2  ADJ R^2 = 8997
#
#
# for p2 data['m0'] = (abs(((a1*data.nr + np.log10(b1*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b2*data.ni)*1j)**2 + 2)))**2 with a1 = 1.17, a2 = 0.92, b1=160, b2 = 200
# The best fit is either Poly 2 or linear a*(sin(x/4 -pi*1.15))+b*((x+1))+c*(1) with R^2 0.8289
#
#
# FOR P3 Uncorrected M0
# for p3 -> data['m0'] = (abs(((a1*data.nr + np.log10(b*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b*data.ni)*1j)+2)))**2 with a = 1.215, a2 = 2.2, b1 = 138, b2 = 50
# for p3 Linear fitting with this function: a*sin(x/2 -0.4*pi)+b*((x + 1))+c*(1) or polynomial 2nd degree. Both good, former better. R^2 = 0.8362 for linear
# Corrected M0
# data['m0'] = (abs(((a1*data.nr + np.log10(b1*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b2*data.ni)*1j)**2 + 2)))**2 with a1 = 1.38, a2 = 0.38, b1 = 170, b2 = 80
# linear fit is the best with a*(sin(x/2 -0.5*pi))+b*((x +1))+c*(1) R^2 = 0.827
#
# For p4  -> data['m0'] = (abs(((a1*data.nr + np.log10(b1*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b2*data.ni)*1j)+2)))**2 with a1 = 1.65, a2 = 2.6, b1 = 130, b2 = 65
# fit with linear function a*(sin(x-pi*1.3))+b*((x+1))+c*(1) R^2 = 0.8588
# For p4 with corrected M0
# data['m0'] = (abs(((a1*data.nr + np.log10(b1*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b2*data.ni)*1j)**2 + 2)))**2 with a1=1.95, a2 = 0.66, b1=170, b2 = 80
# linear fit is far the best a*(sin(x/2 -0.7*pi))+b*((x + 1))+c*(1) with R^2 = 0.8686. Not only in terms of R^2 but also it is much more stable and makes sense above the range


# columns_to_keep = ['Ns','sp','nr','ni', 'm0','p1','p2','p3','p4']#,'m0_p1']
t = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.6398) & (LP_Coeff.nr == 1.68)]
#t = linearize(t, lp)

t2 = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.6398) & (LP_Coeff.nr == 1.45)]
#t2 = linearize(t2, lp)

t3 = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.6398) & (LP_Coeff.nr == 1.3)]
#t3 = linearize(t3, lp)

t4 = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.6398) & (LP_Coeff.nr == 1.8)]
#t4 = linearize(t4, lp)

t5 = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.6398) & (LP_Coeff.nr == 2.0)]
#t5 = linearize(t5, lp)

t6 = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.6398) & (LP_Coeff.nr == 2.3)]
# t6 = linearize(t6, lp)def

dt = [t[columns_to_keep], t2[columns_to_keep], t3[columns_to_keep],
      t4[columns_to_keep], t5[columns_to_keep], t6[columns_to_keep]]
A064_ltd = pd.concat(dt).reset_index().drop(['index'], axis=1)


t = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.9598) & (LP_Coeff.nr == 1.68)]
#t = linearize(t, lp)

t2 = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.9598) & (LP_Coeff.nr == 1.45)]
#t2 = linearize(t2, lp)

t3 = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.9598) & (LP_Coeff.nr == 1.3)]
#t3 = linearize(t3, lp)

t4 = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.9598) & (LP_Coeff.nr == 1.8)]
#t4 = linearize(t4, lp)

t5 = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.9598) & (LP_Coeff.nr == 2.0)]
#t5 = linearize(t5, lp)
t6 = LP_Coeff[(LP_Coeff.Ns == 256) & (
    LP_Coeff.sp == 0.9598) & (LP_Coeff.nr == 2.3)]
# t6 = linearize(t6, lp)def


dt = [t[columns_to_keep], t2[columns_to_keep], t3[columns_to_keep],
      t4[columns_to_keep], t5[columns_to_keep], t6[columns_to_keep]]
A096_ltd = pd.concat(dt).reset_index().drop(['index'], axis=1)


A064 = LP_Coeff[(LP_Coeff.Ns == 256) & (LP_Coeff.sp == 0.6398)
                ].reset_index().drop(['index'], axis=1)
A064 = A064[columns_to_keep]

A096 = LP_Coeff[(LP_Coeff.Ns == 256) & (LP_Coeff.sp == 0.9598)
                ].reset_index().drop(['index'], axis=1)
A096 = A096[columns_to_keep]


# lp=2
# if lp == 1:
#    p = "p1"
# elif lp == 2:
#    p = 'p2'
# elif lp == 3:
#    p = 'p3'
# elif lp == 4:
#    p = 'p4'
# else:
#    print('wrong p values')
#
# if lp == 1:
#    m = "m0_p1"
# else:
#    m = "m0"

m = "Rf"

if True:

    plt.figure(2)
    plt.subplot(2, 2, 1)
    plt.plot(A096[m], A096[p], 'bo')
    plt.title('A096')
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(A096_ltd[m], A096_ltd[p], 'bo')
    plt.title('A096ltd')
    plt.grid(True)
    plt.tight_layout()

    plt.subplot(223)
    plt.plot(A064_ltd[m], A064_ltd[p], 'bo')

    plt.title('A064 ltd ')
    plt.grid(True)

    plt.subplot(224)
    plt.plot(A064[m], A064[p], 'bo')
    plt.title('A064 ')
    plt.grid(True)

#aagt06 = linearize(LP_Coeff[LP_Coeff.sp >= 0.6 ])
#aalt06 = linearize(LP_Coeff[LP_Coeff.sp < 0.6 ])
#aa_all = linearize(LP_Coeff)
# Now grouping is possible. Here is an example:
# LP_Coeff[(LP_Coeff['sp'] ==0.64) & (LP_Coeff['nr'] == 2)]

    # %% Error P22 25-65 theta recording coefficients
sphere_number = [64, 128, 256, 512, 1024]
#sphere_number = [1024]
size_param = ['01680', '02350', '03200', '03360', '04299', '04370', '04480',
              '04795', '04799', '05040', '05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200', '230']
img_ref = ['00226', '00900', '00450', '00020',
           '00010', '00060', '03000', '00044']
old_run_pm()

# adding parameters from old runs

#sphere_number = [512]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']
s = 0
alpha_value = 1.0
_log = []
theta = np.arange(0, 181)

# Setting boundaries for angular fit
b1 = 0
b2 = 7
b_end = 181

# Setting the b2 to fit forward scattering (where b1=0)
if b1 == 0:
    if N <= 256:
        b2 = 20
    elif N == 512:
        b2 = 13
    elif N == 1024:
        b2 = 6
else:
    b2 = b2
b2 = 7

# Setting angular boundaries for the plots
a1 = 0
a2 = 181
x1 = theta[a1:a2]

dt = []  # to be used to write Legend. Pol. coefficients data


# Set te degree of Legendre Polynomials
dg = 1

if dg == 3:
    columns_to_keep = ['Ns', 'sp', 'nr', 'ni',
                       'm0', 'Rf', 'p1', 'p2', 'p3', 'p4']
elif dg == 2:
    columns_to_keep = ['Ns', 'sp', 'nr', 'ni', 'm0', 'Rf', 'p1', 'p2', 'p3']
elif g == 1:
    columns_to_keep = ['Ns', 'sp', 'nr', 'ni', 'm0', 'A', 'B']

for N in sphere_number:

    # Setting b2 manually
    # b2=13
    t0 = 133
    x = theta[t0:]
    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)

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

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])

                tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                tm = vars()['tm'+runid+'_mx']
                pm = vars()['newpm'+runid+'_mx']
                m = complex(n_real, n_img)
                m0 = abs((m**2-1)/(m**2+2))

                enh = tm.P11[t0:]/tm.P11[t0] - 1

                # Fitting a straight line AX + B. After standartization we can remove B from model
                # Since

                _A = (enh[180] - enh[t0])/(180 - t0)

                if True:
                    fig, ax = plt.subplots(ncols=2)
                    ax[0].plot((tm.P11[t0:]/tm.P11[t0]), '.', label='tm')
    #                ax.plot(pm.P11[t0:]/pm.P11[180], '.', label = 'pm')
                    ax[0].set_title(runid)
                    ax[0].legend()

                    ax[1].plot(np.log10(tm.P11[0:]), '.', label='tm')
                    ax[1].plot(np.log10(pm.P11[0:]), '.', label='pm')
                    ax[1].set_title(runid)
                    ax[1].legend()
                    plt.show()
                    plt.close()

                sw = {}

                sw['N'] = N
                sw['sp'] = sp
                sw['nr'] = n_real
                sw['ni'] = n_img
                sw['taus_out'] = pm_eff.taus[0]
                sw['taua_out'] = pm_eff.taua[0]
#                sw['qa_tm'] = tm_eff.qa[0]
                sw['qs_tm'] = tm_eff.qs[0]
#                sw['qa_pm'] = pm_eff.qa[0]
#                sw['qs_pm'] = pm_eff.qs[0]
#                sw['cs_pm'] = pm_eff.cs[0]
#                sw['cs_tm'] = tm_eff.cs[0]
#                sw['Aproj'] = aprj
#                sw['corr_sca'] = corr_sca
                sw['m0'] = m0
#                sw['maxpol_tm'] = maxpol_tm
#                sw['maxpol_pm'] = maxpol_pm
                sw['A'] = _A

                dt.append(sw)

                # Should you need the plots, edit the "if" below

                plotting = False

                if plotting:
                    fig, ax = plt.subplots(ncols=2)
                    ax[0].plot((tm.P11[t0:]/tm.P11[t0]), '.', label='tm')
    #                ax.plot(pm.P11[t0:]/pm.P11[180], '.', label = 'pm')
                    ax[0].set_title(runid)
                    ax[0].legend()

                    ax[1].plot(np.log10(tm.P11[0:]), '.', label='tm')
                    ax[1].plot(np.log10(pm.P11[0:]), '.', label='pm')
                    ax[1].set_title(runid)
                    ax[1].legend()
                    plt.show()
                    plt.close()


LP_Coeff = pd.DataFrame(dt)
linearize(LP_Coeff)
# optional parameters which makes filtering easier visually.
#LP_Coeff['sp_m0'] = LP_Coeff['sp']*LP_Coeff['m0']
#LP_Coeff['N_m0'] = LP_Coeff['Ns']*LP_Coeff['m0']*0.05
#LP_Coeff['N_sp'] = LP_Coeff['Ns']*LP_Coeff['sp']

# Breaking in to 4 regimes
LP512_lt063 = LP_Coeff[(LP_Coeff.N <= 512) & (LP_Coeff.sp < 0.63)]
LP512_gt063 = LP_Coeff[(LP_Coeff.N <= 512) & (LP_Coeff.sp >= 0.63)]
LP1024_lt063 = LP_Coeff[(LP_Coeff.N >= 512) & (LP_Coeff.sp < 0.63)]
LP1024_gt063 = LP_Coeff[(LP_Coeff.N >= 512) & (LP_Coeff.sp >= 0.63)]
LP1024 = LP_Coeff[LP_Coeff.N >= 512]
LP_lt063 = LP_Coeff[LP_Coeff.sp < 0.63]
LP_gt063 = LP_Coeff[LP_Coeff.sp >= 0.63]
