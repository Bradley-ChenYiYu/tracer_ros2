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
	pkg_realsense = get_package_share_directory('realsense2_camera')
	rs_launch = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			os.path.join(pkg_realsense, 'launch', 'rs_launch.py')
		),
		launch_arguments={
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
	ld.add_action(rs_launch)

	return ld

