#!/usr/bin/env python3.8

import rospy
from std_msgs.msg import Float64

msg_rad = Float64()
msg_rad.data = 1.00

rospy.init_node('radius_node')
pub = rospy.Publisher('radius', Float64, queue_size = 10)

rate = rospy.Rate(10)

while not rospy.is_shutdown():
	pub.publish(msg_rad)
	rate.sleep()
	
	
