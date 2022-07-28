#!/bin/bash

set -e

if [ $PWD != /home/ucnk/Dropbox/Dropbox/matlab_plots_and_data/mstmoutputs/special/main ]; then
cd main; 
else 
echo " "; 
fi

# Writing the codes to import t-matrix data in to fullretrieve.m
./tmdata.sh

# Writing the codes to import parameterization data in to fullretrieve.m and paramimport.m

./paramdata.sh
