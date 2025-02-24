#!/usr/bin/env python3
import os
import sys
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, TimerAction, RegisterEventHandler
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit, OnProcessStart
import xacro

def generate_launch_description():
    gazebo_pkg = get_package_share_directory('rom2109_gazebo')
    #joy_pkg = get_package_share_directory('rom_robotics_joy')
    description_pkg = get_package_share_directory('rom2109_description')

    rom_world = os.environ.get('ROM_GZ_WORLD', 'rom_maze_1.world')
    default_world_path = os.path.join(gazebo_pkg, 'worlds', rom_world)

    urdf_file = os.path.join(description_pkg,'urdf', 'lidarbot.urdf')
    # robot_description_config = xacro.process_file(xacro_file)
    # my_xml = robot_description_config.toxml()

    bot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            description_pkg, 'launch', 'description_ros2_control.launch.py'
        )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(gazebo_pkg, 'rviz2', 'slam.rviz')],
        condition=IfCondition(LaunchConfiguration('open_rviz'))
    )

    gazebo_params_file = os.path.join(get_package_share_directory(
        'rom2109_gazebo'), 'config', 'gazebo_params.yaml')

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py")),
        launch_arguments={
            "use_sim_time": "true",
            "robot_name": "rom2109",
            "world": default_world_path,
            "lite": "false",
            "world_init_x": "0.0",
            "world_init_y": "0.0",
            "world_init_heading": "0.0",
            "gui": "true",
            "close_loop_odom": "true",
            "extra_gazebo_args": "--ros-args --params-file " + gazebo_params_file
        }.items(),
    )

    spawn_robot_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        # arguments=['-database', 'rom2109_tall_ros', '-entity', 'rom2109_tall_ros',
        arguments=['-file', urdf_file, '-entity', 'rom2109_tall_psa',
                   "-x", '0.0',
                   "-y", '0.0',
                   "-z", '0.3'],
        output='screen'
    )
    
    """ joystick_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(joy_pkg, 'launch', 'joystick.launch.py')]),
        launch_arguments={'use_sim_time': 'true'}.items(),
        #condition=IfCondition('use_joystick')
    ) """

    twist_mux_params = os.path.join(get_package_share_directory('rom2109_gazebo'), 'config', 'twist_mux.yaml')
    twist_mux_node = Node(
        package="twist_mux",
        executable="twist_mux",
        parameters=[twist_mux_params],
        remappings=[('/cmd_vel_out', '/diff_cont/cmd_vel_unstamped')]
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        namespace='',
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument('open_rviz', default_value='false', description='Open RViz.'),
            DeclareLaunchArgument('use_joystick', default_value='true', description='JoyStick.'),
            DeclareLaunchArgument('use_sim_time', default_value='true', description='Sim Time'),
            bot,
            gazebo_launch,
            rviz_node,
            spawn_robot_node,
            #joystick_launch,
            twist_mux_node,
            diff_drive_spawner,
            joint_broad_spawner,
        ]
    )
''' 
respawn=use_respawn,
respawn_delay=2.0,
'''
