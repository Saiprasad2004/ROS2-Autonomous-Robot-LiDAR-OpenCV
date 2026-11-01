from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterFile

def generate_launch_description():

    return LaunchDescription([

        # Start Gazebo
        ExecuteProcess(
            cmd=[
                'gz',
                'sim',
                '/home/prasad/ros2_ws/src/obstacle_avoiding_robot_v3/worlds/room.world'
            ],
            output='screen'
        ),

        # Spawn robot
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name',
                'obstacle_robot',
                '-file',
                '/home/prasad/ros2_ws/src/obstacle_avoiding_robot_v3/urdf/robot.urdf',
                '-x',
                '0',
                '-y',
                '0',
                '-z',
                '0.15'
            ],
            output='screen'
        ),

        # LiDAR bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'
            ],
            output='screen'
        ),
 
        # Camera image bridge (Gazebo -> ROS 2)
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/camera@sensor_msgs/msg/Image[gz.msgs.Image'
            ],
            output='screen'
        ),

        # cmd_vel bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist'
            ],
            output='screen'
        ),
        
        # Odometry bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry'
            ],
            output='screen'
        ),
       
        # Publish odom -> base_link TF
        Node(
            package='obstacle_avoiding_robot_v3',
            executable='odom_tf_publisher',
            output='screen'
        ), 

        # Publish robot TF from URDF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[
                {
                    'robot_description': ParameterValue(
                        open(
                            '/home/prasad/ros2_ws/src/obstacle_avoiding_robot_v3/urdf/robot.urdf',
                            'r'
                        ).read(),
                        value_type=str
                    )
                }
            ],
            output='screen'
        ),

        # Obstacle avoidance
        Node(
            package='obstacle_avoiding_robot_v3',
            executable='obstacle_avoid',
            output='screen'
        ),
        # SLAM mapping
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                ParameterFile(
                    '/home/prasad/ros2_ws/src/obstacle_avoiding_robot_v3/config/mapper_params_online_async.yaml',
                    allow_substs=True
                )
            ]
        ),
    ])
