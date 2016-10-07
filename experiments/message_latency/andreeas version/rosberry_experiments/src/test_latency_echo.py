#!/usr/bin/env python
# license removed for brevity
import rospy
from rosberry_experiments.msg import StampedMessage
import time
import sys

RATE = None

def listener(msg, args):
    rate = rospy.Rate(RATE) # 10hz
	pub = args[0]
    pub.publish(msg)
    rate.sleep()

def main():
	global RATE
	RATE = int(sys.argv[1])
	try:
	    rospy.init_node('talker1', anonymous=True)
	    pub = rospy.Publisher('chatter_s', StampedMessage, queue_size=RATE)
        sub = rospy.Subscriber("chatter_m", StampedMessage, listener, callback_args=[pub])
		rospy.spin()
	except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
	main()
