#!/bin/bash
set -e
N=( 64 128 256 512 1024 )
xm=( 032 073 0168 0235 0437 0448 0504 0832 3360 6398 9598 0320 0730 0336 0640 0960 5795 0580 4795 0480 4799 5299 0530 4299 0430 8319 7299 0730)
real_ref=( 13 130 20 200 171 170 166 168 23 230 145 18 180 )
img_ref=( 0002 00226 0023 009 0090 0045 045 03 0300 0006 000438 0004 0001 )


########### functions ###########
size_param ()

{ # this substitue the size parameter
case $sp in
	032)
	    _sp=0320
	    ;;
	073)
	    _sp=0730
	    ;;
	3360)
	    _sp=0336
	    ;;
	4299)
	    _sp=0430
	    ;;
	4795)
	    _sp=0480
	    ;;
	5299)
	    _sp=0530
	    ;;
	5795)
	    _sp=0580
	    ;;
	6398)
	    _sp=0640
	    ;;
	9598)
	    _sp=0960
	    ;;
	8319)
	    _sp=0832
	    ;;
	7299)
	    _sp=0730
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
	 _ni=0023
	;;
	009)
	 _ni=0090
	;;
	03)
	 _ni=0300
	;;
	045)
	 _ni=0045
	;;
	000438)
	 _ni=0004
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
		else
			
			size_param  # this converts the current value of size param and returns as _sp
			#echo "_sp = $_sp and sp = $sp "
			if [[ $sp != $_sp ]] && [[ -d ${n}/x${sp} ]] ;then
				mv ${n}/x${sp} ${n}/x${_sp}
			fi
			
		fi

		for nr in ${real_ref[@]}; do
			
			if [[ ! -d ${n}/x${_sp}/${nr} ]] && [[ ! -d ${n}/x${_sp}/${_nr} ]]; then 
				continue
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
					mt=mt_${i}_${n}_${sp}_${nr}_${ni}.dat
					mt_ancient=mt_${i}_${n}_${sp}.dat # Some files still have such names " mt_1_256_x0437.dat"
					if [[ -f ${n}/x${_sp}/${_nr}/${_ni}/$mt ]]; then
						
						##### Warning! IF $mt exist (old style) then following if is allways True. So it is unnecessary
						##### This does not give an error, so I am keeping it for now, but I think it is safe to take the below code out of if.
						if [[ $mt != mt_${i}_${n}_${_sp}_${_nr}_${_ni}.dat ]];then

							echo "renaming  mt_${i}_* to mt_${i}_${n}_${_sp}_${_nr}_${_ni}"
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
			
