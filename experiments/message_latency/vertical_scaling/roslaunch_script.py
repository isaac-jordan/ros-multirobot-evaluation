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
	launch = roslaunch.scriptapi.ROSLaunch()
	launch.start()
	print("Launch parent: " + str(launch.parent))
	print("Remote runner: " + str(launch.parent.remote_runner))

	launch.parent._init_remote()
	print("Remote runner: " + str(launch.parent.remote_runner))

	launch.parent.remote_runner = roslaunch.remote.ROSRemoteRunner(launch.parent.run_id, launch.parent.config, launch.parent.pm, launch.parent.server)
	print("Remote runner WHYY: " + str(launch.parent.remote_runner))

	print("Creating machine objects")
	sender = roslaunch.core.Machine("sender", "192.168.2.105",
		env_loader="/home/pi/isaac-project-l4/experiments/message_latency/vertical_scaling/devel/setup.sh",
		user="pi", password="raspberry")

	echoer = roslaunch.core.Machine("echoer", "192.168.2.183",
		env_loader="/home/pi/isaac-project-l4/experiments/message_latency/vertical_scaling/devel/setup.sh",
		user="pi", password="raspberry")

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

	print("Starting {} nodes...".format(number_of_nodes))

	for n in range(number_of_nodes / 2):
		# Create an echoer node
		echoerNode = roslaunch.core.Node("rosberry_experiments",
			"test_latency_echo_sensor.py",
			name="echoer_"+str(n), machine_name="echoer",
			required=True,
			args="{} {} {} {} {}".format(message_frequency, number_of_nodes, n, bag_name, current_run))
		echoerNode.machine = echoer

		# Create a sender node
		senderNode = roslaunch.core.Node("rosberry_experiments",
			"test_latency_main_sensor.py",
			name="sender_"+str(n), machine_name="sender",
			required=True,
			args="{} {} {} {} {}".format(message_frequency, number_of_nodes, n, bag_name, current_run))
		senderNode.machine = sender

		echoerProcess = launch.launch(echoerNode)
		running_echoers.add(echoerProcess)

		senderProcess = launch.launch(senderNode)
		running_senders.add(senderProcess)

	while len(running_senders) > 0:
		print("Waiting on {} senders to finish".format(len(running_senders)))
		running_senders_copy = [x for x in running_senders]
		for senderProcess in running_senders_copy:
			if not senderProcess.is_alive():
				running_senders.remove(senderProcess)

		time.sleep(5)

	launch.stop()
	print("Stopping roscore")
	roscore.terminate()

	print("Exiting roslaunch Python script.")

if __name__ == "__main__":
	startNodes()
