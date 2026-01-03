try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
import numpy as np
from ..util import image_dimensions
import logging

logger = logging.getLogger(__name__)


def rgb_to_bgr(rgb):
    return [rgb[2], rgb[1], rgb[0]]


def save_png(_map, output_file, obstacles_only=False):
    if not CV2_AVAILABLE:
        raise RuntimeError('Can not save as PNG, OpenCV2 not avaialbe')
    width, height, offset_x, offset_y = image_dimensions(_map)
    res = _map.resolution
    img = np.zeros((int(height / res), int(width / res), 3), dtype=np.uint8)
    img.fill(255)
    if _map.area and not obstacles_only:
        for area in _map.area:
            pts = [
                (
                    int((p.x + offset_x) / res),
                    int((p.y + offset_y) / res)
                ) for p in area.local_points()
            ]
            pts = np.array(
                [pts],
                dtype=np.int32)
            color = rgb_to_bgr(area.color) if area.color \
                else [255, 100, 100]
            cv2.fillPoly(img, [pts], color)

    for wall in _map.wall:
        pts = [
            (
                int((p.x + offset_x) / res),
                int((p.y + offset_y) / res)
            ) for p in wall.local_points()
        ]
        pts = np.array(
            [pts],
            dtype=np.int32)
        color = [0, 0, 0]
        cv2.fillPoly(img, [pts], color)

    if _map.lane_graph and not obstacles_only:
        for edge in _map.lane_graph.edges:
            s = edge.source.position
            t = edge.target.position
            x1 = int((s.x + offset_x) / res)
            y1 = int((s.y + offset_y) / res)
            x2 = int((t.x + offset_x) / res)
            y2 = int((t.y + offset_y) / res)
            thickness = 1
            color = (0, 0, 255)
            start = (x1, y1)
            end = (x2, y2)
            cv2.line(img, start, end, color, thickness)

    if not obstacles_only:
        for marker in _map.marker:
            pos = marker.pose.position
            x = int((pos.x + offset_x) / res)
            y = int((pos.y + offset_y) / res)
            color = rgb_to_bgr(marker.color) if marker.color else (0, 0, 255)
            radius = (marker.radius if marker.radius else 1.0) / res
            cv2.circle(img, (x, y), int(radius), color)
    if width == 0 or height == 0:
        logger.error(
            'Can not safe image %s, invalid dimensions %i:%i',
            output_file, width, height)
        return
    cv2.imwrite(str(output_file), img)
