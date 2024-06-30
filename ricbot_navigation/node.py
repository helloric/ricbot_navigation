#!/usr/bin/env python3
# rclpy
import rclpy
from rclpy.task import Future
from rclpy.node import Node

# ROS 2 basics
from geometry_msgs.msg import Pose, PoseStamped

# Nav2
from nav2_simple_commander.robot_navigator import BasicNavigator

# mapdesc_msgs
from mapdesc_msgs.srv import ListMarker


class NavNode(Node):
    def __init__(self):
        super().__init__('ricbot_navigation_node')
        self.nav = BasicNavigator()
        self.marker_cli = self.create_client(
            ListMarker, 'list_marker')

    def _create_pose_stamped(self, basic_pose: Pose) -> PoseStamped:
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.nav.get_clock().now().to_msg()
        pose.pose = basic_pose
        return pose

    def wait_for_service(self, cli):
        """wait for a service to become available."""
        for _try in range(10):
            if cli.wait_for_service(timeout_sec=.5):
                self.get_logger().info('Service is available 👍!')
                return True
            self.get_logger().info('service not available, waiting...')
        return False

    def set_initial_pose(self):
        self.nav.setInitialPose(self._create_pose_stamped(Pose()))
        self.nav.waitUntilNav2Active()

    def get_marker(self):
        # request marker from service
        self.wait_for_service(self.marker_cli)
        request = ListMarker.Request()
        future = self.marker_cli.call_async(request)
        future.add_done_callback(self.get_marker_callback)

    def get_marker_callback(self, future: Future):
        _marker = future.result().marker
        self.get_logger().info(f'Received {len(_marker)} marker 👍!')
        if len(_marker) == 0:
            return
        while True:
            for marker in _marker:
                self.get_logger().info(
                    f"Will move to waypoint {marker.name} - "
                    f"x: {marker.pose.position.x} "
                    f"y: {marker.pose.position.y}")
                self.move_to_waypoint(
                    self._create_pose_stamped(marker.pose))

    def move_to_waypoint(self, pose: PoseStamped):
        nav = self.nav
        try:
            nav.goToPose(pose)
            while not nav.isTaskComplete():
                nav.getFeedback()
                # feedback = nav.getFeedback()
                # self.get_logger().info(feedback)
            result = nav.getResult()
            print(result)
            # self.get_logger().info(result)
        except KeyboardInterrupt:
            self.get_logger().info("Keyboard interrupt!")
            nav.cancelTask()

    def spin(self):
        while rclpy.ok():
            rclpy.spin_once(self)


def main(args=None):
    rclpy.init(args=args)
    node = NavNode()
    node.set_initial_pose()
    node.get_marker()
    node.spin()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
