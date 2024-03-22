#!/bin/bash# Define list of arguments for the job

readarray -t jobs < "../Noether/card_list_fermion_0.33.txt"

mkdir -p condor_out

# Define the script name

i=0
for index in "${!jobs[@]}"; do
    extracted_str=$(echo "$job" | tr "/" "_")
    #extracted_str=$(echo "$extracted_str" | tr "fermion/" "_")
    #extracted_str=$(echo "$extracted_str" | tr ".dat" "_")

    extracted_str=$(echo "${extracted_str/scalar/}")
    extracted_str=$(echo "${extracted_str/fermion/}")
    extracted_str=$(echo "${extracted_str/.dat/}")
    echo $extracted_str
    script="node${extracted_str}" # Loop through each index in the jobs array

    # Get the argument corresponding to the current index
    job="${jobs[i]}"    # Generate submit file for each job
    submit_file="${script}.sub"
    echo "executable     = node_setup.sh" > "$submit_file"
    echo "arguments      = $job" >> "$submit_file"
    echo "universe       = vanilla" >> "$submit_file"
    echo "output         = condor_out/${script}.out" >> "$submit_file"
    echo "error          = condor_out/${script}.err" >> "$submit_file"
    echo "log            = condor_out/${script}.log" >> "$submit_file"
    echo "request_memory = 1 GB" >> "$submit_file"
    echo "queue" >> "$submit_file"    # Submit the job
    condor_submit "$submit_file"
    echo "Job submitted with dat file: $job"
    i=$((i + 1))
done

mv *.sub condor_out/
