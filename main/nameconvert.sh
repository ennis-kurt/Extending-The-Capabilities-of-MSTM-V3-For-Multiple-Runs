#!/bin/bash
#set -e
echo "Specify the folders to run this code. To run the for all the folders press Enter"
read n
if [ "$n" != "" ]; then
	N=($n)
else
	echo 'running the code for all N=( 64 128 256 512 1024 )'
	N=( 64 128 256 512 1024 )
fi

echo N is ${N[@]}
xm=( 032 073 0168 01680 1680 0235 02350 0437 04370 0448 04480 0504 05040 0832 8320 08320 08319 3360 6398 9598 0320 03200 0730 07300 0336 03360 0640 06398 0960 09598 5795 05795 0580 4795 04795 0480 4799 04799 5299 05299 0530 4299 04299 0430 8319 08319 7299 07299 0730)
real_ref=( 13 130 20 200 171 170 166 168 23 230 145 18 180 )
img_ref=( 0002 00020 00226 0023 009 0090 00900 0045 00450 045 03 0300 03000 0006 00060 000438 0004 00044 0001 00010)


########### functions ###########
size_param ()

{ # this substitue the size parameter
case $sp in
	032)
	    _sp=03200
	    ;;
	073)
	    _sp=07300
	    ;;
	3360)
	    _sp=03360
	    ;;
	4299)
	    _sp=04299
	    ;;
	4795)
	    _sp=04795
	    ;;
	5299)
	    _sp=05299
	    ;;
	5795)
	    _sp=05795
	    ;;
	6398)
	    _sp=06398
	    ;;
	9598)
	    _sp=09598
	    ;;
	8319)
	    _sp=08319
	    ;;
	7299)
	    _sp=07300
	    ;;
	0320)
	    _sp=03200
	    ;;
	0730)
	    _sp=07300
	    ;;
	0336)
	    _sp=03360
	    ;;
	0430)
	    _sp=04299
	    ;;
	0480)
	    _sp=04795
	    ;;
	0530)
	    _sp=05299
	    ;;
	0580)
	    _sp=05795
	    ;;
	0640)
	    _sp=06398
	    ;;
	0960)
	    _sp=09598
	    ;;
	0832)
	    _sp=08319
	    ;;
	08320) # expect some minor inaccuracy on this one, since it is actually 08320. This is not a rounding.
		_sp=08319
	;;
	8320) # expect some minor inaccuracy on this one, since it is actually 08320. This is not a rounding.
		_sp=08319
	;;
	0730)
	    _sp=07299
	    ;;
	0168)
	    _sp=01680
	    ;;
	1680)
	    _sp=01680
	    ;;
	0235)
	    _sp=02350
	    ;;
	0437)
	    _sp=04370
	    ;;
	0448)
	    _sp=04480
	    ;;
	0504)
	    _sp=05040
	    ;;
	4799)
	    _sp=04799
	    ;;
	*)
	    _sp=$sp

esac
}

###############
n_real()

{

case $nr in
	13)
	 _nr=130
	;;
	20)
	 _nr=200
	;;
	23)
	 _nr=230
	;;
	170)
	 _nr=171
	;;
	18)
	 _nr=180
	;;
	*)
	 _nr=$nr
esac
}

###############
n_img ()

{

case $ni in
	00226)
	 _ni=00226
	;;
	009)
	 _ni=00900
	;;
	03)
	 _ni=03000
	;;
	045)
	 _ni=00450
	;;
	000438)
	 _ni=00044
	;;
	0023)
	 _ni=00226
	;;
	0090)
	 _ni=00900
	;;
	0300)
	 _ni=03000
	;;
	0045)
	 _ni=00450
	;;
	0004)
	 _ni=00044
	;;
	0002)
	 _ni=00020
	;;
	0001)
	 _ni=00010
	;;
	0006)
	 _ni=00060
	;;
	*)
	 _ni=$ni
esac
}

for n in ${N[@]}; do
	#echo loop1
	
	for sp in ${xm[@]}; do

		if [[ ! -d ${n}/x${sp} ]] && [[ ! -d ${n}/x${_sp} ]]  ; then 
			continue
			echo no data: ${n}/x${sp}
		else
			
			size_param  # this converts the current value of size param and returns as _sp

			if [[ $sp != $_sp ]] && [[ -d ${n}/x${sp} ]] ;then
				mv ${n}/x${sp} ${n}/x${_sp}

			fi
			
		fi

		for nr in ${real_ref[@]}; do
			
			if [[ ! -d ${n}/x${_sp}/${nr} ]] && [[ ! -d ${n}/x${_sp}/${_nr} ]]; then 
				continue
				echo no data ${n}/x${_sp}/${nr}
			else
				
				n_real
				#echo " _nr = $_nr "
				if [[ $nr != $_nr ]] && [[ -d ${n}/x${_sp}/${nr} ]]; then					
					mv ${n}/x${_sp}/${nr} ${n}/x${_sp}/${_nr}
				fi

			fi
			
			for ni in ${img_ref[@]}; do
				if [[ ! -d ${n}/x${_sp}/${_nr}/${ni} ]] && [[ ! -d ${n}/x${_sp}/${_nr}/${_ni} ]] ; then
					continue
					echo no data: ${n}/x${_sp}/${_nr}/${ni}
				else
					
					n_img
					#echo " _ni = $_ni"
					if [[ $ni != $_ni ]] && [[ -d ${n}/x${_sp}/${_nr}/${ni} ]] ;then					
						mv ${n}/x${_sp}/${_nr}/${ni} ${n}/x${_sp}/${_nr}/${_ni}
					fi

				fi
				
				### Now Converting t-matrix output files' names. From old styles to new style.
				for i in $(seq 1 25); do
		
					#echo file is mt_${i}_${n}_${sp}_${nr}_${ni}.dat
					for x in $sp $_sp; do
						for xnr in $nr $_nr; do
							for xni in $ni $_ni; do

								mt=mt_${i}_${n}_${x}_${xnr}_${xni}.dat
								mt_ancient=mt_${i}_${n}_${x}.dat # Some files still have such names " mt_1_256_x0437.dat"
								if [[ -f ${n}/x${_sp}/${_nr}/${_ni}/$mt ]]; then
						
									##### Warning! IF $mt exist (old style) then following if is allways True. So it is unnecessary
									##### This does not give an error, so I am keeping it for now, but I think it is safe to take the below code out of if.
									if [[ $mt != mt_${i}_${n}_${_sp}_${_nr}_${_ni}.dat ]];then

										echo "renaming  $mt to mt_${i}_${n}_${_sp}_${_nr}_${_ni}"
										mv -u ${n}/x${_sp}/${_nr}/${_ni}/$mt ${n}/x${_sp}/${_nr}/${_ni}/mt_${i}_${n}_${_sp}_${_nr}_${_ni}.dat
									 										
									fi
						
								elif [[ -f ${n}/x${_sp}/${_nr}/${_ni}/$mt_ancient ]]; then
									echo " \e[91mAncient names detected in this file\e[0m \e[7m${n}/x${_sp}/${_nr}/${_ni}/$mt_ancient \e[27m. ALL BEING RENAMED "
									mv -u ${n}/x${_sp}/${_nr}/${_ni}/$mt_ancient ${n}/x${_sp}/${_nr}/${_ni}/mt_${i}_${n}_${_sp}_${_nr}_${_ni}.dat
								else
									
									continue

								fi
							done
						done
					done
					
				done
			done
		done
	done
done
			
