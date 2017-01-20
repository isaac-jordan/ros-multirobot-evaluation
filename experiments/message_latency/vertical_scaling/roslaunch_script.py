import roslaunch
import time


def startNodes():
	print("Starting roslaunch Python script")
	launch = roslaunch.scriptapi.ROSLaunch()
	launch.start()

	print("Creating machine objects")

	sender = Machine("sender", "ros_root",
		"ros_package_path", "rosworker1",
		user="pi", password="raspberry")

	echoer = Machine("echoer", "ros_root",
		"ros_package_path", "rosworker1",
		user="pi", password="raspberry")

	print("Reading arguments")

	number_of_nodes = int(sys.argv[2])
	if n % 2 != 0:
		print("Number of nodes is not even! Exiting.")
		return

	message_frequency = int(sys.argv[3])

	bag_name = sys.argv[4]

	current_run = int(sys.argv[5])

	running_echoers = Set()
	running_senders = Set()

	print("Starting {} nodes...".format(number_of_nodes))

	for n in range(number_of_nodes / 2):
		# Create an echoer node
		echoerNode = Node("rosberry_experiments",
			"test_latency_echo_sensor.py",
			name="echoer_"+n, machine_name="echoer",
			required=True,
			args="{} {} {} {} {}".format(message_frequency, number_of_nodes, n, bag_name, current_run))

		# Create a sender node
		senderNode = Node("rosberry_experiments",
			"test_latency_main_sensor.py",
			name="sender_"+n, machine_name="sender",
			required=True,
			args="{} {} {} {} {}".format(message_frequency, number_of_nodes, n, bag_name, current_run))

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
	print("Exiting roslaunch Python script.")

if __name__ == "__main__":
	startNodes()
