#!/bin/bash

RESULTS_FOLDER="results/experiment_3_cpu"

LOWEST_FREQ=200
HIGHEST_FREQ=2000
FREQ_STEP=200
N_RUNS=3

mkdir $RESULTS_FOLDER -p

for((CURRENT_RUN=1;$CURRENT_RUN<=$N_RUNS;++CURRENT_RUN)) do
	RUN_FOLDER="$RESULTS_FOLDER/run_$CURRENT_RUN/"
	mkdir $RUN_FOLDER -p
	
	for((CURRENT_FREQ=$LOWEST_FREQ;$CURRENT_FREQ<=$HIGHEST_FREQ;CURRENT_FREQ=$((CURRENT_FREQ+FREQ_STEP)))) do
		echo "Running Frequency: $CURRENT_FREQ KHz"
		rosrun rosberry_experiments test_latency_main.py $CURRENT_FREQ
		sleep 15
		mv "times_$CURRENT_FREQ.csv" $RUN_FOLDER
	done
done
