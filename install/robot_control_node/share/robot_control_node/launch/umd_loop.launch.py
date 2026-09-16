from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    # -------------------------
    # Gazebo
    # -------------------------

    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                ros_gz_sim_share,
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': 'umd_loop_challenge_week_s1.sdf'
        }.items()
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/model/vehicle/cmd_vel'
            '@geometry_msgs/msg/Twist'
            '@gz.msgs.Twist',

            '/model/vehicle/pose'
            '@geometry_msgs/msg/Pose'
            '@gz.msgs.Pose',

            '/model/vehicle/lidar_sensor'
            '@sensor_msgs/msg/LaserScan'
            '@gz.msgs.LaserScan',
        ],
        output='screen'
    )

    controller = Node(
            package='robot_control_node',
            executable='vehicle_controller',
            output='screen'
    )

    return LaunchDescription([
        gazebo,
        bridge,
        controller,
    ])
