# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 20:23:42 2018

@author: kurt_
"""
from import_tm import *
from par_import import *
import matplotlib.pyplot as plt
#import_tm
#par_import

#%%  Functions

def mark_size(sphere_num):
    """ This func chooses a markszie based on sphere number """
    if sphere_num == '1024':
        m_size = 12
    elif sphere_num =='512':
        m_size = 9
    elif sphere_num =='256':
        m_size = 6
    elif sphere_num =='128':
        m_size = 4
    return m_size

def mark_color(mon_size):
    """ This func chooses a marker color based on Monomer Size parameter """
    # Let's convert the mon_size to float by adding "." after the first "0"

    mon_size = float( ".".join(mon_size[0:2]) + mon_size[2:] )

    # Now choose a color using a color scheme module
    colorselect = plt.cm.gist_ncar #nipy_spectral, Set1,Paired
    m_color = colorselect(mon_size)

    """Note that some xm values very close to each other"""
    """ If this causes confusion in color scheme then extend the distance between each xm values"""
    """ Also, by choosing a color randomly costs not being able to create custon legend easily"""

    return m_color

def




#%%
sphere_number = ['128', '256', '512', '1024']
sphere_number = ['1024']
size_param = ['0336', '0640']
ref_ind_real = ['130', '166', '171', '200']
ref_ind_img = ['0023', '0090', '0045', '0002']

for n in sphere_number:
    for xm in size_param:
         for nr in ref_ind_real:
             for ni in ref_ind_img:

                 try:
                     tm = vars()['tm{}_{}_{}_{}_eff'.format(n, xm, nr, ni)]
                     param = vars()['param{}_{}_{}_{}_eff'.format(n, xm, nr, ni)]

                     if tm.qa.values > 1e3 or tm.qa.values < -1e3:
                         continue
                     print(param.qa,tm.qa)

                     plt.plot(param.qa.values,tm.qa.values,marker='o', markersize=3, color="red")

                     plt.plot(param.qs.values,tm.qs.values,marker='o', markersize=3, color="red")
                 except KeyError:
                    #print('{}_{}_{}_{}_eff'.format(n, xm, nr, ni))
                    continue
 #                plt.plot(np.log(tm1024_0640_130_0023_mx['P11'].values))
