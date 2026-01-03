# Basic tutorial
mapdesc provides a command line interface (cli) as well as a Python API.

In this first tutorial we will look at the CLI, for the API take a look at [02: Basic API usage](02_basic_api_usage.md)

## Bring a map to Gazebo simulation
mapdesc allows you convert data from one source to another. 

A typical use case would be to create an SDF-file form a recorded ROS map, so you could easily create a simulation environment of your recorded map for testing your robot in simulation first.

First store your ROS 2 map using the [ROS map_server](http://wiki.ros.org/map_server) for ROS 1 or ROS 2. You can then load the map and export it to SDF.

Replace `your_ros_map.yml` with the filename of the file from your map.
```bash
mapdesc rosmap your_ros_map.yml sdf ./generated/sdf/test2
```

Then you could either copy the exported SDF to your `.gazebo/models`-folder or just run gazebo with the `GAZEBO_MODEL_PATH` set to the parent folder of where you generated the sdf-file:
```bash
GAZEBO_MODEL_PATH=/home/user/mapdesc/generated/sdf/ gazebo
```
in Gazebo click on the "Insert"-tab. There you should see the model that you can insert in your gazebo world.

## Load map to ROS map_server
1. Generate a ROSMap for a mapdesc description (or import it from another format like a YAML)
1. You can then use the YAML-file in your ROS 2 nav2 as part of the [map-server parameter](https://navigation.ros.org/configuration/packages/configuring-map-server.html#map-server-parameters)

<!--
TODO: create screenshots and example Docker environment.

TODO: Create a map from map-editor description and load it on the map-server of a robot.


# Different data sources
## Working with indoorGML 
### Import
### Export

## Working with IFC
To load and safe IFC we are using the (IFC Open Shell)[https://ifcopenshell.org/].

### Import
TODO: import simple IFC-file e.g. https://www.ifcwiki.org/images/e/e3/AC20-FZK-Haus.ifc

### Export
TODO: load simple description of a house, export it and show it in an IFC online viewer

## Working with openstreetmap (buildings) 
This downloads JSON data from (osmbuildings.org)[https://osmbuildings.org], which might be pretty big. We recommend you use a proxy-server to cache the data.

### Import
TODO: How to convert coordinates to URL? maybe an example with coordinates from openstreetmap.org
-->