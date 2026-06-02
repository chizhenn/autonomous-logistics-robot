### How to Run

```bash
# Build
cd ~/catkin_ws && catkin_make
source devel/setup.bash

# Launch simulation
export TURTLEBOT3_MODEL=burger
roslaunch turtlebot3_gazebo turtlebot3_world.launch

# Launch navigation (new terminal)
export TURTLEBOT3_MODEL=burger
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/catkin_ws/src/slam_navigation/maps/my_map.yaml

# Manual control (new terminal)
export TURTLEBOT3_MODEL=burger 
roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

# Run waypoint navigation (new terminal)
rosrun slam_navigation waypoint_nav.py
```

Set the robot's initial pose with **2D Pose Estimate** in RViz before navigating.
