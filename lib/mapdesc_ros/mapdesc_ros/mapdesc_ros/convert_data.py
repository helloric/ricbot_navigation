from geometry_msgs.msg import Pose as PoseMsg
from geometry_msgs.msg import Point as PointMsg
from geometry_msgs.msg import Vector3 as Vector3Msg
from geometry_msgs.msg import Quaternion as QuaternionMsg

from mapdesc_msgs.msg import Area as AreaMsg
from mapdesc_msgs.msg import Box as BoxMsg
from mapdesc_msgs.msg import Map as MapMsg
from mapdesc_msgs.msg import Marker as MarkerMsg
from mapdesc_msgs.msg import Mesh as MeshMsg

# mapdesc
from mapdesc.model.geom.pose import Pose
from mapdesc.model.geom.vector3 import Vector3
from mapdesc.model.geom.quaternion import Quaternion

from mapdesc.model.geom.box import Box
from mapdesc.model.geom.mesh import Mesh

from mapdesc.model.area import Area
from mapdesc.model.map import Map
from mapdesc.model.marker import Marker


def pose_ros_to_mapdesc(pose: PoseMsg) -> Pose:
    return Pose(
        position=Vector3(
            x=pose.position.x,
            y=pose.position.y,
            z=pose.position.z),
        orientation=Quaternion(
            x=pose.orientation.x,
            y=pose.orientation.y,
            z=pose.orientation.z,
            w=pose.orientation.w)
    )


def pose_mapdesc_to_ros(pose: Pose) -> PoseMsg:
    return PoseMsg(
        position=PointMsg(
            x=float(pose.position.x),
            y=float(pose.position.y),
            z=float(pose.position.z)),
        orientation=QuaternionMsg(
            x=float(pose.orientation.x),
            y=float(pose.orientation.y),
            z=float(pose.orientation.z),
            w=float(pose.orientation.w))
    )


def mesh_ros_to_mapdesc(data: MeshMsg | BoxMsg) -> Mesh | Box:
    """Convert mapdesc_msg/MeshBox to mapdesc.model.Mesh/mapdesc.model.Box
    """
    pose = pose_ros_to_mapdesc(data.pose)
    if isinstance(data, MeshMsg):
        return Mesh(
            pose=pose,
            polygons=data.polygons
        )
    elif isinstance(data, BoxMsg):
        return Box(
            pose=pose,
            size=data.size
        )
    else:
        raise RuntimeError('Not a valid ros mapdesc_msg mesh/box')


def mesh_mapdesc_to_ros(data: Mesh | Box) -> MeshMsg | BoxMsg:
    """Convert mapdesc_msg/MeshBox to mapdesc.model.Mesh/mapdesc.model.Box
    """
    if isinstance(data, Mesh):
        return MeshMsg(
            pose=pose_mapdesc_to_ros(data.pose),
            polygons=[Vector3Msg(
                x=float(p.x), y=float(p.y), z=0.0)
                for p in data.polygons]
        )
    elif isinstance(data, Box):
        return BoxMsg(
            pose=pose_mapdesc_to_ros(data.pose)
        )
    else:
        raise RuntimeError('Not a valid mapdesc mesh/box geometry')


def area_ros_to_mapdesc(area: AreaMsg) -> Area:
    assert isinstance(area, AreaMsg)
    return Area(
        name=area.name,
        type=area.type,
        area_type=area.area_type,
        color=area.color,
        data=mesh_ros_to_mapdesc(area.data)
    )


def area_mapdesc_to_ros(area: Area) -> AreaMsg:
    assert isinstance(area, Area)
    return AreaMsg(
        name=area.name,
        type=area.type,
        area_type=area.area_type,
        color=area.color,
        data=mesh_mapdesc_to_ros(area.data)
    )


def marker_ros_to_mapdesc(marker: MarkerMsg) -> Marker:
    return Marker(
        name=marker.name,
        pose=pose_ros_to_mapdesc(marker.pose),
        color=marker.color,
        type=marker.type,
        radius=marker.radius
    )


def marker_mapdesc_to_ros(marker: Marker) -> MarkerMsg:
    return MarkerMsg(
        name=marker.name,
        pose=pose_mapdesc_to_ros(marker.pose),
        color=marker.color,
        type=marker.type,
        radius=float(marker.radius)
    )


def map_ros_to_mapdesc(_map: Map):
    return MapMsg(
        name=_map.name,
        marker=[marker_mapdesc_to_ros(m) for m in _map.marker],
        # area=[area_mapdesc_to_ros(a) for a in _map.area]
    )
