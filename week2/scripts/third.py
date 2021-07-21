#!/usr/bin/env python3.8

import rospy
from std_msgs.msg import String

msg_one = String()
msg_two = String()

def call_one(msg):
	msg_one.data = msg.data
	
def call_two(msg):
	msg_two.data = msg.data
		
rospy.init_node('ara_ara')
pub = rospy.Publisher('helloworld', String, queue_size=10)

sub_one = rospy.Subscriber('hello', String, call_one)
sub_two = rospy.Subscriber('world', String, call_two)

rate = rospy.Rate(2)

while not rospy.is_shutdown():
	pub.publish(msg_one.data + msg_two.data)
	rate.sleep()
