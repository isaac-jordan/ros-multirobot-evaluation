#!/usr/bin/env python

import rospy
import rosbag
from rosberry_experiments.msg import StampedLaserScan
import time
import sys

N_MESSAGES = 1000
RATE = None
f = None

def listener(msg):
    recv_time = rospy.get_rostime()
    sent_time = msg.t
    f.write(str(msg.id) + "," + str(sent_time) + "," + str(recv_time) + "\n")

def talker():
    pub = rospy.Publisher('chatter_m', StampedLaserScan, queue_size=N_MESSAGES)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(RATE)
    bag = rosbag.Bag(sys.argv[2])
    # Topics in realistic-dataset.bag are '/base_scan' and '/camera/rgb/image_raw'

    i = 0
    for topic, msg, t in bag.read_messages(topics=["/base_scan"]):
        timestamp = rospy.get_rostime()
        pub.publish(id=i, t=timestamp, message=msg)
        i += 1
        rate.sleep()

def main():
    global RATE, f
    RATE = int(sys.argv[1])
    f = open("times_"+str(RATE)+".csv", "w+")
    print RATE, N_MESSAGES
    try:
        sub = rospy.Subscriber("chatter_s", StampedLaserScan, listener)
        talker()
        rospy.sleep(5)
        f.close()

    except rospy.ROSInterruptException:
        print "Exception: ROSInterruptException"


if __name__ == '__main__':
    main()
