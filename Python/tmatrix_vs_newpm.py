# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 11:17:04 2019

@author: kurt_
"""

# -*- coding: utf-8 -*-
"""
Created o-- Fri Sep 28 16:02:52 2018

@author: kurt_
"""
import platform
op_sys = platform.system()
if op_sys == 'Windows':
    dtdir = 'C:\\Users\\kurt_\\Dropbox\\Code\\special\\data\\'
    _sl = '\\'
elif op_sys == 'Linux':
    dtdir = '/home/cihat/Dropbox/Code/special/data/'
import os
os.chdir(dtdir)
import glob
from import_tm import *
from par_import import *
      
import pandas as pd
#%config InlineBackend.figure_format = 'svg'
import matplotlib.pyplot as plt

#Re-write the functions.-
#
#add marker border to separate ni


#%%
## FUNCTIONS
#export the errors then using the matlab fit with basic fit tool
# List of all xm values

 ### NEEDS TO BE UPDATED ########
mon_size_par =[ '01680', '02350', '03200', '03360', '04370', '04480',
               '05040', '06398', '08319', '09598' ]

# Functionst

def mark_size(sphere_num):
    """ This func chooses a markszie based on sphere number """
    if sphere_num >= 1024:
        marker_size = 36
    elif sphere_num ==512:
        marker_size = 24
    elif sphere_num ==256:
        marker_size = 15
    elif sphere_num ==128:
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

    if mon_size in ['01680', '02350','03200', '03360']:
        marker_color = 'green'
    elif mon_size in ['04370', '04480', '05040']:
        marker_color = "purple"
    elif mon_size  == '06398':
        marker_color = "blue"
    elif mon_size  == '08319':
        marker_color = "red"
    elif mon_size  == '09598':
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
        marker_style = "*"# Star
    elif n_real == "130":
        marker_style = "p"  # Pentagon
    else:
        marker_style = "+"
    return marker_style

def mark_edge_color (n_img):
    """ This func chooses a marker edge color based on Imaginary linearizeactive Index """
    # Let's convert the string type ni to float

    n_img = float( ".".join(n_img[0:2]) + n_img[2:] )
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


def linearize(data, sec_lin = False):
    # This function linearize the m0. The linerization functions has to be modified each time.
    k1 = 1.20; l1 = 0.66; k2 = 4.3; l2 = 1
    e = 2 # Better M. Regression comparing to e=1
    data['m0'] = np.log((abs(((k1*data.nr + np.log10(k2*data.ni)*1j)**2 -1)/((l1*data.nr + np.log10(l2*data.ni)*1j)**2 + 2)))**e)



    if sec_lin:
        # this needs to be modified. It is the best fit of LPi against m0. fit function obtained from matlab. Needs to be modified for each LPi
        # Incase of LP4 both linear sinisoidal function and 1st degre pol. regression fit well. Thus 2nd linearization may not be necessary
        data.m0 = (-1.605e-09)*(np.sin(data.m0/2 -0.7*np.pi))+2.237e-09*((data.m0 + 1))
    return data


def calcm0( nr, ni, sec_lin = False):
    # This function linearize the m0. The linerization functions has to be modified each time.

    k1 = 1.20; l1 = 0.66; k2 = 4.3; l2 = 1
    e = 2
    rf = (abs(((k1*nr + np.log10(k2*ni)*1j)**2 -1)/((l1*nr + np.log10(l2*ni)*1j)**2 + 2)))**2


    if sec_lin:
        # this needs to be modified. It is the best fit of LPi against m0. fit function obtained from matlab. Needs to be modified for each LPi
        # Incase of LP4 both linear sinisoidal function and 1st degre pol. regression fit well. Thus 2nd linearization may not be necessary
        data.m0 = (-1.605e-09)*(np.sin(data.m0/2 -0.7*np.pi))+2.237e-09*((data.m0 + 1))
    return rf

def old_run_pm ():
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
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']

old_run_pm ()

def Leg_Pol (x,deg):

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
        vars()[p_next] = ((2*n + 1)*x*vars()[p] - n*vars()[p_prev])/(n+1) # Recursion formula to generate L.Ps
        lps.append(vars()[p_next])

    return lps

#%%

_log = []
sphere_number = [128, 256, 512, 1024]

qa_tm = [];qa_pm = []
qs_tm = [];qs_pm = []
count = 0
for N in sphere_number:

    for xm in size_param:

        for nr in real_ref:

             for ni in img_ref:

                 try:
                     missing = 't-matrix'
                     tm = vars()['tm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                     missing = ' f-fasm'
                     param = vars()['newpm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                 except KeyError:
                     print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                     _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                     continue
 #                plt.plot(np.log10(tm1024_06398_130_00226_mx['P11'].values))


                 if abs(tm.qa.values) < 1e3:


                     qa_pm.append(param.qa.values)
                     qa_tm.append(tm.qa.values)

                     # Choosing the style based on the parameter values
                     m_size = mark_size(N)
                     m_col = mark_color (xm)
                     m_st = mark_style(nr)
                     alpha_val = (1 - count/52)
                     alpha_val = np.where(alpha_val < 0.6, alpha_val, 0.6)
                     alpha_val = np.where(alpha_val > 0.35, alpha_val, 0.35)

                     plt.plot(param.qa.values,tm.qa.values,marker=m_st, markersize=m_size, color=m_col, markerfacecoloralt='black', alpha = alpha_val, markeredgecolor = 'black')
                     count+=1


                     #plt.plot(param.qs.values,tm.qs.values,marker='o', markersize=3, color="red")

                     qs_pm.append(param.qs.values)
                     qs_tm.append(tm.qs.values)





plt.show()
plt.close()

plt.scatter(qa_pm,qa_tm)
plt.plot(np.linspace(0,1.5),np.linspace(0,1.5), color="C0")
plt.show()
plt.close()

plt.scatter(qs_pm,qs_tm)
plt.plot(np.linspace(0,11),np.linspace(0,11), color="C1")
plt.show()
plt.close()

print('count %d'%count)

#%%
#sphere_number = [64, 128, 256, 512, 1024]
#size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
#real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
#img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
#def old_run_pm ()g
alpha_value = 1.0
_log = []

for N in sphere_number:

    for xm in size_param:

        for nr in real_ref:

             for ni in img_ref:

                 try:
                     missing = 't-matrix'
                     tm = vars()['tm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                     missing = ' f-fasm'
                     param = vars()['newpm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                 except KeyError:
                     #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                     _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                     continue

                 if abs(tm.qs.values) < 1e3 :


                     # Choosing the style based on the parameter values
                     m_size = mark_size(N)
                     m_col = mark_color (xm)
                     m_st = mark_style(nr)
                     m_col2 = mark_edge_color (ni)


                     plt.plot(param.qs.values,tm.qs.values,marker=m_st,\
                              markersize=m_size + 10, color=m_col2, alpha = 0.6)#,\
                              #markeredgecolor='red', markeredgewidth = N/160)

                     plt.plot(param.qs.values,tm.qs.values,marker=m_st,\
                              markersize=m_size, color=m_col, alpha = 0.6)#,\
                             # markeredgecolor='red', markeredgewidth = N/160)
                 else:
                     print('qs value is wrong in this run: tm{}_{}_{}_{}'.format(N, xm, nr, ni))




                 plt.plot(np.linspace(0,11),np.linspace(0,11), color='purple', linestyle="-.", alpha = 0.1)
                 #%% LINEAR POLARIZATION


sphere_number = [64, 128, 256, 512, 1024]
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
old_run_pm ()
sphere_number = [256, 512, 1024]
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
# adding parameters from old runs

#sphere_number = [256]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']

alpha_value = 1.0
_log = []
theta=np.arange(0,181)
x = theta[65:]
dt=[] # to be used to write Legend. Pol. coefficients data
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

                    print('There are at least one data to compare')

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])

                tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                tm =  vars()['tm'+runid+'_mx']
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
                    fig, ax = plt.subplots(ncols=3,figsize=(22,6))

                    ax[0].plot((-old_pm.P12/old_pm.P11), '.', label = 'old_pm')
                    ax[0].plot((-tm.P12), '.', label = 'tm')
                    ax[0].set_title('Old Lin Polar'+runid)
                    ax[0].legend()

                    # new fit
                    ax[1].plot((-pm.P12/pm.P11), '.', label = 'new_pm')
                    ax[1].plot((-tm.P12), '.', label = 'tm')
                    ax[1].legend()
                    ax[1].set_title('New Lin. Polar'+runid)


#                    # Error Function and the Fit
#                    ax[2].plot(x, new_p22_err, '.', label = 'new_p22_err')
#                    ax[2].plot(x, old_p22_err,'.', label = 'old_p22_err' )
#                    ax[2].legend()
#                    ax[2].set_title('p22 error & the fit')

                    # old and new p22
                    ax[2].plot(old_pm.P12/old_pm.P11 - tm.P12, '-', label = 'old_pm')
                    ax[2].plot(pm.P12/pm.P11 - tm.P12, '.', label = 'new_pm')
                    ax[2].set_title('Old & New Lin. Pol Error'+runid)
                    ax[2].legend()
                    plt.tight_layout()
                    plt.show()

            #%% P11
sphere_number = [64, 128, 256, 512, 1024]
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
old_run_pm ()
sphere_number = [256, 512, 1024]
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
# adding parameters from old runs

#sphere_number = [256]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']

alpha_value = 1.0
_log = []
theta=np.arange(0,181)
x = theta[65:]
dt=[] # to be used to write Legend. Pol. coefficients data
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

                    print('There are at least one data to compare')

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])

                tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                tm =  vars()['tm'+runid+'_mx']
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
                    fig, ax = plt.subplots(ncols=3,figsize=(22,6))

                    ax[0].plot(np.log10(old_pm.P11), '.', label = 'old_pm')
                    ax[0].plot(np.log10(tm.P11), '.', label = 'tm')
                    ax[0].set_title('Old P11'+runid)
                    ax[0].legend()

                    # new fit
                    ax[1].plot(np.log10(pm.P11), '.', label = 'new_pm')
                    ax[1].plot(np.log10(tm.P11), '.', label = 'tm')
                    ax[1].legend()
                    ax[1].set_title('New P11'+runid)


#                    # Error Function and the Fit
#                    ax[2].plot(x, new_p22_err, '.', label = 'new_p22_err')
#                    ax[2].plot(x, old_p22_err,'.', label = 'old_p22_err' )
#                    ax[2].legend()
#                    ax[2].set_title('p22 error & the fit')

                    # old and new p22
                    ax[2].plot(np.log10(old_pm.P11), '.', label = 'old_pm')
                    ax[2].plot(np.log10(pm.P11), '.', label = 'new_pm')
                    ax[2].set_title('Old & New P11 Python'+runid)
                    ax[2].legend()
                    plt.tight_layout()
                    plt.show()


                    #%% COMPARING OLD AND NEW PARAMETERIZATION FROM IDL OUTPUTS
sphere_number = [64, 128, 256, 512, 1024]
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
old_run_pm ()
#sphere_number = [128]
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
# adding parameters from old runs

#sphere_number = [256]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']

alpha_value = 1.0
_log = []
theta=np.arange(0,181)
x = theta[65:]
dt=[] # to be used to write Legend. Pol. coefficients data
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

                    print('There are at least one data to compare')

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])

                tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                tm =  vars()['tm'+runid+'_mx']
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
                    fig, ax = plt.subplots(ncols=3,figsize=(22,6))

                    ax[0].plot(np.log10(old_pm.P22), '.', label = 'old_pm')
                    ax[0].plot(np.log10(tm.P22*tm.P11), '.', label = 'tm')
                    ax[0].set_title('Old P22'+runid)
                    ax[0].legend()

                    # new fit
                    ax[1].plot(np.log10(pm.P22), '.', label = 'new_pm')
                    ax[1].plot(np.log10(tm.P22*tm.P11), '.', label = 'tm')
                    ax[1].legend()
                    ax[1].set_title('New P22'+runid)


#                    # Error Function and the Fit
#                    ax[2].plot(x, new_p22_err, '.', label = 'new_p22_err')
#                    ax[2].plot(x, old_p22_err,'.', label = 'old_p22_err' )
#                    ax[2].legend()
#                    ax[2].set_title('p22 error & the fit')

                    # old and new p22
                    ax[2].plot(np.log10(old_pm.P22), '.', label = 'old_pm')
                    ax[2].plot(np.log10(pm.P22), '.', label = 'new_pm')
                    ax[2].set_title('Old & New P22 Python'+runid)
                    ax[2].legend()
                    plt.tight_layout()
                    plt.show()



                #%% CORRECTIING P22 WITH THE COMPLETE GENERAL CORRECTION FITS
sphere_number = [64, 128, 256, 512, 1024]
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
old_run_pm ()
sphere_number = [256, 512, 1024]
size_param = [ '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
# adding parameters from old runs

#sphere_number = [256]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']
s=0
alpha_value = 1.0
_log = []
theta=np.arange(0,181)
x = theta[65:]
dt=[] # to be used to write Legend. Pol. coefficients data
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
                    s+=1

                    #print('There are at least one data to compare')


                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])

                tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                tm =  vars()['tm'+runid+'_mx']
                pm = vars()['newpm'+runid+'_mx']
                old_pm = vars()['param'+runid+'_mx']
                Rf = calcm0(n_real, n_img)
                print('Rf = {}'.format(Rf))

                new_p22_err = (tm.P22*tm.P11 - pm.P22)[65:]
                old_p22_err = (tm.P22*tm.P11 - old_pm.P22)[65:]


                # Now Correcting P22 Here
                # LPol.
                th_corr = np.arange(116) + 65
                P0 = 1
                P1 = th_corr
                P2  = 0.5*(3*th_corr**2 -1)
                P3 = 0.5*(5*th_corr**3 - 3*th_corr)
                ttl = 'LPs Deg = 3'

#                P2  = 0.5*(3*(th_corr**2) -1)
#                P3 = 0.5*(5*(th_corr**3) - (3*th_corr))

#  FIT WITH LEGNDRE POLY DEG = 4
#                if N < 256:
#                    if sp < 0.63:
#                        print('xm<=0.63 N<256')
#                        ttl = ' N < 256 & sp < 0.63'
#                        C0 = 3.145 - 35.43*N**(-0.5) - 7.849*sp - 0.05542*Rf_P1 + 266.8/N + 6.465*sp**2
#                        C1 = -0.06246 + 0.7774*N**(-0.5) + 0.1379*sp - 0.000462*Rf - 5.890/N - 0.0974*sp**2 + 0.000134*Rf**2
#                        C2 = 1e-5*(26.49 - 398.4*N**(-0.5)  - 46.74*sp + 0.635*Rf + 2711/N + 21.00*sp**2 - 0.0803*Rf**2 + 85.7*sp*N**(-0.5) - 0.938*sp*Rf)
#                        C3 = 1e-8*(-32.87 + 578.9*N**(-0.5) + 42.06*sp - 1.263*Rf - 3744/N + 0.1138*Rf**2 - 180.1*sp*N**(-0.5) + 2.499*sp*Rf)
#
#                    elif sp >= 0.63:
#                        ttl = 'N < 256 & sp >= 0.63'
#                        C0 = -0.451 - 16.45*N**(-0.5) + 0.462*sp - 0.0417*Rf_P1 + 118.1/N + 0.942*sp**2 - 0.0870*sp*Rf_P1
#                        C1 = -0.01203 + 0.4113*N**(-0.5) + 0.0523*sp - 0.001452*Rf - 3.072/N - 0.0621*sp**2 + 0.000140*Rf**2 + 0.001652*sp*Rf
#                        C2 = 0.0001949 - 0.002211*N**(-0.5) - 0.0005709*sp + 0.00000016*Rf + 0.01665/N + 0.0004893*sp**2 - 0.00000569*sp*Rf
#                        C3 = 1E-8*(-46.16 + 323.9*N**(-0.5) + 123.9*sp + 1.238*Rf - 2476/N - 93.4*sp**2 - 0.0730*Rf**2)
#                elif N >= 256:
#                    if sp < 0.63:
#                        ttl = 'N >= 256 & sp < 0.63'
#                        C0 = -0.473 - 6.774*sp + 95.24*N**(-0.5) - 0.05482*Rf_P1 - 923.9/N + 5.763*sp**2 - 8.42*sp*N**(-0.5)
#                        C1 = 0.01969 + 0.1225*sp - 2.2802*N**(-0.5) - 0.000436*Rf - 0.0792*sp**2 + 22.777/N + 0.000133*Rf**2
#                        C2 = 1e-5*(-14.60 + 1138.8*N**(-0.5) + 0.097*Rf - 37.87*sp - 11343/N - 0.0539*Rf**2 + 13.56*sp**2 )
#                        C3 = 1e-8*(26.90 + 33.22*sp - 1667.3*N**(-0.5) - 1.026*Rf + 16575/N + 0.1038*Rf**2 + 2.213*sp*Rf)
#                    elif sp >= 0.63:
#                        ttl = 'N >= 256 & sp >= 0.63'
#                        C0 = -0.895 - 9.00*N**(-0.5) + 1.19*sp - 0.0607*Rf_P1 - 173.3/N - 0.826*sp**2 + 0.01409*Rf_P1**2 + 34.31*sp*N**(-0.5) - 0.1030*sp*Rf_P1
##                        0.00566 + 0.01154 sp + 0.3092 N_std - 0.001219 M0 + 3.990 N_std*N_std + 0.000093 M0*M0 - 0.951 sp*N_std + 0.001657 sp*M0
#                        C1 = 0.00237 + 0.2055*N**(-0.5) + 0.0280*sp - 0.001471*Rf + 3.981/N - 0.01487*sp**2 + 0.000084*Rf**2 - 0.826*sp*N**(-0.5) + 0.00765*Rf*N**(-0.5) + 0.001501*sp*Rf
#                        C2 = 1E-3*(0.1271 - 1.440*N**(-0.5) - 0.4423*sp + 0.00054*Rf - 20.92/N + 0.2279*sp**2 + 4.723*sp*N**(-0.5) - 0.00599*sp*Rf)
#                        C3 = 1E-7*(-3.718 + 25.4*N**(-0.5) + 10.34*sp + 0.1486*Rf + 306/N - 5.16*sp**2 - 0.01172*Rf**2 - 75.6*sp*N**(-0.5))
#
#                print('C0, C1, C2, C3 = ', C0, C1, C2, C3)
#                P22_corr = C0*P0 + C1*P1 + C2*P2 + C3*P3

# FIT WITH LEGENDRE POL DEG = 3

#                C0 = -1.579 - 0.961*N**(-0.5) - 0.0460*Rf + 3.331*sp - 1.750*sp**2 + 0.2567*Rf*sp
#                C1 = 0.02012 + 0.01353*N**(-0.5) + 0.00196*Rf - 0.041*sp - 0.000458*Rf**2 + 0.01992*sp**2 - 0.00406*Rf*sp
#                C2 = 1e-6*(-18.25 - 37.3*N**(-0.5) - 7.21*Rf + 21.31*sp + 1.773*Rf**2 + 12.64*Rf*sp)


# Alpha 0.1 nr, ni lp deg=3

                if N >= 256:
                    if sp >= 0.63:

                        C0 = 1e-4*(-16975.0 - 25764*N**(-0.5) + 31462*sp + 7181*n_img + 784*n_real + 34490*sp*N**(-1/3) - 19996*sp**2 + 6292*n_img**2 - 14456*N**(-0.5)*n_real - 11003*sp*n_img + 2831*sp*n_real - 3470*n_img*n_real)
                        #C0	= -1.748634 + 1.213953*N**(-0.5) + 0.077905*n_real + 0.716604*n_img + 3.206932*sp - 41.257866/N + 0.637984*n_img**2 - 1.954500*sp**2 - 1.419139*n_real*N**(-0.5) + 6.630444*sp*N**(-0.5) - 0.345698*n_real*n_img + 0.281347*n_real*sp - 1.103876*n_img*sp
                        C1 =  1e-9*(23088583 + 56737779*N**(-0.5) - 39337463*sp - 12869455*n_img - 1404510*n_real - 61350003*sp*N**(-1/3) + 24864889*sp**2 - 9397056*n_img**2 + 17401258*N**(-0.5)*n_real + 16553497*sp*n_img - 3984079*sp*n_real + 6081156*n_img*n_real)

                        #C1 = 1e-9*(23970122 - 3836940*N**(-0.5) - 1397647*n_real - 12847251*n_img - 40735854*sp + 651481612*N**(-0.5)*N**(-0.5) - 9525495*n_img*n_img + 24205665*sp*sp + 17015218*N**(-0.5)*n_real - 116320844*N**(-0.5)*sp + 6062606*n_real*n_img - 3958994*n_real*sp + 16606371*n_img*sp)
                        C2 = 1E-6*(-44.26 - 153.3*N**(-0.5) + 59.8*sp + 38.96*n_img + 3.55*n_real + 158.7*sp*N**(-1/3) - 40.20*sp**2 + 28.82*n_img**2 - 41.7*N**(-0.5)*n_real - 43.58*sp*n_img + 12.49*sp*n_real - 19.89*n_img*n_real)
                        #C2 = 1e-6*(-46.659 + 32.724*N**(-0.5) + 3.53*n_real + 38.879*n_img + 62.06*sp - 2037.870/N + 29.276*n_img**2 - 37.881*sp**2 - 40.384*N**(-0.5)*n_real + 307.752*N**(-0.5)*sp - 19.821*n_real*n_img + 12.404*n_real*sp - 43.769*n_img*sp)

                    elif sp < 0.63:

                        C0 = 1e-6*(842899.0 + 28220926*N**(-0.5) - 6331451*sp + 159187*n_img - 163855*n_real - 246145239*N**(-0.5)*N**(-0.5) + 5939266*sp**2+ 16704*n_real**2 - 7267633*N**(-0.5)*sp - 1023402*N**(-0.5)*n_real - 1135069*sp*n_img + 519085*sp*n_real + 59978*n_img *n_real)

                        C1 = 1e-8*(-1141490.0 - 44580223*N**(-0.5) + 8728174*sp + 282575*n_img + 308942*n_real + 370482706/N - 7942697*sp**2 - 36447*n_real**2 + 14987028*N**(-0.5)*sp + 1425123*N**(-0.5)*n_real - 838731*sp*n_real - 77876*n_img*n_real)

                        C2 = 1e-10*(198695.0 + 11349042*N**(-0.5) - 1755465*sp - 42187*n_img - 97833*n_real - 95551058/N+ 1494842*sp**2+ 13940*n_real**2 - 3644281*N**(-0.5)*sp - 297345*N**(-0.5)*n_real + 232545*sp*n_real)






# FIT WITH NR AND NI LP DEG3. Multiple Reg Results looked promising but the actual fit here was not good especiallly araound exact backscattering region, there is an ugly downward curvature

#                C0	=	-1.874 + 1.669*N**(-0.5) + 0.889*n_img + 0.0757*n_real + 3.461*sp - 1.860*sp**2 - 1.432*N**(-0.5)*n_real - 0.3451*n_img*n_real - 1.077*n_img*sp + 0.2827*n_real*sp
#                C1	=	0.02537 + 0.01049*N**(-0.5) - 0.01574*n_img - 0.000730*n_real - 0.04626*sp + 0.02272*sp**2 + 0.006221*n_img*n_real + 0.01625*n_img*sp - 0.003528*n_real*sp
#                C2	=	-0.000049 - 0.000031*N**(-0.5) + 0.000039*n_img + 0.000002*n_real + 0.000074*sp + 0.000027*n_img**2 - 0.000032*sp**2 - 0.000020*n_img*n_real - 0.000043*n_img*sp + 0.000011*n_real*sp



                print(runid)
                print('C0, C1, C2 = ', C0, C1, C2)
                P22_corr = C0*P0 + C1*P1 + C2*P2
                P22 = old_pm['P22'].copy()

                P22[65:181] = P22_corr + old_pm.P22[65:181]



                plotting = True
                #if plotting:
                if mod(s,7) == 0:
                    # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
#                    p22_corr = pd.Series(np.polynomial.legendre.legval(x, coeffs), index=x)
#                    new_pm = pm.copy()
#                    new_pm.P22 = pm.P22.add(p22_corr, fill_value=0)
                    fig, ax = plt.subplots(ncols=3,figsize=(22,6))

                    ax[0].plot(np.log10(old_pm.P22), '.', label = 'old_pm')
                    ax[0].plot(np.log10(tm.P22*tm.P11), '.', label = 'tm')
                    ax[0].set_title('Old P22'+runid)
                    ax[0].legend()

                    # new fit
                    ax[1].plot(np.log10(pm.P22), '.', label = 'new_pm')
                    ax[1].plot(np.log10(tm.P22*tm.P11), '.', label = 'tm')
                    ax[1].legend()
                    ax[1].set_title('New P22'+runid)

                    ax[2].plot(np.log10(P22), '.', label = 'new_pm_py')
                    ax[2].plot(np.log10(tm.P22*tm.P11), '.', label = 'tm')
                    ax[2].legend()
                    ax[2].set_title('New P22 python'+runid)


#                    # Error Function and the Fit
#                    ax[2].plot(x, new_p22_err, '.', label = 'new_p22_err')
#                    ax[2].plot(x, old_p22_err,'.', label = 'old_p22_err' )
#                    ax[2].legend()
#                    ax[2].set_title('p22 error & the fit')

                    # old and new p22
#                    ax[3].plot(np.log10(old_pm.P22), '.', label = 'old_pm')
#                    ax[3].plot(np.log10(P22), '.', label = 'new_pm_py')
#                    ax[3].set_title('Old & New P22 Python'+runid)
#                    ax[3].legend()
                    plt.title(ttl)
                    plt.tight_layout()
                    plt.show()
                    #%% Error P22 25-65 theta recording coefficients
sphere_number = [64, 128, 256, 512, 1024]
#sphere_number = [1024]
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
old_run_pm ()

# adding parameters from old runs

#sphere_number = [512]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']
s=0
alpha_value = 1.0
_log = []
theta=np.arange(0,181)
b1=25
b2=65
a1 = 0
a2 = 181
x1 = theta[a1:a2]
x = theta[b1:b2]
dt=[] # to be used to write Legend. Pol. coefficients data

from numpy.polynomial import Legendre as L
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
                    s+=1

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])

                tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                tm =  vars()['tm'+runid+'_mx']
                pm = vars()['newpm'+runid+'_mx']
                old_pm = vars()['param'+runid+'_mx']
                new_p22_err = (tm.P22*tm.P11 - pm.P22)[b1:b2]
                old_p22_err = (tm.P22*tm.P11 - old_pm.P22)[b1:b2]

                # Now the correction
                # First fit the error function with a 3rd Degree Legendre Polynomial
                xw = 2*(x-x[0])/(x[-1]-x[0]) - 1
                #xw = np.cos(np.deg2rad(x))
                #coeffs = np.polynomial.legendre.legfit(x, old_p22_err, deg=2)

                ############
                coeffs = L.fit(x, old_p22_err, deg=2) # coeffs are mapped to [-1,1] window since L.P. are orthogonal in this domain
                coeff = coeffs.convert() # this converts the coeffs in to the original domain. These are the coeffs that will be analyzed statistically and passed to New Parameterization model

                #coeffs_w = np.polynomial.legendre.legfit(xw, old_p22_err, deg=3)
                #coeffs_w = L.fit(x, old_p22_err, deg=2)

                plotting = False
                if plotting:
#                if mod(s,7) == 0:
                    # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
#                    p22_corr = pd.Series(np.polynomial.legendre.legval(x, coeffs), index=x)
#                    new_pm = pm.copy()
#                    new_pm.P22 = pm.P22.add(p22_corr, fill_value=0)
                    fig, ax = plt.subplots(ncols=2,figsize=(22,6))
                    p22_err = (tm.P22*tm.P11 - old_pm.P22)[a1:a2]
                    ax[0].plot((old_pm.P22[a1:a2]), '.', label = 'pm')
                    ax[0].plot((tm.P22*tm.P11)[a1:a2], '.', label = 'tm')
                    ax[0].set_title('Old P22'+runid)
                    ax[0].legend()

                    ax[1].plot(x1, p22_err/(tm.P22*tm.P11)[a1:a2],'.', x1, np.zeros(len(x1),),label = 'Relative p22_err' )
                    ax[1].legend()

                    # new fit
#                    ax[1].plot((pm.P22), '.', label = 'new_pm')
#                    ax[1].plot((tm.P22*tm.P11), '.', label = 'tm')
#                    ax[1].legend()
#                    ax[1].set_title('New P22'+runid)

                    # Error Function and the Fit
#                    ax[2].plot(x, new_p22_err, '.', label = 'new_p22_err')
                    #ax[2].plot(x, old_p22_err,'.', label = 'old_p22_err' )
                    #ax[2].legend()
#                    ax[2].set_title('p22 error & the fit')

                    # old and new p22
#                    ax[3].plot((old_pm.P22), '.', label = 'old_pm')
#                    ax[3].plot((pm.P22), '.', label = 'new_pm')
#                    ax[3].set_title('Old & New P22'+runid)
#                    ax[3].legend()
                    plt.grid()
                    plt.tight_layout()
                    plt.show()

                              # Calculating Param Csca from Qs
                srf=((np.pi * sp**2) * (N**(2/3)))
                c_sca_m_1 = 0.200
                c_sca_m_2 = 0.164
                c_sca_m_3 = 1.047
                c_sca_m_4 = 0.127
                c_sca_x_1 = 3.082
                c_sca_x_2 = 0.757
                m = complex(n_real, n_img)
                m0 = abs((m**2-1)/(m**2+2))
                corr_sca = 1. + c_sca_m_3 * (m0-c_sca_m_4)* np.sin(c_sca_x_1 * sp) * np.exp(-sp * c_sca_x_2)



                sw={}

                sw['Ns'] = N
                sw['sp'] = sp
                sw['nr'] = n_real
                sw['ni'] = n_img
                sw['pm_taus'] = pm_eff.taus[0]
                sw['pm_taua'] = pm_eff.taua[0]
#                sw['qa_tm'] = tm_eff.qa[0]
#                sw['qs_tm'] = tm_eff.qs[0]
#                sw['qa_pm'] = pm_eff.qa[0]
#                sw['qs_pm'] = pm_eff.qs[0]
#                sw['cs_pm'] = pm_eff.cs[0]
#                sw['cs_tm'] = tm_eff.cs[0]
#                sw['srf'] = srf
#                sw['corr_sca'] = corr_sca
                sw['m'] = m0
                sw['p1'] = coeff.coef[0]
                sw['p2'] = coeff.coef[1]
                sw['p3'] = coeff.coef[2]
                #sw['p4'] = coeffs[3]
                dt.append(sw)


                # Should you need the plots, edit the "if" below

                plotting = True

                if plotting:
                #if np.mod(s,7) == 0:
                    # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
                    if sp < 0.63 and N >= 512:
                        p22_corr = pd.Series(coeffs(x), index=x)

                        new_pm = old_pm.copy()
                        new_pm.P22 = (old_pm.P22).add(p22_corr, fill_value=0) # P22_corr does not cover the whole domain, so fill_value is necessary
                        fig, ax = plt.subplots(ncols=3,figsize=(24,6))

                        ax[0].plot((np.log10(new_pm.P22))[a1:a2], label = 'new_pm python')
                        ax[0].plot( (np.log10(tm.P22*tm.P11))[a1:a2] , '.', label = 'tm')
                        ax[0].set_title('New P22 Python Correction'+runid)
                        ax[0].legend()
                        plt.grid()

                        # Old fit
                        ax[1].plot( (np.log10(old_pm.P22))[a1:a2], label = 'old_pm')
                        ax[1].plot( (np.log10(tm.P22*tm.P11))[a1:a2], '.', label = 'tm')
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
                        ax[2].plot(x, old_p22_err , '.', label = 'p22_err')
                        ax[2].plot(x, p22_corr,'.', label = 'p22_corr' )
                        ax[2].legend()
                        ax[2].set_title('P22 error & the fit')
                        plt.grid()
                        plt.tight_layout()
                        plt.show()


#%%
lp=3
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
LP1024 = LP_Coeff[ LP_Coeff.Ns >= 512 ]
LP_lt063 = LP_Coeff[LP_Coeff.sp < 0.63]
LP_gt063 = LP_Coeff[LP_Coeff.sp >= 0.63]
##%%
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



columns_to_keep = ['Ns','sp','nr','ni', 'm0','p1','p2','p3','m'] #,'p4','m0_p1']
t = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 1.68 )  ]
#t = linearize(t, lp)

t2 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 1.45 )  ]
#t2 = linearize(t2, lp)

t3 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 1.3 )  ]
#t3 = linearize(t3, lp)

t4 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 1.8 )  ]
#t4 = linearize(t4, lp)

t5 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 2.0 )  ]
#t5 = linearize(t5, lp)

t6 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 2.3 )  ]
#t6 = linearize(t6, lp)def

dt=[t[columns_to_keep],t2[columns_to_keep], t3[columns_to_keep], t4[columns_to_keep], t5[columns_to_keep], t6[columns_to_keep]]
A064_ltd = pd.concat(dt).reset_index().drop(['index'], axis = 1)



t = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 1.68 )  ]
#t = linearize(t, lp)

t2 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 1.45 )  ]
#t2 = linearize(t2, lp)

t3 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 1.3 )  ]
#t3 = linearize(t3, lp)

t4 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 1.8 )  ]
#t4 = linearize(t4, lp)

t5 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 2.0 )  ]
#t5 = linearize(t5, lp)
t6 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 2.3 )  ]
#t6 = linearize(t6, lp)def


dt=[t[columns_to_keep],t2[columns_to_keep], t3[columns_to_keep], t4[columns_to_keep], t5[columns_to_keep], t6[columns_to_keep]]
A096_ltd = pd.concat(dt).reset_index().drop(['index'], axis = 1)


A064 = LP_Coeff[(LP_Coeff.Ns == 256) & (LP_Coeff.sp == 0.6398)].reset_index().drop(['index'], axis = 1)
A064 = A064[columns_to_keep]

A096 = LP_Coeff[(LP_Coeff.Ns == 256) & (LP_Coeff.sp == 0.9598)].reset_index().drop(['index'], axis = 1)
A096 = A096[columns_to_keep]


#lp=2
#if lp == 1:
#    p = "p1"
#elif lp == 2:
#    p = 'p2'
#elif lp == 3:
#    p = 'p3'
#elif lp == 4:
#    p = 'p4'
#else:
#    print('wrong p values')
#
#if lp == 1:
#    m = "m0_p1"
#else:
#    m = "m0"

m = "m0"
plt.figure(2, figsize=(14,5))
plt.subplot(2, 2, 1)
plt.plot(A096[m],A096[p],'bo');
plt.title('A096')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(A096_ltd[m],A096_ltd[p],'bo');
plt.title('A096ltd')
plt.grid(True)
plt.tight_layout()

plt.subplot(223)
plt.plot(A064_ltd[m],A064_ltd[p],'bo');

plt.title('A064 ltd ')
plt.grid(True)

plt.subplot(224)
plt.plot(A064[m],A064[p],'bo');
plt.title('A064 ')
plt.grid(True)

#aagt06 = linearize(LP_Coeff[LP_Coeff.sp >= 0.6 ])
#aalt06 = linearize(LP_Coeff[LP_Coeff.sp < 0.6 ])
#aa_all = linearize(LP_Coeff)
# Now grouping is possible. Here is an example:
# LP_Coeff[(LP_Coeff['sp'] ==0.64) & (LP_Coeff['nr'] == 2)]
#%%
sphere_number = [64, 128, 256, 512, 1024]
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
old_run_pm ()

# adding parameters from old runs

#sphere_number = [256]
#size_param = ['01680']
#real_ref = ['130']
#img_ref = ['00226']
s=0
alpha_value = 1.0
_log = []
theta=np.arange(0,181)
x = theta[65:]
dt=[] # to be used to write Legend. Pol. coefficients data
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
                    s+=1

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])

                tm_eff['cs'] = tm_eff.qs[0]*np.pi*(sp*N**(1/3))**2
                tm =  vars()['tm'+runid+'_mx']
                pm = vars()['newpm'+runid+'_mx']
                old_pm = vars()['param'+runid+'_mx']
                new_p22_err = (tm.P22*tm.P11 - pm.P22)[65:]
                old_p22_err = (tm.P22*tm.P11 - old_pm.P22)[65:]

                # Now the correction
                # First fit the error function with a 3rd Degree Legendre Polynomial

                coeffs = np.polynomial.legendre.legfit(x, p22_err, deg=3)

                rsq = 1- np.polynomial.legendre.legfit(x, p22_err, deg=3,full = True)[1][0][0]



                # Calculating Param Csca from Qs
                srf=((np.pi * sp**2) * (N**(2/3)))
                c_sca_m_1 = 0.200
                c_sca_m_2 = 0.164
                c_sca_m_3 = 1.047
                c_sca_m_4 = 0.127
                c_sca_x_1 = 3.082
                c_sca_x_2 = 0.757
                m = complex(n_real, n_img)
                m0 = abs((m**2-1)/(m**2+2))
                corr_sca = 1. + c_sca_m_3 * (m0-c_sca_m_4)* np.sin(c_sca_x_1 * sp) * np.exp(-sp * c_sca_x_2)
                m = complex(n_real, n_img)
                m0 = abs((m**2-1)/(m**2+2))


                sw={}

                sw['Ns'] = N
                sw['sp'] = sp
                sw['nr'] = n_real
                sw['ni'] = n_img
                sw['qa_tm'] = tm_eff.qa[0]
                sw['qs_tm'] = tm_eff.qs[0]
                sw['qa_pm'] = pm_eff.qa[0]
                sw['qs_pm'] = pm_eff.qs[0]
                sw['cs_pm'] = pm_eff.cs[0]
                sw['cs_tm'] = tm_eff.cs[0]
                sw['srf'] = srf
                sw['corr_sca'] = corr_sca
                sw['m'] = m0
                sw['p1'] = coeffs[0]
                sw['p2'] = coeffs[1]
                sw['p3'] = coeffs[2]
                sw['p4'] = coeffs[3]
                sw['r_sqr'] = rsq
                dt.append(sw)


                # Should you need the plots, edit the "if" below

                plotting = False
                #if plotting:
                if mod(s,7) == 0:
                    # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
#                    p22_corr = pd.Series(np.polynomial.legendre.legval(x, coeffs), index=x)
#                    new_pm = pm.copy()
#                    new_pm.P22 = pm.P22.add(p22_corr, fill_value=0)
                    fig, ax = plt.subplots(ncols=3,figsize=(22,6))

                    ax[0].plot(np.log10(old_pm.P22), '.', label = 'old_pm')
                    ax[0].plot(np.log10(tm.P22*tm.P11), '.', label = 'tm')
                    ax[0].set_title('Old P22'+runid)
                    ax[0].legend()

                    # new fit
                    ax[1].plot(np.log10(pm.P22), '.', label = 'new_pm')
                    ax[1].plot(np.log10(tm.P22*tm.P11), '.', label = 'tm')
                    ax[1].legend()
                    ax[1].set_title('New P22'+runid)

                    # Error Function and the Fit
                    ax[2].plot(x, new_p22_err, '.', label = 'new_p22_err')
                    ax[2].plot(x, old_p22_err,'.', label = 'old_p22_err' )
                    ax[2].legend()
                    ax[2].set_title('p22 error & the fit')

                    # old and new p22
#                    ax[3].plot(np.log10(old_pm.P22), '.', label = 'old_pm')
#                    ax[3].plot(np.log10(pm.P22), '.', label = 'new_pm')
#                    ax[3].set_title('Old & New P22'+runid)
#                    ax[3].legend()
                    plt.tight_layout()
                    plt.show()

lp=1
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
linearize(LP_Coeff,lp)
# optional parameters which makes filtering easier visually.
LP_Coeff['sp_m0'] = LP_Coeff['sp']*LP_Coeff['m0']
LP_Coeff['N_m0'] = LP_Coeff['Ns']*LP_Coeff['m0']*0.05
LP_Coeff['N_sp'] = LP_Coeff['Ns']*LP_Coeff['sp']

# Breaking in to 4 regimes
LP512_lt063 = LP_Coeff[(LP_Coeff.Ns <= 512) & (LP_Coeff.sp < 0.63)]
LP512_gt063 = LP_Coeff[(LP_Coeff.Ns <= 512) & (LP_Coeff.sp >= 0.63)]
LP1024_lt063 = LP_Coeff[(LP_Coeff.Ns >= 512) & (LP_Coeff.sp < 0.63)]
LP1024_gt063 = LP_Coeff[(LP_Coeff.Ns >= 512) & (LP_Coeff.sp >= 0.63)]
LP1024 = LP_Coeff[ LP_Coeff.Ns >= 512 ]
LP_lt063 = LP_Coeff[LP_Coeff.sp < 0.63]
LP_gt063 = LP_Coeff[LP_Coeff.sp >= 0.63]
#%%
# Selecting m0 data
# For p1 i cant decide if I should use the corrected m0 formula or not. They are both good, but wrong formula slightly better.
# I will try the new corrected formula for all the others.
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



columns_to_keep = ['Ns','sp','nr','ni', 'm0','p1','p2','p3','p4','m']
t = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 1.68 )  ]
#t = linearize(t, lp)

t2 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 1.45 )  ]
#t2 = linearize(t2, lp)

t3 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 1.3 )  ]
#t3 = linearize(t3, lp)

t4 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 1.8 )  ]
#t4 = linearize(t4, lp)

t5 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 2.0 )  ]
#t5 = linearize(t5, lp)

t6 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.6398 )  &  (LP_Coeff.nr == 2.3 )  ]
#t6 = linearize(t6, lp)def

dt=[t[columns_to_keep],t2[columns_to_keep], t3[columns_to_keep], t4[columns_to_keep], t5[columns_to_keep], t6[columns_to_keep]]
A064_ltd = pd.concat(dt).reset_index().drop(['index'], axis = 1)



t = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 1.68 )  ]
#t = linearize(t, lp)

t2 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 1.45 )  ]
#t2 = linearize(t2, lp)

t3 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 1.3 )  ]
#t3 = linearize(t3, lp)

t4 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 1.8 )  ]
#t4 = linearize(t4, lp)

t5 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 2.0 )  ]
#t5 = linearize(t5, lp)

t6 = LP_Coeff[(LP_Coeff.Ns == 256) &  (LP_Coeff.sp== 0.9598 )  &  (LP_Coeff.nr == 2.3 )  ]
#t6 = linearize(t6, lp)def


dt=[t[columns_to_keep],t2[columns_to_keep], t3[columns_to_keep], t4[columns_to_keep], t5[columns_to_keep], t6[columns_to_keep]]
A096_ltd = pd.concat(dt).reset_index().drop(['index'], axis = 1)


A064 = LP_Coeff[(LP_Coeff.Ns == 256) & (LP_Coeff.sp == 0.6398)].reset_index().drop(['index'], axis = 1)
A064 = A064[columns_to_keep]

A096 = LP_Coeff[(LP_Coeff.Ns == 256) & (LP_Coeff.sp == 0.9598)].reset_index().drop(['index'], axis = 1)
A096 = A096[columns_to_keep]


plt.figure(2, figsize=(14,5))
plt.subplot(2, 2, 1)
plt.plot(A096.m0,A096[p],'bo');
plt.grid(True)
plt.subplot(2, 2, 2)
plt.plot(A096_ltd.m0,A096_ltd[p],'bo');
plt.grid(True)
plt.tight_layout()

plt.subplot(223)
plt.plot(A064_ltd.m0,A064_ltd[p],'bo');
plt.grid(True)

#aagt06 = linearize(LP_Coeff[LP_Coeff.sp >= 0.6 ])
#aalt06 = linearize(LP_Coeff[LP_Coeff.sp < 0.6 ])
#aa_all = linearize(LP_Coeff)
# Now grouping is possible. Here is an example:
# LP_Coeff[(LP_Coeff['sp'] ==0.64) & (LP_Coeff['nr'] == 2)]
#%%
                ######## P11 FIT ##########

#%%
sphere_number = [64, 128, 256, 512, 1024]
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
old_run_pm ()
alpha_value = 1.0
_log = []
theta=np.arange(0,181)
v0 = 0
v1 = 180
bound0 = 25
bound1 = 74

x = theta[bound0:bound1]

for N in sphere_number:

    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                try:
                    missing = 't-matrix'
                    tm = vars()['tm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                    missing = ' f-fasm'
                    param = vars()['newpm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)
                tm =  vars()['tm'+runid+'_mx']
                pm = vars()['newpm'+runid+'_mx']
                old_pm = vars()['param'+runid+'_mx']
                P11_err = (tm.P11 - pm.P11)[bound0:bound1]

                # Now the correction
                # First fit the error function with a 3rd Degree Legendre Polynomial


                z = np.polynomial.legendre.Legendre.fit(x, P11_err, deg=2)
                # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix

                P11_corr = pd.Series(z(x), index=x)
                new_pm = pm.copy()
                new_pm.P11 = pm.P11.add(P11_corr, fill_value=0)
                fig, ax = plt.subplots(ncols=3,figsize=(22,6))

                ax[0].plot(np.log10(new_pm.P11[v0:v1]), '.', label = 'new_pm')
                ax[0].plot(np.log10(tm.P11[v0:v1]), '.', label = 'tm')
                ax[0].set_title('New P11'+runid)
                ax[0].legend()

                # Old fit
                ax[1].plot(np.log10(old_pm.P11[v0:v1]), '.', label = 'old_pm')
                ax[1].plot(np.log10(tm.P11[v0:v1]), '.', label = 'tm')
                ax[1].legend()
                ax[1].set_title('Old P11'+runid)

                # Error Function and the Fit
                ax[2].plot(x, P11_err, '.', label = 'P11_err')
                ax[2].plot(x, P11_corr,'.', label = 'P11_corr' )
                ax[2].legend()
                ax[2].set_title('P11 error & the fit')
                plt.tight_layout()
                plt.show()

#* Before Trying to do any of the below, First collect all the coeeefiicients of the legend. pol. in a pd.DataFrame. Then by grouping, plot each coeeffcient against a parameter while keeping all the others constant. Repeat this for all the parameters. Then What.
#
#* I will find a function for each paramater against each coeefficient. If all the functions are linear for a coeff. then this means product is (f(N)*f(xm)*f(nr)*f(ni)). If for example N is not linear then find a version of N which will give a linear function. This means, if, for example, logN gives linear then the coefficient is modelled with (log(N)*xm*nr*ni) assuming all the others linear.
#
#* After finding the linear functions for each coeff. Now find the function for the product of (f(N)*f(xm)*f(nr)*f(ni)) in its form for the coeeficient which is being fitted against that coeeficient.
#
#    I will at the end find F((f(N)*f(xm)*f(nr)*f(ni)))P0 + G((f(N)*f(xm)*f(nr)*f(ni)))*P1 + ... *P4
#    Where P1 P2 ... are the first the second, third and the fourth terms of the legendre polynomial.
#
#*Warning. Be sure if I need the product of each parameters functions for each coeff. or the sum of the parameter functions to fit the coeeff.
#     This means: Which one is true: (f(N)*f(xm)*f(nr)*f(ni)) or (f(N) + f(xm) + f(nr) + f(ni))
#
#
#
#* Then fit the plot to see if it makes sense. if it does then do the same thing
#
#* Errors are decreasing as the xm increases when nr = 1.3 ni=0.023
#
#* Now test nr=1.3 ni = 0.090
#
#* and ni = 0.023 and nr = 2.0
#
#* looks like as xm increasing quantum effect in the backscattering is kicking. This increases the error because there is a positive bias in the model which is surpressed by the coherent backscattering enahncement near the exact backscattering.
#
#* if the above is true then this should appear more cearly with nr = 2.0 because quantum effect is more strong. [ Yes Confirmed ]
#
#* But there is more:  Look at 1024 03360 200 00226. Correction has the same shape as 1024 06398 200 00226. This suggest that after some point quantum effect start kickng when N is increasing. Since 1024 shows minimal quantum effect we can start from this.
#
#* now find the threshold where the quantum effect starts for each of the other parameters. some kind of their product should define the threshold for quantum effect. When you finbd this value you can check possible different combinations of parameters which give the same value. If quantum effect is similar for all those combinations then i can be confident about this threshold value ( this threshold is probably in this form N^i * xm^j * nr^k * ni^l)

#%% Pure P22 correction


#%%
sphere_number = [64, 128, 256, 512, 1024]
size_param = ['01680', '02350','03200', '03360','04299', '04370', '04480','04795', '04799', '05040','05299', '05795', '06398', '07300', '08319', '09598']
real_ref = ['130', '145', '166', '168', '171', '180', '200','230']
img_ref = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
old_run_pm ()
alpha_value = 1.0
_log = []
theta=np.arange(0,181)
v0 = 0
v1 = 180
bound0 = 25
bound1 = 65
# forward (0:13 or 12), backward (0:65), intermediate (25:65)
x = theta[bound0:bound1]

for N in sphere_number:

    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                try:
                    missing = 't-matrix'
                    tm = vars()['tm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                    missing = ' f-fasm'
                    param = vars()['newpm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)
                tm =  vars()['tm'+runid+'_mx']
                pm = vars()['newpm'+runid+'_mx']
                old_pm = vars()['param'+runid+'_mx']
                P22_err = (tm.P22*tm.P11 - old_pm.P22)[bound0:bound1]

                # Now the correction
                # First fit the error function with a 3rd Degree Legendre Polynomial


                z = np.polynomial.legendre.Legendre.fit(x, P22_err, deg=2)
                # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix

                P22_corr = pd.Series(z(x), index=x)
                new_pm = old_pm.copy()
                new_pm.P22 = old_pm.P22.add(P22_corr, fill_value=0)
                fig, ax = plt.subplots(ncols=3,figsize=(22,6))

                ax[0].plot(np.log10(new_pm.P22[v0:v1]), '.', label = 'new_pm')
                ax[0].plot(np.log10(tm.P22*tm.P11[v0:v1]), '.', label = 'tm')
                ax[0].set_title('New P22'+runid)
                ax[0].legend()

                # Old fit
                ax[1].plot(np.log10(old_pm.P22[v0:v1]), '.', label = 'old_pm')
                ax[1].plot(np.log10(tm.P22*tm.P11[v0:v1]), '.', label = 'tm')
                ax[1].legend()
                ax[1].set_title('Old P22'+runid)

                # Error Function and the Fit
                ax[2].plot(x, P22_err, '.', label = 'P22_err')
                ax[2].plot(x, P22_corr,'.', label = 'P22_corr' )
                ax[2].legend()
                ax[2].set_title('P22 error & the fit')
                plt.tight_layout()
                plt.show()




#%% Code Testing Cell
#answer = input('Running the test')

print((-newpm512_06398_200_00900_mx.P12/newpm512_06398_200_00900_mx.P11).idxmax())
print((-tm256_06398_200_00900_mx.P12).idxmax())
plt.plot(-newpm512_06398_200_00900_mx.P12/newpm512_06398_200_00900_mx.P11)
plt.plot(-tm512_06398_200_00900_mx.P12)
plt.plot(((-newpm512_06398_200_00900_mx.P12/newpm512_06398_200_00900_mx.P11) + tm512_06398_200_00900_mx.P12)*10 )
plt.legend('PT')

#%%
plt.plot(((-newpm512_06398_200_00900_mx.P12/newpm512_06398_200_00900_mx.P11) + tm512_06398_200_00900_mx.P12)*10 )
plt.plot(((-newpm1024_06398_200_00900_mx.P12/newpm1024_06398_200_00900_mx.P11) + tm1024_06398_200_00900_mx.P12)*10 )
plt.legend('512','1024')

#%%
plt.plot(newpm128_06398_200_00900_mx.P22/newpm128_06398_200_00900_mx.P11)
plt.plot(newpm256_06398_200_00900_mx.P22/newpm256_06398_200_00900_mx.P11)
plt.plot(newpm512_06398_200_00900_mx.P22/newpm512_06398_200_00900_mx.P11)
plt.plot(newpm1024_06398_200_00900_mx.P22/newpm1024_06398_200_00900_mx.P11)
plt.legend(['N128','N256','N512','N1024'])

#%%
plt.plot(np.log10(tm128_06398_200_00900_mx.P22*tm128_06398_200_00900_mx.P11), linewidth = 5, alpha=0.3)
plt.plot(np.log10(tm256_06398_200_00900_mx.P22*tm256_06398_200_00900_mx.P11), linewidth = 5, alpha=0.3)
plt.plot(np.log10(tm512_06398_200_00900_mx.P22*tm512_06398_200_00900_mx.P11), linewidth = 5, alpha=0.3)
plt.plot(np.log10(tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11), linewidth = 5, alpha=0.3)

plt.plot(np.log10(newpm128_06398_200_00900_mx.P22), '-.')
plt.plot(np.log10(newpm256_06398_200_00900_mx.P22), '-.')
plt.plot(np.log10(newpm512_06398_200_00900_mx.P22), '-.')
plt.plot(np.log10(newpm1024_06398_200_00900_mx.P22), '-.')

plt.legend(['N128','N256','N512','N1024'])
#%%
plt.plot(np.log10(tm128_06398_200_00226_mx.P22*tm128_06398_200_00226_mx.P11), linewidth = 5, alpha=0.5)
#plt.plot(np.log10(tm256_06398_200_00226_mx.P22*tm256_06398_200_00226_mx.P11), linewidth = 5, alpha=0.3)
#plt.plot(np.log10(tm512_06398_200_00226_mx.P22*tm512_06398_200_00226_mx.P11), linewidth = 5, alpha=0.3)
plt.plot(np.log10(tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11), linewidth = 5, alpha=0.5)
#
#plt.plot(np.log10(newpm128_06398_200_00226_mx.P22), '-.')
##plt.plot(np.log10(newpm256_06398_200_00226_mx.P22), '-.')
##plt.plot(np.log10(newpm512_06398_200_00226_mx.P22), '-.')
#plt.plot(np.log10(newpm1024_06398_200_00226_mx.P22), '-.')

plt.plot(np.log10(tm128_06398_200_00900_mx.P22*tm128_06398_200_00900_mx.P11), linewidth = 5, alpha=0.5)
plt.plot(np.log10(tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11), linewidth = 5, alpha=0.5)

#plt.plot(np.log10(newpm128_06398_200_00900_mx.P22), '-')
#plt.plot(np.log10(newpm1024_06398_200_00900_mx.P22), '-')

#plt.legend(['N128','N256','N512','N1024'])

#%%
plt.plot(np.log(tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11 - newpm1024_06398_130_00226_mx.P22), linewidth = 2, alpha=0.5, color='k')
plt.plot(np.log(tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11))
plt.plot(np.log(newpm1024_06398_130_00226_mx.P22))
plt.legend(['error', 'tm','newpm'])


#%%%
#Only p22 errors
plt.plot((tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11[0:] - newpm1024_06398_130_00226_mx.P22[0:])/(tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11[0:]), linewidth = 2, alpha=0.5, linestyle= '-.')
plt.plot((tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11[0:] - newpm1024_06398_200_00226_mx.P22[0:])/(tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11[0:]), linewidth = 2, alpha=0.5,linestyle='-')

plt.plot((tm1024_06398_130_00900_mx.P22*tm1024_06398_130_00900_mx.P11[0:] - newpm1024_06398_130_00900_mx.P22[0:])/(tm1024_06398_130_00900_mx.P22*tm1024_06398_130_00900_mx.P11[0:]), linewidth = 2, alpha=0.5, linestyle= '-.')
plt.plot((tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11[0:] - newpm1024_06398_200_00900_mx.P22[0:])/(tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11[0:]), linewidth = 2, alpha=0.5,linestyle='-')

plt.title(' P22 Relative error')
plt.legend(['1.3 & 0.023','2.0  & 0.023', '1.3 & 0.090','2.0  & 0.090'])

#%%
# Absolute error P22
plt.plot((tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11[25:] - newpm1024_06398_130_00226_mx.P22[25:]), linewidth = 2, alpha=0.5, linestyle= '-.')
plt.plot((tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11[25:] - newpm1024_06398_200_00226_mx.P22[25:]), linewidth = 2, alpha=0.5,linestyle='-')

plt.plot((tm1024_06398_130_00900_mx.P22*tm1024_06398_130_00900_mx.P11[25:] - newpm1024_06398_130_00900_mx.P22[25:]), linewidth = 2, alpha=0.5, linestyle= '-.')
plt.plot((tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11[25:] - newpm1024_06398_200_00900_mx.P22[25:]), linewidth = 2, alpha=0.5,linestyle='-')


##plt.plot(tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11[25:], linestyle = ':', linewidth=4)
#plt.plot((tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11[25:]), linestyle = ':', linewidth=4)
#
##plt.plot(newpm1024_06398_130_00226_mx.P22[25:], linestyle = (0, (3, 1, 1, 1, 1, 1)), linewidth=4)
#plt.plot((newpm1024_06398_200_00226_mx.P22[25:]), linestyle = (0, (3, 1, 1, 1, 1, 1)), linewidth=4)


plt.title('P22 Absolute Error')
plt.legend(['1.3 & 0.023','2.0  & 0.023', '1.3 & 0.090','2.0  & 0.090'])

#%%

# Errors Here

p2210246413023err = tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11 - newpm1024_06398_130_00226_mx.P22
p2210246413009 = tm1024_06398_130_00900_mx.P22*tm1024_06398_130_00900_mx.P11[0:] - newpm1024_06398_130_00900_mx.P22[0:]
p22102464200226err = tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11[0:] - newpm1024_06398_200_00226_mx.P22[0:]
p221024642009 = tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11 - newpm1024_06398_200_00900_mx.P22

#%%
# Fit the data using polynomials
theta=np.arange(0,181)
x = theta[25:]
p22 = p221024642009[25:]
z1=np.poly1d(np.polyfit(x, p22, deg=3))
z0 = np.polynomial.legendre.Legendre.fit(x,p22, deg=3)

fig, axes = plt.subplots(ncols=2, figsize=(18,6))
axes[0].plot(x, p22,'.', x, z1(x), '.')
axes[0].set_title('Simple Pol. Fit')
axes[1].plot(x, p22,'.', x, z0(x), '.')
axes[1].set_title('Legendre Pol. Fit')
plt.tight_layout()
plt.show()

#%%



#Now Add the correction to the param p22 and on the left plot new param with tm and on the right old param to pm then compare the errors, abs and rel.

new_param1024_06398_200_00900_mx = param1024_06398_200_00900_mx.copy()
new_param1024_06398_200_00900_mx.P22 = param1024_06398_200_00900_mx.P22.add( p221024642009[25:], fill_value=0)
fig, ax = plt.subplots(ncols=2,figsize=(18,6))

ax[0].plot(np.log10(new_param1024_06398_200_00900_mx.P22), '.')
ax[0].plot(np.log10(tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11), '.')

# Old fit
ax[1].plot(np.log10(param1024_06398_200_00900_mx.P22), '.')
ax[1].plot(np.log10(tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11), '.')
plt.tight_layout()
plt.show()
