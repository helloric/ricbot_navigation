#!/bin/bash

source /opt/ros/${ROS_DISTRO}/setup.sh
source ${COLCON_WS}/install/setup.sh
exec "$@"
