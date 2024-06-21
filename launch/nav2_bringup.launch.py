from launch import LaunchDescription
from launch.actions import OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import\
    get_package_share_directory as find_pkg_share
from launch.substitutions import EnvironmentVariable


def launch_setup(context, *args, **kwargs):
    launch_description = []

    # location of the robot, defaults to "rh1_eg"
    location_name = LaunchConfiguration('location_name').perform(context)

    # robot name, should be black, blue, green or eve
    robot_name = LaunchConfiguration('robot_name').perform(context)

    map_yaml_path = find_pkg_share(
        'ricbot_navigation') + f'/maps/{location_name}_map.yaml'

    # TODO: check, if we need to start the livecycle manager?!

    # Nav2 Bringup
    launch_description.append(IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [find_pkg_share('nav2_bringup'), '/launch/bringup_launch.py']),
        launch_arguments={
            'namespace': robot_name,
            'map': map_yaml_path,
            'slam': 'False',
            'autostart': LaunchConfiguration('autostart').perform(context),
            'use_sim_time': LaunchConfiguration('simulation').perform(context),
            #'params_file': params_file,
            #'default_bt_xml_filename': bt_xml_file
        }.items()
    ))

    return launch_description


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("location_name", default_value="rh1_eg"),
        DeclareLaunchArgument("simulation",    default_value="true"),
        DeclareLaunchArgument("autostart",     default_value="true"),
        DeclareLaunchArgument("robot_name"),
        OpaqueFunction(function=launch_setup)
    ])
