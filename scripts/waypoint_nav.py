#!/usr/bin/env python
import rospy, yaml, actionlib, os, rospkg
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus

rospy.init_node('waypoint_nav')

pkg = rospkg.RosPack().get_path('slam_navigation') # package path
wp = yaml.safe_load(open(os.path.join(pkg, 'maps', 'waypoints.yaml'))) # load saved points

client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
client.wait_for_server()

while not rospy.is_shutdown():
    pid = input("Enter destination ID: ") # user enters e.g. labA
    if pid not in wp:
        print("Unknown ID"); continue
    p = wp[pid]
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = p['x']
    goal.target_pose.pose.position.y = p['y']
    goal.target_pose.pose.orientation.z = p['z']
    goal.target_pose.pose.orientation.w = p['w']
    client.send_goal(goal) # robot navigates
    client.wait_for_result()
    ok = client.get_state() == GoalStatus.SUCCEEDED
    print("Arrived" if ok else "Failed")