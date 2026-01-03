from mapdesc.model.geom.mesh import Mesh


def test_recenter():
    mesh = Mesh(
        polygons=[
            (1, 2),
            (11, 2),
            (11, 11),
            (1, 11)
        ]
    )
    mesh.recenter()
    assert mesh.pose.position.x == 6
    assert mesh.pose.position.y == 6.5
    assert mesh.pose.position.z == 0

    assert mesh.polygons[0].x == -5
    assert mesh.polygons[0].y == -4.5
