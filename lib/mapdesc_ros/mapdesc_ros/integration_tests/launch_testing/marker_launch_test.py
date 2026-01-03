#!/usr/bin/env python
# based on https://github.com/ros2/launch_ros/blob/master/
# launch_testing_ros/test/examples/check_msgs_launch_test.py

# ROS 2 basics
from rclpy.task import Future
import rclpy

# ROS 2 launchfile
import launch
import launch.actions
import launch_ros.actions
import launch_testing.actions

# unit testing and pytest
import pytest
from threading import Event
from threading import Thread
import unittest

# launch_testing
from launch_testing.io_handler import ActiveIoHandler
import launch_testing.markers

# custom messages and services
from pathlib import Path
from mapdesc_msgs.srv import MapMarkerCreate, MapMarkerList, MapOverwrite

BASE_PATH = Path(__file__).parent.absolute()


@pytest.mark.launch_test
@launch_testing.markers.keep_alive
def generate_test_description():
    map_yaml = str(BASE_PATH.parent / 'data' / 'simple_marker_map.yml')
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='mapdesc_ros',
            executable='mapdesc_service',
            name='mapdesc_node',
            parameters=[
                {'map_yaml': map_yaml}
            ]
        ),
        launch_testing.actions.ReadyToTest()
    ])


class TestFixture(unittest.TestCase):
    def marker_added_callback(self, future: Future):
        """Callback that gets executed when the marker has been added."""
        assert future.result().success
        self.add_marker_service_success_event.set()

    def marker_listed_callback(self, future: Future):
        known_marker = [
            'center_marker', 'north_west', 'north_east', 'south_east']
        marker = future.result().marker
        marker_names = [m.name for m in marker]
        if len(marker) == len(known_marker):
            assert marker_names == known_marker
        elif len(marker) == len(known_marker)+1:
            # the other test has been executed first
            assert marker_names == known_marker + ['new point']
        else:
            assert False, 'number of stored marker does not match'
        self.list_marker_service_success_event.set()

    def spin(self):
        try:
            while rclpy.ok() and not self.spinning.is_set():
                rclpy.spin_once(self.node, timeout_sec=0.1)
        finally:
            return

    def setUp(self):
        rclpy.init()
        self.node = rclpy.create_node('test_node')
        self.list_marker_service_success_event = Event()
        self.add_marker_service_success_event = Event()
        self.spinning = Event()
        # Add a spin thread
        self.ros_spin_thread = Thread(target=self.spin)
        self.ros_spin_thread.start()

    def wait_for_service(self, service_clz, service_name):
        """wait for a service to become available."""
        self.cli = self.node.create_client(service_clz, service_name)
        service_available = False
        for _try in range(10):
            if self.cli.wait_for_service(timeout_sec=.5):
                service_available = True
                self.node.get_logger().info(
                    f'service {service_name} is available 👍!')
                break
            self.node.get_logger().info(
                f'service "{service_name}" not available, waiting again...')

        if not service_available:
            raise RuntimeError(f'Service "{service_name}" not available ☠!')

    def list_marker(self):
        """check if loaded marker are in the list."""
        self.wait_for_service(MapMarkerList, 'mapdesc/marker/list')
        request = MapMarkerList.Request(name='simple_map_marker')
        future = self.cli.call_async(request)
        future.add_done_callback(self.marker_listed_callback)

    def check_overwrite_map(self):
        self.wait_for_service(MapOverwrite, '/mapdesc/map/overwrite')

    def add_marker(self):
        """test if we can add a new marker"""
        self.wait_for_service(MapMarkerCreate, 'mapdesc/marker/create')
        request = MapMarkerCreate.Request(name='simple_map_marker')
        marker = request.item
        marker.name = 'new point'
        marker.pose.position.x = 10.0
        marker.pose.position.y = 12.0
        marker.pose.position.z = 0.5
        future = self.cli.call_async(request)
        future.add_done_callback(self.marker_added_callback)

    def tearDown(self):
        self.spinning.set()
        self.ros_spin_thread.join()
        self.node.destroy_client(self.cli)
        self.node.destroy_node()
        rclpy.shutdown()

    def test_check_if_service_called(self, proc_output: ActiveIoHandler):
        self.add_marker()
        service_called = self.add_marker_service_success_event.wait(
            timeout=15.0)
        assert service_called, 'Service to add marker not called!'

    def test_check_marker_listed(self, proc_output: ActiveIoHandler):
        self.list_marker()
        marker_listed = self.list_marker_service_success_event.wait(
            timeout=15.0)
        assert marker_listed, 'Service to list marker not called!'
