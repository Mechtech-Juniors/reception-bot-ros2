import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg = get_package_share_directory('reception_bot')

    # Process xacro → URDF string
    xacro_file = os.path.join(pkg, 'urdf', 'reception_bot.urdf.xacro')
    robot_desc = xacro.process_file(xacro_file).toxml()

    # Gazebo launch (with world file)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'),
                         'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={
            'world': os.path.join(pkg, 'worlds', 'office_world.world'),
            'verbose': 'false',
        }.items()
    )

    # Robot state publisher
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True,
        }],
        output='screen'
    )

    # Spawn robot into Gazebo
    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'reception_bot',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1',
        ],
        output='screen'
    )

    # Joint state publisher (for non-driven joints)
    jsp = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': True}]
    )

    # Teleop for testing
    teleop = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop',
        remappings=[('/cmd_vel', '/reception_bot/cmd_vel')],
        prefix='xterm -e',
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        rsp,
        jsp,
        TimerAction(period=3.0, actions=[spawn]),
    ])