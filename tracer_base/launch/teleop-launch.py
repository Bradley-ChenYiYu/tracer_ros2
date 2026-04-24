import os

from ament_index_python.packages import get_package_share_directory

import launch
import launch_ros.actions


def generate_launch_description():
    joy_vel = launch.substitutions.LaunchConfiguration('joy_vel')
    joy_config = launch.substitutions.LaunchConfiguration('joy_config')
    joy_dev = launch.substitutions.LaunchConfiguration('joy_dev')
    publish_stamped_twist = launch.substitutions.LaunchConfiguration('publish_stamped_twist')
    config_filepath = launch.substitutions.LaunchConfiguration('config_filepath')

    # Build a path like: <pkg_share>/config/xbox.config.yaml
    # Build a path like: <pkg_share>/config/xbox.config.yaml
    config_default = launch.substitutions.PathJoinSubstitution([
        get_package_share_directory('tracer_base'),
        'config',
        joy_config,
    ])

    return launch.LaunchDescription([
        # Declare launch arguments first so substitutions can be resolved by later actions
        launch.actions.DeclareLaunchArgument('joy_vel', default_value='cmd_vel'),
        launch.actions.DeclareLaunchArgument('joy_config', default_value='xbox.config.yaml'),
        launch.actions.DeclareLaunchArgument('joy_dev', default_value='0'),
        launch.actions.DeclareLaunchArgument('publish_stamped_twist', default_value='false'),
        launch.actions.DeclareLaunchArgument('config_filepath', default_value=config_default),
        # Print the resolved config filepath so we can confirm the YAML being used
        launch.actions.LogInfo(msg=["teleop config_filepath: ", config_filepath]),

        launch_ros.actions.Node(
            package='joy', executable='joy_node', name='joy_node',
            parameters=[{
                'device_id': joy_dev,
                'deadzone': 0.1,
                'autorepeat_rate': 20.0,
            }, config_filepath]),
        launch_ros.actions.Node(
            package='teleop_twist_joy', executable='teleop_node',
            name='teleop_twist_joy_node',
            parameters=[config_filepath, {'publish_stamped_twist': publish_stamped_twist}],
            remappings=[('/cmd_vel', joy_vel)],
        ),
    ])
