#!/bin/bash# Define list of arguments for the job

readarray -t jobs < "../repo/parameter_cards/card_list_test.txt"

# Define the script name
script="alex_jobsub" # Loop through each index in the jobs array

i=0
for index in "${!jobs[@]}"; do
    # Get the argument corresponding to the current index
    job="${jobs[i]}"    # Generate submit file for each job
    submit_file="${script}_${i}.sub"
    echo "executable  = alex_jobsub.sh" > "$submit_file"
    echo "arguments   = $job" >> "$submit_file"
    echo "universe    = vanilla" >> "$submit_file"
    echo "output      = ${script}_${i}.out" >> "$submit_file"
    echo "error       = ${script}_${i}.err" >> "$submit_file"
    echo "log         = ${script}_${i}.log" >> "$submit_file"
    echo "queue" >> "$submit_file"    # Submit the job
    condor_submit "$submit_file"
    echo "Job submitted with dat file: $job"
    i=$((i + 1))
done
