# ROS 2 Autonomous Obstacle-Avoiding Robot

A simulated mobile robot project built using ROS 2 Jazzy and Gazebo.

## Features

- ROS 2 Jazzy integration
- Gazebo robot simulation
- Custom enclosed environment with multiple obstacles
- LiDAR-based reactive obstacle avoidance
- Camera integration using ROS 2
- OpenCV image processing and bounding boxes
- SLAM Toolbox integration

## Technology Stack

- ROS 2 Jazzy
- Python
- Gazebo
- OpenCV
- cv_bridge
- SLAM Toolbox

## Repository Structure

- obstacle_avoiding_robot_v3/ - Robot simulation, control, launch files, URDF and world.
- camera_opencv/ - Camera subscriber and OpenCV processing.

## Build Instructions

Clone this repository into your ROS 2 workspace src directory.

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-up-to obstacle_avoiding_robot_v3 camera_opencv
source install/setup.bash
```

## Launch Simulation

```bash
ros2 launch obstacle_avoiding_robot_v3 obstacle_robot.launch.py
```

## Run Camera Node

```bash
ros2 run camera_opencv camera_subscriber
```

## Future Improvements

- Nav2 autonomous navigation
- Improved SLAM mapping
- Camera-LiDAR sensor fusion
- Object recognition
- Navigation performance evaluation

## Author

Pasupula Prasad
