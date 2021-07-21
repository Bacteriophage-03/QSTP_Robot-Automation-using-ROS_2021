#!/usr/bin/env python3.8

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from week2.srv import Angular


rospy.init_node('Turtle_Move')
rospy.wait_for_service('compute_ang_vel')
circle = rospy.ServiceProxy('compute_ang_vel', Angular)
vel = Twist()

def callback(msg):
	vel.linear.x = 0.1
	vel.linear.y = 0.0
	vel.linear.z = 0.0
	vel.angular.x = 0.0
	vel.angular.y = 0.0
	obj = circle(msg.data)
	vel.angular.z = obj.ang_vel
	


pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
sub = rospy.Subscriber('radius', Float64, callback)

rate = rospy.Rate(10)

while not rospy.is_shutdown():
	pub.publish(vel)
	rate.sleep()
	
	
