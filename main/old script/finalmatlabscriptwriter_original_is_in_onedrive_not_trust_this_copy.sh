#!/bin/bash

echo " %Matlab Script to FullRetrieve all the Data" > FullRetrieve.m
echo " addpath(genpath('/home/ucnk/Dropbox/Dropbox/matlab_plots_and_data/mstmoutputs/special'))" >>FullRetrieve.m
echo " Please indicate the main folders. eg., 1024 256"
read f
for file in ${f[@]}
do
c='reset'
for xs in ${file}/x*; do
c='reset'
N=${file} # N is fixed to monomer number value
for nr in ${xs}/*; do # eg.nr is 512/x0336/168
c='reset'
for ni in ${nr}/*; do # ni is 512/x0336/168/0001
c='reset'

x=${xs/${file}\//}; # eg. xs is 512/x0336 this line redefines it as x = x0336
x=${x/x/} # now x is 0336
xm=$x


rn=${nr/${xs}\//} # rn is 168
echo " rn is $rn it it supposed to be in this form 168 "
in=${ni/${xs}\//}
in=${in/${rn}\//}
# in is 0001
echo " in is $in it supposed to be in this form 009 "
x=${x}${rn}${in} # x is 03361680001
ms=m${N}${x}
echo " x is $x "
r=${x}
echo " r is $r "
R=${file}${r}
echo " R is $R "
echo "${file}"
echo " N is $N "
echo " ms is $ms "
#Now counting the number of mstm outputs. In a perfect world it should be 25, but some times it is less then this.
c=$(find ${ni}/mt* -type f -size +3000c)  # this is another way c=$(ls -l ${ni}/mt* | wc -l) without filtering any file by the size  another way to do this: c=( ${ni}/mt* ); c=${#c[@]} or a better way 
mstm=(${c})
c=${#mstm[@]}
if [ "${c}" -eq "0" ]; then
	continue
else
echo "%% There are $c mstm output files in this directory">${ni}/m${R}.m
e=0

mt=$(ls ${ni} | grep "\.dat"); mt=(${mt}) # this writes an array consisting of the name of all .dat in ${ni}
for m in ${mstm[@]}; do


#filesize=$( wc -c < ${m} )
#echo "filesize is $filesize"
#if [ "$filesize" -lt "3000" ]; then
#echo " this output file ( $m ) is incomplete. It is now skiped "
#break

#else

o=$pwd

echo "%% Initialize variables.

filename = '~/Dropbox/Dropbox/matlab_plots_and_data/mstmoutputs/special${o}/${m}';
startRow = 52;
endRow = 232;

%% Format string for each line of text:

formatSpec = '%8f%13f%13f%13f%13f%13f%13f%13f%13f%13f%f%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to format string.
textscan(fileID, '%[^\n\r]', startRow-1, 'WhiteSpace', '', 'ReturnOnError', false);
dataArray = textscan(fileID, formatSpec, endRow-startRow+1, 'Delimiter', '', 'WhiteSpace', '', 'ReturnOnError', false);

%% Close the text file.
fclose(fileID);

%% Allocate imported array to column variable names
theta = dataArray{:, 1};
${ms}_S_${e}_11 = dataArray{:, 2}; % Exm: 640336_S_1_11 = dataArray{:, 2}
${ms}_S_${e}_12 = dataArray{:, 3}; % Exm: 640336_S_1_11 = dataArray{:, 3}
${ms}_S_${e}_13 = dataArray{:, 4};
${ms}_S_${e}_14 = dataArray{:, 5};
${ms}_S_${e}_22 = dataArray{:, 6};
${ms}_S_${e}_23 = dataArray{:, 7};
${ms}_S_${e}_24 = dataArray{:, 8};
${ms}_S_${e}_33 = dataArray{:, 9};
${ms}_S_${e}_34 = dataArray{:, 10};
${ms}_S_${e}_44 = dataArray{:, 11}; 

%% Clear temporary variables
clearvars filename startRow endRow formatSpec fileID dataArray ans;" >> ${ni}/m${R}.m
echo " tail is stupid" > .optic.in
<${m} tail -n +51 | head -n 1 >.optic.in
optic=''
optic=$(cat .optic.in)
echo " optic string is $optic "
optic=(${optic})
Qe=${optic[0]}; Qabs=${optic[1]}; Qsca=${optic[2]}
echo " ******* optic ${optic[@]} and Qe is ${optic[2]}"
#lets create nested arrays
Qe[${e}]=${Qe} ; Qabs[${e}]=$Qabs ; Qsca[${e}]=$Qsca
s11[${e}]=${ms}_S_${e}_11 
s12[${e}]=${ms}_S_${e}_12
s13[${e}]=${ms}_S_${e}_13
s14[${e}]=${ms}_S_${e}_14
s22[${e}]=${ms}_S_${e}_22
s23[${e}]=${ms}_S_${e}_23
s24[${e}]=${ms}_S_${e}_24
s33[${e}]=${ms}_S_${e}_33
s34[${e}]=${ms}_S_${e}_34
s44[${e}]=${ms}_S_${e}_44
echo " e is $e ######################## "
echo " $s11[${e}] @@@@@@@@@@@@@@ "
e=$((${e}+1))

#fi
done # with the For $m

lastterm=${ms}_S_11

 


cc=$((${c}-1))
  
for i in $(seq 0 ${cc})   ; do
if (($i == 0));then

Qetot=${Qe[$i]}; Qabstot=${Qabs[$i]}; Qscatot=${Qsca[$i]}
s11tot=${s11[$i]} 
s12tot=${s12[$i]}
s13tot=${s13[$i]} 
s14tot=${s14[$i]} 
s22tot=${s22[$i]} 
s23tot=${s23[$i]} 
s24tot=${s24[$i]} 
s33tot=${s33[$i]} 
s34tot=${s34[$i]}
s44tot=${s44[$i]} 
else 
Qetot=${Qetot}+${Qe[$i]}
Qabstot=${Qabstot}+${Qabs[$i]}
Qscatot=${Qscatot}+${Qsca[$i]}
s11tot=${s11tot}+${s11[$i]}
s12tot=${s12tot}+${s12[$i]}
s13tot=${s13tot}+${s13[$i]}
s14tot=${s14tot}+${s14[$i]} 
s22tot=${s22tot}+${s22[$i]} 
s23tot=${s23tot}+${s23[$i]} 
s24tot=${s24tot}+${s24[$i]}
s33tot=${s33tot}+${s33[$i]} 
s34tot=${s34tot}+${s34[$i]}
s44tot=${s44tot}+${s44[$i]} 
fi
done



echo "%AVARAGING ALL COMPONENTS
Qeavg${R}= ( ${Qetot} )./ ${c}
Qabsavg${R}= ( ${Qabstot} )./ ${c}
Qscaavg${R}= ( ${Qscatot} )./ ${c}
S11avg${R}= ( ${s11tot} )./ ${c} 
s12avg${R}= ( ${s12tot} )./ ${c} 
S13avg${R}= ( ${s13tot} )./ ${c} 
S14avg${R}= ( ${s14tot} )./ ${c} 
S22avg${R}= ( ${s22tot} )./ ${c} 
S23avg${R}= ( ${s23tot} )./ ${c} 
S24avg${R}= ( ${s24tot} )./ ${c} 
S33avg${R}= ( ${s33tot} )./ ${c} 
S34avg${R}= ( ${s34tot} )./ ${c} 
S44avg${R}= ( ${s44tot} )./ ${c}

frwd_tm${R}= S11avg${R}(1)
back_tm${R}= S11avg${R}(181)
pol_tm${R}=-s12avg${R}
maxpol_tm${R}=max(pol_tm${R})

%% Clear temporary variables" >> ${ni}/m${R}.m
#Clearing all variables requires first removin "+" signs from sxxtot 
for i in $(seq 0 ${cc})   ; do
if [ " $i " -lt " $c " ]; then
s11tot=${s11tot/+/ }
s12tot=${s12tot/+/ }
s13tot=${s13tot/+/ }
s14tot=${s14tot/+/ }
s22tot=${s22tot/+/ }
s23tot=${s23tot/+/ }
s24tot=${s24tot/+/ }
s33tot=${s33tot/+/ }
s34tot=${s34tot/+/ }
s44tot=${s44tot/+/ }
else
break
fi
done


echo " clearvars ${s11tot} ${s12tot} ${s13tot} ${s14tot} ${s22tot} ${s23tot} ${s24tot} ${s33tot} ${s34tot} ${s44tot} ">> ${ni}/m${R}.m



echo " %Plots 
theta=[0:180]
theta=theta'
%figure1= figure
%plot(theta,S11avg${R},'b')
%hold on
%title('Phase Function - N= $file Xm= ${xm} nr= ${rn} ni= ${in} ' )
%hold off

pol${R}=-s12avg${R}
%figure2= figure
%plot(theta,pol${R},'b')
%hold on
%title('Linear Polarization - N= $file Xm= ${xm} nr= ${rn} ni= ${in}' )
%hold off
%maxpol${R}=max(pol${R})
%minpol${R}=min(pol${R})" >> ${ni}/m${R}.m

cat ${ni}/m${R}.m >> FullRetrieve.m
fi
done
done
done
done

echo " #######################################################################"
echo "#######################################################################"
echo "#######################################################################"


echo " DO NOT TRUST THIS COPY! DROPBOX HAVE ONE OF THE WORST BUG." 
echo " IT FREQUENTLY REPLACES ANY FILES TO AN OLD VERSION."

echo " ALWAYS UPDATE THE CODES FROM TAMU ONEDRIVE ACCOUNT."


echo "#######################################################################"
echo "#######################################################################"
echo "#######################################################################"

