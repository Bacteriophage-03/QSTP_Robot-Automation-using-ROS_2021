import rospy
from week2.srv import Pose
import sys
import matplotlib.pyplot as plt



rospy.init_node('server_client')
rospy.wait_for_service('calc_traj')

trajec = rospy.ServiceProxy('calc_traj', Pose)

def plot(x_test, y_test, v: float, w: float):
	plt.title(f"Unicycle Model: {v}, {w}")
	plt.xlabel("X-Coordinates")
	plt.ylabel("Y-Coordinates")
	plt.plot(x_test, y_test, color="red", alpha=0.75)
	plt.grid()
	plt.show()
        

if __name__ == "__main__":
	
	x = float(sys.argv[1])
	y = float(sys.argv[2])
	theta = float(sys.argv[3])
	v = float(sys.argv[4])
	w = float(sys.argv[5])
	obj = trajec(x,y,theta,v,w)
	
	plot(obj.x_points, obj.y_points, v, w)

#rospy.spin() 





