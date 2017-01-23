import roslaunch
import roslaunch.remote
import time, sys, subprocess
from sets import Set

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

	running_echoers = Set()
	running_senders = Set()

	print("Creating {} nodes...".format(number_of_nodes))

	for n in range(number_of_nodes / 2):
		# Create an echoer node
		echoerNode = roslaunch.core.Node("rosberry_experiments",
			"test_latency_echo_sensor.py",
			name="echoer_"+str(n), machine_name="echoer",
			required=True,
			args="{} {} {} {} {}".format(message_frequency, number_of_nodes, n, bag_name, current_run))

		# Create a sender node
		senderNode = roslaunch.core.Node("rosberry_experiments",
			"test_latency_main_sensor.py",
			name="sender_"+str(n), machine_name="sender",
			required=False,
			args="{} {} {} {} {}".format(message_frequency, number_of_nodes, n, bag_name, current_run))

		#echoerProcess = launch.launch(echoerNode)
		#running_echoers.add(echoerProcess)
		config.add_node(echoerNode)

		#senderProcess = launch.launch(senderNode)
		#running_senders.add(senderProcess)
		config.add_node(senderNode)

	launch = roslaunch.scriptapi.ROSLaunch()
	launch.start()

	#launch.parent.remote_runner = roslaunch.remote.ROSRemoteRunner(launch.parent.run_id, launch.parent.config, launch.parent.pm, launch.parent.server)
	#launch.parent.start()
	config.assign_machines()
	launch.parent.config = config
	launch.parent.start()

	running_senders = [x for x in launch.parent.remote_runner.remote_processes if "sender" in x.get_info()["name"]]
	print("Running senders: " + str(running_senders))
	print("All remote processes: " + str([x.get_info() for x in launch.parent.remote_runner.remote_processes]))

	while len(running_senders) > 0:
		print("Waiting on {} senders to finish".format(len(running_senders)))
		running_senders_copy = [x for x in running_senders]
		for senderProcess in running_senders_copy:
			if not senderProcess.is_alive():
				running_senders.remove(senderProcess)

		time.sleep(5)

	print("All done. Stopping roslaunch.")
	launch.stop()
	print("Stopping roscore")
	roscore.terminate()

	print("Exiting roslaunch Python script.")

if __name__ == "__main__":
	startNodes()
