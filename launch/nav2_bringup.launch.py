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

    # TODO: generate namespace using robot name
    # robot name, should be black, blue, green or eve
    # robot_name = LaunchConfiguration('robot_name').perform(context)

    map_yaml_path = find_pkg_share('ricbot_navigation') + \
        f'/maps/{location_name}_map.yaml'

    # Nav2 Bringup
    params_file = find_pkg_share('ricbot_navigation') +  \
        '/config/nav2_params.yaml'

    launch_description.append(IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            find_pkg_share('nav2_bringup'),
            '/launch/bringup_launch.py'
        ]),
        launch_arguments={
            # 'namespace': robot_name,
            # 'use_namespace': 'True',
            'map': map_yaml_path,
            'slam': 'False',
            'map_subscribe_transient_local': 'True',
            'params_file': params_file,
            'autostart': LaunchConfiguration('autostart').perform(context),
            'use_sim_time': LaunchConfiguration('simulation').perform(context)
        }.items()
    ))

    return launch_description


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("location_name", default_value="rh1_eg"),
        DeclareLaunchArgument("simulation",    default_value="true"),
        DeclareLaunchArgument("autostart",     default_value="true"),
        DeclareLaunchArgument("robot_name",    default_value="eve"),
        OpaqueFunction(function=launch_setup)
    ])
