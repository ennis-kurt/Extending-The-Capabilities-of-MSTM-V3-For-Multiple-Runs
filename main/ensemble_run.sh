#!/bin/bash
set -e
IBlue='\033[1;94m'
Color_Off='\033[0m'
On_IRed='\033[0;101m'
IWhite='\033[0;97m'
green='\e[32m'

#[ "$(whoami)" = "root" ] && echo -e Access granted. ulimit will be modified for this session || { echo -e "
#$IBlue Please run the script with sudo or under root. $Color_Off " && 
#echo -e "
#$IBlue Otherwise it can't modify ulimit and mstm may crash easily due to memory issue $Color_Off " 

#echo -e " 
#Type ${IWhite}${On_IRed}y${Color_Off} if you still wish to run without sudo privilidge or ${IWhite}${On_IRed}n${Color_Off} to exit "

#for ((i=1; i<=100; i++))
#do
#read rsp
#rsp=($rsp)
#if [ "$rsp" = n ]; then
#exit
#elif [ "$rsp" = y ]; then
#echo -e "${IBlue}Script is Starting Without ulimit modifications${Color_Off}"
#break
#else
#echo -e "${IBlue}Please type a legitimate input${Color_Off} "
#fi
#done }

#if [ "$(whoami)" = "root" ]; then
#echo -e "${IBlue}Following changes will be made${Color_Off}

uli=$(ulimit -i)
ull=$(ulimit -l)
ulm=$(ulimit -m)
uln=$(ulimit -n)
ulq=$(ulimit -q)
uls=$(ulimit -s)
ult=$(ulimit -t)
ulu=$(ulimit -u)
ulv=$(ulimit -v)
ulx=$(ulimit -x)

#ulimit -S -i unlimited 
ulimit -S -l unlimited
ulimit -S -m unlimited
ulimit -S -n unlimited
ulimit -S -q unlimited
ulimit -S -s unlimited
ulimit -S -t unlimited
ulimit -S -u unlimited
ulimit -S -v unlimited
ulimit -S -x unlimited

newuli=$(ulimit -i)
newull=$(ulimit -l)
newulm=$(ulimit -m)
newuln=$(ulimit -n)
newulq=$(ulimit -q)
newuls=$(ulimit -s)
newult=$(ulimit -t)
newulu=$(ulimit -u)
newulv=$(ulimit -v)
newulx=$(ulimit -x)

echo " Following changes have been made For the Ulimit values


    
Ulimit Identity   Old value             New Value		
		
    i             $uli            	$newuli
    l	          $ull            	$newull
    m	          $ulm            	$newulm
    q	          $ulq            	$newulq
    s	          $uls            	$newuls
    t	          $ult            	$newult
    u	          $ulu            	$newulu
    v	          $ulv            	$newulv
    x	          $ulx            	$newulx
    n	          $uln            	$newuln
    
Changes Are limited with Hard Values. Only Soft Limits are set due to lack of sudo privilidge "
    
    
    
    
    
    
    
echo -e "${IBlue}user limits are now:${Color_Off} " 
ulimit -a
#else
#echo -e '${IBlue}Please Note That the following user limits may affect the executions performance. 
#Memory crashes are more likely comparing to unlimited cases${Color_Off}'
#ulimit -a
#fi




# ==============================Starts Here=============================

#25 realization of aggregate shape


aggreal=({1..25}) # This defines an Array From 1 to 25


# ====================================================================================================================================================================================
#Section 1. Input variables are read here. No need to modify this section since a request message for each variable will be prompted to terminal, then variable will be given by the user during the execution


#number of monomers
echo -e "${IBlue}Please type the Number of monomers separated by space .Eg. 32 64 128${Color_Off}"
read n
ns=($n)
echo -e "${IBlue}number of monomers ${ns[@]}${Color_Off}" | tee outbash.log

