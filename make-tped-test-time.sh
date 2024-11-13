#!/bin/bash

# Function to run the command and check for success
run_command() {
    local output_name=$1
    local success=0
    local start_time=$(date +%s)

    while [ $success -eq 0 ]; do
        # Run the command in the background
        env COSI_NEWSIM=1 COSI_MAXATTEMPTS=1000000 coalescent -p test.par -v -g --genmapRandomRegions --drop-singletons .25 --tped ${output_name} -n 1 -M -m -r 0 &
        local cmd_pid=$!

        # Wait for the command to finish or timeout after 5 minutes
        local timeout=90
        local elapsed=0
        while kill -0 $cmd_pid 2>/dev/null; do
            sleep 1
            elapsed=$((elapsed + 1))
            if [ $elapsed -ge $timeout ]; then
                echo "Command running too long, killing process..."
                kill -9 $cmd_pid
                break
            fi
        done

        # Check if the command succeeded
        if wait $cmd_pid; then
            success=1
        else
            echo "Run failed for ${output_name}, retrying..."
        fi
    done

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    echo "Run for ${output_name} took ${duration} seconds" >> run_log.txt
}

# Start total time tracking
total_start_time=$(date +%s)

# Loop to run the command for each output name from 1 to 100
for a in $(seq 1 100); do
    output_name="hap.${a}"
    run_command $output_name
done

# End total time tracking
total_end_time=$(date +%s)
total_duration=$((total_end_time - total_start_time))
echo "Total time for all runs: ${total_duration} seconds" >> run_log.txt
