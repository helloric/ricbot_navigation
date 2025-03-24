#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.task import Future

from visualization_msgs.msg import Marker

from geometry_msgs.msg import Pose, PoseStamped
from mapdesc_msgs.srv import ListMarker


class MarkerInfoNode(Node):
    def __init__(self):
        super().__init__('ricbot_navigation_marker_node')
        self.marker_cli = self.create_client(ListMarker, 'mapdesc/marker/list')
        self.publisher_ = self.create_publisher(Marker, 'helloric_marker', 10)
        # TODO: rewrite to use ROSCrud, and only update on update message,
        # do not repeat all the time
        self.timer = self.create_timer(5.0, self.timer_callback)

    def timer_callback(self):
        self.get_marker()

    def wait_for_service(self, cli):
        for _try in range(10):
            if cli.wait_for_service(timeout_sec=.5):
                self.get_logger().info('Service is available 👍!')
                return True
            self.get_logger().info('service not available, waiting...')
        return False

    def get_marker(self):
        self.wait_for_service(self.marker_cli)
        request = ListMarker.Request()
        future = self.marker_cli.call_async(request)
        future.add_done_callback(self.get_marker_callback)

    def get_marker_callback(self, future: Future):
        marker_data = future.result().marker
        for _id, my_marker in enumerate(marker_data):
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.id = _id
            marker.type = Marker.TEXT_VIEW_FACING
            marker.action = Marker.ADD

            marker.text = my_marker.name

            marker.pose.position = my_marker.pose.position
            marker.pose.orientation.w = 1.0

            # Set the color of the marker
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 1.0

            marker.scale.x = 0.5
            marker.scale.y = 0.5
            marker.scale.z = 0.5
            self.get_logger().info(f'created marker {my_marker.name}')
            self.publisher_.publish(marker)

    def spin(self):
        while rclpy.ok():
            rclpy.spin_once(self)


def main(args=None):
    rclpy.init(args=args)
    node = MarkerInfoNode()
    node.spin()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
