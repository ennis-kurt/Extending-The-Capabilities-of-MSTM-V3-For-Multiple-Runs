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

import matplotlib.pyplot as plt

#Re-write the functions.
#
#add marker border to separate ni

#%% Code Testing Cell
answer = input('Running the test')

n=256
size_param_dir = glob.glob(dtdir+'{}\\x*'.format(n))
size_param = size_param_dir[0]
xm = size_param[len(dtdir) + len(str(n)) + 2 : size_param.find('\\x')+6]
real_ref_dir = glob.glob(size_param+'\\*')
real_ref = real_ref_dir[0]
nr = real_ref[len(size_param)+1 : ]
img_ref_dir = glob.glob(real_ref+'\\*')
img_ref=img_ref_dir[0]
ni = img_ref[len(real_ref)+1:]


#%%

# List of all xm values
mon_size_par =[ '0168', '0235', '0320', '0336', '0437', '0448',
               '0504', '0640', '0832', '0960' ]

# Functions

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

#    if mon_size == '0168':
#        marker_color = "C0"
#    elif mon_size == '0235':
#        marker_color = "C1"
#    elif mon_size in [ '0320', '0336' ]:
#        marker_color = "C2"
#    elif mon_size in [ '0437', '0448' ]:
#        marker_color = "C3"
#    elif mon_size == '0504':
#        marker_color = "C4"
#    elif mon_size == '0640':
#        marker_color = "C7"
#    elif mon_size == '0832':
#        marker_color = "C8"
#    elif mon_size == '0960':
#        marker_color = "C9"

    if mon_size in ['0168', '0235','0320', '0336']:
        marker_color = 'green'
    elif mon_size in ['0437', '0448', '0504']:
        marker_color = "purple"
    elif mon_size  == '0640':
        marker_color = "blue"
    elif mon_size  == '0832':
        marker_color = "red"
    elif mon_size  == '0960':
        marker_color = "yellow"


    return marker_color

def mark_style(n_real):
    """ This func chooses a marker style based on Real Refractive Index """
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
    """ This func chooses a marker edge color based on Imaginary Refractive Index """
    # Let's convert the string type ni to float

    n_img = float( ".".join(n_img[0:2]) + n_img[2:] )
    if n_img < 0.02:
        m_color2 = 'yellow'
    elif n_img == 0.023:
        m_color2 = 'red'
    elif n_img == 0.045:
        m_color2 = 'blue'
    elif n_img == 0.09:
        m_color2 = 'green'






#%%
sphere_number = [128, 256, 512, 1024]
sphere_number = [1024]

#size_param_dir = ['0168', '0235','0320', '0336', '0640', '0832', '0960']
#ref_ind_real = ['130', '166', '168' '171', '200']
#ref_ind_img = ['0023', '0090', '0045', '0002', '0004','0001']

qa_tm = [];qa_pm = []
qs_tm = [];qs_pm = []
count = 0
for N in sphere_number:
    # size_param_dir = glob.glob(dtdir+'{}\\x*'.format(N))
    for size_param in size_param_dir:
        xm = size_param[len(dtdir) + len(str(N)) + 2 : size_param.find('\\x')+6]
        real_ref_dir = glob.glob(size_param+'\\*')
        for real_ref in real_ref_dir:
             nr = real_ref[len(size_param)+1 : ]
             img_ref_dir = glob.glob(real_ref+'\\*')
             for img_ref in img_ref_dir:
                 ni = img_ref[len(real_ref)+1:]

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
                     continue
 #                plt.plot(np.log(tm1024_0640_130_0023_mx['P11'].values))


plt.show()
plt.close()

plt.scatter(qa_pm,qa_tm)
plt.plot(np.linspace(0,1.5),np.linspace(0,1.5), color="C0")
plt.show()
plt.close()

plt.scatter(qs_pm,qs_tm,marker = '.')
plt.plot(np.linspace(0,11),np.linspace(0,11), color="C1")
plt.show()
plt.close()

print('count %d'%count)

#%%

sphere_number = [1024]
alpha_value = 1.0
for N in sphere_number:
    size_param_dir = glob.glob(dtdir+'{}\\x*'.format(N))
    for size_param in size_param_dir:
        xm = size_param[len(dtdir) + len(str(N)) + 2 : size_param.find('\\x')+6]
        real_ref_dir = glob.glob(size_param+'\\*')
        for real_ref in real_ref_dir:
             nr = real_ref[len(size_param)+1 : ]
             img_ref_dir = glob.glob(real_ref+'\\*')
             for img_ref in img_ref_dir:
                 ni = img_ref[len(real_ref)+1:]

                 try:
                     missing = 't-matrix'
                     tm = vars()['tm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                     missing = ' f-fasm'
                     param = vars()['param{}_{}_{}_{}_eff'.format(N, xm, nr, ni)]

                     if tm.qa.values < 1e3 and tm.qa.values > -1e3:


                         # Choosing the style based on the parameter values
                         m_size = mark_size(N)
                         m_col = mark_color (xm)
                         m_st = mark_style(nr)
                         m_col2 = mark_edge_color (ni)


                         plt.plot(param.qs.values,tm.qs.values,marker=m_st,\
                                  markersize=m_size + 10, color=m_col2, alpha = 1)#,\
                                  #markeredgecolor='red', markeredgewidth = N/160)

                         plt.plot(param.qs.values,tm.qs.values,marker=m_st,\
                                  markersize=m_size, color=m_col, alpha = 1)#,\
                                 # markeredgecolor='red', markeredgewidth = N/160)



                 except KeyError:
                     print('missing run {} {}_{}_{}_{}_eff'.format(missing, N, xm, nr, ni))
                     continue
                 plt.plot(np.linspace(0,11),np.linspace(0,11), color='purple', linestyle="-.", alpha = 0.1)
