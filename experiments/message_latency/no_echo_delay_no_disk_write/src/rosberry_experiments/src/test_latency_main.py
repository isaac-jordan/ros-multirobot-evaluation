#!/usr/bin/env python

import rospy
from rosberry_experiments.msg import StampedMessage
import sys, csv, itertools, os

MIN_FREQ = 500
MAX_FREQ = 10000
FREQ_STEP = 500
N_MESSAGES = 1000

# Stores current run's data
SENT_TIMES = [None] * N_MESSAGES
RECV_TIMES = [None] * N_MESSAGES

# Utility
def writeToCsv(currentFrequency):
    if os.path.isfile("results.csv"):
        with open("results.csv", "rb") as csv_in:
            csvReader = csv.reader(csv_in)
            with open("results_temp.csv", "wb") as csv_out:
                csvWriter = csv.writer(csv_out)
                csvWriter.writerow(next(csvReader) + ['sent_time' + str(currentFrequency), "recv_time" + str(currentFrequency)])
                for msg_id, sent_time, recv_time in itertools.izip_longest(xrange(N_MESSAGES), SENT_TIMES, RECV_TIMES):
                    csvWriter.writerow(next(csvReader) + [sent_time, recv_time])
                csv_out.flush()
        os.rename("results_temp.csv", "results.csv")
    else:
        with open("results.csv", "wb") as csv_out:
            csvWriter = csv.writer(csv_out)
            csvWriter.writerow(["id", "sent_time" + str(currentFrequency), "recv_time" + str(currentFrequency)])
            for msg_id, sent_time, recv_time in itertools.izip_longest(xrange(N_MESSAGES), SENT_TIMES, RECV_TIMES):
                csvWriter.writerow([msg_id, sent_time, recv_time])
            csv_out.flush()

def listener(msg):
    recv_time = rospy.get_rostime()
    sent_time = msg.t

    SENT_TIMES[msg.id] = sent_time
    RECV_TIMES[msg.id] = recv_time

def talker(numberOfMessages, frequency):
    pub = rospy.Publisher('chatter_m', StampedMessage, queue_size=numberOfMessages)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(frequency)
    for i in xrange(numberOfMessages):
        hello_str = "hello world"
        timestamp = rospy.get_rostime()
        pub.publish(id=i, t=timestamp, message=hello_str)
        rate.sleep()

def main():
    N_MESSAGES = int(sys.argv[1])
    FREQ = int(sys.argv[2])
    print str(N_MESSAGES) + " msgs at " + str(FREQ) + " Hz."

    try:
        sub = rospy.Subscriber("chatter_s", StampedMessage, listener)
        talker(N_MESSAGES, FREQ)

        rospy.sleep(5) # Sleep to allow for slow messages to catch up
    except rospy.ROSInterruptException:
        print "Exception: ROSInterruptException"

    # Write out data
    writeToCsv(FREQ)


if __name__ == '__main__':
    main()
