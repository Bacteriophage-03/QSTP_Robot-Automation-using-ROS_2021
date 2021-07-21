#!/usr/bin/env python3.8

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from week2.srv import Angular


class Infinity:

	def __init__(self):
		self.sub_one = rospy.Subscriber('odom', Odometry, self.call_one)
		self.sub_two = rospy.Subscriber('radius', Float64, self.call_two)
		self.inif = rospy.ServiceProxy('compute_ang_vel', Angular)
		self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
		self.total_distance = 0
		self.previous_x = 0
		self.previous_y = 0
		self.rad = 1.0
		self.counter = 1
		self.vel = Twist()
		self.first_run = True

	def call_one(self, msg):
  
		if(self.first_run):
			self.previous_x = msg.pose.pose.position.x
			self.previous_y = msg.pose.pose.position.y
			
		x = msg.pose.pose.position.x
		y = msg.pose.pose.position.y
		d_increment = math.sqrt((x - self.previous_x) * (x - self.previous_x) + (y - self.previous_y) * (y - self.previous_y))
		self.total_distance = self.total_distance + d_increment
		
		self.vel.linear.x = 0.1
		obj = self.inif(self.rad)
		
		
		self.vel.angular.z = obj.ang_vel * self.counter
		
		self.pub.publish(self.vel)
		
		self.previous_x = msg.pose.pose.position.x
		self.previous_y = msg.pose.pose.position.y
		
		self.first_run = False
		print(self.total_distance)
		
		
		if(self.total_distance >= 2 * math.pi * self.rad):
			self.counter = -1 * self.counter
			self.total_distance = 0
			self.first_run = True
			

	def call_two(self,msg):
		self.rad = msg.data
		


if __name__ == '__main__':
  
	rospy.init_node('final_infinity')
	rospy.wait_for_service('compute_ang_vel')
	
	
	bot = Infinity()
	rospy.spin()
