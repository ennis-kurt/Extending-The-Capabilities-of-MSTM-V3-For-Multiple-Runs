# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:53:57 2019

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

              #%% Writing Efficiencies to an output
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


dt=[] # to be used to write the whole data into an outpu


for N in sphere_number:

    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)
                #print(runid)
                try:
                    missing = 't-matrix'
                    tm_eff = vars()['tm'+runid+'_eff']
                    missing = ' f-fasm'
                    pm_eff = vars()['newpm'+runid+'_eff']
                    s+=1
                    print(s)
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
#                old_pm = vars()['param'+runid+'_mx']

                # Calculating Param Csca from Qs
                aprj=((np.pi * sp**2) * (N**(2/3)))
                c_sca_m_1 = 0.200
                c_sca_m_2 = 0.164
                c_sca_m_3 = 0.533451# original 1.047
                c_sca_m_4 = 0.0784451#0.127
                c_sca_x_1 = 4.64024#3.082
                c_sca_x_2 = -0.18188


                m = complex(n_real, n_img)
                m0 = abs((m**2-1)/(m**2+2))

                c_sca_m_3 = 0.533451# original 1.047
                c_sca_m_4 = 0.0784451#0.127
                c_sca_x_1 = 4.64024#3.082
                c_sca_x_2 = -0.18188
                corr_sca = 1. + c_sca_m_3 * (m0-c_sca_m_4)* np.sin(c_sca_x_1 * sp) * np.exp(-sp * c_sca_x_2)

                c_sca_m_3 =  1.047
                c_sca_m_4 = 0.127
                c_sca_x_1 = 3.082
                c_sca_x_2 = 0.757
                corr_sca_old = 1. + c_sca_m_3 * (m0-c_sca_m_4)* np.sin(c_sca_x_1 * sp) * np.exp(-sp * c_sca_x_2)

                #corr_sca = tm_eff.qs[0]/pm_eff.qs[0]
                raw_qspm = pm_eff.qs[0]/corr_sca_old

                sw={}

                sw['N'] = N
                sw['xm'] = sp
                sw['nr'] = n_real
                sw['ni'] = n_img
                sw['taus_out'] = pm_eff.taus[0]
                sw['taua_out'] = pm_eff.taua[0]
                sw['qa_tm'] = tm_eff.qa[0]
                sw['qs_tm'] = tm_eff.qs[0]
                sw['qa_pm'] = pm_eff.qa[0]
                sw['qs_pm'] = pm_eff.qs[0]
                sw['raw_qspm'] = raw_qspm
#                sw['cs_pm'] = pm_eff.cs[0]
#                sw['cs_tm'] = tm_eff.cs[0]
#                sw['Aproj'] = aprj
#                sw['corr_sca_old'] = corr_sca_old
                sw['corr_sca'] = corr_sca
                sw['m0'] = m0
                dt.append(sw)

Qsca = pd.DataFrame(dt)
Qsca['qs_Rerr'] = (Qsca['qs_tm'] - Qsca['qs_pm'])/Qsca['qs_tm']
Qsca_lt063 = Qsca[Qsca.xm < 0.63]
Qsca_gt063 = Qsca[Qsca.xm >= 0.63]
Qsca_gt047 = Qsca[Qsca.xm >= 0.47]
Qsca_wl = Qsca[(Qsca.xm >= 0.6) & (Qsca.m0 * Qsca.xm > 0.23) ]
#%%
 Resid = Qsca.qs_tm - (Qsca.raw_qspm*Qsca.corr_sca)
 import scipy.stats as stats
 stats.probplot(Resid, dist="norm", plot=plt,rvalue=True, fit=False)
 qq = np.linspace(-4,3)
 plt.plot(qq,qq)
 plt.xlim([-4,3])
 plt.ylim([-4,3])
 plt.show()
 plt.tight_layout()
 #%%
import statsmodels.api as sm
import statsmodels.graphics.gofplots as stg
test = np.random.normal(0,1, 1000)

# sm.qqplot(Resid, line='45')
fig,ax = plt.subplots(figsize=(7,5))
stg.qqplot(Resid,dist='norm', line='r',ax=ax)
ax.set_xlabel('Normal Quantiles',fontsize=17)
ax.set_ylabel('Residual',fontsize=17)
ax.set_title('Normal Probability Plot', fontsize=20)
plt.xlim([-2,2])
plt.ylim([-2,2])
plt.show()
plt.close()
plt.hist(Resid)
plt.xlim([-1.1,1.1])
 #%%
Resid = Qsca.qs_tm - Qsca.qs_pm
fig,ax = plt.subplots(figsize=(8,7))
#qspm=Qsca.raw_qspm*Qsca.corr_sca
qspm=Qsca.qs_pm
ax.scatter(qspm, Qsca.qs_tm)
line=np.linspace(0,15)
ax.plot(line,line)
ax.set_xlabel('$Q_{sca,param.}$', fontsize=26)
ax.set_ylabel('$Q_{sca,t-matrix}$', fontsize=26)
ax.set_title('$T-Matrix\ vs.\ Param.$', fontsize=24)
for item in (ax.get_xticklabels() +ax.get_yticklabels()) :
    item.set_fontsize(14)
ax0 = fig.add_axes([0.18,0.55,0.35,0.35])
ax0.hist(Resid)
ax0.set_xlim([-1.1,1.1])
ax1 = fig.add_axes([0.66,0.22,0.3,0.3])
#stg.qqplot(Resid,dist='norm', line='r',ax=ax1)
stats.probplot(Resid, dist="norm", plot=ax1,rvalue=True, fit=False)
plt.tight_layout()
plt.show()