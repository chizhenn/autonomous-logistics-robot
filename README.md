# Autonomous Indoor Logistics Robot for Laboratory Materials Delivery

Academic Project I - Faculty of Computer Science & IT, University of Malaya.
An autonomous indoor robot for delivering laboratory materials in the Parasitology Department, using SLAM navigation and human-aware variable speed control.

autonomous-logistics-robot/
├── README.md
├── catkin_ws/            
│   ├── build/
│   ├── devel/
│   └── src/
│       ├── slam_navigation/
│       │   ├── maps/
│       │   ├── scripts/
│       │   ├── CMakeLists.txt
│       │   └── package.xml
│       ├── turtlebot3/
│       ├── turtlebot3_msgs/
│       └── turtlebot3_simulations/
└── yolo_fuzzy_speed.py
    
## Modules

### Module 1 — SLAM Navigation (`slam_navigation/`)
ROS-based mapping and navigation:
- **GMapping** builds the map, saved as `.pgm` + `.yaml`
- **AMCL** localizes the robot on the map
- **A\*** (global) + **DWA** (local) plan and execute paths
- User enters a saved location ID to navigate the robot there

Scripts:
- `waypoint_nav.py` — navigate by destination ID
- `plot_map.py` — plot map with labeled locations
- `extract_landmarks.py` — RANSAC landmark extraction (feature analysis)

### Module 2 — Human Detection & Fuzzy Speed Control (`yolo_fuzzy_speed/`)
Detects people via **YOLO11** and uses **fuzzy logic** to adjust speed by distance — slowing when near, speeding up when far.

## Tech Stack
Python, ROS (Ubuntu), Gazebo, RViz, GMapping, OpenCV, Ultralytics (YOLO11), PyTorch, scikit-fuzzy, NumPy, matplotlib

## How to Run

### Module 1 (on The Construct / ROS)
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

# Run waypoint navigation (new terminal)
rosrun slam_navigation waypoint_nav.py
```
Set the robot's initial pose with **2D Pose Estimate** in RViz before navigating.

### Module 2 (standalone)
```bash
pip install -U ultralytics opencv-python scikit-fuzzy "numpy<2"
python3 yolo_fuzzy_speed.py
```
Press `q` to quit.

## Author
Ooi Chien Zhen — University of Malaya
