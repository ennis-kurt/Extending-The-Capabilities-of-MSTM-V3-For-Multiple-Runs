# Automated Multi-Run Execution of the Multi Sphere T-Matrix (MSTM-v3) Code
## Overview 

This repository contains the output files of hundreds of Multi Sphere T-Matrix (MSTM-v3) runs. The purpose of these runs is to calculate the properties of the haze particles in Titan's atmosphere. Therefore, the parameters of the runs are selected within the current estimates of the Titan's haze particle properties.

MSTM is a FORTRAN-90 code for calculating the time-harmonic electromagnetic scattering properties of a group of spheres. The algorithm applies the multiple sphere matrix method, and the results can be considered exact to the truncation error of the vector spherical wave function (VSWF) expansions used to represent the fields.

## Comprehensive Bash Script

Included in this repository is a comprehensive bash script for running, pre-processing, and post-processing the input and output of a series of T-Matrix codes on multiple CPU cores efficiently without exhausting memory. Under the main folder, there are several bash scripts to pre-process the input files, execute the MSTM codes on multiple CPU cores, and post-process the output files.

## Limitations of the original MSTM code

The MSTM code already has multiple runs and parallel processing capabilities. However, these features are limited. To improve upon this, I have written a bash script (ensemble_run.sh and its variants) to automate the execution of multiple MSTM runs using multiple CPU cores serially. The original MSTM code can perform a single run with parallel processing, but when multiple runs are required, its parallel processing is less efficient than executing each run on a single CPU core. Additionally, during the calculation of phase metrics, the t-matrix is stored in memory, and if a run is executed on multiple cores using parallel processing, a copy of the t-matrix run is stored for each core, which can easily exhaust memory, especially when run on a personal computer. When only a limited number of runs are needed, parallel processing is still beneficial. However, when tens of multiple runs are needed, dedicating each CPU core to a single run simultaneously while using multiple cores is much more efficient in terms of both run time and memory usage. The ensemble_run.sh script handles this automatically, along with other features.

Another issue with the MSTM code when it comes to multiple runs is that the original code provides only a limited way to select run parameters. The ensemble_run script extends its multiple run features. For example, you can tell the computer to execute several hundred runs by selecting a range of values for each parameter and the number of cores to be used for the calculations. The ensemble_run.sh script will create a number of scripts (the same number as the selected CPU cores) to be executed on a single core. The scripts created by ensemble_run.sh ensure that there will never be more than one run being executed by any processor. Alternatively, you can give a range of values for each parameter and let the computer randomly select the values of the parameters within the range provided. Currently, the random values are selected from a uniform distribution of parameter values, but in the future, I plan to add the option to select the values from Gaussian distributions.

## Note

Please note that this repository is still under development. Most of these codes were developed during a project to retrieve the properties of Titan's haze particle without the intention of publishing the code to the public.
