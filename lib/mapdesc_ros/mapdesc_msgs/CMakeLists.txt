cmake_minimum_required(VERSION 3.8)
project(mapdesc_msgs)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

find_package(std_msgs REQUIRED)
find_package(diagnostic_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(rclcpp REQUIRED)

find_package(rosidl_default_generators REQUIRED)
ament_export_dependencies(rosidl_default_runtime)

rosidl_generate_interfaces(${PROJECT_NAME} "msg/Area.msg"
  "msg/Box.msg"
  "msg/Dimension.msg"
  "msg/External.msg"
  "msg/LaneEdge.msg"
  "msg/LaneGraph.msg"
  "msg/LaneNode.msg"
  "msg/Map.msg"
  "msg/Marker.msg"
  "msg/Mesh.msg"
  "msg/Path.msg"
  "msg/Wall.msg"
  "srv/MapAreaCreate.srv"
  "srv/MapAreaDelete.srv"
  "srv/MapAreaList.srv"
  "srv/MapAreaUpdate.srv"
  "srv/MapCreate.srv"
  "srv/MapDelete.srv"
  "srv/MapExtCreate.srv"
  "srv/MapExtDelete.srv"
  "srv/MapExtList.srv"
  "srv/MapExtUpdate.srv"
  "srv/MapGet.srv"
  "srv/MapList.srv"
  "srv/MapMarkerCreate.srv"
  "srv/MapMarkerDelete.srv"
  "srv/MapMarkerList.srv"
  "srv/MapMarkerUpdate.srv"
  "srv/MapOverwrite.srv"
  "srv/MapPathCreate.srv"
  "srv/MapPathDelete.srv"
  "srv/MapPathList.srv"
  "srv/MapPathUpdate.srv"
  "srv/MapUpdate.srv"
  "srv/MapWallCreate.srv"
  "srv/MapWallDelete.srv"
  "srv/MapWallList.srv"
  "srv/MapWallUpdate.srv"
  DEPENDENCIES diagnostic_msgs std_msgs geometry_msgs)

ament_package()
