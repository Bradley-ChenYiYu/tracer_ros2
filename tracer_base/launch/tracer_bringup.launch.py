"""Bringup launch that composes tracer package and RealSense driver.

This launch file includes two other launch files:
- `tracer_base.launch.py` from this package
- `rs_launch.py` from the `realsense2_camera` package with the provided args

Usage:
  ros2 launch tracer_base tracer_bringup.launch.py

"""

import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
	# Locate this package's share directory and the tracer_base launch file
	pkg_tracer = get_package_share_directory('tracer_base')
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
			'usb_port_id': '4-6.1.1',
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
	)
	left_rs_launch = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			os.path.join(pkg_realsense, 'launch', 'rs_launch.py')
		),
		launch_arguments={
			'camera_name': 'left',
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
	)
	right_rs_launch = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			os.path.join(pkg_realsense, 'launch', 'rs_launch.py')
		),
		launch_arguments={
			'camera_name': 'right',
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
	)

	ld = LaunchDescription()
	ld.add_action(tracer_launch)
	ld.add_action(front_rs_launch)
	ld.add_action(left_rs_launch)
	ld.add_action(right_rs_launch)

	return ld

