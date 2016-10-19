#!/usr/bin/env python

import rospy
from rosberry_experiments.msg import StampedMessage
import time
import sys


N_MESSAGES = 1000
f = None

def listener(msg):
    recv_time = rospy.get_rostime()
    sent_time = msg.t
    f.write(str(msg.id) + "," + str(sent_time) + "," + str(recv_time) + "\n")

def main():
    global f
    RATE = int(sys.argv[1])
    print RATE, N_MESSAGES
    f = open("times_"+str(RATE)+".csv", "w+")
    rospy.init_node('listener', anonymous=True)

    try:
        sub = rospy.Subscriber("chatter_s", StampedMessage, listener)

        rospy.spin() # Needs to be shutdown manually
    except rospy.ROSInterruptException:
        print "Exception: ROSInterruptException"

    f.close()


if __name__ == '__main__':
    main()
