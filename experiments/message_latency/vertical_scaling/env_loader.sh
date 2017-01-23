#!/bin/bash
export ROS_WS=/home/pi/2016-level4-isaac/experiments/message_latency/vertical_scaling
source $ROS_WS/devel/setup.bash
export PATH=$ROS_ROOT/bin:$PATH
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$ROS_WS
