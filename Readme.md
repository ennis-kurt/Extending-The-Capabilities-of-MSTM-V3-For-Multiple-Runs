# T-Matrix-Titan
This repository contains the output files of hundreds of Multi Sphere T-Matrix (MSTM-v3) runs. The purpose of these runs is to calculate the properties of the haze particle in Titan's Atmosphere. Therefore, the parameters of the runs are selected within the current estimates of the Titan's haze particle properties 

MSTM is a FORTRAN-90 code for calculating the time–harmonic electromagnetic scattering properties of a group of spheres. The algorithm applies the multiple sphere  matrix method, and the results can be considered exact to the truncation error of the vector spherical wave function (VSWF) expansions used to represent the fields.

A Comprehensive Bash Script To run, pre & post-processing of i/o of a series of T-Matrix codes on serial multiple cpus efficiently without exhausting Memory

Under the Main folder there are several bash scripts to pre-process the input files, execute the MSTM codes on multiple cpu cores and post-process the output files.

The MSTM code already have multiple runs and parallel processing capability. However, these features are limited. 
Here, I wrote a bash script ( esnsemble_run.sh and its other versions) to automate the multiple MSTM run executions using multiple cpu-cores serially. Original MSTM code can execute a single run with parallel processing, but when several multiple runs needed then its parallel processing is much less efficient than executing each run on a single cpu core. In addition to this, during the calculation of phase metrices, t-matrix is stored to memory and if the run is executed on multiple core using parallel processing for each cpu a copy of t-matrix run is stored on memory. This can easily exhaust memory especially if run on a personal computer. If only a limited number of runs needed then parallel processing is still benefitial. 

However, when tens of multiple runs are needed dedicated each cpu core to a single run at the same time while using multiple cores is much more efficient in terms of both run time and memory usage. The ensemble_run.sh script does this automatically, along with other things. 

Another issue with MSTM code when it comes to multiple runs is that the original code provides only a limited way to select the run paramaters. ensemble_run script extends its multiple run features. 

For instance, one can tell the computer to execute several hundreds of runs by selecting a range of values for each parameters and the number of cores to be used for the calculations. The ensemble_run.sh will create a number scripts (same number as the selected cpu cores) to be executed on a single core. The scipts created by ensemble_run.sh make sure that there will never be more than one run being executed by any processor. 

Alternatively one can give a range of values for each parameter and let the computer radnomly select the values of the parameters within the range provided. Currently the random values are selected from uniform distribution of parameter values, but in the future I will add the option to select teh values from gaussian distributions.

This reporistory is still under development. Most of these codes were developed during a project to retrive the properties of Titan's haze particle without having the publisihing the code to public in mind. 
