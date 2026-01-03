import math


def dot_product(p1, p2, p3):
    """calculates the dot-product of two vectors from 3 points.

    Useful to determine if it is a right angle."""
    v1 = (p2.x - p1.x, p2.y - p1.y)
    v2 = (p3.x - p2.x, p3.y - p2.y)
    return v1[0] * v2[0] + v1[1] * v2[1]


def calculate_slope(p1, p2):
    """calculate slope of line between 2 points."""
    if p1.x == p2.x:
        return float('inf')  # Use infinity to represent vertical lines
    return (p2.y - p1.y) / (p2.x - p1.x)


def bounding_box(points: list) -> list:
    """get bounding box around all given points."""
    x_min = min([p[0] for p in points])
    y_min = min([p[1] for p in points])
    x_max = max([p[0] for p in points])
    y_max = max([p[1] for p in points])
    return x_min, y_min, x_max, y_max


def ccw_sort(points: list):
    """sort points counter-clockwise.

    We assume the coordinates are taken from the center and calculate the
    degree of each point to order by angle.
    """
    points_distance = [
        (
            math.atan2(p.x, p.y) % (math.pi * 2),
            p
        ) for p in points
    ]
    points_distance.sort(key=lambda x: x[0], reverse=True)
    return [p[1] for p in points_distance]


def image_dimensions(_map) -> list:
    """Get image dimensions for SVG and PNG export."""
    if _map.size.width > 1 and _map.size.length > 1:
        return _map.size.width, _map.size.length, 0, 0
    else:
        points = [p for w in _map.wall for p in w.local_points()]
        if _map.marker:
            # subtract and add radius to get top-left and bottom-right
            # corner of the marker
            points += [m.pose.position + m.radius for m in _map.marker]
            points += [m.pose.position - m.radius for m in _map.marker]
        if _map.lane_graph:
            points += [n.position for n in _map.lane_graph.nodes]
        if not points:
            print('WARN: no obstacles given to calculate bounding box')
            return 0, 0, 0, 0
        x_min, y_min, x_max, y_max = bounding_box(points)
        # image size is calculated by the points, we set the position
        # of the image by the top-left and bottom-right bounding box
        # that the points form. Only works if we have at least 2 points.
        width, height = x_max - x_min, y_max - y_min
        # we move all points between min and max, so we need to move all
        # points by that (shift all points by an offset so they are inside
        # the image)
        return width, height, -x_min, -y_min


def euler_to_quaternion(roll: float, pitch: float, yaw: float) -> set:
    # roll (X), pitch (Y), yaw (Z),
    # Abbreviations for the various angular functions based on
    # https://en.wikipedia.org/wiki/
    #     Conversion_between_quaternions_and_Euler_angles
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    return (
        sr * cp * cy - cr * sp * sy,  # x
        cr * sp * cy + sr * cp * sy,  # y
        cr * cp * sy - sr * sp * cy,  # z
        cr * cp * cy + sr * sp * sy   # w
    )


def quaternion_to_euler(x: float, y: float, z: float, w: float):
    # roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    # math.asin has to be between -1 and 1, so we return 90°(π/2) as limit
    sinp = max(-1, sinp)
    sinp = min(1, sinp)
    pitch = math.asin(sinp)

    # yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw
