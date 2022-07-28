# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:25:22 2022

@author: kurt_
"""
# %%
# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %%

import os
import platform
op_sys = platform.system()
if op_sys == 'Windows':
    path = 'C:\\Users\\kurt_\\Google Drive\\dell_github\\T-Matrix-Titan\\special\\data\\'

elif op_sys == 'Linux':
    path = '/home/cihat/Dropbox/code/special/data/'
os.chdir(path)
# %%
# Reading the coefficients data
df = pd.read_csv(path+'coefficients\\forward\\allregimes.csv')
# print(df.head())
df.plot(x='p2', y='p3', kind='scatter')
# Coefficients depend on each other as expected, not not strongly though.
# Above plotting shows that.
# If synthetic data will be created we should create p1,p2,p3 all together.
# let's plot pairwise correlation heatmap
f, ax = plt.subplots(figsize=(14, 10))
ax = sns.heatmap(df.corr(), annot=True, cmap='PuOr')
plt.show()
