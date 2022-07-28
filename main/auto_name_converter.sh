#!/bin/bash
set -e
#set -x
# We will read the name of the directories each step
# At the top level directories named as monomer numbers
# Second level directories should be named as x[size_parameter] where 
    # size_parameter is 5 digit without dot
# The third level is n_r which should be three digits
# The Fourth level directories named as n_i with 5 digits

# To fix any non-standard names one of the output file 
    # inside the lowest level directories will be read. 

# Recursively looping through the nested directories to read the output files
for N in */; do
    N="${N/\//}"
    for dir_xm in "$N"/*/; do
        dir_xm="${dir_xm}"
        # echo "$dir_xm"
        # Directory names for size parameter start with "x" always, even the old output files
        # Let's extract the diretory names inside N/ to find the output files only
        dir_name=${dir_xm/${N}\//}
        # Only the ones start with "x" are output files. Skip the others
        if [ "${dir_name:0:1}" != "x" ]; then continue; fi
        # check if dir_xm is empty ignoring hidden files. If it is, then move it to a trash_folder for safety
        if [ ! "$(ls -A "$dir_xm")" ]; then # This tests if folder contains any file or subfolder
            # To store the empty files safely create a trash bin
            [ ! -s "$N/empty_folders" ] && {
                mkdir "$N/empty_folders" && echo "empty folder created"
                } || echo "empty folder already exist" # if not exist then create empty_folders
            # Move the empty file to empty_folders
            mv "$dir_xm" "$N/empty_folders"
            continue
        #If not then move on to next level
        else
            for dir_nr in "${dir_xm}"*/; do
                #  only numeric named folders are correct directories.
                # except the "x" in the dir_xm (e.g. x06400)
                # Skip the folders if their names are not numeric

                # convert directory name to a numeric id 
                numeric_dir_id=${dir_nr//\//}
                numeric_dir_id=${numeric_dir_id/x/}
                re='^[0-9]+$'
                if ! [[ $numeric_dir_id =~ $re ]] ; then
                    echo "skipping the directory: ${numeric_dir_id}"
                    continue
                fi

                # check if dir_nr is empty ignoring hidden files. If it is, then skip
                if [ ! "$(ls -A "$dir_nr")" ]; then
                    # To store the empty files safely create a trash bin
                    [ ! -s "${dir_xm}empty_folders" ] && mkdir "${dir_xm}empty_folders" # if not exist then create empty_folders
                    # Move the empty file to empty_folders
                    mv "$dir_nr" "${dir_xm}empty_folders" &&\
                             echo "${dir_nr} was empty. Moved to empty_folders"
                    continue
                #If not then move on to next level
                else
                    for dir_ni in "${dir_nr}"*/; do
                        # Skip the folders if their names are not numeric

                        # convert directory name to a numeric id 
                        numeric_dir_id=${dir_ni//\//}
                        numeric_dir_id=${numeric_dir_id/x/}
                        re='^[0-9]+$'
                        if ! [[ $numeric_dir_id =~ $re ]] ; then
                            echo "skipping the directory: ${numeric_dir_id}"
                            continue
                        fi

                        # check if n_i contains any output file (".dat" files)
                        if [ ! "$(ls "$dir_ni"*dat)" ]; then # note the nested double quote. Allowed with command substitutions $(...)
                            # To store the empty files safely create a trash bin
                            [ ! -s "${dir_nr}empty_folders" ] && mkdir "${dir_nr}empty_folders" # if not exist then create empty_folders
                            # Move the empty file to empty_folders
                            mv "$dir_ni" "${dir_nr}empty_folders" &&\
                             echo "${dir_ni} was empty. Moved to empty_folders"
                            continue
                        #else select an output file
                        else
                            # creating correct formats
                            # echo "creating the correct formats"
                            mapfile -t files < <(ls "${dir_ni}"*dat)
                            output=${files[0]} # select the largest file
                            #output=("$output")
                            # echo " output is $output"
                            #reading the monomer number from
                            line=($(head -n 18 "$output" | tail -n 1)) # read line 18 into an array
                            # n=${line[0]} # The first element is the monomer number
                            # reading the length, ref. indx. scale factors:
                            line=($(head -n 24 "$output" | tail -n 1))
                            xm=${line[0]}; nr=${line[1]}; ni=${line[2]}
                            # use python to convert the number to standard lengths
                            xm=$(python -c "print('{:.4f}'.format($xm))")
                            nr=$(python -c "print('{:.2f}'.format($nr))")
                            ni=$(python -c "print('{:.4f}'.format($ni))")

                            # next line will remove the "." from the variables.
                            x_m=${xm/./}; n_r=${nr/./}; n_i=${ni/./}

                            # print the new formats
                            echo "new formats: xm: $x_m  nr: $n_r  ni: $n_i"
                            # Rename the output files and the directories
                            
                            # Renaming the output files
                            for file in "${files[@]}"; do
                                # Output files named in this format
                                # mt_$run_id_$N_$xm_$nr_$ni.dat
                                # where run_id refers to position file with the same id.
                                # Incase the file name does not follow the standards the following part will fix it
                                
                                # Let's convert the output file name to an array
                                # Set IFS to "_" to separate the file name by _
                                IFS=_ read -ra name_arr <<<"$file"
                                IFS='
                                '
                                # The second element is the run_id
                                run_id=${name_arr[1]}
                                xm_old=${name_arr[3]}
                                nr_old=${name_arr[4]}
                                ni_old=${name_arr[5]}
                                ni_old=${ni_old/.dat/}
                            #     echo "
                            
                            #     Sanity Check
                            #     file name: $file
                            #     run_id = $run_id
                            #     ni_old: $ni_old  n_i: $n_i
                            #     nr_old: $nr_old  n_r: $n_r
                            #     xm_old: $xm_old  x_m: $x_m
                                
                            #     dir_ni: $dir_ni  new_dir: ${dir_nr}$n_i
                            #     dir_nr: $dir_nr  new_dir: ${dir_xm}$n_r
                            #     dir_xm: $dir_xm  new_dir: ${N}/x${x_m}
                            
                            # "    
                                
                                # if output name is already correct then skip
                                # [ "$xm_old" == "$x_m" ] && [ "$nr_old" == "$n_r" ] && [ "$ni_old" == "$n_i" ] && continue
                                [ "$file" == "$dir_ni"mt_"${run_id}"_"${N}"_"${x_m}"_"${n_r}"_"${n_i}".dat ] && continue
                                # Now rename the file
                                # echo moving "$file" to "$dir_ni"mt_"${run_id}"_"${N}"_"${x_m}"_"${n_r}"_"${n_i}".dat 
                                echo "Renaming the file to mt_"${run_id}"_"${N}"_"${x_m}"_"${n_r}"_"${n_i}".dat "
                                mv -n "$file" "$dir_ni"mt_"${run_id}"_"${N}"_"${x_m}"_"${n_r}"_"${n_i}".dat 
                            done
                        
                            # Renaming the directories which are in the following format
                            # dir_ni: N/xm/nr/ni/; dir_nr: N/xm/nr/; dir_xm: N/xm
                            IFS='/'
                            read -ra name_arr <<<"$dir_ni"
                            IFS='
                                '
                            xm_old=${name_arr[1]}
                            xm_old=${xm_old/x/}

                            nr_old=${name_arr[2]}
                            ni_old=${name_arr[3]}

                            echo "
                            
                            Sanity Check
                                ni_old: $ni_old  n_i: $n_i
                                nr_old: $nr_old  n_r: $n_r
                                xm_old: $xm_old  x_m: $x_m
                                
                                dir_ni: $dir_ni  new_dir: ${dir_nr}$n_i
                                dir_nr: $dir_nr  new_dir: ${dir_xm}$n_r
                                dir_xm: $dir_xm  new_dir: ${N}/x${x_m}
                            
                            " >> log_sanity_check.txt

                            # Renaming the directory ni
                            # Sometimes same directory name with correct format already exist
                            # eg. for nr=0.226 there may be two directories with the name 0226 and 023
                            # The wrong format 023 should not be renamed but files in it should be moved into 0226
                            # Let s do this:
                            # # If the dir with correct name doesn't exist and the current directory name is 
                            # wrong then rename the directory 
                            if [ ! -s "${dir_nr}$n_i" ]; then
                                [ "$ni_old" != "$n_i" ] &&\
                                    mv -vui "$dir_ni" "${dir_nr}$n_i"
                            # else the dir with correct name exist and the current directory name is 
                            # wrong then move all the current directory contains in to the one with correct name
                            elif [ -s "${dir_nr}$n_i" ]; then 
                                [ "$ni_old" != "$n_i" ] &&\
                                    mv -vui "$dir_ni"/* "${dir_nr}$n_i"
                            fi
                            # echo " All Done"
                        fi
                    done
                    # Renaming the directory nr
                    echo "Renaming directory at nr level" 

                    # # If the dir with correct name doesn't exist and the current directory name is 
                    # wrong then rename the directory
                    
                    if [ ! -s "${dir_xm}$n_r" ]; then
                        [ "$nr_old" != "$n_r" ] &&\
                            mv -vui "$dir_nr" "${dir_xm}$n_r" 
                    # If the dir with correct name exist and the current directory name is 
                    # wrong then move all the current directory contains in to the one woth correct name
                    elif [ -s "${dir_xm}$n_r" ]; then 
                        [ "$nr_old" != "$n_r" ] &&\
                            mv -vui "$dir_nr"/* "${dir_xm}$n_r"
                    fi
                fi
            done
            echo "moving directory at xm level"
            echo "$xm_old =? $x_m " 
            echo " $dir_xm =?  ${N}/x${x_m}"
            # # If the dir with correct name doesn't exist and the current directory name is 
            # wrong then rename the directory
            if [ ! -s "${N}/x${x_m}" ]; then 
                [ "$xm_old" != "$x_m" ] &&\
                    mv -vui "$dir_xm" "${N}/x${x_m}"
            # If the dir with correct name exist and the current directory name is 
            # wrong then move all the current directory contains in to the one with correct name
            elif [ -s "${N}/x${x_m}" ]; then 
                [ "$xm_old" != "$x_m" ] &&\
                    mv -vui "$dir_xm"/* "${N}/x${x_m}"
            fi
        fi
    done
done