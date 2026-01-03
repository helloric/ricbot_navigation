# lane inspired by
# https://github.com/open-rmf/rmf_building_map_msgs/
from dataclasses import dataclass, field
from .geom.vector3 import Vector3


BIDIRECTIONAL = 0
UNIDIRECTIONAL = 1


@dataclass
class LaneGraph:
    nodes: list = field(default_factory=list)  # list of LaneNode
    edges: list = field(default_factory=list)  # list of edges
    _last_new_number: int = 0  # used to optimize generation of unique ids

    def _unique_node_name(self):
        """Generate a new unique name for a node."""
        known_names = [n.name for n in self.nodes]
        while True:
            new_name = f'node_{self._last_new_number}'
            if new_name in known_names:
                self._last_new_number += 1
            else:
                return new_name

    def __post_init__(self):
        self.nodes = [
            LaneNode(**n) if isinstance(n, dict) else n
            for n in self.nodes
        ]
        self.edges = [
            LaneEdge(**e) if isinstance(e, dict) else e
            for e in self.edges
        ]
        # generate unique id for all nodes if necessary
        for node in self.nodes:
            if not node.name:
                node.name = self._unique_node_name()
        for edge in self.edges:
            edge.graph = self
            edge.update_nodes()

    def __iter__(self):
        yield ('nodes', [dict(node) for node in self.nodes])
        yield ('edges', [dict(edge) for edge in self.edges])


@dataclass
class LaneNode:
    # node in the navigation graph (similar to marker.Marker)
    position: Vector3 = field(default_factory=Vector3)
    name: str = None
    # additional information about this node that the user can define
    # as key-value pair
    params: dict = field(default_factory=dict)

    def __post_init__(self):
        self.position = Vector3.from_any(self.position)

    def __iter__(self):
        yield ('name', self.name)
        yield ('position', list(self.position))
        if self.params:
            yield ('params', self.params)


@dataclass
class LaneEdge:
    source: LaneNode = None
    target: LaneNode = None
    graph: LaneGraph = None

    # Unidirectional lanes only allow driving from source to target
    # not from target to source
    edge_type: int = BIDIRECTIONAL  # enum UNIDIRECTIONAL or BIDIRECTIONAL

    # optional name for the edge
    name: str = None

    # additional information about this edge that the user can define
    params: dict = None

    def update_nodes(self):
        """Set source and target nodes based on their poisitons
        in the graph.
        """
        if isinstance(self.source, int):
            self.source = self.graph.nodes[self.source]
        if isinstance(self.target, int):
            self.target = self.graph.nodes[self.target]

    def __iter__(self):
        yield ('source', self.graph.nodes.index(self.source))
        yield ('target', self.graph.nodes.index(self.target))
        if self.name:
            yield ('name', self.name)
        if self.params:
            yield ('params', self.params)
        yield ('edge_type', self.edge_type)
