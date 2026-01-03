ARG ROS_DISTRO=jazzy
FROM ros:${ROS_DISTRO}

RUN apt update
RUN apt install -y \
    ros-${ROS_DISTRO}-navigation2 \
    ros-${ROS_DISTRO}-nav2-bringup \
    # ros-${ROS_DISTRO}-slam-toolbox \
    # ros-${ROS_DISTRO}-nav2-amcl \
    # ros-${ROS_DISTRO}-map-server \
    # ros-${ROS_DISTRO}-robot-localization \
    && rm -rf /var/lib/apt/lists/*


ENV COLCON_WS=/root/colcon_ws
ENV COLCON_WS_SRC=/root/colcon_ws/src

COPY ./docker/entrypoint.bash /entrypoint.bash
RUN chmod +x /entrypoint.bash
ENTRYPOINT ["/entrypoint.bash"]

COPY ./ ${COLCON_WS_SRC}/ricbot_navigation
COPY ./lib/mapdesc_ros ${COLCON_WS_SRC}/mapdesc_ros


RUN cd ${COLCON_WS}\
    && . /opt/ros/${ROS_DISTRO}/setup.sh\
    && colcon build --packages-select ricbot_navigation mapdesc_msgs mapdesc_ros

CMD ["ros2", "launch", "ricbot_navigation", "ricbot_nav.launch.py"]
