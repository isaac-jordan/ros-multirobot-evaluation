#!/bin/bash

RESULTS_FOLDER="results/experiment_6_real_wifi/wifi_extra/sensor"

LOWEST_FREQ=100
HIGHEST_FREQ=350
FREQ_STEP=50
N_RUNS=3

mkdir $RESULTS_FOLDER -p

for((CURRENT_RUN=1;$CURRENT_RUN<=$N_RUNS;++CURRENT_RUN)) do
	RUN_FOLDER="$RESULTS_FOLDER/run_$CURRENT_RUN/"
	mkdir $RUN_FOLDER -p

	for((CURRENT_FREQ=$LOWEST_FREQ;$CURRENT_FREQ<=$HIGHEST_FREQ;CURRENT_FREQ=$((CURRENT_FREQ+FREQ_STEP)))) do
		echo "Running Frequency: $CURRENT_FREQ Hz"
		rosrun rosberry_experiments test_latency_main_sensor.py $CURRENT_FREQ ~/realistic-dataset.bag
		sleep 15
		mv "times_$CURRENT_FREQ.csv" $RUN_FOLDER
	done
done
