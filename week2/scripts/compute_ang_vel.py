#!/usr/bin/env python3.8

import rospy

from week2.srv import Angular, AngularResponse, AngularRequest

def calc(request):
	return AngularResponse(0.1/(request.rad))


rospy.init_node('turtle_vel')

service = rospy.Service('compute_ang_vel', Angular, calc)
rospy.spin()



