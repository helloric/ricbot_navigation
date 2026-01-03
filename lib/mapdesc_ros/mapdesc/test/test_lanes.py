from mapdesc.model import LaneGraph


def test_lane_from_dict():
    graph_data = {
        'nodes': [
            {'position': [1, 1, 1]},
            {'position': [2, 2, 2]},
            {'position': [3, 3, 3]}
        ],
        'edges': [
            {'edge_type': 0, 'source': 0, 'target': 1},
            {'edge_type': 0, 'source': 1, 'target': 2}
        ]
    }
    graph = LaneGraph(**graph_data)
    assert graph.nodes[0].position.x == 1
    assert graph.edges[1].target.name == 'node_2'
    idx = 0
    for node in graph_data['nodes']:
        node['name'] = f'node_{idx}'
        idx += 1
    assert dict(graph) == graph_data
