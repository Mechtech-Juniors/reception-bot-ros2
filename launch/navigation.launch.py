import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    pkg = get_package_share_directory('reception_bot')
    nav2_bringup = get_package_share_directory('nav2_bringup')

    map_arg = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(pkg, 'maps', 'office_map.yaml'),
        description='Full path to map yaml file'
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': LaunchConfiguration('map'),        # ← passes yaml path correctly
            'use_sim_time': 'false',
            'params_file': os.path.join(pkg, 'config', 'nav2_params.yaml'),
        }.items()
    )

    return LaunchDescription([
        map_arg,
        nav2_launch,
    ])
