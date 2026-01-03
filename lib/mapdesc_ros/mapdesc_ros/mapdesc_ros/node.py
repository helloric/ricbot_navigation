from pathlib import Path

import rclpy

from mapdesc.load.yaml import load_yaml

from .convert_data import map_ros_to_mapdesc
from .map_desc import MapNode


class MapDescNode(MapNode):
    def __init__(self):
        super().__init__('mapdesc_node')
        self.declare_parameter('map_yaml', '')
        self.load_yaml_file()

    def load_yaml_file(self):
        """Load yaml files and set as data"""
        map_yaml = str(self.get_parameter('map_yaml').value)
        if not map_yaml or map_yaml == '':
            self.get_logger().warning('Map not set!')
            return
        if not Path(map_yaml).exists():
            self.get_logger().warning(f'Map does not exist: {map_yaml}')
            return
        map_mapdesc = load_yaml(map_yaml)
        map_msg = map_ros_to_mapdesc(map_mapdesc)
        self.data[map_msg.name] = map_msg
        self.get_logger().info(f'Loaded map: {map_msg.name}')


def main(args=None):
    rclpy.init(args=args)
    node = MapDescNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
