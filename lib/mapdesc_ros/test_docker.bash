# run tests on local machine (no gitlab ci, but in a docker container)
docker compose build ros_with_pip
docker compose build mapdesc_ros
docker compose run mapdesc_ros