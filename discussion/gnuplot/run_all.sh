command="gnuplot plotter_exp1_msg_latency_10khz.txt"
echo ">>"$command"<<"
$command

command="gnuplot plotter_exp1_msg_latency_100khz.txt"
echo ">>"$command"<<"
$command

command="gnuplot plotter_exp1_msg_latency_1000khz.txt"
echo ">>"$command"<<"
$command

command="gnuplot plotter_exp1_msg_latency_two_10khz.txt"
echo ">>"$command"<<"
$command

command="gnuplot plotter_exp1_msg_latency_two_100khz.txt"
echo ">>"$command"<<"
$command

command="gnuplot plotter_exp1_msg_latency_two_1000khz.txt"
echo ">>"$command"<<"
$command

command="gnuplot plotter_exp1_msg_latency_restart_10khz.txt"
echo ">>"$command"<<"
$command

command="gnuplot plotter_exp1_msg_latency_restart_100khz.txt"
echo ">>"$command"<<"
$command

command="gnuplot plotter_exp1_msg_latency_restart_1000khz.txt"
echo ">>"$command"<<"
$command

command="gnuplot plotter_exp1_msg_latency_full_restart.txt"
echo ">>"$command"<<"
$command

command="gnuplot plotter_exp1_msg_latency_partial_restart.txt"
echo ">>"$command"<<"
$command



for f in *.eps; do
	epstopdf $f
	rm $f
done
