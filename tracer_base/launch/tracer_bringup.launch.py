"""Bringup launch that composes tracer package and RealSense driver.

This launch file includes two other launch files:
- `tracer_base.launch.py` from this package
- `rs_launch.py` from the `realsense2_camera` package with the provided args

Usage:
  ros2 launch tracer_base tracer_bringup.launch.py

"""

import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
	# Locate this package's share directory and the tracer_base launch file
	pkg_tracer = get_package_share_directory('tracer_base')
	rviz_config = os.path.join(pkg_tracer, 'config', 'image.rviz')
	launch_rviz_arg = DeclareLaunchArgument(
		'rviz',
		default_value='true',
		description='Launch RViz2 with the tracer_base image config',
	)
	launch_front_cam_arg = DeclareLaunchArgument(
		'enable_front_cam',
		default_value='true',
		description='Whether to launch the front camera RealSense node.',
	)
	launch_right_cam_arg = DeclareLaunchArgument(
		'enable_right_cam',
		default_value='true',
		description='Whether to launch the right camera RealSense node.',
	)
	launch_left_cam_arg = DeclareLaunchArgument(
		'enable_left_cam',
		default_value='true',
		description='Whether to launch the left camera RealSense node.',
	)

	tracer_launch = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			os.path.join(pkg_tracer, 'launch', 'tracer_base.launch.py')
		)
	)

	# Locate realsense2_camera package and include its rs_launch.py with args
	# 	The ID of the USB hub port start from the output side of the hub,
	# 	start from *.1.1, *.1.2, and so on. You can use `lsusb -t` to check the port ID of each camera.
	pkg_realsense = get_package_share_directory('realsense2_camera')
	front_rs_launch = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			os.path.join(pkg_realsense, 'launch', 'rs_launch.py')
		),
		launch_arguments={
			'camera_name': 'front',
			'usb_port_id': '4-2.1.1',
			'enable_color': 'true',
			'enable_depth': 'false',
			'enable_infra': 'false',
			'enable_infra1': 'false',
			'enable_infra2': 'false',
			'enable_gyro': 'false',
			'enable_accel': 'false',
			'enable_motion': 'false',
			'pointcloud.enable': 'false',
			'align_depth.enable': 'false',
			'rgb_camera.color_profile': '320x240x60',
		}.items(),
		condition=IfCondition(LaunchConfiguration('enable_front_cam')),
	)
	left_rs_launch = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			os.path.join(pkg_realsense, 'launch', 'rs_launch.py')
		),
		launch_arguments={
			'camera_name': 'left',
			'usb_port_id': '4-6.1.3',
			'enable_color': 'true',
			'enable_depth': 'false',
			'enable_infra': 'false',
			'enable_infra1': 'false',
			'enable_infra2': 'false',
			'enable_gyro': 'false',
			'enable_accel': 'false',
			'enable_motion': 'false',
			'pointcloud.enable': 'false',
			'align_depth.enable': 'false',
			'rgb_camera.color_profile': '320x240x60',
		}.items(),
		condition=IfCondition(LaunchConfiguration('enable_left_cam')),
	)
	right_rs_launch = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			os.path.join(pkg_realsense, 'launch', 'rs_launch.py')
		),
		launch_arguments={
			'camera_name': 'right',
			'usb_port_id': '4-6.1.2',
			'enable_color': 'true',
			'enable_depth': 'false',
			'enable_infra': 'false',
			'enable_infra1': 'false',
			'enable_infra2': 'false',
			'enable_gyro': 'false',
			'enable_accel': 'false',
			'enable_motion': 'false',
			'pointcloud.enable': 'false',
			'align_depth.enable': 'false',
			'rgb_camera.color_profile': '320x240x60',
		}.items(),
		condition=IfCondition(LaunchConfiguration('enable_right_cam')),
	)

	rviz_launch = Node(
		package='rviz2',
		executable='rviz2',
		arguments=['-d', rviz_config],
		output='screen',
		condition=IfCondition(LaunchConfiguration('rviz')),
	)

	# Static transform: base_link → camera_link
	baselink_to_front_camera = Node(
		package='tf2_ros',
		executable='static_transform_publisher',
		name='baselink_to_front_camera',
		arguments=['0.25', '0', '0.69', '0', '0', '0', 'base_link', 'front_link'],
	)

	ld = LaunchDescription()
	ld.add_action(launch_rviz_arg)
	ld.add_action(launch_front_cam_arg)
	ld.add_action(launch_left_cam_arg)
	ld.add_action(launch_right_cam_arg)
	ld.add_action(tracer_launch)
	ld.add_action(front_rs_launch)
	ld.add_action(left_rs_launch)
	ld.add_action(right_rs_launch)

	ld.add_action(baselink_to_front_camera)
	ld.add_action(rviz_launch)
	return ld
