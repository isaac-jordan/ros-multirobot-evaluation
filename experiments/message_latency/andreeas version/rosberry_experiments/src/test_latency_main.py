#!/usr/bin/env python
# license removed for brevity
import rospy
from rosberry_experiments.msg import StampedMessage
import time
import sys

N = None
RATE = None
f = open("times_"+str(RATE)+".txt", "w+")

def listener(msg):
	recv_time = time.time()
#	recv_time = rospy.get_rostime()

	send_time = float(msg.t)
#	duration = (recv_time-send_time)/2.0
	f.write(str(msg.id))
	f.write(",")
#	f.write(str(send_time.secs))
#	f.write(".")
	f.write(str(send_time))
#	f.write(str(duration*1000))
	f.write(",")
	f.write(str(recv_time))
#	f.write(".")
#	f.write(str(recv_time.nsecs))
#	f.write(str(duration.nsecs/1000000.0))
	f.write("\n")
def talker():
	pub = rospy.Publisher('chatter_m', StampedMessage, queue_size=RATE)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(RATE)
	for i in xrange(N):
        	hello_str = "hello world"
		timestamp = str(time.time())
        	pub.publish(id=i, t=timestamp ,message=hello_str )
#        	pub.publish(id=i, t=rospy.get_rostime(),message=hello_str )
	        rate.sleep()
	
def main():
	global RATE, N
	RATE = int(sys.argv[1])
	N = int(sys.argv[2])
	print RATE, N
	try:
		sub = rospy.Subscriber("chatter_s", StampedMessage, listener)
        	talker()
		rospy.sleep(5)
		f.close()

	except rospy.ROSInterruptException:
        	pass


if __name__ == '__main__':
	main()