#Refractive Index (look at Skorov et al. for optimum values)
echo -e " ${IBlue}Please type: \"yes\" to use empirical refractive index values \"no\" to manually input fixed range of refractive indices${Color_Off} "
for ((i=1; i<=10; i++))
do
read refr
refr=($refr)
if [ "$refr" = "no" ]; then
echo -e "${IBlue}Please Type the real and imaginary refractive index of each realization subsequently. Eg. 1.5 1.7 2.0${Color_Off}"
echo -e "${IBlue}Real refractive index${Color_Off}"
read nr
nr=($nr)
for i in "${!nr[@]}"; do 
	nr[i]=$(python -c "print('{:.2f}'.format(${nr[i]}))")
done
echo "size param range: ${nr[@]}"
echo -e "${IBlue}imaginary refractive index${Color_Off}"
read ni
ni=($ni) #imaginary
for i in "${!ni[@]}"; do 
	ni[i]=$(python -c "print('{:.4f}'.format(${ni[i]}))")
done
echo -e "${IBlue} Refractive Indices: Real: ( ${nr[@]} ) Imginary: ( ${ni[@]} )${Color_Off}" | tee -a outbash.log
break
elif [ "$refr" = "yes" ]; then
echo -e " "
break
else
echo -e "${IBlue}Please type a legitimate input${Color_Off}"
fi
done

echo -e " ${IBlue}Please type the monomer size parameter ${Color_Off}"
read xs
xs=($xs)
for i in "${!xs[@]}"; do 
	xs[i]=$(python -c "print('{:.4f}'.format(${xs[i]}))")
done
echo "size param range: ${xs[@]}"

# echo -e " ${IBlue}Please type the Wavelength range as micrometer${Color_Off}"
# read wv
# wv=($wv)

# echo -e " ${IBlue}Number of monomers : ${ns[@]}${Color_Off}
# monomer radius : ${ls[@]}
# wavelengths : ${wv[@]} "

############ Number of Cpu & how to schedule ##############
echo -e ${IBlue}How many processors would you like to use for this calculation.${Color_Off}
read ncpu
echo -e " ${IBlue} # First $ncpu processors will be used. ${Color_Off}" | tee -a outbash.log

