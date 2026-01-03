import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from mapdesc_msgs.srv import \
    MapCreate, \
    MapDelete, \
    MapGet, \
    MapList, \
    MapUpdate, \
    MapOverwrite, \
    MapMarkerCreate, \
    MapMarkerDelete, \
    MapMarkerList, \
    MapMarkerUpdate, \
    MapAreaCreate, \
    MapAreaDelete, \
    MapAreaList, \
    MapAreaUpdate, \
    MapWallCreate, \
    MapWallDelete, \
    MapWallList, \
    MapWallUpdate, \
    MapPathCreate, \
    MapPathDelete, \
    MapPathList, \
    MapPathUpdate, \
    MapExtCreate, \
    MapExtDelete, \
    MapExtList, \
    MapExtUpdate
from mapdesc_msgs.msg import \
    Area, \
    External, \
    Map, \
    Marker, \
    Path, \
    Wall

# This file has initially been generated using ROSCRUD

PREFIX = 'mapdesc'

# ROS CRUD services
MAP_CREATE = f'{PREFIX}/create'
MAP_DELETE = f'{PREFIX}/delete'
MAP_GET = f'{PREFIX}/get'
MAP_LIST = f'{PREFIX}/list'
MAP_UPDATE = f'{PREFIX}/update'
MAP_OVERWRITE = f'{PREFIX}/overwrite'
MAP_MARKER_CREATE = f'{PREFIX}/marker/create'
MAP_MARKER_DELETE = f'{PREFIX}/marker/delete'
MAP_MARKER_LIST = f'{PREFIX}/marker/list'
MAP_MARKER_UPDATE = f'{PREFIX}/marker/update'
MAP_AREA_CREATE = f'{PREFIX}/area/create'
MAP_AREA_DELETE = f'{PREFIX}/area/delete'
MAP_AREA_LIST = f'{PREFIX}/area/list'
MAP_AREA_UPDATE = f'{PREFIX}/area/update'
MAP_WALL_CREATE = f'{PREFIX}/wall/create'
MAP_WALL_DELETE = f'{PREFIX}/wall/delete'
MAP_WALL_LIST = f'{PREFIX}/wall/list'
MAP_WALL_UPDATE = f'{PREFIX}/wall/update'
MAP_PATH_CREATE = f'{PREFIX}/path/create'
MAP_PATH_DELETE = f'{PREFIX}/path/delete'
MAP_PATH_LIST = f'{PREFIX}/path/list'
MAP_PATH_UPDATE = f'{PREFIX}/path/update'
MAP_EXT_CREATE = f'{PREFIX}/ext/create'
MAP_EXT_DELETE = f'{PREFIX}/ext/delete'
MAP_EXT_LIST = f'{PREFIX}/ext/list'
MAP_EXT_UPDATE = f'{PREFIX}/ext/update'


# ROS Topics to inform data change
MAP_ADDED = f'{PREFIX}/added'
MAP_CHANGED = f'{PREFIX}/changed'
MAP_REMOVED = f'{PREFIX}/removed'
MAP_MARKER_ADDED = f'{PREFIX}/marker/added'
MAP_MARKER_CHANGED = f'{PREFIX}/marker/changed'
MAP_MARKER_REMOVED = f'{PREFIX}/marker/removed'
MAP_AREA_ADDED = f'{PREFIX}/area/added'
MAP_AREA_CHANGED = f'{PREFIX}/area/changed'
MAP_AREA_REMOVED = f'{PREFIX}/area/removed'
MAP_WALL_ADDED = f'{PREFIX}/wall/added'
MAP_WALL_CHANGED = f'{PREFIX}/wall/changed'
MAP_WALL_REMOVED = f'{PREFIX}/wall/removed'
MAP_PATH_ADDED = f'{PREFIX}/path/added'
MAP_PATH_CHANGED = f'{PREFIX}/path/changed'
MAP_PATH_REMOVED = f'{PREFIX}/path/removed'
MAP_EXT_ADDED = f'{PREFIX}/ext/added'
MAP_EXT_CHANGED = f'{PREFIX}/ext/changed'
MAP_EXT_REMOVED = f'{PREFIX}/ext/removed'


