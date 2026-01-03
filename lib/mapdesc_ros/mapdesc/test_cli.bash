#!/bin/bash
mapdesc yaml test/yaml/simple_walls.yaml sdf ./generated/sdf/test1
mapdesc rosmap test/map/mallmap.yaml yaml ./generated/mallmap.yml
mapdesc rosmap test/map/mallmap.yaml yaml -b ./generated/mallmap_bounding_box.yml
mapdesc rosmap test/map/mallmap.yaml sdf ./generated/sdf/test2
mapdesc rosmap test/map/mallmap.yaml png ./generated/test1.png
mapdesc yaml test/yaml/hdp_2_agents_map.yml rosmap ./generated/hdp_rosmap.yaml
mapdesc yaml --recenter test/yaml/demonstrator_map.yml yaml ./generated/demonstrator_map_recenter.yml
mapdesc yaml --boxify test/yaml/demonstrator_map.yml yaml ./generated/demonstrator_map_box.yml
# mapdesc osm 53.0762098 8.8075270 80 earth svg ./generated/bremen_city.svg
# mapdesc osm 53.0762098 8.8075270 80 earth yaml ./generated/bremen_city.yml