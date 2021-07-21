#!/usr/bin/env python3.8

import rospy
import math

from week2.srv import Pose, PoseResponse, PoseRequest

def trajectory(request):
	p = request.x
	q = request.y
	r = request.theta
	s = request.v
	t = request.w
	
	x_test = [p]
	y_test = [q]
	
	for i in range(50):
		r = r + (t * 0.05)
		p = p + ((s * math.cos(r))*0.05)
		q = q + ((s * math.sin(r))*0.05)
		x_test = x_test + [p]
		y_test = y_test + [q]
	
	return PoseResponse(x_test, y_test)
	


rospy.init_node('server')

service = rospy.Service('calc_traj', Pose, trajectory)
rospy.spin()
	
