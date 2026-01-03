import json
from mapdesc.model import Marker


def test_to_json():
    model = Marker()
    assert json.dumps(dict(model)) == '{"name": "new marker", '\
        '"pose": {"orientation": [0.0, 0.0, 0.0, 1.0], "position": '\
        '[0.0, 0.0, 0.0]}, "color": [255, 50, 50], "radius": 1.0, '\
        '"type": "point"}'
