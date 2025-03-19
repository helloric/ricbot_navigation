# RICBot Navigation (ROS2 bringup, mapdesc and basic python services to move)
from pathlib import Path
from launch import LaunchDescription
from launch.actions import OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource, FrontendLaunchDescriptionSource
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory as find_pkg_share
import os


def launch_setup(context, *args, **kwargs):
    launch_description = []

    robot_name = LaunchConfiguration('robot_name').perform(context)
    map_yaml = LaunchConfiguration('map_yaml').perform(context)

    launch_description.append(IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            find_pkg_share('ricbot_navigation') +
            '/launch/nav2_bringup.launch.py'),
        launch_arguments={
            'robot_name': robot_name,
            'autostart': 'True'
        }.items()))

    launch_description.append(IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            find_pkg_share('mapdesc_ros') +
            '/launch/mapdesc.launch.py'),
        launch_arguments={
            'map_yaml': map_yaml
        }.items()))

    launch_description.append(LaunchDescription([
            Node(
                package='ricbot_navigation',
                executable='ricbot_navigation_node',
                name='ricbot_navigation_node',
                parameters=[]
            )
        ]))

    launch_description.append(LaunchDescription([
            Node(
                package='ricbot_navigation',
                executable='marker_info_node',
                name='marker_info_node',
                parameters=[]
            )
        ]))

    return launch_description


def generate_launch_description():
    map_yaml = str(Path('/map_data') / 'rh1_a002.yml')
    return LaunchDescription([
        DeclareLaunchArgument(
            "robot_name", default_value="eve"),
        DeclareLaunchArgument(
            "map_yaml", default_value=map_yaml),
        OpaqueFunction(function=launch_setup)
    ])