class MapNode(Node):
    def __init__(self, name=None):
        self.name = name if name else self.__class__.__name__
        super().__init__(self.name)

        # all map by name
        self.data = {}

        # overwrite map in data if another map
        # with name is received or log an error and ignore
        # the new name
        self.allow_overwrite = False

        # name of the id
        self.id_name = 'name'

        # setup services for data manipulation
        self.init_ros()

    def init_ros(self):
        self.added_pub = self.create_publisher(
            Map, MAP_ADDED, 10)
        self.changed_pub = self.create_publisher(
            Map, MAP_CHANGED, 10)
        self.removed_pub = self.create_publisher(
            String, MAP_REMOVED, 10)
        self.marker_added_pub = self.create_publisher(
            Marker, MAP_MARKER_ADDED, 10)
        self.marker_changed_pub = self.create_publisher(
            Marker, MAP_MARKER_CHANGED, 10)
        self.marker_removed_pub = self.create_publisher(
            String, MAP_MARKER_REMOVED, 10)
        self.area_added_pub = self.create_publisher(
            Area, MAP_AREA_ADDED, 10)
        self.area_changed_pub = self.create_publisher(
            Area, MAP_AREA_CHANGED, 10)
        self.area_removed_pub = self.create_publisher(
            String, MAP_AREA_REMOVED, 10)
        self.wall_added_pub = self.create_publisher(
            Wall, MAP_WALL_ADDED, 10)
        self.wall_changed_pub = self.create_publisher(
            Wall, MAP_WALL_CHANGED, 10)
        self.wall_removed_pub = self.create_publisher(
            String, MAP_WALL_REMOVED, 10)
        self.path_added_pub = self.create_publisher(
            Path, MAP_PATH_ADDED, 10)
        self.path_changed_pub = self.create_publisher(
            Path, MAP_PATH_CHANGED, 10)
        self.path_removed_pub = self.create_publisher(
            String, MAP_PATH_REMOVED, 10)
        self.ext_added_pub = self.create_publisher(
            External, MAP_EXT_ADDED, 10)
        self.ext_changed_pub = self.create_publisher(
            External, MAP_EXT_CHANGED, 10)
        self.ext_removed_pub = self.create_publisher(
            String, MAP_EXT_REMOVED, 10)
        self.create_srv = self.create_service(
            MapCreate, MAP_CREATE,
            self.on_create)
        self.delete_srv = self.create_service(
            MapDelete, MAP_DELETE,
            self.on_delete)
        self.get_srv = self.create_service(
            MapGet, MAP_GET,
            self.on_get)
        self.list_srv = self.create_service(
            MapList, MAP_LIST,
            self.on_list)
        self.update_srv = self.create_service(
            MapUpdate, MAP_UPDATE,
            self.on_update)
        self.overwrite_srv = self.create_service(
            MapOverwrite, MAP_OVERWRITE,
            self.on_overwrite)
        self.create_marker_srv = self.create_service(
            MapMarkerCreate, MAP_MARKER_CREATE,
            self.on_attr_create('marker'))
        self.delete_marker_srv = self.create_service(
            MapMarkerDelete, MAP_MARKER_DELETE,
            self.on_attr_delete('marker'))
        self.list_marker_srv = self.create_service(
            MapMarkerList, MAP_MARKER_LIST,
            self.on_attr_list('marker'))
        self.update_marker_srv = self.create_service(
            MapMarkerUpdate, MAP_MARKER_UPDATE,
            self.on_attr_update('marker'))
        self.create_area_srv = self.create_service(
            MapAreaCreate, MAP_AREA_CREATE,
            self.on_attr_create('area'))
        self.delete_area_srv = self.create_service(
            MapAreaDelete, MAP_AREA_DELETE,
            self.on_attr_delete('area'))
        self.list_area_srv = self.create_service(
            MapAreaList, MAP_AREA_LIST,
            self.on_attr_list('area'))
        self.update_area_srv = self.create_service(
            MapAreaUpdate, MAP_AREA_UPDATE,
            self.on_attr_update('area'))
        self.create_wall_srv = self.create_service(
            MapWallCreate, MAP_WALL_CREATE,
            self.on_attr_create('wall'))
        self.delete_wall_srv = self.create_service(
            MapWallDelete, MAP_WALL_DELETE,
            self.on_attr_delete('wall'))
        self.list_wall_srv = self.create_service(
            MapWallList, MAP_WALL_LIST,
            self.on_attr_list('wall'))
        self.update_wall_srv = self.create_service(
            MapWallUpdate, MAP_WALL_UPDATE,
            self.on_attr_update('wall'))
        self.create_path_srv = self.create_service(
            MapPathCreate, MAP_PATH_CREATE,
            self.on_attr_create('path'))
        self.delete_path_srv = self.create_service(
            MapPathDelete, MAP_PATH_DELETE,
            self.on_attr_delete('path'))
        self.list_path_srv = self.create_service(
            MapPathList, MAP_PATH_LIST,
            self.on_attr_list('path'))
        self.update_path_srv = self.create_service(
            MapPathUpdate, MAP_PATH_UPDATE,
            self.on_attr_update('path'))
        self.create_ext_srv = self.create_service(
            MapExtCreate, MAP_EXT_CREATE,
            self.on_attr_create('ext'))
        self.delete_ext_srv = self.create_service(
            MapExtDelete, MAP_EXT_DELETE,
            self.on_attr_delete('ext'))
        self.list_ext_srv = self.create_service(
            MapExtList, MAP_EXT_LIST,
            self.on_attr_list('ext'))
        self.update_ext_srv = self.create_service(
            MapExtUpdate, MAP_EXT_UPDATE,
            self.on_attr_update('ext'))

    def _get(self, _name):
        if _name not in self.data:
            return None
        return self.data[_name]

    def on_attr_create(self, attr: str):
        def _create(request, response):
            _name = request.name
            elem = self._get(_name)
            if not elem:
                self.get_logger().error(
                    f'Can not get map "{_name}"')
                response.success = False
                return response
            getattr(elem, attr).append(request.item)
            getattr(self, f'{attr}_added_pub').publish(request.item)
            response.success = True
            return response
        return _create

    def on_attr_list(self, attr: str):
        def _list(request, response):
            _name = request.name
            elem = self._get(_name)
            data = getattr(elem, attr, [])
            setattr(response, attr, data)
            return response
        return _list

    def on_attr_update(self, attr: str):
        def _update(request, response):
            _name = request.name
            elem = self._get(_name)
            idx = request.index
            getattr(elem, attr)[idx] = request.item
            getattr(self, f'{attr}_changed_pub').publish(request.item)
            response.success = True
            return response
        return _update

    def on_attr_delete(self, attr: str):
        def _delete(request, response):
            _name = request.name
            elem = self._get(_name)
            idx = request.index
            item = getattr(elem, attr)[idx]
            getattr(elem, attr).remove(idx)
            getattr(self, f'{attr}_removed_pub').publish(item)
            return response
        return _delete

    def on_create(self, request, response):
        elem = request.map
        _name = elem.name
        if self._get(request.name) and not self.allow_overwrite:
            self.get_logger().error(
                'Can not create, name '
                f'{_name} already exists.')
            response.success = False
            return response
        self.data[_name] = elem
        self.added_pub.publish(elem)
        response.success = True
        return response

    def on_delete(self, request, response):
        _name = request.name
        if not self._get(_name):
            self.get_logger().error(
                'Can not delete, name '
                f'{_name} does not exist.')
            response.success = False
            return response
        del self.data[_name]
        self.removed_pub.publish(_name)
        response.success = True
        return response

    def on_get(self, request, response):
        _name = request.name
        elem = self._get(_name)
        if elem:
            response.map = elem
            return response
        else:
            self.get_logger().info(
                'Mission ID '
                f'{request.name} does not exist!')
            return response

    def on_list(self, request, response):
        response.map = list(self.data.values())
        return response

    def on_update(self, request, response):
        elem = request.map
        _name = elem.name
        if not self._get(request.name):
            self.get_logger().error(
                'Can not update, name: '
                f'{_name} does not exist.')
            response.success = False
            return response
        self.data[_name] = elem
        self.changed_pub.publish(elem)
        response.success = True
        return response

    def on_overwrite(self, request, response):
        """allow overwrite map in self.data"""
        self.allow_overwrite = request.allow_overwrite
        return response


def main(args=None):
    rclpy.init(args=args)

    node = MapNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
