
START=500
TOP=1000
STEP=500


for ((i=$START; i<=$TOP; i += $STEP))
do
   echo $i
   rosrun rosberry_experiments test_latency_main.py 1000 $i
done
