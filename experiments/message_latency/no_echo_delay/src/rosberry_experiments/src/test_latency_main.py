#!/usr/bin/env python

import rospy
from rosberry_experiments.msg import StampedMessage
import sys, csv, itertools, os

MIN_FREQ = 500
MAX_FREQ = 10000
FREQ_STEP = 500
N_MESSAGES = 1000

# Stores current run's data
data = {
    "sent_time" : [None] * N_MESSAGES,
    "recv_time" : [None] * N_MESSAGES
}

def listener(msg):
    recv_time = rospy.get_rostime()
    sent_time = msg.t

    data["sent_time"][msg.id] = sent_time
    data["recv_time"][msg.id] = recv_time

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
    if os.path.isfile("results.csv"):
        os.remove("results.csv")

    currentFrequency = MIN_FREQ
    while (currentFrequency <= MAX_FREQ):
        print str(N_MESSAGES) + " msgs at " + str(currentFrequency) + " Hz."
        try:
            sub = rospy.Subscriber("chatter_s", StampedMessage, listener)
            talker(N_MESSAGES, currentFrequency)

            # Sleep to allow for slow messages to catch up
            rospy.sleep(10)
        except rospy.ROSInterruptException:
            print "Exception: ROSInterruptException"

        # Write out data
        writeToCsv(currentFrequency)

        # Reset data storage
        data = {
            "sent_time" : [None] * N_MESSAGES,
            "recv_time" : [None] * N_MESSAGES
        }
        currentFrequency += FREQ_STEP

        # Sleep to allow any file processing to finish
        rospy.sleep(5)


if __name__ == '__main__':
    main()

# Utility
def writeToCsv(currentFrequency):
    if os.path.isfile("results.csv"):
        with open("results.csv", "rb") as csv_in:
            csvReader = csv.reader(csv_in)
            with open("results_temp.csv", "wb") as csv_out:
                csvWriter = csv.writer(csv_out)
                csvWriter.writerow(next(csvReader) + ['sent_time' + str(currentFrequency), "recv_time" + str(currentFrequency)])
                for msg_id, sent_time, recv_time in itertools.izip_longest(xrange(len(data["sent_time"])), data["sent_time"], data["recv_time"]):
                    csvWriter.writerow(next(csvReader) + [sent_time, recv_time])
                csv_out.flush()
        os.rename("results_temp.csv", "results.csv")
    else:
        with open("results.csv", "wb") as csv_out:
            csvWriter = csv.writer(csv_out)
            csvWriter.writerow(["id", "sent_time" + str(currentFrequency), "recv_time" + str(currentFrequency)])
            for msg_id, sent_time, recv_time in itertools.izip_longest(xrange(len(data["sent_time"])), data["sent_time"], data["recv_time"]):
                csvWriter.writerow([msg_id, sent_time, recv_time])
            csv_out.flush()
