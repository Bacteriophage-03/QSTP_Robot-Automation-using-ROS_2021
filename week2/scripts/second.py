#!/usr/bin/env python3.8

import rospy
from std_msgs.msg import String

msg = String()
msg.data = "World!"
rospy.init_node('noob')
pub = rospy.Publisher('world', String, queue_size=10)
rate = rospy.Rate(2)

while not rospy.is_shutdown():
    pub.publish(msg)
    rate.sleep()
