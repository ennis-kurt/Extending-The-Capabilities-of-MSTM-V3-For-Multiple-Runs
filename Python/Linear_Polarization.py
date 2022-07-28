# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 15:09:02 2019

@author: kurt_
"""
import platform
op_sys = platform.system()
if op_sys == 'Windows':
    dtdir = 'C:\\Users\\kurt_\\Dropbox\\Code\\special\\data\\'
elif op_sys == 'Linux':
    dtdir = '/home/cihat/Dropbox/Code/special/data/'
import os
os.chdir(dtdir)
import glob
from import_tm import *
from par_import import *
from newpm_import import *
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


#def linearize(data, sec_lin = False):
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

def linearize(data, sec_lin = False):
    # This function linearize the m0. The linerization functions has to be modified each time.
    # For Forward Scattering Excluding GE256GE063 which uses defaults
    k1 = 1; l1 = 0.6; k2 = 3.4; l2 = 1.78
    e = 1
    data['Rf'] = np.log((abs(((k1*data.nr + np.log(k2*data.ni)*1j )**2 -1)/((l1*data.nr + np.log10(l2*data.ni)*1j)**2 + 2)))**e)
    # Defaults
#    k1 = 1.20; l1 = 0.66; k2 = 4.3; l2 = 1
#    e = 2 # Better Multiple Regression comparing to e = 1
#    data['Rf'] = np.log((abs(((k1*data.nr + np.log10(k2*data.ni)*1j )**2 -1)/((l1*data.nr + np.log10(l2*data.ni)*1j)**2 + 2)))**e)



    if sec_lin:
        # this needs to be modified. It is the best fit of LPi against m0. fit function obtained from matlab. Needs to be modified for each LPi
        # Incase of LP4 both linear sinisoidal function and 1st degre pol. regression fit well. Thus 2nd linearization may not be necessary
        data[m] = (-1.605e-09)*(np.sin(data.m0/2 -0.7*np.pi))+2.237e-09*((data.m0 + 1))
    return data


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
        vars()[p_next] = ((2*n + 1)*x*vars()[p] - n*vars()[p_prev])/(n+1)
        lps.append(vars()[p_next])

        return lps
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


dt=[] # to be used to write Legend. Pol. coefficients data


# Set te degree of Legendre Polynomials
dg = 2

if dg == 3:
    columns_to_keep = ['Ns','sp','nr','ni', 'm0','Rf','maxpol_tm','maxpol_pm','p1','p2','p3','p4']
elif dg == 2:
    columns_to_keep = ['Ns','sp','nr','ni', 'm0', 'Rf', 'maxpol_tm','maxpol_pm', 'p1','p2','p3']

from numpy.polynomial import Legendre as L
for N in sphere_number:



    #Setting b2 manually
    #b2=13
#    x = theta[b1:b2]
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
#                new_p22_err = (tm.P22*tm.P11 - pm.P22)[b1:b2]
#                old_p22_err = (tm.P22*tm.P11 - old_pm.P22)[b1:b2]

                theta_maxpol_tm = tm.theta[-tm.P12 == max(-tm.P12)].values[0]
                theta_maxpol_pm = pm.theta[-pm.P12/pm.P11 == max(-pm.P12/pm.P11)].values[0]
                maxpol_tm = max(-tm.P12)
                maxpol_pm = max(-pm.P12/pm.P11)
                maxpol_pm_rw = max(-pm.P12_rw/pm.P11)


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
                    plt.close()

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
                sw['alpha'] = sp
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
                sw['m0'] = m0
                sw['pm_maxpol_err'] = maxpol_tm - maxpol_pm
                sw['tm_maxpol'] = maxpol_tm
                sw['pm_maxpol'] = maxpol_pm
                sw['pmrw_mxpol'] = maxpol_pm_rw
                sw['tpol_tm'] = theta_maxpol_tm
                sw['tpol_pm'] = theta_maxpol_pm
                sw['mpol'] = pm_eff.mpol[0]
                dt.append(sw)


                # Should you need the plots, edit the "if" below

                plotting = False

                if plotting:
                #if np.mod(s,7) == 0:
                    # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
                    p22_corr = pd.Series(coeffs(x), index=x)

                    new_pm = old_pm.copy()
                    new_pm.P22 = (old_pm.P22).add(p22_corr, fill_value=0) # P22_corr does not cover the whole domain, so fill_value is necessary
                    fig, ax = plt.subplots(ncols=3,figsize=(24,6))

                    ax[0].plot(((new_pm.P22))[a1:a2], label = 'new_pm python')
                    ax[0].plot( ((tm.P22*tm.P11))[a1:a2] , '.', label = 'tm')
                    ax[0].set_title('New P22 Python Correction'+runid)
                    ax[0].legend()
                    plt.grid()

                    # Old fit
                    ax[1].plot( ((old_pm.P22))[a1:a2], label = 'old_pm')
                    ax[1].plot( ((tm.P22*tm.P11))[a1:a2], '.', label = 'tm')
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
                    plt.close()
LP_Coeff = pd.DataFrame(dt)
LP_lt063 = LP_Coeff[LP_Coeff.alpha < 0.63]
LP_gt063 = LP_Coeff[LP_Coeff.alpha >= 0.63]
LP_gt047 = LP_Coeff[LP_Coeff.alpha >= 0.47]