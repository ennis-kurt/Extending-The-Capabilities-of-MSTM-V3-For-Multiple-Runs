#!/bin/bash
set -e
#set -x
# Reading the name of the directories each step
# At the top level directories named as monomer numbers
# Second level directories should be named as x[size_parameter] where ,
    # size_parameter is 5 digit without dot
# The third level is n_r which should be three digits
# The Fourth level directories named as n_i with 5 digits
touch output_list.csv
echo "N,xm,nr,ni">>output_list.csv
# Recursively looping through the nested directories to read the output files
for N in */; do
    N="${N/\//}"
    re='^[0-9]+$'
    if ! [[ $N =~ $re ]] ; then
        echo "skipping the directory: ${N}"
        continue
    fi
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
                            echo "${N},${xm},${nr},${ni}">>output_list.csv
                            
                            # echo " All Done"
                        fi
                    done

                fi
            done
            
        fi
    done
done
