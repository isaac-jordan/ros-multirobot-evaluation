#!/usr/bin/env python

import rospy
from rosberry_experiments.msg import StampedLaserScan
import time
import sys

N_MESSAGES = 1000

def listener(msg, args):
    pub = args[0]
    pub.publish(msg)

def main():
    RATE = int(sys.argv[1])
    N_NODES = int(sys.argv[2])
    N_NODE = int(sys.argv[3])
    BAG_FILE_NAME = int(sys.argv[4])
    rospy.init_node('echoer_'+N_NODE, anonymous=True)
    pub = rospy.Publisher('echoer_publisher_'+N_NODE, StampedLaserScan, queue_size=N_MESSAGES)
    sub = rospy.Subscriber("chatter_publisher_"+N_NODE, StampedLaserScan, listener, callback_args=[pub])
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        print "Exception: ROSInterruptException"

if __name__ == '__main__':
    main()
