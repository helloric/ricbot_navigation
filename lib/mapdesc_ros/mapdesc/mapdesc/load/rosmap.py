# load data description
import logging
import math
from pathlib import Path
import yaml
try:
    import cv2
    from imutils import contours
    import imutils
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
from ..model import Map, Wall
from ..model.geom import Box, Mesh, Dimension, Vector2, Vector3

logger = logging.getLogger(__name__)


def _shapes_from_image(res, path):
    """Generate list of x, y shapes from contours of an image
    """
    if not CV2_AVAILABLE:
        raise RuntimeError('Can not modify image, OpenCV2 not available')
    img = cv2.imread(str(path))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_img, 20, 100)
    cnts = cv2.findContours(
        edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    (cnts, _) = contours.sort_contours(cnts)
    shapes = []
    for cnt in cnts:
        # approx = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)

        coords = [(a[0][0], a[0][1]) for a in approx]
        shapes.append(coords)
    return shapes


def load_rosmap(yaml_file, height=2.0):
    """Find contours in an image and create map from it.
    """
    _map = Map()
    _map.wall = []
    with open(yaml_file, encoding='utf-8') as f:
        data = yaml.safe_load(f)
        res = data['resolution']
        _map.origin.position = Vector3.from_any(data['origin'])
        # get data from image
        img_path = Path(yaml_file).absolute().parent / data['image']
        shapes = _shapes_from_image(res, img_path)
        for coords in shapes:
            points = [(x * res, y * res) for x, y in coords]
            center = Mesh.calculate_position([
                Vector2(x, y) for x, y in points])
            if len(points) == 4 and \
                math.isclose(
                    math.dist(points[0], points[1]),
                    math.dist(points[2], points[3])) and \
                math.isclose(
                    math.dist(points[1], points[2]),
                    math.dist(points[3], points[0])):

                wall = Wall(data=Box())

                center_top = (points[0][0] + points[1][0]), \
                    (points[0][1] + points[1][1])
                center_btm = (points[2][0] + points[3][0]), \
                    (points[2][1] + points[3][1])
                width = math.dist(center_top, center_btm) / 2

                center_lft = (points[1][0] + points[2][0]), \
                    (points[1][1] + points[2][1])
                center_rgt = (points[3][0] + points[0][0]), \
                    (points[3][1] + points[0][1])
                length = math.dist(center_lft, center_rgt) / 2
                wall.data.size = Dimension(width, length, height)
            else:
                wall = Wall(data=Mesh())
                wall.data.polygons = [(
                    Vector2(*p))-center for p in points]
                wall.data.size = Dimension(1.0, 1.0, height)
            # our coordinates are relative (we subtracted center earlier so)
            # we have to save it as the walls position
            wall.data.pose.position = center
            _map.wall.append(wall)
    if not _map.wall:
        logger.error('No walls found, aborting!')
        return None
    return _map
