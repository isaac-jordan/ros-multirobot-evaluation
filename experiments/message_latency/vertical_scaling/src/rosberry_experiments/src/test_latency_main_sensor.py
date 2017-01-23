#!/usr/bin/env python

import rospy
import rosbag
from rosberry_experiments.msg import StampedLaserScan
import time
import sys
import os

N_MESSAGES = 1000
N_NODES = None
N_NODE = None
RATE = None
BAG_FILE_NAME = None
f = None

def listener(msg):
    recv_time = rospy.get_rostime()
    sent_time = msg.t
    f.write(str(msg.id) + "," + str(sent_time) + "," + str(recv_time) + "\n")

def talker():
    pub = rospy.Publisher('chatter_publisher_' + str(N_NODE), StampedLaserScan, queue_size=N_MESSAGES)
    rospy.init_node('chatter_'+str(N_NODE), anonymous=True)
    rate = rospy.Rate(RATE)
    bag = rosbag.Bag(BAG_FILE_NAME)
    # Topics in realistic-dataset.bag are '/base_scan' and '/camera/rgb/image_raw'

    i = 0
    for topic, msg, t in bag.read_messages(topics=["/base_scan"]):
        timestamp = rospy.get_rostime()
        pub.publish(id=i, t=timestamp, message=msg)
        i += 1
        rate.sleep()

def main():
    global RATE, N_NODES, N_NODE, BAG_FILE_NAME, f
    RATE = int(sys.argv[1])
    N_NODES = int(sys.argv[2])
    N_NODE = int(sys.argv[3])
    BAG_FILE_NAME = sys.argv[4]
    RUN_NUMBER = int(sys.argv[5])
    outFileName = "times_"+str(RATE)+"_"+str(N_NODES)+"_"+str(N_NODE)+"_"+str(RUN_NUMBER)+".csv"
    f = open(outFileName, "w+")

    print("Output file located at: " + os.path.dirname(os.path.realpath(__file__)))
    print("Current Working Directory: " + os.getcwd())

    try:
        sub = rospy.Subscriber("echoer_publisher_"+str(N_NODE), StampedLaserScan, listener)
        talker()
        rospy.sleep(5)
    except rospy.ROSInterruptException:
        print "Exception: ROSInterruptException"
    f.close()


if __name__ == '__main__':
    main()
