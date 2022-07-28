# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 19:23:00 2018

@author: kurt_
"""

import numpy as np
import pandas as pd
import linecache as gl
import glob
import os
import platform
op_sys = platform.system()
if op_sys == 'Windows':
    dtdir = 'C:\\Users\\kurt_\\Google Drive\\dell_github\\T-Matrix-Titan\\special\\data\\output\\'
    _sl = '\\'
elif op_sys == 'Linux':
    dtdir = '/home/cihat/Dropbox/code/special/data/'
    _sl = '/'
os.chdir(dtdir)

###### The structure of this code is summarized here  #######
# 1. N=[256,512,1024]; xm=[0.336,0.64]; nr=[1.3,1.71,2.0]; ni=[0.0226,0.09]
# 2. for N, for xm, for nr, for ni:
# 3. Only process the runs which have 10 or more runs.Also check the file size.

####################### To Do list ######################
# 1) I already wrote the bash code to check the file size. Use this code to
# remove the incomplete runs. they have no use at all.

# update 1) I did this here in this code. It was simplier. It is commented now.


# dtdir=r'C:\Users\kurt_\Google Drive\Code\special\data\1024\x6398\171\00226'
# Notice the r before the string. It tells the pyhton read the string as raw,
# so that do nothing just read when there is \ in the text
# other option to read \ as is: using \\. For eg. C:\\Users\\kurt_

# %%

old_tm_files = glob.glob(
    'C:\\Users\\kurt_\\Google Drive\\Code\\special\\data\\old_tm_data\\*.dat')

# Lets create an array to record some log info which not need to be prompted
# during the execution. These log info could be used for debugging but they
# would be too unimportant to record in a file.
_log = []
# Directories organised as, 1024/x3360/166/0002/mt_1_1024_x3360_166_0002.dat

sphere_number = [64, 128, 256, 512, 1024]
# ref_ind_real = [130, 145, 166, 168, 171, 185, 200, 230]
# ref_ind_img = ['00226', '00900', '00450', '00020', '00010', '00060', '03000', '00044']
# %%
tm_all_mx = []
tm_all_eff = []
count = 0
for N in sphere_number:
    size_param_dir = glob.glob(dtdir+'{}{}x*'.format(N, _sl))
    print(size_param_dir)
    for size_param in size_param_dir:
        xm = size_param[len(dtdir) + len(str(N)) +
                        2: size_param.find('{}x'.format(_sl))+7]
        # this extract only this part '3360'

        real_ref_dir = glob.glob(size_param+'{}*'.format(_sl))
        for real_ref in real_ref_dir:
            nr = real_ref[len(size_param)+1:]

            # We need to skip the loop if there is no data for this nr.
            try:
                qs = glob.glob(size_param+'{}{}'.format(_sl, nr))
                # if There is No Such File (TNSF) qs=[] --> len(qs) =0
                qs[0]  # If TNSF this will give IndexError
            except IndexError:
                _log.append(['There is no data for this set:  {}_{}_{}'
                             .format(N, size_param, nr)])
                continue

            img_ref_dir = glob.glob(real_ref+'{}*'.format(_sl))
            for img_ref in img_ref_dir:

                ni = img_ref[len(real_ref)+1:]

                # We need to skip the loop if there is no data for this ni.
                try:
                    qs = glob.glob(
                        size_param+'{}{}{}'.format(_sl, nr, _sl) + ni)
                    qs[0]
                except IndexError:
                    _log.append(['There is no data for this set:  {}_{}_{}_'
                                 .format(N, xm, nr) + ni])
                    continue

                tmatrix_files = glob.glob(qs[0]+'{}mt*.dat'.format(_sl))

                # Skipping runs if there are not atleast 10 outputs available.

                if len(tmatrix_files) < 5 and len(tmatrix_files) > 0:

                    print('There are {} outputs for the run {}_{}_{}_'
                          .format(len(tmatrix_files), N, xm, nr) + ni)
                    print('For the sake of accuracy this run will not be included ')
                    continue
                elif len(tmatrix_files) == 0:
                    print('There is NO outputs for the run {}_{}_{}_'
                          .format(N, xm, nr) + ni)
                    continue
                # print('There are {} output files for the run {}_{}_{}_'
                 #     .format(len(tmatrix_files), N, xm, nr) + ni)
                i = 0
                df_mx = []
                df_eff_concat = []
                for tmf in tmatrix_files:

                    # Warning! here i, run number, may not be equal to run
                    # number which appear in the name of the file. Such as
                    # mt1024_x6398_13_009_1 may be referred with i different than 1.

                    ## Skip Incomplete output files ##
                    file_size = os.path.getsize(tmf)

                    if file_size < 2000:
                        continue

                    i += 1

                    # Let's read the mstm output files and save the data into
                    # a pd.DataFrame
                    # Outside this loop, I will calculate the ensemble average.

                    # Let's first collect the efficiencies and asymmetry parm.

                    q = gl.getline(tmf, 51)
                    q = q.split()
                    qext = [float(q[0])]
                    qabs = [float(q[1])]
                    qsca = [float(q[2])]
                    g = [float(q[3])]

                    # A few runs seems like have wrong qe and/or qa values.
                    # I did not investigate the scattering matrix but I will
                    # completely skip all these runs.

                    if (qsca[0] < 1e3 and qsca[0] > -1e3) and (qabs[0] < 1e3 and qabs[0] > -1e3)\
                            and (g[0] >= 0 and g[0] <= 1):

                        eff = {'qa': qabs, 'qs': qsca, 'qe': qext, 'g': g}
                        dt_eff = pd.DataFrame(eff)
                        dt_eff = dt_eff.apply(pd.to_numeric)
                        df_eff_concat.append(dt_eff)

                        data = []

                        for line in range(54, 235):
                            a = gl.getline(tmf, line)
                            columns = a.split()
                            rw = {}
                            rw['theta'] = columns[0]
                            rw['P11'] = columns[1]
                            rw['P12'] = columns[2]
                            rw['P13'] = columns[3]
                            rw['P14'] = columns[4]
                            rw['P22'] = columns[5]
                            rw['P23'] = columns[6]
                            rw['P24'] = columns[7]
                            rw['P33'] = columns[8]
                            rw['P34'] = columns[9]
                            rw['P44'] = columns[10]
                            data.append(rw)

                        # Dataframe for each run with a name, e.g., tm1024_x3360_171_009_1
                        dt_mx = pd.DataFrame(data)

                        # Let's convert the string values to numeric all at once
                        dt_mx = dt_mx.apply(pd.to_numeric)

                        # Now lets collect all the dataframes to get an average at the end.

                        df_mx.append(dt_mx)
                    else:
                        continue

                    # Now let's average the all runs for the same input parameters
                    # df_concat stack all the datframes vertically.
                    # indexes, 1 to 180, repeats for each output
                    # To calculate the mean we just need to group the
                    # df_concat by the index.
                    # then we can simply take the mean.

                    # Let's convert the df_concat to a pandas dataframe
                    df_mx_concat = pd.concat(df_mx)
                    df_eff = pd.concat(df_eff_concat)

                    # Let's take the average of all runs for each set

                    # Averaging Scattering matrices
                    group_by_index_mx = df_mx_concat.groupby(
                        df_mx_concat.index)
                    tm_run_mx = 'tm{}_{}_{}_{}_mx'.format(N, xm, nr, ni)
                    vars()[tm_run_mx] = group_by_index_mx.mean()
                    # For eg. 1024_x6398_13_009_mx
                    tm_all_mx.append(vars()[tm_run_mx])

                    # Averaging Efficiencies and asym. par.
                    group_by_index_eff = df_eff.groupby(
                        df_eff.index)
                    tm_run_eff = 'tm{}_{}_{}_{}_eff'.format(N, xm, nr, ni)
                    vars()[tm_run_eff] = group_by_index_eff.mean()
                    tm_all_eff.append(vars()[tm_run_eff])
                count += 1


# %%
# Now Collecting The Old Data ( Dr. Lemmon's work )
# All these runs already averaged. Importing them is thus similar to importing parameterization data.

# Substitutions
# file = old_tm_files; par = tm_old; param_run = tm_old_run

# Let's store each parameters in an array. They will be added to parameters choosen in main script (plot.py)
old_xm = []
old_nr = []
old_ni = []

sphere_number = [64, 128, 256, 512]
count_old = 0
#old_switch = input('Do you need to include OLD TMATRIX RUNS \nPlease type "y" or "n" ')
old_switch = "n"
if old_switch == "y":
    for tm_old in old_tm_files:
        # grabbing the run id from the name of the file from tm to .dat not including the end
        tm_old_run = tm_old[tm_old.find(
            '{}tm'.format(_sl))+1:tm_old.find('.dat')]
        # Now tm_old_run = 'tm8_35000_175_02000' let's get the each parameter from this, and store
        # this exracts size param
        old_xm.append(tm_old_run[tm_old_run.find(
            '_')+1:tm_old_run.find('_')+6])
        old_nr.append(tm_old_run[tm_old_run.find(
            '_')+7:tm_old_run.find('_')+10])
        old_ni.append(tm_old_run[tm_old_run.find('_')+11:])

        q = gl.getline(tm_old, 2)
        q = q.split()
        qabs = [float(q[0])]
        qsca = [float(q[1])]
        qext = [float(q[2])]
        eff = {'qa': qabs, 'qs': qsca, 'qe': qext}
        vars()[tm_old_run+'_eff'] = pd.DataFrame(eff)

        # Now let's collect the scattering matrix in a data frame
        data = []
        for line in range(4, 185):
            a = gl.getline(tm_old, line)
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
        vars()[tm_old_run+'_mx'] = dt.apply(pd.to_numeric)
        vars()[tm_old_run+'_mx']['theta'] = np.arange(0, 181)
        count_old += 1

        # For now I will not convert the data to xarray. I do not see any benefit from
        # doing that other than being able to collect matrix elements and efficien-
        # ies in the same dataset. Hence, below code block is commented

    #    # Now collecting everything in an xarray dataset
    #    # Note that PXX are saved as variable, but Qx and g are saved as dimension
    #    vars()[param_run] = xr.Dataset.from_dataframe(dt)
    #    vars()[param_run]['qext'] = qext
    #    vars()[param_run]['qabs'] = qabs
    #    vars()[param_run]['qsca'] = qsca
    #    vars()[param_run]['g'] = g


print('Please read _log to see missing data')
