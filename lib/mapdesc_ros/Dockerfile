ARG ROS_DISTRO
FROM d-reg.hb.dfki.de/robot-config/ros-pip-pytest:${ROS_DISTRO}-0.0.1

ENV COLCON_WS=/root/colcon_ws
ENV COLCON_WS_SRC=/root/colcon_ws/src

COPY ./mapdesc/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY ./mapdesc /opt/mapdesc
WORKDIR /opt/mapdesc
RUN pip3 install .

WORKDIR ${COLCON_WS}
COPY ./mapdesc_ros ${COLCON_WS_SRC}/mapdesc_ros
COPY ./mapdesc_msgs ${COLCON_WS_SRC}/mapdesc_msgs
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && colcon build

COPY ./run_tests.bash /run_tests.bash
RUN chmod +x /run_tests.bash
CMD [ "bash", "-c", "/run_tests.bash"]