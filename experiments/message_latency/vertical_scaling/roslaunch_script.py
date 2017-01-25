import roslaunch
import roslaunch.remote
import time, sys, subprocess
from sets import Set
import rospy
import std_msgs.msg
import datetime

NODES_STILL_RUNNING = Set()

LAST_TIME_NODES_STILL_RUNNING_CHANGED = datetime.datetime.now()

def listener(msg):
    str_n = msg.data
    NODES_STILL_RUNNING.remove(int(str_n))
	LAST_TIME_NODES_STILL_RUNNING_CHANGED = datetime.datetime.now()
    print("Node " + str_n + " has finished.")

def startNodes():
	print("Starting roslaunch Python script")

	print("Starting roscore")
	roscore_popen_file = open("roscore_popen.log", "w+")
	roscore_popen_err_file = open("roscore_popen_err.log", "w+")
	roscore = subprocess.Popen('roscore', stdout=roscore_popen_file, stderr=roscore_popen_err_file)
	time.sleep(2)  # wait a bit to be sure the roscore is really launched

	print("Starting roslaunch")
	uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
  	roslaunch.configure_logging(uuid)

	config = roslaunch.config.ROSLaunchConfig()

	print("Creating machine objects")
	sender = roslaunch.core.Machine("sender", "rosworker1",
		env_loader="/home/pi/2016-level4-isaac/experiments/message_latency/vertical_scaling/env_loader.sh",
		user="pi", password="raspberry")
	config.add_machine(sender)

	echoer = roslaunch.core.Machine("echoer", "rosworker2",
		env_loader="/home/pi/2016-level4-isaac/experiments/message_latency/vertical_scaling/env_loader.sh",
		user="pi", password="raspberry")
	config.add_machine(echoer)

	print("Reading arguments")

	message_frequency = int(sys.argv[1])
	number_of_nodes = int(sys.argv[2])
	if number_of_nodes % 2 != 0:
		print("Number of nodes is not even! Exiting.")
		return

	bag_name = sys.argv[3]
	current_run = int(sys.argv[4])
	output_dir = sys.argv[5]

	running_echoers = Set()
	running_senders = Set()

	print("Creating {} nodes...".format(number_of_nodes))
	rospy.init_node('big_daddy', anonymous=True)

	for n in range(number_of_nodes / 2):
		# Create an echoer node
		echoerNode = roslaunch.core.Node("rosberry_experiments",
			"test_latency_echo_sensor.py",
			name="echoer_"+str(n), machine_name="echoer",
			required=False,
			args="{} {} {} {} {} {}".format(message_frequency, number_of_nodes, n, bag_name, current_run, output_dir))

		# Create a sender node
		senderNode = roslaunch.core.Node("rosberry_experiments",
			"test_latency_main_sensor.py",
			name="sender_"+str(n), machine_name="sender",
			required=False,
			args="{} {} {} {} {} {}".format(message_frequency, number_of_nodes, n, bag_name, current_run, output_dir))

		#echoerProcess = launch.launch(echoerNode)
		#running_echoers.add(echoerProcess)
		config.add_node(echoerNode)

		#senderProcess = launch.launch(senderNode)
		#running_senders.add(senderProcess)
		config.add_node(senderNode)
		NODES_STILL_RUNNING.add(n)
		rospy.Subscriber("chatter_finished_publisher_"+str(n), std_msgs.msg.String, listener)

	launch = roslaunch.scriptapi.ROSLaunch()
	launch.start()

	#launch.parent.remote_runner = roslaunch.remote.ROSRemoteRunner(launch.parent.run_id, launch.parent.config, launch.parent.pm, launch.parent.server)
	#launch.parent.start()
	config.assign_machines()
	launch.parent.config = config
	launch.parent.start()

	print("All remote processes: " + str([x.get_info() for x in launch.parent.remote_runner.remote_processes]))

	all_procs = [x for x in launch.parent.remote_runner.remote_processes]
	while len(NODES_STILL_RUNNING) > 0 and len(all_procs) / 2 > 0:
		all_procs_copy = [x for x in all_procs]
		for proc in all_procs_copy:
			if not proc.is_alive():
				all_procs.remove(proc)

		print("Waiting on {} senders to finish, {} processes still alive.".format(len(NODES_STILL_RUNNING), len(all_procs)))
		time.sleep(5)

		d = LAST_TIME_NODES_STILL_RUNNING_CHANGED - datetime.datetime.now()
		if d.total_seconds() > 60 * 60:
			print("ERROR: Count of nodes still running hasn't changed in an hour. Killing.")
			break

	print("All done. Stopping roslaunch.")
	launch.stop()
	print("Stopping roscore")
	roscore.terminate()

	print("Exiting roslaunch Python script.")

if __name__ == "__main__":
	startNodes()
