#!/usr/bin/env python

import rospy
from rosberry_experiments.msg import StampedMessage
import time
import sys

N_MESSAGES = 1000
RATE = None

def talker():
    pub = rospy.Publisher('chatter_m', StampedMessage, queue_size=N_MESSAGES)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(RATE)
    for i in xrange(N_MESSAGES):
        hello_str = "hello world"
        timestamp = rospy.get_rostime()
        pub.publish(id=i, t=timestamp, message=hello_str)

        rate.sleep()

def main():
    global RATE
    RATE = int(sys.argv[1])
    print RATE, N_MESSAGES
    try:
        talker()
        rospy.sleep(5)
    except rospy.ROSInterruptException:
        print "Exception: ROSInterruptException"


if __name__ == '__main__':
    main()
