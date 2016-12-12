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
    rospy.init_node('talker1', anonymous=True)
    pub = rospy.Publisher('chatter_s', StampedLaserScan, queue_size=N_MESSAGES)
    sub = rospy.Subscriber("chatter_m", StampedLaserScan, listener, callback_args=[pub])
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        print "Exception: ROSInterruptException"

if __name__ == '__main__':
    main()