echo -e "${IBlue} You can specify the cpu ids separated by space to run the processes${Color_Off}"
echo -e ${IBlue}For example. with 4 cpus used you should specify 4 cpu ids. 0 1 3 7 ${Color_Off}
echo -e ${IBlue}Press ${On_IRed}Enter${Color_Off} ${IBlue}for default setup which let the OS schedule automotically${Color_Off}
for ((i=1; i<=20; i++))
{
	read cpu_ids

	if [ "$cpu_ids" != "" ]; then
	cpu_ids=($cpu_ids)

		if [ ${#cpu_ids[@]} -ne $ncpu ]; then
			echo -e ${On_IRed}You should specify a list of cpu ids whose number of elements equal to number of cpus${Color_Off}
			continue
		else
			break
		fi
	else
		echo 'Default Mode'
		break
	fi
	

	## cpu_ids is used in the part mstm runs initiated. 
}

echo -e "${IBlue}please press Enter to start calculations${Color_Off}"
read enter
if [ "$enter" = "\
" ]; then
echo -e " "
else
echo -e ${IBlue}please Press Enter to Start${Color_Off}
fi



q=$((25/${ncpu})) # incase ncpu=6 q=4 because bash works with integers, but no worries, it also has built in remainder function (%)
r=$((25%${ncpu})) #This should give the remainder, for 6 cpu it should be 1
echo -e ${IBlue}Realization number is $q ${Color_Off}| tee -a outbash.log 
echo r is $r >>log
[ ! -d tmatrixfiles ] && mkdir -p tmatrixfiles
[ ! -d dnearfieldfiles ] && mkdir dnearfieldfiles

# ====================================================================================================================================================================================

# Section 2. THIS SECTION IS TO CREATE MSTM.INP FILES. ALL INPUT FILES ARE NAMED ACCORDING TO CHOICE OF THE INPUT VARIABLES.

: <<"END"
# ------------------------------------------------------------------------------------------------------------------------------------------

K=$((${#ls[@]} * ${#wv[@]}))

B=$(seq 0 $K) # this is 1d array ( or string) which needs to be converted to multi-d array as in next line
B=($B)

    for rmon in ${ls[@]}
      do
	for wl in ${wv[@]}
	 do
	 xs=(${xs[@]} `echo "scale = 4; 2*3.1416*${rmon}/${wl}" | bc`)
  	
	done
    done
# ------------------------------------------------------------------------------------------------------------------------------------------
END


for i in ${ns[@]} 
 do
# for wl in ${wv[@]}
# do 
# 	#

# 	if [ "$refr" = "yes" ]; then
# 	 # ------------------------------------------------------------------------------------------------------------------------------------------
#     	wl1=0.4909
# 		wl2=0.9348
	 
# 		if [[ $wl == $wl1 ]] ;then
# 			nr=(1.3 1.71 2.0)  ; ni=(0.0226 0.09) # note that i still need to run with the following comb. (1.3 2.0) * ( 0.0452 )
# 		elif [[ $wl == $wl2 ]]; then
#        		nr=(1.3 1.66 2.0) ; ni=(0.00438  0.001) # note that i still need another run with the following comb. (1.3 2.0) * ( 0.00219 )
#       	else 
#       		echo -e "${IBlue} please modify the Section 2. in the script if dynamic creation of refractive indices is needed${Color_Off}"
#       	fi
# # ------------------------------------------------------------------------------------------------------------------------------------------
#   	else 
#   		echo -e "${IBlue} Input values of Refractive Indices are being used: nr: ( ${nr[@]} ) ni: ( ${ni[@]} ) ${Color_Off}"
#   	fi
  
  for l in ${nr[@]} 
   do
   for m in ${ni[@]}
    do
    for j in ${aggreal[@]}
     do
	for k in ${xs[@]} 
	do
	
	#   # k is the monomer size parameter.
	#   k=$(echo "scale = 4; 2*3.1416*${rmon}/${wl}" | bc)
	#   echo monomer size paramater = $k
	

	  #for the file names rescaling these parameters and remove the "." from the variables.
	  # Such as, l=0.01 will be converted to 001
	  
	  kx=${k/./}; lr=${l/./}; mi=${m/./}

	  # Noting the date and time of the run started
		sed '8i\'$date mstm.inp > mstm${j}_${i}_${kx}_${lr}_${mi}.inp

	  #number_spheres
	  sed '13i\'$i mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile 
	  mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp #number of sphere
	  
	  #aggregate shape files
	  #a='home/titan/Titan/New/input/n'$i'/a'$j'.out' # has to be modified
	  a='position/n'$i'/a'$j'.out'
	  sed '15i\'$a mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile 
	  mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp
	  
	  #output_file
	  b='output/'$i'/x'$kx'/'$lr'/'$mi'/mt_'$j'_'$i'_'$kx'_'$lr'_'$mi'.dat' # data files stored in harddisk in an organized way
	  #All the output files stored in a following way: ?/512/x0.01/nr1.7/ni1.3/mt_25_512_001_17_13.dat.Note that all dots '.' are removed, 
	  #Thus interperation of the name should be made carefully.
	  sed '17i\'$b mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile 
	  mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp 
	  #Next line creates the directories to put the output files, just declared above.
	  #[ -d File ] is true if File exist and a directory, [! -d File ] is true if File DOES NOT exist and a directory
	  
	  [ ! -d output ] && mkdir -p output; [ ! -d output/$i ] && mkdir -p output/$i
	  [ ! -d output/$i/x${kx} ] && mkdir -p output/$i/x${kx} &&
	  [ ! -d output/$i/x${kx}/${lr} ] && mkdir -p output/$i/x${kx}/nr${lr} 
	  [ ! -d output/$i/x${kx}/${lr}/${mi} ] && mkdir -p output/$i/x${kx}/${lr}/${mi} &&
	  echo -e " ${IBlue}Directories for the T-Matrix output files are created succesfully${Color_Off}" | tee -a outbash.log
	 
	  #length scale factor
	  sed '25i\'$k mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile 
	  mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp
	  
	  #real_ref_index_scale_factor
	  sed '27i\'$l mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile 
	  mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp
	 
	  #imag_ref_index_scale_factor
	  sed '29i\'$m mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile 
	  mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp
	  
	   #Near filed position 
	  nfp='dnearfieldfiles/nf_'$j'_'$i'_'$kx'_'$lr'_'$mi'.dat'
	  sed '103i\'$nfp mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile 
	  mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp
	  
	   # Tmatrixfiles, iF THE TMATRIX FILE EXISTS, CREATED BY A PREVIOUSLY COMPLETED OR DISRUPTED RUN, THEN THIS FILE WILL BE USED. BELOW CODE ALSO CHECKS IF THE TMATRIX CALCULATION IS 		   #COMPLETED OR DISTRUPTED. IF THE CALCULATION IS DISTRUPTED THEN THE SCRIPT WILL CARRY ON THE CALCULATION FROM THE MAXIMUM EXECUTED T-MATRIX ORDER. IF THE CT-MATRIX FILE IS 		   #COMPLETE THEN IT #WILL USE THIS FILE TO WRITE THE SCATTERING MATRIX. OTHERWISE NEW T-MATRIX FILE WILL BE WRITTEN BY STARTING OVER THE T-MATRIX CALCUALTION. PS. FOR NOW IT DOES 		   #NOT WOR AS IT IS PROMISED #ABOVE. IT ONLY CHECKS IF THE FILE IS CREATED PREVIOUSLY OR NOT. NOW IT CANNOT CHECK IF IT COMPLETED OR NOT. BUT I WILL FIX THIS SOON.
	
	tmf='tmatrixfiles/'${j}${i}${kx}${lr}${mi}
	tmtf=${j}${i}${kx}${lr}${mi}
	#NEXT LINE SHOULD BE MODIFIED FOR GENERAL USE Note that I do not need the next few lines for now.
	
	#[ -d tmatrixfiles/tmf_'$j'_'$i'_'$kx'_'$lr' ] && sed '102i\2' mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile || sed '102i\1' mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile 
        #mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp	
	

	#below by [ -s File ] is true if file exist and its size greater than zero.	
	#check if tmatrix file exist
	

	
	[ -s ./tmatrixfiles/${tmtf} -a -s $b ] && { filesize=$( wc -c < $b )
											   echo -e " ${filesize}${Color_Off}"
	[ "${filesize}" -lt "3000" ] && { echo -e "${On_IRed} T-Matrix run for \e[7m[ ${j}_${i}_${kx}_${lr}_${mi} ]\e[27m was interrupted ${Color_Off}" | tee -a outbash.log
	echo -e "${On_IRed} MSTM will Resume the interrupted Run${Color_Off}" | tee -a outbash.log
	sed '109i\2' mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile
	mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp 
	} || { echo -e "${green} Looks like T-MATRIX run is complete for \e[7m[ ${j}_${i}_${kx}_${lr}_${mi} ]\e[27m. This run will be skipped ${Color_Off}" | tee -a outbash.log
		sed '109i\0' mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile 
		mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp
	      }
	 }

	[ -s ./tmatrixfiles/${tmtf} -a ! -s $b ] && { echo -e "${IBlue} T-Matrix run for \e[7m[ ${j}_${i}_${kx}_${lr}_${mi} ]\e[27m was interrupted ${Color_Off}" | tee -a outbash.log
			echo -e "${IBlue} MSTM will Resume the interrupted Run${Color_Off}" | tee -a outbash.log
			sed '109i\2' mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile
	  		mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp ; }
	
	[ ! -s ./tmatrixfiles/${tmtf} ] && { echo -e "${IBlue} T-Matrix run will start from begining for [ ${j}_${i}_${kx}_${lr}_${mi} ]${Color_Off}" | tee -a outbash.log
		sed '109i\1' mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile
	  	mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp ; }

# Below commented block does exactly the same thing as the above block

#	if [ -s ./tmatrixfiles/${tmf} ]; then 
#	#check if output file also exists (but scattering matrix not completed). if so then tell mstm no need for starting over. 
#		if [ -s $b ]; then 
#		   filesize=$( wc -c < $b )

#			# Check if the output file (scattering Matrix) is complete or only the headers written on it. 
#			# if not complete this means that t-matrix run had started but later it was interupted. If that is the case we will tell MSTM not to start over. 
#			# It will Resume where it was interrupted 
#	 		if [ "$filesize" -lt "3000" ]; then  
#				echo -e " T-Matrix run for [ ${j}_${i}_${kx}_${lr}_${mi} ] was interrupted"
#				echo -e " MSTM will Resume the interrupted Run"
#	 			sed '109i\2' mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile
#	 			mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp 
#	#Now, if there is tmatrix file and there is output file but output file looks like large enough to be regarded as completed then no need to calculate t-matrix
#				
#			else 
#				echo -e " Looks like T-MATRIX run is complete for [ ${j}_${i}_${kx}_${lr}_${mi} ]. This run will be skipped "
#				sed '109i\0' mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile 
#	 			mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp
#			fi 
#	#Note that this still starts unnecassarily scattering matrix ,which allready exists, calculation from tmatrix file. This will be resolved  in 
#	#section #3, but this line still written in case completely skipping this run will fail somehow in section 3.	   

#	#if not, then still no need to start over tmatrix calculation, since tmatrix file exist but scattering matrix file had not been created	 		
#		else		
#			sed '109i\2' mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile
#	  		mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp 
#		fi
#	else	
# 	# If there is no T-matrix file at all then start over.
#		sed '109i\1' mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile
#	  	mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp
#	fi 
	
	


	  sed '111i\'$tmf mstm${j}_${i}_${kx}_${lr}_${mi}.inp > newfile 
	  mv newfile mstm${j}_${i}_${kx}_${lr}_${mi}.inp
	 
	 #Moving All the input files into input/${i}'_'${kx}'_'${lr}'_'${mi}
	  file=${i}'_'${kx}'_'${lr}'_'${mi}
	
	  [ ! -d position/$file ] && mkdir -p position/$file
	 # mv mstm${j}_${i}_${kx}_${lr}_${mi}.inp ./input/$file/mstm${j}_${i}_${kx}_${lr}_${mi}_${lr}_${mi}.inp
	# [[ -f input/mstm/${file}/ms ]] && rm ms; [[ -f input/mstm/${file}/m ]] && rm m; [[ -f input/mstm/${file}/mst ]] && rm mst
	# find . input/mstm/${file}/ -size 0 -delete
	
	#mv "./input/mstm/${file}/mstm${j}_${file}.inp " "./input/mstm/${file}/mstm${j}_${file/./}.inp"
	#cd ..
        echo -e ${IBlue}Input Files are Created succesfully! ${Color_Off}| tee -a outbash.log
	
     done
    # done	
   done
  done
 done
done



#===========================================================================================================================================================

# SECTION 3 : This part is to create the external scripts 

 #mv n* position/
  echo -e ${IBlue}Now The External Scripts Are Being Written.${Color_Off} | tee -a outbash.log
 for (( np=1;np<=${ncpu};np++));do
#    xs=('') #this will reset the previous array
   
   echo "# This script runs a set of child processes on a single cpu core. 
	 #The main script is ensemble_run.sh which writes and controls all the 
	 #child processes " > script${np}
   
  # Following first 6 lines may be unnecessary
   echo "#number of monomers " >> script${np}
 #  echo "ns=( ${ns[@]} )" >> script${np}
  # echo "#Refractive Index (look at Skorov et al. for optimum values) " >> script${np}
   #echo "nr=( ${nr[@]} ) #real " >> script${np}
   #echo "ni=( ${ni[@]} ) #imaginary " >> script${np}
   #echo "xs=( ${xs[@]} )" >> script${np}
	
	frst=$(((${np}-1)*${q}+1)) # this is for the iteration 1..25 separated on each cpu.sh (for 6 cpu, np =1 => dg =4, np=2 => dg=8
	lst=$(((${np}-1)*${q}+${q}))
	
	
	if [ $np -ne ${ncpu} ] ; then
	rng=$((${q}-1))
	else
	rng=$((${r}+${q}-1))
	fi
	
	a=$(seq 0 $rng) # This will make a 1d- array. Eg. for ncpu=6 q=4 a= 0 1 2 3 . it means a[0]= 0 1 2 3
	elm=($a) # this will make multi-d array by splitting the array "a"
	 
	for i in ${elm[@]}; 
	do b[i]=$frst
	frst=$(($frst + 1 )) # or let frst ++
	done
	echo -e ${IBlue}following agregate input files are being calculated ${b[@]}${Color_Off}
	
  # echo z="("${b[@]}")" >>script${np}

# ------------------------------------------------------------------------------------------------------------------------------------------

# K=$((${#ls[@]} * ${#wv[@]}))

# B=$(seq 0 $K) # this is 1d array ( or string) which needs to be converted to multi-d array as in next line
# B=($B)

    # for rmon in ${ls[@]}
    #   do
	# for wl in ${wv[@]}
	#  do
	#  xs=(${xs[@]} `echo "scale = 4; 2*3.1416*${rmon}/${wl}" | bc`)
  	
	# done
    #  done

# ------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------------
echo "for sn in ${ns[@]} ;do " >> script${np}
echo "	for sx in ${xs[@]/./};do " >> script${np}
echo "		for rn in ${nr[@]/./};do " >> script${np}
echo "	   		for im in ${ni[@]/./};do " >> script${np}
echo "	        	for sf in ${b[@]};do " >> script${np} #or "for dos in cat($ls);do ' ~/programs/mstmv3.0/run_mstm input/mstm/${sn}_${sx}_${rn}_${im}/$dos"
echo '		            	tmtf=${sf}${sn}${sx}${rn}${im}
							if [ -s ./output/${sn}/x${sx}/$rn/$im/mt_${sf}_${sn}_${sx}_${rn}_${im}.dat ]; then 
							Size=$( wc -c < ./output/${sn}/x${sx}/$rn/$im/mt_${sf}_${sn}_${sx}_${rn}_${im}.dat )
							if [ "${Size}" -gt "3000" ]; then
								continue
							
							else
								./run_mstm mstm${sf}_${sn}_${sx}_${rn}_${im}.inp
								echo "The run ${sf}_${sn}_${sx}_${rn}_${im} is completed on $(date)"
								rm tmatrixfiles/${tmtf}
							fi
						else 
							./run_mstm mstm${sf}_${sn}_${sx}_${rn}_${im}.inp
							echo "The run ${sf}_${sn}_${sx}_${rn}_${im} is completed on $(date)"
							rm tmatrixfiles/${tmtf}
						fi' >> script${np}
echo "      		done" >> script${np}
echo "			done" >> script${np}
echo "		done " >> script${np}
echo "	done " >> script${np}
echo "done " >> script${np}
   
 
   
 done

#===========================================================================================================================================================
#Section 4

#Now Executing All The external scripts simultaneously on an individual cpu core ( Serial processing )

#: <<"END"

if [ "$cpu_ids" != "" ]; then
	echo 'Manual Task Schedule Mode is Selected'
	for (( c=1; c<=${ncpu}; c++))
	{
		chmod +x script${c}
		p=$(( ${c}-1 ))
		cpu=${cpu_ids[p]}
            
        if [ $cpu -ne $(( ${cpu_ids[-1]} )) ]; then 
			taskset -c ${cpu} ./script${c} &  # if not the last run then run on background
        else
            taskset -c ${cpu} ./script${c} # Last run in a script allways run on foreground
        fi
	}
else
	echo 'Default Mode is Selected'
	for (( c=1; c<=${ncpu}; c++))
	{
		if [ $c -ne ${ncpu} ]; then
            echo "echo new run initiated on background"
            # setting priority to low so that all cpus can be used and at the same time 
            # the computer can be still run for daily tasks. Higher the nice value lower the priority
            ./script${c} &  # if not the last run then run on background # nice -n 10 
        else
            ./script${c} # Last run in a script allways run on foreground #
        fi
	}

fi
#END


# The next Section is blocked because it is still in construction
: <<"END"
# =========================================================================================================================================================

#Section 5
# This section creates Matlab scripts which will be used during postprocessing ( such as, taking avarage of all 25 realization )

for sn in ${ns[@]} ;do " >> script${np}
	for sx in ${xs[@]/./};do " >> script${np}
		for rn in ${nr[@]/./};do " >> script${np}
			for im in ${ni[@]/./};do " >> script${np}
				for file in ./output/${sn}/x${sx}/$rn/$im/mt_ ;do
					for rm in ${file}/x*; do
					x=${rm/${file}\//}
					x=${x/x/}

#Now counting the number of mstm outputs. In a perfect world it should be 25, but some times it is less then this.
c=$(ls -l ${rm}/mt* | wc -l) 
echo -e "%% There are $c mstm output files in this directory">${rm}/m${x}.m
e=0
for m in ${rm}/mt*.dat; do
ms=${m/\//}
ms=${ms/\//}
ms=${ms/.dat/}
ms=m${ms}


echo -e "%% Initialize variables.
filename = '/home/ucnk/matlab/April11/mstmoutputs/${m}';
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
${ms}_S_11 = dataArray{:, 2}; % Exm: 640336_S_1_11 = dataArray{:, 2}
${ms}_S_12 = dataArray{:, 3}; % Exm: 640336_S_1_11 = dataArray{:, 3}
${ms}_S_13 = dataArray{:, 4};
${ms}_S_14 = dataArray{:, 5};
${ms}_S_22 = dataArray{:, 6};
${ms}_S_23 = dataArray{:, 7};
${ms}_S_24 = dataArray{:, 8};
${ms}_S_33 = dataArray{:, 9};
${ms}_S_34 = dataArray{:, 10};
${ms}_S_44 = dataArray{:, 11}; 

%% Clear temporary variables
clearvars filename startRow endRow formatSpec fileID dataArray ans;" >> ${rm}/m${x}.m

s11[${e}]=${ms}_S_11 #this will create a nested array
s12[${e}]=${ms}_S_12
s13[${e}]=${ms}_S_13
s14[${e}]=${ms}_S_14
s22[${e}]=${ms}_S_22
s23[${e}]=${ms}_S_23
s24[${e}]=${ms}_S_24
s33[${e}]=${ms}_S_33
s34[${e}]=${ms}_S_34
s44[${e}]=${ms}_S_44
echo -e $e
e=$((${e}+1))
done # with the For $m

lastterm=${ms}_S_11

 



  
for i in $(seq 0 ${c})   ; do
if (($i == 0));then
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

echo -e "%AVARAGING ALL COMPONENTS
S11avg= ( ${s11tot} )./ ${c} 
s12avg= ( ${s12tot} )./ ${c} 
S13avg= ( ${s13tot} )./ ${c} 
S14avg= ( ${s14tot} )./ ${c} 
S22avg= ( ${s22tot} )./ ${c} 
S23avg= ( ${s23tot} )./ ${c} 
S24avg= ( ${s24tot} )./ ${c} 
S33avg= ( ${s33tot} )./ ${c} 
S34avg= ( ${s34tot} )./ ${c} 
S44avg= ( ${s44tot} )./ ${c}" >> ${rm}/m${x}.m


#echo -e " S11avg = s11tot./$c " >> ${m}.

#for sum in ${s11[${@}]} # which means sum in mt_1_(...)_S11_... mt_2_(...)_S11_...  ...
#do
#s="}

done
done
END


