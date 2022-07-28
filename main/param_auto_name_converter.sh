# Properly create a list of files in the directory files=$(ls *dat) could cause problems
echo "Do you want to rename the old runs or new runs?"
echo "Type 'old' or 'new'"
read -r model
if [ "$model" == "new" ]; then
    mdl="newpm"
elif [ "$model" == "old" ]; then
    mdl="param"
else
    echo "Invalid argument. Type either 'new' or 'old' "
    return 1 2>>/dev/null
    exit 1
fi

cd ./"$model" >>/dev/null || echo " No such folder as $model " 

mapfile -t files < <(ls *dat)

# Renaming the output files
for file in "${files[@]}"; do
    # Output files named in this format
    # {model}$N_$xm_$nr_$ni.dat {model} is param or newpm
    # Incase the file name does not follow the standards the following part will fix it

    # Let's convert the output file name to an array
    # Set IFS to "_" to separate the file name by _
    IFS=_ read -ra name_arr <<<"$file"
    IFS='
    '
    # name_arr = (param1024 01680 130 00020.dat)
    N=${name_arr[0]}
    N=${N/"$mdl"/}
    xm_old=${name_arr[1]}
    nr_old=${name_arr[2]}
    ni_old=${name_arr[3]}
    ni_old=${ni_old/.dat/}

    # The variables named without decimal points, we will add them now
    # Luckily all the variables are less than 10, so we put "." right after the first digit
    xm="${xm_old:0:1}"".""${xm_old:1}" # e.g. xm_old = 006, xm = 0.06 
    nr="${nr_old:0:1}"".""${nr_old:1}"
    ni="${ni_old:0:1}"".""${ni_old:1}" 
    # use python to convert the number to standard lengths

    # IDL converts 0.9600 to 0.9598 so name the files accordingly.
    # fix is simple as follows:
    xm=$(python -c "print('{:.3f}'.format($xm))")
    xm=$(python -c "print('{:.4f}'.format($xm))")
    
    nr=$(python -c "print('{:.2f}'.format($nr))")
    ni=$(python -c "print('{:.4f}'.format($ni))")

    # Now convert them as string without decimal separator
    xm=${xm/./}
    nr=${nr/./}
    ni=${ni/./}
    # Print to see if it works

    # if output name is already correct then skip
    [ "$file" == "$mdl""${N}""_""${xm}""_""${nr}""_""${ni}".dat ] && continue
    
    echo "
        
            Sanity Check
            file name: $file
            N: $N
            ni_old: $ni_old  ni: $ni
            nr_old: $nr_old  nr: $nr
            xm_old: $xm_old  xm: $xm 

            new formats: xm: $xm  nr: $nr  ni: $ni
            "

    # Rename the files

    # Now rename the file
    new_name="$mdl""${N}""_""${xm}""_""${nr}""_""${ni}".dat
    echo "Renaming the file to $new_name "
    mv -n "$file" "$new_name"
done