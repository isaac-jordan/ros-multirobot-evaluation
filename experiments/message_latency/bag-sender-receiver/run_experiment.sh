#!/bin/bash

RESULTS_FOLDER="results/experiment_6_real_wifi/wifi/sensor"

LOWEST_FREQ=200
HIGHEST_FREQ=2000
FREQ_STEP=200
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

git add .
git commit -m "Added experimental data for Experiment 5 and 6. Some modifications to code were required."
git pull
git push
