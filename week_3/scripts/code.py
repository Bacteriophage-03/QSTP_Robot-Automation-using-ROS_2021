#!/usr/bin/env python3.8

import rospy
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import Point, Pose, PoseStamped, Quaternion, Twist
from std_msgs.msg import Header, Float64
from tf.transformations import euler_from_quaternion
import sys
import math

class Lmao:
	
	def __init__(self):
		self.sub_one = rospy.Subscriber('odom', Odometry, self.call_two)
		self.sub_two = rospy.Subscriber(sys.argv[1], Path, self.call_one)
		self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
		self.length = 0
		
		
		self.kp_linear = 0.05
		self.kd_linear = 0.1
		self.ki_linear = 0.0
		
		
		self.kp_angular = 0.2
		self.kd_angular = 0.1
		self.ki_angular = 0.0
		
		self.command = Twist()
		self.arr = Path.poses
		
		
		self.ang_diff_ini = 0.0
		self.x_ini = 0.0
		self.y_ini = 0.0
		self.ang_diff_ini=0.0
		self.x_fin = 0.0
		self.y_fin = 0.0
		
		self.count = 1
		self.first_run = True
		self.dist_ini = 0.0
		self.dist_fin = 0.0
		self.x_fin = 0.0
		self.y_fin = 0.0
		
		self.e_linear_d = 0.0
		self.e_angular_d = 0.0
		
		self.int_sum_linear = 0.0
		self.int_sum_ang = 0.0
		
		
	def call_one(self, msg):
		self.arr = msg.poses
		self.length = len(msg.poses)
		
		
		
		
	def normalize(self, angle):
		if(math.fabs(angle) > math.pi):
			angle = angle - (2 * math.pi * angle) / (math.fabs(angle))
		return angle
			
			
			
				
	def call_two(self, msg):
	
	
		if(self.count < self.length):
			self.x_fin = self.arr[self.count].pose.position.x
			self.y_fin = self.arr[self.count].pose.position.y
			
			
	
		
			if(self.first_run):
				self.x_ini = msg.pose.pose.position.x
				self.y_ini = msg.pose.pose.position.y
				goal_angle_ini = math.atan2(self.y_fin - self.y_ini, self.x_fin - self.x_ini)
				yaw_ini = math.atan2((2 * msg.pose.pose.orientation.z * msg.pose.pose.orientation.w) , (msg.pose.pose.orientation.w * msg.pose.pose.orientation.w) - 	(msg.pose.pose.orientation.z * msg.pose.pose.orientation.z))
				self.ang_diff_ini = (goal_angle_ini - yaw_ini) 
				self.dist_ini = math.sqrt((self.x_fin - self.x_ini)**2 + (self.y_fin - self.y_ini)**2)
		
			x = msg.pose.pose.position.x
			y = msg.pose.pose.position.y
			yaw = math.atan2((2 * msg.pose.pose.orientation.z * msg.pose.pose.orientation.w) , (msg.pose.pose.orientation.w * msg.pose.pose.orientation.w)-(msg.pose.pose.orientation.z * msg.pose.pose.orientation.z))
			goal_angle = math.atan2(self.y_fin - self.y_ini, self.x_fin - self.x_ini)
		
			ang_diff_final = (goal_angle - yaw)
			self.dist_fin = math.sqrt((self.x_fin - x)**2 + (self.y_fin - y)**2)
		
			self.e_linear_d = self.dist_fin - self.dist_ini
			self.e_angular_d = (ang_diff_final) - (self.ang_diff_ini)
			self.int_sum_linear = self.int_sum_linear + self.dist_fin
			self.int_sum_ang = self.int_sum_ang + ang_diff_final
		
			self.x_ini = msg.pose.pose.position.x
			self.y_ini = msg.pose.pose.position.y
			goal_angle_ini = goal_angle
			yaw_ini = yaw
		
			self.dist_ini = self.dist_fin
			self.ang_diff_ini = ang_diff_final
		
			self.first_run = False
			
			norm_ang = self.normalize(self.ang_diff_ini)
			
			
			
			
			
			if(self.dist_ini >= 0.05):
			
				if(math.fabs(norm_ang) >= 0.1):
					self.command.angular.z = min(((self.kp_angular * (norm_ang)) + (self.kd_angular * self.e_angular_d) + (self.ki_angular * self.int_sum_ang)), 0.22)	
					self.command.linear.x = 0.0
					self.pub.publish(self.command)
		
				else:
					self.command.linear.x = (self.kp_linear * self.dist_ini) + (self.kd_linear * self.e_linear_d) + (self.ki_linear * self.int_sum_linear)
					self.command.angular.z = 0.0
					self.pub.publish(self.command)
		
			else:
				self.count = self.count + 1
				self.first_run = True
				self.int_sum_linear = 0
				self.int_sum_ang = 0
				
		else:
			self.command.angular.z = 0
			self.command.linear.x = 0
			self.pub.publish(self.command)		
		
		
		
		

if __name__ == '__main__':
	rospy.init_node('path')
	
	
	bot = Lmao()
	
	rospy.spin()
