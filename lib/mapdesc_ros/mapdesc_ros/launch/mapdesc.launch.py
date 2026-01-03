from pathlib import Path
from launch import LaunchDescription
from launch.actions import OpaqueFunction
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def launch_setup(context, *args, **kwargs):
    """
    Generate launch description to start the wrapper for the mapdesc library.
    """
    map_yaml = LaunchConfiguration('map_yaml').perform(context)
    return [
        LaunchDescription([
            Node(
                package='mapdesc_ros',
                executable='mapdesc_service',
                name='mapdesc_node',
                parameters=[
                    {'map_yaml': map_yaml}
                ]
            )
        ])]


def generate_launch_description():
    map_yaml = str(Path('/map_data') / 'rh1_eg.yml')
    return LaunchDescription([
        DeclareLaunchArgument(
            "map_yaml", default_value=map_yaml),
        OpaqueFunction(function=launch_setup)
    ])
