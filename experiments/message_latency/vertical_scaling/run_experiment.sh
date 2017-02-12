#!/bin/bash
set -x

RESULTS_FOLDER="results/experiment_8_vertical_scaling"

FREQUENCY_OVERRIDE=(20 10 1)

LOWEST_FREQ=100
HIGHEST_FREQ=300
FREQ_STEP=100

LOWEST_N_NODES=2
HIGHEST_N_NODES=256
N_NODES_MULTIPLIER=2

N_RUNS=3

mkdir $RESULTS_FOLDER -p

for((CURRENT_RUN=1;$CURRENT_RUN<=$N_RUNS;++CURRENT_RUN)) do
	echo "On run number: $CURRENT_RUN"
	RUN_FOLDER="$RESULTS_FOLDER/run_$CURRENT_RUN/"
	mkdir -p $RUN_FOLDER

	for CURRENT_FREQ in $FREQUENCY_OVERRIDE; do
	#for((CURRENT_FREQ=$LOWEST_FREQ;$CURRENT_FREQ<=$HIGHEST_FREQ;CURRENT_FREQ=$((CURRENT_FREQ+FREQ_STEP)))) do
		for((CURRENT_N_NODES=$LOWEST_N_NODES;$CURRENT_N_NODES<=$HIGHEST_N_NODES;CURRENT_N_NODES=$((CURRENT_N_NODES*N_NODES_MULTIPLIER)))) do
			echo "Running $CURRENT_N_NODES at message frequency: $CURRENT_FREQ Hz"
			#rosrun rosberry_experiments test_latency_main_sensor.py $CURRENT_FREQ ~/realistic-dataset.bag
			CURRENT_DIR=$(dirname $(readlink -f $0))
			python roslaunch_script.py $CURRENT_FREQ $CURRENT_N_NODES /home/pi/realistic-dataset.bag $CURRENT_RUN "$CURRENT_DIR/$RUN_FOLDER"
			echo "Waiting 30 seconds"
			sleep 30
		done
	done
done
