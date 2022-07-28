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
dtdir = 'C:\\Users\\kurt_\\Google Drive\\Code\\special\\data\\'
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
    if sphere_num == 1024:
        marker_size = 36
    elif sphere_num ==512:
        marker_size = 24
    elif sphere_num ==256:
        marker_size = 15
    elif sphere_num ==128:
        marker_size = 8
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
    return m_color2

def linearize(data, lp, sec_lin = False):
    # This function linearize the m0. The linerization functions has to be modified each time.
    if lp == 1:
        print('a1=1; b1=0.85; a2=0.73; b2 = 18')
        k1=1; l1=0.73; k2=0.85; l2 = 18
        #k1 = 1.17; l1 = 0.92; k2 = 160; l2 = 200

    elif lp == 2:
        print('a1 = 1.17; a2 = 0.92; b1 = 160; b2 = 200')
        k1 = 1.17; l1 = 0.92; k2 = 160; l2 = 200

    elif lp == 3:
        print( 'a1 = 1.38; a2 = 0.38; b1 = 170; b2 = 80' )
        k1 = 1.38; l1 = 0.38; k2 = 170; l2 = 80

    elif lp == 4:
        print('a1 = 1.95; a2 = 0.66; b1 = 170; b2 = 80')
        k1 = 1.95; l1 = 0.66; k2 = 170; l2 = 80


    if lp == 1:
        e = -2*1.7218

    else:
        e = 2


    data['m0'] = (abs(((k1*data.nr + np.log10(k2*data.ni)*1j)**2 -1)/((l1*data.nr + np.log10(l2*data.ni)*1j)**2 + 2)))**e
    if sec_lin:
        # this needs to be modified. It is the best fit of LPi against m0. fit function obtained from matlab. Needs to be modified for each LPi
        # Incase of LP4 both linear sinisoidal function and 1st degre pol. regression fit well. Thus 2nd linearization may not be necessary
        data.m0 = (-1.605e-09)*(np.sin(data.m0/2 -0.7*np.pi))+2.237e-09*((data.m0 + 1))
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
                     param = vars()['param{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                     if tm.qa.values < 1e3 and tm.qa.values > -1e3:


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



                 except KeyError:
                     print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                     _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                     continue
 #                plt.plot(np.log10(tm1024_06398_130_00226_mx['P11'].values))


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
                     param = vars()['param{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                     if tm.qs.values < 1e3 and tm.qs.values > -1e3:


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



                 except KeyError:
                     #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                     _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                     continue
                 plt.plot(np.linspace(0,11),np.linspace(0,11), color='purple', linestyle="-.", alpha = 0.1)


#%%
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

alpha_value = 1.0
_log = []
theta=np.arange(0,181)
x = theta[65:]
dt=[] # to be used to write Legend. Pol. coefficients data
for N in sphere_number:

    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                try:
                    missing = 't-matrix'
                    tm = vars()['tm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                    missing = ' f-fasm'
                    param = vars()['param{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                except KeyError:
                    print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)
                tm =  vars()['tm'+runid+'_mx']
                pm = vars()['param'+runid+'_mx']
                p22_err = (tm.P22*tm.P11 - pm.P22)[65:]

                # Now the correction
                # First fit the error function with a 3rd Degree Legendre Polynomial

                coeffs = np.polynomial.legendre.legfit(x, p22_err, deg=3)

                rsq = 1- np.polynomial.legendre.legfit(x, p22_err, deg=3,full = True)[1][0][0]

                # Keeping ceofficients in a Dataframe
                sp = float(".".join(xm[0:2]) + xm[2:])
                n_real = float(".".join(nr[0:2]) + nr[2:])
                n_img = float(".".join(ni[0:2]) + ni[2:])
                sw={}
                sw['Ns'] = N
                sw['sp'] = sp
                sw['nr'] = n_real
                sw['ni'] = n_img
                sw['p1'] = coeffs[0]
                sw['p2'] = coeffs[1]
                sw['p3'] = coeffs[2]
                sw['p4'] = coeffs[3]
                sw['r_sqr'] = rsq
                dt.append(sw)


                # Shoul you need the plots, edit the "if" below

                plotting = "no"
                if plotting == "yes":
                    # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix
                    p22_corr = pd.Series(np.polynomial.legendre.legval(x, coeffs), index=x)
                    new_pm = pm.copy()
                    new_pm.P22 = pm.P22.add(p22_corr, fill_value=0)
                    fig, ax = plt.subplots(ncols=3,figsize=(12,6))

                    ax[0].plot(np.log10(new_pm.P22), '.', label = 'new_pm')
                    ax[0].plot(np.log10(tm.P22*tm.P11), '.', label = 'tm')
                    ax[0].set_title('New P22'+runid)
                    ax[0].legend()

                    # Old fit
                    ax[1].plot(np.log10(pm.P22), '.', label = 'old_pm')
                    ax[1].plot(np.log10(tm.P22*tm.P11), '.', label = 'tm')
                    ax[1].legend()
                    ax[1].set_title('Old P22'+runid)

                    # Error Function and the Fit
                    ax[2].plot(x, p22_err, '.', label = 'p22_err')
                    ax[2].plot(x, p22_corr,'.', label = 'p22_corr' )
                    ax[2].legend()
                    ax[2].set_title('p22 error & the fit')
                    plt.tight_layout()
                    plt.show()


LP_Coeff = pd.DataFrame(dt)
linearize(LP_Coeff,1)
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



# for p1 =  data['m0'] = (abs(((a1*data.nr + np.log10(b1*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b2*data.ni)*1j)**2 + 2)))**-1.7218 a1=1, b1=0.85,a2=0.73, b2 = 18 This behave perfectly linear. Hence no need to find a fit against p1.
# for p1 = data['m0'] = (abs(((0.82*data.nr + np.log10(data.ni)*1j)**2 -1)/((0.82*data.nr + 1.95*np.log10(data.ni)*1j)+2)))**2  ADJ R^2 = 8997


# for p2 data['m0'] = (abs(((a1*data.nr + np.log10(b1*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b2*data.ni)*1j)**2 + 2)))**2 with a1 = 1.17, a2 = 0.92, b1=160, b2 = 200
# The best fit is either Poly 2 or linear a*(sin(x/4 -pi*1.15))+b*((x+1))+c*(1) with R^2 0.8289


# FOR P3 Uncorrected M0
# for p3 -> data['m0'] = (abs(((a1*data.nr + np.log10(b*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b*data.ni)*1j)+2)))**2 with a = 1.215, a2 = 2.2, b1 = 138, b2 = 50
# for p3 Linear fitting with this function: a*sin(x/2 -0.4*pi)+b*((x + 1))+c*(1) or polynomial 2nd degree. Both good, former better. R^2 = 0.8362 for linear
# Corrected M0
# data['m0'] = (abs(((a1*data.nr + np.log10(b1*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b2*data.ni)*1j)**2 + 2)))**2 with a1 = 1.38, a2 = 0.38, b1 = 170, b2 = 80
# linear fit is the best with a*(sin(x/2 -0.5*pi))+b*((x +1))+c*(1) R^2 = 0.827

# For p4  -> data['m0'] = (abs(((a1*data.nr + np.log10(b1*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b2*data.ni)*1j)+2)))**2 with a1 = 1.65, a2 = 2.6, b1 = 130, b2 = 65
# fit with linear function a*(sin(x-pi*1.3))+b*((x+1))+c*(1) R^2 = 0.8588
# For p4 with corrected M0
# data['m0'] = (abs(((a1*data.nr + np.log10(b1*data.ni)*1j)**2 -1)/((a2*data.nr + np.log10(b2*data.ni)*1j)**2 + 2)))**2 with a1=1.95, a2 = 0.66, b1=170, b2 = 80
# linear fit is far the best a*(sin(x/2 -0.7*pi))+b*((x + 1))+c*(1) with R^2 = 0.8686. Not only in terms of R^2 but also it is much more stable and makes sense above the range



columns_to_keep = ['Ns','sp','nr','ni', 'm0','p1','p2','p3','p4']
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
aa = pd.concat(dt)
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
def old_run_pm ()
alpha_value = 1.0
_log = []
theta=np.arange(0,181)

bound0 = 75
bound1 = 180

x = theta[bound0:bound1]

for N in sphere_number:

    for xm in size_param:

        for nr in real_ref:

            for ni in img_ref:

                try:
                    missing = 't-matrix'
                    tm = vars()['tm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                    missing = ' f-fasm'
                    param = vars()['param{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                except KeyError:
                    #print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    _log.append('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                    continue

                runid = '{}_{}_{}_{}'.format(N, xm, nr, ni)
                tm =  vars()['tm'+runid+'_mx']
                pm = vars()['param'+runid+'_mx']
                P11_err = (tm.P11 - pm.P11)[bound0:bound1]

                # Now the correction
                # First fit the error function with a 3rd Degree Legendre Polynomial


                z = np.polynomial.legendre.Legendre.fit(x, P11_err, deg=3)
                # Now Let's Correct the parametrization and plot the new and old comparison with tmatrix

                P11_corr = pd.Series(z(x), index=x)
                new_pm = pm.copy()
                new_pm.P11 = pm.P11.add(P11_corr, fill_value=0)
                fig, ax = plt.subplots(ncols=3,figsize=(22,6))

                ax[0].plot(np.log10(new_pm.P11[bound0:bound1]), '.', label = 'new_pm')
                ax[0].plot(np.log10(tm.P11[bound0:bound1]), '.', label = 'tm')
                ax[0].set_title('New P11'+runid)
                ax[0].legend()

                # Old fit
                ax[1].plot(np.log10(pm.P11[bound0:bound1]), '.', label = 'old_pm')
                ax[1].plot(np.log10(tm.P11[bound0:bound1]), '.', label = 'tm')
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

#%%
#%% Code Testing Cell
#answer = input('Running the test')

print((-param512_06398_200_00900_mx.P12/param512_06398_200_00900_mx.P11).idxmax())
print((-tm256_06398_200_00900_mx.P12).idxmax())
plt.plot(-param512_06398_200_00900_mx.P12/param512_06398_200_00900_mx.P11)
plt.plot(-tm512_06398_200_00900_mx.P12)
plt.plot(((-param512_06398_200_00900_mx.P12/param512_06398_200_00900_mx.P11) + tm512_06398_200_00900_mx.P12)*10 )
plt.legend('PT')

#%%
plt.plot(((-param512_06398_200_00900_mx.P12/param512_06398_200_00900_mx.P11) + tm512_06398_200_00900_mx.P12)*10 )
plt.plot(((-param1024_06398_200_00900_mx.P12/param1024_06398_200_00900_mx.P11) + tm1024_06398_200_00900_mx.P12)*10 )
plt.legend('512','1024')

#%%
plt.plot(param128_06398_200_00900_mx.P22/param128_06398_200_00900_mx.P11)
plt.plot(param256_06398_200_00900_mx.P22/param256_06398_200_00900_mx.P11)
plt.plot(param512_06398_200_00900_mx.P22/param512_06398_200_00900_mx.P11)
plt.plot(param1024_06398_200_00900_mx.P22/param1024_06398_200_00900_mx.P11)
plt.legend(['N128','N256','N512','N1024'])

#%%
plt.plot(np.log10(tm128_06398_200_00900_mx.P22*tm128_06398_200_00900_mx.P11), linewidth = 5, alpha=0.3)
plt.plot(np.log10(tm256_06398_200_00900_mx.P22*tm256_06398_200_00900_mx.P11), linewidth = 5, alpha=0.3)
plt.plot(np.log10(tm512_06398_200_00900_mx.P22*tm512_06398_200_00900_mx.P11), linewidth = 5, alpha=0.3)
plt.plot(np.log10(tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11), linewidth = 5, alpha=0.3)

plt.plot(np.log10(param128_06398_200_00900_mx.P22), '-.')
plt.plot(np.log10(param256_06398_200_00900_mx.P22), '-.')
plt.plot(np.log10(param512_06398_200_00900_mx.P22), '-.')
plt.plot(np.log10(param1024_06398_200_00900_mx.P22), '-.')

plt.legend(['N128','N256','N512','N1024'])
#%%
plt.plot(np.log10(tm128_06398_200_00226_mx.P22*tm128_06398_200_00226_mx.P11), linewidth = 5, alpha=0.5)
#plt.plot(np.log10(tm256_06398_200_00226_mx.P22*tm256_06398_200_00226_mx.P11), linewidth = 5, alpha=0.3)
#plt.plot(np.log10(tm512_06398_200_00226_mx.P22*tm512_06398_200_00226_mx.P11), linewidth = 5, alpha=0.3)
plt.plot(np.log10(tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11), linewidth = 5, alpha=0.5)
#
#plt.plot(np.log10(param128_06398_200_00226_mx.P22), '-.')
##plt.plot(np.log10(param256_06398_200_00226_mx.P22), '-.')
##plt.plot(np.log10(param512_06398_200_00226_mx.P22), '-.')
#plt.plot(np.log10(param1024_06398_200_00226_mx.P22), '-.')

plt.plot(np.log10(tm128_06398_200_00900_mx.P22*tm128_06398_200_00900_mx.P11), linewidth = 5, alpha=0.5)
plt.plot(np.log10(tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11), linewidth = 5, alpha=0.5)

#plt.plot(np.log10(param128_06398_200_00900_mx.P22), '-')
#plt.plot(np.log10(param1024_06398_200_00900_mx.P22), '-')

#plt.legend(['N128','N256','N512','N1024'])

#%%
plt.plot(np.log(tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11 - param1024_06398_130_00226_mx.P22), linewidth = 2, alpha=0.5, color='k')
plt.plot(np.log(tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11))
plt.plot(np.log(param1024_06398_130_00226_mx.P22))
plt.legend(['error', 'tm','param'])


#%%%
#Only p22 errors
plt.plot((tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11[0:] - param1024_06398_130_00226_mx.P22[0:])/(tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11[0:]), linewidth = 2, alpha=0.5, linestyle= '-.')
plt.plot((tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11[0:] - param1024_06398_200_00226_mx.P22[0:])/(tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11[0:]), linewidth = 2, alpha=0.5,linestyle='-')

plt.plot((tm1024_06398_130_00900_mx.P22*tm1024_06398_130_00900_mx.P11[0:] - param1024_06398_130_00900_mx.P22[0:])/(tm1024_06398_130_00900_mx.P22*tm1024_06398_130_00900_mx.P11[0:]), linewidth = 2, alpha=0.5, linestyle= '-.')
plt.plot((tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11[0:] - param1024_06398_200_00900_mx.P22[0:])/(tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11[0:]), linewidth = 2, alpha=0.5,linestyle='-')

plt.title(' P22 Relative error')
plt.legend(['1.3 & 0.023','2.0  & 0.023', '1.3 & 0.090','2.0  & 0.090'])

#%%
# Absolute error P22
plt.plot((tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11[25:] - param1024_06398_130_00226_mx.P22[25:]), linewidth = 2, alpha=0.5, linestyle= '-.')
plt.plot((tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11[25:] - param1024_06398_200_00226_mx.P22[25:]), linewidth = 2, alpha=0.5,linestyle='-')

plt.plot((tm1024_06398_130_00900_mx.P22*tm1024_06398_130_00900_mx.P11[25:] - param1024_06398_130_00900_mx.P22[25:]), linewidth = 2, alpha=0.5, linestyle= '-.')
plt.plot((tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11[25:] - param1024_06398_200_00900_mx.P22[25:]), linewidth = 2, alpha=0.5,linestyle='-')


##plt.plot(tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11[25:], linestyle = ':', linewidth=4)
#plt.plot((tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11[25:]), linestyle = ':', linewidth=4)
#
##plt.plot(param1024_06398_130_00226_mx.P22[25:], linestyle = (0, (3, 1, 1, 1, 1, 1)), linewidth=4)
#plt.plot((param1024_06398_200_00226_mx.P22[25:]), linestyle = (0, (3, 1, 1, 1, 1, 1)), linewidth=4)


plt.title('P22 Absolute Error')
plt.legend(['1.3 & 0.023','2.0  & 0.023', '1.3 & 0.090','2.0  & 0.090'])

#%%

# Errors Here

p2210246413023err = tm1024_06398_130_00226_mx.P22*tm1024_06398_130_00226_mx.P11 - param1024_06398_130_00226_mx.P22
p2210246413009 = tm1024_06398_130_00900_mx.P22*tm1024_06398_130_00900_mx.P11[0:] - param1024_06398_130_00900_mx.P22[0:]
p22102464200226err = tm1024_06398_200_00226_mx.P22*tm1024_06398_200_00226_mx.P11[0:] - param1024_06398_200_00226_mx.P22[0:]
p221024642009 = tm1024_06398_200_00900_mx.P22*tm1024_06398_200_00900_mx.P11 - param1024_06398_200_00900_mx.P22

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
